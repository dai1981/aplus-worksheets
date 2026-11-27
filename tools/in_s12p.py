# -*- coding: utf-8 -*-
"""Class 12 Physics (NCERT Physics Part I and II, 14 chapters): question makers and UNITS()."""
import math
from in_sci import _R
from in_srs import ch, A, N, B, SU, pairs, tq, nf, al_phys as P
import in_s11c

PH = "Physics"
KC, E0, MU0, QE, ME, H, C = 9e9, 8.85e-12, 4 * math.pi * 1e-7, 1.6e-19, 9.1e-31, 6.63e-34, 3e8


def ri(a, b, step=1):
    return _R[0].randrange(a, b + 1, step)


def rf(a, b, step):
    return round(_R[0].randint(round(a / step), round(b / step)) * step, 6)


def K(f, *kinds):
    return lambda: f(ch(kinds))


def mu(x):
    """microcoulombs as text"""
    return "%s μC" % nf(x)


# =================================================================== 1 electric charges and fields
def ec(k=None):
    k = k or ch(["n", "q", "F", "E", "flux", "line", "dip", "tq", "sheet"])
    if k == "n":
        q = rf(0.5, 9.5, 0.5) * 10 ** -ri(6, 12)
        return N("How many electrons must be removed from a body to give it a charge of +%s C? (e = 1.6 × 10⁻¹⁹ C)" % nf(q), q / QE, [q * QE, QE / q, q / QE / 2], "",
                 "q = ne, so n = %s ÷ (1.6 × 10⁻¹⁹) = <b>%s</b>." % (nf(q), nf(q / QE)))
    if k == "q":
        n = ri(2, 9) * 10 ** ri(10, 16)
        return N("A body gains %s electrons. What is its charge? (e = 1.6 × 10⁻¹⁹ C)" % nf(n), -n * QE, [n * QE, -n / QE, -n * QE * 10], " C", "q = −ne = −%s × 1.6 × 10⁻¹⁹ = <b>%s C</b> (negative)." % (nf(n), nf(-n * QE)))
    if k == "F":
        q1, q2, r = ri(1, 9), ri(1, 9), rf(0.05, 0.5, 0.05)
        F = KC * q1 * q2 * 1e-12 / r / r
        return N("Two point charges of %d μC and %d μC are %s m apart in air. What is the force between them? (1/4πε₀ = 9 × 10⁹ N m² C⁻²)" % (q1, q2, nf(r)), F,
                 [F * r, KC * q1 * q2 * 1e-6 / r / r, F / 2], " N", "F = kq₁q₂/r² = 9 × 10⁹ × %d × 10⁻⁶ × %d × 10⁻⁶ ÷ %s² = <b>%s N</b>." % (q1, q2, nf(r), nf(F)))
    if k == "E":
        q, r = ri(1, 9), rf(0.1, 1, 0.1)
        E = KC * q * 1e-9 / r / r
        return N("What is the electric field %s m from a point charge of %d nC? (1/4πε₀ = 9 × 10⁹ N m² C⁻²)" % (nf(r), q), E, [E * r, E * r * r, E / 2], " N/C", "E = kq/r² = <b>%s N/C</b>." % nf(E))
    if k == "flux":
        q = ri(1, 20)
        return N("A charge of %d μC is placed at the centre of a closed cube. What is the electric flux through the whole surface? (ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻²)" % q, q * 1e-6 / E0,
                 [q * 1e-6 * E0, q * 1e-6 / E0 / 6, q / E0], " N m²/C", "Gauss's law: Φ = q/ε₀ = <b>%s N m²/C</b> (the cube's size does not matter)." % nf(q * 1e-6 / E0))
    if k == "sheet":
        q = ri(1, 20)
        return N("A charge of %d μC is at the centre of a cube. What is the electric flux through ONE face? (ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻²)" % q, q * 1e-6 / E0 / 6,
                 [q * 1e-6 / E0, q * 1e-6 / E0 / 4, q * 1e-6 * E0 / 6], " N m²/C", "By symmetry each of the 6 faces gets one-sixth: q/(6ε₀) = <b>%s N m²/C</b>." % nf(q * 1e-6 / E0 / 6))
    if k == "line":
        lam, r = ri(1, 9), rf(0.05, 0.5, 0.05)
        E = 2 * KC * lam * 1e-6 / r
        return N("A long straight wire carries a charge of %d μC per metre. What is the field %s m from it? (1/4πε₀ = 9 × 10⁹ N m² C⁻²)" % (lam, nf(r)), E,
                 [E / 2, E / r, KC * lam * 1e-6 / r / r], " N/C", "E = λ/(2πε₀r) = 2kλ/r = <b>%s N/C</b>." % nf(E))
    if k == "dip":
        q, d = ri(1, 9), ri(1, 10)
        return N("Charges of +%d nC and −%d nC are %d mm apart. What is the electric dipole moment?" % (q, q, d), q * 1e-9 * d * 1e-3, [2 * q * 1e-9 * d * 1e-3, q * 1e-9 / (d * 1e-3), q * d * 1e-9], " C m",
                 "p = q × 2a = %d × 10⁻⁹ × %d × 10⁻³ = <b>%s C m</b>." % (q, d, nf(q * 1e-9 * d * 1e-3)))
    p, E, th = ri(1, 9) * 1e-9, ri(1, 9) * 1e4, ch([30, 60, 90])
    t = p * E * math.sin(math.radians(th))
    return N("A dipole of moment %s C m is placed at %d° to a uniform field of %s N/C. What torque acts on it?" % (nf(p), th, nf(E)), t, [p * E * math.cos(math.radians(th)) or p * E / 2, p * E if th != 90 else p * E * 2, p / E], " N m",
             "τ = pE sin θ = <b>%s N m</b>." % nf(t))


B1 = [("What is the SI unit of electric charge?", "the coulomb (C)", ["the ampere", "the volt", "the newton"], "1 C = 1 A s."),
      ("What does quantisation of charge mean?", "charge always comes in whole-number multiples of e", ["charge can have any value", "charge is always positive", "charge is destroyed in reactions"], "q = ne."),
      ("What does conservation of charge say?", "the total charge of an isolated system stays the same", ["charge always increases", "charge turns into mass", "only positive charge is conserved"], "Charge moves but is not created or destroyed."),
      ("How does the force between two charges change if the distance between them is halved?", "it becomes four times", ["it doubles", "it halves", "it becomes one-fourth"], "F ∝ 1/r²."),
      ("Why do electric field lines never cross?", "the field would have two directions at the same point", ["they repel each other", "they are too thin", "they carry no energy"], "At each point E has one direction."),
      ("Where do electric field lines start and end?", "they start on positive charges and end on negative charges", ["they start on negative charges", "they form closed loops", "they start and end at infinity only"], "Electric field lines do not form closed loops."),
      ("What is the electric field inside a charged hollow conducting sphere?", "zero", ["maximum", "the same as outside", "infinite"], "All the charge sits on the outer surface."),
      ("What is the net force on an electric dipole in a uniform electric field?", "zero, though there may be a torque", ["always maximum", "pE", "infinite"], "The forces on +q and −q cancel."),
      ("What is the dielectric constant (relative permittivity) of a medium?", "ε/ε₀, which tells how much it reduces the force between charges", ["the charge on a body", "the speed of light in it", "its resistance"], "Force in the medium is F/K."),
      ("Which law relates the electric flux through a closed surface to the charge inside it?", "Gauss's law", ["Coulomb's law", "Ohm's law", "Faraday's law"], "Φ = q/ε₀."),
      ("What happens when a glass rod is rubbed with silk?", "the glass loses electrons and becomes positive", ["the glass gains electrons", "both become positive", "no charge moves"], "Silk becomes negative."),
      ("What is the field due to an infinite plane sheet of charge?", "σ/2ε₀, the same at all distances", ["it falls as 1/r²", "zero", "it rises with distance"], "The field is uniform."),
      ("What is the SI unit of electric field?", "N/C (or V/m)", ["C/N", "J", "N m"], "Force per unit charge."),
      ("What is the value of 1/(4πε₀)?", "9 × 10⁹ N m² C⁻²", ["8.85 × 10⁻¹² N m² C⁻²", "6.67 × 10⁻¹¹ N m² kg⁻²", "1.6 × 10⁻¹⁹ C"], "ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻²."),
      ("What is charging by induction?", "charging a body without touching it, by bringing a charged body near", ["charging by rubbing", "charging by contact", "charging by heating"], "The induced charge is opposite to the inducing charge.")]


# =================================================================== 2 potential and capacitance
def cp(k=None):
    k = k or ch(["V", "W", "U", "C", "K", "Q", "E", "ser", "par", "Eg"])
    if k == "V":
        q, r = ri(1, 9), rf(0.1, 1, 0.1)
        return N("What is the electric potential %s m from a point charge of %d nC? (1/4πε₀ = 9 × 10⁹ N m² C⁻²)" % (nf(r), q), KC * q * 1e-9 / r, [KC * q * 1e-9 / r / r, KC * q * 1e-9 * r, KC * q / r], " V",
                 "V = kq/r = <b>%s V</b>." % nf(KC * q * 1e-9 / r))
    if k == "W":
        q, V = ri(1, 9), ri(2, 100, 2)
        return N("How much work is needed to move a charge of %d μC through a potential difference of %d V?" % (q, V), q * 1e-6 * V, [q * 1e-6 / V, q * V, V / (q * 1e-6)], " J", "W = qV = <b>%s J</b>." % nf(q * 1e-6 * V))
    if k == "U":
        q1, q2, r = ri(1, 9), ri(1, 9), rf(0.1, 1, 0.1)
        return N("What is the electrostatic potential energy of two charges of %d μC and %d μC placed %s m apart? (1/4πε₀ = 9 × 10⁹ N m² C⁻²)" % (q1, q2, nf(r)), KC * q1 * q2 * 1e-12 / r,
                 [KC * q1 * q2 * 1e-12 / r / r, KC * (q1 + q2) * 1e-6 / r, KC * q1 * q2 * 1e-12 * r], " J", "U = kq₁q₂/r = <b>%s J</b>." % nf(KC * q1 * q2 * 1e-12 / r))
    if k == "C":
        A, d = rf(0.01, 0.2, 0.01), ri(1, 5)
        c = E0 * A / (d * 1e-3)
        return N("A parallel plate capacitor has plates of area %s m² that are %d mm apart in air. What is its capacitance? (ε₀ = 8.85 × 10⁻¹² F/m)" % (nf(A), d), c, [E0 * A / d, E0 * d * 1e-3 / A, c * 1000], " F",
                 "C = ε₀A/d = 8.85 × 10⁻¹² × %s ÷ %s = <b>%s F</b>." % (nf(A), nf(d * 1e-3), nf(c)))
    if k == "K":
        c0, kk = ri(2, 50), ch([2, 3, 4, 5, 6, 8])
        return N("A capacitor of %d pF is filled with a dielectric of dielectric constant %d. What is its new capacitance?" % (c0, kk), c0 * kk, [c0 / kk, c0 + kk, c0], " pF", "C = KC₀ = <b>%d pF</b>." % (c0 * kk))
    if k == "Eg":
        c, V = ri(2, 50) * 1e-6, ri(5, 200, 5)
        Q = c * V
        return N("A %s μF capacitor holds a charge of %s C. How much energy is stored? (U = Q²/2C)" % (nf(c * 1e6), nf(Q)), Q * Q / (2 * c), [Q * Q / c, Q / (2 * c), Q * c], " J", "U = Q²/2C = <b>%s J</b>." % nf(Q * Q / (2 * c)))
    if k in ("ser", "par"):
        a, b = ri(1, 12), ri(1, 12)
        if k == "ser":
            return N("Capacitors of %d μF and %d μF are joined in series. What is the equivalent capacitance?" % (a, b), a * b / (a + b), [a + b, (a + b) / 2, abs(a - b) or a * 2], " μF", "1/C = 1/%d + 1/%d, so C = <b>%s μF</b>." % (a, b, nf(a * b / (a + b))))
        return N("Capacitors of %d μF and %d μF are joined in parallel. What is the equivalent capacitance?" % (a, b), a + b, [a * b / (a + b), a * b, (a + b) / 2], " μF", "In parallel C = C₁ + C₂ = <b>%d μF</b>." % (a + b))
    c, V = ri(1, 50), ri(5, 200, 5)
    if k == "Q":
        return N("A %d μF capacitor is connected to a %d V battery. What charge is stored?" % (c, V), c * 1e-6 * V, [c * 1e-6 / V, c * V, V / (c * 1e-6)], " C", "Q = CV = <b>%s C</b>." % nf(c * 1e-6 * V))
    return N("A %d μF capacitor is charged to %d V. What energy is stored?" % (c, V), 0.5 * c * 1e-6 * V * V, [c * 1e-6 * V * V, 0.5 * c * 1e-6 * V, c * 1e-6 * V], " J", "U = ½CV² = <b>%s J</b>." % nf(0.5 * c * 1e-6 * V * V))


B2 = [("What is an equipotential surface?", "a surface on which the potential is the same everywhere", ["a surface with no charge", "a surface with zero field always", "a charged plate"], "No work is done moving a charge along it."),
      ("What is the angle between field lines and an equipotential surface?", "90°", ["0°", "45°", "180°"], "The field is always perpendicular to equipotentials."),
      ("How much work is done in moving a charge along an equipotential surface?", "zero", ["qV", "maximum", "it depends on the path"], "There is no potential difference."),
      ("What is the SI unit of capacitance?", "the farad (F)", ["the coulomb", "the volt", "the henry"], "1 F = 1 C/V."),
      ("What happens to the capacitance of a parallel plate capacitor if the distance between the plates is doubled?", "it halves", ["it doubles", "it stays the same", "it becomes four times"], "C = ε₀A/d."),
      ("What does a dielectric do when placed between capacitor plates (battery disconnected)?", "it reduces the potential difference and increases the capacitance", ["it increases the charge", "it reduces the capacitance", "it discharges the capacitor"], "The induced charges partly cancel the field."),
      ("What is the electric potential inside a charged conducting sphere?", "constant, equal to its value at the surface", ["zero", "increasing towards the centre", "infinite"], "The field inside is zero, so V does not change."),
      ("What is the relation between field and potential?", "E = −dV/dr", ["E = V × r", "E = dV/dt", "E = V/q"], "The field points in the direction of falling potential."),
      ("What is the potential energy of a dipole in a uniform field when it is aligned with the field?", "−pE, a minimum", ["zero", "+pE, a maximum", "2pE"], "U = −pE cos θ."),
      ("What is electrostatic shielding?", "protecting a region from electric fields by surrounding it with a conductor", ["using rubber gloves", "earthing a wire", "a type of capacitor"], "e.g. staying inside a car in a lightning storm."),
      ("Which quantity is the same for capacitors connected in series?", "the charge on each", ["the potential difference across each", "the capacitance", "the energy"], "In parallel, the p.d. is the same."),
      ("What is the electron volt (eV)?", "the energy gained by an electron moving through 1 V; 1.6 × 10⁻¹⁹ J", ["1 J", "the charge of an electron", "the potential of an electron"], "Used for atomic energies."),
      ("What is the potential at a point due to a dipole on its equatorial line?", "zero", ["maximum", "kp/r²", "kq/r"], "The contributions of +q and −q cancel."),
      ("How is the energy stored in a capacitor written?", "½CV² = Q²/2C = ½QV", ["CV²", "Q/V", "C/V"], "It is stored in the electric field between the plates."),
      ("What are polar molecules?", "molecules with a permanent dipole moment, such as water", ["molecules with no dipole", "ions", "metals"], "Non-polar molecules like O₂ have no permanent dipole.")]


# =================================================================== 3 current electricity
def cu(k=None):
    k = k or ch(["drift", "wb", "mb", "R2", "kirch", "cells"])
    if k == "drift":
        I, A = ri(1, 10), rf(0.5, 5, 0.5)
        n = 8.5e28
        v = I / (n * QE * A * 1e-6)
        return N("A copper wire of cross-section %s mm² carries %d A. Taking n = 8.5 × 10²⁸ m⁻³ and e = 1.6 × 10⁻¹⁹ C, what is the drift velocity?" % (nf(A), I), v,
                 [v * 1e6, I / (n * A * 1e-6), v / 1000], " m/s", "v<sub>d</sub> = I/(neA) = <b>%s m/s</b> (very slow)." % nf(v))
    if k == "wb":
        Pp, Q, R = ri(2, 20, 2), ri(2, 20, 2), ri(2, 20, 2)
        S = R * Q / Pp
        return N("In a balanced Wheatstone bridge P = %d Ω, Q = %d Ω and R = %d Ω (P/Q = R/S). What is S?" % (Pp, Q, R), S, [Pp * R / Q, Pp * Q / R, Pp + Q + R], " Ω", "P/Q = R/S, so S = RQ/P = <b>%s Ω</b>." % nf(S))
    if k == "mb":
        Rv, l = ri(2, 20), ri(25, 75, 5)
        S = Rv * (100 - l) / l
        return N("In a metre bridge the balance point is %d cm from the end where R = %d Ω is connected. What is the unknown resistance S? (R/S = l/(100 − l))" % (l, Rv), S, [Rv * l / (100 - l), Rv * l / 100, Rv], " Ω",
                 "S = R(100 − l)/l = %d × %d/%d = <b>%s Ω</b>." % (Rv, 100 - l, l, nf(S))) if l != 50 else None
    if k == "R2":
        R1, f = ri(2, 20), ch([2, 3, 0.5])
        return N("A wire of resistance %d Ω is stretched to %s times its length (volume unchanged). What is its new resistance?" % (R1, nf(f)), R1 * f * f, [R1 * f, R1 / f, R1], " Ω",
                 "R ∝ l²  when volume is fixed, so R = %d × %s² = <b>%s Ω</b>." % (R1, nf(f), nf(R1 * f * f)))
    if k == "cells":
        n, e, r, R = ri(2, 6), rf(1, 2, 0.5), rf(0.1, 1, 0.1), ri(2, 20)
        I = n * e / (R + n * r)
        return N("%d cells, each of e.m.f. %s V and internal resistance %s Ω, are joined in series to an external resistance of %d Ω. What is the current?" % (n, nf(e), nf(r), R), I,
                 [n * e / R, e / (R + r), n * e / (R + r)], " A", "I = nE/(R + nr) = %s ÷ %s = <b>%s A</b>." % (nf(n * e), nf(R + n * r), nf(I)))
    I1, I2 = ri(1, 9), ri(1, 9)
    return N("At a junction, currents of %d A and %d A flow in. One wire carries 1 A out. What current flows out through the other wire?" % (I1, I2), I1 + I2 - 1, [I1 + I2 + 1, abs(I1 - I2), I1 + I2], " A",
             "Kirchhoff's junction rule: current in = current out, so %d + %d − 1 = <b>%d A</b>." % (I1, I2, I1 + I2 - 1))


B3 = [("What is the drift velocity of electrons in a conductor?", "the small average velocity of free electrons along the wire when a current flows", ["the speed of light", "the speed of the electric signal", "zero"], "It is of the order of mm/s."),
      ("Why does a bulb light up almost at once when the switch is closed, though drift velocity is small?", "the electric field is set up along the wire almost instantly and all free electrons start drifting together", ["electrons move at light speed", "the bulb stores electrons", "the switch pushes electrons"], "The signal travels very fast."),
      ("How does the resistivity of a metal change with temperature?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "Electrons collide more often."),
      ("How does the resistivity of a semiconductor change with temperature?", "it decreases", ["it increases", "it stays the same", "it becomes infinite"], "More charge carriers are freed."),
      ("Which material is used for the wires of standard resistors?", "manganin or constantan", ["copper", "silver", "tungsten"], "Their resistance hardly changes with temperature."),
      ("What does Kirchhoff's loop rule express?", "conservation of energy", ["conservation of charge", "conservation of momentum", "Ohm's law only"], "The sum of potential changes round a loop is zero."),
      ("What does Kirchhoff's junction rule express?", "conservation of charge", ["conservation of energy", "Newton's third law", "conservation of mass"], "Current in = current out."),
      ("What is the SI unit of resistivity?", "Ω m", ["Ω", "Ω/m", "S"], "R = ρl/A."),
      ("Why is a metre bridge most accurate when the balance point is near the middle?", "the percentage error in measuring lengths is smallest there", ["the wire is thickest there", "no current flows", "the battery works best"], "End errors matter less."),
      ("What is the terminal voltage of a cell when it is being discharged?", "V = E − Ir", ["V = E + Ir", "V = E", "V = Ir"], "Some voltage is lost inside the cell."),
      ("Cells are joined in parallel. What is the advantage?", "they can supply a larger current for longer", ["the e.m.f. adds up", "the internal resistance adds up", "no current flows"], "Equal cells in parallel give the same e.m.f."),
      ("What is mobility of a charge carrier?", "drift velocity per unit electric field", ["charge per unit mass", "current per unit area", "speed of light"], "μ = v<sub>d</sub>/E."),
      ("What is current density?", "current per unit area of cross-section", ["charge per unit time", "voltage per unit length", "resistance per unit length"], "j = I/A."),
      ("Does Ohm's law hold for all conductors?", "no; diodes and electrolytes are non-ohmic", ["yes, always", "only for semiconductors", "only at high temperature"], "Ohmic conductors have a straight V–I graph."),
      ("Which instrument compares potential differences without drawing current (classical method)?", "a potentiometer", ["an ammeter", "a galvanometer alone", "a voltmeter of low resistance"], "At balance no current is drawn from the cell.")]


# =================================================================== 4 moving charges and magnetism
def mg(k=None):
    k = k or ch(["wire", "loop", "sol", "cyc", "par", "shunt", "volt"])
    if k == "wire":
        I, r = ri(1, 20), rf(0.01, 0.2, 0.01)
        B_ = MU0 * I / (2 * math.pi * r)
        return N("What is the magnetic field %s m from a long straight wire carrying %d A? (μ₀ = 4π × 10⁻⁷ T m/A)" % (nf(r), I), B_, [MU0 * I / r, MU0 * I / (2 * r), B_ * r], " T", "B = μ₀I/(2πr) = 2 × 10⁻⁷ × %d ÷ %s = <b>%s T</b>." % (I, nf(r), nf(B_)))
    if k == "loop":
        n, I, R = ri(1, 100), ri(1, 10), rf(0.05, 0.3, 0.05)
        B_ = MU0 * n * I / (2 * R)
        return N("A circular coil of %d turn%s and radius %s m carries %d A. What is the field at its centre? (μ₀ = 4π × 10⁻⁷ T m/A)" % (n, "" if n == 1 else "s", nf(R), I), B_,
                 [MU0 * n * I / (2 * math.pi * R), MU0 * I / (2 * R), MU0 * n * I / R], " T", "B = μ₀NI/(2R) = <b>%s T</b>." % nf(B_))
    if k == "sol":
        n, I = ri(5, 50) * 100, rf(0.5, 5, 0.5)
        return N("A long solenoid has %d turns per metre and carries %s A. What is the field inside it? (μ₀ = 4π × 10⁻⁷ T m/A)" % (n, nf(I)), MU0 * n * I, [MU0 * n * I / 2, MU0 * I, MU0 * n * I / (2 * math.pi)], " T",
                 "B = μ₀nI = <b>%s T</b>." % nf(MU0 * n * I))
    if k == "cyc":
        Bv = rf(0.5, 2, 0.1)
        f = QE * Bv / (2 * math.pi * 1.67e-27)
        return N("What is the cyclotron frequency for protons in a magnetic field of %s T? (q = 1.6 × 10⁻¹⁹ C, m = 1.67 × 10⁻²⁷ kg)" % nf(Bv), f, [QE * Bv / 1.67e-27, f * 2 * math.pi * 2, f / 2], " Hz",
                 "f = qB/(2πm) = <b>%s Hz</b> (it does not depend on speed)." % nf(f))
    if k == "par":
        I1, I2, d = ri(1, 20), ri(1, 20), rf(0.01, 0.2, 0.01)
        F = MU0 * I1 * I2 / (2 * math.pi * d)
        return N("Two long parallel wires %s m apart carry currents of %d A and %d A. What is the force per metre between them? (μ₀ = 4π × 10⁻⁷ T m/A)" % (nf(d), I1, I2), F,
                 [MU0 * I1 * I2 / d, F * d, MU0 * (I1 + I2) / (2 * math.pi * d)], " N/m", "F/l = μ₀I₁I₂/(2πd) = <b>%s N/m</b>." % nf(F))
    G, Ig = ri(10, 100, 5), ri(1, 10)
    if k == "shunt":
        I = ri(1, 10)
        S = Ig * 1e-3 * G / (I - Ig * 1e-3)
        return N("A galvanometer of resistance %d Ω gives full deflection with %d mA. What shunt converts it into an ammeter of range 0–%d A?" % (G, Ig, I), S, [G * I / (Ig * 1e-3), Ig * G, S * 1000], " Ω",
                 "S = I<sub>g</sub>G/(I − I<sub>g</sub>) = <b>%s Ω</b> (small, in parallel)." % nf(S))
    V = ri(1, 20) * 5
    R = V / (Ig * 1e-3) - G
    return N("A galvanometer of resistance %d Ω gives full deflection with %d mA. What resistance in series converts it into a voltmeter of range 0–%d V?" % (G, Ig, V), R, [V / (Ig * 1e-3), V / (Ig * 1e-3) + G, V * G], " Ω",
             "R = V/I<sub>g</sub> − G = <b>%s Ω</b> (large, in series)." % nf(R))


B4 = [("Who first found that a current produces a magnetic field?", "Hans Christian Oersted", ["Michael Faraday", "André-Marie Ampère", "James Clerk Maxwell"], "In 1820 a compass needle moved near a current."),
      ("What is the direction of the magnetic force on a moving charge?", "perpendicular to both the velocity and the field", ["along the velocity", "along the field", "opposite to the velocity"], "F = q(v × B)."),
      ("How much work does a magnetic field do on a moving charge?", "none, because the force is perpendicular to the motion", ["qvB", "½mv²", "it depends on the charge"], "The speed stays the same."),
      ("What path does a charged particle follow when it enters a uniform magnetic field at right angles?", "a circle", ["a straight line", "a parabola", "a helix always"], "At an angle it follows a helix."),
      ("Which rule gives the direction of the field round a straight current?", "the right-hand thumb rule", ["Fleming's left-hand rule", "Lenz's law", "the left-hand thumb rule"], "Thumb along the current, fingers curl along B."),
      ("What does Ampère's circuital law state?", "∮B · dl = μ₀I (current enclosed)", ["F = qE", "V = IR", "Φ = q/ε₀"], "It is used for long wires and solenoids."),
      ("Two parallel wires carry currents in the same direction. What happens?", "they attract each other", ["they repel each other", "nothing happens", "they rotate"], "Opposite currents repel."),
      ("How is the ampere defined (older definition) using parallel wires?", "the current that gives a force of 2 × 10⁻⁷ N per metre between two wires 1 m apart", ["1 C per minute", "the current in a 1 Ω resistor", "the current through a bulb"], "It came from the force between currents."),
      ("What is the magnetic moment of a current loop?", "m = NIA", ["m = NI/A", "m = IB", "m = qv"], "Its direction is given by the right-hand rule."),
      ("Why is a radial magnetic field used in a moving coil galvanometer?", "so the torque, and hence the deflection, is proportional to the current", ["to make the coil heavier", "to reduce friction", "to make the field zero"], "The plane of the coil is always along the field lines."),
      ("How is a galvanometer converted into an ammeter?", "by connecting a small resistance (shunt) in parallel", ["by a large resistance in series", "by a battery in series", "by removing the coil"], "Most of the current passes through the shunt."),
      ("How is a galvanometer converted into a voltmeter?", "by connecting a large resistance in series", ["by a small shunt in parallel", "by a capacitor", "by a diode"], "Very little current is drawn."),
      ("What is the field outside a long ideal solenoid?", "almost zero", ["the same as inside", "twice the field inside", "infinite"], "The field inside is uniform, μ₀nI."),
      ("What is the Lorentz force?", "the total force qE + q(v × B) on a moving charge", ["the force between masses", "the force of friction", "the force in a spring"], "It combines electric and magnetic forces."),
      ("Does the cyclotron frequency depend on the speed of the particle?", "no", ["yes, it rises with speed", "yes, it falls with speed", "only for electrons"], "f = qB/(2πm).")]


# =================================================================== 5 magnetism and matter
def mm(k=None):
    k = k or ch(["m", "tq", "U", "W", "chi"])
    if k == "m":
        n, I, A_ = ri(10, 500, 10), rf(0.5, 5, 0.5), rf(0.001, 0.02, 0.001)
        return N("A coil of %d turns, each of area %s m², carries %s A. What is its magnetic moment?" % (n, nf(A_), nf(I)), n * I * A_, [I * A_, n * I / A_, n * A_], " A m²", "m = NIA = <b>%s A m²</b>." % nf(n * I * A_))
    m_, B_ = rf(0.5, 5, 0.5), rf(0.1, 1, 0.1)
    if k == "tq":
        th = ch([30, 60, 90])
        return N("A bar magnet of magnetic moment %s A m² is at %d° to a uniform field of %s T. What torque acts on it?" % (nf(m_), th, nf(B_)), m_ * B_ * math.sin(math.radians(th)),
                 [m_ * B_ * math.cos(math.radians(th)) or m_ * B_ / 2, m_ / B_, m_ * B_ * 2], " N m", "τ = mB sin θ = <b>%s N m</b>." % nf(m_ * B_ * math.sin(math.radians(th))))
    if k == "U":
        th = ch([0, 60, 90, 120, 180])
        U = -m_ * B_ * math.cos(math.radians(th))
        U = 0 if abs(U) < 1e-12 else U
        return N("A magnetic dipole of moment %s A m² makes %d° with a field of %s T. What is its potential energy?" % (nf(m_), th, nf(B_)), U, [-U if U else m_ * B_, m_ * B_ * math.sin(math.radians(th)) or m_ * B_ * 2, 2 * m_ * B_], " J",
                 "U = −mB cos θ = <b>%s J</b>." % (nf(U) if U else "0"))
    if k == "W":
        return N("How much work is needed to turn a magnet of moment %s A m² from along a field of %s T to the opposite direction?" % (nf(m_), nf(B_)), 2 * m_ * B_, [m_ * B_, 0.5 * m_ * B_, 4 * m_ * B_], " J",
                 "W = U(180°) − U(0°) = mB − (−mB) = <b>%s J</b>." % nf(2 * m_ * B_))
    T1, T2 = ri(200, 400, 10), ri(200, 400, 10)
    x1 = rf(1, 9, 0.5) * 1e-5
    if T1 == T2:
        return None
    return N("A paramagnetic salt has a susceptibility of %s at %d K. Using Curie's law (χ ∝ 1/T), what is it at %d K?" % (nf(x1), T1, T2), x1 * T1 / T2, [x1 * T2 / T1, x1, x1 * (T2 - T1)], "",
             "χ₂ = χ₁T₁/T₂ = <b>%s</b>." % nf(x1 * T1 / T2))


MAG = {"diamagnetic": ["bismuth", "copper", "water", "silver", "lead", "nitrogen gas"], "paramagnetic": ["aluminium", "sodium", "oxygen gas", "platinum", "calcium"],
       "ferromagnetic": ["iron", "cobalt", "nickel", "gadolinium", "alnico"]}
B5 = [("What happens when a bar magnet is cut into two pieces?", "each piece becomes a complete magnet with N and S poles", ["one piece is N and the other S", "the magnetism is lost", "only one piece is magnetic"], "Magnetic monopoles do not exist."),
      ("What is Gauss's law for magnetism?", "the net magnetic flux through any closed surface is zero", ["the flux equals q/ε₀", "the flux is always maximum", "magnetic charges exist"], "Magnetic field lines are closed loops."),
      ("Where are the field lines of a bar magnet inside it?", "from the S pole to the N pole", ["from N to S", "there are none", "in circles"], "They form closed loops."),
      ("What is the susceptibility of a diamagnetic substance?", "small and negative", ["small and positive", "large and positive", "zero"], "It is weakly repelled by a magnet."),
      ("What is the susceptibility of a ferromagnetic substance?", "very large and positive", ["small and negative", "small and positive", "zero"], "It is strongly attracted."),
      ("What happens to a ferromagnet above its Curie temperature?", "it becomes paramagnetic", ["it becomes diamagnetic", "it becomes stronger", "it melts"], "Thermal motion breaks up the domains."),
      ("What is a superconductor's magnetic behaviour called?", "perfect diamagnetism (Meissner effect)", ["ferromagnetism", "paramagnetism", "hysteresis"], "It expels magnetic field lines."),
      ("Which material is best for permanent magnets?", "one with high retentivity and high coercivity, such as alnico or steel", ["soft iron", "copper", "aluminium"], "It keeps its magnetism."),
      ("Which material is best for electromagnet cores and transformers?", "soft iron, with high permeability and low coercivity", ["steel", "alnico", "copper"], "It magnetises and demagnetises easily."),
      ("What is hysteresis?", "the lagging of magnetisation behind the magnetising field", ["the loss of charge", "the heating of wires", "the bending of light"], "The area of the loop is the energy lost per cycle."),
      ("What is retentivity?", "the magnetisation that remains when the magnetising field is removed", ["the field needed to remove magnetism", "the resistance of iron", "the speed of domains"], "Also called remanence."),
      ("What is coercivity?", "the reverse field needed to reduce the magnetisation to zero", ["the magnetisation left over", "the susceptibility", "the Curie temperature"], "Hard magnets have high coercivity."),
      ("What is the relation between B, H and M?", "B = μ₀(H + M)", ["B = H − M", "B = μ₀HM", "B = M/H"], "M is the magnetisation."),
      ("What is the relative permeability of a diamagnetic material?", "slightly less than 1", ["slightly more than 1", "much more than 1", "zero"], "μ<sub>r</sub> = 1 + χ."),
      ("A magnet is freely suspended. How does it come to rest?", "pointing roughly north–south", ["east–west", "vertically", "in any direction"], "It aligns with the Earth's field.")]


# =================================================================== 6 electromagnetic induction
def emi(k=None):
    k = k or ch(["Blv", "Ldi", "UL", "flux", "rate", "M"])
    if k == "Blv":
        B_, l, v = rf(0.1, 1, 0.1), rf(0.1, 2, 0.1), ri(1, 20)
        return N("A rod of length %s m moves at %d m/s at right angles to a field of %s T. What e.m.f. is induced between its ends?" % (nf(l), v, nf(B_)), B_ * l * v, [B_ * l / v, B_ * v, B_ * l * v * 2], " V", "ε = Blv = <b>%s V</b>." % nf(B_ * l * v))
    if k == "Ldi":
        L, di, dt = rf(0.1, 5, 0.1), ri(1, 10), rf(0.01, 0.5, 0.01)
        return N("The current in a coil of self-inductance %s H changes by %d A in %s s. What is the induced e.m.f.?" % (nf(L), di, nf(dt)), L * di / dt, [L * di * dt, di / (L * dt), L * di], " V", "ε = L dI/dt = <b>%s V</b>." % nf(L * di / dt))
    if k == "UL":
        L, I = rf(0.1, 5, 0.1), ri(1, 10)
        return N("A current of %d A flows in an inductor of %s H. What energy is stored in its magnetic field?" % (I, nf(L)), 0.5 * L * I * I, [L * I * I, 0.5 * L * I, L * I], " J", "U = ½LI² = <b>%s J</b>." % nf(0.5 * L * I * I))
    if k == "M":
        M_, di, dt = rf(0.1, 2, 0.1), ri(1, 10), rf(0.01, 0.5, 0.01)
        return N("Two coils have a mutual inductance of %s H. The current in the first changes by %d A in %s s. What e.m.f. is induced in the second?" % (nf(M_), di, nf(dt)), M_ * di / dt, [M_ * di * dt, M_ * di, di / dt], " V", "ε = M dI/dt = <b>%s V</b>." % nf(M_ * di / dt))
    if k == "flux":
        n, A_, B_ = ri(10, 500, 10), rf(0.01, 0.1, 0.01), rf(0.1, 1, 0.1)
        return N("A coil of %d turns, each of area %s m², is at right angles to a field of %s T. What is the total flux linkage?" % (n, nf(A_), nf(B_)), n * A_ * B_, [A_ * B_, n * B_, n * A_ / B_], " Wb", "NΦ = NBA = <b>%s Wb</b>." % nf(n * A_ * B_))
    n, d, t = ri(10, 500, 10), rf(0.01, 0.5, 0.01), rf(0.01, 1, 0.01)
    return N("The flux through each turn of a %d-turn coil falls by %s Wb in %s s. What is the average induced e.m.f.?" % (n, nf(d), nf(t)), n * d / t, [d / t, n * d * t, n * t / d], " V", "ε = NΔΦ/Δt = <b>%s V</b>." % nf(n * d / t))


B6 = [("What does Faraday's law of induction state?", "the induced e.m.f. equals the rate of change of magnetic flux linkage", ["current is proportional to voltage", "flux is always constant", "charge is conserved"], "ε = −dΦ/dt."),
      ("What does Lenz's law state?", "the induced current opposes the change that causes it", ["the induced current helps the change", "no current is induced", "the induced e.m.f. is always zero"], "It follows from conservation of energy."),
      ("Lenz's law is a consequence of the conservation of…", "energy", ["charge", "momentum", "mass"], "Otherwise energy could be created."),
      ("What are eddy currents?", "currents induced in a solid piece of metal by a changing magnetic flux", ["currents in a superconductor", "currents in a battery", "static charges"], "They cause heating and damping."),
      ("How are eddy currents reduced in a transformer core?", "by using thin insulated laminations", ["by using a solid iron block", "by using copper", "by heating the core"], "The current paths are broken up."),
      ("Which device uses eddy currents in brakes?", "electric trains (electromagnetic braking)", ["bicycles", "torches", "thermometers"], "Eddy currents also damp galvanometers."),
      ("What is the SI unit of inductance?", "the henry (H)", ["the tesla", "the weber", "the farad"], "1 H = 1 V s/A."),
      ("What is the SI unit of magnetic flux?", "the weber (Wb)", ["the tesla", "the henry", "the gauss"], "1 Wb = 1 T m²."),
      ("Why does a coil oppose a change of current in itself?", "self-induction produces a back e.m.f.", ["its resistance increases", "it stores charge", "it is a capacitor"], "This is like inertia for current."),
      ("What does an AC generator convert?", "mechanical energy into electrical energy", ["electrical into mechanical energy", "heat into light", "chemical into electrical energy"], "A coil rotates in a magnetic field."),
      ("What is the peak e.m.f. of a coil of N turns, area A, rotating with angular speed ω in field B?", "NBAω", ["NBA", "BAω", "NBω"], "ε = NBAω sin ωt."),
      ("Which rule gives the direction of induced current in a moving conductor?", "Fleming's right-hand rule", ["Fleming's left-hand rule", "the right-hand thumb rule", "Lenz's rule of thumb"], "The motor uses the left-hand rule."),
      ("A magnet is dropped through a copper ring. What happens?", "it falls more slowly than free fall", ["it falls faster", "it stops in the ring", "nothing happens"], "Induced currents oppose its motion."),
      ("On what does the self-inductance of a solenoid depend?", "the number of turns, its area, its length and the core material", ["the current only", "the voltage only", "the colour of the wire"], "L = μ₀μ<sub>r</sub>n²Al.")]


# =================================================================== 7 alternating current
def ac(k=None):
    k = k or ch(["rms", "peak", "XL", "XC", "Z", "f0", "pf"])
    if k == "rms":
        v0 = ri(10, 400, 10)
        return N("An AC voltage has a peak value of %d V. What is its rms value?" % v0, v0 / math.sqrt(2), [v0 * math.sqrt(2), v0 / 2, v0], " V", "V<sub>rms</sub> = V₀/√2 = <b>%s V</b>." % nf(v0 / math.sqrt(2)))
    if k == "peak":
        v = ch([110, 220, 230, 240, 120])
        return N("The rms voltage of a supply is %d V. What is its peak value?" % v, v * math.sqrt(2), [v / math.sqrt(2), 2 * v, v], " V", "V₀ = √2 × V<sub>rms</sub> = <b>%s V</b>." % nf(v * math.sqrt(2)))
    if k == "XL":
        L, f = rf(0.1, 2, 0.1), ch([50, 60, 100, 200, 500])
        return N("What is the reactance of a %s H inductor at %d Hz?" % (nf(L), f), 2 * math.pi * f * L, [f * L, 1 / (2 * math.pi * f * L), 2 * math.pi * L], " Ω", "X<sub>L</sub> = 2πfL = <b>%s Ω</b>." % nf(2 * math.pi * f * L))
    if k == "XC":
        c, f = ri(1, 100), ch([50, 60, 100, 200, 500])
        x = 1 / (2 * math.pi * f * c * 1e-6)
        return N("What is the reactance of a %d μF capacitor at %d Hz?" % (c, f), x, [2 * math.pi * f * c * 1e-6, 1 / (f * c * 1e-6), x / (2 * math.pi)], " Ω", "X<sub>C</sub> = 1/(2πfC) = <b>%s Ω</b>." % nf(x))
    if k == "Z":
        R, XL, XC = ch([(3, 8, 4), (6, 10, 2), (5, 20, 8), (8, 12, 6), (12, 20, 4), (9, 15, 3), (15, 30, 10), (20, 25, 10)])
        m = ri(1, 4)
        R, XL, XC = R * m, XL * m, XC * m
        return N("A series LCR circuit has R = %d Ω, X<sub>L</sub> = %d Ω and X<sub>C</sub> = %d Ω. What is its impedance?" % (R, XL, XC), math.hypot(R, XL - XC), [R + XL - XC, math.hypot(R, XL + XC), R + XL + XC], " Ω",
                 "Z = √(R² + (X<sub>L</sub> − X<sub>C</sub>)²) = <b>%s Ω</b>." % nf(math.hypot(R, XL - XC)))
    if k == "f0":
        L, c = rf(0.1, 2, 0.1), ri(1, 100)
        f = 1 / (2 * math.pi * math.sqrt(L * c * 1e-6))
        return N("At what frequency does a series LCR circuit with L = %s H and C = %d μF resonate?" % (nf(L), c), f, [1 / math.sqrt(L * c * 1e-6), 2 * math.pi * math.sqrt(L * c * 1e-6), f * 2], " Hz", "f₀ = 1/(2π√(LC)) = <b>%s Hz</b>." % nf(f))
    R, Z = ch([(3, 5), (6, 10), (5, 13), (8, 17), (12, 13), (9, 15), (20, 25), (7, 25)])
    return N("A series LCR circuit has R = %d Ω and impedance %d Ω. What is its power factor?" % (R, Z), R / Z, [Z / R, math.sqrt(Z * Z - R * R) / Z, R / Z / 2], "", "cos φ = R/Z = <b>%s</b>." % nf(R / Z))


B7 = [("Why is AC preferred to DC for supplying electricity over long distances?", "AC voltage can be stepped up with transformers, so less power is lost in the lines", ["AC cannot shock people", "AC has no resistance", "DC cannot light bulbs"], "High voltage means low current and low I²R loss."),
      ("In a purely inductive AC circuit, how is the current related to the voltage?", "the current lags the voltage by π/2", ["the current leads by π/2", "they are in phase", "they are out of phase by π"], "Inductors oppose changes of current."),
      ("In a purely capacitive AC circuit, how is the current related to the voltage?", "the current leads the voltage by π/2", ["the current lags by π/2", "they are in phase", "they are out of phase by π"], "The capacitor charges before the voltage peaks."),
      ("What is the average power used in a pure inductor over a cycle?", "zero", ["V<sub>rms</sub>I<sub>rms</sub>", "I²R", "maximum"], "Energy is stored and returned each cycle."),
      ("What happens at resonance in a series LCR circuit?", "X<sub>L</sub> = X<sub>C</sub>, the impedance is minimum and the current is maximum", ["the current is zero", "the impedance is maximum", "the voltage is zero"], "Z = R at resonance."),
      ("What is wattless current?", "current in a circuit with zero power factor, as in a pure L or C circuit", ["current with no charge", "DC current", "current in a resistor"], "cos φ = 0."),
      ("What is the power factor of a purely resistive circuit?", "1", ["0", "0.5", "infinite"], "Voltage and current are in phase."),
      ("What does a step-up transformer do?", "it increases the voltage and decreases the current", ["it increases both", "it increases the current only", "it changes AC to DC"], "N<sub>s</sub> > N<sub>p</sub>."),
      ("Why can transformers not work with DC?", "a steady current gives no changing flux, so no e.m.f. is induced", ["DC is too strong", "DC melts the coil", "they can, equally well"], "Induction needs changing flux."),
      ("What is the quality factor (Q) of a series resonant circuit?", "a measure of the sharpness of resonance", ["the power used", "the resistance", "the voltage"], "Q = ω₀L/R."),
      ("How does the reactance of a capacitor change with frequency?", "it decreases as frequency rises", ["it increases", "it stays the same", "it becomes zero at low frequency"], "X<sub>C</sub> = 1/(ωC)."),
      ("How does the reactance of an inductor change with frequency?", "it increases as frequency rises", ["it decreases", "it stays the same", "it is infinite at all frequencies"], "X<sub>L</sub> = ωL."),
      ("What are the energy losses in a transformer?", "copper (I²R) loss, eddy currents, hysteresis and flux leakage", ["none at all", "only light", "only sound"], "Laminated soft iron cores reduce them."),
      ("What is the frequency of the AC mains supply in India?", "50 Hz", ["60 Hz", "100 Hz", "220 Hz"], "The rms voltage is 220–230 V.")]


# =================================================================== 8 electromagnetic waves
EMW = [("radio waves", "radio and TV broadcasting"), ("microwaves", "radar and cooking"), ("infrared waves", "remote controls and heat lamps"), ("visible light", "seeing with our eyes"),
       ("ultraviolet rays", "sterilising water and killing germs"), ("X-rays", "imaging bones in medicine"), ("gamma rays", "treating cancer (radiotherapy)")]


def em(k=None):
    k = k or ch(["f", "lam", "c", "E0", "n"])
    if k == "f":
        u, m = ch([("m", 1), ("cm", 1e-2), ("mm", 1e-3), ("μm", 1e-6), ("nm", 1e-9)])
        x = ri(1, 9) * ch([1, 10, 100]) if u != "nm" else ri(10, 90) * 10
        lam = ("%d %s" % (x, u), x * m)
        return N("What is the frequency of an electromagnetic wave of wavelength %s? (c = 3 × 10⁸ m/s)" % lam[0], C / lam[1], [C * lam[1], lam[1] / C, C / lam[1] / 1000], " Hz", "f = c/λ = <b>%s Hz</b>." % nf(C / lam[1]))
    if k == "lam":
        u = ch(["kHz", "MHz", "GHz"])
        f = ri(1, 999)
        return N("What is the wavelength of an electromagnetic wave of frequency %s %s? (c = 3 × 10⁸ m/s)" % (nf(f), u), C / (f * 1e0 * {"MHz": 1e6, "GHz": 1e9, "kHz": 1e3}[u]), [C * f, f / C, C / f], " m",
                 "λ = c/f = <b>%s m</b>." % nf(C / (f * {"MHz": 1e6, "GHz": 1e9, "kHz": 1e3}[u])))
    if k == "E0":
        B0 = ri(1, 9) * 10 ** -ri(7, 9)
        return N("In an electromagnetic wave the magnetic field has an amplitude of %s T. What is the amplitude of the electric field? (c = 3 × 10⁸ m/s)" % nf(B0), B0 * C, [B0 / C, C / B0, B0 * C / 2], " V/m",
                 "E₀ = cB₀ = <b>%s V/m</b>." % nf(B0 * C))
    if k == "n":
        n = ch([1.33, 1.5, 1.6, 2.42, 1.2, 1.25])
        return N("What is the speed of light in a medium of refractive index %s? (c = 3 × 10⁸ m/s)" % nf(n), C / n, [C * n, C, C / n / n], " m/s", "v = c/n = <b>%s m/s</b>." % nf(C / n))
    eps = ch([2, 4, 9, 16, 25])
    return N("A non-magnetic medium has relative permittivity %d. What is the speed of electromagnetic waves in it? (v = c/√ε<sub>r</sub>)" % eps, C / math.sqrt(eps), [C / eps, C * math.sqrt(eps), C], " m/s", "v = c/√%d = <b>%s m/s</b>." % (eps, nf(C / math.sqrt(eps))))


B8 = [("Who predicted electromagnetic waves?", "James Clerk Maxwell", ["Heinrich Hertz", "Jagadish Chandra Bose", "Guglielmo Marconi"], "Hertz produced them in the laboratory."),
      ("What is displacement current?", "a current due to a changing electric field, as between capacitor plates", ["a current in a wire", "a flow of protons", "a static charge"], "Maxwell added it to Ampère's law."),
      ("What produces electromagnetic waves?", "accelerated (oscillating) charges", ["charges at rest", "charges moving at steady speed", "neutral atoms only"], "They radiate energy."),
      ("How are E and B related in an electromagnetic wave?", "they are perpendicular to each other and to the direction of travel", ["they are parallel", "E is along the direction of travel", "B is zero"], "EM waves are transverse."),
      ("Which EM waves have the longest wavelength?", "radio waves", ["gamma rays", "X-rays", "visible light"], "Gamma rays have the shortest."),
      ("Which part of the spectrum has wavelengths of about 400–700 nm?", "visible light", ["ultraviolet", "infrared", "X-rays"], "Violet is about 400 nm, red about 700 nm."),
      ("Which layer of the atmosphere absorbs most of the Sun's ultraviolet radiation?", "the ozone layer", ["the troposphere", "the ionosphere", "clouds"], "UV can cause skin cancer."),
      ("Why are infrared waves called heat waves?", "they are readily absorbed by water molecules and raise the temperature", ["they are hot", "they come only from fire", "they cannot be seen"], "This is the basis of the greenhouse effect."),
      ("Do EM waves need a medium to travel?", "no; they can travel through a vacuum", ["yes, always", "only through air", "only through water"], "Light reaches us from the Sun."),
      ("What is the speed of EM waves in vacuum in terms of μ₀ and ε₀?", "1/√(μ₀ε₀)", ["√(μ₀ε₀)", "μ₀/ε₀", "μ₀ε₀"], "It equals 3 × 10⁸ m/s."),
      ("Which EM waves are used in microwave ovens to heat food?", "microwaves", ["X-rays", "gamma rays", "ultraviolet"], "Their frequency matches the resonant frequency of water molecules."),
      ("Which Indian scientist worked with millimetre-wavelength waves?", "Jagadish Chandra Bose", ["C. V. Raman", "Homi Bhabha", "S. N. Bose"], "In the 1890s, in Kolkata."),
      ("Do EM waves carry momentum?", "yes, and so they exert radiation pressure", ["no", "only gamma rays", "only in a medium"], "p = U/c.")]


# =================================================================== 9 ray optics
def rayo(k=None):
    k = k or ch(["mir", "lens", "P", "m", "prism", "tel", "mic", "lm", "app", "comb"])
    if k == "mir":
        f, u = -ri(5, 30), -ri(10, 60)
        if u == f or abs(u) <= abs(f):
            return None
        v = 1 / (1 / f - 1 / u)
        return N("An object is %d cm in front of a concave mirror of focal length %d cm. Where is the image? (1/v + 1/u = 1/f, distances in front of the mirror negative)" % (-u, -f), v,
                 [-v, 1 / (1 / f + 1 / u), f - u], " cm", "1/v = 1/f − 1/u = 1/(%d) − 1/(%d), v = <b>%s cm</b> (real, in front of the mirror)." % (f, u, nf(v)))
    if k == "lens":
        f, u = ri(5, 30), -ri(10, 60)
        if abs(u) <= f:
            return None
        v = 1 / (1 / f + 1 / u)
        return N("An object is %d cm from a convex lens of focal length %d cm. Where is the image? (1/v − 1/u = 1/f)" % (-u, f), v, [1 / (1 / f - 1 / u), -v, f + u if f + u else f], " cm",
                 "1/v = 1/f + 1/u = 1/%d + 1/(%d), v = <b>%s cm</b> (real, on the other side)." % (f, u, nf(v)))
    if k == "P":
        f = ch([10, 20, 25, 40, 50, 100, -20, -25, -40, -50])
        return N("What is the power of a lens of focal length %s cm?" % nf(f), 100 / f, [f / 100, 1 / f, -100 / f], " D", "P = 1/f (in metres) = 100/%s = <b>%s D</b>." % (nf(f), nf(100 / f)))
    if k == "m":
        f, u = ri(5, 30), -ri(10, 60)
        if abs(u) <= f:
            return None
        v = 1 / (1 / f + 1 / u)
        return N("An object is %d cm from a convex lens of focal length %d cm. What is the magnification? (m = v/u)" % (-u, f), v / u, [-v / u, u / v, v / f], "", "v = %s cm; m = v/u = <b>%s</b> (inverted)." % (nf(v), nf(v / u)))
    if k == "prism":
        A_, D = ch([60, 60, 60, 45]), ri(30, 50, 2)
        n = math.sin(math.radians((A_ + D) / 2)) / math.sin(math.radians(A_ / 2))
        return N("A prism of angle %d° gives a minimum deviation of %d°. What is the refractive index of its glass?" % (A_, D), n, [math.sin(math.radians(A_ + D)) / math.sin(math.radians(A_)), (A_ + D) / A_, math.sin(math.radians(D)) / math.sin(math.radians(A_ / 2))], "",
                 "n = sin((A + D)/2)/sin(A/2) = <b>%s</b>." % nf(n))
    if k == "tel":
        fo, fe = ri(50, 200, 10), ri(2, 10)
        return N("An astronomical telescope has an objective of focal length %d cm and an eyepiece of %d cm. What is its magnifying power in normal adjustment?" % (fo, fe), fo / fe, [fe / fo, fo * fe, fo + fe], "", "m = f<sub>o</sub>/f<sub>e</sub> = <b>%s</b>; the tube length is %d cm." % (nf(fo / fe), fo + fe))
    if k == "mic":
        fe = ch([2.5, 5, 10, 25 / 3, 5])
        return N("What is the angular magnification of a simple microscope (magnifying glass) of focal length %s cm when the image is at the near point, 25 cm?" % nf(fe), 1 + 25 / fe, [25 / fe, 25 * fe, 1 - 25 / fe], "", "m = 1 + D/f = 1 + 25/%s = <b>%s</b>." % (nf(fe), nf(1 + 25 / fe)))
    if k == "lm":
        n, R1 = ch([1.5, 1.6, 1.4]), ri(10, 40, 5)
        f = 1 / ((n - 1) * (2 / R1))
        return N("A biconvex lens has both radii of curvature %d cm and refractive index %s. What is its focal length? (lens maker's formula)" % (R1, nf(n)), f, [1 / ((n - 1) / R1), R1 / 2, R1 * n], " cm", "1/f = (n − 1)(1/R₁ − 1/R₂) = (%s)(2/%d), f = <b>%s cm</b>." % (nf(n - 1), R1, nf(f)))
    if k == "app":
        d, n = ri(1, 10) * 10, ch([1.33, 1.5])
        return N("A coin lies at the bottom of a tank %d cm deep filled with a liquid of refractive index %s. How deep does it appear from above?" % (d, nf(n)), d / n, [d * n, d - n, d / n / 2], " cm", "Apparent depth = real depth ÷ n = <b>%s cm</b>." % nf(d / n))
    f1, f2 = ch([10, 15, 20, 25, 30, 40, 50]), ch([-10, -15, -20, -25, -40, -50, 10, 20, 50])
    if f1 + f2 == 0 or f1 == f2:
        return None
    return N("Two thin lenses of focal lengths %d cm and %d cm are placed in contact. What is the focal length of the combination?" % (f1, f2), 1 / (1 / f1 + 1 / f2), [f1 + f2, f1 * f2 / 100, 1 / (1 / f1 - 1 / f2)], " cm",
             "1/F = 1/f₁ + 1/f₂, so F = <b>%s cm</b>." % nf(1 / (1 / f1 + 1 / f2))) if f1 + f2 else None


B9 = [("What is total internal reflection?", "complete reflection of light at a boundary when it goes from a denser to a rarer medium at an angle greater than the critical angle", ["refraction into a denser medium", "partial reflection", "absorption of light"], "Used in optical fibres."),
      ("Why does a diamond sparkle?", "its critical angle is small (about 24°), so light is totally internally reflected many times", ["it emits light", "it is very hard", "it is transparent"], "n = 2.42."),
      ("Why is the sky blue?", "air molecules scatter short (blue) wavelengths much more than long ones", ["the sea reflects blue light", "the Sun is blue", "air absorbs red light"], "Scattering ∝ 1/λ⁴."),
      ("Why does the Sun look reddish at sunrise and sunset?", "light travels through more air, so most blue light is scattered away", ["the Sun cools down", "the Earth is red", "red light is scattered most"], "Mostly red reaches the eye."),
      ("What is the focal length of a plane mirror?", "infinity", ["zero", "1 m", "equal to its size"], "Its power is zero."),
      ("A convex mirror is used as a rear-view mirror. Why?", "it always gives an erect, diminished image with a wide field of view", ["it magnifies", "it gives real images", "it is cheaper"], "It shows more of the road."),
      ("What is dispersion of light?", "splitting of white light into its colours", ["bending of light", "reflection of light", "scattering of light"], "Different colours have different refractive indices."),
      ("Which colour is deviated most by a glass prism?", "violet", ["red", "yellow", "green"], "Glass has the highest refractive index for violet."),
      ("What is the power of a combination of lenses in contact?", "the sum of their powers", ["the product of their powers", "the difference of their powers", "always zero"], "P = P₁ + P₂."),
      ("What is the sign of the focal length of a concave lens (Cartesian sign convention)?", "negative", ["positive", "zero", "it has no sign"], "A convex lens has a positive focal length."),
      ("Where must an object be placed for a convex lens to give a virtual, erect, magnified image?", "between the lens and its focus", ["beyond 2F", "at F", "at 2F"], "This is how a magnifying glass works."),
      ("What is the least distance of distinct vision for a normal eye?", "about 25 cm", ["about 2.5 cm", "about 1 m", "infinity"], "It is called the near point."),
      ("Why are reflecting telescopes preferred for large telescopes?", "mirrors have no chromatic aberration and are easier to support", ["mirrors are cheaper always", "lenses cannot focus starlight", "mirrors magnify more"], "e.g. Cassegrain telescopes."),
      ("What is a mirage?", "an image of the sky seen as water on a hot road, due to total internal reflection in hot air layers", ["a reflection from water", "a rainbow", "a shadow"], "Hot air near the ground is optically rarer."),
      ("What is the critical angle for glass of refractive index 1.5 (approximately)?", "about 42°", ["about 24°", "about 49°", "about 90°"], "sin C = 1/n.")]


# =================================================================== 10 wave optics
def wo(k=None):
    k = k or ch(["ss", "brew", "malus", "ref", "fw"])
    if k == "ss":
        lam, a, D = ri(400, 700, 50), rf(0.1, 0.5, 0.05), rf(1, 2, 0.5)
        w = 2 * lam * 1e-9 * D / (a * 1e-3)
        return N("Light of wavelength %d nm passes through a single slit of width %s mm onto a screen %s m away. What is the width of the central bright band?" % (lam, nf(a), nf(D)), w * 1000,
                 [w * 500, lam * 1e-9 * D / (a * 1e-3) * 2000 / 4, w * 1e6], " mm", "Width = 2λD/a = <b>%s mm</b>." % nf(w * 1000))
    if k == "brew":
        n = ch([1.33, 1.5, 1.6, 1.73, 1.0 + 0.732])
        ang = math.degrees(math.atan(n))
        return N("At what angle of incidence is light reflected from glass of refractive index %s completely polarised? (Brewster's law)" % nf(n), ang, [math.degrees(math.asin(1 / n)), 90 - ang, math.degrees(math.atan(1 / n)) + 10], "°",
                 "tan i<sub>B</sub> = n, so i<sub>B</sub> = <b>%s°</b>." % nf(ang))
    if k == "malus":
        I0, th = ri(10, 100, 10), ch([30, 45, 60])
        return N("Polarised light of intensity %d W/m² falls on an analyser whose axis is at %d° to the polarisation. What intensity comes through? (Malus's law)" % (I0, th), I0 * math.cos(math.radians(th)) ** 2,
                 [I0 * math.cos(math.radians(th)), I0 * math.sin(math.radians(th)) ** 2, I0 / 2], " W/m²", "I = I₀ cos²θ = <b>%s W/m²</b>." % nf(I0 * math.cos(math.radians(th)) ** 2))
    if k == "ref":
        n, lam = ch([1.33, 1.5, 1.6]), ri(400, 700, 50)
        return N("Light of wavelength %d nm in air enters glass of refractive index %s. What is its wavelength in the glass?" % (lam, nf(n)), lam / n, [lam * n, lam, lam - n], " nm", "λ = λ₀/n = <b>%s nm</b>; the frequency does not change." % nf(lam / n))
    I0 = ri(10, 100, 10)
    return N("Unpolarised light of intensity %d W/m² passes through a polaroid. What is the transmitted intensity?" % I0, I0 / 2, [I0, I0 / 4, 0], " W/m²", "A polaroid passes half of unpolarised light: <b>%s W/m²</b>." % nf(I0 / 2))


B10 = [("What is a wavefront?", "a surface of points that vibrate in the same phase", ["a ray of light", "the speed of a wave", "a shadow"], "Rays are perpendicular to wavefronts."),
       ("What does Huygens' principle say?", "every point on a wavefront acts as a source of secondary wavelets", ["light travels in straight lines only", "light is a particle", "waves cannot interfere"], "The new wavefront is the envelope of the wavelets."),
       ("What are coherent sources?", "sources with the same frequency and a constant phase difference", ["any two bulbs", "sources of different colours", "very bright sources"], "Needed for a steady interference pattern."),
       ("Why can two separate bulbs not give a steady interference pattern?", "they are not coherent; their phase difference changes randomly", ["they are too bright", "their light is polarised", "they are too far apart"], "Young used one source and two slits."),
       ("What is the condition for constructive interference?", "path difference = nλ", ["path difference = (n + ½)λ", "path difference = λ/4", "no path difference ever"], "Bright fringes form."),
       ("What is the condition for destructive interference?", "path difference = (n + ½)λ", ["path difference = nλ", "path difference = 2λ", "zero path difference"], "Dark fringes form."),
       ("What happens to the fringe width in Young's experiment if the slits are moved closer together?", "it increases", ["it decreases", "it stays the same", "the fringes vanish"], "β = λD/d."),
       ("What happens to the fringes if the whole apparatus is put in water?", "the fringe width decreases", ["it increases", "it stays the same", "the fringes disappear"], "λ becomes λ/n."),
       ("What is diffraction?", "the spreading of waves around an obstacle or through a gap", ["reflection from a mirror", "splitting into colours", "absorption of light"], "It is clearest when the gap is about the wavelength."),
       ("Which property shows that light is a transverse wave?", "polarisation", ["interference", "diffraction", "reflection"], "Longitudinal waves cannot be polarised."),
       ("What does a polaroid do?", "it lets through light vibrating in one direction only", ["it splits light into colours", "it magnifies", "it reflects all light"], "Used in sunglasses and 3D glasses."),
       ("In Young's experiment, what is at the centre of the screen?", "a bright fringe", ["a dark fringe", "nothing", "a coloured band always"], "The path difference is zero there."),
       ("What happens to the central maximum in single-slit diffraction if the slit is made narrower?", "it becomes wider", ["it becomes narrower", "it disappears", "it stays the same"], "Width = 2λD/a.")]


# =================================================================== 11 dual nature
def dn(k=None):
    k = k or ch(["V0", "Kmax", "lamV", "f0", "lam0"])
    if k == "V0":
        K_ = rf(0.5, 4, 0.1)
        return N("The maximum kinetic energy of photoelectrons is %s eV. What is the stopping potential?" % nf(K_), K_, [K_ * 1.6e-19, K_ / 1.6e-19, K_ * 2], " V", "eV₀ = K<sub>max</sub>, so V₀ = <b>%s V</b>." % nf(K_))
    if k == "Kmax":
        hv, phi = rf(3, 8, 0.1), rf(1.8, 5, 0.1)
        if hv <= phi:
            return None
        return N("Photons of energy %s eV fall on a metal of work function %s eV. What is the maximum kinetic energy of the photoelectrons?" % (nf(hv), nf(phi)), hv - phi, [hv + phi, hv, phi], " eV",
                 "K<sub>max</sub> = hν − φ₀ = <b>%s eV</b>." % nf(hv - phi))
    if k == "lamV":
        V = ch([25, 49, 64, 100, 144, 150, 400, 900, 1600, 2500, 10000])
        return N("Electrons are accelerated through %d V. What is their de Broglie wavelength? (λ = 1.227/√V nm)" % V, 1.227 / math.sqrt(V), [1.227 / V, 1.227 * math.sqrt(V), 12.27 / math.sqrt(V)], " nm",
                 "λ = 1.227/√%d = <b>%s nm</b>." % (V, nf(1.227 / math.sqrt(V))))
    if k == "f0":
        phi = rf(1.8, 5, 0.1)
        return N("A metal has a work function of %s eV. What is its threshold frequency? (h = 6.63 × 10⁻³⁴ J s, 1 eV = 1.6 × 10⁻¹⁹ J)" % nf(phi), phi * QE / H, [phi / H, H / (phi * QE), phi * QE * H], " Hz",
                 "ν₀ = φ₀/h = %s × 1.6 × 10⁻¹⁹ ÷ 6.63 × 10⁻³⁴ = <b>%s Hz</b>." % (nf(phi), nf(phi * QE / H)))
    phi = rf(1.8, 5, 0.1)
    return N("A metal has a work function of %s eV. What is its threshold wavelength? (hc = 1240 eV nm)" % nf(phi), 1240 / phi, [phi * 1240, 1240 / phi / 2, 124 / phi], " nm", "λ₀ = hc/φ₀ = 1240/%s = <b>%s nm</b>." % (nf(phi), nf(1240 / phi)))


B11 = [("What does the photoelectric effect show about light?", "light comes in packets of energy (photons)", ["light is only a wave", "light has no energy", "light travels slowly"], "Einstein explained it in 1905."),
       ("What happens to the number of photoelectrons if the intensity of light is increased (above threshold)?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "The maximum kinetic energy stays the same."),
       ("What happens to the maximum kinetic energy of photoelectrons if the frequency of light is increased?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "K<sub>max</sub> = hν − φ₀."),
       ("Why is there no photoemission below the threshold frequency, however bright the light?", "each photon has too little energy to free an electron", ["the light is too dim", "the metal is too cold", "electrons are too heavy"], "One photon frees one electron."),
       ("Is there a time lag between light falling on a metal and electrons being emitted?", "no, emission is practically instantaneous", ["yes, several seconds", "yes, if the light is dim", "only for red light"], "This supports the photon picture."),
       ("What is the work function of a metal?", "the minimum energy needed to remove an electron from its surface", ["the energy of a photon", "the kinetic energy of electrons", "the charge of an electron"], "It is measured in eV."),
       ("Which experiment confirmed the wave nature of electrons?", "the Davisson–Germer experiment", ["Millikan's oil drop experiment", "Rutherford's scattering experiment", "Young's double-slit experiment with light"], "Electrons were diffracted by a nickel crystal."),
       ("For the same speed, which has the shorter de Broglie wavelength, an electron or a proton?", "the proton", ["the electron", "both are equal", "neither has a wavelength"], "λ = h/mv; the proton is heavier."),
       ("Why do we not notice the wave nature of a cricket ball?", "its de Broglie wavelength is far too small to detect", ["it has no wavelength", "it is not moving", "it is too light"], "Its mass is large."),
       ("What does the stopping potential depend on?", "the frequency of light and the metal, not the intensity", ["the intensity only", "the colour of the metal", "the size of the plate"], "eV₀ = hν − φ₀."),
       ("What is the slope of a graph of stopping potential against frequency?", "h/e", ["e/h", "h", "φ₀"], "It is the same for all metals."),
       ("What is the energy of a photon in terms of its wavelength?", "hc/λ", ["hλ/c", "h/λ", "cλ"], "Shorter wavelength means more energy.")]


# =================================================================== 12 atoms
def at(k=None):
    k = k or ch(["closest", "E", "r", "ion", "trans"])
    if k == "closest":
        K_ = rf(2, 9, 0.5)
        Z = ch([(79, "gold"), (47, "silver"), (29, "copper")])
        d = KC * 2 * Z[0] * QE * QE / (K_ * 1e6 * QE)
        return N("An α-particle of energy %s MeV moves straight towards a %s nucleus (Z = %d). What is its distance of closest approach? (1/4πε₀ = 9 × 10⁹ N m² C⁻²)" % (nf(K_), Z[1], Z[0]), d,
                 [d * 2, KC * Z[0] * QE * QE / (K_ * 1e6 * QE), d / 1e3], " m", "d = k(2e)(Ze)/K = <b>%s m</b>." % nf(d))
    if k == "ion":
        n = ri(1, 7)
        return N("How much energy is needed to ionise a hydrogen atom from the n = %d level? (E<sub>n</sub> = −13.6/n² eV)" % n, 13.6 / n / n, [13.6 / n, 13.6, 13.6 * n * n], " eV", "Ionisation energy = 0 − E<sub>n</sub> = <b>%s eV</b>." % nf(13.6 / n / n))
    if k == "trans":
        n1 = ri(1, 3)
        n2 = ri(n1 + 1, 6)
        dE = 13.6 * (1 / n1 ** 2 - 1 / n2 ** 2)
        return N("What is the wavelength of the photon emitted when a hydrogen atom goes from n = %d to n = %d? (hc = 1240 eV nm)" % (n2, n1), 1240 / dE, [1240 * dE, 1240 / (13.6 / n1 ** 2), 1240 / dE / 2], " nm",
                 "ΔE = 13.6(1/%d² − 1/%d²) = %s eV; λ = 1240/ΔE = <b>%s nm</b>." % (n1, n2, nf(dE), nf(1240 / dE)))
    return in_s11c.b_bohr(ch(["En", "r", "dE", "series", "lam", "Z"]))


B12 = [("What did most α-particles do in the Geiger–Marsden experiment?", "they passed straight through the gold foil", ["they bounced back", "they stuck to the foil", "they were absorbed"], "So most of the atom is empty space."),
       ("What did the few α-particles deflected through large angles show?", "the positive charge and mass are concentrated in a tiny nucleus", ["electrons are heavy", "the atom is a solid sphere", "gold is magnetic"], "Rutherford's nuclear model."),
       ("Why could Rutherford's model not explain the stability of atoms?", "an orbiting electron should radiate energy and spiral into the nucleus", ["it had no nucleus", "it had no electrons", "it predicted continuous spectra correctly"], "Bohr added stationary orbits."),
       ("What is Bohr's quantisation condition?", "the angular momentum of the electron is a whole-number multiple of h/2π", ["the energy is zero", "the speed is constant", "the radius is constant"], "mvr = nh/2π."),
       ("What is the ground-state energy of the hydrogen atom?", "−13.6 eV", ["+13.6 eV", "0 eV", "−3.4 eV"], "It takes 13.6 eV to ionise it."),
       ("Which series of the hydrogen spectrum lies in the visible region?", "the Balmer series", ["the Lyman series", "the Paschen series", "the Pfund series"], "Lyman is ultraviolet; Paschen is infrared."),
       ("What is the radius of the first Bohr orbit of hydrogen?", "0.53 Å (5.3 × 10⁻¹¹ m)", ["5.3 Å", "0.053 Å", "53 Å"], "r ∝ n²."),
       ("How does the radius of a Bohr orbit depend on n?", "r ∝ n²", ["r ∝ n", "r ∝ 1/n", "r ∝ 1/n²"], "The energy goes as −1/n²."),
       ("What is the impact parameter in α-particle scattering?", "the perpendicular distance of the α-particle's initial path from the nucleus", ["the radius of the nucleus", "the speed of the particle", "the angle of scattering"], "A small impact parameter gives a large deflection."),
       ("Why does the hydrogen spectrum consist of lines?", "electrons can only jump between fixed energy levels", ["hydrogen is a gas", "light is a wave", "atoms are large"], "Each line has a definite frequency."),
       ("How many spectral lines can be emitted when electrons fall from n = 4 to the ground state (all routes)?", "6", ["3", "4", "10"], "n(n − 1)/2 = 6."),
       ("Does Bohr's model work for helium (neutral)?", "no, only for one-electron (hydrogen-like) atoms", ["yes, perfectly", "only for heavy atoms", "yes, with no changes"], "It ignores electron–electron effects.")]


# =================================================================== 13 nuclei
NUC = [("helium-4", 2, 4, 4.00260), ("lithium-7", 3, 7, 7.01600), ("carbon-12", 6, 12, 12.0), ("nitrogen-14", 7, 14, 14.00307), ("oxygen-16", 8, 16, 15.99491), ("neon-20", 10, 20, 19.99244),
       ("iron-56", 26, 56, 55.93494), ("deuterium (²H)", 1, 2, 2.01410), ("beryllium-9", 4, 9, 9.01218), ("boron-11", 5, 11, 11.00931), ("sodium-23", 11, 23, 22.98977),
       ("aluminium-27", 13, 27, 26.98154), ("chlorine-35", 17, 35, 34.96885), ("copper-63", 29, 63, 62.92960), ("uranium-238", 92, 238, 238.05079), ("calcium-40", 20, 40, 39.96259)]


def nu(k=None):
    k = k or ch(["md", "BE", "BEn", "R", "dens", "E"])
    nm, Z, A_, m = ch(NUC)
    mp, mn = 1.00783, 1.00867
    dm = Z * mp + (A_ - Z) * mn - m
    if k == "md":
        return N("The atomic mass of %s is %s u. Taking m(¹H) = 1.00783 u and m<sub>n</sub> = 1.00867 u, what is its mass defect?" % (nm, nf(m, 7)), dm, [dm * 931.5, Z * mp + A_ * mn - m, dm / A_], " u",
                 "Δm = Zm<sub>H</sub> + (A − Z)m<sub>n</sub> − M = <b>%s u</b>." % nf(dm, 4), sf=4)
    if k in ("BE", "BEn"):
        be = dm * 931.5
        if k == "BE":
            return N("The mass defect of %s is %s u. What is its binding energy? (1 u = 931.5 MeV/c²)" % (nm, nf(dm, 4)), be, [be / A_, dm * 931.5 * 1e6, dm / 931.5], " MeV", "E = Δm × 931.5 = <b>%s MeV</b>." % nf(be))
        return N("The binding energy of %s is %s MeV. What is its binding energy per nucleon? (A = %d)" % (nm, nf(be), A_), be / A_, [be * A_, be / Z, be], " MeV", "BE/A = %s ÷ %d = <b>%s MeV</b>." % (nf(be), A_, nf(be / A_)))
    if k == "R":
        A2 = ch([8, 27, 64, 125, 216, 343, 512, 729, 1000])
        R_ = 1.2 * A2 ** (1 / 3)
        return N("What is the radius of a nucleus of mass number %d? (R = R₀A<sup>1/3</sup>, R₀ = 1.2 fm)" % A2, R_, [1.2 * A2, 1.2 * A2 ** 0.5, 1.2 / A2 ** (1 / 3)], " fm", "R = 1.2 × %d<sup>1/3</sup> = <b>%s fm</b>." % (A2, nf(R_)))
    if k == "dens":
        a, b = ch([(8, 27), (27, 64), (64, 125), (8, 64), (1, 27), (27, 216)])
        return N("What is the ratio of the radii of nuclei with mass numbers %d and %d?" % (a, b), (a / b) ** (1 / 3), [a / b, (a / b) ** 0.5, (b / a) ** (1 / 3)], "",
                 "R ∝ A<sup>1/3</sup>, so R₁/R₂ = (%d/%d)<sup>1/3</sup> = <b>%s</b>; nuclear density is the same for all nuclei." % (a, b, nf((a / b) ** (1 / 3))))
    g = rf(0.1, 10, 0.1)
    return N("How much energy is released if %s g of matter is converted completely into energy? (c = 3 × 10⁸ m/s)" % nf(g), g * 1e-3 * C * C, [g * C * C, g * 1e-3 * C, g * 1e-3 * C * C / 2], " J", "E = mc² = %s × 10⁻³ × (3 × 10⁸)² = <b>%s J</b>." % (nf(g), nf(g * 1e-3 * C * C)))


B13 = [("What are isotones?", "nuclei with the same number of neutrons", ["nuclei with the same number of protons", "nuclei with the same mass number", "ions"], "e.g. ¹⁹⁸Hg and ¹⁹⁷Au both have 118 neutrons."),
       ("What is the nuclear force like?", "very strong, short-range and charge-independent", ["weak and long-range", "only attractive between protons", "the same as gravity"], "It holds nucleons together within a few fm."),
       ("What is nuclear fission?", "a heavy nucleus splitting into two lighter nuclei with release of energy", ["light nuclei joining", "an electron leaving an atom", "emission of light"], "e.g. uranium-235 in reactors."),
       ("What is nuclear fusion?", "light nuclei joining to form a heavier nucleus with release of energy", ["a heavy nucleus splitting", "burning of hydrogen in oxygen", "a chemical reaction"], "It powers the Sun."),
       ("Why does fusion need very high temperatures?", "the nuclei must overcome their electrostatic repulsion", ["to melt the fuel", "to make electrons faster", "to stop radiation"], "Millions of kelvin are needed."),
       ("Which nuclei have the highest binding energy per nucleon?", "nuclei of mass number about 56, such as iron", ["hydrogen", "uranium", "helium only"], "About 8.8 MeV per nucleon."),
       ("Why do heavy nuclei release energy when they split?", "the products have a higher binding energy per nucleon", ["the products are heavier", "mass is created", "the nucleus absorbs energy"], "The extra binding energy is released."),
       ("What is one atomic mass unit in energy terms?", "931.5 MeV", ["1 MeV", "13.6 eV", "1.6 × 10⁻¹⁹ J"], "From E = mc²."),
       ("Is the density of nuclear matter the same for all nuclei?", "yes, about 2.3 × 10¹⁷ kg/m³", ["no, it rises with A", "no, it falls with A", "it is the same as water"], "Because R ∝ A<sup>1/3</sup>."),
       ("What is the mass defect?", "the difference between the total mass of the separate nucleons and the mass of the nucleus", ["the mass of electrons", "the mass lost by burning", "the mass of a neutron"], "It appears as binding energy."),
       ("What holds the protons together in a nucleus despite their repulsion?", "the strong nuclear force", ["gravity", "magnetism", "the weak force only"], "It is much stronger at short range."),
       ("What is a chain reaction in fission?", "neutrons released from one fission cause further fissions", ["fusion of chains of nuclei", "a reaction with no neutrons", "radioactive decay"], "It is controlled in a reactor.")]


# =================================================================== 14 semiconductor electronics
def sc(k=None):
    k = k or ch(["ni", "half", "full", "dop"])
    if k == "ni":
        ni, ne = ch([1.5e16, 1e16, 2e16, 5e15]), ri(1, 9) * 10 ** ri(20, 22)
        return N("A doped semiconductor has an intrinsic carrier density of %s m⁻³ and %s electrons per m³. What is the hole density? (n<sub>e</sub>n<sub>h</sub> = n<sub>i</sub>²)" % (nf(ni), nf(ne)), ni * ni / ne,
                 [ne, ni, ne / ni], " m⁻³", "n<sub>h</sub> = n<sub>i</sub>²/n<sub>e</sub> = <b>%s m⁻³</b>." % nf(ni * ni / ne))
    if k in ("half", "full"):
        f = ch([50, 60, 100, 200, 400, 500])
        if k == "half":
            return N("A half-wave rectifier is fed with AC of frequency %d Hz. What is the frequency of the output ripple?" % f, f, [2 * f, f / 2, 0], " Hz", "One pulse per cycle: <b>%d Hz</b>." % f)
        return N("A full-wave rectifier is fed with AC of frequency %d Hz. What is the frequency of the output ripple?" % f, 2 * f, [f, f / 2, 4 * f], " Hz", "Two pulses per cycle: <b>%d Hz</b>." % (2 * f))
    nd = ri(1, 99)
    return N("Silicon has 5 × 10²⁸ atoms per m³. It is doped with arsenic at %d parts per million. How many arsenic atoms are there per m³?" % nd, 5e28 * nd * 1e-6, [5e28 / nd, 5e28 * nd * 1e-3, 5e28 * nd * 1e-4], " m⁻³",
             "5 × 10²⁸ × %d × 10⁻⁶ = <b>%s m⁻³</b>." % (nd, nf(5e28 * nd * 1e-6)))


SEMI = {"an n-type dopant for silicon": ["arsenic", "phosphorus", "antimony"], "a p-type dopant for silicon": ["boron", "aluminium", "indium", "gallium"],
        "an elemental semiconductor": ["silicon", "germanium"], "a compound semiconductor": ["gallium arsenide", "cadmium sulphide", "indium phosphide", "zinc oxide", "silicon carbide"]}
B14 = [("What is the energy gap of an insulator like?", "large, more than 3 eV", ["zero", "less than 0.1 eV", "negative"], "Diamond has about 6 eV."),
       ("What is the band structure of a metal?", "the valence and conduction bands overlap", ["there is a large gap", "there is no valence band", "the conduction band is empty"], "So electrons move freely."),
       ("What is the energy gap of silicon?", "about 1.1 eV", ["about 0.7 eV", "about 6 eV", "zero"], "Germanium is about 0.7 eV."),
       ("What are the majority carriers in an n-type semiconductor?", "electrons", ["holes", "protons", "positive ions"], "Donor atoms give extra electrons."),
       ("What are the majority carriers in a p-type semiconductor?", "holes", ["electrons", "neutrons", "negative ions"], "Acceptor atoms create holes."),
       ("Is an n-type semiconductor negatively charged?", "no, it is electrically neutral", ["yes", "only when hot", "only in light"], "The donor ions balance the electrons."),
       ("What is the depletion region of a p-n junction?", "a region near the junction with no free charge carriers", ["the p side", "the n side", "a metal contact"], "It contains fixed ions."),
       ("What happens to the depletion layer under forward bias?", "it becomes narrower", ["it becomes wider", "it disappears and reappears", "it stays the same"], "Current flows easily."),
       ("What happens to the depletion layer under reverse bias?", "it becomes wider", ["it becomes narrower", "it vanishes", "it stays the same"], "Only a tiny reverse current flows."),
       ("What is the barrier potential of a silicon p-n junction?", "about 0.7 V", ["about 0.3 V", "about 7 V", "about 0.07 V"], "Germanium is about 0.3 V."),
       ("What is a rectifier?", "a circuit that converts AC into DC", ["a circuit that amplifies", "a circuit that stores charge", "a circuit that makes AC"], "Diodes conduct only one way."),
       ("Why is a capacitor used after a rectifier?", "to smooth (filter) the ripples in the output", ["to increase the ripple", "to make AC", "to break the circuit"], "It charges and discharges between peaks."),
       ("What is an intrinsic semiconductor?", "a pure semiconductor with equal numbers of electrons and holes", ["a doped semiconductor", "a metal", "an insulator"], "n<sub>e</sub> = n<sub>h</sub> = n<sub>i</sub>."),
       ("What happens to the conductivity of a semiconductor when it is heated?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "More electron–hole pairs form.")]


def UNITS():
    b = {k: B(globals()["B%d" % k]) for k in range(1, 15)}
    from in_s11b import OD
    emw = pairs(EMW, "What is a common use of %s?", "Which part of the electromagnetic spectrum is used for %s?")
    mag = OD(MAG, "Which of these is %s?", "Which of these is NOT %s?")
    semi = OD(SEMI, "Which of these is %s?", "Which of these is NOT %s?")
    S = lambda *a, **kw: SU(PH, *a, **kw)
    return [
        S(1, "electric-charges-and-fields", 1,
          "Electric charges, conservation of charge, Coulomb's law – force between two point charges, forces between multiple charges; superposition principle and continuous charge distribution. Electric field, electric field due to a point charge, electric field lines, electric dipole, electric field due to a dipole, torque on a dipole in uniform electric field. Electric flux, statement of Gauss's theorem and its applications to find field due to infinitely long straight wire, uniformly charged infinite plane sheet and uniformly charged thin spherical shell.",
          "Electric Charges and Fields", "electric charges and fields",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 1 Electric Charges and Fields: quantisation of charge, Coulomb's law, electric field, dipoles, electric flux and Gauss's law. 100 questions with answers.",
          "F = kq₁q₂/r²; E = kq/r².", "Gauss's law: total flux = q/ε₀.",
          "<p>Charge is quantised (q = ne, e = 1.6 × 10⁻¹⁹ C) and conserved. Coulomb's law gives the force F = kq₁q₂/r² with k = 1/4πε₀ = 9 × 10⁹ N m² C⁻². The electric field E = F/q is kq/r² for a point charge; field lines start on positive and end on negative charges.</p>"
          "<p>A dipole has moment p = q × 2a; in a uniform field it feels no net force but a torque pE sin θ. Gauss's law says the flux through a closed surface is q/ε₀, giving E = λ/2πε₀r for a long wire and σ/2ε₀ for a plane sheet.</p>",
          [("2 μC and 3 μC, 0.3 m apart?", ["9 × 10⁹ × 6 × 10⁻¹² ÷ 0.09"], "0.6 N"), ("Flux from 1 μC in a cube?", ["q/ε₀"], "1.13 × 10⁵ N m²/C")],
          ["Forgetting to square r.", "Leaving μC unconverted.", "Thinking the cube's size changes the flux."],
          [("What is Gauss's law?", "The total electric flux through any closed surface equals the enclosed charge divided by ε₀."),
           ("What is the net force on a dipole in a uniform field?", "Zero; the forces on the two charges cancel, though a torque pE sin θ may act.")],
          lambda: [("Electric charge", [(K(ec, "n", "q"), 15), (b[1], 5)]), ("Coulomb's law", [(K(ec, "F"), 12), (A(P.f_elec, "coul"), 6), (b[1], 2)]), ("Electric field", [(K(ec, "E"), 11), (A(P.f_elec, "E", "plates"), 8), (b[1], 1)]),
                   ("Electric dipole", [(K(ec, "dip", "tq"), 18), (b[1], 2)]), ("Electric flux and Gauss's law", [(K(ec, "flux", "sheet", "line"), 18), (b[1], 2)])]),
        S(2, "electrostatic-potential-and-capacitance", 2,
          "Electric potential, potential difference, electric potential due to a point charge, a dipole and system of charges; equipotential surfaces, electrical potential energy of a system of two point charges and of electric dipole in an electrostatic field. Conductors and insulators, free charges and bound charges inside a conductor. Dielectrics and electric polarization, capacitors and capacitance, combination of capacitors in series and in parallel, capacitance of a parallel plate capacitor with and without dielectric medium between the plates, energy stored in a capacitor.",
          "Electrostatic Potential and Capacitance", "electrostatic potential and capacitance",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 2 Electrostatic Potential and Capacitance: potential, potential energy, equipotentials, capacitors in series and parallel, dielectrics and stored energy. 100 questions with answers.",
          "V = kq/r; C = Q/V.", "Energy in a capacitor = ½CV².",
          "<p>Electric potential V = kq/r is the work done per unit charge in bringing a charge from infinity; W = qV. Two charges have potential energy kq₁q₂/r. Equipotential surfaces are perpendicular to field lines, and no work is done along them.</p>"
          "<p>A capacitor stores charge Q = CV. A parallel plate capacitor has C = ε₀A/d, multiplied by K with a dielectric. In parallel C = C₁ + C₂; in series 1/C = 1/C₁ + 1/C₂. The stored energy is ½CV² = Q²/2C.</p>",
          [("2 μF and 3 μF in series?", ["6 ÷ 5"], "1.2 μF"), ("10 μF at 100 V. Energy?", ["½ × 10⁻⁵ × 10⁴"], "0.05 J")],
          ["Adding series capacitors directly.", "Using kq/r² for potential.", "Forgetting the ½ in ½CV²."],
          [("How do capacitors combine?", "In parallel the capacitances add; in series the reciprocals add."),
           ("What does a dielectric do to a capacitor?", "It increases the capacitance by its dielectric constant K.")],
          lambda: [("Electric potential", [(K(cp, "V"), 10), (A(P.f_elec, "Vpt"), 6), (b[2], 4)]), ("Work and potential energy", [(K(cp, "W", "U"), 16), (b[2], 4)]),
                   ("Capacitance", [(K(cp, "C", "K", "Q"), 16), (b[2], 4)]), ("Combining capacitors", [(K(cp, "ser", "par"), 16), (A(P.k_cap, "ser", "par"), 4)]),
                   ("Energy stored in a capacitor", [(K(cp, "E", "Eg"), 14), (A(P.k_cap, "E"), 6)])]),
        S(3, "current-electricity", 3,
          "Electric current, flow of electric charges in a metallic conductor, drift velocity, mobility and their relation with electric current; Ohm's law, V–I characteristics (linear and non-linear), electrical energy and power, electrical resistivity and conductivity, temperature dependence of resistance, internal resistance of a cell, potential difference and emf of a cell, combination of cells in series and in parallel, Kirchhoff's rules, Wheatstone bridge.",
          "Current Electricity", "current electricity",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 3 Current Electricity: current and drift velocity, Ohm's law, resistivity, resistors in series and parallel, power, cells, Kirchhoff's rules and the Wheatstone bridge. 100 questions with answers.",
          "V = IR; R = ρl/A.", "Kirchhoff: current in = current out; ΣV round a loop = 0.",
          "<p>Current I = Q/t = neAv<sub>d</sub>, where the drift velocity is only about a millimetre per second. Ohm's law V = IR holds for ohmic conductors; resistance R = ρl/A rises with temperature for metals. Resistors add in series and their reciprocals add in parallel; power is VI = I²R = V²/R.</p>"
          "<p>A cell of e.m.f. E and internal resistance r gives I = E/(R + r). Kirchhoff's junction rule (charge) and loop rule (energy) solve networks; a Wheatstone bridge balances when P/Q = R/S.</p>",
          [("P = 10, Q = 20, R = 15. S?", ["RQ/P"], "30 Ω"), ("E = 12 V, r = 1 Ω, R = 5 Ω. I?", ["12 ÷ 6"], "2 A")],
          ["Forgetting internal resistance.", "Thinking electrons move at light speed.", "Adding parallel resistances directly."],
          [("Why is drift velocity so small but a bulb lights at once?", "The electric field travels along the wire almost instantly, so all the free electrons start drifting together."),
           ("What is a balanced Wheatstone bridge?", "When P/Q = R/S no current flows through the galvanometer.")],
          lambda: [("Current and drift velocity", [(K(cu, "drift"), 8), (A(P.e_charge, "Q", "I", "N"), 8), (b[3], 4)]), ("Resistance and resistivity", [(A(P.e_resist, "ohm", "rho", "rho2"), 14), (K(cu, "R2"), 4), (b[3], 2)]),
                   ("Combining resistors and power", [(A(P.e_combo, "par2", "mix", "ser"), 12), (A(P.e_power, "I2R", "V2R", "IV"), 8)]), ("Cells and internal resistance", [(A(P.e_emf, "I", "V", "r"), 12), (K(cu, "cells"), 6), (b[3], 2)]),
                   ("Kirchhoff's rules and bridges", [(K(cu, "wb", "mb", "kirch"), 16), (b[3], 4)])]),
        S(4, "moving-charges-and-magnetism", 4,
          "Concept of magnetic field, Oersted's experiment. Biot–Savart law and its application to current carrying circular loop. Ampere's law and its applications to infinitely long straight wire, straight solenoid (only qualitative treatment), force on a moving charge in uniform magnetic and electric fields. Force on a current-carrying conductor in a uniform magnetic field, force between two parallel current-carrying conductors – definition of ampere, torque experienced by a current loop in uniform magnetic field; current loop as a magnetic dipole and its magnetic dipole moment, moving coil galvanometer – its current sensitivity and conversion to ammeter and voltmeter.",
          "Moving Charges and Magnetism", "moving charges and magnetism",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 4 Moving Charges and Magnetism: magnetic force on charges and wires, fields of wires, loops and solenoids, the cyclotron, parallel currents and the galvanometer. 100 questions with answers.",
          "F = qvB sin θ; F = BIl sin θ.", "B = μ₀I/2πr (wire); μ₀NI/2R (loop centre); μ₀nI (solenoid).",
          "<p>A magnetic field exerts a force qvB sin θ on a moving charge, at right angles to its velocity, so the charge moves in a circle of radius mv/qB and does no work. A wire in a field feels F = BIl sin θ. Currents make fields: μ₀I/2πr round a long wire, μ₀NI/2R at the centre of a loop and μ₀nI inside a solenoid.</p>"
          "<p>Parallel currents in the same direction attract. A current loop is a magnetic dipole with m = NIA. A galvanometer becomes an ammeter with a small shunt in parallel and a voltmeter with a large resistance in series.</p>",
          [("5 A, 0.1 m from a long wire?", ["2 × 10⁻⁷ × 5 ÷ 0.1"], "10⁻⁵ T"), ("Galvanometer to voltmeter?", ["series"], "large resistance in series")],
          ["Thinking a magnetic field speeds up a charge.", "Using μ₀I/2R for a long wire.", "Putting the shunt in series."],
          [("Why does a magnetic field do no work on a moving charge?", "The magnetic force is always perpendicular to the velocity, so the speed does not change."),
           ("How is a galvanometer made into an ammeter?", "By connecting a small shunt resistance in parallel so most of the current bypasses the coil.")],
          lambda: [("Force on moving charges", [(A(P.k_mag, "BQv", "r"), 13), (K(mg, "cyc"), 4), (b[4], 3)]), ("Force on a current", [(A(P.k_mag, "BIL"), 12), (K(mg, "par"), 6), (b[4], 2)]),
                   ("Fields of wires and loops", [(K(mg, "wire", "loop"), 16), (b[4], 4)]), ("Solenoids and Ampère's law", [(K(mg, "sol"), 14), (b[4], 2), (K(mg, "wire"), 4)]),
                   ("The galvanometer", [(K(mg, "shunt", "volt"), 19), (b[4], 1)])]),
        S(5, "magnetism-and-matter", 5,
          "Bar magnet, bar magnet as an equivalent solenoid (qualitative treatment only), magnetic field intensity due to a magnetic dipole (bar magnet) along its axis and perpendicular to its axis (qualitative treatment only), torque on a magnetic dipole (bar magnet) in a uniform magnetic field (qualitative treatment only), magnetic field lines. Magnetic properties of materials – para-, dia- and ferromagnetic substances with examples, magnetization of materials, effect of temperature on magnetic properties.",
          "Magnetism and Matter", "magnetism and matter",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 5 Magnetism and Matter: bar magnets, magnetic moment, torque and energy of a dipole, Gauss's law for magnetism, and dia-, para- and ferromagnetism. 100 questions with answers.",
          "τ = mB sin θ; U = −mB cos θ.", "Dia: weakly repelled; para: weakly attracted; ferro: strongly attracted.",
          "<p>A bar magnet behaves like a solenoid: its field lines are closed loops, so the net flux through any closed surface is zero and there are no magnetic monopoles. A magnetic dipole of moment m feels a torque mB sin θ and has potential energy −mB cos θ in a field.</p>"
          "<p>Materials respond differently: diamagnetic substances (bismuth, copper, water) have small negative susceptibility; paramagnetic ones (aluminium, oxygen) small positive susceptibility that falls with temperature (Curie's law); ferromagnetic ones (iron, cobalt, nickel) are strongly magnetised and become paramagnetic above the Curie temperature.</p>",
          [("m = 2 A m², B = 0.5 T, θ = 90°. τ?", ["mB"], "1 N m"), ("Copper is?", ["χ small, negative"], "diamagnetic")],
          ["Thinking a magnet cut in half gives separate poles.", "Saying copper is paramagnetic.", "Forgetting the minus sign in U = −mB cos θ."],
          [("Why are there no magnetic monopoles?", "Every magnet, however small, has both a north and a south pole; magnetic field lines form closed loops."),
           ("What happens to a ferromagnet above its Curie temperature?", "Its domains break up and it becomes paramagnetic.")],
          lambda: [("Bar magnets and field lines", [(b[5], 6), (K(mm, "m"), 14)]), ("Torque and energy of a dipole", [(K(mm, "tq", "U", "W"), 20)]), ("Magnetic materials", [(mag, 15), (b[5], 3), (K(mm, "chi"), 2)]),
                   ("Curie's law and magnetisation", [(K(mm, "chi"), 12), (mag, 6), (b[5], 2)]), ("Mixed problems", [(mag, 8), (K(mm, "m", "tq", "U"), 11), (b[5], 1)])]),
        S(6, "electromagnetic-induction", 6,
          "Electromagnetic induction; Faraday's laws, induced EMF and current; Lenz's law, self and mutual induction.",
          "Electromagnetic Induction", "electromagnetic induction",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 6 Electromagnetic Induction: magnetic flux, Faraday's and Lenz's laws, motional e.m.f., eddy currents, self and mutual inductance and the AC generator. 100 questions with answers.",
          "ε = −N dΦ/dt.", "The induced current opposes the change (Lenz).",
          "<p>Magnetic flux Φ = BA cos θ is measured in webers. Faraday's law says a changing flux linkage induces an e.m.f. ε = −N dΦ/dt; Lenz's law gives the minus sign — the induced current opposes the change, as energy conservation requires. A rod moving through a field has motional e.m.f. Blv.</p>"
          "<p>A changing current in a coil induces a back e.m.f. L dI/dt in itself (self-inductance) and M dI/dt in a nearby coil (mutual inductance). An inductor stores energy ½LI². Eddy currents are reduced by laminating cores.</p>",
          [("B = 0.5 T, l = 1 m, v = 4 m/s?", ["Blv"], "2 V"), ("L = 2 H, I = 3 A. Energy?", ["½ × 2 × 9"], "9 J")],
          ["Forgetting to multiply by the number of turns.", "Thinking Lenz's law helps the change.", "Using L I instead of ½LI²."],
          [("What is Lenz's law?", "The direction of an induced current is such that it opposes the change in flux producing it."),
           ("How are eddy currents reduced?", "By making cores from thin, insulated laminations.")],
          lambda: [("Magnetic flux", [(K(emi, "flux"), 10), (A(P.k_mag, "flux"), 6), (b[6], 4)]), ("Faraday's and Lenz's laws", [(K(emi, "rate"), 14), (b[6], 4), (A(P.k_mag, "emf"), 2)]),
                   ("Motional e.m.f.", [(K(emi, "Blv"), 16), (b[6], 2), (A(P.k_mag, "emf"), 2)]), ("Self and mutual inductance", [(K(emi, "Ldi", "M"), 19), (b[6], 1)]),
                   ("Energy and mixed problems", [(K(emi, "UL"), 14), (K(emi, "rate", "Blv"), 6)])]),
        S(7, "alternating-current", 7,
          "Alternating currents, peak and RMS value of alternating current/voltage; reactance and impedance; LCR series circuit (phasors only), resonance, power in AC circuits, power factor, wattless current. AC generator, transformer.",
          "Alternating Current", "alternating current",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 7 Alternating Current: rms and peak values, inductive and capacitive reactance, impedance, resonance, power factor and transformers. 100 questions with answers.",
          "V(rms) = V₀/√2.", "Z = √(R² + (X(L) − X(C))²); resonance at f₀ = 1/(2π√LC).",
          "<p>An AC voltage V₀ sin ωt has rms value V₀/√2; Indian mains is 220–230 V rms at 50 Hz. An inductor has reactance X<sub>L</sub> = ωL and makes the current lag by 90°; a capacitor has X<sub>C</sub> = 1/ωC and makes it lead by 90°.</p>"
          "<p>In a series LCR circuit Z = √(R² + (X<sub>L</sub> − X<sub>C</sub>)²); at resonance X<sub>L</sub> = X<sub>C</sub>, Z = R and the current is greatest. Average power is V<sub>rms</sub>I<sub>rms</sub> cos φ with power factor cos φ = R/Z. Transformers change voltage in the ratio of turns.</p>",
          [("V₀ = 311 V. Vrms?", ["311 ÷ 1.414"], "220 V"), ("R = 3, XL = 8, XC = 4. Z?", ["√(9 + 16)"], "5 Ω")],
          ["Adding X<sub>L</sub> and X<sub>C</sub>.", "Using peak values for power.", "Saying a capacitor passes DC."],
          [("What happens at resonance in a series LCR circuit?", "X<sub>L</sub> = X<sub>C</sub>, the impedance equals R and the current is a maximum."),
           ("What is the power factor?", "cos φ = R/Z, the fraction of V<sub>rms</sub>I<sub>rms</sub> that is actually used as power.")],
          lambda: [("Peak and rms values", [(K(ac, "rms", "peak"), 16), (b[7], 4)]), ("Reactance", [(K(ac, "XL", "XC"), 17), (b[7], 3)]), ("Impedance and resonance", [(K(ac, "Z", "f0"), 18), (b[7], 2)]),
                   ("Power factor", [(K(ac, "pf"), 5), (b[7], 2), (K(ac, "XL", "XC", "f0"), 13)]), ("Transformers and mixed problems", [(A(P.k_mag, "trans", "trI"), 14), (K(ac, "rms", "Z"), 6)])]),
        S(8, "electromagnetic-waves", 8,
          "Basic idea of displacement current, electromagnetic waves, their characteristics, their transverse nature (qualitative idea only). Electromagnetic spectrum (radio waves, microwaves, infrared, visible, ultraviolet, X-rays, gamma rays) including elementary facts about their uses.",
          "Electromagnetic Waves", "electromagnetic waves",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 8 Electromagnetic Waves: displacement current, properties of EM waves, c = fλ, E₀ = cB₀, and the uses of each part of the electromagnetic spectrum. 100 questions with answers.",
          "c = fλ = 3 × 10⁸ m/s in vacuum.", "Radio → microwave → IR → visible → UV → X-ray → gamma: λ gets shorter.",
          "<p>Maxwell added the displacement current, due to a changing electric field, and predicted electromagnetic waves: oscillating E and B fields, perpendicular to each other and to the direction of travel, moving at c = 1/√(μ₀ε₀) = 3 × 10⁸ m/s, with E₀ = cB₀.</p>"
          "<p>The electromagnetic spectrum runs from radio waves (longest wavelength) through microwaves, infrared, visible light, ultraviolet and X-rays to gamma rays (shortest). Each has its uses, from broadcasting to radiotherapy.</p>",
          [("λ = 3 m. f?", ["3 × 10⁸ ÷ 3"], "10⁸ Hz"), ("Used in remote controls?", ["heat waves"], "infrared")],
          ["Thinking EM waves need a medium.", "Mixing up the order of the spectrum.", "Saying E and B are parallel."],
          [("What is displacement current?", "A current term due to a changing electric field, as between the plates of a charging capacitor."),
           ("Which EM waves have the shortest wavelength?", "Gamma rays.")],
          lambda: [("Displacement current and EM waves", [(b[8], 6), (K(em, "E0"), 14)]), ("Speed, frequency and wavelength", [(K(em, "f", "lam"), 20)]), ("Speed in a medium", [(K(em, "n", "eps"), 8), (b[8], 4), (K(em, "f", "lam"), 8)]),
                   ("The electromagnetic spectrum", [(emw, 10), (K(em, "f", "lam"), 10)]), ("Mixed questions", [(K(em, "E0", "f", "lam"), 20)])]),
        S(9, "ray-optics-and-optical-instruments", 9,
          "Ray optics: reflection of light, spherical mirrors, mirror formula, refraction of light, total internal reflection and optical fibres, refraction at spherical surfaces, lenses, thin lens formula, lens maker's formula, magnification, power of a lens, combination of thin lenses in contact, refraction of light through a prism. Optical instruments: microscopes and astronomical telescopes (reflecting and refracting) and their magnifying powers.",
          "Ray Optics and Optical Instruments", "ray optics",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 9 Ray Optics and Optical Instruments: mirror and lens formulae, magnification, power, total internal reflection, prisms, microscopes and telescopes. 100 questions with answers.",
          "Mirror: 1/v + 1/u = 1/f; lens: 1/v − 1/u = 1/f.", "P = 1/f (in metres), in dioptres.",
          "<p>With the Cartesian sign convention, distances are measured from the pole or optical centre, and distances against the incident light are negative. Mirrors obey 1/v + 1/u = 1/f, thin lenses 1/v − 1/u = 1/f; magnification is −v/u for a mirror and v/u for a lens. Lens power P = 1/f in dioptres, and powers add for lenses in contact.</p>"
          "<p>Light going from a denser to a rarer medium beyond the critical angle (sin C = 1/n) is totally internally reflected, as in optical fibres. A prism's refractive index is sin((A + D)/2)/sin(A/2). A telescope magnifies f<sub>o</sub>/f<sub>e</sub>; a simple microscope 1 + D/f.</p>",
          [("f = 20 cm, u = −30 cm, convex lens. v?", ["1/20 − 1/30"], "+60 cm"), ("f = 25 cm. P?", ["100 ÷ 25"], "+4 D")],
          ["Forgetting the sign convention.", "Using the mirror formula for a lens.", "Using f in cm for power."],
          [("What is total internal reflection?", "Complete reflection of light going from a denser to a rarer medium when the angle of incidence exceeds the critical angle."),
           ("What is the magnifying power of an astronomical telescope?", "f<sub>o</sub>/f<sub>e</sub> in normal adjustment.")],
          lambda: [("Spherical mirrors", [(K(rayo, "mir"), 16), (b[9], 4)]), ("Refraction and total internal reflection", [(A(P.w_refr, "snell", "v", "crit"), 11), (K(rayo, "app"), 6), (b[9], 3)]),
                   ("Lenses", [(K(rayo, "lens", "m", "lm"), 17), (b[9], 3)]), ("Power and combinations", [(K(rayo, "P", "comb"), 19), (b[9], 1)]), ("Prisms and optical instruments", [(K(rayo, "prism", "tel", "mic"), 19), (b[9], 1)])]),
        S(10, "wave-optics", 10,
          "Wave optics: wave front and Huygens's principle, proof of laws of reflection and refraction using Huygens's principle. Interference, Young's double slit experiment and expression for fringe width (no derivation, final expression only), coherent sources and sustained interference of light, diffraction due to a single slit, width of central maxima (qualitative treatment only).",
          "Wave Optics", "wave optics",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 10 Wave Optics: wavefronts, Huygens' principle, Young's double-slit experiment, fringe width, single-slit diffraction and polarisation. 100 questions with answers.",
          "Fringe width β = λD/d.", "Bright: path difference nλ; dark: (n + ½)λ.",
          "<p>A wavefront joins points vibrating in phase; Huygens' principle builds each new wavefront from secondary wavelets and explains reflection and refraction. Light from two coherent sources interferes: bright fringes where the path difference is nλ, dark where it is (n + ½)λ. In Young's experiment the fringe width is β = λD/d.</p>"
          "<p>A single slit of width a gives a central bright band of width 2λD/a. Polarisation shows that light is transverse: a polaroid passes half of unpolarised light, Malus's law gives I = I₀ cos²θ, and light reflected at Brewster's angle (tan i<sub>B</sub> = n) is completely polarised.</p>",
          [("λ = 600 nm, D = 1 m, d = 1 mm. β?", ["λD/d"], "0.6 mm"), ("Glass n = 1.5 in light: wavelength 600 nm becomes?", ["λ/n"], "400 nm")],
          ["Thinking frequency changes in glass.", "Using d in mm without converting.", "Saying two bulbs are coherent."],
          [("Why must the two sources in Young's experiment be coherent?", "Only coherent sources keep a constant phase difference, so the fringe pattern stays still."),
           ("What does polarisation tell us about light?", "That light is a transverse wave.")],
          lambda: [("Wavefronts and Huygens' principle", [(b[10], 6), (K(wo, "ref"), 14)]), ("Young's double-slit experiment", [(A(P.w_slits, "w", "lam"), 17), (b[10], 3)]), ("Interference conditions", [(A(P.w_phase, "cons"), 10), (b[10], 1), (A(P.w_slits, "w"), 9)]),
                   ("Diffraction", [(K(wo, "ss"), 16), (A(P.w_grating, "angle"), 4)]), ("Polarisation", [(K(wo, "brew", "malus", "fw"), 20)])]),
        S(11, "dual-nature-of-radiation-and-matter", 11,
          "Dual nature of radiation, photoelectric effect, Hertz and Lenard's observations; Einstein's photoelectric equation – particle nature of light. Experimental study of photoelectric effect. Matter waves – wave nature of particles, de Broglie relation.",
          "Dual Nature of Radiation and Matter", "dual nature of radiation and matter",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 11 Dual Nature of Radiation and Matter: photons, the photoelectric effect, work function, stopping potential, threshold frequency and de Broglie wavelength. 100 questions with answers.",
          "K(max) = hν − φ₀ = eV₀.", "λ = h/p; for electrons λ = 1.227/√V nm.",
          "<p>Light behaves as photons of energy E = hν = hc/λ. In the photoelectric effect, a photon frees an electron only if hν is at least the work function φ₀; the fastest electrons have K<sub>max</sub> = hν − φ₀ = eV₀, where V₀ is the stopping potential. Brighter light gives more electrons, not faster ones.</p>"
          "<p>Matter also has wave properties: a particle of momentum p has de Broglie wavelength λ = h/p. Electrons accelerated through V volts have λ = 1.227/√V nm, which the Davisson–Germer experiment confirmed.</p>",
          [("hν = 5 eV, φ₀ = 2 eV. Kmax?", ["5 − 2"], "3 eV"), ("Electrons through 100 V. λ?", ["1.227 ÷ 10"], "0.123 nm")],
          ["Thinking brighter light gives faster electrons.", "Forgetting to convert eV to joules.", "Using λ = h/m."],
          [("What is Einstein's photoelectric equation?", "K<sub>max</sub> = hν − φ₀: the photon's energy minus the work function."),
           ("What is the de Broglie wavelength?", "The wavelength λ = h/p of a moving particle.")],
          lambda: [("Photons", [(A(P.p_photon, "J", "eV", "f"), 16), (b[11], 4)]), ("The photoelectric effect", [(A(P.p_photoelectric, "ke", "ke2"), 12), (K(dn, "Kmax"), 7), (b[11], 1)]),
                   ("Work function and threshold", [(K(dn, "f0", "lam0"), 15), (A(P.p_photoelectric, "f0"), 4), (b[11], 1)]), ("Stopping potential", [(K(dn, "V0"), 14), (A(P.p_photoelectric, "ke"), 6)]),
                   ("Matter waves", [(A(P.p_debroglie, "e", "p"), 11), (K(dn, "lamV"), 8), (b[11], 1)])]),
        S(12, "atoms", 12,
          "Alpha-particle scattering experiment; Rutherford's model of atom; Bohr model of hydrogen atom, expression for radius of nth possible orbit, velocity and energy of electron in nth orbit, hydrogen line spectra (qualitative treatment only).",
          "Atoms", "atoms",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 12 Atoms: α-particle scattering, Rutherford's model, Bohr's model, orbit radii and energies, and the hydrogen spectrum. 100 questions with answers.",
          "E(n) = −13.6/n² eV; r(n) = 0.53 n² Å.", "A jump between levels gives one spectral line.",
          "<p>In the Geiger–Marsden experiment most α-particles went straight through gold foil, but a few bounced back, showing a tiny, massive, positive nucleus. Rutherford's model could not explain why atoms are stable or why spectra have lines.</p>"
          "<p>Bohr's model allows only orbits with angular momentum nh/2π. For hydrogen r<sub>n</sub> = 0.53 n² Å and E<sub>n</sub> = −13.6/n² eV. When an electron falls between levels it emits a photon of energy equal to the difference; the Lyman series ends on n = 1, Balmer (visible) on n = 2 and Paschen on n = 3.</p>",
          [("H, n = 2. Energy?", ["−13.6 ÷ 4"], "−3.4 eV"), ("n = 3 → 2 photon?", ["1.89 eV"], "656 nm")],
          ["Forgetting the minus sign of energy.", "Saying r ∝ n.", "Naming the series by the upper level."],
          [("Why did Rutherford's model fail?", "An orbiting electron should radiate energy and spiral into the nucleus, so atoms would not be stable."),
           ("Why is the hydrogen spectrum a line spectrum?", "Electrons can only jump between fixed energy levels, so only certain photon energies are emitted.")],
          lambda: [("α-particle scattering", [(K(at, "closest"), 15), (b[12], 5)]), ("Bohr's model", [(K(at, "bohr"), 18), (b[12], 2)]), ("Energy levels", [(K(at, "ion"), 4), (A(P.p_levels, "E"), 6), (K(at, "bohr"), 10)]),
                   ("The hydrogen spectrum", [(K(at, "trans"), 10), (A(P.p_levels, "lam"), 6), (K(at, "bohr"), 4)]), ("Mixed problems", [(K(at, "closest"), 10), (b[12], 2), (K(at, "bohr"), 8)])]),
        S(13, "nuclei", 13,
          "Composition and size of nucleus, nuclear force. Mass-energy relation, mass defect; binding energy per nucleon and its variation with mass number; nuclear fission, nuclear fusion.",
          "Nuclei", "nuclei",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 13 Nuclei: composition and size of nuclei, nuclear force, mass defect, binding energy, E = mc², fission and fusion. 100 questions with answers.",
          "Binding energy = Δm × 931.5 MeV.", "R = R₀A^(1/3); nuclear density is the same for all nuclei.",
          "<p>A nucleus has Z protons and A − Z neutrons, held by the strong, short-range nuclear force. Its radius is R = R₀A<sup>1/3</sup> with R₀ = 1.2 fm, so all nuclei have about the same density.</p>"
          "<p>The mass of a nucleus is less than the mass of its separate nucleons; this mass defect Δm appears as binding energy Δm × 931.5 MeV. Binding energy per nucleon peaks near iron-56, so heavy nuclei release energy by fission and light nuclei by fusion.</p>",
          [("¹²⁶⁸Pb? Neutrons in ²⁰⁶₈₂Pb?", ["206 − 82"], "124"), ("Δm = 0.03 u. BE?", ["0.03 × 931.5"], "27.9 MeV")],
          ["Forgetting to multiply by 931.5.", "Saying fusion splits nuclei.", "Using A instead of A<sup>1/3</sup> for the radius."],
          [("What is binding energy?", "The energy needed to separate a nucleus into its protons and neutrons; it equals the mass defect × c²."),
           ("Why do both fission and fusion release energy?", "In both, the products have a higher binding energy per nucleon than the starting nuclei.")],
          lambda: [("Composition of the nucleus", [(A(P.p_nucleus), 16), (b[13], 4)]), ("Size and density", [(K(nu, "R", "dens"), 12), (A(P.n_nuclear, "radius"), 7), (b[13], 1)]), ("Mass defect", [(K(nu, "md"), 12), (b[13], 2), (K(nu, "E"), 6)]),
                   ("Binding energy", [(K(nu, "BE", "BEn"), 16), (b[13], 1), (A(P.n_nuclear, "BE"), 3)]), ("Fission and fusion", [(K(nu, "BE", "BEn", "E"), 15), (A(P.n_nuclear, "emc"), 4), (b[13], 1)])]),
        S(14, "semiconductor-electronics", 14,
          "Energy bands in conductors, semiconductors and insulators (qualitative ideas only). Intrinsic and extrinsic semiconductors – p and n type, p-n junction. Semiconductor diode – I–V characteristics in forward and reverse bias, application of junction diode – diode as a rectifier.",
          "Semiconductor Electronics: Materials, Devices and Simple Circuits", "semiconductor electronics",
          "Free CBSE Class 12 Physics worksheets for NCERT Chapter 14 Semiconductor Electronics: energy bands, intrinsic and extrinsic semiconductors, doping, the p-n junction, diode bias and rectifiers. 100 questions with answers.",
          "n-type: extra electrons (group 15 dopant); p-type: holes (group 13 dopant).", "A diode conducts in forward bias, not reverse.",
          "<p>Conductors have overlapping bands, insulators a large gap and semiconductors a small gap (silicon about 1.1 eV). A pure (intrinsic) semiconductor has equal electrons and holes, n<sub>e</sub> = n<sub>h</sub> = n<sub>i</sub>. Doping with a group 15 element (arsenic) gives n-type; with a group 13 element (boron) gives p-type; always n<sub>e</sub>n<sub>h</sub> = n<sub>i</sub>².</p>"
          "<p>A p-n junction forms a depletion region and a barrier (about 0.7 V for silicon). Forward bias narrows it and current flows; reverse bias widens it. Diodes rectify AC: a half-wave rectifier gives one pulse per cycle and a full-wave rectifier two.</p>",
          [("Si doped with boron?", ["group 13"], "p-type"), ("Full-wave, 50 Hz input?", ["2 × 50"], "100 Hz ripple")],
          ["Saying n-type is negatively charged.", "Swapping forward and reverse bias.", "Using the input frequency for a full-wave ripple."],
          [("What is the difference between n-type and p-type semiconductors?", "n-type has extra electrons from group 15 donors; p-type has holes from group 13 acceptors."),
           ("Why does a p-n junction rectify?", "It conducts easily in forward bias but hardly at all in reverse bias.")],
          lambda: [("Energy bands", [(b[14], 6), (semi, 6), (K(sc, "ni"), 8)]), ("Intrinsic and extrinsic semiconductors", [(semi, 8), (K(sc, "ni", "dop"), 12)]), ("Doping", [(K(sc, "dop"), 12), (semi, 6), (b[14], 2)]),
                   ("The p-n junction", [(b[14], 3), (semi, 7), (K(sc, "ni"), 10)]), ("Rectifiers", [(K(sc, "half", "full"), 8), (semi, 5), (K(sc, "dop"), 7)])]),
    ]
