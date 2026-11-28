# -*- coding: utf-8 -*-
"""Deutschland / Klasse 12（Oberstufe, Qualifikationsphase 1: Biologie, Chemie, Physik）"""
import math
from de_sci import H, nq, num


def f_ph(R):
    k = R.choice(["pH", "pH", "c", "lauge", "verd"])
    if k == "pH":
        n = R.choice([1, 2, 3, 4, 5, 6])
        c = 10 ** -n
        return nq("Wie groß ist der pH-Wert einer Salzsäure mit c(H₃O⁺) = %s mol/l?" % num(c), n, [14 - n, -n + 1 if n > 1 else 7, n + 1], "",
                  "pH = −lg c(H₃O⁺) = −lg %s = %d." % (num(c), n))
    if k == "c":
        n = R.choice([2, 3, 4, 5, 6])
        return nq("Eine Lösung hat pH = %d. Wie groß ist c(H₃O⁺)?" % n, 10 ** -n, [10 ** -(14 - n), 10 ** -(n - 1), n / 10], "mol/l",
                  "c(H₃O⁺) = 10<sup>−pH</sup> = 10<sup>−%d</sup> mol/l." % n)
    if k == "lauge":
        n = R.choice([1, 2, 3, 4, 5])
        return nq("Natronlauge hat c(OH⁻) = %s mol/l. Wie groß ist der pH-Wert? (pH + pOH = 14)" % num(10 ** -n), 14 - n, [n, 7 + n if n < 7 else 13, 14 + n], "",
                  "pOH = %d, also pH = 14 − %d = %d." % (n, n, 14 - n))
    n, f = R.choice([(1, 10), (2, 10), (1, 100), (3, 10), (2, 100), (1, 1000)])
    m = int(round(math.log10(f)))
    return nq("Eine Salzsäure mit pH = %d wird mit Wasser auf das %s-Fache verdünnt. Welchen pH-Wert hat sie dann?" % (n, num(f)), n + m, [n * f if n * f < 14 else n + 2 * m, n - m if n - m > 0 else n + m + 1, n + 0.5 * m], "",
              "Verdünnen um den Faktor 10 erhöht den pH-Wert um 1: %d + %d = %d." % (n, m, n + m))


def f_titr(R):
    k = R.choice(["c", "c", "V", "n"])
    if k == "c":
        cb, Vb, Va = R.choice([(0.1, 20, 10), (0.1, 15, 25), (0.2, 12.5, 25), (0.5, 8, 20), (0.1, 30, 20), (0.2, 25, 50), (1, 5, 25), (0.1, 18, 20), (0.25, 16, 40), (0.5, 12, 30), (0.2, 7.5, 15)])
        ca = cb * Vb / Va
        return nq("%s ml Salzsäure werden mit Natronlauge (c = %s mol/l) titriert. Am Äquivalenzpunkt sind %s ml verbraucht. Wie groß ist c(HCl)?" % (num(Va), num(cb), num(Vb)), ca,
                  [cb * Va / Vb, cb * Vb * Va / 1000, cb], "mol/l", "c(HCl) = c(NaOH) · V(NaOH) : V(HCl) = %s · %s : %s = %s mol/l." % (num(cb), num(Vb), num(Va), num(ca)))
    if k == "V":
        ca, Va, cb = R.choice([(0.1, 25, 0.1), (0.2, 10, 0.1), (0.05, 40, 0.1), (0.5, 10, 0.25), (0.1, 30, 0.2), (0.3, 20, 0.6), (0.2, 15, 0.1), (0.4, 25, 0.5), (0.15, 20, 0.1)])
        Vb = ca * Va / cb
        return nq("Wie viel Natronlauge (c = %s mol/l) braucht man, um %s ml Salzsäure (c = %s mol/l) zu neutralisieren?" % (num(cb), num(Va), num(ca)), Vb,
                  [cb * Va / ca, ca * cb * Va, Va], "ml", "V(NaOH) = c(HCl) · V(HCl) : c(NaOH) = %s · %s : %s = %s ml." % (num(ca), num(Va), num(cb), num(Vb)))
    c, V = R.choice([(0.1, 20), (0.2, 50), (0.5, 10), (1, 25), (0.25, 40), (0.05, 200)])
    return nq("Wie viel Stoffmenge HCl enthalten %s ml Salzsäure mit c = %s mol/l?" % (num(V), num(c)), c * V / 1000, [c * V, c / V, c * V / 100], "mol",
              "n = c · V = %s mol/l · %s l = %s mol." % (num(c), num(V / 1000), num(c * V / 1000)))


EO = [("Li/Li⁺", -3.04), ("K/K⁺", -2.93), ("Mg/Mg²⁺", -2.37), ("Al/Al³⁺", -1.66), ("Zn/Zn²⁺", -0.76), ("Fe/Fe²⁺", -0.41), ("Pb/Pb²⁺", -0.13),
      ("H₂/H₃O⁺", 0.0), ("Cu/Cu²⁺", 0.34), ("Ag/Ag⁺", 0.80), ("Au/Au³⁺", 1.50)]


def f_redox(R):
    k = R.choice(["U", "U", "U", "minus"])
    a, b = sorted(R.sample(EO, 2), key=lambda t: t[1])
    U = b[1] - a[1]
    if k == "U":
        return nq("Welche Spannung liefert eine galvanische Zelle aus den Halbzellen %s (E° = %s V) und %s (E° = %s V) unter Standardbedingungen?" % (a[0], num(a[1]), b[0], num(b[1])), round(U, 2),
                  [round(abs(a[1] + b[1]), 2), round(abs(a[1]) + abs(b[1]) + 0.5, 2), round(U / 2, 3)], "V",
                  "U = E°(Kathode) − E°(Anode) = %s V − (%s V) = %s V." % (num(b[1]), num(a[1]), num(round(U, 2))))
    names = [a[0], b[0]]
    from de_sci import it
    return it("In einer galvanischen Zelle aus %s und %s: Welche Halbzelle ist der Minuspol (Anode)?" % (a[0], b[0]), a[0], [b[0], "beide gleich", "keine von beiden"],
              "Das unedlere System (kleineres E°, hier %s V) gibt Elektronen ab und ist der Minuspol." % num(a[1]))


def f_kond(R):
    k = R.choice(["C", "Q", "E", "W", "F"])
    if k == "C":
        Q, U = R.choice([(2e-3, 100), (6e-4, 12), (1e-6, 10), (5e-5, 50), (3e-3, 300), (4.7e-5, 10)])
        return nq("Ein Kondensator trägt bei U = %s V die Ladung Q = %s C. Wie groß ist seine Kapazität?" % (num(U), num(Q)), Q / U, [Q * U, U / Q, Q / U * 1000], "F",
                  "C = Q : U = %s C : %s V = %s F." % (num(Q), num(U), num(Q / U)))
    if k == "Q":
        C, U = R.choice([(1e-6, 12), (4.7e-6, 10), (1e-4, 9), (2.2e-5, 100), (1e-3, 5), (5e-6, 200)])
        return nq("Ein Kondensator mit C = %s F wird an %s V geladen. Welche Ladung trägt er?" % (num(C), num(U)), C * U, [C / U, U / C, C * U * U], "C",
                  "Q = C · U = %s F · %s V = %s C." % (num(C), num(U), num(C * U)))
    if k == "E":
        U, d = R.choice([(100, 0.01), (2000, 0.05), (12, 0.002), (500, 0.02), (300, 0.003), (1000, 0.04)])
        return nq("Zwischen zwei Platten im Abstand %s m liegt die Spannung %s V. Wie groß ist die elektrische Feldstärke?" % (num(d), num(U)), U / d, [U * d, d / U, U / d / 100], "V/m",
                  "E = U : d = %s V : %s m = %s V/m." % (num(U), num(d), num(U / d)))
    if k == "W":
        C, U = R.choice([(1e-3, 10), (2e-4, 100), (5e-6, 400), (1e-2, 5), (4.7e-4, 20), (1e-4, 300)])
        return nq("Wie viel Energie speichert ein Kondensator mit C = %s F bei U = %s V?" % (num(C), num(U)), 0.5 * C * U * U, [C * U * U, C * U, 0.5 * C * U], "J",
                  "W = ½ · C · U² = 0,5 · %s F · (%s V)² = %s J." % (num(C), num(U), num(0.5 * C * U * U)))
    q, E = R.choice([(2e-6, 5000), (1.6e-19, 1e4), (3e-9, 2e5), (5e-6, 400), (1e-8, 3e4)])
    return nq("Auf eine Ladung q = %s C wirkt im Feld mit E = %s N/C welche Kraft?" % (num(q), num(E)), q * E, [q / E, E / q, q * E * 10], "N",
              "F = q · E = %s C · %s N/C = %s N." % (num(q), num(E), num(q * E)))


def f_mag(R):
    k = R.choice(["leiter", "leiter", "lorentz", "radius"])
    if k == "leiter":
        B, I, l = R.choice([(0.2, 5, 0.1), (0.05, 2, 0.4), (0.5, 3, 0.2), (1, 10, 0.05), (0.1, 4, 0.25), (0.3, 6, 0.5), (0.02, 8, 1)])
        return nq("Ein Leiter (l = %s m) steht senkrecht zum Magnetfeld B = %s T, es fließt I = %s A. Welche Kraft wirkt?" % (num(l), num(B), num(I)), B * I * l,
                  [B * I, B * l / I, I * l / B], "N", "F = B · I · l = %s T · %s A · %s m = %s N." % (num(B), num(I), num(l), num(B * I * l)))
    if k == "lorentz":
        v, B = R.choice([(1e6, 0.1), (2e6, 0.05), (5e5, 0.2), (3e6, 0.01), (1e7, 0.002), (4e5, 0.5), (8e5, 0.25), (6e6, 0.03), (2.5e6, 0.4)])
        q = 1.6e-19
        return nq("Ein Elektron (e = 1,6 · 10⁻¹⁹ C) fliegt mit %s m/s senkrecht zu B = %s T. Wie groß ist die Lorentzkraft?" % (num(v), num(B)), q * v * B,
                  [q * v, v * B, q * v / B], "N", "F = e · v · B = 1,6 · 10⁻¹⁹ C · %s m/s · %s T = %s N." % (num(v), num(B), num(q * v * B)))
    v, B = R.choice([(1e7, 1e-3), (2e7, 2e-3), (5e6, 1e-3), (3e7, 5e-3), (1.6e7, 4e-3), (4e6, 2e-3), (8e6, 5e-3)])
    m, q = 9.1e-31, 1.6e-19
    r = m * v / (q * B)
    return nq("Ein Elektron (m = 9,1 · 10⁻³¹ kg, e = 1,6 · 10⁻¹⁹ C) bewegt sich mit %s m/s senkrecht zu B = %s T auf einer Kreisbahn. Wie groß ist der Radius?" % (num(v), num(B)), r,
              [q * B / (m * v), m * v * v / (q * B), r * 10], "m", "Lorentzkraft = Zentripetalkraft: r = m · v : (e · B) = %s m." % num(r))


def f_ind(R):
    k = R.choice(["U", "U", "trafo", "trafoI", "phi"])
    if k == "U":
        N, dB, A, t = R.choice([(100, 0.5, 0.01, 0.1), (200, 0.2, 0.005, 0.02), (500, 0.1, 0.002, 0.05), (50, 1, 0.04, 0.5), (1000, 0.05, 0.001, 0.01), (300, 0.4, 0.01, 0.2)])
        U = N * dB * A / t
        return nq("Eine Spule (N = %d, A = %s m²) steht senkrecht im Magnetfeld. B ändert sich in %s s um %s T. Wie groß ist die induzierte Spannung?" % (N, num(A), num(t), num(dB)), U,
                  [dB * A / t, N * dB * A * t, N * dB / t], "V", "U = N · ΔB · A : Δt = %d · %s T · %s m² : %s s = %s V." % (N, num(dB), num(A), num(t), num(U)))
    if k == "trafo":
        N1, N2, U1 = R.choice([(1000, 50, 230), (500, 25, 230), (200, 2000, 12), (600, 30, 230), (1200, 60, 240), (100, 4000, 10)])
        U2 = U1 * N2 / N1
        return nq("Ein idealer Transformator hat N₁ = %d und N₂ = %d Windungen, U₁ = %s V. Wie groß ist U₂?" % (N1, N2, num(U1)), U2, [U1 * N1 / N2, U1, U1 * N2], "V",
                  "U₂ = U₁ · N₂ : N₁ = %s V · %d : %d = %s V." % (num(U1), N2, N1, num(U2)))
    if k == "trafoI":
        N1, N2, I1 = R.choice([(1000, 50, 0.1), (500, 25, 0.2), (200, 2000, 5), (600, 30, 0.5), (400, 40, 0.3)])
        I2 = I1 * N1 / N2
        return nq("Ein idealer Transformator hat N₁ = %d und N₂ = %d Windungen, I₁ = %s A. Wie groß ist I₂?" % (N1, N2, num(I1)), I2, [I1 * N2 / N1, I1, I1 * N1 * N2], "A",
                  "Beim idealen Trafo gilt I₂ = I₁ · N₁ : N₂ = %s A · %d : %d = %s A." % (num(I1), N1, N2, num(I2)))
    B, A = R.choice([(0.5, 0.02), (0.2, 0.1), (1.5, 0.004), (0.05, 0.3), (0.8, 0.025), (2, 0.01)])
    return nq("Ein Magnetfeld B = %s T durchsetzt eine Fläche A = %s m² senkrecht. Wie groß ist der magnetische Fluss?" % (num(B), num(A)), B * A, [B / A, A / B, B + A], "Wb",
              "Φ = B · A = %s T · %s m² = %s Wb." % (num(B), num(A), num(B * A)))


def f_welle(R):
    k = R.choice(["c", "c", "lam", "gitter", "gang"])
    if k == "c":
        lam, f = R.choice([(0.5, 680), (2, 170), (0.2, 1700), (1.5, 220), (0.04, 8500), (3, 110), (0.85, 400)])
        return nq("Eine Welle hat λ = %s m und f = %s Hz. Wie schnell breitet sie sich aus?" % (num(lam), num(f)), lam * f, [lam / f, f / lam, lam * f / 10], "m/s",
                  "c = λ · f = %s m · %s Hz = %s m/s." % (num(lam), num(f), num(lam * f)))
    if k == "lam":
        f = R.choice([100, 200, 440, 1000, 50, 2000, 170])
        return nq("Wie groß ist die Wellenlänge eines Tons mit %s Hz in Luft (c = 340 m/s)?" % num(f), 340 / f, [f / 340, 340 * f, 340 / f / 2], "m",
                  "λ = c : f = 340 m/s : %s Hz = %s m." % (num(f), num(340 / f)))
    if k == "gitter":
        g, a, e = R.choice([(1e-5, 0.05, 1), (2e-6, 0.3, 1), (1e-5, 0.06, 1), (5e-6, 0.12, 1), (1e-6, 0.6, 1), (2e-6, 0.27, 1)])
        lam = g * a / e
        return nq("Ein Gitter mit g = %s m steht e = %s m vor dem Schirm. Das 1. Maximum liegt a = %s m neben der Mitte. Wie groß ist λ (Kleinwinkelnäherung)?" % (num(g), num(e), num(a)), lam,
                  [g / a, a / g, g * a * 10], "m", "λ = g · a : e = %s m · %s m : %s m = %s m." % (num(g), num(a), num(e), num(lam)))
    lam = R.choice([2, 4, 0.5, 1, 3, 0.8])
    n = R.choice([1, 2, 3])
    return nq("Zwei gleichphasige Quellen senden Wellen mit λ = %s cm aus. Bei welchem Gangunterschied liegt das %d. Maximum?" % (num(lam), n), n * lam, [n * lam / 2, (n + 0.5) * lam, n * lam * 2], "cm",
              "Maxima liegen bei Δs = k · λ: %d · %s cm = %s cm." % (n, num(lam), num(n * lam)))

DIS = [("Mukoviszidose", "r"), ("Phenylketonurie", "r"), ("Albinismus", "r"), ("Sichelzellanämie", "r"), ("Chorea Huntington", "d"), ("Marfan-Syndrom", "d"),
       ("Bluterkrankheit", "x"), ("Rot-Grün-Sehschwäche", "x"), ("Duchenne-Muskeldystrophie", "x")]
PCT = ["0 Prozent", "25 Prozent", "50 Prozent", "75 Prozent", "100 Prozent"]


def f_erb(R):
    from de_sci import it
    d, t = R.choice(DIS)
    if t == "r":
        cross, p, why = R.choice([("beide Eltern sind gesunde Träger (Aa × Aa)", 25, "Aa × Aa ergibt AA, Aa, Aa, aa: ein Viertel ist aa."),
                                  ("ein Elternteil ist krank (aa), der andere gesunder Träger (Aa)", 50, "aa × Aa ergibt Aa und aa je zur Hälfte."),
                                  ("ein Elternteil ist Träger (Aa), der andere reinerbig gesund (AA)", 0, "AA × Aa ergibt nur AA und Aa, kein Kind ist aa."),
                                  ("beide Eltern sind krank (aa × aa)", 100, "aa × aa ergibt nur aa.")])
        q = "%s wird autosomal-rezessiv vererbt. Bei einem Paar gilt: %s. Wie wahrscheinlich ist ein Kind krank?" % (d, cross)
    elif t == "d":
        cross, p, why = R.choice([("ein Elternteil ist heterozygot krank (Aa), der andere gesund (aa)", 50, "Aa × aa ergibt Aa und aa je zur Hälfte, Aa ist krank."),
                                  ("beide Eltern sind heterozygot krank (Aa × Aa)", 75, "Aa × Aa ergibt AA, Aa, Aa, aa: drei Viertel tragen A."),
                                  ("beide Eltern sind gesund (aa × aa)", 0, "Gesunde Eltern haben bei dominantem Erbgang kein A-Allel.")])
        q = "%s wird autosomal-dominant vererbt. Bei einem Paar gilt: %s. Wie wahrscheinlich ist ein Kind krank?" % (d, cross)
    else:
        cross, who, p, why = R.choice([("eine Konduktorin und ein gesunder Mann", "ein Sohn", 50, "Der Sohn erhält mit 50 Prozent das Xᵃ der Mutter."),
                                       ("eine Konduktorin und ein gesunder Mann", "eine Tochter", 0, "Die Tochter erhält vom Vater ein gesundes X."),
                                       ("eine gesunde Frau (kein Träger) und ein kranker Mann", "ein Sohn", 0, "Der Sohn erhält vom Vater nur das Y-Chromosom."),
                                       ("eine gesunde Frau (kein Träger) und ein kranker Mann", "eine Tochter", 0, "Die Tochter ist sicher Konduktorin, aber gesund."),
                                       ("eine Konduktorin und ein kranker Mann", "eine Tochter", 50, "Die Tochter erhält Xᵃ vom Vater und mit 50 Prozent Xᵃ von der Mutter."),
                                       ("eine Konduktorin und ein kranker Mann", "ein Sohn", 50, "Der Sohn erhält mit 50 Prozent das Xᵃ der Mutter.")])
        q = "%s wird X-chromosomal-rezessiv vererbt. Eltern sind %s. Wie wahrscheinlich ist %s krank?" % (d, cross, who)
    a = "%d Prozent" % p
    return it(q, a, R.sample([x for x in PCT if x != a], 3), why)


def UNITS(grade):
    return [
        H("B", "proteinbiosynthese-und-genregulation", "Proteinbiosynthese und Genregulation", "Proteinbiosynthese",
          "Die Schülerinnen und Schüler erklären DNA-Replikation, Transkription und Translation, nutzen die Codesonne, beschreiben Genmutationen und die Genregulation bei Pro- und Eukaryoten.",
          "semikonservative Replikation, Transkription, RNA-Polymerase, mRNA, Codon und Anticodon, tRNA, Ribosom, genetischer Code, Punktmutation, Rasterschubmutation, Operon-Modell, Spleißen",
          "Ein Gen wird transkribiert und an den Ribosomen translatiert", "Drei Basen der mRNA (ein Codon) codieren für eine Aminosäure.",
          ["Bei der Replikation wird die DNA semikonservativ verdoppelt: Jeder neue Doppelstrang enthält einen alten und einen neuen Strang.",
           "Transkription: Die RNA-Polymerase schreibt im Zellkern einen DNA-Abschnitt in mRNA um (U statt T). Bei Eukaryoten werden die Introns herausgespleißt.",
           "Translation: Am Ribosom paaren die Anticodons der tRNA mit den Codons der mRNA. Start ist AUG, Stopp sind UAA, UAG und UGA. Beim lac-Operon schaltet Lactose die Gene ein."],
          [("Der codogene DNA-Strang lautet TAC-GGA. Wie lautet die mRNA?", ["mRNA ist komplementär zum codogenen Strang.", "T→A, A→U, C→G, G→C"], "AUG-CCU")],
          [("Die mRNA enthält Thymin.", "In RNA steht Uracil statt Thymin."), ("Eine Punktmutation verändert immer das Protein.", "Stille Mutationen ändern die Aminosäure nicht, weil der Code redundant ist."),
           ("Die Translation läuft im Zellkern.", "Die Translation läuft an den Ribosomen im Cytoplasma.")],
          [("Was bedeutet „der Code ist degeneriert“?", "Mehrere Codons codieren dieselbe Aminosäure."), ("Was ist eine Rasterschubmutation?", "Durch Einfügen oder Verlust einer Base verschiebt sich das Leseraster, oft entsteht ein ganz anderes Protein."),
           ("Was macht der Repressor beim lac-Operon?", "Ohne Lactose blockiert er den Operator, die Gene werden nicht abgelesen.")],
          [("Begriffe", [("Codon", "drei Basen der mRNA für eine Aminosäure"), ("Anticodon", "drei Basen der tRNA, passend zum Codon"), ("Promotor", "Startstelle der RNA-Polymerase"), ("Intron", "nichtcodierender Abschnitt, der herausgespleißt wird"),
                         ("Exon", "codierender Abschnitt der eukaryotischen DNA"), ("tRNA", "bringt Aminosäuren zum Ribosom"), ("Operator", "Bindestelle für den Repressor"), ("Startcodon", "AUG")],
            "Was beschreibt „{k}“?", "Welcher Begriff passt: {v}?"),
           ("Basenpaarung bei der Transkription", [("DNA-Base A", "mRNA-Base U"), ("DNA-Base T", "mRNA-Base A"), ("DNA-Base G", "mRNA-Base C"), ("DNA-Base C", "mRNA-Base G"),
                                                   ("codogener Strang TAC", "mRNA AUG"), ("codogener Strang ACT", "mRNA UGA"), ("codogener Strang GGC", "mRNA CCG"), ("codogener Strang ATT", "mRNA UAA"),
                                                   ("codogener Strang CTT", "mRNA GAA")],
            "Was entsteht in der mRNA? {k}", None),
           ("Mutationen", [("eine Base wird ausgetauscht, gleiche Aminosäure", "stumme Mutation"), ("eine Base wird ausgetauscht, andere Aminosäure", "Missense-Mutation"), ("eine Base wird ausgetauscht, Stoppcodon entsteht", "Nonsense-Mutation"),
                           ("eine Base wird eingefügt", "Rasterschubmutation"), ("eine Base geht verloren", "Rasterschubmutation"), ("ein Chromosomenabschnitt wird umgedreht", "Inversion"), ("ein Chromosom liegt dreimal vor", "Genommutation (Trisomie)")],
            "Welche Mutation ist das? {k}", None)],
          ["Die Replikation ist semikonservativ.", "In der mRNA steht Uracil statt Thymin.", "Ein Codon besteht aus drei Basen.", "AUG ist das Startcodon.",
           "Die Translation findet an den Ribosomen statt.", "Introns werden beim Spleißen entfernt.", "Der genetische Code ist degeneriert.", "Ohne Lactose blockiert der Repressor das lac-Operon."],
          [("Die mRNA enthält Thymin.", "Sie enthält Uracil."), ("Die Translation läuft im Zellkern.", "Sie läuft an den Ribosomen."), ("Jede Punktmutation verändert das Protein.", "Stumme Mutationen nicht."),
           ("Exons werden herausgespleißt.", "Introns werden herausgespleißt."), ("Ein Codon besteht aus zwei Basen.", "Es besteht aus drei Basen."), ("Die Replikation ist konservativ.", "Sie ist semikonservativ.")],
          "die Proteinbiosynthese", "living-things-and-ecosystems"),

        H("B", "neurobiologie-und-synapsen", "Neurobiologie: Aktionspotenzial und Synapse", "Neurobiologie",
          "Die Schülerinnen und Schüler erklären Ruhepotenzial und Aktionspotenzial mit Ionenströmen, die Erregungsleitung und die Vorgänge an chemischen Synapsen sowie die Wirkung von Giften und Drogen.",
          "Ruhepotenzial, Natrium-Kalium-Pumpe, Aktionspotenzial, Depolarisation, Repolarisation, Refraktärzeit, saltatorische Erregungsleitung, Synapse, Acetylcholin, Synapsengifte",
          "Aktionspotenziale entstehen durch Ionenströme", "Na⁺ strömt ein (Depolarisation), dann K⁺ aus (Repolarisation).",
          ["Das Ruhepotenzial von etwa −70 mV entsteht durch ungleiche Ionenverteilung: innen viel K⁺, außen viel Na⁺. Die Natrium-Kalium-Pumpe hält diesen Zustand unter ATP-Verbrauch.",
           "Wird der Schwellenwert erreicht, öffnen sich Na⁺-Kanäle: Na⁺ strömt ein, das Membranpotenzial steigt auf etwa +30 mV. Dann strömt K⁺ aus, die Membran repolarisiert. Es gilt das Alles-oder-nichts-Prinzip.",
           "An der Synapse löst das Aktionspotenzial den Ca²⁺-Einstrom aus, Vesikel geben Acetylcholin in den Spalt. Es bindet an Rezeptoren der Folgezelle. Cholinesterase baut es wieder ab."],
          [("Ein Gift blockiert die Acetylcholinesterase. Was passiert?", ["Acetylcholin wird nicht abgebaut.", "Die Folgezelle bleibt dauererregt."], "Dauererregung, zum Beispiel Krämpfe")],
          [("Beim Aktionspotenzial strömt K⁺ ein.", "Bei der Depolarisation strömt Na⁺ ein, K⁺ strömt bei der Repolarisation aus."), ("Starke Reize erzeugen höhere Aktionspotenziale.", "Reizstärke wird über die Frequenz codiert, nicht die Höhe."),
           ("Die Erregung springt im Spalt elektrisch über.", "An chemischen Synapsen überträgt ein Transmitter die Erregung.")],
          [("Warum leiten markhaltige Fasern schneller?", "Die Erregung springt von Schnürring zu Schnürring (saltatorische Leitung)."), ("Was macht Curare?", "Es blockiert die Acetylcholin-Rezeptoren an der motorischen Endplatte, es kommt zur Lähmung."),
           ("Was ist die Refraktärzeit?", "Eine kurze Zeit nach einem Aktionspotenzial, in der kein neues ausgelöst werden kann.")],
          [("Phasen", [("Ruhepotenzial", "etwa −70 mV, innen negativ"), ("Depolarisation", "Na⁺-Kanäle öffnen, Na⁺ strömt ein"), ("Repolarisation", "K⁺ strömt aus"), ("Hyperpolarisation", "Potenzial kurz negativer als in Ruhe"),
                       ("Schwellenwert", "ab hier wird ein Aktionspotenzial ausgelöst"), ("Refraktärzeit", "kein neues Aktionspotenzial möglich"), ("Overshoot", "Potenzial kurz positiv, etwa +30 mV")],
            "Was beschreibt {k}?", "Welche Phase ist das: {v}?"),
           ("Synapsengifte und Drogen", [("Curare", "blockiert Acetylcholin-Rezeptoren"), ("E 605 (Parathion)", "hemmt die Acetylcholinesterase"), ("Botulinumtoxin", "verhindert die Ausschüttung von Acetylcholin"),
                                         ("Atropin", "blockiert Acetylcholin-Rezeptoren am Herzen und an Drüsen"), ("Nikotin", "aktiviert Acetylcholin-Rezeptoren"), ("Kokain", "hemmt die Wiederaufnahme von Dopamin"),
                                         ("Tetrodotoxin", "blockiert Natriumkanäle")],
            "Wie wirkt {k}?", "Welcher Stoff {v}?"),
           ("Synapse", [("Vesikel", "enthalten den Transmitter"), ("Acetylcholin", "Transmitter an der motorischen Endplatte"), ("Ca²⁺-Einstrom", "löst die Ausschüttung des Transmitters aus"),
                        ("synaptischer Spalt", "Raum zwischen den Zellen"), ("Rezeptor", "bindet den Transmitter an der Folgezelle"), ("Cholinesterase", "spaltet Acetylcholin"),
                        ("Myelinscheide", "isoliert das Axon")],
            "Welche Rolle spielt {k}?", "Was ist gemeint? {v}")],
          ["Das Ruhepotenzial beträgt etwa −70 mV.", "Bei der Depolarisation strömt Na⁺ ein.", "Bei der Repolarisation strömt K⁺ aus.", "Für Aktionspotenziale gilt das Alles-oder-nichts-Prinzip.",
           "Reizstärke wird über die Frequenz codiert.", "Ca²⁺ löst die Transmitterausschüttung aus.", "Markhaltige Fasern leiten saltatorisch.", "Curare blockiert Acetylcholin-Rezeptoren."],
          [("Bei der Depolarisation strömt K⁺ ein.", "Na⁺ strömt ein."), ("Starke Reize erzeugen höhere Aktionspotenziale.", "Sie erzeugen eine höhere Frequenz."), ("Das Ruhepotenzial ist innen positiv.", "Es ist innen negativ."),
           ("An chemischen Synapsen springt der Strom über den Spalt.", "Ein Transmitter überträgt die Erregung."), ("Markhaltige Fasern leiten langsamer.", "Sie leiten schneller."),
           ("Die Natrium-Kalium-Pumpe braucht keine Energie.", "Sie verbraucht ATP.")],
          "die Neurobiologie", "living-things-and-ecosystems"),

        H("B", "molekulargenetische-methoden", "Molekulargenetische Methoden", "Gentechnik",
          "Die Schülerinnen und Schüler beschreiben PCR, Gelelektrophorese, genetischen Fingerabdruck, Klonierung mit Plasmiden und CRISPR/Cas, werten Gelbilder aus und bewerten Anwendungen.",
          "Polymerase-Kettenreaktion, Primer, Taq-Polymerase, Gelelektrophorese, Restriktionsenzyme, genetischer Fingerabdruck, Plasmide, Antibiotikaresistenz als Marker, CRISPR/Cas, Bewertung",
          "Mit PCR wird DNA millionenfach vervielfältigt", "In der Gelelektrophorese wandern kleine DNA-Stücke weiter als große.",
          ["PCR: Denaturieren (94 °C), Anlagern der Primer (etwa 55 °C), Verlängern durch die hitzestabile Taq-Polymerase (72 °C). Jeder Zyklus verdoppelt die DNA.",
           "In der Gelelektrophorese wandert die negativ geladene DNA zum Pluspol. Kleine Fragmente wandern weiter. So vergleicht man DNA-Muster beim genetischen Fingerabdruck.",
           "Restriktionsenzyme schneiden DNA an Erkennungssequenzen. Ein Gen wird in ein Plasmid eingebaut und in Bakterien übertragen. CRISPR/Cas schneidet gezielt an einer Stelle des Genoms."],
          [("Wie viele DNA-Kopien entstehen aus einem Molekül nach 10 PCR-Zyklen?", ["Jeder Zyklus verdoppelt die DNA.", "2¹⁰ = 1024"], "1024 Kopien")],
          [("Große DNA-Stücke wandern im Gel am weitesten.", "Kleine Stücke wandern am weitesten."), ("DNA wandert zum Minuspol.", "DNA ist negativ geladen und wandert zum Pluspol."),
           ("Die Taq-Polymerase wird bei 94 °C zerstört.", "Sie stammt aus einem hitzeliebenden Bakterium und ist hitzestabil.")],
          [("Wozu dient ein Antibiotikaresistenz-Gen im Plasmid?", "Nur Bakterien mit Plasmid überleben auf Antibiotika-Nährboden, so findet man die erfolgreich veränderten Zellen."),
           ("Warum ist der genetische Fingerabdruck so sicher?", "Die Muster nichtcodierender, sich wiederholender Abschnitte sind bei jedem Menschen anders, außer bei eineiigen Zwillingen."),
           ("Was ist ein Primer?", "Ein kurzes DNA-Stück, das den Startpunkt für die Polymerase festlegt.")],
          [("PCR-Schritte", [("Denaturierung", "etwa 94 °C, die Stränge trennen sich"), ("Anlagerung", "etwa 55 °C, Primer binden"), ("Elongation", "etwa 72 °C, Taq-Polymerase verlängert"),
                             ("ein Zyklus", "verdoppelt die DNA-Menge"), ("Primer", "legt den Startpunkt fest"), ("Taq-Polymerase", "hitzestabile DNA-Polymerase"), ("Nucleotide", "Bausteine für die neuen Stränge")],
            "Was gilt für {k}?", "Was ist gemeint? {v}"),
           ("Methoden", [("PCR", "vervielfältigt DNA"), ("Gelelektrophorese", "trennt DNA-Stücke nach Größe"), ("Restriktionsenzym", "schneidet DNA an Erkennungssequenzen"), ("Ligase", "verknüpft DNA-Stücke"),
                         ("CRISPR/Cas", "schneidet gezielt an einer Stelle im Genom"), ("DNA-Sequenzierung", "bestimmt die Basenfolge"), ("Plasmid", "Vektor zur Übertragung eines Gens in Bakterien"), ("Gensonde", "markiert einen gesuchten Abschnitt")],
            "Was leistet {k}?", "Welche Methode {v}?"),
           ("Gelbild", [("kleines Fragment", "wandert am weitesten"), ("großes Fragment", "bleibt nahe der Tasche"), ("gleiche Banden bei Spur und Täter", "DNA stimmt überein"),
                        ("Kind hat eine Bande, die keiner der Eltern hat", "Abstammung fraglich"), ("DNA-Leiter", "Vergleich bekannter Fragmentgrößen"), ("Gel mit Stromrichtung", "DNA wandert zum Pluspol")],
            "Was bedeutet im Gelbild: {k}?", "Woran erkennt man: {v}?")],
          ["PCR vervielfältigt DNA.", "Jeder PCR-Zyklus verdoppelt die DNA.", "DNA wandert im Gel zum Pluspol.", "Kleine DNA-Stücke wandern am weitesten.",
           "Restriktionsenzyme schneiden an Erkennungssequenzen.", "Die Taq-Polymerase ist hitzestabil.", "Plasmide dienen als Vektoren.", "CRISPR/Cas schneidet gezielt im Genom."],
          [("Große DNA-Stücke wandern am weitesten.", "Kleine wandern am weitesten."), ("DNA wandert zum Minuspol.", "Sie wandert zum Pluspol."), ("Die Taq-Polymerase wird bei 94 °C zerstört.", "Sie ist hitzestabil."),
           ("PCR trennt DNA nach Größe.", "Das macht die Gelelektrophorese."), ("Ligasen schneiden DNA.", "Ligasen verknüpfen DNA."), ("Nach 3 PCR-Zyklen gibt es 6 Kopien.", "Es gibt 8 Kopien.")],
          "molekulargenetische Methoden", "living-things-and-ecosystems"),

        H("B", "humangenetik-und-stammbaumanalyse", "Humangenetik und Stammbaumanalyse", "Stammbaumanalyse",
          "Die Schülerinnen und Schüler werten Stammbäume aus, unterscheiden autosomal-dominante, autosomal-rezessive und X-chromosomal-rezessive Erbgänge und berechnen Erkrankungswahrscheinlichkeiten.",
          "Karyogramm, Autosomen und Gonosomen, Erbgänge, Konduktorin, Stammbaumanalyse, Mukoviszidose, Chorea Huntington, Rot-Grün-Sehschwäche, Bluterkrankheit, genetische Beratung",
          "Gesunde Eltern, krankes Kind: der Erbgang ist rezessiv", "X-chromosomal-rezessive Krankheiten treten viel häufiger bei Männern auf.",
          ["Autosomal-dominant: Jeder Merkmalsträger hat mindestens einen betroffenen Elternteil. Autosomal-rezessiv: Gesunde Eltern können ein krankes Kind haben, beide sind dann Träger (Aa).",
           "X-chromosomal-rezessiv: Männer (XY) erkranken, wenn ihr einziges X das Allel trägt. Frauen sind meist Konduktorinnen. Ein kranker Vater gibt das Allel nie an Söhne weiter.",
           "Die Wahrscheinlichkeit berechnet man mit Kreuzungsschemata: Bei Aa × Aa ist ein Kind mit 25 Prozent aa."],
          [("Eine Konduktorin (XᴬXᵃ) und ein gesunder Mann (XᴬY) bekommen einen Sohn. Wie wahrscheinlich ist er krank?", ["Der Sohn erhält sein X von der Mutter.", "Mit 50 Prozent erhält er Xᵃ."], "50 Prozent")],
          [("Bei dominanten Krankheiten haben gesunde Eltern oft kranke Kinder.", "Das spricht für einen rezessiven Erbgang."), ("Ein kranker Vater vererbt X-chromosomale Krankheiten an seine Söhne.", "Söhne erhalten vom Vater das Y-Chromosom."),
           ("Konduktorinnen sind krank.", "Konduktorinnen tragen das Allel, sind aber meist gesund.")],
          [("Was ist Mukoviszidose?", "Eine autosomal-rezessive Krankheit, bei der zäher Schleim Lunge und Verdauung belastet."), ("Was ist Chorea Huntington?", "Eine autosomal-dominante Krankheit des Nervensystems, die meist erst im Erwachsenenalter beginnt."),
           ("Wozu dient genetische Beratung?", "Familien erfahren Risiken und Möglichkeiten, die Entscheidung bleibt bei ihnen.")],
          [("Erbgänge", [("Mukoviszidose", "autosomal-rezessiv"), ("Phenylketonurie", "autosomal-rezessiv"), ("Sichelzellanämie", "autosomal-rezessiv"), ("Albinismus", "autosomal-rezessiv"),
                         ("Chorea Huntington", "autosomal-dominant"), ("Marfan-Syndrom", "autosomal-dominant"), ("Bluterkrankheit (Hämophilie A)", "X-chromosomal-rezessiv"), ("Rot-Grün-Sehschwäche", "X-chromosomal-rezessiv"),
                         ("Duchenne-Muskeldystrophie", "X-chromosomal-rezessiv")],
            "Welcher Erbgang liegt vor bei {k}?", None),
           ("Hinweise im Stammbaum", [("gesunde Eltern haben ein krankes Kind", "rezessiver Erbgang"), ("jeder Kranke hat einen kranken Elternteil", "spricht für dominanten Erbgang"), ("fast nur Männer betroffen", "spricht für X-chromosomal-rezessiv"),
                                      ("kranker Vater hat eine kranke Tochter mit gesunder Mutter", "nicht X-chromosomal-rezessiv"), ("Krankheit überspringt Generationen", "spricht für rezessiven Erbgang"), ("Kranker Vater, alle Töchter Konduktorinnen", "X-chromosomal-rezessiv")],
            "Was folgt daraus? {k}", None),
           ("Begriffe der Humangenetik", [("Karyogramm", "geordnetes Bild aller Chromosomen einer Zelle"), ("Autosom", "Chromosom, das kein Geschlechtschromosom ist"), ("Gonosom", "Geschlechtschromosom (X oder Y)"),
                                          ("Konduktorin", "Frau, die ein rezessives X-Allel trägt, aber gesund ist"), ("homozygot", "mit zwei gleichen Allelen"), ("heterozygot", "mit zwei verschiedenen Allelen"),
                                          ("Genotyp", "die Kombination der Allele"), ("Phänotyp", "das sichtbare Erscheinungsbild"), ("Allel", "eine Ausprägungsform eines Gens"), ("Merkmalsträger", "Person, bei der das Merkmal ausgeprägt ist")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Gesunde Eltern mit krankem Kind sprechen für einen rezessiven Erbgang.", "Söhne erhalten das X-Chromosom von der Mutter.", "Konduktorinnen sind meist gesund.", "Mukoviszidose wird autosomal-rezessiv vererbt.",
           "Chorea Huntington wird autosomal-dominant vererbt.", "X-chromosomal-rezessive Krankheiten betreffen vor allem Männer.", "Aa × Aa ergibt mit 25 Prozent ein krankes Kind (rezessiv).", "Die Bluterkrankheit ist X-chromosomal-rezessiv."],
          [("Söhne erhalten das X-Chromosom vom Vater.", "Sie erhalten es von der Mutter."), ("Konduktorinnen sind immer krank.", "Sie sind meist gesund."), ("Mukoviszidose ist dominant.", "Sie ist rezessiv."),
           ("X-chromosomal-rezessive Krankheiten betreffen vor allem Frauen.", "Sie betreffen vor allem Männer."), ("Dominante Krankheiten überspringen oft Generationen.", "Das tun eher rezessive."),
           ("Chorea Huntington ist X-chromosomal.", "Sie ist autosomal-dominant.")],
          "die Humangenetik", "living-things-and-ecosystems", calc=f_erb),

        H("C", "saeure-base-gleichgewichte-und-ph-wert", "Säure-Base-Gleichgewichte und pH-Wert", "pH-Wert",
          "Die Schülerinnen und Schüler beschreiben Säure-Base-Reaktionen nach Brønsted als Protonenübergänge, berechnen pH-Werte starker Säuren und Basen und vergleichen Säurestärken mit dem pK<sub>S</sub>-Wert.",
          "Brønsted-Säuren und -Basen, korrespondierende Säure-Base-Paare, Ampholyte, Autoprotolyse des Wassers, Ionenprodukt, pH und pOH, starke und schwache Säuren, pKS-Wert",
          "Säuren geben Protonen ab, Basen nehmen Protonen auf", "pH = −lg c(H₃O⁺). Ein kleiner pKS-Wert bedeutet eine starke Säure.",
          ["Nach Brønsted ist eine Säure ein Protonendonator, eine Base ein Protonenakzeptor. Säure und Base, die sich um ein Proton unterscheiden, bilden ein korrespondierendes Paar.",
           "Wasser protolysiert selbst: K<sub>W</sub> = c(H₃O⁺) · c(OH⁻) = 10⁻¹⁴ mol²/l². Daraus folgt pH + pOH = 14. Neutral ist pH = 7.",
           "Starke Säuren protolysieren vollständig: pH = −lg c₀. Schwache Säuren nur teilweise. Je kleiner der pK<sub>S</sub>-Wert, desto stärker die Säure."],
          [("Welchen pH-Wert hat Salzsäure mit c = 0,01 mol/l?", ["Salzsäure ist stark: c(H₃O⁺) = 0,01 mol/l = 10⁻² mol/l.", "pH = −lg 10⁻² = 2"], "pH = 2")],
          [("Eine verdünnte Säure ist eine schwache Säure.", "Stärke (Protolysegrad) und Konzentration sind verschiedene Dinge."), ("Wasser enthält keine Ionen.", "Durch Autoprotolyse enthält Wasser H₃O⁺ und OH⁻."),
           ("pH 2 ist doppelt so sauer wie pH 4.", "pH 2 hat die hundertfache H₃O⁺-Konzentration.")],
          [("Was ist ein Ampholyt?", "Ein Teilchen, das als Säure und als Base reagieren kann, zum Beispiel Wasser oder HCO₃⁻."), ("Warum ist Essigsäure schwach?", "Sie gibt in Wasser nur einen kleinen Teil ihrer Protonen ab (pK<sub>S</sub> = 4,75)."),
           ("Was ist die korrespondierende Base von HCl?", "Das Chloridion Cl⁻.")],
          [("Korrespondierende Paare", [("HCl", "Cl⁻"), ("H₂O als Säure", "OH⁻"), ("H₃O⁺", "H₂O"), ("NH₄⁺", "NH₃"), ("CH₃COOH", "CH₃COO⁻"), ("H₂SO₄", "HSO₄⁻"), ("HSO₄⁻", "SO₄²⁻"), ("H₂CO₃", "HCO₃⁻"), ("HCO₃⁻ als Säure", "CO₃²⁻")],
            "Welche korrespondierende Base gehört zur Säure {k}?", "Welche Säure gehört zur Base {v}?"),
           ("Stark oder schwach?", {"den starken Säuren": ["Salzsäure", "Schwefelsäure", "Salpetersäure", "Perchlorsäure", "Bromwasserstoffsäure"],
                                    "den schwachen Säuren": ["Essigsäure", "Kohlensäure", "Ameisensäure", "Ammoniumion", "Blausäure", "Citronensäure", "Schwefelwasserstoff", "Milchsäure"]}),
           ("Begriffe", [("Brønsted-Säure", "Protonendonator"), ("Brønsted-Base", "Protonenakzeptor"), ("Ampholyt", "kann als Säure und als Base reagieren"), ("Autoprotolyse", "Wasser reagiert mit sich selbst zu H₃O⁺ und OH⁻"),
                         ("Ionenprodukt des Wassers", "10⁻¹⁴ mol²/l² bei 25 °C"), ("pK<sub>S</sub>-Wert", "Maß für die Säurestärke"), ("Protolyse", "Protonenübergang von einer Säure auf eine Base")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Säuren sind Protonendonatoren.", "Basen sind Protonenakzeptoren.", "pH + pOH = 14 bei 25 °C.", "Wasser ist ein Ampholyt.",
           "Ein kleiner pK<sub>S</sub>-Wert bedeutet eine starke Säure.", "pH 2 ist hundertmal saurer als pH 4.", "Starke Säuren protolysieren vollständig.", "Die korrespondierende Base von NH₄⁺ ist NH₃."],
          [("Säuren sind Protonenakzeptoren.", "Säuren geben Protonen ab."), ("Wasser enthält keine Ionen.", "Es enthält durch Autoprotolyse Ionen."), ("Ein großer pK<sub>S</sub>-Wert bedeutet eine starke Säure.", "Er bedeutet eine schwache Säure."),
           ("pH 2 ist doppelt so sauer wie pH 4.", "Es ist hundertmal saurer."), ("Verdünnte Säuren sind schwache Säuren.", "Stärke und Konzentration sind verschieden."), ("Essigsäure ist eine starke Säure.", "Sie ist schwach.")],
          "Säuren und Basen", "matter", calc=f_ph),

        H("C", "titration-und-puffer", "Titration und Puffersysteme", "Titration und Puffer",
          "Die Schülerinnen und Schüler führen Säure-Base-Titrationen aus, werten Titrationskurven aus, bestimmen Konzentrationen am Äquivalenzpunkt und erklären die Wirkung von Puffersystemen.",
          "Maßlösung, Bürette, Äquivalenzpunkt, Halbäquivalenzpunkt, Indikatorwahl, Titrationskurve starker und schwacher Säuren, Puffer, Henderson-Hasselbalch-Gleichung, Blutpuffer",
          "Am Äquivalenzpunkt ist n(Säure) = n(Base)", "Ein Puffer aus schwacher Säure und ihrer Base hält den pH-Wert fast konstant.",
          ["Bei der Titration gibt man eine Maßlösung bekannter Konzentration aus der Bürette zu. Am Äquivalenzpunkt gilt c₁ · V₁ = c₂ · V₂ (bei einprotonigen Säuren).",
           "Die Titrationskurve einer starken Säure mit starker Base hat einen steilen Sprung um pH 7. Bei schwachen Säuren liegt der Äquivalenzpunkt im Basischen, am Halbäquivalenzpunkt gilt pH = pK<sub>S</sub>.",
           "Ein Puffer enthält eine schwache Säure und ihre korrespondierende Base. Zugegebene H₃O⁺- oder OH⁻-Ionen werden abgefangen. Henderson-Hasselbalch: pH = pK<sub>S</sub> + lg(c(A⁻) : c(HA))."],
          [("Ein Essigsäure-Acetat-Puffer enthält gleich viel Säure und Base (pK<sub>S</sub> = 4,75). Welchen pH-Wert hat er?", ["pH = pKS + lg 1", "lg 1 = 0"], "pH = 4,75")],
          [("Am Äquivalenzpunkt ist der pH-Wert immer 7.", "Nur bei starker Säure mit starker Base, bei schwacher Säure liegt er im Basischen."), ("Ein Puffer verhindert jede pH-Änderung.", "Er dämpft sie nur, bis seine Kapazität erschöpft ist."),
           ("Jeder Indikator passt zu jeder Titration.", "Der Umschlagsbereich muss im Sprungbereich liegen.")],
          [("Welcher Puffer wirkt im Blut?", "Vor allem der Kohlensäure-Hydrogencarbonat-Puffer, er hält den pH-Wert bei etwa 7,4."), ("Was ist der Halbäquivalenzpunkt?", "Die Hälfte der Säure ist neutralisiert, dort gilt pH = pK<sub>S</sub>."),
           ("Warum nimmt man Phenolphthalein für Essigsäure?", "Sein Umschlag liegt bei pH 8 bis 10, im Sprungbereich der Titration einer schwachen Säure.")],
          [("Titrationskurven", [("starke Säure mit starker Base", "Äquivalenzpunkt bei pH 7"), ("schwache Säure mit starker Base", "Äquivalenzpunkt im basischen Bereich"), ("schwache Base mit starker Säure", "Äquivalenzpunkt im sauren Bereich"),
                                 ("Halbäquivalenzpunkt einer schwachen Säure", "pH = pK<sub>S</sub>"), ("flacher Bereich vor dem Sprung", "Pufferbereich"), ("steiler Anstieg", "Sprungbereich um den Äquivalenzpunkt")],
            "Was gilt? {k}", "Wozu passt: {v}?"),
           ("Indikatoren", [("Methylorange", "Umschlag bei etwa pH 3 bis 4,4"), ("Bromthymolblau", "Umschlag bei etwa pH 6 bis 7,6"), ("Phenolphthalein", "Umschlag bei etwa pH 8,2 bis 10"),
                            ("Methylrot", "Umschlag bei etwa pH 4,4 bis 6,2"), ("Universalindikator", "Mischung, zeigt viele pH-Werte durch Farben")],
            "Wo schlägt {k} um?", "Welcher Indikator hat {v}?", ("Umschlag bei pH 12 bis 14",)),
           ("Puffer", [("Essigsäure und Natriumacetat", "Puffer um pH 4,75"), ("Kohlensäure und Hydrogencarbonat", "Blutpuffer um pH 7,4"), ("Ammonium und Ammoniak", "Puffer um pH 9,25"),
                       ("Dihydrogenphosphat und Hydrogenphosphat", "Puffer um pH 7,2"), ("Salzsäure und Natriumchlorid", "kein Puffer"), ("Natronlauge und Kochsalz", "kein Puffer")],
            "Was gilt für {k}?", "Welches Paar ist {v}?")],
          ["Am Äquivalenzpunkt sind Säure und Base stöchiometrisch gleich.", "Bei schwachen Säuren liegt der Äquivalenzpunkt im Basischen.", "Am Halbäquivalenzpunkt gilt pH = pK<sub>S</sub>.", "Puffer enthalten eine schwache Säure und ihre Base.",
           "Der Blutpuffer hält den pH bei etwa 7,4.", "Ein Puffer hat eine begrenzte Kapazität.", "Phenolphthalein schlägt im Basischen um.", "c₁ · V₁ = c₂ · V₂ gilt am Äquivalenzpunkt einprotoniger Säuren."],
          [("Der Äquivalenzpunkt liegt immer bei pH 7.", "Nur bei starker Säure und starker Base."), ("Ein Puffer verhindert jede pH-Änderung.", "Er dämpft sie nur."), ("Salzsäure und Kochsalz bilden einen Puffer.", "HCl ist stark, das ist kein Puffer."),
           ("Am Halbäquivalenzpunkt gilt pH = 7.", "Dort gilt pH = pK<sub>S</sub>."), ("Methylorange schlägt bei pH 9 um.", "Es schlägt bei pH 3 bis 4,4 um."), ("Der Blutpuffer hält pH 5.", "Er hält etwa pH 7,4.")],
          "Titration und Puffer", "matter", calc=f_titr),

        H("C", "redoxreaktionen-und-elektrochemie", "Redoxreaktionen und galvanische Zellen", "Elektrochemie",
          "Die Schülerinnen und Schüler beschreiben Redoxreaktionen als Elektronenübergänge, bestimmen Oxidationszahlen, nutzen die elektrochemische Spannungsreihe und berechnen Zellspannungen galvanischer Zellen.",
          "Oxidation und Reduktion als Elektronenabgabe und -aufnahme, Oxidationszahlen, Redoxpaare, Daniell-Element, Halbzellen, Salzbrücke, Standardwasserstoffelektrode, Standardpotenziale, Spannungsreihe",
          "Oxidation ist Elektronenabgabe, Reduktion Elektronenaufnahme", "Zellspannung = E°(Kathode) − E°(Anode). Das unedlere Metall ist der Minuspol.",
          ["Oxidation ist Elektronenabgabe, Reduktion ist Elektronenaufnahme. Oxidationszahlen helfen beim Aufstellen von Redoxgleichungen: Die Oxidationszahl steigt bei der Oxidation.",
           "In einer galvanischen Zelle laufen Oxidation (Anode, Minuspol) und Reduktion (Kathode, Pluspol) räumlich getrennt ab. Die Salzbrücke schließt den Stromkreis.",
           "Standardpotenziale werden gegen die Standardwasserstoffelektrode (0 V) gemessen. Je kleiner E°, desto unedler. Zellspannung U = E°(Kathode) − E°(Anode), beim Daniell-Element 0,34 V − (−0,76 V) = 1,10 V."],
          [("Ein Eisennagel wird in Kupfersulfatlösung getaucht. Was passiert?", ["Eisen (−0,41 V) ist unedler als Kupfer (+0,34 V).", "Eisen gibt Elektronen an Cu²⁺ ab."], "Kupfer scheidet sich ab, Eisen geht in Lösung.")],
          [("An der Anode findet die Reduktion statt.", "An der Anode findet die Oxidation statt."), ("Das edlere Metall ist der Minuspol.", "Das unedlere Metall gibt Elektronen ab und ist der Minuspol."),
           ("Die Salzbrücke leitet Elektronen.", "Die Salzbrücke leitet Ionen, Elektronen fließen durch den Draht.")],
          [("Was ist die Oxidationszahl von Mn in KMnO₄?", "+VII, denn K ist +I und die vier O-Atome sind zusammen −VIII."), ("Warum braucht man eine Salzbrücke?", "Sie gleicht die Ladungen in den Halbzellen durch Ionenwanderung aus."),
           ("Wovon hängt das Potenzial ab?", "Von Konzentration und Temperatur. Das beschreibt die Nernst-Gleichung.")],
          [("Begriffe", [("Oxidation", "Elektronenabgabe"), ("Reduktion", "Elektronenaufnahme"), ("Anode", "Elektrode, an der oxidiert wird"), ("Kathode", "Elektrode, an der reduziert wird"),
                         ("Salzbrücke", "schließt den Stromkreis durch Ionenwanderung"), ("Standardwasserstoffelektrode", "Bezugselektrode mit 0 V"), ("Oxidationsmittel", "nimmt Elektronen auf"),
                         ("Reduktionsmittel", "gibt Elektronen ab")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Standardpotenziale", [("Li/Li⁺", "−3,04 V"), ("Mg/Mg²⁺", "−2,37 V"), ("Al/Al³⁺", "−1,66 V"), ("Zn/Zn²⁺", "−0,76 V"), ("Fe/Fe²⁺", "−0,41 V"), ("Pb/Pb²⁺", "−0,13 V"),
                                   ("H₂/H₃O⁺", "0 V"), ("Cu/Cu²⁺", "+0,34 V"), ("Ag/Ag⁺", "+0,80 V"), ("Cl⁻/Cl₂", "+1,36 V")],
            "Welches Standardpotenzial hat {k}?", "Welches Redoxpaar hat E° = {v}?"),
           ("Oxidationszahlen", [("S in H₂SO₄", "+VI"), ("Mn in KMnO₄", "+VII"), ("Cr in K₂Cr₂O₇", "+VI"), ("N in NH₃", "−III"), ("N in HNO₃", "+V"), ("C in CO₂", "+IV"),
                                 ("C in CH₄", "−IV"), ("O in H₂O₂", "−I"), ("Fe in Fe₂O₃", "+III"), ("Cl in Cl₂", "0")],
            "Welche Oxidationszahl hat {k}?", None)],
          ["Oxidation ist Elektronenabgabe.", "An der Anode wird oxidiert.", "Das unedlere Metall ist der Minuspol.", "Die Standardwasserstoffelektrode hat 0 V.",
           "Das Daniell-Element liefert etwa 1,10 V.", "Die Salzbrücke leitet Ionen.", "Zink ist unedler als Kupfer.", "Die Oxidationszahl steigt bei der Oxidation."],
          [("An der Anode wird reduziert.", "An der Anode wird oxidiert."), ("Das edlere Metall ist der Minuspol.", "Das unedlere ist der Minuspol."), ("Die Salzbrücke leitet Elektronen.", "Sie leitet Ionen."),
           ("Reduktion ist Elektronenabgabe.", "Reduktion ist Elektronenaufnahme."), ("Kupfer ist unedler als Zink.", "Zink ist unedler."), ("Die Oxidationszahl sinkt bei der Oxidation.", "Sie steigt.")],
          "die Elektrochemie", "matter", calc=f_redox),

        H("C", "batterien-akkus-und-elektrolyse", "Batterien, Akkus, Brennstoffzellen und Elektrolyse", "Batterien und Elektrolyse",
          "Die Schülerinnen und Schüler beschreiben Aufbau und Vorgänge in Batterien, Akkumulatoren und Brennstoffzellen, erklären Elektrolyse und Korrosion und bewerten elektrochemische Energiespeicher.",
          "Primär- und Sekundärelemente, Alkali-Mangan-Batterie, Bleiakku, Lithium-Ionen-Akku, Brennstoffzelle, Elektrolyse, Zersetzungsspannung, Überspannung, Korrosion, Opferanode, Galvanisieren",
          "Elektrolyse: Spannung erzwingt eine Redoxreaktion", "Akkus lassen sich durch Elektrolyse wieder aufladen, Batterien nicht.",
          ["Batterien (Primärelemente) wandeln chemische Energie einmalig in elektrische um. Akkus (Sekundärelemente) können durch Laden wieder in den Ausgangszustand gebracht werden.",
           "Bei der Elektrolyse wird eine Redoxreaktion durch eine äußere Spannung erzwungen. Am Minuspol (Kathode) wird reduziert, am Pluspol (Anode) oxidiert.",
           "In der Brennstoffzelle reagieren Wasserstoff und Sauerstoff kontrolliert zu Wasser. Korrosion ist eine elektrochemische Reaktion. Eine Opferanode aus unedlerem Metall schützt Eisen."],
          [("Was entsteht bei der Elektrolyse von Wasser am Minuspol?", ["Am Minuspol werden Elektronen aufgenommen.", "H₃O⁺ bzw. H₂O wird reduziert."], "Wasserstoff")],
          [("Bei der Elektrolyse ist die Kathode der Pluspol.", "Bei der Elektrolyse ist die Kathode der Minuspol."), ("Eine Brennstoffzelle verbrennt Wasserstoff mit einer Flamme.", "Die Reaktion läuft kontrolliert ohne Flamme an Elektroden."),
           ("Eine Opferanode muss edler sein als Eisen.", "Sie muss unedler sein, damit sie statt des Eisens oxidiert wird.")],
          [("Wie funktioniert ein Lithium-Ionen-Akku?", "Beim Entladen wandern Li⁺-Ionen von der Graphit-Anode zur Metalloxid-Kathode, beim Laden zurück."),
           ("Was ist Galvanisieren?", "Ein Gegenstand wird als Kathode in eine Metallsalzlösung gehängt und durch Elektrolyse mit Metall überzogen."), ("Was ist Überspannung?", "Zusätzliche Spannung, die über das Potenzial hinaus nötig ist, besonders bei Gasabscheidung.")],
          [("Energiespeicher", [("Alkali-Mangan-Batterie", "Primärelement, nicht wiederaufladbar"), ("Bleiakku", "Starterbatterie im Auto"), ("Lithium-Ionen-Akku", "Smartphone und E-Auto"),
                                ("Wasserstoff-Brennstoffzelle", "wandelt Wasserstoff und Sauerstoff in Strom und Wasser um"), ("Nickel-Metallhydrid-Akku", "wiederaufladbare Mignonzelle"), ("Zink-Luft-Batterie", "Hörgerätebatterie")],
            "Wofür steht {k}?", "Welcher Speicher ist das: {v}?"),
           ("Elektrolyse oder galvanisches Element?", {"den galvanischen Elementen": ["Taschenlampenbatterie beim Entladen", "Daniell-Element", "Brennstoffzelle", "Akku beim Entladen", "Zitronenbatterie"],
                                                       "den Elektrolysen": ["Akku beim Laden", "Aluminiumherstellung aus Schmelze", "Verkupfern eines Schlüssels", "Wasserstoffgewinnung aus Wasser", "Chloralkali-Elektrolyse", "Versilbern eines Löffels", "Raffination von Kupfer"]}),
           ("Elektrolyse-Produkte", [("Wasser, Minuspol", "Wasserstoff"), ("Wasser, Pluspol", "Sauerstoff"), ("Kochsalzlösung, Pluspol", "Chlor"), ("Kupferchloridlösung, Minuspol", "Kupfer"),
                                     ("Zinkiodidlösung, Pluspol", "Iod"), ("Aluminiumoxidschmelze, Minuspol", "Aluminium"), ("Kochsalzlösung, Minuspol", "Wasserstoff")],
            "Was entsteht? {k}", None)],
          ["Akkus sind wiederaufladbar.", "Bei der Elektrolyse ist die Kathode der Minuspol.", "In der Brennstoffzelle entsteht Wasser.", "Eine Opferanode ist unedler als Eisen.",
           "Beim Laden eines Akkus läuft eine Elektrolyse.", "Korrosion ist eine elektrochemische Reaktion.", "Beim Galvanisieren ist der Gegenstand die Kathode.", "Aluminium wird durch Schmelzflusselektrolyse gewonnen."],
          [("Batterien lassen sich beliebig oft laden.", "Nur Akkus sind wiederaufladbar."), ("Bei der Elektrolyse ist die Kathode der Pluspol.", "Sie ist der Minuspol."), ("Eine Opferanode ist edler als Eisen.", "Sie ist unedler."),
           ("Brennstoffzellen verbrennen Wasserstoff mit Flamme.", "Die Reaktion läuft kontrolliert ohne Flamme."), ("Bei der Wasserelektrolyse entsteht am Minuspol Sauerstoff.", "Dort entsteht Wasserstoff."),
           ("Beim Galvanisieren ist der Gegenstand die Anode.", "Er ist die Kathode.")],
          "Batterien und Elektrolyse", "matter"),

        H("P", "elektrisches-feld-und-kondensator", "Elektrisches Feld und Kondensator", "Elektrisches Feld",
          "Die Schülerinnen und Schüler beschreiben elektrische Felder mit Feldlinien und Feldstärke, berechnen Kräfte auf Ladungen und Größen am Plattenkondensator und beschreiben Auf- und Entladevorgänge.",
          "Ladung, Coulomb-Gesetz, Feldlinien, Feldstärke E = F : q, homogenes Feld E = U : d, Kondensator, Kapazität C = Q : U, Energie W = ½CU², Auf- und Entladekurve, Millikan-Versuch",
          "Im Plattenkondensator ist das Feld homogen: E = U : d", "Die Kapazität gibt an, wie viel Ladung pro Volt gespeichert wird: C = Q : U.",
          ["Ein elektrisches Feld übt auf Ladungen Kräfte aus. Die Feldstärke ist E = F : q in N/C. Feldlinien zeigen von Plus nach Minus.",
           "Zwischen zwei parallelen Platten ist das Feld homogen, E = U : d. Ein Kondensator speichert Ladung: C = Q : U in Farad. Die gespeicherte Energie ist W = ½ · C · U².",
           "Beim Laden über einen Widerstand steigt die Spannung zuerst schnell, dann langsamer. Beim Entladen nimmt der Strom exponentiell ab."],
          [("Zwischen zwei Platten im Abstand 2 cm liegen 200 V. Wie groß ist E?", ["E = U : d", "200 V : 0,02 m = 10 000 V/m"], "10 000 V/m")],
          [("Feldlinien zeigen von Minus nach Plus.", "Feldlinien zeigen von Plus nach Minus."), ("Ein Kondensator erzeugt Energie.", "Er speichert Energie, die beim Laden zugeführt wurde."),
           ("Doppelte Spannung gibt doppelte gespeicherte Energie.", "W wächst mit U², also vierfach.")],
          [("Was bewies der Millikan-Versuch?", "Die elektrische Ladung tritt nur in Vielfachen der Elementarladung e = 1,6 · 10⁻¹⁹ C auf."), ("Wovon hängt die Kapazität ab?", "Von der Plattenfläche, dem Abstand und dem Material zwischen den Platten."),
           ("Wo braucht man Kondensatoren?", "In Blitzgeräten, Netzteilen, Defibrillatoren und als Speicher in Schaltungen.")],
          [("Größen", [("Feldstärke", "Kraft pro Ladung, E = F : q"), ("Kapazität", "Ladung pro Spannung, C = Q : U"), ("Elementarladung", "e ≈ 1,6 · 10⁻¹⁹ C"), ("Farad", "Einheit der Kapazität"),
                       ("Coulomb", "Einheit der Ladung"), ("Energie im Kondensator", "W = ½ · C · U²"), ("homogenes Feld", "überall gleiche Feldstärke und Richtung")],
            "Was beschreibt „{k}“?", "Was ist gemeint? {v}"),
           ("Anwendungen und Versuche", [("Millikan-Versuch", "zeigt, dass Ladung in Vielfachen von e auftritt"), ("Blitzgerät einer Kamera", "Kondensator gibt Energie schnell ab"), ("Defibrillator", "Kondensator entlädt sich durch das Herz"),
                                         ("Faradaykäfig", "schirmt elektrische Felder ab"), ("Elektronenkanone", "beschleunigt Elektronen im elektrischen Feld"), ("Kopierer", "Toner haftet an geladenen Stellen der Trommel"),
                                         ("Elektrofilter im Kraftwerk", "geladene Staubteilchen werden an Platten abgeschieden"), ("Touchscreen", "der Finger ändert die Kapazität"), ("Elektroskop", "zeigt Ladung durch abstoßende Zeiger an")],
            "Was zeigt oder nutzt {k}?", "Wo wird das genutzt: {v}?"),
           ("Feldformen", [("einzelne positive Ladung", "radiale Feldlinien nach außen"), ("einzelne negative Ladung", "radiale Feldlinien nach innen"), ("Plattenkondensator", "parallele Feldlinien, homogen"),
                           ("zwei ungleichnamige Ladungen", "Feldlinien verbinden die Ladungen"), ("zwei gleichnamige Ladungen", "Feldlinien stoßen sich ab, Mitte feldfrei"), ("Inneres eines Faradaykäfigs", "feldfrei")],
            "Wie sieht das Feld aus? {k}", "Wo gibt es {v}?")],
          ["Feldlinien zeigen von Plus nach Minus.", "Im Plattenkondensator ist das Feld homogen.", "Die Kapazität ist Ladung durch Spannung.", "Die Energie im Kondensator wächst mit U².",
           "Ladung tritt in Vielfachen der Elementarladung auf.", "Das Innere eines Faradaykäfigs ist feldfrei.", "Größere Plattenfläche erhöht die Kapazität.", "E = U : d gilt im Plattenkondensator."],
          [("Feldlinien zeigen von Minus nach Plus.", "Sie zeigen von Plus nach Minus."), ("Ein Kondensator erzeugt Energie.", "Er speichert sie."), ("Doppelte Spannung gibt doppelte Energie.", "Sie gibt vierfache Energie."),
           ("Größerer Plattenabstand erhöht die Kapazität.", "Er verringert sie."), ("Im Faradaykäfig ist das Feld besonders stark.", "Er ist innen feldfrei."), ("Die Einheit der Kapazität ist das Coulomb.", "Sie ist das Farad.")],
          "das elektrische Feld", "energy", calc=f_kond),

        H("P", "magnetfeld-und-lorentzkraft", "Magnetfeld und Lorentzkraft", "Lorentzkraft",
          "Die Schülerinnen und Schüler beschreiben magnetische Felder von Dauermagneten, Leitern und Spulen, berechnen die Kraft auf stromdurchflossene Leiter und bewegte Ladungen und erklären Fadenstrahlrohr und Hall-Effekt.",
          "Magnetfeldlinien, magnetische Flussdichte B in Tesla, Feld einer langen Spule, Kraft auf Leiter F = B · I · l, Lorentzkraft F = q · v · B, Drei-Finger-Regel, Fadenstrahlrohr, spezifische Ladung, Hall-Effekt",
          "Bewegte Ladungen im Magnetfeld erfahren die Lorentzkraft", "Die Lorentzkraft steht senkrecht auf v und B und zwingt Elektronen auf eine Kreisbahn.",
          ["Die magnetische Flussdichte B (Tesla) beschreibt die Stärke des Magnetfelds. Im Innern einer langen Spule ist das Feld nahezu homogen.",
           "Auf einen Leiter senkrecht zum Feld wirkt F = B · I · l. Auf eine bewegte Ladung wirkt die Lorentzkraft F = q · v · B. Die Richtung liefert die Drei-Finger-Regel.",
           "Da die Lorentzkraft immer senkrecht zur Bewegung steht, beschreibt ein Elektron im homogenen Feld eine Kreisbahn mit r = m · v : (e · B). So bestimmt man im Fadenstrahlrohr die spezifische Ladung e : m."],
          [("Ein Leiter (0,2 m) mit 5 A steht senkrecht in einem Feld von 0,1 T. Welche Kraft wirkt?", ["F = B · I · l", "0,1 · 5 · 0,2 = 0,1 N"], "0,1 N")],
          [("Die Lorentzkraft beschleunigt das Elektron auf der Kreisbahn.", "Sie ändert nur die Richtung, der Betrag der Geschwindigkeit bleibt gleich."), ("Ruhende Ladungen erfahren eine Lorentzkraft.", "Nur bewegte Ladungen erfahren sie."),
           ("Die Kraft wirkt in Richtung der Feldlinien.", "Sie wirkt senkrecht zu Feld und Bewegungsrichtung.")],
          [("Was misst eine Hall-Sonde?", "Die magnetische Flussdichte: Im Halbleiterplättchen entsteht durch die Lorentzkraft eine Spannung proportional zu B."),
           ("Warum leuchtet die Bahn im Fadenstrahlrohr?", "Die Elektronen stoßen Gasatome an, die dabei Licht aussenden."), ("Wie stark ist das Erdmagnetfeld?", "In Deutschland etwa 50 Mikrotesla.")],
          [("Größen und Gesetze", [("Tesla", "Einheit der magnetischen Flussdichte"), ("Kraft auf einen Leiter", "F = B · I · l"), ("Lorentzkraft", "F = q · v · B"), ("Bahnradius im Fadenstrahlrohr", "r = m · v : (e · B)"),
                                   ("spezifische Ladung des Elektrons", "e : m ≈ 1,76 · 10¹¹ C/kg"), ("Feld einer langen Spule", "nahezu homogen im Innern"), ("Hall-Spannung", "proportional zur Flussdichte")],
            "Was gilt für {k}?", "Was ist gemeint? {v}"),
           ("Anwendungen", [("Elektromotor", "Kraft auf stromdurchflossene Leiter"), ("Fadenstrahlrohr", "Bestimmung von e : m"), ("Hall-Sonde", "Messung der Flussdichte"), ("Massenspektrometer", "Trennung von Ionen nach Masse"),
                            ("Lautsprecher", "Kraft auf eine Spule im Dauermagnetfeld"), ("Polarlicht", "geladene Teilchen werden vom Erdfeld zu den Polen gelenkt"), ("Zyklotron", "Beschleunigung von Teilchen auf Spiralbahnen")],
            "Was wird bei {k} genutzt?", "Wo wird {v} genutzt?"),
           ("Was ändert sich?", [("doppelte Geschwindigkeit im Fadenstrahlrohr", "doppelter Bahnradius"), ("doppelte Flussdichte im Fadenstrahlrohr", "halber Bahnradius"), ("Leiter parallel zu den Feldlinien", "keine Kraft"),
                                 ("Stromrichtung umkehren", "Kraft kehrt sich um"), ("doppelte Stromstärke im Leiter", "doppelte Kraft"), ("Elektron statt Proton gleicher Geschwindigkeit", "Ablenkung in Gegenrichtung")],
            "Was folgt daraus? {k}", None)],
          ["Bewegte Ladungen erfahren im Magnetfeld die Lorentzkraft.", "Die Lorentzkraft steht senkrecht zur Bewegung.", "Elektronen beschreiben im homogenen Feld eine Kreisbahn.", "Auf einen Leiter parallel zum Feld wirkt keine Kraft.",
           "Die Einheit der Flussdichte ist das Tesla.", "Doppelte Flussdichte halbiert den Bahnradius.", "Hall-Sonden messen die Flussdichte.", "Die Lorentzkraft ändert den Betrag der Geschwindigkeit nicht."],
          [("Ruhende Ladungen erfahren die Lorentzkraft.", "Nur bewegte Ladungen."), ("Die Lorentzkraft wirkt entlang der Feldlinien.", "Sie wirkt senkrecht dazu."), ("Die Lorentzkraft beschleunigt das Elektron.", "Sie ändert nur die Richtung."),
           ("Auf einen Leiter parallel zum Feld wirkt die größte Kraft.", "Dort wirkt keine Kraft."), ("Doppelte Flussdichte verdoppelt den Bahnradius.", "Sie halbiert ihn."), ("Die Einheit von B ist das Weber.", "Sie ist das Tesla.")],
          "die Lorentzkraft", "energy", calc=f_mag),

        H("P", "elektromagnetische-induktion", "Elektromagnetische Induktion", "Induktion",
          "Die Schülerinnen und Schüler erklären Induktion durch Änderung des magnetischen Flusses, wenden das Induktionsgesetz und die lenzsche Regel an und beschreiben Generator, Transformator und Selbstinduktion.",
          "magnetischer Fluss Φ = B · A, Induktionsgesetz U = −N · ΔΦ : Δt, lenzsche Regel, Wirbelströme, Generator, Wechselspannung, Effektivwert, Transformator, Selbstinduktion, Induktivität",
          "Ändert sich der magnetische Fluss, entsteht Spannung", "Die lenzsche Regel: Der Induktionsstrom wirkt seiner Ursache entgegen.",
          ["Der magnetische Fluss ist Φ = B · A (Weber). Ändert sich Φ in einer Spule, wird eine Spannung induziert: U = −N · ΔΦ : Δt.",
           "Lenzsche Regel: Der induzierte Strom ist so gerichtet, dass sein Magnetfeld der Änderung entgegenwirkt. Das erklärt Wirbelstrombremsen.",
           "Ein Generator erzeugt durch Drehen einer Spule eine sinusförmige Wechselspannung. Der ideale Transformator gilt U₁ : U₂ = N₁ : N₂ und I₁ : I₂ = N₂ : N₁."],
          [("Ein Trafo hat 1000 und 50 Windungen und liegt an 230 V. Welche Spannung gibt er ab?", ["U₂ = U₁ · N₂ : N₁", "230 · 50 : 1000"], "11,5 V")],
          [("Ein ruhender Magnet in einer Spule induziert Spannung.", "Nur eine Änderung des Flusses induziert Spannung."), ("Der Induktionsstrom verstärkt seine Ursache.", "Er wirkt ihr nach der lenzschen Regel entgegen."),
           ("Ein Trafo erhöht Spannung und Strom gleichzeitig.", "Steigt die Spannung, sinkt der Strom, die Leistung bleibt (ideal) gleich.")],
          [("Was ist der Effektivwert?", "Der Wert einer Gleichspannung mit gleicher Leistung. Bei Sinusspannung ist U<sub>eff</sub> = U<sub>max</sub> : √2, im Netz 230 V."),
           ("Wie funktioniert die Wirbelstrombremse?", "In einer bewegten Metallscheibe entstehen Wirbelströme, deren Magnetfeld die Bewegung bremst."), ("Was ist Selbstinduktion?", "Eine Spule induziert bei Stromänderung in sich selbst eine Gegenspannung.")],
          [("Induktion oder nicht?", [("Magnet wird in die Spule geschoben", "Spannung wird induziert"), ("Magnet ruht in der Spule", "keine Spannung"), ("Spule dreht sich im Magnetfeld", "Wechselspannung"),
                                      ("Strom in der Nachbarspule wird eingeschaltet", "kurzer Spannungsstoß"), ("Gleichstrom fließt konstant in der Nachbarspule", "keine Spannung"), ("Leiterschleife wird aus dem Feld gezogen", "Spannung wird induziert"),
                                      ("Fläche einer Leiterschleife im Feld wird verkleinert", "Spannung wird induziert")],
            "Was passiert? {k}", None),
           ("Begriffe", [("magnetischer Fluss", "Φ = B · A"), ("Weber", "Einheit des magnetischen Flusses"), ("lenzsche Regel", "der Induktionsstrom wirkt seiner Ursache entgegen"), ("Wirbelströme", "Induktionsströme in ausgedehnten Leitern"),
                         ("Selbstinduktion", "Gegenspannung bei Stromänderung in der eigenen Spule"), ("Henry", "Einheit der Induktivität"), ("Effektivwert", "Wechselspannung mit gleicher Leistung wie eine Gleichspannung")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Anwendungen", [("Generator", "erzeugt Wechselspannung durch Drehung"), ("Transformator", "wandelt Wechselspannungen um"), ("Induktionsherd", "erhitzt den Topfboden durch Wirbelströme"),
                            ("Wirbelstrombremse", "bremst ohne Berührung"), ("Metalldetektor", "erkennt Metall durch Induktion"), ("kabelloses Laden", "überträgt Energie mit zwei Spulen"),
                            ("dynamisches Mikrofon", "wandelt Schall in Spannung um")],
            "Was leistet {k}?", "Welches Gerät {v}?")],
          ["Spannung wird nur bei Flussänderung induziert.", "Der Induktionsstrom wirkt seiner Ursache entgegen.", "Für den magnetischen Fluss gilt Φ = B · A.", "Ein Generator erzeugt Wechselspannung.",
           "Beim idealen Trafo gilt U₁ : U₂ = N₁ : N₂.", "Wirbelströme bremsen bewegte Metallscheiben.", "Der Effektivwert der Netzspannung beträgt 230 V.", "Steigt beim Trafo die Spannung, sinkt der Strom."],
          [("Ein ruhender Magnet induziert Spannung.", "Nur Änderungen induzieren."), ("Der Induktionsstrom verstärkt seine Ursache.", "Er wirkt ihr entgegen."), ("Ein Trafo erhöht Spannung und Strom.", "Der Strom sinkt dabei."),
           ("Transformatoren arbeiten mit Gleichspannung.", "Sie brauchen Wechselspannung."), ("Die Einheit des Flusses ist das Tesla.", "Sie ist das Weber."), ("Wirbelströme beschleunigen Metallscheiben.", "Sie bremsen sie.")],
          "die Induktion", "energy", calc=f_ind),

        H("P", "wellen-und-interferenz", "Mechanische Wellen und Interferenz", "Wellen und Interferenz",
          "Die Schülerinnen und Schüler beschreiben Transversal- und Longitudinalwellen, wenden c = λ · f an, erklären Reflexion, Beugung und Interferenz und bestimmen Wellenlängen am Doppelspalt und Gitter.",
          "Transversal- und Longitudinalwelle, Wellenlänge, Ausbreitungsgeschwindigkeit, huygenssches Prinzip, Reflexion, Brechung, Beugung, Interferenz, Gangunterschied, stehende Wellen, Doppelspalt, Gitter",
          "Bei Gangunterschied k · λ verstärken sich Wellen", "Bei Gangunterschied (k + ½) · λ löschen sie sich aus.",
          ["Eine Welle transportiert Energie, aber keine Materie. Bei Transversalwellen schwingen die Teilchen senkrecht, bei Longitudinalwellen parallel zur Ausbreitung. Es gilt c = λ · f.",
           "Nach Huygens ist jeder Punkt einer Wellenfront Ausgangspunkt einer Elementarwelle. Damit erklärt man Beugung hinter Spalten und Hindernissen.",
           "Treffen Wellen zusammen, überlagern sie sich (Interferenz). Maxima bei Gangunterschied k · λ, Minima bei (k + ½) · λ. Am Gitter gilt für kleine Winkel λ = g · a : e."],
          [("Ein Ton hat 440 Hz. Wie groß ist seine Wellenlänge in Luft (340 m/s)?", ["λ = c : f", "340 : 440 ≈ 0,773 m"], "etwa 0,77 m")],
          [("Mit der Welle wandert das Wasser mit.", "Die Teilchen schwingen nur um ihre Ruhelage, transportiert wird Energie."), ("Schall ist eine Transversalwelle.", "Schall in Luft ist eine Longitudinalwelle."),
           ("Beugung tritt nur bei Licht auf.", "Alle Wellen werden gebeugt, besonders an Öffnungen in der Größe der Wellenlänge.")],
          [("Was ist eine stehende Welle?", "Die Überlagerung zweier gegenläufiger Wellen mit festen Knoten und Bäuchen, zum Beispiel auf einer Gitarrensaite."),
           ("Warum hört man um die Ecke?", "Schallwellen haben Wellenlängen im Meterbereich und werden an Türen und Ecken stark gebeugt."), ("Wie arbeiten Kopfhörer mit Geräuschunterdrückung?", "Sie erzeugen Gegenschall, der den Lärm durch destruktive Interferenz auslöscht.")],
          [("Wellenarten", [("Schall in Luft", "Longitudinalwelle"), ("Welle auf einem Seil", "Transversalwelle"), ("Licht", "Transversalwelle"), ("P-Welle eines Erdbebens", "Longitudinalwelle"),
                            ("S-Welle eines Erdbebens", "Transversalwelle"), ("Druckwelle in einer Feder", "Longitudinalwelle"), ("Radiowelle", "Transversalwelle"), ("Schwingende Gitarrensaite", "Transversalwelle")],
            "Welche Wellenart ist das: {k}?", None, ("stehende Ruhe", "Teilchenstrahl")),
           ("Interferenz", [("Gangunterschied 0", "Verstärkung"), ("Gangunterschied λ", "Verstärkung"), ("Gangunterschied 2λ", "Verstärkung"), ("Gangunterschied λ/2", "Auslöschung"),
                            ("Gangunterschied 3λ/2", "Auslöschung"), ("Gangunterschied 5λ/2", "Auslöschung"), ("Gangunterschied 3λ", "Verstärkung"), ("Gangunterschied 4λ", "Verstärkung"), ("Gangunterschied 7λ/2", "Auslöschung"), ("Gangunterschied 9λ/2", "Auslöschung"), ("Gangunterschied 5λ", "Verstärkung"), ("Gangunterschied 11λ/2", "Auslöschung")],
            "Was passiert bei {k}?", None, ("Brechung", "Polarisation")),
           ("Begriffe", [("Wellenlänge", "Abstand zweier benachbarter Wellenberge"), ("Amplitude", "größte Auslenkung"), ("Beugung", "Ausbreitung in den Schattenraum hinter Hindernissen"), ("Interferenz", "Überlagerung von Wellen"),
                         ("Gangunterschied", "Wegdifferenz zweier Wellen"), ("Knoten", "Stelle einer stehenden Welle ohne Schwingung"), ("huygenssches Prinzip", "jeder Punkt einer Wellenfront sendet Elementarwellen aus"),
                         ("Kohärenz", "feste Phasenbeziehung zweier Wellen")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Wellen transportieren Energie, keine Materie.", "Schall in Luft ist longitudinal.", "Licht ist eine Transversalwelle.", "Für Wellen gilt c = λ · f.",
           "Gangunterschied λ führt zu Verstärkung.", "Gangunterschied λ/2 führt zu Auslöschung.", "Auch Schall wird gebeugt.", "Stehende Wellen haben Knoten und Bäuche."],
          [("Mit der Wasserwelle wandert das Wasser mit.", "Es schwingt nur um die Ruhelage."), ("Schall ist eine Transversalwelle.", "In Luft ist er longitudinal."), ("Gangunterschied λ führt zu Auslöschung.", "Er führt zu Verstärkung."),
           ("Nur Licht wird gebeugt.", "Alle Wellen werden gebeugt."), ("Für Wellen gilt c = λ : f.", "Es gilt c = λ · f."), ("Knoten schwingen besonders stark.", "Knoten schwingen nicht.")],
          "Wellen", "waves-and-light", calc=f_welle),
    ]
