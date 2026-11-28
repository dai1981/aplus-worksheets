# -*- coding: utf-8 -*-
"""Deutschland / Klasse 11（Oberstufe, Einführungsphase: Biologie, Chemie, Physik）"""
import math
from de_sci import H, nq, num


def f_rate(R):
    k = R.choice(["v", "v", "dc", "t", "rgt"])
    if k == "v":
        c1, c2, t = R.choice([(1.0, 0.6, 20), (0.8, 0.2, 30), (2.0, 1.2, 40), (0.5, 0.3, 10), (1.5, 0.9, 60), (0.9, 0.3, 120), (2.4, 1.6, 16), (1.2, 0.8, 50)])
        v = (c1 - c2) / t
        return nq("Die Konzentration eines Edukts sinkt in %d s von %s mol/l auf %s mol/l. Wie groß ist die mittlere Reaktionsgeschwindigkeit?" % (t, num(c1), num(c2)), v,
                  [(c1 - c2) * t, t / (c1 - c2), c1 / t, c2 / t], "mol/(l·s)", "v = Δc : Δt = (%s − %s) mol/l : %d s = %s mol/(l·s)." % (num(c1), num(c2), t, num(v)))
    if k == "dc":
        v, t = R.choice([(0.02, 10), (0.005, 40), (0.01, 30), (0.04, 5), (0.003, 100), (0.025, 8)])
        return nq("Eine Reaktion läuft mit v = %s mol/(l·s). Um wie viel sinkt die Konzentration des Edukts in %d s?" % (num(v), t), v * t,
                  [v / t, t / v, v * t * 10], "mol/l", "Δc = v · Δt = %s mol/(l·s) · %d s = %s mol/l." % (num(v), t, num(v * t)))
    if k == "t":
        dc, v = R.choice([(0.6, 0.02), (0.4, 0.01), (1.2, 0.04), (0.3, 0.005), (0.9, 0.03), (0.5, 0.025)])
        return nq("Die Konzentration soll um %s mol/l sinken, v = %s mol/(l·s). Wie lange dauert das?" % (num(dc), num(v)), dc / v,
                  [dc * v, v / dc, dc / v / 10], "s", "Δt = Δc : v = %s : %s = %s s." % (num(dc), num(v), num(dc / v)))
    t0, n = R.choice([(80, 1), (80, 2), (120, 2), (60, 3), (240, 3), (40, 1), (160, 4)])
    return nq("Nach der RGT-Regel verdoppelt sich die Geschwindigkeit pro 10 °C. Eine Reaktion braucht %d s. Wie lange braucht sie %d °C wärmer?" % (t0, 10 * n), t0 / 2 ** n,
              [t0 * 2 ** n, t0 / (2 * n) if n > 1 else t0 / 4, t0 - 10 * n], "s", "%d · 10 °C wärmer: %d-mal so schnell, also %d s : %d = %s s." % (n, 2 ** n, t0, 2 ** n, num(t0 / 2 ** n)))


def f_K(R):
    k = R.choice(["K", "K", "c"])
    if k == "K":
        a, b, c, d = R.choice([(0.2, 0.4, 0.8, 0.5), (0.5, 0.5, 1.0, 1.0), (0.1, 0.2, 0.4, 0.3), (0.4, 0.2, 0.6, 0.6), (0.3, 0.3, 0.9, 0.6), (0.25, 0.5, 1.0, 0.5), (0.2, 0.2, 0.4, 0.8), (0.1, 0.1, 0.3, 0.3), (0.6, 0.3, 0.9, 0.4), (0.5, 0.2, 0.2, 0.25), (0.4, 0.4, 0.2, 0.4), (0.8, 0.5, 1.2, 1.0)])
        K = c * d / (a * b)
        return nq("Für A + B ⇌ C + D liegen im Gleichgewicht vor: c(A) = %s, c(B) = %s, c(C) = %s, c(D) = %s (in mol/l). Wie groß ist K<sub>c</sub>?" % (num(a), num(b), num(c), num(d)), K,
                  [a * b / (c * d), c * d, (c + d) / (a + b)], "", "K<sub>c</sub> = c(C) · c(D) : (c(A) · c(B)) = %s · %s : (%s · %s) = %s." % (num(c), num(d), num(a), num(b), num(K)))
    K, a, b, d = R.choice([(4, 0.5, 0.5, 1.0), (2, 0.2, 0.5, 0.4), (8, 0.25, 0.5, 0.5), (10, 0.1, 0.2, 0.4), (3, 0.4, 0.5, 0.3), (6, 0.2, 0.3, 0.6), (5, 0.4, 0.4, 0.8), (12, 0.1, 0.5, 0.3), (2, 0.6, 0.5, 0.2), (9, 0.2, 0.2, 0.6)])
    c = K * a * b / d
    return nq("Für A + B ⇌ C + D ist K<sub>c</sub> = %s. Im Gleichgewicht gilt c(A) = %s, c(B) = %s und c(D) = %s mol/l. Wie groß ist c(C)?" % (num(K), num(a), num(b), num(d)), c,
              [K * d / (a * b), a * b / (K * d), K * a * b * d], "mol/l", "c(C) = K<sub>c</sub> · c(A) · c(B) : c(D) = %s · %s · %s : %s = %s mol/l." % (num(K), num(a), num(b), num(d), num(c)))


def f_kin(R):
    k = R.choice(["s", "s", "v", "fall", "wurf", "brems"])
    if k == "s":
        v0, a, t = R.choice([(0, 2, 5), (5, 2, 4), (10, 1, 6), (0, 3, 4), (4, 0.5, 10), (2, 4, 3), (0, 1.5, 8), (8, 2, 2)])
        s = v0 * t + 0.5 * a * t * t
        return nq("Ein Körper hat v₀ = %s m/s und beschleunigt mit a = %s m/s². Welchen Weg legt er in %s s zurück?" % (num(v0), num(a), num(t)), s,
                  [v0 * t + a * t * t, v0 * t + 0.5 * a * t, a * t * t / 2 if v0 else a * t], "m", "s = v₀ · t + ½ · a · t² = %s m." % num(s))
    if k == "v":
        v0, a, t = R.choice([(3, 2, 5), (0, 4, 6), (10, -2, 3), (6, 1.5, 4), (20, -4, 2), (2, 3, 7)])
        v = v0 + a * t
        return nq("Ein Fahrzeug hat v₀ = %s m/s und a = %s m/s². Wie schnell ist es nach %s s?" % (num(v0), num(a), num(t)), v,
                  [a * t, v0 + a * t * t, v0 * a * t, v0 - a * t if v0 - a * t > 0 else None], "m/s", "v = v₀ + a · t = %s m/s." % num(v))
    if k == "fall":
        h = R.choice([5, 20, 45, 80, 125, 1.25, 0.8, 3.2])
        t = math.sqrt(2 * h / 10)
        return nq("Ein Stein fällt aus %s m Höhe frei herunter. Wie lange fällt er? (g ≈ 10 m/s², ohne Luftwiderstand)" % num(h), t,
                  [h / 10, 2 * h / 10, math.sqrt(h / 10)], "s", "h = ½ · g · t², also t = √(2h : g) = %s s." % num(t))
    if k == "wurf":
        h, v = R.choice([(5, 4), (20, 3), (45, 2), (1.25, 6), (80, 5), (5, 10), (20, 8)])
        t = math.sqrt(2 * h / 10)
        return nq("Ein Ball wird aus %s m Höhe mit %s m/s waagerecht geworfen. Wie weit fliegt er? (g ≈ 10 m/s²)" % (num(h), num(v)), v * t,
                  [v * 2 * h / 10, v * h / 10, v * t / 2], "m", "Fallzeit t = √(2h : g) = %s s; Wurfweite = v₀ · t = %s m." % (num(t), num(v * t)))
    v, a = R.choice([(20, 5), (30, 6), (10, 4), (25, 5), (14, 7), (40, 8)])
    return nq("Ein Auto bremst von %s m/s mit a = −%s m/s² bis zum Stillstand. Wie lang ist der Bremsweg?" % (num(v), num(a)), v * v / (2 * a),
              [v * v / a, v / a, v * v / (4 * a)], "m", "s = v₀² : (2a) = %s² : %s = %s m." % (num(v), num(2 * a), num(v * v / (2 * a))))


def f_impuls(R):
    k = R.choice(["p", "p", "unel", "unel", "kraft", "rueck"])
    if k == "p":
        m, v = R.choice([(0.4, 20), (70, 5), (1200, 15), (0.16, 30), (2, 3), (80, 9), (0.05, 400)])
        return nq("Welchen Impuls hat ein Körper mit %s kg und %s m/s?" % (num(m), num(v)), m * v, [m / v, 0.5 * m * v * v, m + v], "kg·m/s",
                  "p = m · v = %s kg · %s m/s = %s kg·m/s." % (num(m), num(v), num(m * v)))
    if k == "unel":
        m1, v1, m2 = R.choice([(2, 6, 1), (1000, 12, 500), (3, 4, 1), (60, 5, 40), (0.5, 8, 1.5), (4, 10, 6), (1500, 20, 1000)])
        v = m1 * v1 / (m1 + m2)
        return nq("Ein Wagen (%s kg, %s m/s) stößt auf einen ruhenden Wagen (%s kg). Beide fahren gekoppelt weiter. Wie schnell?" % (num(m1), num(v1), num(m2)), v,
                  [v1 / 2, m1 * v1 / m2, v1, m2 * v1 / (m1 + m2)], "m/s", "Impulserhaltung: %s · %s = (%s + %s) · v, also v = %s m/s." % (num(m1), num(v1), num(m1), num(m2), num(v)))
    if k == "kraft":
        m, dv, t = R.choice([(0.4, 20, 0.02), (1000, 15, 0.1), (70, 10, 0.5), (0.06, 50, 0.005), (2, 6, 0.3), (80, 12, 0.2)])
        return nq("Ein Körper (%s kg) ändert seine Geschwindigkeit in %s s um %s m/s. Wie groß ist die mittlere Kraft?" % (num(m), num(t), num(dv)), m * dv / t,
                  [m * dv * t, m * dv, dv / t], "N", "F = Δp : Δt = %s kg · %s m/s : %s s = %s N." % (num(m), num(dv), num(t), num(m * dv / t)))
    M, m, v = R.choice([(60, 2, 3), (300, 10, 6), (80, 4, 5), (200, 5, 8), (50, 1, 4), (120, 3, 6), (90, 6, 3)])
    return nq("Jemand steht still auf einem Rollbrett oder in einem Boot (zusammen %s kg) und wirft einen Gegenstand (%s kg) mit %s m/s nach vorn. Wie schnell bewegt er sich zurück?" % (num(M), num(m), num(v)), m * v / M,
              [M * v / m, m * v, v], "m/s", "Gesamtimpuls bleibt 0: %s · %s = %s · v, also v = %s m/s." % (num(m), num(v), num(M), num(m * v / M)))


def f_kreis(R):
    k = R.choice(["F", "F", "v", "T", "grav"])
    if k == "F":
        m, v, r = R.choice([(1000, 20, 50), (0.5, 4, 1), (70, 10, 20), (2, 6, 3), (1200, 15, 100), (0.2, 3, 0.5), (60, 8, 16)])
        return nq("Ein Körper (%s kg) fährt mit %s m/s auf einem Kreis mit r = %s m. Wie groß ist die Zentripetalkraft?" % (num(m), num(v), num(r)), m * v * v / r,
                  [m * v / r, m * v * v * r, m * v * v / (r * r)], "N", "F = m · v² : r = %s · %s² : %s = %s N." % (num(m), num(v), num(r), num(m * v * v / r)))
    if k == "v":
        r, T = R.choice([(2, 4), (0.5, 1), (10, 20), (3, 6), (50, 25), (1, 0.5), (4, 8)])
        v = 2 * math.pi * r / T
        return nq("Ein Körper umläuft einen Kreis mit r = %s m in T = %s s. Wie groß ist seine Bahngeschwindigkeit?" % (num(r), num(T)), v,
                  [math.pi * r / T, 2 * math.pi * r * T, r / T], "m/s", "v = 2π · r : T = 2π · %s m : %s s ≈ %s m/s." % (num(r), num(T), num(v)))
    if k == "T":
        f = R.choice([2, 5, 0.5, 10, 4, 0.25, 50])
        return nq("Ein Rad dreht sich mit der Frequenz %s Hz. Wie groß ist die Umlaufdauer?" % num(f), 1 / f, [f, 2 * math.pi / f, 2 * f], "s",
                  "T = 1 : f = 1 : %s Hz = %s s." % (num(f), num(1 / f)))
    n = R.choice([2, 3, 4, 5, 10])
    return nq("Ein Satellit ist %d-mal so weit vom Erdmittelpunkt entfernt wie die Erdoberfläche. Wie groß ist dort der Ortsfaktor? (an der Oberfläche 10 N/kg)" % n, 10 / n ** 2,
              [10 / n, 10 * n, 10 / n ** 3], "N/kg", "Die Gravitationskraft nimmt mit 1/r² ab: 10 N/kg : %d² = %s N/kg." % (n, num(10 / n ** 2)))


def f_schw(R):
    k = R.choice(["fad", "fad", "feder", "f", "l"])
    if k == "fad":
        l = R.choice([0.4, 1, 2.5, 0.1, 1.6, 0.9, 3.6, 0.25])
        T = 2 * math.pi * math.sqrt(l / 10)
        return nq("Wie groß ist die Schwingungsdauer eines Fadenpendels mit l = %s m? (g ≈ 10 m/s²)" % num(l), T,
                  [2 * math.pi * l / 10, math.pi * math.sqrt(l / 10), 2 * math.pi * math.sqrt(10 / l)], "s", "T = 2π · √(l : g) = 2π · √(%s : 10) ≈ %s s." % (num(l), num(T)))
    if k == "feder":
        m, D = R.choice([(0.1, 10), (0.4, 40), (0.2, 50), (1, 100), (0.5, 20), (0.25, 25), (2, 50)])
        T = 2 * math.pi * math.sqrt(m / D)
        return nq("Ein Federpendel hat m = %s kg und D = %s N/m. Wie groß ist T?" % (num(m), num(D)), T,
                  [2 * math.pi * math.sqrt(D / m), 2 * math.pi * m / D, math.sqrt(m / D)], "s", "T = 2π · √(m : D) = 2π · √(%s : %s) ≈ %s s." % (num(m), num(D), num(T)))
    if k == "f":
        n, t = R.choice([(20, 10), (50, 25), (12, 30), (30, 6), (100, 20), (8, 16)])
        return nq("Ein Pendel macht %d volle Schwingungen in %d s. Wie groß ist die Frequenz?" % (n, t), n / t, [t / n, n * t, 1 / (n * t) * 100], "Hz",
                  "f = Anzahl : Zeit = %d : %d s = %s Hz." % (n, t, num(n / t)))
    T = R.choice([1, 2, 3, 0.5, 4])
    l = 10 * (T / (2 * math.pi)) ** 2
    return nq("Wie lang muss ein Fadenpendel sein, damit T = %s s ist? (g ≈ 10 m/s²)" % num(T), l, [l * 4, T / (2 * math.pi) * 10, l / 2], "m",
              "l = g · (T : 2π)² = 10 · (%s : 2π)² ≈ %s m." % (num(T), num(l)))


def UNITS(grade):
    return [
        H("B", "zellbiologie-und-biomembranen", "Zellbiologie und Biomembranen", "Biomembranen",
          "Die Schülerinnen und Schüler erklären Bau und Funktion von Zellorganellen und Biomembranen, vergleichen Pro- und Eucyten und beschreiben passive und aktive Transportvorgänge.",
          "Procyte und Eucyte, Endosymbiontentheorie, Flüssig-Mosaik-Modell, Diffusion, Osmose, Plasmolyse, erleichterte Diffusion, aktiver Transport, Endo- und Exocytose",
          "Biomembranen trennen Räume und regeln den Stofftransport", "Wasser folgt bei der Osmose dem Konzentrationsgefälle des Gelösten, aktiver Transport braucht ATP.",
          ["Eucyten haben einen Zellkern und Organellen mit Membranen, Procyten wie Bakterien nicht. Mitochondrien und Chloroplasten stammen nach der Endosymbiontentheorie von Bakterien ab.",
           "Nach dem Flüssig-Mosaik-Modell besteht die Membran aus einer Lipiddoppelschicht mit eingelagerten Proteinen. Kleine unpolare Teilchen diffundieren hindurch, Ionen brauchen Kanäle oder Carrier.",
           "Osmose ist die Diffusion von Wasser durch eine semipermeable Membran zur höheren Konzentration gelöster Teilchen. Aktiver Transport gegen das Gefälle braucht Energie (ATP)."],
          [("Rote Zwiebelzellen liegen in konzentrierter Salzlösung. Was passiert?", ["Außen ist die Konzentration gelöster Teilchen höher.", "Wasser strömt aus der Vakuole hinaus."], "Plasmolyse: Der Protoplast löst sich von der Zellwand.")],
          [("Bei der Osmose wandern die gelösten Teilchen.", "Bei der Osmose wandert das Wasser."), ("Bakterien haben Mitochondrien.", "Procyten haben keine membranumhüllten Organellen."),
           ("Diffusion braucht ATP.", "Diffusion ist passiv, nur aktiver Transport braucht Energie.")],
          [("Was belegt die Endosymbiontentheorie?", "Mitochondrien und Chloroplasten haben eine eigene ringförmige DNA, 70S-Ribosomen und eine doppelte Membran."),
           ("Was ist Deplasmolyse?", "In Wasser nimmt der Protoplast wieder Wasser auf und legt sich an die Zellwand."), ("Wozu dient die Natrium-Kalium-Pumpe?", "Sie transportiert unter ATP-Verbrauch Na⁺ hinaus und K⁺ hinein und hält so das Membranpotenzial aufrecht.")],
          [("Organellen", [("Mitochondrium", "Zellatmung und ATP-Bildung"), ("Chloroplast", "Fotosynthese"), ("raues ER", "Proteinsynthese an Ribosomen"), ("glattes ER", "Lipidsynthese"),
                           ("Golgi-Apparat", "Verpacken und Versenden von Stoffen in Vesikeln"), ("Lysosom", "Abbau von Stoffen mit Enzymen"), ("Zellkern", "Speicherung der DNA"),
                           ("Ribosom", "Übersetzen der mRNA in Proteine"), ("Vakuole", "Speicher und Zellsaft in Pflanzenzellen")],
            "Welche Aufgabe hat: {k}?", "Welches Organell ist zuständig für: {v}?"),
           ("Transportvorgänge", [("Diffusion", "passiv, mit dem Konzentrationsgefälle"), ("Osmose", "Wasser wandert durch eine semipermeable Membran"), ("erleichterte Diffusion", "passiv mit Kanal- oder Carrierprotein"),
                                  ("aktiver Transport", "gegen das Gefälle unter ATP-Verbrauch"), ("Endocytose", "Aufnahme in Vesikeln durch Einstülpen der Membran"), ("Exocytose", "Abgabe durch Verschmelzen von Vesikeln mit der Membran"),
                                  ("Plasmolyse", "Ablösen des Protoplasten von der Zellwand"), ("Phagocytose", "Aufnahme fester Partikel durch Fresszellen")],
            "Was beschreibt {k}?", "Welcher Vorgang ist das: {v}?"),
           ("Procyte oder Eucyte?", {"den Procyten": ["kein Zellkern", "ringförmige DNA im Cytoplasma", "70S-Ribosomen", "Escherichia coli", "Plasmide", "Cyanobakterien"],
                                     "den Eucyten": ["Zellkern mit Kernhülle", "Mitochondrien", "endoplasmatisches Retikulum", "80S-Ribosomen", "Hefezelle", "Leberzelle"]})],
          ["Biomembranen bestehen aus einer Lipiddoppelschicht mit Proteinen.", "Bei der Osmose wandert Wasser.", "Aktiver Transport braucht ATP.", "Procyten haben keinen Zellkern.",
           "Mitochondrien haben eine eigene DNA.", "Diffusion ist ein passiver Vorgang.", "In konzentrierter Salzlösung tritt Plasmolyse ein.", "Der Golgi-Apparat verpackt Stoffe in Vesikel."],
          [("Bei der Osmose wandern die gelösten Teilchen durch die Membran.", "Es wandert das Wasser."), ("Bakterien haben Mitochondrien.", "Sie haben keine membranumhüllten Organellen."),
           ("Diffusion braucht ATP.", "Diffusion ist passiv."), ("Die Membran besteht aus Cellulose.", "Sie besteht aus Lipiden und Proteinen."),
           ("In destilliertem Wasser tritt Plasmolyse ein.", "Plasmolyse tritt in konzentrierter Lösung ein."), ("Lysosomen betreiben Fotosynthese.", "Fotosynthese läuft in Chloroplasten.")],
          "Biomembranen", "living-things-and-ecosystems"),

        H("B", "enzyme-und-enzymkinetik", "Enzyme und Enzymkinetik", "Enzymkinetik",
          "Die Schülerinnen und Schüler erklären Bau und Wirkungsweise von Enzymen, Substrat- und Wirkungsspezifität, die Abhängigkeit der Enzymaktivität von Temperatur, pH und Substratkonzentration sowie Hemmung und Regulation.",
          "aktives Zentrum, Enzym-Substrat-Komplex, Aktivierungsenergie, Substrat- und Wirkungsspezifität, Sättigungskurve, kompetitive und allosterische Hemmung, Denaturierung, Cofaktoren",
          "Enzyme senken die Aktivierungsenergie", "Bei hoher Substratkonzentration sind alle aktiven Zentren besetzt: Die Geschwindigkeit erreicht ihr Maximum.",
          ["Enzyme sind Proteine, die als Biokatalysatoren die Aktivierungsenergie senken. Das Substrat bindet am aktiven Zentrum, es entsteht der Enzym-Substrat-Komplex.",
           "Mit steigender Substratkonzentration steigt die Geschwindigkeit, bis alle Enzyme ausgelastet sind (Sättigung, v<sub>max</sub>). Temperatur und pH haben ein Optimum, Hitze denaturiert.",
           "Ein kompetitiver Hemmstoff konkurriert um das aktive Zentrum, eine hohe Substratkonzentration hebt die Hemmung auf. Ein allosterischer Hemmstoff bindet an anderer Stelle und verändert die Form."],
          [("Ein Hemmstoff ähnelt dem Substrat. Bei sehr viel Substrat wird v<sub>max</sub> trotzdem erreicht. Welche Hemmung ist das?", ["Er besetzt das aktive Zentrum.", "Viel Substrat verdrängt ihn."], "kompetitive Hemmung")],
          [("Enzyme verschieben das Gleichgewicht.", "Enzyme beschleunigen nur die Einstellung des Gleichgewichts."), ("Kälte denaturiert Enzyme.", "Kälte verlangsamt sie, Hitze denaturiert."),
           ("Allosterische Hemmstoffe binden im aktiven Zentrum.", "Sie binden an einer anderen Stelle, dem allosterischen Zentrum.")],
          [("Was ist die Michaelis-Konstante?", "Die Substratkonzentration, bei der die Hälfte von v<sub>max</sub> erreicht wird. Ein kleiner Wert bedeutet hohe Affinität."),
           ("Was ist Endprodukthemmung?", "Das Endprodukt eines Stoffwechselwegs hemmt allosterisch ein Enzym am Anfang des Wegs."), ("Was sind Cofaktoren?", "Nicht-Eiweiß-Bestandteile wie Metallionen oder Coenzyme, die manche Enzyme brauchen.")],
          [("Begriffe", [("aktives Zentrum", "Bindestelle für das Substrat"), ("Substratspezifität", "ein Enzym setzt nur ein bestimmtes Substrat um"), ("Wirkungsspezifität", "ein Enzym katalysiert nur eine bestimmte Reaktion"),
                         ("Denaturierung", "irreversible Zerstörung der Raumstruktur"), ("v<sub>max</sub>", "maximale Geschwindigkeit bei Sättigung"), ("K<sub>M</sub>", "Substratkonzentration bei halber Maximalgeschwindigkeit"),
                         ("Coenzym", "organischer Hilfsstoff, der Gruppen überträgt"), ("Aktivierungsenergie", "Energie, die zum Start der Reaktion nötig ist")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Hemmungen", [("Hemmstoff ähnelt dem Substrat", "kompetitive Hemmung"), ("viel Substrat hebt die Hemmung auf", "kompetitive Hemmung"), ("Hemmstoff bindet am allosterischen Zentrum", "allosterische Hemmung"),
                          ("v<sub>max</sub> sinkt trotz viel Substrat", "allosterische Hemmung"), ("Schwermetallionen zerstören die Raumstruktur", "irreversible Hemmung"), ("Endprodukt hemmt das erste Enzym", "allosterische Hemmung"),
                          ("Hemmstoff bindet fest und dauerhaft", "irreversible Hemmung"), ("Hemmstoff konkurriert um das aktive Zentrum", "kompetitive Hemmung")],
            "Welche Hemmung liegt vor? {k}", None, ("Aktivierung",)),
           ("Einflüsse", [("Temperatur von 20 °C auf 30 °C erhöht", "Aktivität steigt"), ("Temperatur weit über das Optimum", "Enzym denaturiert"), ("Substratkonzentration im Sättigungsbereich verdoppelt", "Geschwindigkeit bleibt fast gleich"),
                          ("Enzymmenge verdoppelt", "v<sub>max</sub> verdoppelt sich"), ("pH weit vom Optimum", "Aktivität sinkt stark"), ("Substratkonzentration niedrig und wird erhöht", "Geschwindigkeit steigt deutlich")],
            "Was passiert? {k}", None)],
          ["Enzyme senken die Aktivierungsenergie.", "Enzyme werden nicht verbraucht.", "Hitze denaturiert Enzyme.", "Bei Sättigung ist v<sub>max</sub> erreicht.",
           "Kompetitive Hemmung lässt sich durch viel Substrat aufheben.", "Allosterische Hemmstoffe verändern die Form des Enzyms.", "Ein kleiner K<sub>M</sub>-Wert zeigt hohe Affinität.", "Enzyme sind substratspezifisch."],
          [("Enzyme erhöhen die Aktivierungsenergie.", "Sie senken sie."), ("Enzyme verschieben das Gleichgewicht.", "Sie beschleunigen nur seine Einstellung."), ("Kälte denaturiert Enzyme.", "Hitze denaturiert sie."),
           ("Kompetitive Hemmung senkt v<sub>max</sub>.", "v<sub>max</sub> wird bei viel Substrat erreicht."), ("Enzyme werden bei der Reaktion verbraucht.", "Sie bleiben erhalten."),
           ("Allosterische Hemmstoffe binden im aktiven Zentrum.", "Sie binden an einer anderen Stelle.")],
          "Enzyme", "living-things-and-ecosystems"),

        H("B", "zellatmung-und-energiestoffwechsel", "Zellatmung und Energiestoffwechsel", "Zellatmung",
          "Die Schülerinnen und Schüler beschreiben Glykolyse, Citratzyklus und Atmungskette, ATP als Energieträger, Gärungen und die Energiebilanz im Überblick.",
          "ATP, Glykolyse, oxidative Decarboxylierung, Citratzyklus, Atmungskette, Protonengradient, ATP-Synthase, Reduktionsäquivalente NADH, alkoholische Gärung und Milchsäuregärung",
          "Zellatmung gewinnt aus Glucose bis zu etwa 32 ATP", "Gärungen ohne Sauerstoff liefern nur 2 ATP pro Glucose.",
          ["ATP ist der universelle Energieträger der Zelle. Bei der Zellatmung wird Glucose schrittweise zu CO₂ und H₂O abgebaut.",
           "Die Glykolyse im Cytoplasma spaltet Glucose in 2 Pyruvat (2 ATP netto). Im Mitochondrium folgen oxidative Decarboxylierung und Citratzyklus, dabei entstehen CO₂ und NADH.",
           "In der Atmungskette geben NADH und FADH₂ Elektronen ab. Ein Protonengradient treibt die ATP-Synthase an, Sauerstoff ist der letzte Elektronenakzeptor und wird zu Wasser."],
          [("Ein Sprinter hat zu wenig Sauerstoff in den Muskeln. Wie gewinnen die Muskeln trotzdem ATP?", ["Ohne O₂ stoppt die Atmungskette.", "Pyruvat wird zu Lactat reduziert, NAD⁺ wird frei."], "durch Milchsäuregärung")],
          [("Die Glykolyse läuft im Mitochondrium.", "Die Glykolyse läuft im Cytoplasma."), ("Der Sauerstoff wird im Citratzyklus verbraucht.", "Sauerstoff wird erst am Ende der Atmungskette verbraucht."),
           ("Das CO₂ der Ausatemluft stammt aus dem Sauerstoff.", "Das CO₂ entsteht bei der Decarboxylierung und im Citratzyklus.")],
          [("Warum braucht Gärung die zweite Reaktion?", "Damit NADH wieder zu NAD⁺ oxidiert wird und die Glykolyse weiterlaufen kann."), ("Was ist die Chemiosmose?", "Die ATP-Bildung durch einen Protonengradienten über die innere Mitochondrienmembran."),
           ("Wozu nutzt man die alkoholische Gärung?", "Beim Brotbacken (CO₂ lockert den Teig) und zur Herstellung von Wein und Bier.")],
          [("Schritte und Orte", [("Glykolyse", "Cytoplasma"), ("oxidative Decarboxylierung", "Mitochondrienmatrix"), ("Citratzyklus", "Mitochondrienmatrix"), ("Atmungskette", "innere Mitochondrienmembran"),
                                  ("ATP-Synthase", "innere Mitochondrienmembran"), ("Milchsäuregärung", "Cytoplasma"), ("alkoholische Gärung", "Cytoplasma")],
            "Wo läuft das ab: {k}?", None, ("Zellkern", "Ribosom")),
           ("Bilanzen", [("Glykolyse", "2 ATP netto und 2 NADH"), ("Citratzyklus je Glucose", "2 ATP, 6 NADH, 2 FADH₂ und 4 CO₂"), ("vollständige Zellatmung", "bis zu etwa 32 ATP je Glucose"),
                         ("Milchsäuregärung", "2 ATP je Glucose und Lactat"), ("alkoholische Gärung", "2 ATP je Glucose, Ethanol und CO₂"), ("Atmungskette", "der größte Teil des ATP, Sauerstoff wird zu Wasser")],
            "Was liefert {k}?", "Welcher Abschnitt liefert: {v}?"),
           ("Begriffe", [("ATP", "universeller Energieträger der Zelle"), ("NADH", "überträgt Elektronen und Wasserstoff"), ("Pyruvat", "Endprodukt der Glykolyse"), ("Acetyl-CoA", "Eingangsstoff des Citratzyklus"),
                         ("Protonengradient", "treibt die ATP-Synthase an"), ("Sauerstoff", "letzter Elektronenakzeptor der Atmungskette"), ("Lactat", "Endprodukt der Milchsäuregärung")],
            "Was beschreibt „{k}“?", "Was ist gemeint? {v}")],
          ["Die Glykolyse läuft im Cytoplasma.", "Der Citratzyklus läuft in der Mitochondrienmatrix.", "Sauerstoff ist der letzte Elektronenakzeptor.", "Gärungen liefern 2 ATP je Glucose.",
           "Ein Protonengradient treibt die ATP-Synthase an.", "Das ausgeatmete CO₂ stammt aus dem Citratzyklus und der Decarboxylierung.", "Bei der Milchsäuregärung entsteht Lactat.", "Hefe bildet bei der Gärung Ethanol und CO₂."],
          [("Die Glykolyse läuft im Mitochondrium.", "Sie läuft im Cytoplasma."), ("Gärungen liefern mehr ATP als die Zellatmung.", "Sie liefern viel weniger."), ("Sauerstoff wird im Citratzyklus verbraucht.", "Er wird in der Atmungskette verbraucht."),
           ("Bei der Milchsäuregärung entsteht CO₂.", "Es entsteht nur Lactat."), ("ATP-Synthase sitzt in der äußeren Membran.", "Sie sitzt in der inneren Mitochondrienmembran."), ("Die Atmungskette liefert kaum ATP.", "Sie liefert den größten Teil.")],
          "die Zellatmung", "living-things-and-ecosystems"),

        H("B", "oekologie-populationen-und-umweltfaktoren", "Ökologie: Populationen und Umweltfaktoren", "Populationsökologie",
          "Die Schülerinnen und Schüler beschreiben Toleranzkurven, ökologische Potenz, Populationswachstum, Regulation durch dichteabhängige Faktoren, Räuber-Beute-Beziehungen und Konkurrenz.",
          "Toleranzkurve, Optimum und Pessimum, stenök und euryök, Zeigerarten, exponentielles und logistisches Wachstum, Kapazität, r- und K-Strategen, Lotka-Volterra-Regeln, Konkurrenzausschluss",
          "Populationen wachsen bis zur Kapazitätsgrenze", "Dichteabhängige Faktoren wie Nahrung und Krankheiten regulieren die Populationsgröße.",
          ["Jede Art hat für einen Umweltfaktor einen Toleranzbereich mit Optimum. Stenöke Arten haben einen engen, euryöke einen weiten Bereich.",
           "Bei unbegrenzten Ressourcen wächst eine Population exponentiell. Real flacht das Wachstum ab, bis die Kapazität K erreicht ist (logistisches Wachstum).",
           "Räuber- und Beutepopulationen schwanken periodisch und phasenverschoben. Zwei Arten mit gleicher Nische können nicht dauerhaft nebeneinander bestehen (Konkurrenzausschlussprinzip)."],
          [("Eine Bakterienkultur verdoppelt sich alle 20 Minuten. Wie viele Zellen sind es aus 100 Zellen nach einer Stunde?", ["Eine Stunde = 3 Verdopplungen.", "100 · 2³ = 800"], "800 Zellen")],
          [("Eine Population wächst in der Natur dauerhaft exponentiell.", "Begrenzte Ressourcen bremsen das Wachstum."), ("Räuber und Beute schwanken gleichzeitig.", "Die Räuberkurve folgt der Beutekurve zeitversetzt."),
           ("Temperatur ist ein dichteabhängiger Faktor.", "Temperatur wirkt unabhängig von der Dichte.")],
          [("Was sind r-Strategen?", "Arten mit vielen Nachkommen, kurzer Lebensdauer und wenig Brutpflege, zum Beispiel Mäuse oder Insekten."), ("Was ist eine ökologische Nische?", "Die Gesamtheit der Ansprüche einer Art an ihre Umwelt, kein Ort."),
           ("Warum gibt es Zeigerarten?", "Stenöke Arten zeigen bestimmte Umweltbedingungen an, etwa Flechten saubere Luft.")],
          [("Dichteabhängig oder dichteunabhängig?", {"den dichteabhängigen Faktoren": ["Nahrungsmangel", "Konkurrenz", "Fressfeinde", "Parasiten", "ansteckende Krankheiten", "Stress durch Enge"],
                                                      "den dichteunabhängigen Faktoren": ["Frost", "Hochwasser", "Dürre", "Waldbrand durch Blitz", "Temperatur", "Vulkanausbruch"]}),
           ("Begriffe", [("Optimum", "Bereich der besten Lebensbedingungen"), ("Pessimum", "Bereich, in dem eine Art gerade noch überlebt"), ("stenök", "enger Toleranzbereich"), ("euryök", "weiter Toleranzbereich"),
                         ("Kapazität", "maximale Populationsgröße, die ein Lebensraum trägt"), ("ökologische Nische", "Gesamtheit der Ansprüche einer Art"), ("Zeigerart", "stenöke Art, die bestimmte Bedingungen anzeigt"),
                         ("ökologische Potenz", "Fähigkeit, Schwankungen eines Faktors zu ertragen")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Wachstum und Strategien", [("exponentielles Wachstum", "J-förmige Kurve ohne Grenze"), ("logistisches Wachstum", "S-förmige Kurve bis zur Kapazität"), ("r-Strategen", "viele Nachkommen, wenig Brutpflege"),
                                        ("K-Strategen", "wenige Nachkommen, viel Brutpflege"), ("Lotka-Volterra-Regel 1", "Räuber und Beute schwanken periodisch und phasenverschoben"),
                                        ("Lotka-Volterra-Regel 3", "nach starker Dezimierung erholt sich die Beute schneller"), ("Konkurrenzausschlussprinzip", "zwei Arten mit gleicher Nische können nicht dauerhaft koexistieren")],
            "Was beschreibt {k}?", "Welcher Begriff ist gemeint: {v}?")],
          ["Jede Art hat einen Toleranzbereich.", "Stenöke Arten haben einen engen Toleranzbereich.", "Logistisches Wachstum endet an der Kapazitätsgrenze.", "Nahrungsmangel ist ein dichteabhängiger Faktor.",
           "Räuberkurven folgen der Beutekurve zeitversetzt.", "K-Strategen betreiben viel Brutpflege.", "Eine ökologische Nische ist kein Ort.", "Flechten zeigen saubere Luft an."],
          [("Populationen wachsen in der Natur unbegrenzt.", "Die Kapazität begrenzt das Wachstum."), ("Frost ist ein dichteabhängiger Faktor.", "Frost wirkt dichteunabhängig."),
           ("Euryöke Arten haben einen engen Toleranzbereich.", "Sie haben einen weiten."), ("Räuber und Beute schwanken gleichzeitig.", "Sie schwanken zeitversetzt."),
           ("r-Strategen betreiben viel Brutpflege.", "Das sind K-Strategen."), ("Eine ökologische Nische ist ein Wohnort.", "Sie ist die Gesamtheit der Ansprüche.")],
          "Populationen", "living-things-and-ecosystems"),

        H("C", "molekuelstruktur-und-zwischenmolekulare-kraefte", "Molekülstruktur und zwischenmolekulare Kräfte", "Zwischenmolekulare Kräfte",
          "Die Schülerinnen und Schüler leiten Molekülgeometrien mit dem Elektronenpaarabstoßungsmodell ab, bestimmen Polarität mit der Elektronegativität und erklären Siedetemperaturen und Löslichkeit mit zwischenmolekularen Kräften.",
          "Elektronenpaarabstoßungsmodell (EPA), tetraedrisch, trigonal-pyramidal, gewinkelt, linear, Elektronegativitätsdifferenz, Dipolmolekül, Van-der-Waals-Kräfte, Dipol-Dipol-Kräfte, Wasserstoffbrücken",
          "Stärkere Kräfte zwischen Molekülen: höhere Siedetemperatur", "Wasserstoffbrücken sind stärker als Dipol-Dipol-Kräfte, diese stärker als Van-der-Waals-Kräfte.",
          ["Nach dem EPA-Modell stoßen sich Elektronenpaare ab und ordnen sich möglichst weit voneinander an. Methan ist tetraedrisch, Ammoniak trigonal-pyramidal, Wasser gewinkelt, CO₂ linear.",
           "Eine Bindung ist polar, wenn die Elektronegativitätsdifferenz groß ist (etwa 0,5 bis 1,7). Ein Molekül ist ein Dipol, wenn sich die Teilladungen nicht aufheben.",
           "Van-der-Waals-Kräfte wirken zwischen allen Molekülen und wachsen mit der Oberfläche. Dipol-Dipol-Kräfte wirken zwischen Dipolen. Wasserstoffbrücken entstehen bei H an N, O oder F."],
          [("Warum siedet Wasser (100 °C) viel höher als Schwefelwasserstoff H₂S (−60 °C)?", ["Beide Moleküle sind gewinkelt.", "Nur zwischen Wassermolekülen bilden sich starke Wasserstoffbrücken."], "wegen der Wasserstoffbrücken")],
          [("CO₂ ist ein Dipol, weil die Bindungen polar sind.", "Das lineare CO₂ ist kein Dipol, die Teilladungen heben sich auf."), ("Beim Sieden werden Atombindungen gespalten.", "Beim Sieden werden nur zwischenmolekulare Kräfte überwunden."),
           ("Wasserstoffbrücken gibt es bei jedem H-Atom.", "Nur bei H an stark elektronegativen Atomen wie N, O und F.")],
          [("Warum steigt die Siedetemperatur der Alkane mit der Kettenlänge?", "Längere Moleküle haben eine größere Oberfläche und stärkere Van-der-Waals-Kräfte."),
           ("Was bedeutet „Ähnliches löst sich in Ähnlichem“?", "Polare Stoffe lösen sich in polaren Lösemitteln, unpolare in unpolaren."), ("Welcher Bindungswinkel hat Methan?", "Etwa 109,5°, der Tetraederwinkel.")],
          [("Molekülgeometrie", [("CH₄", "tetraedrisch"), ("NH₃", "trigonal-pyramidal"), ("H₂O", "gewinkelt"), ("CO₂", "linear"), ("BF₃", "trigonal-planar"), ("HCN", "linear"),
                                 ("H₂S", "gewinkelt"), ("CCl₄", "tetraedrisch"), ("PH₃", "trigonal-pyramidal")],
            "Welche Form hat das Molekül {k}?", None),
           ("Dipol oder nicht?", {"den Dipolmolekülen": ["H₂O", "NH₃", "HCl", "CH₃Cl", "H₂S", "Ethanol"],
                                  "den unpolaren Molekülen": ["CO₂", "CH₄", "CCl₄", "O₂", "N₂", "BF₃"]}),
           ("Stärkste Kraft", [("zwischen Wassermolekülen", "Wasserstoffbrücken"), ("zwischen Ammoniakmolekülen", "Wasserstoffbrücken"), ("zwischen Ethanolmolekülen", "Wasserstoffbrücken"),
                               ("zwischen Chlorwasserstoffmolekülen", "Dipol-Dipol-Kräfte"), ("zwischen Chlormethanmolekülen", "Dipol-Dipol-Kräfte"), ("zwischen Methanmolekülen", "Van-der-Waals-Kräfte"),
                               ("zwischen Octanmolekülen", "Van-der-Waals-Kräfte"), ("zwischen Iodmolekülen", "Van-der-Waals-Kräfte")],
            "Welche zwischenmolekulare Kraft ist am stärksten? {k}", None, ("Ionenbindung",))],
          ["Methan ist tetraedrisch gebaut.", "Wasser ist ein gewinkeltes Dipolmolekül.", "CO₂ ist linear und kein Dipol.", "Wasserstoffbrücken bilden sich bei H an N, O oder F.",
           "Beim Sieden werden zwischenmolekulare Kräfte überwunden.", "Van-der-Waals-Kräfte wachsen mit der Moleküloberfläche.", "Polare Stoffe lösen sich in polaren Lösemitteln.", "Ammoniak ist trigonal-pyramidal."],
          [("CO₂ ist ein Dipol.", "CO₂ ist linear und unpolar."), ("Beim Sieden werden Atombindungen gespalten.", "Es werden nur zwischenmolekulare Kräfte überwunden."),
           ("Methan bildet Wasserstoffbrücken.", "Methan hat keine H-Atome an N, O oder F."), ("Wasser ist linear gebaut.", "Es ist gewinkelt."),
           ("Van-der-Waals-Kräfte sind stärker als Wasserstoffbrücken.", "Wasserstoffbrücken sind stärker."), ("Öl löst sich gut in Wasser.", "Öl ist unpolar und löst sich nicht in Wasser.")],
          "zwischenmolekulare Kräfte", "matter"),

        H("C", "funktionelle-gruppen-und-isomerie", "Funktionelle Gruppen und Isomerie", "Funktionelle Gruppen",
          "Die Schülerinnen und Schüler ordnen organische Verbindungen nach funktionellen Gruppen, benennen sie nach der IUPAC-Nomenklatur, unterscheiden Isomere und beschreiben die Oxidationsreihe der Alkohole.",
          "Alkanole, Alkanale, Alkanone, Alkansäuren, Ester, Amine, primäre, sekundäre und tertiäre Alkohole, Oxidation mit Kupferoxid, Konstitutionsisomerie, IUPAC-Namen",
          "Die funktionelle Gruppe bestimmt die Stoffklasse", "Primäre Alkohole werden zu Aldehyden und weiter zu Carbonsäuren oxidiert.",
          ["Hydroxygruppe –OH: Alkohole (Alkanole). Carbonylgruppe C=O: am Kettenende Aldehyde (Alkanale), in der Kette Ketone (Alkanone). Carboxygruppe –COOH: Carbonsäuren.",
           "Primäre Alkohole oxidieren zu Aldehyden und dann zu Carbonsäuren, sekundäre zu Ketonen. Tertiäre Alkohole lassen sich so nicht oxidieren.",
           "Konstitutionsisomere haben dieselbe Summenformel, aber eine andere Verknüpfung der Atome, zum Beispiel Propan-1-ol und Propan-2-ol."],
          [("Was entsteht, wenn Propan-2-ol mit heißem Kupferoxid oxidiert wird?", ["Propan-2-ol ist ein sekundärer Alkohol.", "Sekundäre Alkohole werden zu Ketonen oxidiert."], "Propanon (Aceton)")],
          [("Ketone werden zu Carbonsäuren oxidiert.", "Ketone lassen sich nicht weiter oxidieren, Aldehyde schon."), ("Isomere haben verschiedene Summenformeln.", "Isomere haben die gleiche Summenformel."),
           ("Ethanol ist ein Aldehyd.", "Ethanol ist ein Alkohol, Ethanal ist ein Aldehyd.")],
          [("Wie weist man Aldehyde nach?", "Mit der Fehling-Probe (roter Niederschlag) oder der Silberspiegelprobe."), ("Woran erkennt man die Endung im Namen?", "-ol für Alkohole, -al für Aldehyde, -on für Ketone, -säure für Carbonsäuren."),
           ("Was ist ein tertiärer Alkohol?", "Das C-Atom mit der OH-Gruppe ist an drei weitere C-Atome gebunden.")],
          [("Stoffklassen", [("Ethanol", "Alkohol"), ("Propan-2-ol", "Alkohol"), ("Methanal", "Aldehyd"), ("Ethanal", "Aldehyd"), ("Propanon", "Keton"), ("Butanon", "Keton"),
                             ("Ethansäure", "Carbonsäure"), ("Methansäure", "Carbonsäure"), ("Ethansäureethylester", "Ester"), ("Methylamin", "Amin")],
            "Zu welcher Stoffklasse gehört {k}?", None),
           ("Oxidation", [("Ethanol", "Ethanal"), ("Ethanal", "Ethansäure"), ("Propan-1-ol", "Propanal"), ("Propanal", "Propansäure"), ("Propan-2-ol", "Propanon"), ("Butan-2-ol", "Butanon"),
                          ("Methanol", "Methanal"), ("Methanal", "Methansäure")],
            "Was entsteht bei der Oxidation von {k}?", "Woraus entsteht {v} durch Oxidation?"),
           ("Gruppen und Endungen", [("–OH an einem C-Atom", "Endung -ol"), ("–CHO am Kettenende", "Endung -al"), ("C=O in der Kette", "Endung -on"), ("–COOH", "Endung -säure"),
                                     ("–COO– zwischen zwei Resten", "Ester"), ("–NH₂", "Amin"), ("C=C-Doppelbindung", "Endung -en")],
            "Welche Endung oder Stoffklasse passt zu {k}?", "Welche Gruppe gehört zu: {v}?")],
          ["Alkohole haben eine Hydroxygruppe.", "Aldehyde haben die Carbonylgruppe am Kettenende.", "Primäre Alkohole werden zu Aldehyden oxidiert.", "Sekundäre Alkohole werden zu Ketonen oxidiert.",
           "Isomere haben die gleiche Summenformel.", "Die Fehling-Probe weist Aldehyde nach.", "Tertiäre Alkohole lassen sich kaum oxidieren.", "Propanon ist ein Keton."],
          [("Ketone werden zu Carbonsäuren oxidiert.", "Ketone lassen sich nicht weiter oxidieren."), ("Isomere haben verschiedene Summenformeln.", "Sie haben die gleiche Summenformel."),
           ("Ethanol ist ein Aldehyd.", "Ethanol ist ein Alkohol."), ("Sekundäre Alkohole werden zu Aldehyden oxidiert.", "Sie werden zu Ketonen oxidiert."),
           ("Die Endung -al steht für Alkohole.", "Die Endung -al steht für Aldehyde."), ("Propan-1-ol und Propan-2-ol haben verschiedene Summenformeln.", "Sie sind Isomere mit der gleichen Summenformel.")],
          "funktionelle Gruppen", "matter"),

        H("C", "reaktionsgeschwindigkeit", "Reaktionsgeschwindigkeit", "Reaktionsgeschwindigkeit",
          "Die Schülerinnen und Schüler bestimmen mittlere Reaktionsgeschwindigkeiten aus Messwerten, erklären den Einfluss von Konzentration, Temperatur, Zerteilungsgrad und Katalysatoren mit dem Stoßmodell.",
          "mittlere Reaktionsgeschwindigkeit v = Δc : Δt, Stoßtheorie, wirksame Stöße, Aktivierungsenergie, RGT-Regel, Zerteilungsgrad, Katalysator, Energiediagramm",
          "Mehr wirksame Stöße: schnellere Reaktion", "Temperatur, Konzentration, Zerteilungsgrad und Katalysatoren erhöhen die Reaktionsgeschwindigkeit.",
          ["Die mittlere Reaktionsgeschwindigkeit ist die Konzentrationsänderung pro Zeit: v = Δc : Δt in mol/(l·s).",
           "Nach der Stoßtheorie reagieren Teilchen nur bei wirksamen Zusammenstößen mit genug Energie und richtiger Orientierung. Höhere Konzentration und feinere Zerteilung erhöhen die Stoßzahl.",
           "Höhere Temperatur erhöht Stoßzahl und Anteil energiereicher Teilchen (RGT-Regel: etwa doppelt so schnell pro 10 °C). Ein Katalysator senkt die Aktivierungsenergie und wird nicht verbraucht."],
          [("Warum reagiert Zinkpulver schneller mit Salzsäure als ein Zinkblech?", ["Pulver hat eine viel größere Oberfläche.", "Es gibt mehr Zusammenstöße mit Säureteilchen."], "wegen des höheren Zerteilungsgrads")],
          [("Ein Katalysator liefert Energie.", "Ein Katalysator senkt die Aktivierungsenergie, er liefert keine Energie."), ("Jeder Zusammenstoß führt zur Reaktion.", "Nur wirksame Stöße mit genug Energie führen zur Reaktion."),
           ("Die Geschwindigkeit bleibt während der Reaktion gleich.", "Sie nimmt meist ab, weil die Eduktkonzentration sinkt.")],
          [("Warum wird die Reaktion mit der Zeit langsamer?", "Die Eduktkonzentration sinkt, es gibt weniger Zusammenstöße."), ("Was zeigt ein Energiediagramm?", "Die Energie von Edukten, Übergangszustand und Produkten. Der Abstand zum Übergangszustand ist die Aktivierungsenergie."),
           ("Wo nutzt man Katalysatoren?", "Im Autoabgaskatalysator, bei der Ammoniaksynthese und in Enzymen.")],
          [("Einflüsse", [("Konzentration der Salzsäure erhöhen", "schneller"), ("Temperatur um 10 °C erhöhen", "schneller"), ("Kalkstein zu Pulver mahlen", "schneller"), ("Katalysator zugeben", "schneller"),
                          ("Lösung stark verdünnen", "langsamer"), ("Reaktionsgemisch kühlen", "langsamer"), ("großes Stück statt Pulver", "langsamer"), ("Edukt wird mit der Zeit verbraucht", "langsamer")],
            "Wie ändert sich die Reaktionsgeschwindigkeit? {k}", None, ("gleich", "Reaktion stoppt sofort")),
           ("Begriffe", [("Reaktionsgeschwindigkeit", "Konzentrationsänderung pro Zeit"), ("wirksamer Stoß", "Zusammenstoß mit genug Energie und richtiger Orientierung"), ("Aktivierungsenergie", "Mindestenergie für den Start der Reaktion"),
                         ("Katalysator", "senkt die Aktivierungsenergie und wird nicht verbraucht"), ("RGT-Regel", "pro 10 °C etwa doppelte Geschwindigkeit"), ("Zerteilungsgrad", "wie fein ein Feststoff verteilt ist"),
                         ("Übergangszustand", "energiereichster Punkt der Reaktion")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Messmethoden", [("Kalk mit Salzsäure", "Gasvolumen des CO₂ messen"), ("Magnesium mit Salzsäure", "Volumen des Wasserstoffs messen"), ("Natriumthiosulfat mit Salzsäure", "Zeit bis zur Trübung messen"),
                             ("Marmor in Säure auf der Waage", "Massenabnahme durch entweichendes Gas messen"), ("Abbau eines Farbstoffs", "Farbintensität mit dem Fotometer messen"), ("Ester-Verseifung", "Leitfähigkeit messen")],
            "Wie verfolgt man diese Reaktion? {k}", "Bei welcher Reaktion misst man so: {v}?")],
          ["Reaktionsgeschwindigkeit ist Δc durch Δt.", "Nur wirksame Stöße führen zur Reaktion.", "Höhere Temperatur beschleunigt Reaktionen.", "Katalysatoren senken die Aktivierungsenergie.",
           "Pulver reagiert schneller als ein Block.", "Die Geschwindigkeit nimmt mit sinkender Eduktkonzentration ab.", "Katalysatoren werden nicht verbraucht.", "Nach der RGT-Regel verdoppelt sich v pro 10 °C etwa."],
          [("Ein Katalysator liefert Energie.", "Er senkt die Aktivierungsenergie."), ("Jeder Zusammenstoß führt zur Reaktion.", "Nur wirksame Stöße."), ("Kühlen beschleunigt Reaktionen.", "Kühlen verlangsamt sie."),
           ("Katalysatoren werden verbraucht.", "Sie bleiben erhalten."), ("Verdünnen erhöht die Geschwindigkeit.", "Verdünnen verlangsamt."), ("Die Geschwindigkeit bleibt immer konstant.", "Sie nimmt meist ab.")],
          "die Reaktionsgeschwindigkeit", "matter", calc=f_rate),

        H("C", "chemisches-gleichgewicht", "Chemisches Gleichgewicht", "Chemisches Gleichgewicht",
          "Die Schülerinnen und Schüler beschreiben umkehrbare Reaktionen und das dynamische Gleichgewicht, wenden das Massenwirkungsgesetz an und sagen mit dem Prinzip von Le Chatelier Verschiebungen voraus.",
          "umkehrbare Reaktion, dynamisches Gleichgewicht, Massenwirkungsgesetz, Gleichgewichtskonstante, Prinzip von Le Chatelier, Konzentration, Druck, Temperatur, Haber-Bosch-Verfahren",
          "Im Gleichgewicht laufen Hin- und Rückreaktion gleich schnell", "Ein gestörtes Gleichgewicht weicht dem Zwang aus (Prinzip von Le Chatelier).",
          ["Bei umkehrbaren Reaktionen stellt sich ein dynamisches Gleichgewicht ein: Hin- und Rückreaktion laufen weiter, aber gleich schnell. Die Konzentrationen bleiben konstant.",
           "Massenwirkungsgesetz für A + B ⇌ C + D: K<sub>c</sub> = c(C) · c(D) : (c(A) · c(B)). Ist K<sub>c</sub> groß, liegt das Gleichgewicht auf der Seite der Produkte.",
           "Le Chatelier: Mehr Edukt verschiebt zu den Produkten. Druckerhöhung verschiebt zur Seite mit weniger Gasteilchen. Erwärmen begünstigt die endotherme Richtung. Ein Katalysator verschiebt nichts."],
          [("N₂ + 3 H₂ ⇌ 2 NH₃ ist exotherm. Wie erhält man mehr Ammoniak?", ["Rechts stehen weniger Gasteilchen (2 statt 4).", "Die Hinreaktion gibt Wärme ab."], "hoher Druck und niedrige Temperatur")],
          [("Im Gleichgewicht ist die Reaktion zu Ende.", "Hin- und Rückreaktion laufen weiter, nur gleich schnell."), ("Ein Katalysator verschiebt das Gleichgewicht.", "Er beschleunigt nur seine Einstellung."),
           ("Im Gleichgewicht sind die Konzentrationen gleich groß.", "Sie sind konstant, aber nicht unbedingt gleich.")],
          [("Warum arbeitet das Haber-Bosch-Verfahren bei etwa 450 °C?", "Bei niedriger Temperatur wäre die Ausbeute höher, aber die Reaktion zu langsam. 450 °C ist ein Kompromiss."),
           ("Was ändert K<sub>c</sub>?", "Nur die Temperatur. Konzentrations- und Druckänderungen verschieben die Lage, K<sub>c</sub> bleibt gleich."), ("Was ist ein offenes System?", "Ein System, das Stoffe mit der Umgebung austauscht, dort stellt sich kein Gleichgewicht ein.")],
          [("Verschiebungen", [("Edukt zugeben", "zu den Produkten"), ("Produkt entfernen", "zu den Produkten"), ("Produkt zugeben", "zu den Edukten"), ("Edukt entfernen", "zu den Edukten"),
                               ("Druck erhöhen bei weniger Gasteilchen rechts", "zu den Produkten"), ("Druck erhöhen bei weniger Gasteilchen links", "zu den Edukten"),
                               ("bei exothermer Hinreaktion erwärmen", "zu den Edukten"), ("bei endothermer Hinreaktion erwärmen", "zu den Produkten"), ("Katalysator zugeben", "keine Verschiebung")],
            "Wohin verschiebt sich das Gleichgewicht? {k}", None),
           ("Begriffe", [("dynamisches Gleichgewicht", "Hin- und Rückreaktion laufen gleich schnell"), ("Massenwirkungsgesetz", "Quotient aus Produkt- und Eduktkonzentrationen ist konstant"),
                         ("K<sub>c</sub> viel größer als 1", "Gleichgewicht liegt bei den Produkten"), ("K<sub>c</sub> viel kleiner als 1", "Gleichgewicht liegt bei den Edukten"),
                         ("Prinzip von Le Chatelier", "das System weicht einem Zwang aus"), ("umkehrbare Reaktion", "Reaktion, die in beide Richtungen ablaufen kann"), ("geschlossenes System", "kein Stoffaustausch mit der Umgebung")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Beispiele", [("Haber-Bosch-Verfahren", "Ammoniak aus Stickstoff und Wasserstoff"), ("Kontaktverfahren", "Schwefeltrioxid für die Schwefelsäure"), ("Estergleichgewicht", "Ester und Wasser aus Säure und Alkohol"),
                          ("Kalkbrennen im offenen Ofen", "CO₂ entweicht, kein Gleichgewicht"), ("Mineralwasserflasche geöffnet", "CO₂ entweicht, das Gleichgewicht verschiebt sich"), ("Stickstoffdioxid und Distickstofftetraoxid", "Farbänderung beim Erwärmen und Kühlen")],
            "Worum geht es bei {k}?", "Welches Beispiel passt: {v}?")],
          ["Im Gleichgewicht laufen Hin- und Rückreaktion gleich schnell.", "Ein Katalysator verschiebt das Gleichgewicht nicht.", "K<sub>c</sub> hängt nur von der Temperatur ab.", "Druckerhöhung begünstigt die Seite mit weniger Gasteilchen.",
           "Entfernen eines Produkts verschiebt zu den Produkten.", "Erwärmen begünstigt die endotherme Richtung.", "Im Gleichgewicht sind die Konzentrationen konstant.", "Ein großes K<sub>c</sub> bedeutet viel Produkt."],
          [("Im Gleichgewicht ist die Reaktion beendet.", "Beide Richtungen laufen weiter."), ("Ein Katalysator verschiebt das Gleichgewicht.", "Er beschleunigt nur die Einstellung."),
           ("Im Gleichgewicht sind alle Konzentrationen gleich.", "Sie sind konstant, nicht gleich."), ("Druckerhöhung begünstigt die Seite mit mehr Gasteilchen.", "Sie begünstigt die Seite mit weniger."),
           ("Erwärmen begünstigt immer die Produkte.", "Es begünstigt die endotherme Richtung."), ("K<sub>c</sub> ändert sich mit der Konzentration.", "K<sub>c</sub> ändert sich nur mit der Temperatur.")],
          "das chemische Gleichgewicht", "matter", calc=f_K),

        H("P", "kinematik-und-wurfbewegungen", "Kinematik und Wurfbewegungen", "Kinematik",
          "Die Schülerinnen und Schüler beschreiben gleichmäßig beschleunigte Bewegungen mit Bewegungsgleichungen, werten t-s- und t-v-Diagramme aus und zerlegen waagerechte Würfe in unabhängige Bewegungen.",
          "Ort, Geschwindigkeit, Beschleunigung, s = v₀t + ½at², v = v₀ + at, Diagramme, freier Fall, senkrechter und waagerechter Wurf, Unabhängigkeitsprinzip, Bremsweg",
          "Der waagerechte Wurf besteht aus zwei Bewegungen", "Waagerecht gleichförmig mit v₀, senkrecht freier Fall mit g.",
          ["Für die gleichmäßig beschleunigte Bewegung gilt: v = v₀ + a · t und s = v₀ · t + ½ · a · t². Im t-v-Diagramm ist die Fläche unter der Kurve der Weg, die Steigung die Beschleunigung.",
           "Beim freien Fall ist a = g ≈ 9,81 m/s² (hier gerundet 10 m/s²). Die Fallzeit aus der Höhe h ist t = √(2h : g).",
           "Beim waagerechten Wurf bewegt sich der Körper waagerecht gleichförmig und fällt gleichzeitig frei. Die Bahn ist eine Parabel, die Wurfweite ist v₀ · t."],
          [("Ein Stein wird von einer 20 m hohen Klippe mit 5 m/s waagerecht geworfen. Wie weit fliegt er?", ["Fallzeit t = √(2 · 20 : 10) = 2 s", "Wurfweite = 5 m/s · 2 s"], "10 m")],
          [("Ein schneller geworfener Stein fällt langsamer.", "Die Fallzeit hängt nur von der Höhe ab, nicht von v₀."), ("Im t-v-Diagramm ist die Steigung der Weg.", "Die Steigung ist die Beschleunigung, die Fläche der Weg."),
           ("Doppelte Fallzeit bedeutet doppelte Fallhöhe.", "Die Fallhöhe wächst mit t², also vierfach.")],
          [("Wann fliegt ein schräger Wurf am weitesten?", "Ohne Luftwiderstand bei einem Abwurfwinkel von 45°."), ("Was ist das Unabhängigkeitsprinzip?", "Teilbewegungen in verschiedene Richtungen beeinflussen sich nicht."),
           ("Wie liest man die Beschleunigung ab?", "Als Steigung der Geraden im t-v-Diagramm.")],
          [("Diagramme", [("Steigung im t-s-Diagramm", "Geschwindigkeit"), ("Steigung im t-v-Diagramm", "Beschleunigung"), ("Fläche unter der t-v-Kurve", "zurückgelegter Weg"),
                          ("Parabel im t-s-Diagramm", "gleichmäßig beschleunigte Bewegung"), ("waagerechte Linie im t-v-Diagramm", "gleichförmige Bewegung"), ("Gerade durch null im t-v-Diagramm", "Start aus der Ruhe mit konstantem a"),
                          ("Fläche unter der t-a-Kurve", "Geschwindigkeitsänderung")],
            "Was zeigt {k}?", "Woran erkennt man: {v}?"),
           ("Würfe", [("waagerechter Wurf, waagerecht", "gleichförmige Bewegung mit v₀"), ("waagerechter Wurf, senkrecht", "freier Fall"), ("senkrechter Wurf nach oben, am höchsten Punkt", "Geschwindigkeit null"),
                      ("schräger Wurf ohne Luftreibung", "größte Weite bei 45°"), ("Bahn des waagerechten Wurfs", "Parabel"), ("Fallzeit beim waagerechten Wurf", "hängt nur von der Höhe ab")],
            "Was gilt? {k}", "Wozu passt: {v}?"),
           ("Formeln", [("Weg bei konstanter Beschleunigung", "s = v₀ · t + ½ · a · t²"), ("Geschwindigkeit bei konstanter Beschleunigung", "v = v₀ + a · t"), ("Fallzeit aus der Höhe h", "t = √(2h : g)"),
                        ("Bremsweg bis zum Stillstand", "s = v₀² : (2a)"), ("Wurfweite beim waagerechten Wurf", "x = v₀ · t"), ("mittlere Geschwindigkeit", "v = Δs : Δt")],
            "Welche Formel gilt für {k}?", "Was berechnet man mit {v}?")],
          ["Die Steigung im t-v-Diagramm ist die Beschleunigung.", "Die Fläche unter der t-v-Kurve ist der Weg.", "Beim waagerechten Wurf fällt der Körper frei.", "Die Fallzeit hängt nur von der Höhe ab.",
           "Die Bahn des waagerechten Wurfs ist eine Parabel.", "Am höchsten Punkt eines senkrechten Wurfs ist v = 0.", "Doppelte Fallzeit bedeutet vierfache Fallhöhe.", "Der Bremsweg wächst mit v²."],
          [("Ein schneller geworfener Stein fällt langsamer.", "Die Fallzeit hängt nur von der Höhe ab."), ("Die Fläche unter der t-v-Kurve ist die Beschleunigung.", "Sie ist der Weg."),
           ("Doppelte Fallzeit bedeutet doppelte Fallhöhe.", "Die Höhe wächst mit t²."), ("Am höchsten Punkt ist die Beschleunigung null.", "Dort ist die Geschwindigkeit null, a = g bleibt."),
           ("Die Bahn des waagerechten Wurfs ist eine Gerade.", "Sie ist eine Parabel."), ("Der Bremsweg wächst linear mit v.", "Er wächst mit v².")],
          "die Kinematik", "forces-and-motion", calc=f_kin),

        H("P", "impuls-und-stoesse", "Impuls und Stöße", "Impuls",
          "Die Schülerinnen und Schüler definieren den Impuls, wenden den Impulserhaltungssatz auf elastische und unelastische Stöße und den Rückstoß an und berechnen Kräfte aus Impulsänderungen.",
          "Impuls p = m · v, Impulserhaltung, Kraftstoß F · Δt = Δp, elastischer und unelastischer Stoß, Energieerhaltung, Rückstoß, Airbag und Knautschzone",
          "Im abgeschlossenen System bleibt der Impuls erhalten", "Beim unelastischen Stoß bleibt der Impuls erhalten, nicht aber die Bewegungsenergie.",
          ["Der Impuls ist p = m · v in kg·m/s, er ist eine Vektorgröße. Ohne äußere Kräfte bleibt der Gesamtimpuls eines Systems erhalten.",
           "Beim elastischen Stoß bleiben Impuls und Bewegungsenergie erhalten. Beim vollkommen unelastischen Stoß bewegen sich die Körper gemeinsam weiter, ein Teil der Energie wird zu Wärme und Verformung.",
           "Eine Kraft ändert den Impuls: F · Δt = Δp. Airbag und Knautschzone verlängern die Bremszeit und verkleinern so die Kraft."],
          [("Ein Wagen (2 kg, 3 m/s) koppelt an einen ruhenden Wagen (1 kg). Wie schnell fahren beide weiter?", ["Impuls vorher: 2 · 3 = 6 kg·m/s", "6 = 3 kg · v, also v = 2 m/s"], "2 m/s")],
          [("Beim unelastischen Stoß geht Impuls verloren.", "Der Impuls bleibt erhalten, nur Bewegungsenergie wird umgewandelt."), ("Der Impuls hat keine Richtung.", "Der Impuls ist ein Vektor."),
           ("Ein Airbag verringert die Impulsänderung.", "Die Impulsänderung ist gleich, aber sie dauert länger, die Kraft ist kleiner.")],
          [("Wie fliegt eine Rakete im Weltall?", "Sie stößt Gas nach hinten aus und erhält einen gleich großen Impuls nach vorn."), ("Was passiert beim elastischen Stoß gleicher Massen, wenn eine ruht?", "Die Geschwindigkeiten werden getauscht: Die erste bleibt stehen, die zweite rollt weiter."),
           ("Warum knickt man beim Springen in die Knie?", "Die Bremszeit wird länger, die Kraft auf die Gelenke kleiner.")],
          [("Stoßarten", [("Billardkugeln stoßen zusammen", "nahezu elastisch"), ("Zwei Autos verkeilen sich", "unelastisch"), ("Knetkugel bleibt am Wagen kleben", "unelastisch"), ("Kugeln beim Newton-Pendel", "nahezu elastisch"),
                          ("Güterwagen werden angekoppelt", "unelastisch"), ("Flummi prallt vom Boden ab", "nahezu elastisch"), ("Geschoss bleibt im Holzklotz stecken", "unelastisch"), ("Stahlkugeln auf einer Luftkissenbahn mit Federpuffern", "nahezu elastisch"), ("Schneeball klatscht an eine Wand", "unelastisch"), ("Golfschläger trifft den Golfball", "nahezu elastisch"), ("Fußgänger springt auf einen fahrenden Wagen auf", "unelastisch"), ("Tischtennisball prallt von der Platte ab", "nahezu elastisch")],
            "Welche Stoßart ist das? {k}", None, ("gar kein Stoß",)),
           ("Erhaltungsgrößen", [("Impuls beim elastischen Stoß", "bleibt erhalten"), ("Bewegungsenergie beim elastischen Stoß", "bleibt erhalten"), ("Impuls beim unelastischen Stoß", "bleibt erhalten"),
                                 ("Bewegungsenergie beim unelastischen Stoß", "nimmt ab"), ("Gesamtimpuls beim Rückstoß aus der Ruhe", "bleibt null"), ("Masse beim Stoß", "bleibt erhalten")],
            "Was gilt für {k}?", None, ("nimmt zu", "wird verdoppelt")),
           ("Sicherheit", [("Airbag", "verlängert die Bremszeit des Kopfes"), ("Knautschzone", "verformt sich und verlängert die Stoßzeit"), ("Sicherheitsgurt", "bremst den Körper mit dem Auto ab"),
                           ("Fahrradhelm", "verteilt die Kraft und verlängert den Aufprall"), ("Weichbodenmatte", "verlängert die Bremszeit beim Landen"), ("Fangnetz", "bremst über einen längeren Weg")],
            "Wie schützt {k}?", "Welche Schutzmaßnahme {v}?")],
          ["Der Impuls ist Masse mal Geschwindigkeit.", "Der Gesamtimpuls bleibt im abgeschlossenen System erhalten.", "Beim unelastischen Stoß bleibt der Impuls erhalten.", "Beim elastischen Stoß bleibt auch die Bewegungsenergie erhalten.",
           "Kraft mal Zeit ist die Impulsänderung.", "Ein Airbag verkleinert die Kraft durch längere Bremszeit.", "Der Impuls ist ein Vektor.", "Raketen fliegen durch Rückstoß."],
          [("Beim unelastischen Stoß geht Impuls verloren.", "Der Impuls bleibt erhalten."), ("Der Impuls hat keine Richtung.", "Er ist ein Vektor."), ("Ein Airbag verringert die Impulsänderung.", "Er verlängert nur die Zeit."),
           ("Beim unelastischen Stoß bleibt die Bewegungsenergie erhalten.", "Sie nimmt ab."), ("Raketen brauchen Luft zum Abstoßen.", "Sie fliegen durch Rückstoß."), ("Für den Impuls gilt p = m : v.", "Es gilt p = m · v.")],
          "den Impuls", "forces-and-motion", calc=f_impuls),

        H("P", "kreisbewegung-und-gravitation", "Kreisbewegung und Gravitation", "Kreisbewegung",
          "Die Schülerinnen und Schüler beschreiben gleichförmige Kreisbewegungen mit Umlaufdauer, Frequenz und Bahngeschwindigkeit, berechnen die Zentripetalkraft und erklären Planetenbahnen mit dem Gravitationsgesetz und den keplerschen Gesetzen.",
          "Umlaufdauer, Frequenz, Bahngeschwindigkeit, Winkelgeschwindigkeit, Zentripetalkraft F = m · v² : r, Gravitationsgesetz, Ortsfaktor, keplersche Gesetze, Satellitenbahnen",
          "Eine Kreisbewegung braucht eine Kraft zum Mittelpunkt", "Bei Planeten und Satelliten liefert die Gravitation die Zentripetalkraft.",
          ["Bei der gleichförmigen Kreisbewegung gilt v = 2π · r : T und f = 1 : T. Die Richtung ändert sich ständig, also wirkt eine Kraft zum Mittelpunkt: F = m · v² : r.",
           "Das Gravitationsgesetz: F = G · m₁ · m₂ : r². Die Kraft nimmt mit dem Quadrat des Abstands ab. Doppelter Abstand bedeutet ein Viertel der Kraft.",
           "Kepler: Planeten laufen auf Ellipsen, die Sonne steht in einem Brennpunkt. Nahe der Sonne laufen sie schneller. T² : a³ ist für alle Planeten gleich."],
          [("Ein Auto (1000 kg) fährt mit 20 m/s durch eine Kurve mit r = 50 m. Wie groß ist die nötige Zentripetalkraft?", ["F = m · v² : r", "1000 · 400 : 50 = 8000 N"], "8000 N")],
          [("Die Zentrifugalkraft zieht nach außen.", "Im Inertialsystem wirkt nur die Zentripetalkraft nach innen, nach außen wirkt die Trägheit."), ("Im Satelliten herrscht keine Schwerkraft.", "Die Schwerkraft wirkt, alles fällt gemeinsam frei."),
           ("Doppelter Abstand halbiert die Gravitationskraft.", "Doppelter Abstand gibt ein Viertel der Kraft.")],
          [("Was ist ein geostationärer Satellit?", "Ein Satellit, der in etwa 36 000 km Höhe mit der Erde umläuft und immer über demselben Punkt steht."), ("Warum fliegt man in der Kurve nach außen?", "Der Körper will wegen seiner Trägheit geradeaus weiter."),
           ("Was ist die Gravitationskonstante?", "G ≈ 6,67 · 10⁻¹¹ N·m²/kg², sie wurde von Cavendish gemessen.")],
          [("Größen", [("Umlaufdauer", "Zeit für einen vollen Umlauf"), ("Frequenz", "Umläufe pro Sekunde"), ("Bahngeschwindigkeit", "v = 2π · r : T"), ("Zentripetalkraft", "zum Mittelpunkt gerichtete Kraft"),
                       ("Zentripetalbeschleunigung", "a = v² : r"), ("Winkelgeschwindigkeit", "ω = 2π : T"), ("Gravitationskonstante", "G ≈ 6,67 · 10⁻¹¹ N·m²/kg²")],
            "Was beschreibt „{k}“?", "Welche Größe ist das: {v}?"),
           ("Zentripetalkraft im Alltag", [("Auto in der Kurve", "Haftreibung der Reifen"), ("Mond um die Erde", "Gravitation"), ("Hammerwerfer", "Zugkraft im Seil"), ("Elektron um den Kern (Modell)", "elektrische Anziehung"),
                                          ("Kettenkarussell", "Kette und Gewichtskraft"), ("Wäsche in der Schleudertrommel", "Trommelwand"), ("Satellit um die Erde", "Gravitation")],
            "Was liefert die Zentripetalkraft? {k}", None, ("Zentrifugalkraft",)),
           ("Kepler und Gravitation", [("1. keplersches Gesetz", "Planeten laufen auf Ellipsen, die Sonne steht in einem Brennpunkt"), ("2. keplersches Gesetz", "der Fahrstrahl überstreicht in gleichen Zeiten gleiche Flächen"),
                                       ("3. keplersches Gesetz", "T² : a³ ist für alle Planeten gleich"), ("Gravitationsgesetz", "F = G · m₁ · m₂ : r²"), ("doppelter Abstand", "ein Viertel der Gravitationskraft"),
                                       ("doppelte Masse eines Körpers", "doppelte Gravitationskraft")],
            "Was besagt {k}?", "Was ist gemeint? {v}")],
          ["Bei der Kreisbewegung wirkt eine Kraft zum Mittelpunkt.", "Die Zentripetalkraft ist m · v² : r.", "Bei Satelliten liefert die Gravitation die Zentripetalkraft.", "Doppelter Abstand gibt ein Viertel der Gravitationskraft.",
           "Planeten laufen auf Ellipsen.", "Nahe der Sonne laufen Planeten schneller.", "Frequenz ist 1 durch die Umlaufdauer.", "In der ISS wirkt die Schwerkraft."],
          [("Im Satelliten wirkt keine Schwerkraft.", "Sie wirkt, alles fällt frei."), ("Doppelter Abstand halbiert die Gravitationskraft.", "Er gibt ein Viertel."), ("Planeten laufen auf Kreisen mit der Sonne in der Mitte.", "Sie laufen auf Ellipsen."),
           ("In der Kurve wirkt eine Kraft nach außen auf das Auto.", "Die Kraft wirkt nach innen."), ("Nahe der Sonne laufen Planeten langsamer.", "Sie laufen schneller."), ("Für die Bahngeschwindigkeit gilt v = r : T.", "Es gilt v = 2π · r : T.")],
          "die Kreisbewegung", "forces-and-motion", calc=f_kreis),

        H("P", "mechanische-schwingungen", "Mechanische Schwingungen", "Schwingungen",
          "Die Schülerinnen und Schüler beschreiben harmonische Schwingungen mit Amplitude, Periodendauer und Frequenz, berechnen Faden- und Federpendel und erklären Dämpfung und Resonanz.",
          "Auslenkung, Amplitude, Periodendauer, Frequenz, harmonische Schwingung, rücktreibende Kraft, Fadenpendel, Federpendel, Energieumwandlung, Dämpfung, erzwungene Schwingung, Resonanz",
          "Die Pendeldauer hängt nur von Länge und g ab", "Fadenpendel T = 2π · √(l : g), Federpendel T = 2π · √(m : D).",
          ["Eine harmonische Schwingung entsteht, wenn die rücktreibende Kraft proportional zur Auslenkung ist. Das Zeit-Auslenkungs-Diagramm ist eine Sinuskurve.",
           "Für das Fadenpendel gilt T = 2π · √(l : g), unabhängig von Masse und (kleiner) Amplitude. Für das Federpendel gilt T = 2π · √(m : D).",
           "Beim Schwingen wandelt sich Lageenergie in Bewegungsenergie um und zurück. Reibung dämpft die Schwingung. Bei Anregung mit der Eigenfrequenz tritt Resonanz auf."],
          [("Wie ändert sich T, wenn man ein Fadenpendel viermal so lang macht?", ["T ist proportional zu √l.", "√4 = 2"], "Die Schwingungsdauer verdoppelt sich.")],
          [("Ein schwereres Pendel schwingt langsamer.", "Die Masse hat beim Fadenpendel keinen Einfluss."), ("Die Amplitude bestimmt die Periodendauer.", "Bei harmonischen Schwingungen ist T unabhängig von der Amplitude."),
           ("Resonanz tritt bei jeder Frequenz auf.", "Resonanz tritt bei Anregung nahe der Eigenfrequenz auf.")],
          [("Warum ist Resonanz bei Brücken gefährlich?", "Wird eine Brücke mit ihrer Eigenfrequenz angeregt, können die Ausschläge so groß werden, dass sie beschädigt wird."),
           ("Wo nutzt man Pendel?", "In Pendeluhren, Metronomen und Schwingungsdämpfern in Hochhäusern."), ("Was ist die Federkonstante?", "D = F : s gibt an, wie viel Kraft man für 1 m Dehnung braucht.")],
          [("Begriffe", [("Amplitude", "größte Auslenkung aus der Ruhelage"), ("Periodendauer", "Zeit für eine volle Schwingung"), ("Frequenz", "Schwingungen pro Sekunde"), ("Eigenfrequenz", "Frequenz, mit der ein System frei schwingt"),
                         ("Resonanz", "große Ausschläge bei Anregung mit der Eigenfrequenz"), ("Dämpfung", "Abnahme der Amplitude durch Reibung"), ("rücktreibende Kraft", "zieht den Körper zur Ruhelage zurück")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Was ändert T?", [("Fadenpendel viermal so lang", "T verdoppelt sich"), ("Fadenpendel mit doppelter Masse", "T bleibt gleich"), ("Federpendel mit vierfacher Masse", "T verdoppelt sich"),
                              ("Feder mit vierfacher Federkonstante", "T halbiert sich"), ("Fadenpendel auf dem Mond", "T wird größer"), ("Fadenpendel mit kleinerer Amplitude", "T bleibt gleich"),
                              ("Fadenpendel ein Viertel so lang", "T halbiert sich")],
            "Wie ändert sich die Periodendauer? {k}", None, ("T vervierfacht sich",)),
           ("Energie beim Pendel", [("im Umkehrpunkt", "nur Lageenergie, Geschwindigkeit null"), ("beim Durchgang durch die Ruhelage", "größte Bewegungsenergie"), ("mit Reibung", "Energie wird zu Wärme, Amplitude nimmt ab"),
                                    ("ohne Reibung", "Gesamtenergie bleibt konstant"), ("Federpendel in größter Dehnung", "größte Spannenergie"), ("auf halber Strecke zur Ruhelage", "Lage- und Bewegungsenergie gemischt")],
            "Wie ist die Energie verteilt? {k}", "Wann gilt: {v}?")],
          ["Die Schwingungsdauer des Fadenpendels hängt nicht von der Masse ab.", "Ein viermal so langes Pendel schwingt doppelt so lange.", "Resonanz tritt bei Anregung mit der Eigenfrequenz auf.", "Frequenz ist 1 durch T.",
           "In der Ruhelage ist die Bewegungsenergie am größten.", "Dämpfung verringert die Amplitude.", "Die rücktreibende Kraft zeigt zur Ruhelage.", "Eine harmonische Schwingung ergibt eine Sinuskurve."],
          [("Ein schwereres Fadenpendel schwingt langsamer.", "Die Masse hat keinen Einfluss."), ("Ein doppelt so langes Pendel schwingt doppelt so lange.", "T wächst mit √l."),
           ("Im Umkehrpunkt ist die Geschwindigkeit am größten.", "Dort ist sie null."), ("Resonanz tritt bei jeder Anregung auf.", "Nur nahe der Eigenfrequenz."),
           ("Dämpfung vergrößert die Amplitude.", "Sie verringert sie."), ("Eine größere Amplitude verlängert T deutlich.", "T bleibt bei harmonischen Schwingungen gleich.")],
          "Schwingungen", "waves-and-light", calc=f_schw),
    ]
