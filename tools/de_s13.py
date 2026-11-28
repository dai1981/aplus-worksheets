# -*- coding: utf-8 -*-
"""Deutschland / Klasse 13（Oberstufe, Qualifikationsphase 2: Biologie, Chemie, Physik）"""
import math
from de_sci import H, nq, num


def f_hw(R):
    k = R.choice(["aa", "q", "het", "p2", "trag"])
    if k in ("aa", "q"):
        n = R.choice([100, 400, 900, 2500, 10000, 1600, 3600, 4900])
        q = 1 / math.sqrt(n)
        if k == "aa":
            return nq("In einer Population ist 1 von %s Personen homozygot rezessiv (aa). Wie groß ist die Allelfrequenz q (Hardy-Weinberg)?" % num(n), q,
                      [1 / n, 1 - q, 2 * q], "", "q² = 1 : %s, also q = √(1 : %s) = %s." % (num(n), num(n), num(q)))
        p = 1 - q
        return nq("In einer Population ist 1 von %s Personen homozygot rezessiv (aa). Wie groß ist die Allelfrequenz p des dominanten Allels?" % num(n), p,
                  [q, 1 - 1 / n, p * p], "", "q = √(1 : %s) = %s, p = 1 − q = %s." % (num(n), num(q), num(p)))
    p, q = R.choice([(0.9, 0.1), (0.8, 0.2), (0.7, 0.3), (0.6, 0.4), (0.95, 0.05), (0.99, 0.01), (0.75, 0.25)])
    if k == "het":
        return nq("In einer Population gilt p = %s und q = %s. Welcher Anteil ist heterozygot (Hardy-Weinberg)?" % (num(p), num(q)), 2 * p * q,
                  [p * q, q * q, p * p], "", "Anteil Aa = 2pq = 2 · %s · %s = %s." % (num(p), num(q), num(2 * p * q)))
    if k == "p2":
        return nq("In einer Population gilt p = %s und q = %s. Welcher Anteil ist homozygot dominant (AA)?" % (num(p), num(q)), p * p,
                  [2 * p * q, p, q * q], "", "Anteil AA = p² = %s² = %s." % (num(p), num(p * p)))
    N = R.choice([1000, 2000, 5000, 10000, 500])
    return nq("Eine Population mit %s Individuen hat q = %s. Wie viele Individuen sind heterozygote Träger (Hardy-Weinberg)?" % (num(N), num(q)), 2 * p * q * N,
              [q * q * N, p * q * N, q * N], "", "2pq · N = 2 · %s · %s · %s = %s." % (num(p), num(q), num(N), num(2 * p * q * N)))


def f_energ(R):
    k = R.choice(["E", "E", "eff", "stufe"])
    if k == "E":
        E, n = R.choice([(10000, 2), (50000, 3), (8000, 1), (200000, 3), (30000, 2), (1000000, 4), (6000, 1), (40000, 2)])
        names = ["Primärkonsumenten", "Sekundärkonsumenten", "Tertiärkonsumenten", "Quartärkonsumenten"]
        v = E * 0.1 ** n
        return nq("Produzenten binden %s kJ. Wie viel Energie gelangt etwa zu den %n (10-Prozent-Regel)?".replace("%n", names[n - 1]) % num(E), v,
                  [E * 0.1 ** (n + 1), E * 0.9 ** n, E * 0.1 ** (n - 1) if n > 1 else E / 2], "kJ",
                  "Pro Trophiestufe gehen etwa 90 Prozent verloren: %s kJ · 0,1%s = %s kJ." % (num(E), "" if n == 1 else "<sup>%d</sup>" % n, num(v)))
    if k == "eff":
        a, b = R.choice([(5000, 500), (20000, 1800), (800, 64), (12000, 1500), (3000, 150), (40000, 4800), (900, 81)])
        return nq("Eine Trophiestufe enthält %s kJ, die nächste %s kJ. Wie groß ist der ökologische Wirkungsgrad?" % (num(a), num(b)), 100 * b / a,
                  [100 * a / b, b / a, 100 - 100 * b / a], "%", "Wirkungsgrad = %s : %s · 100 %% = %s %%." % (num(b), num(a), num(100 * b / a)))
    E, v = R.choice([(10000, 10), (100000, 100), (50000, 5), (1000000, 100), (2000, 2), (300000, 30)])
    n = int(round(math.log10(E / v)))
    return nq("Produzenten binden %s kJ, eine Stufe erhält noch %s kJ. Die wievielte Konsumentenstufe ist das bei 10 Prozent Weitergabe?" % (num(E), num(v)), n,
              [n + 1, n - 1 if n > 1 else n + 2, n * 10], "", "%s : %s = 10<sup>%d</sup>, also %d Stufen über den Produzenten." % (num(E), num(v), n, n))


def f_poly(R):
    k = R.choice(["n", "n", "M"])
    mono = [("Ethen", 28), ("Propen", 42), ("Styrol", 104), ("Vinylchlorid", 62.5), ("Tetrafluorethen", 100)]
    m, Mm = R.choice(mono)
    if k == "n":
        n = R.choice([500, 1000, 2000, 5000, 800, 1500, 3000, 10000])
        M = n * Mm
        return nq("Ein Polymer aus %s (M = %s g/mol) hat eine mittlere molare Masse von %s g/mol. Wie groß ist der Polymerisationsgrad?" % (m, num(Mm), num(M)), n,
                  [M * Mm, n / 10, n * 2], "", "n = M(Polymer) : M(Monomer) = %s : %s = %s." % (num(M), num(Mm), num(n)))
    n = R.choice([500, 1000, 2000, 400, 2500, 1200])
    return nq("Ein Polymer aus %s (M = %s g/mol) hat den Polymerisationsgrad %s. Welche molare Masse hat es etwa?" % (m, num(Mm), num(n)), n * Mm,
              [n / Mm, n + Mm, n * Mm / 2], "g/mol", "M = n · M(Monomer) = %s · %s g/mol = %s g/mol." % (num(n), num(Mm), num(n * Mm)))


H_ = 6.63e-34
E_ = 1.6e-19


def f_photo(R):
    k = R.choice(["E", "E", "Ekin", "lam", "grenz"])
    if k == "E":
        lam = R.choice([400, 450, 500, 550, 600, 650, 700, 300, 250])
        E = H_ * 3e8 / (lam * 1e-9)
        return nq("Welche Energie hat ein Photon mit λ = %d nm? (h = 6,63 · 10⁻³⁴ Js, c = 3 · 10⁸ m/s)" % lam, E,
                  [H_ * lam * 1e-9 / 3e8, H_ * 3e8 / lam, E / E_], "J", "E = h · c : λ = %s J." % num(E))
    if k == "Ekin":
        Ep, W = R.choice([(3.1, 2.3), (4.1, 2.3), (2.8, 1.9), (5.0, 4.3), (3.5, 2.1), (6.2, 4.7), (4.0, 2.7), (3.3, 2.0)])
        return nq("Photonen mit %s eV treffen auf ein Metall mit Austrittsarbeit %s eV. Welche maximale kinetische Energie haben die Elektronen?" % (num(Ep), num(W)), round(Ep - W, 2),
                  [Ep + W, Ep, W], "eV", "E<sub>kin</sub> = h · f − W<sub>A</sub> = %s eV − %s eV = %s eV." % (num(Ep), num(W), num(round(Ep - W, 2))))
    if k == "lam":
        E_eV = R.choice([2.0, 2.5, 3.0, 1.5, 4.0, 1.8, 2.2])
        lam = 1240 / E_eV
        return nq("Ein Photon hat die Energie %s eV. Welche Wellenlänge hat es? (h · c ≈ 1240 eV · nm)" % num(E_eV), lam,
                  [E_eV * 1240, 1240 / E_eV / 2, lam * 10], "nm", "λ = 1240 eV · nm : %s eV = %s nm." % (num(E_eV), num(lam)))
    W = R.choice([2.3, 2.1, 4.3, 4.7, 1.9, 2.7, 3.1])
    f = W * E_ / H_
    return nq("Ein Metall hat die Austrittsarbeit %s eV. Wie groß ist die Grenzfrequenz? (h = 6,63 · 10⁻³⁴ Js, 1 eV = 1,6 · 10⁻¹⁹ J)" % num(W), f,
              [H_ / (W * E_), W / H_, f / 1000], "Hz", "f<sub>G</sub> = W<sub>A</sub> : h = %s J : 6,63 · 10⁻³⁴ Js = %s Hz." % (num(W * E_), num(f)))


def f_bohr(R):
    k = R.choice(["En", "En", "dE", "lam"])
    if k == "En":
        n = R.choice([1, 2, 3, 4, 5, 6])
        E = -13.6 / n ** 2
        return nq("Welche Energie hat das Elektron im Wasserstoffatom auf Niveau n = %d? (Eₙ = −13,6 eV : n²)" % n, E,
                  [-13.6 / n, -13.6 * n * n, 13.6 / n ** 2], "eV", "Eₙ = −13,6 eV : %d = %s eV." % (n * n, num(E)))
    a, b = R.choice([(2, 1), (3, 1), (3, 2), (4, 2), (4, 1), (5, 2), (4, 3), (6, 2), (5, 3)])
    dE = 13.6 * (1 / b ** 2 - 1 / a ** 2)
    if k == "dE":
        return nq("Ein Elektron im Wasserstoffatom springt von n = %d auf n = %d. Welche Energie hat das ausgesandte Photon?" % (a, b), dE,
                  [13.6 * (1 / b - 1 / a), 13.6 / (a - b) ** 2, 13.6 * (1 / b ** 2 + 1 / a ** 2)], "eV",
                  "ΔE = 13,6 eV · (1/%d − 1/%d) = %s eV." % (b * b, a * a, num(dE)))
    lam = 1240 / dE
    return nq("Beim Übergang von n = %d auf n = %d sendet Wasserstoff ein Photon mit %s eV aus. Welche Wellenlänge hat es? (h · c ≈ 1240 eV · nm)" % (a, b, num(dE)), lam,
              [dE * 1240, lam / 2, lam * 2], "nm", "λ = 1240 eV · nm : %s eV = %s nm." % (num(dE), num(lam)))


def f_hwz(R):
    k = R.choice(["rest", "rest", "zeit", "T"])
    nuc = [("Iod-131", 8, "Tage"), ("Cobalt-60", 5.3, "Jahre"), ("Caesium-137", 30, "Jahre"), ("Kohlenstoff-14", 5730, "Jahre"), ("Radon-222", 3.8, "Tage"),
           ("Technetium-99m", 6, "Stunden"), ("Strontium-90", 29, "Jahre"), ("Phosphor-32", 14, "Tage")]
    name, T, u = R.choice(nuc)
    n = R.choice([1, 2, 3, 4, 5])
    if k == "rest":
        m0 = R.choice([80, 160, 64, 200, 400, 32, 1000])
        return nq("Eine Probe enthält %s mg %s (Halbwertszeit %s %s). Wie viel ist nach %s %s noch vorhanden?" % (num(m0), name, num(T), u, num(n * T), u), m0 / 2 ** n,
                  [m0 / (2 * n), m0 - m0 / 2 ** n, m0 / 2 ** (n + 1)], "mg", "Nach %d Halbwertszeiten: %s mg · (½)<sup>%d</sup> = %s mg." % (n, num(m0), n, num(m0 / 2 ** n)))
    if k == "zeit":
        f = 2 ** n
        return nq("Nach welcher Zeit ist von %s (Halbwertszeit %s %s) nur noch 1/%d der Kerne übrig?" % (name, num(T), u, f), n * T,
                  [f * T, T / f, (n + 1) * T], u, "1/%d = (½)<sup>%d</sup>, also %d Halbwertszeiten: %d · %s = %s %s." % (f, n, n, n, num(T), num(n * T), u))
    t, n = R.choice([(12, 2), (24, 3), (30, 2), (60, 4), (36, 3), (48, 6), (90, 3), (24, 4), (30, 3), (60, 2), (40, 5), (16, 4)])
    return nq("Die Aktivität einer Probe sinkt in %d Tagen auf 1/%d. Wie groß ist die Halbwertszeit?" % (t, 2 ** n), t / n,
              [t * n, t / 2 ** n, t / (n + 1)], "Tage", "1/%d = (½)<sup>%d</sup>: %d Halbwertszeiten in %d Tagen, T = %s Tage." % (2 ** n, n, n, t, num(t / n)))


def f_lc(R):
    k = R.choice(["f", "f", "lam", "T"])
    if k == "f":
        L, C = R.choice([(1e-3, 1e-6), (1e-2, 1e-6), (2e-3, 5e-9), (5e-4, 2e-9), (1e-1, 1e-5), (4e-3, 1e-8), (1e-3, 2.5e-7)])
        f = float("%.3g" % (1 / (2 * math.pi * math.sqrt(L * C))))
        return nq("Ein Schwingkreis hat L = %s H und C = %s F. Wie groß ist seine Eigenfrequenz? (f = 1 : (2π√(L · C)))" % (num(L), num(C)), f,
                  [float("%.3g" % (1 / math.sqrt(L * C))), 2 * math.pi * math.sqrt(L * C), f * 2], "Hz", "f = 1 : (2π · √(%s · %s)) = %s Hz." % (num(L), num(C), num(f)))
    if k == "lam":
        f, nm = R.choice([(1e8, "UKW-Radio"), (2.4e9, "WLAN"), (9e5, "Mittelwellenradio"), (5e9, "WLAN"), (1.8e9, "Mobilfunk"), (6e14, "grünes Licht"), (3e10, "Radar"), (2.45e9, "Mikrowellenherd")])
        return nq("Welche Wellenlänge hat eine elektromagnetische Welle mit %s Hz (%s)? (c = 3 · 10⁸ m/s)" % (num(f), nm), 3e8 / f,
                  [f / 3e8, 3e8 * f, 3e8 / f * 10], "m", "λ = c : f = 3 · 10⁸ m/s : %s Hz = %s m." % (num(f), num(3e8 / f)))
    f = R.choice([50, 1000, 100, 500, 2000, 250])
    return nq("Ein Schwingkreis schwingt mit %s Hz. Wie lange dauert eine Periode?" % num(f), 1 / f, [f, 2 * math.pi / f, 1 / (2 * f)], "s",
              "T = 1 : f = 1 : %s Hz = %s s." % (num(f), num(1 / f)))


def UNITS(grade):
    return [
        H("B", "fotosynthese-lichtreaktion-und-calvin-zyklus", "Fotosynthese: Lichtreaktion und Calvin-Zyklus", "Fotosynthese",
          "Die Schülerinnen und Schüler erklären Bau und Funktion der Chloroplasten, die lichtabhängigen Reaktionen an der Thylakoidmembran und den Calvin-Zyklus und werten Versuche zu begrenzenden Faktoren aus.",
          "Chloroplast, Thylakoid, Stroma, Chlorophyll und Absorptionsspektrum, Fotosysteme I und II, Fotolyse des Wassers, Elektronentransport, ATP-Synthase, NADPH, Calvin-Zyklus, RuBisCO, begrenzende Faktoren",
          "Licht liefert ATP und NADPH, der Calvin-Zyklus bindet CO₂", "Der Sauerstoff der Fotosynthese stammt aus dem Wasser.",
          ["An der Thylakoidmembran absorbieren die Fotosysteme Licht. Wasser wird gespalten (Fotolyse), es entstehen O₂, Protonen und Elektronen. Die Elektronen wandern zum NADP⁺.",
           "Der Protonengradient treibt die ATP-Synthase an. ATP und NADPH sind die Produkte der Lichtreaktion.",
           "Im Stroma bindet RuBisCO CO₂ an Ribulose-1,5-bisphosphat. Mit ATP und NADPH wird daraus Zucker aufgebaut, der Akzeptor wird regeneriert. Licht, CO₂ und Temperatur können begrenzen."],
          [("Eine Pflanze bekommt Wasser mit schwerem Sauerstoff ¹⁸O. Wo findet man ¹⁸O wieder?", ["Die Fotolyse spaltet Wasser.", "Der Sauerstoff aus Wasser wird frei."], "im freigesetzten O₂")],
          [("Der Sauerstoff stammt aus dem CO₂.", "Er stammt aus dem Wasser (Fotolyse)."), ("Der Calvin-Zyklus läuft an der Thylakoidmembran.", "Er läuft im Stroma."),
           ("Grünes Licht wird am besten genutzt.", "Chlorophyll absorbiert vor allem Blau und Rot, Grün wird reflektiert.")],
          [("Warum heißt der Calvin-Zyklus lichtunabhängig?", "Er braucht kein Licht direkt, aber ATP und NADPH aus der Lichtreaktion."), ("Was ist ein begrenzender Faktor?", "Der Faktor im Minimum bestimmt die Fotosyntheserate."),
           ("Was macht RuBisCO?", "Das Enzym bindet CO₂ an Ribulose-1,5-bisphosphat. Es ist das häufigste Protein der Erde.")],
          [("Orte und Stoffe", [("Thylakoidmembran", "Ort der Lichtreaktion"), ("Stroma", "Ort des Calvin-Zyklus"), ("Fotolyse", "Spaltung von Wasser durch Licht"), ("ATP-Synthase", "nutzt den Protonengradienten"),
                                ("NADPH", "liefert Elektronen für den Calvin-Zyklus"), ("RuBisCO", "fixiert CO₂"), ("Chlorophyll a", "Hauptpigment der Fotosysteme"), ("Ribulose-1,5-bisphosphat", "CO₂-Akzeptor im Calvin-Zyklus")],
            "Was gilt für „{k}“?", "Was ist gemeint? {v}"),
           ("Lichtreaktion oder Calvin-Zyklus?", {"der Lichtreaktion": ["Fotolyse des Wassers", "Freisetzung von Sauerstoff", "Bildung von NADPH", "Anregung von Chlorophyll", "Elektronentransportkette", "Aufbau eines Protonengradienten"],
                                                   "dem Calvin-Zyklus": ["Fixierung von CO₂", "Bildung von Glucose", "Regeneration des Akzeptors", "Verbrauch von NADPH", "Arbeit von RuBisCO", "Bildung von Glycerinaldehyd-3-phosphat"]}),
           ("Begrenzende Faktoren", [("Rate steigt mit mehr Licht", "Licht ist begrenzend"), ("Rate steigt mit mehr CO₂", "CO₂ ist begrenzend"), ("Rate sinkt über 40 °C stark", "Enzyme denaturieren"),
                                     ("Rate steigt bei Kälte mit Erwärmung", "Temperatur ist begrenzend"), ("Rate bleibt trotz mehr Licht gleich", "ein anderer Faktor ist begrenzend"), ("Pflanze im Dunkeln", "nur Zellatmung, CO₂ wird abgegeben"),
                                     ("Lichtkompensationspunkt", "Fotosynthese und Atmung sind gleich stark")],
            "Was folgt daraus? {k}", None)],
          ["Der Sauerstoff der Fotosynthese stammt aus dem Wasser.", "Der Calvin-Zyklus läuft im Stroma.", "Die Lichtreaktion liefert ATP und NADPH.", "RuBisCO fixiert CO₂.",
           "Chlorophyll absorbiert vor allem blaues und rotes Licht.", "Die ATP-Synthase nutzt einen Protonengradienten.", "Der Faktor im Minimum begrenzt die Rate.", "Im Dunkeln betreiben Pflanzen nur Zellatmung."],
          [("Der Sauerstoff stammt aus dem CO₂.", "Er stammt aus dem Wasser."), ("Der Calvin-Zyklus läuft an der Thylakoidmembran.", "Er läuft im Stroma."), ("Grünes Licht wird am stärksten absorbiert.", "Es wird reflektiert."),
           ("Die Lichtreaktion bildet Glucose.", "Glucose entsteht im Calvin-Zyklus."), ("RuBisCO spaltet Wasser.", "RuBisCO fixiert CO₂."), ("Der Calvin-Zyklus braucht kein ATP.", "Er verbraucht ATP und NADPH.")],
          "die Fotosynthese", "living-things-and-ecosystems"),

        H("B", "evolutionstheorie-und-artbildung", "Evolutionstheorie und Artbildung", "Evolution und Artbildung",
          "Die Schülerinnen und Schüler erklären Evolution mit der synthetischen Theorie, berechnen Allelfrequenzen mit dem Hardy-Weinberg-Gesetz, beschreiben Artbildung und deuten Homologien und Stammbäume.",
          "Variation, Mutation, Rekombination, Selektionsformen, Gendrift, Genfluss, Hardy-Weinberg-Gesetz, Isolationsmechanismen, allopatrische und sympatrische Artbildung, adaptive Radiation, Homologie und Analogie",
          "Evolution ist die Änderung von Allelfrequenzen", "Hardy-Weinberg: p² + 2pq + q² = 1, solange keine Evolutionsfaktoren wirken.",
          ["Evolutionsfaktoren sind Mutation, Rekombination, Selektion, Gendrift und Genfluss. Sie verändern die Allelfrequenzen im Genpool einer Population.",
           "Im Hardy-Weinberg-Gleichgewicht (große Population, keine Selektion, keine Mutation, keine Wanderung, Zufallspaarung) gilt p + q = 1 und p² + 2pq + q² = 1.",
           "Neue Arten entstehen durch Isolation: räumlich (allopatrisch) oder ohne räumliche Trennung (sympatrisch, zum Beispiel durch Polyploidie). Homologe Organe zeigen gemeinsame Abstammung."],
          [("1 von 2500 Menschen hat Mukoviszidose (aa). Wie häufig sind Träger?", ["q² = 1/2500, q = 0,02, p = 0,98", "2pq = 2 · 0,98 · 0,02 ≈ 0,039"], "etwa 4 Prozent, also 1 von 25")],
          [("Lebewesen passen sich gezielt an, weil sie es brauchen.", "Mutationen entstehen zufällig, die Selektion wählt aus."), ("Individuen evolvieren.", "Populationen evolvieren, ihre Allelfrequenzen ändern sich."),
           ("Flügel von Vogel und Insekt sind homolog.", "Sie sind analog: gleiche Funktion, aber verschiedene Herkunft.")],
          [("Was ist Gendrift?", "Zufällige Änderung der Allelfrequenzen, besonders stark in kleinen Populationen (Flaschenhals, Gründereffekt)."), ("Was ist adaptive Radiation?", "Aus einer Stammart entstehen viele Arten mit verschiedenen ökologischen Nischen, zum Beispiel die Darwinfinken."),
           ("Was ist eine biologische Art?", "Eine Gruppe von Lebewesen, die sich untereinander fruchtbar fortpflanzen kann.")],
          [("Evolutionsfaktoren", [("Mutation", "neue Allele entstehen zufällig"), ("Rekombination", "Allele werden bei der Meiose neu kombiniert"), ("Selektion", "besser angepasste Individuen haben mehr Nachkommen"),
                                   ("Gendrift", "zufällige Änderung der Allelfrequenz in kleinen Populationen"), ("Genfluss", "Allele gelangen durch Wanderung in eine Population"), ("Isolation", "verhindert den Genaustausch zwischen Populationen"),
                                   ("Gründereffekt", "wenige Individuen gründen eine neue Population")],
            "Was bewirkt {k}?", "Welcher Faktor ist das: {v}?"),
           ("Homolog oder analog?", {"den homologen Organen": ["Arm des Menschen und Flügel der Fledermaus", "Vorderbein des Pferdes und Flosse des Wals", "Blütenblätter und Laubblätter", "Gehörknöchelchen und Kiefergelenk der Reptilien", "Flügel von Vogel und Fledermaus (Knochenbau)", "Stoßzähne des Elefanten und Schneidezähne des Menschen"],
                                     "den analogen Organen": ["Flügel von Vogel und Insekt", "Grabbein von Maulwurf und Maulwurfsgrille", "Auge von Tintenfisch und Mensch", "Körperform von Hai und Delfin", "Dornen der Berberitze und Stacheln der Rose", "Flosse des Pinguins und Flosse des Fisches"]}),
           ("Artbildung", [("Population wird durch ein Gebirge getrennt", "allopatrische Artbildung"), ("Chromosomensatz verdoppelt sich in einer Pflanze", "sympatrische Artbildung durch Polyploidie"),
                           ("unterschiedliche Balzgesänge", "ethologische Isolation"), ("Blütezeit zu verschiedenen Jahreszeiten", "zeitliche Isolation"), ("Bastarde sind unfruchtbar", "postzygotische Isolation"),
                           ("Darwinfinken auf den Galapagosinseln", "adaptive Radiation"), ("Geschlechtsorgane passen nicht zusammen", "mechanische Isolation")],
            "Was liegt vor? {k}", None)],
          ["Evolution ist die Änderung von Allelfrequenzen.", "Mutationen entstehen zufällig.", "Gendrift wirkt in kleinen Populationen stark.", "Im Hardy-Weinberg-Gleichgewicht gilt p + q = 1.",
           "Homologe Organe zeigen gemeinsame Abstammung.", "Flügel von Vogel und Insekt sind analog.", "Populationen evolvieren, nicht Individuen.", "Polyploidie kann zu sympatrischer Artbildung führen."],
          [("Lebewesen passen sich gezielt an.", "Mutationen sind zufällig."), ("Individuen evolvieren.", "Populationen evolvieren."), ("Flügel von Vogel und Insekt sind homolog.", "Sie sind analog."),
           ("Gendrift wirkt in großen Populationen am stärksten.", "Sie wirkt in kleinen am stärksten."), ("Im Hardy-Weinberg-Gleichgewicht wirkt Selektion.", "Dort wirkt keine Selektion."),
           ("Allopatrische Artbildung braucht keine räumliche Trennung.", "Sie beruht auf räumlicher Trennung.")],
          "die Evolution", "living-things-and-ecosystems", calc=f_hw),

        H("B", "energiefluss-und-stoffkreislaeufe", "Energiefluss und Stoffkreisläufe im Ökosystem", "Energiefluss",
          "Die Schülerinnen und Schüler beschreiben Trophiestufen, Nahrungsnetze und Energiepyramiden, berechnen den Energiefluss und erklären Kohlenstoff- und Stickstoffkreislauf.",
          "Produzenten, Konsumenten, Destruenten, Trophiestufen, Nahrungsnetz, Biomasse- und Energiepyramide, ökologischer Wirkungsgrad, Primärproduktion, Kohlenstoffkreislauf, Stickstoffkreislauf",
          "Energie fließt durch das Ökosystem, Stoffe kreisen", "Pro Trophiestufe gehen etwa 90 Prozent der Energie verloren, vor allem als Wärme.",
          ["Produzenten bauen mit Lichtenergie Biomasse auf. Konsumenten fressen Biomasse, Destruenten bauen tote Biomasse zu Mineralstoffen ab.",
           "Bei jedem Schritt im Nahrungsnetz gehen etwa 90 Prozent der Energie durch Atmung, Wärme und Ausscheidung verloren. Darum sind Nahrungsketten kurz.",
           "Kohlenstoff kreist zwischen Atmosphäre (CO₂), Lebewesen und Gesteinen. Stickstoff wird von Bakterien gebunden (N₂-Fixierung), nitrifiziert und denitrifiziert."],
          [("Gras bindet 100 000 kJ. Wie viel erreicht ein Fuchs als Sekundärkonsument?", ["Gras → Hase (10 %) → Fuchs (10 %)", "100 000 · 0,1 · 0,1"], "etwa 1000 kJ")],
          [("Energie wird im Ökosystem recycelt.", "Energie fließt hindurch und geht als Wärme verloren, nur Stoffe kreisen."), ("Destruenten sind unwichtig.", "Ohne Destruenten würden keine Mineralstoffe zurückgewonnen."),
           ("Pflanzen holen den Stickstoff direkt aus der Luft.", "Nur bestimmte Bakterien können N₂ binden.")],
          [("Warum gibt es selten mehr als vier Trophiestufen?", "Es bleibt zu wenig Energie übrig, um weitere Stufen zu versorgen."), ("Was machen Knöllchenbakterien?", "Sie leben in den Wurzeln von Hülsenfrüchtlern und binden Luftstickstoff."),
           ("Wie greift der Mensch in den Kohlenstoffkreislauf ein?", "Durch Verbrennen fossiler Stoffe und Abholzen steigt der CO₂-Gehalt der Atmosphäre.")],
          [("Rollen im Ökosystem", [("Produzenten", "bauen mit Licht Biomasse auf"), ("Primärkonsumenten", "fressen Pflanzen"), ("Sekundärkonsumenten", "fressen Pflanzenfresser"), ("Destruenten", "bauen tote Biomasse zu Mineralstoffen ab"),
                                    ("Endkonsumenten", "haben keine Fressfeinde"), ("Nitrifizierer", "wandeln Ammonium in Nitrat um"), ("Denitrifizierer", "setzen N₂ in die Luft frei"), ("Knöllchenbakterien", "binden Luftstickstoff")],
            "Was tun {k}?", "Wer {v}?"),
           ("Kohlenstoffkreislauf", [("Fotosynthese", "entzieht der Luft CO₂"), ("Zellatmung", "gibt CO₂ an die Luft ab"), ("Verbrennung fossiler Stoffe", "setzt lange gespeicherten Kohlenstoff frei"),
                                     ("Zersetzung durch Destruenten", "gibt CO₂ aus toter Biomasse frei"), ("Meere", "lösen CO₂ und speichern es"), ("Kalkgestein", "langfristiger Kohlenstoffspeicher"),
                                     ("Moore", "speichern Kohlenstoff in Torf"), ("Abholzung", "verringert die CO₂-Aufnahme")],
            "Welche Rolle spielt {k}?", "Was ist gemeint? {v}"),
           ("Pyramiden", [("Energiepyramide", "nimmt nach oben immer ab"), ("Biomassepyramide eines Waldes", "nimmt nach oben ab"), ("Zahlenpyramide eines Baumes mit Insekten", "kann umgekehrt sein"),
                          ("Biomassepyramide im Meer zu einem Zeitpunkt", "kann umgekehrt sein (Plankton wächst schnell nach)"), ("Wirkungsgrad zwischen Stufen", "etwa 10 Prozent"),
                          ("Bruttoprimärproduktion", "gesamte Fotosyntheseleistung der Produzenten"), ("Nettoprimärproduktion", "Bruttoproduktion minus Atmung der Pflanzen")],
            "Was gilt für {k}?", "Was ist gemeint? {v}")],
          ["Energie fließt durch das Ökosystem.", "Stoffe kreisen im Ökosystem.", "Pro Stufe werden etwa 10 Prozent weitergegeben.", "Destruenten schließen die Stoffkreisläufe.",
           "Knöllchenbakterien binden Luftstickstoff.", "Die Energiepyramide ist nie umgekehrt.", "Zellatmung gibt CO₂ an die Luft ab.", "Moore speichern Kohlenstoff."],
          [("Energie wird im Ökosystem recycelt.", "Sie fließt hindurch."), ("Pro Stufe werden 90 Prozent weitergegeben.", "Etwa 10 Prozent."), ("Pflanzen binden N₂ direkt aus der Luft.", "Das können nur Bakterien."),
           ("Die Energiepyramide kann umgekehrt sein.", "Sie nimmt immer ab."), ("Destruenten erzeugen Energie.", "Sie bauen tote Biomasse ab."), ("Fotosynthese gibt CO₂ ab.", "Sie nimmt CO₂ auf.")],
          "den Energiefluss", "living-things-and-ecosystems", calc=f_energ),

        H("B", "oekosysteme-und-nachhaltigkeit", "Ökosysteme, Biodiversität und Nachhaltigkeit", "Nachhaltigkeit",
          "Die Schülerinnen und Schüler beschreiben Einflüsse des Menschen auf Ökosysteme, erklären Treibhauseffekt, Eutrophierung und Artenverlust und bewerten Maßnahmen für eine nachhaltige Entwicklung.",
          "Biodiversität, invasive Arten, Eutrophierung eines Sees, Treibhauseffekt, Ozeanversauerung, Flächenverbrauch, Ökosystemdienstleistungen, ökologischer Fußabdruck, Naturschutz, nachhaltige Nutzung",
          "Nachhaltig ist, was heute nutzt, ohne Morgen zu schaden", "Biodiversität sichert Ökosystemdienstleistungen wie Bestäubung und sauberes Wasser.",
          ["Biodiversität umfasst die Vielfalt der Gene, Arten und Ökosysteme. Ökosystemdienstleistungen sind zum Beispiel Bestäubung, Bodenbildung, Klimaregulation und sauberes Wasser.",
           "Zu viel Dünger (Nitrat, Phosphat) führt im See zur Eutrophierung: Algen wachsen, sterben, werden unter Sauerstoffverbrauch abgebaut, der See kann „umkippen“.",
           "Treibhausgase wie CO₂ und Methan verstärken den Treibhauseffekt. Nachhaltigkeit verbindet Ökologie, Wirtschaft und Soziales."],
          [("In einen See gelangt viel Phosphat aus Dünger. Was passiert zuerst?", ["Phosphat ist oft der Minimumfaktor.", "Algen vermehren sich stark."], "Algenblüte")],
          [("Der Treibhauseffekt ist an sich schädlich.", "Der natürliche Treibhauseffekt macht die Erde bewohnbar, der zusätzliche ist das Problem."), ("Ein eutrophierter See hat zu viel Sauerstoff.", "Durch den Abbau toter Algen fehlt Sauerstoff am Grund."),
           ("Invasive Arten bereichern immer die Vielfalt.", "Sie verdrängen oft heimische Arten.")],
          [("Was ist der ökologische Fußabdruck?", "Die Fläche, die nötig ist, um den Lebensstil eines Menschen dauerhaft zu ermöglichen."), ("Warum ist Ozeanversauerung gefährlich?", "Gelöstes CO₂ senkt den pH-Wert des Meeres, Korallen und Muscheln bilden schlechter Kalk."),
           ("Was bedeutet Nachhaltigkeit?", "Ressourcen so nutzen, dass sie auch künftigen Generationen zur Verfügung stehen.")],
          [("Eingriffe und Folgen", [("viel Dünger im See", "Eutrophierung"), ("CO₂ aus fossilen Brennstoffen", "verstärkter Treibhauseffekt"), ("CO₂ löst sich im Meer", "Ozeanversauerung"), ("Monokulturen", "einseitige Nutzung und Auslaugung des Bodens"),
                                     ("Waschbär in Europa", "invasive Art"), ("Versiegelung von Flächen", "Verlust von Lebensräumen"), ("Pestizide auf Feldern", "Rückgang von Insekten"), ("Überfischung", "Zusammenbruch von Fischbeständen")],
            "Was folgt aus {k}?", "Was führt zu {v}?"),
           ("Ökosystemdienstleistungen", [("Bienen", "Bestäubung von Nutzpflanzen"), ("Moore", "Speicherung von Kohlenstoff in Torf"), ("Wälder", "Schutz vor Erosion und Bildung von Grundwasser"),
                                         ("Auen", "Rückhalt von Hochwasser"), ("Regenwürmer", "Lockerung und Düngung des Bodens"), ("Feuchtgebiete", "Reinigung von Wasser"), ("Seegraswiesen", "Kinderstube für Fische")],
            "Welche Leistung erbringen {k}?", "Wer sorgt für {v}?"),
           ("Nachhaltig oder nicht?", {"den nachhaltigen Maßnahmen": ["Blühstreifen am Feldrand", "Renaturierung von Mooren", "Fischfang nach Fangquoten", "Mischwald statt Monokultur", "Strom aus Wind und Sonne", "Recycling von Kunststoff"],
                                        "den nicht nachhaltigen Maßnahmen": ["Trockenlegen von Mooren", "Überdüngung von Feldern", "Grundschleppnetze ohne Quote", "Abholzen von Regenwald für Weideland", "Kohlekraftwerke ohne Ersatz", "Müll im Meer entsorgen"]})],
          ["Biodiversität umfasst Gene, Arten und Ökosysteme.", "Zu viel Dünger führt zur Eutrophierung.", "Der natürliche Treibhauseffekt macht die Erde bewohnbar.", "Gelöstes CO₂ senkt den pH-Wert des Meeres.",
           "Invasive Arten können heimische Arten verdrängen.", "Moore speichern viel Kohlenstoff.", "Nachhaltigkeit berücksichtigt künftige Generationen.", "Im eutrophierten See fehlt am Grund Sauerstoff."],
          [("Ein eutrophierter See hat zu viel Sauerstoff.", "Am Grund fehlt Sauerstoff."), ("Der Treibhauseffekt ist an sich schädlich.", "Erst der zusätzliche ist ein Problem."), ("Invasive Arten fördern immer die Vielfalt.", "Sie verdrängen oft heimische Arten."),
           ("Ozeanversauerung erhöht den pH-Wert.", "Sie senkt ihn."), ("Trockengelegte Moore speichern mehr Kohlenstoff.", "Sie setzen ihn frei."), ("Monokulturen erhöhen die Artenvielfalt.", "Sie verringern sie.")],
          "die Nachhaltigkeit", "earths-systems"),

        H("C", "organische-reaktionsmechanismen", "Organische Reaktionsmechanismen", "Reaktionsmechanismen",
          "Die Schülerinnen und Schüler beschreiben radikalische Substitution, elektrophile Addition, nucleophile Substitution und Eliminierung, ordnen Reaktionen zu und erklären Induktive Effekte und Zwischenstufen.",
          "homolytische und heterolytische Spaltung, Radikal, Elektrophil, Nucleophil, radikalische Substitution, elektrophile Addition, Markownikow-Regel, nucleophile Substitution SN1 und SN2, Eliminierung, Kondensation, Esterbildung",
          "Elektrophile suchen, Nucleophile bieten Elektronen", "Alkane reagieren radikalisch, Alkene addieren elektrophil.",
          ["Bei der radikalischen Substitution (Alkan + Halogen, Licht) entstehen Radikale durch homolytische Spaltung. Start, Kettenreaktion und Abbruch bilden den Mechanismus.",
           "An die Doppelbindung der Alkene addieren Elektrophile wie Br₂ oder H⁺. Über ein Carbokation entsteht das Produkt. Nach Markownikow geht H an das C-Atom mit mehr H-Atomen.",
           "Bei der nucleophilen Substitution ersetzt ein Nucleophil (OH⁻) ein Halogenatom. Bei der Eliminierung wird ein kleines Molekül abgespalten, es entsteht eine Doppelbindung."],
          [("Ethen reagiert mit Bromwasser. Welche Reaktion liegt vor, was beobachtet man?", ["Br₂ addiert an die Doppelbindung.", "Das Produkt 1,2-Dibromethan ist farblos."], "elektrophile Addition, Bromwasser entfärbt sich")],
          [("Alkane entfärben Bromwasser sofort im Dunkeln.", "Alkane reagieren nur mit Licht und langsam (radikalische Substitution)."), ("Ein Nucleophil sucht Elektronen.", "Ein Nucleophil hat freie Elektronenpaare und sucht positive Zentren."),
           ("Bei der Esterbildung entsteht Wasserstoff.", "Es wird Wasser abgespalten (Kondensation).")],
          [("Was sagt die Markownikow-Regel?", "Bei der Addition von HX an unsymmetrische Alkene geht das H an das C-Atom, das schon mehr H-Atome hat."), ("Was ist ein Radikal?", "Ein Teilchen mit einem ungepaarten Elektron, es ist sehr reaktiv."),
           ("Wie unterscheidet man Alkan und Alken?", "Mit Bromwasser: Alkene entfärben es sofort, Alkane nicht.")],
          [("Mechanismen", [("Methan + Chlor im Licht", "radikalische Substitution"), ("Ethen + Brom", "elektrophile Addition"), ("Brommethan + Hydroxidion", "nucleophile Substitution"), ("Ethanol mit konz. Schwefelsäure erhitzt", "Eliminierung"),
                            ("Essigsäure + Ethanol", "Kondensation (Veresterung)"), ("Propen + Bromwasserstoff", "elektrophile Addition"), ("Ester + Natronlauge", "Verseifung (Hydrolyse)"), ("Ethen + Wasser mit Säure", "elektrophile Addition (Hydratisierung)")],
            "Welche Reaktion ist das: {k}?", None),
           ("Elektrophil oder Nucleophil?", {"den Elektrophilen": ["H⁺", "Br⁺", "Carbokation", "NO₂⁺", "AlCl₃", "SO₃"], "den Nucleophilen": ["OH⁻", "NH₃", "H₂O", "CN⁻", "Cl⁻", "Alkoholat-Ion"]}),
           ("Begriffe", [("Radikal", "Teilchen mit ungepaartem Elektron"), ("homolytische Spaltung", "jedes Atom erhält ein Elektron der Bindung"), ("heterolytische Spaltung", "ein Atom erhält beide Bindungselektronen"),
                         ("Carbokation", "positiv geladenes Kohlenstoff-Zwischenprodukt"), ("Elektrophil", "elektronenarmes Teilchen"), ("Nucleophil", "Teilchen mit freiem Elektronenpaar"),
                         ("Kettenabbruch", "zwei Radikale verbinden sich"), ("Markownikow-Regel", "H addiert an das C-Atom mit mehr H-Atomen")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Alkane reagieren mit Halogenen radikalisch.", "Alkene entfärben Bromwasser.", "Elektrophile sind elektronenarm.", "Nucleophile haben freie Elektronenpaare.",
           "Bei der Veresterung wird Wasser abgespalten.", "Bei der Eliminierung entsteht eine Doppelbindung.", "Radikale haben ein ungepaartes Elektron.", "Ester werden durch Natronlauge verseift."],
          [("Alkane entfärben Bromwasser sofort im Dunkeln.", "Alkene tun das."), ("Nucleophile sind elektronenarm.", "Elektrophile sind elektronenarm."), ("Bei der Veresterung entsteht Wasserstoff.", "Es entsteht Wasser."),
           ("Bei der Addition entsteht eine Doppelbindung.", "Die Doppelbindung wird aufgehoben."), ("Ein Radikal hat nur gepaarte Elektronen.", "Es hat ein ungepaartes Elektron."), ("Ethen + Brom ist eine Substitution.", "Es ist eine Addition.")],
          "Reaktionsmechanismen", "matter"),

        H("C", "aromaten-und-farbstoffe", "Aromaten und Farbstoffe", "Aromaten und Farbstoffe",
          "Die Schülerinnen und Schüler beschreiben das Benzolmolekül mit dem Mesomeriemodell, erklären die elektrophile Substitution und die Farbigkeit von Stoffen durch Lichtabsorption und konjugierte Doppelbindungen.",
          "Benzol, Mesomerie, Aromatizität, Hückel-Regel, elektrophile aromatische Substitution, Phenol, Anilin, Farbe und Komplementärfarbe, Absorption, konjugierte Doppelbindungen, Azofarbstoffe, Indikatoren",
          "Man sieht die Komplementärfarbe des absorbierten Lichts", "Je mehr konjugierte Doppelbindungen, desto langwelliger wird absorbiert.",
          ["Im Benzol (C₆H₆) sind sechs π-Elektronen über den Ring delokalisiert. Mesomere Grenzformeln beschreiben diesen Zustand. Benzol ist darum besonders stabil.",
           "Benzol addiert nicht wie Alkene, sondern reagiert durch elektrophile Substitution: Ein H-Atom wird ersetzt, das aromatische System bleibt erhalten (Katalysator FeBr₃).",
           "Farbstoffe absorbieren sichtbares Licht. Wir sehen die Komplementärfarbe. Ein großes System konjugierter Doppelbindungen verschiebt die Absorption zu längeren Wellenlängen."],
          [("Ein Farbstoff absorbiert Licht um 450 nm (blau). Welche Farbe sieht man?", ["Man sieht die Komplementärfarbe.", "Blau ↔ Orange (Gelb)"], "orange bis gelb")],
          [("Benzol entfärbt Bromwasser wie ein Alken.", "Benzol addiert nicht, es reagiert nur mit Katalysator durch Substitution."), ("Ein roter Stoff absorbiert rotes Licht.", "Er absorbiert grünes Licht und reflektiert Rot."),
           ("Im Benzol wechseln echte Einfach- und Doppelbindungen.", "Alle Bindungen sind gleich lang, die Elektronen sind delokalisiert.")],
          [("Was sagt die Hückel-Regel?", "Ebene, ringförmig konjugierte Systeme mit 4n + 2 π-Elektronen sind aromatisch, Benzol hat 6."), ("Warum ändern Indikatoren ihre Farbe?", "Durch Protonierung ändert sich das konjugierte System, damit die absorbierte Wellenlänge."),
           ("Was sind Azofarbstoffe?", "Farbstoffe mit der Gruppe –N=N– zwischen zwei Aromaten, zum Beispiel Methylorange.")],
          [("Komplementärfarben", [("absorbiert Violett", "erscheint gelbgrün"), ("absorbiert Blau", "erscheint orange"), ("absorbiert Blaugrün", "erscheint rot"), ("absorbiert Grün", "erscheint purpur"),
                                   ("absorbiert Gelb", "erscheint blau"), ("absorbiert Orange", "erscheint blaugrün"), ("absorbiert Rot", "erscheint grünblau"), ("absorbiert nichts Sichtbares", "erscheint weiß oder farblos")],
            "Welche Farbe sieht man? Ein Stoff {k}.", None),
           ("Aromaten", [("Benzol", "C₆H₆, sechs delokalisierte π-Elektronen"), ("Phenol", "Benzolring mit OH-Gruppe, schwach sauer"), ("Anilin", "Benzolring mit NH₂-Gruppe"), ("Toluol", "Benzolring mit Methylgruppe"),
                         ("Brombenzol", "Produkt der Bromierung von Benzol"), ("Nitrobenzol", "Produkt der Nitrierung von Benzol"), ("Naphthalin", "zwei kondensierte Benzolringe"), ("Benzoesäure", "Benzolring mit COOH-Gruppe")],
            "Was ist {k}?".replace("{k}", "„{k}“"), "Welcher Aromat ist gemeint: {v}?"),
           ("Begriffe", [("Mesomerie", "Beschreibung mit mehreren Grenzformeln"), ("Delokalisation", "Elektronen gehören nicht zu einer einzelnen Bindung"), ("elektrophile Substitution", "typische Reaktion des Benzols"),
                         ("Chromophor", "Molekülteil, der Licht absorbiert"), ("konjugierte Doppelbindungen", "abwechselnd Doppel- und Einfachbindungen"), ("Komplementärfarbe", "die Farbe, die man nach Absorption sieht"),
                         ("Azogruppe", "–N=N–"), ("Hückel-Regel", "4n + 2 π-Elektronen im ebenen Ring")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Benzol hat sechs delokalisierte π-Elektronen.", "Benzol reagiert durch elektrophile Substitution.", "Man sieht die Komplementärfarbe des absorbierten Lichts.", "Mehr konjugierte Doppelbindungen verschieben die Absorption ins Langwellige.",
           "Methylorange ist ein Azofarbstoff.", "Alle Bindungen im Benzol sind gleich lang.", "Phenol ist schwach sauer.", "Benzol hat nach Hückel 4n + 2 π-Elektronen."],
          [("Benzol entfärbt Bromwasser ohne Katalysator.", "Es braucht einen Katalysator."), ("Ein roter Stoff absorbiert rotes Licht.", "Er absorbiert grünes Licht."), ("Im Benzol gibt es feste Doppelbindungen.", "Die Elektronen sind delokalisiert."),
           ("Benzol reagiert typischerweise durch Addition.", "Es reagiert durch Substitution."), ("Weniger konjugierte Doppelbindungen machen Stoffe farbiger.", "Mehr konjugierte machen sie farbig."),
           ("Anilin enthält eine OH-Gruppe.", "Anilin enthält eine NH₂-Gruppe.")],
          "Aromaten und Farbstoffe", "matter"),

        H("C", "kunststoffe-und-polymerisation", "Kunststoffe und Polymerisation", "Polymere",
          "Die Schülerinnen und Schüler beschreiben Polymerisation, Polykondensation und Polyaddition, unterscheiden Thermoplaste, Duroplaste und Elastomere und bewerten Recycling und Biokunststoffe.",
          "Monomer und Polymer, Polymerisationsgrad, radikalische Polymerisation, Polykondensation (Polyester, Polyamide), Polyaddition, Thermoplaste, Duroplaste, Elastomere, Recycling, Biokunststoffe, Mikroplastik",
          "Viele Monomere verbinden sich zu einem Polymer", "Thermoplaste sind nicht vernetzt und schmelzen, Duroplaste sind stark vernetzt.",
          ["Bei der Polymerisation öffnen sich die Doppelbindungen der Monomere (z. B. Ethen → Polyethen). Bei der Polykondensation reagieren zwei funktionelle Gruppen, ein kleines Molekül wird abgespalten.",
           "Thermoplaste bestehen aus unvernetzten Ketten und werden beim Erwärmen weich. Elastomere sind schwach vernetzt und gummielastisch. Duroplaste sind engmaschig vernetzt und zersetzen sich beim Erhitzen.",
           "Kunststoffe kann man werkstofflich, rohstofflich oder energetisch verwerten. Biokunststoffe stammen aus nachwachsenden Rohstoffen oder sind biologisch abbaubar."],
          [("Ein Polyethen hat M = 28 000 g/mol. Wie groß ist der Polymerisationsgrad?", ["M(Ethen) = 28 g/mol", "28 000 : 28"], "1000")],
          [("Duroplaste lassen sich einschmelzen und neu formen.", "Das gilt für Thermoplaste, Duroplaste zersetzen sich."), ("Bei der Polymerisation entsteht Wasser.", "Bei der Polymerisation wird nichts abgespalten, bei der Polykondensation schon."),
           ("Biokunststoffe sind immer biologisch abbaubar.", "Manche Biokunststoffe aus Pflanzen sind nicht abbaubar.")],
          [("Wie entsteht Nylon?", "Durch Polykondensation einer Dicarbonsäure mit einem Diamin, dabei wird Wasser abgespalten."), ("Was ist Mikroplastik?", "Kunststoffteilchen unter 5 mm, die sich in Umwelt und Nahrungsketten anreichern."),
           ("Warum ist PET gut recycelbar?", "Es ist ein Thermoplast und lässt sich einschmelzen und neu verarbeiten.")],
          [("Kunststoffe und Monomere", [("Polyethen (PE)", "Ethen"), ("Polypropen (PP)", "Propen"), ("Polystyrol (PS)", "Styrol"), ("Polyvinylchlorid (PVC)", "Vinylchlorid"), ("Teflon (PTFE)", "Tetrafluorethen"),
                                         ("Plexiglas (PMMA)", "Methacrylsäuremethylester"), ("PET", "Terephthalsäure und Ethandiol"), ("Nylon", "Dicarbonsäure und Diamin")],
            "Aus welchem Monomer entsteht {k}?", "Welcher Kunststoff entsteht aus {v}?"),
           ("Kunststoffklassen", {"den Thermoplasten": ["Polyethen-Folie", "PET-Flasche", "Polystyrol-Becher", "Plexiglas", "PVC-Rohr"], "den Duroplasten": ["Bakelit-Steckdose", "Melaminharz-Teller", "Epoxidharz-Kleber", "Leiterplatte aus Harz"],
                                  "den Elastomeren": ["Autoreifen", "Gummiband", "Silikon-Backform", "Neopren-Anzug"]}),
           ("Reaktionen und Verwertung", [("Ethen zu Polyethen", "Polymerisation"), ("Diamin + Dicarbonsäure", "Polykondensation"), ("Diisocyanat + Diol", "Polyaddition (Polyurethan)"),
                                          ("Einschmelzen und neu formen", "werkstoffliche Verwertung"), ("Spalten in Öl und Gas", "rohstoffliche Verwertung"), ("Verbrennen mit Energiegewinnung", "energetische Verwertung"),
                                          ("Milchsäure zu PLA", "Polykondensation zu einem Biokunststoff")],
            "Was liegt vor? {k}", None)],
          ["Bei der Polymerisation wird nichts abgespalten.", "Bei der Polykondensation wird ein kleines Molekül abgespalten.", "Thermoplaste werden beim Erwärmen weich.", "Duroplaste sind stark vernetzt.",
           "Elastomere sind schwach vernetzt.", "Polyethen entsteht aus Ethen.", "Nylon ist ein Polyamid.", "Mikroplastik sind Teilchen unter 5 mm."],
          [("Duroplaste lassen sich einschmelzen.", "Sie zersetzen sich."), ("Bei der Polymerisation entsteht Wasser.", "Das ist bei der Polykondensation so."), ("Biokunststoffe sind immer abbaubar.", "Nicht alle sind abbaubar."),
           ("Thermoplaste sind stark vernetzt.", "Sie sind unvernetzt."), ("PVC entsteht aus Ethen.", "Es entsteht aus Vinylchlorid."), ("Autoreifen sind Duroplaste.", "Sie sind Elastomere.")],
          "Kunststoffe", "matter", calc=f_poly),

        H("C", "naturstoffe-kohlenhydrate-fette-und-proteine", "Naturstoffe: Kohlenhydrate, Fette und Proteine", "Naturstoffe",
          "Die Schülerinnen und Schüler beschreiben Bau und Eigenschaften von Kohlenhydraten, Fetten und Proteinen, erklären Nachweisreaktionen und die Bedeutung von Struktur für die Funktion.",
          "Glucose und Fructose, Fischer- und Haworth-Projektion, Disaccharide, Stärke und Cellulose, Fehling- und Iod-Probe, Fette als Ester, gesättigte und ungesättigte Fettsäuren, Aminosäuren, Peptidbindung, Proteinstruktur, Denaturierung",
          "Struktur bestimmt die Eigenschaften der Naturstoffe", "Proteine sind Ketten aus Aminosäuren, verbunden durch Peptidbindungen.",
          ["Kohlenhydrate: Glucose ist ein Monosaccharid, Saccharose ein Disaccharid. Stärke und Cellulose bestehen beide aus Glucose, aber mit verschiedener Verknüpfung (α bzw. β).",
           "Fette sind Ester aus Glycerin und drei Fettsäuren. Ungesättigte Fettsäuren haben Doppelbindungen, ihre Fette sind meist flüssig (Öle).",
           "Aminosäuren verknüpfen sich unter Wasserabspaltung zu Peptiden. Die Faltung (Sekundär-, Tertiär-, Quartärstruktur) bestimmt die Funktion. Hitze und Säure denaturieren Proteine."],
          [("Zu einer Lösung gibt man Iod-Kaliumiodid-Lösung, sie wird blauschwarz. Was ist enthalten?", ["Die Iod-Probe weist Stärke nach."], "Stärke")],
          [("Stärke und Cellulose sind verschieden aufgebaute Stoffe aus verschiedenen Bausteinen.", "Beide bestehen aus Glucose, nur die Verknüpfung ist anders."), ("Öle haben gesättigte Fettsäuren.", "Öle enthalten viele ungesättigte Fettsäuren."),
           ("Beim Kochen eines Eis ändert sich die Aminosäurefolge.", "Die Primärstruktur bleibt, nur die Faltung wird zerstört.")],
          [("Warum kann der Mensch Cellulose nicht verdauen?", "Ihm fehlt ein Enzym, das die β-glycosidischen Bindungen spaltet."), ("Was zeigt die Fehling-Probe?", "Reduzierende Zucker wie Glucose bilden einen ziegelroten Niederschlag."),
           ("Was ist die Biuret-Reaktion?", "Ein Nachweis für Peptidbindungen: Die Lösung färbt sich violett.")],
          [("Nachweise", [("Iod-Kaliumiodid-Lösung wird blauschwarz", "Stärke"), ("Fehling-Probe ergibt ziegelroten Niederschlag", "reduzierender Zucker"), ("Biuret-Reaktion färbt violett", "Proteine (Peptidbindungen)"),
                          ("Fettfleck auf Papier", "Fett"), ("Ninhydrin färbt violett", "Aminosäuren"), ("Bromwasser wird entfärbt", "ungesättigte Fettsäuren"), ("Glucoseteststreifen färbt sich", "Glucose")],
            "Was ist nachgewiesen? {k}", "Wie weist man {v} nach?"),
           ("Naturstoffe einordnen", {"den Kohlenhydraten": ["Glucose", "Fructose", "Saccharose", "Stärke", "Cellulose", "Glykogen", "Lactose"], "den Fetten und Fettsäuren": ["Ölsäure", "Stearinsäure", "Olivenöl", "Butterfett", "Glycerintristearat"],
                                     "den Proteinen und Aminosäuren": ["Glycin", "Alanin", "Keratin", "Hämoglobin", "Kollagen", "Insulin"]}),
           ("Strukturen", [("Primärstruktur", "Reihenfolge der Aminosäuren"), ("Sekundärstruktur", "α-Helix und β-Faltblatt durch Wasserstoffbrücken"), ("Tertiärstruktur", "räumliche Faltung der ganzen Kette"),
                           ("Quartärstruktur", "Zusammenlagerung mehrerer Ketten"), ("Peptidbindung", "–CO–NH– zwischen zwei Aminosäuren"), ("glycosidische Bindung", "verknüpft Zuckerbausteine"), ("Esterbindung im Fett", "verknüpft Glycerin und Fettsäure")],
            "Was beschreibt „{k}“?", "Welcher Begriff passt: {v}?")],
          ["Stärke und Cellulose bestehen aus Glucose.", "Fette sind Ester aus Glycerin und Fettsäuren.", "Öle enthalten viele ungesättigte Fettsäuren.", "Proteine bestehen aus Aminosäuren.",
           "Die Iod-Probe weist Stärke nach.", "Hitze denaturiert Proteine.", "Bei der Peptidbindung wird Wasser abgespalten.", "Die Biuret-Reaktion weist Proteine nach."],
          [("Cellulose besteht aus Fructose.", "Sie besteht aus Glucose."), ("Öle enthalten nur gesättigte Fettsäuren.", "Sie enthalten viele ungesättigte."), ("Beim Kochen ändert sich die Aminosäurefolge.", "Nur die Faltung ändert sich."),
           ("Die Fehling-Probe weist Stärke nach.", "Sie weist reduzierende Zucker nach."), ("Fette sind Proteine.", "Fette sind Ester."), ("Die Primärstruktur ist die räumliche Faltung.", "Sie ist die Aminosäurefolge.")],
          "Naturstoffe", "matter"),

        H("P", "quantenobjekte-und-photoeffekt", "Quantenobjekte und Photoeffekt", "Photoeffekt",
          "Die Schülerinnen und Schüler erklären den Photoeffekt mit dem Photonenmodell, berechnen Photonenenergien, beschreiben den Wellencharakter von Elektronen und deuten Doppelspaltversuche mit Quantenobjekten.",
          "Photoeffekt, Austrittsarbeit, Grenzfrequenz, Einstein-Gleichung, Photon, plancksches Wirkungsquantum, Elektronenvolt, De-Broglie-Wellenlänge, Elektronenbeugung, Doppelspalt mit Einzelquanten, Unschärferelation",
          "Licht gibt Energie in Portionen ab: E = h · f", "Nur die Frequenz, nicht die Helligkeit, entscheidet, ob Elektronen austreten.",
          ["Beim Photoeffekt löst Licht Elektronen aus einem Metall. Ein Photon gibt seine ganze Energie E = h · f an ein Elektron ab. Es gilt E<sub>kin</sub> = h · f − W<sub>A</sub>.",
           "Unterhalb der Grenzfrequenz treten keine Elektronen aus, egal wie hell das Licht ist. Mehr Helligkeit bedeutet mehr Photonen und mehr Elektronen, aber keine höhere Energie pro Elektron.",
           "Auch Elektronen zeigen Wellenverhalten: λ = h : p (De Broglie). Am Doppelspalt entsteht aus vielen einzelnen Quanten ein Interferenzmuster."],
          [("Grünes Licht (2,3 eV) löst bei Kalium (W = 2,3 eV) gerade noch Elektronen aus. Was passiert mit rotem Licht?", ["Rotes Licht hat weniger Energie pro Photon.", "h · f < W"], "Es treten keine Elektronen aus.")],
          [("Helleres Licht gibt den Elektronen mehr Energie.", "Mehr Helligkeit gibt mehr Elektronen, die Energie hängt von der Frequenz ab."), ("Licht ist entweder Welle oder Teilchen.", "Je nach Versuch zeigt es Wellen- oder Teilcheneigenschaften."),
           ("Rotes Licht hat mehr Energie pro Photon als blaues.", "Blaues Licht hat die höhere Frequenz und mehr Energie.")],
          [("Was ist ein Elektronenvolt?", "Die Energie, die ein Elektron beim Durchlaufen von 1 V gewinnt: 1 eV = 1,6 · 10⁻¹⁹ J."), ("Was sagt die Unschärferelation?", "Ort und Impuls eines Quantenobjekts lassen sich nicht gleichzeitig beliebig genau bestimmen."),
           ("Wo nutzt man den Photoeffekt?", "In Solarzellen, Fotodioden und Bildsensoren von Kameras.")],
          [("Begriffe", [("Photon", "Energieportion des Lichts"), ("Austrittsarbeit", "Energie, die ein Elektron braucht, um das Metall zu verlassen"), ("Grenzfrequenz", "kleinste Frequenz, bei der Elektronen austreten"),
                         ("plancksches Wirkungsquantum", "h ≈ 6,63 · 10⁻³⁴ Js"), ("Elektronenvolt", "1 eV ≈ 1,6 · 10⁻¹⁹ J"), ("De-Broglie-Wellenlänge", "λ = h : p"), ("Welle-Teilchen-Dualismus", "Quantenobjekte zeigen beide Eigenschaften"),
                         ("Unschärferelation", "Ort und Impuls nicht zugleich beliebig genau")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Was ändert sich?", [("höhere Lichtfrequenz", "höhere kinetische Energie der Elektronen"), ("helleres Licht oberhalb der Grenzfrequenz", "mehr ausgelöste Elektronen"), ("Licht unterhalb der Grenzfrequenz", "keine Elektronen"),
                                 ("Metall mit größerer Austrittsarbeit", "höhere Grenzfrequenz"), ("schnellere Elektronen", "kleinere De-Broglie-Wellenlänge"), ("UV-Licht statt rotem Licht", "mehr Energie pro Photon"),
                                 ("einzelne Elektronen am Doppelspalt", "nach und nach entsteht ein Interferenzmuster")],
            "Was folgt? {k}", "Was führt zu {v}?"),
           ("Experimente", [("Hallwachs-Versuch", "negativ geladene Zinkplatte entlädt sich mit UV-Licht"), ("Gegenfeldmethode", "Messung der kinetischen Energie der Photoelektronen"), ("Elektronenbeugungsröhre", "Ringe zeigen Wellencharakter von Elektronen"),
                            ("Doppelspalt mit Einzelphotonen", "Interferenz entsteht aus vielen Einzelereignissen"), ("Compton-Effekt", "Photonen stoßen wie Teilchen mit Elektronen"), ("Franck-Hertz-Versuch", "Atome nehmen Energie nur in Portionen auf")],
            "Was zeigt der {k}?".replace("der {k}", "„{k}“"), "Welches Experiment zeigt: {v}?")],
          ["Ein Photon hat die Energie E = h · f.", "Unterhalb der Grenzfrequenz treten keine Elektronen aus.", "Helleres Licht löst mehr Elektronen aus.", "Blaues Licht hat mehr Energie pro Photon als rotes.",
           "Elektronen zeigen Beugung.", "Die De-Broglie-Wellenlänge ist λ = h : p.", "1 eV entspricht etwa 1,6 · 10⁻¹⁹ J.", "Solarzellen nutzen den Photoeffekt."],
          [("Helleres Licht gibt jedem Elektron mehr Energie.", "Es löst mehr Elektronen aus."), ("Rotes Licht hat mehr Energie pro Photon als blaues.", "Blaues hat mehr."), ("Unterhalb der Grenzfrequenz hilft sehr helles Licht.", "Es treten trotzdem keine Elektronen aus."),
           ("Elektronen zeigen nie Welleneigenschaften.", "Sie werden gebeugt."), ("Schnellere Elektronen haben eine größere Wellenlänge.", "Sie haben eine kleinere."), ("Die Austrittsarbeit ist für alle Metalle gleich.", "Sie hängt vom Metall ab.")],
          "Quantenobjekte", "energy", calc=f_photo),

        H("P", "atomhuelle-und-spektren", "Atomhülle und Spektren", "Atomspektren",
          "Die Schülerinnen und Schüler beschreiben Energieniveaus im Atom, erklären Linienspektren durch Übergänge, berechnen Photonenenergien beim Wasserstoff und beschreiben Franck-Hertz-Versuch und Fluoreszenz.",
          "Energieniveaus, Grundzustand und angeregter Zustand, Ionisierungsenergie, Emissions- und Absorptionsspektrum, Balmer-Serie, Eₙ = −13,6 eV : n², Franck-Hertz-Versuch, Fluoreszenz, Laser, Spektralanalyse",
          "Atome senden Licht nur bei bestimmten Energien aus", "Ein Linienspektrum entsteht durch Sprünge zwischen festen Energieniveaus.",
          ["Elektronen im Atom besitzen nur bestimmte Energien (Niveaus). Springt ein Elektron von einem höheren auf ein tieferes Niveau, wird ein Photon mit ΔE = h · f ausgesandt.",
           "Beim Wasserstoff gilt Eₙ = −13,6 eV : n². Übergänge auf n = 2 liefern die sichtbare Balmer-Serie (zum Beispiel rot bei 656 nm). Die Ionisierungsenergie aus dem Grundzustand ist 13,6 eV.",
           "Ein Gas absorbiert genau die Wellenlängen, die es auch aussendet: dunkle Linien im Absorptionsspektrum. So erkennt man Elemente in Sternen."],
          [("Welche Energie hat das Photon beim Übergang von n = 3 auf n = 2 im Wasserstoff?", ["E₃ = −1,51 eV, E₂ = −3,4 eV", "ΔE = 3,4 − 1,51"], "etwa 1,89 eV (rotes Licht, 656 nm)")],
          [("Atome senden beliebige Energien aus.", "Nur Energien, die den Abständen der Niveaus entsprechen."), ("Im Absorptionsspektrum fehlen andere Linien als im Emissionsspektrum.", "Die dunklen Linien liegen genau dort, wo das Gas auch emittiert."),
           ("Das Elektron hat im Grundzustand die meiste Energie.", "Der Grundzustand ist der Zustand mit der niedrigsten Energie.")],
          [("Was zeigt der Franck-Hertz-Versuch?", "Quecksilberatome nehmen von Elektronen Energie nur in Portionen von 4,9 eV auf, es gibt also diskrete Niveaus."),
           ("Wie funktioniert ein Laser?", "Durch stimulierte Emission entstehen viele Photonen gleicher Wellenlänge und Phase."), ("Wie erkennt man Elemente in der Sonne?", "Durch die dunklen Fraunhofer-Linien im Sonnenspektrum.")],
          [("Begriffe", [("Grundzustand", "Zustand niedrigster Energie"), ("angeregter Zustand", "Elektron auf höherem Niveau"), ("Ionisierungsenergie", "Energie, um ein Elektron ganz zu entfernen"), ("Emissionsspektrum", "helle Linien auf dunklem Grund"),
                         ("Absorptionsspektrum", "dunkle Linien im kontinuierlichen Spektrum"), ("Balmer-Serie", "Übergänge auf n = 2, sichtbares Licht"), ("Lyman-Serie", "Übergänge auf n = 1, Ultraviolett"), ("Fluoreszenz", "UV-Licht wird absorbiert, sichtbares Licht ausgesandt")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Spektren", [("glühender Festkörper", "kontinuierliches Spektrum"), ("leuchtendes Natriumgas", "Linienspektrum mit gelber Doppellinie"), ("Sonnenlicht durch ein Prisma", "kontinuierliches Spektrum mit dunklen Fraunhofer-Linien"),
                         ("Wasserstoff-Gasentladungsröhre", "Linienspektrum mit roter, türkiser und violetter Linie"), ("weißes Licht durch kaltes Natriumgas", "Absorptionsspektrum mit dunkler gelber Linie"), ("Laser", "einzelne scharfe Linie"),
                         ("Glühlampe", "kontinuierliches Spektrum")],
            "Welches Spektrum zeigt {k}?", None),
           ("Wasserstoff-Niveaus", [("Niveau n = 1", "−13,6 eV"), ("Niveau n = 2", "−3,4 eV"), ("Niveau n = 3", "−1,51 eV"), ("Niveau n = 4", "−0,85 eV"), ("Niveau n = 5", "−0,544 eV"), ("Niveau n = ∞", "0 eV"),
                                    ("Übergang 3 → 2", "1,89 eV, rotes Licht"), ("Übergang 2 → 1", "10,2 eV, Ultraviolett")],
            "Welche Energie gehört zu {k}?", "Was gehört zu {v}?")],
          ["Elektronen haben im Atom nur bestimmte Energien.", "Beim Sprung nach unten wird ein Photon ausgesandt.", "Die Balmer-Serie liegt im sichtbaren Bereich.", "Im Grundzustand ist die Energie am niedrigsten.",
           "Gase absorbieren dieselben Linien, die sie aussenden.", "Glühende Festkörper liefern ein kontinuierliches Spektrum.", "Die Ionisierungsenergie des Wasserstoffs beträgt 13,6 eV.", "Der Franck-Hertz-Versuch zeigt diskrete Energieniveaus."],
          [("Atome senden beliebige Energien aus.", "Nur bestimmte Energien."), ("Im Grundzustand ist die Energie am höchsten.", "Sie ist am niedrigsten."), ("Die Lyman-Serie ist sichtbar.", "Sie liegt im Ultraviolett."),
           ("Glühende Festkörper liefern Linienspektren.", "Sie liefern ein kontinuierliches Spektrum."), ("Beim Sprung nach oben wird ein Photon ausgesandt.", "Dabei wird eins absorbiert."),
           ("Absorptionslinien liegen an anderen Stellen als Emissionslinien.", "Sie liegen an denselben Stellen.")],
          "Atomspektren", "energy", calc=f_bohr),

        H("P", "atomkern-und-radioaktivitaet", "Atomkern, Radioaktivität und Kernreaktionen", "Kernphysik",
          "Die Schülerinnen und Schüler beschreiben Aufbau und Stabilität von Atomkernen, Zerfallsarten und das Zerfallsgesetz, berechnen Halbwertszeiten und erklären Kernspaltung, Kernfusion und Strahlenschutz.",
          "Nukleonen, Isotope, Nuklidkarte, Alpha-, Beta- und Gammastrahlung, Zerfallsgesetz, Halbwertszeit, Aktivität in Becquerel, C-14-Methode, Massendefekt, Bindungsenergie, Kernspaltung, Kernfusion, Strahlenschutz",
          "Nach jeder Halbwertszeit ist die Hälfte der Kerne zerfallen", "Spaltung schwerer und Fusion leichter Kerne setzen Energie frei (Massendefekt).",
          ["Atomkerne bestehen aus Protonen und Neutronen. Instabile Kerne zerfallen: Alpha (Heliumkern, Massenzahl −4), Beta-minus (Neutron → Proton + Elektron), Gamma (Energieabgabe).",
           "Der Zerfall ist zufällig, für viele Kerne gilt N(t) = N₀ · (½)<sup>t/T</sup>. Die Aktivität (Zerfälle pro Sekunde) wird in Becquerel gemessen.",
           "Die Masse eines Kerns ist kleiner als die Summe seiner Nukleonen (Massendefekt). Nach E = m · c² wird bei Spaltung von Uran und Fusion von Wasserstoff Energie frei."],
          [("Ein Knochen enthält noch 1/4 des C-14 lebender Organismen (T = 5730 a). Wie alt ist er?", ["1/4 = (½)², also 2 Halbwertszeiten.", "2 · 5730 a"], "etwa 11 460 Jahre")],
          [("Nach zwei Halbwertszeiten ist alles zerfallen.", "Nach zwei Halbwertszeiten ist noch ein Viertel übrig."), ("Gammastrahlung ändert die Massenzahl.", "Gammastrahlung ändert weder Massen- noch Ordnungszahl."),
           ("Bestrahlte Lebensmittel werden radioaktiv.", "Bestrahlung mit Gammastrahlen macht Stoffe nicht radioaktiv.")],
          [("Wie schützt man sich vor Strahlung?", "Abstand halten, Aufenthaltszeit kurz halten, abschirmen und radioaktive Stoffe nicht aufnehmen."),
           ("Warum fusioniert die Sonne Wasserstoff?", "Bei der Fusion leichter Kerne zu Helium wird Bindungsenergie frei, die als Strahlung abgegeben wird."), ("Was ist eine Kettenreaktion?", "Bei der Uranspaltung entstehen Neutronen, die weitere Kerne spalten.")],
          [("Zerfallsarten", [("Alphazerfall", "Massenzahl −4, Ordnungszahl −2"), ("Beta-minus-Zerfall", "Massenzahl gleich, Ordnungszahl +1"), ("Beta-plus-Zerfall", "Massenzahl gleich, Ordnungszahl −1"),
                              ("Gammastrahlung", "Massen- und Ordnungszahl unverändert"), ("Alphastrahlung", "wird schon von Papier gestoppt"), ("Betastrahlung", "wird von wenigen Millimetern Aluminium gestoppt"),
                              ("Gammastrahlung abschirmen", "dicke Bleischicht oder Beton")],
            "Was gilt für {k}?", "Was ist gemeint? {v}"),
           ("Kernreaktionen und Anwendungen", [("Kernspaltung", "schwerer Kern zerfällt in zwei mittelschwere Kerne"), ("Kernfusion", "leichte Kerne verschmelzen"), ("C-14-Methode", "Altersbestimmung organischer Funde"),
                                              ("Szintigrafie mit Technetium-99m", "Untersuchung von Organen"), ("Strahlentherapie", "Zerstörung von Tumorzellen"), ("Geiger-Müller-Zählrohr", "Messung ionisierender Strahlung"),
                                              ("Massendefekt", "Kern ist leichter als seine Bausteine"), ("Moderator im Reaktor", "bremst Neutronen ab")],
            "Was bedeutet {k}?", "Was ist gemeint? {v}"),
           ("Halbwertszeiten", [("Iod-131", "8 Tage"), ("Radon-222", "3,8 Tage"), ("Technetium-99m", "6 Stunden"), ("Cobalt-60", "5,3 Jahre"), ("Caesium-137", "30 Jahre"), ("Kohlenstoff-14", "5730 Jahre"),
                                ("Uran-238", "4,5 Milliarden Jahre"), ("Phosphor-32", "14 Tage")],
            "Welche Halbwertszeit hat {k}?", "Welches Nuklid hat die Halbwertszeit {v}?")],
          ["Nach einer Halbwertszeit ist die Hälfte der Kerne zerfallen.", "Beim Alphazerfall sinkt die Massenzahl um 4.", "Gammastrahlung ändert die Massenzahl nicht.", "Alphastrahlung wird von Papier gestoppt.",
           "Die Aktivität wird in Becquerel gemessen.", "Kerne sind leichter als ihre Bausteine.", "In der Sonne läuft Kernfusion ab.", "Bestrahlte Lebensmittel werden nicht radioaktiv."],
          [("Nach zwei Halbwertszeiten ist alles zerfallen.", "Ein Viertel ist noch übrig."), ("Gammastrahlung senkt die Massenzahl.", "Sie ändert sie nicht."), ("Alphastrahlung durchdringt Blei.", "Sie wird schon von Papier gestoppt."),
           ("In der Sonne läuft Kernspaltung ab.", "Es läuft Kernfusion ab."), ("Beim Beta-minus-Zerfall sinkt die Ordnungszahl.", "Sie steigt um 1."), ("Bestrahlte Lebensmittel werden radioaktiv.", "Sie werden nicht radioaktiv.")],
          "die Kernphysik", "energy", calc=f_hwz),

        H("P", "elektromagnetische-schwingungen-und-wellen", "Elektromagnetische Schwingungen und Wellen", "EM-Wellen",
          "Die Schülerinnen und Schüler beschreiben den elektromagnetischen Schwingkreis, berechnen Eigenfrequenzen mit der Thomson-Gleichung, erklären die Entstehung elektromagnetischer Wellen am Dipol und ordnen das Spektrum.",
          "Schwingkreis aus Spule und Kondensator, Energieumwandlung zwischen elektrischem und magnetischem Feld, Thomson-Gleichung, Dämpfung, Rückkopplung, Hertzscher Dipol, Ausbreitung mit Lichtgeschwindigkeit, elektromagnetisches Spektrum",
          "Energie pendelt zwischen Kondensator und Spule", "Elektromagnetische Wellen breiten sich mit c = 3 · 10⁸ m/s aus.",
          ["Ein geladener Kondensator entlädt sich über eine Spule. Die Energie wechselt zwischen elektrischem Feld (Kondensator) und magnetischem Feld (Spule). Es entsteht eine Schwingung.",
           "Die Eigenfrequenz ist f = 1 : (2π · √(L · C)) (Thomson). Durch den Widerstand ist die Schwingung gedämpft, eine Rückkopplung kann sie entdämpfen.",
           "Ein offener Schwingkreis (Hertzscher Dipol) strahlt elektromagnetische Wellen ab. Sie brauchen kein Medium und breiten sich im Vakuum mit Lichtgeschwindigkeit aus: c = λ · f."],
          [("Ein UKW-Sender sendet mit 100 MHz. Wie lang ist die Welle?", ["λ = c : f", "3 · 10⁸ : 10⁸"], "3 m")],
          [("Elektromagnetische Wellen brauchen Luft.", "Sie breiten sich auch im Vakuum aus."), ("Größere Kapazität erhöht die Frequenz.", "Größere Kapazität oder Induktivität senken die Frequenz."),
           ("Radiowellen und Licht sind ganz verschiedene Dinge.", "Beide sind elektromagnetische Wellen, nur mit verschiedener Wellenlänge.")],
          [("Warum ist die Antenne oft λ/2 lang?", "Dann schwingt der Dipol in Resonanz und strahlt am stärksten ab."), ("Was ist Dämpfung?", "Durch den Widerstand wird Energie in Wärme umgewandelt, die Amplitude nimmt ab."),
           ("Wie hängen Frequenz und Energie zusammen?", "Je höher die Frequenz, desto mehr Energie trägt ein Photon, Röntgen- und Gammastrahlung sind energiereich.")],
          [("Elektromagnetisches Spektrum", [("Radiowellen", "Wellenlänge Meter bis Kilometer"), ("Mikrowellen", "Wellenlänge Millimeter bis Zentimeter"), ("Infrarot", "Wärmestrahlung"), ("sichtbares Licht", "etwa 380 bis 780 nm"),
                                             ("Ultraviolett", "verursacht Sonnenbrand"), ("Röntgenstrahlung", "durchdringt Weichgewebe"), ("Gammastrahlung", "entsteht bei Kernumwandlungen")],
            "Was gilt für {k}?", "Welche Strahlung ist das: {v}?"),
           ("Schwingkreis", [("Kondensator voll geladen", "Energie im elektrischen Feld"), ("Strom maximal", "Energie im magnetischen Feld der Spule"), ("Widerstand im Kreis", "Schwingung wird gedämpft"),
                             ("Rückkopplung mit Transistor", "ungedämpfte Schwingung"), ("Kapazität vervierfacht", "Frequenz halbiert sich"), ("Induktivität vervierfacht", "Frequenz halbiert sich"),
                             ("offener Schwingkreis", "Hertzscher Dipol strahlt Wellen ab")],
            "Was gilt? {k}", None),
           ("Anwendungen", [("UKW-Radio", "Radiowellen um 100 MHz"), ("Mikrowellenherd", "2,45 GHz, regt Wassermoleküle an"), ("Fernbedienung", "Infrarot"), ("Röntgenbild", "Röntgenstrahlung"),
                            ("Sterilisation", "UV-C oder Gammastrahlung"), ("Wärmebildkamera", "Infrarot"), ("WLAN", "Mikrowellen um 2,4 und 5 GHz"), ("Radar", "Mikrowellen")],
            "Welche Strahlung nutzt „{k}“?", "Wo wird {v} genutzt?")],
          ["Im Schwingkreis pendelt Energie zwischen Kondensator und Spule.", "Größere Kapazität senkt die Eigenfrequenz.", "Elektromagnetische Wellen brauchen kein Medium.", "Für elektromagnetische Wellen gilt c = λ · f.",
           "Ein Widerstand dämpft die Schwingung.", "Licht ist eine elektromagnetische Welle.", "Röntgenstrahlung ist energiereicher als Infrarot.", "Ein Hertzscher Dipol strahlt Wellen ab."],
          [("Elektromagnetische Wellen brauchen Luft.", "Sie breiten sich auch im Vakuum aus."), ("Größere Kapazität erhöht die Frequenz.", "Sie senkt sie."), ("Radiowellen sind keine elektromagnetischen Wellen.", "Sie sind es."),
           ("Infrarot ist energiereicher als Ultraviolett.", "Ultraviolett ist energiereicher."), ("Ein Widerstand verstärkt die Schwingung.", "Er dämpft sie."), ("Mikrowellen haben Wellenlängen im Kilometerbereich.", "Sie liegen im Millimeter- bis Zentimeterbereich.")],
          "elektromagnetische Wellen", "waves-and-light", calc=f_lc),
    ]
