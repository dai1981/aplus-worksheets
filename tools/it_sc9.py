# -*- coding: utf-8 -*-
"""Italia / Liceo scientifico: prima liceo（Fisica e Scienze naturali, primo biennio）"""
import math
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"
G = 9.8


def f_misure(R):
    k = R.choice(["conv", "conv2", "sci", "err", "relerr", "cifre"])
    if k == "conv":
        x, u1, f, u2 = R.choice([(72, "km/h", 1 / 3.6, "m/s"), (2.5, "g/cm³", 1000, "kg/m³"), (3.6, "km", 1000, "m"), (450, "mm", 0.001, "m"), (2.4, "h", 3600, "s"),
                                 (850, "kg/m³", 0.001, "g/cm³"), (15, "m/s", 3.6, "km/h"), (1.5, "dm³", 0.001, "m³"), (250, "cm²", 0.0001, "m²"), (0.75, "l", 1000, "cm³")])
        return nq("Converti %s %s in %s." % (num(x), u1, u2), x * f, [x / f, x * f * 10, x * f / 10, x], u2, "%s %s = %s %s." % (num(x), u1, num(x * f), u2))
    if k == "conv2":
        x, u1, f, u2 = R.choice([(5, "min", 60, "s"), (2, "giorni", 86400, "s"), (3, "m²", 10000, "cm²"), (2, "m³", 1e6, "cm³"), (90, "km/h", 1 / 3.6, "m/s"), (4.2, "t", 1000, "kg")])
        return nq("Quanto vale %s %s in %s?" % (num(x), u1, u2), x * f, [x / f, x * f / 10, x * f * 10, x * 100], u2, "%s %s = %s %s." % (num(x), u1, num(x * f), u2))
    if k == "sci":
        x = R.choice([0.00045, 0.0000032, 6020000, 384000000, 0.00000071, 150000000000, 0.000081, 72000000])
        a = "%s" % num(x)
        m, e = ("%.2e" % x).split("e")
        e = int(e)
        sup = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
        mm = m.rstrip("0").rstrip(".").replace(".", ",")
        wr = ["%s × 10%s" % (mm, str(-e).translate(sup)), "%s × 10%s" % (mm, str(e + 1).translate(sup)), "%s × 10%s" % (mm, str(e - 1).translate(sup))]
        disp = ("%.10f" % x).rstrip("0").rstrip(".").replace(".", ",") if x < 1 else "{:,}".format(int(x)).replace(",", " ")
        return it("Come si scrive %s in notazione scientifica?" % disp, a, wr, "Si sposta la virgola fino ad avere una sola cifra prima: %s." % a)
    if k == "err":
        v = R.choice([(12.3, 12.7, 12.5), (4.8, 5.4, 5.1), (20.1, 20.9, 20.5), (0.62, 0.68, 0.65), (98, 104, 101), (3.3, 3.9, 3.6)])
        mn, mx, md = v
        return nq("Le misure di una lunghezza vanno da %s cm a %s cm. Quanto vale l’errore assoluto (semidispersione)?" % (num(mn), num(mx)), (mx - mn) / 2, [mx - mn, md, (mx + mn) / 2 * 0.1, (mx - mn) / 4], "cm",
                  "Errore = (valore massimo − valore minimo) : 2 = (%s − %s) : 2 = %s cm." % (num(mx), num(mn), num((mx - mn) / 2)))
    if k == "relerr":
        v, e = R.choice([(50, 0.5), (200, 2), (25, 0.5), (80, 4), (12.5, 0.25), (40, 0.8)])
        return nq("Una misura vale (%s ± %s) cm. Quanto vale l’errore relativo percentuale?" % (num(v), num(e)), e / v * 100, [e / v, v / e, e * v, e / v * 10], "%",
                  "εr = %s : %s × 100 = %s %%." % (num(e), num(v), num(e / v * 100)))
    x, n = R.choice([("0,0450", 3), ("12,30", 4), ("105", 3), ("0,007", 1), ("3,1416", 5), ("2,0", 2), ("6,02 × 10²³", 3), ("1200,0", 5)])
    return nq("Quante cifre significative ha il numero %s?" % x, n, [n + 1, n - 1 if n > 1 else 4, n + 2], "", "Gli zeri iniziali non contano; quelli finali dopo la virgola sì: %d cifre." % n)


def f_forze(R):
    k = R.choice(["peso", "molla", "molla2", "pit", "ris", "attr"])
    if k == "peso":
        m = R.choice([0.25, 1.2, 3.5, 12, 65, 80, 0.8])
        return nq("Quanto pesa un corpo di massa %s kg? (g = 9,8 N/kg)" % num(m), m * G, [m, m / G, m * 10, m * G * 10], "N", "P = m g = %s × 9,8 = %s N." % (num(m), num(m * G)))
    if k == "molla":
        kk, x = R.choice([(40, 0.05), (250, 0.02), (120, 0.1), (800, 0.015), (60, 0.25), (500, 0.04)])
        return nq("Una molla di costante %d N/m si allunga di %s cm. Quanto vale la forza elastica?" % (kk, num(x * 100)), kk * x, [kk * x * 100, kk / x, kk * x / 10, x / kk], "N",
                  "F = k x = %d × %s = %s N (attenzione: %s cm = %s m)." % (kk, num(x), num(kk * x), num(x * 100), num(x)))
    if k == "molla2":
        f, x = R.choice([(10, 0.05), (6, 0.03), (20, 0.08), (3, 0.015), (15, 0.06), (49, 0.07)])
        return nq("Una molla si allunga di %s cm se le appendi un peso di %s N. Quanto vale la costante elastica?" % (num(x * 100), num(f)), f / x, [f * x, f / (x * 100), x / f, f / x / 10], "N/m",
                  "k = F : x = %s : %s = %s N/m." % (num(f), num(x), num(f / x)))
    if k == "pit":
        a, b = R.choice([(3, 4), (6, 8), (5, 12), (9, 12), (8, 15), (12, 16), (7, 24)])
        return nq("Due forze perpendicolari di %d N e %d N agiscono sullo stesso punto. Quanto vale la risultante?" % (a, b), math.hypot(a, b), [a + b, abs(b - a), a * b, (a + b) / 2], "N",
                  "Per il teorema di Pitagora: R = √(%d² + %d²) = %s N." % (a, b, num(math.hypot(a, b))))
    if k == "ris":
        a, b = R.choice([(40, 25), (120, 70), (18, 11), (300, 120), (65, 40)])
        return nq("Due forze di %d N e %d N hanno la stessa direzione e verso opposto. Quanto vale la risultante?" % (a, b), a - b, [a + b, math.hypot(a, b), a * b, (a + b) / 2], "N",
                  "Verso opposto: R = %d − %d = %d N, nel verso della forza maggiore." % (a, b, a - b))
    mu, m = R.choice([(0.3, 10), (0.5, 4), (0.2, 25), (0.4, 15), (0.6, 5), (0.25, 20)])
    return nq("Una cassa di %d kg è su un pavimento con coefficiente d’attrito statico %s. Quale forza serve per smuoverla? (g = 9,8 N/kg)" % (m, num(mu)), mu * m * G, [mu * m, m * G, mu * G, m * G / mu], "N",
              "F = μ m g = %s × %d × 9,8 = %s N." % (num(mu), m, num(mu * m * G)))


def f_equil(R):
    k = R.choice(["mom", "leva", "inc", "inc2", "bar"])
    if k == "mom":
        f, b = R.choice([(20, 0.3), (50, 0.2), (15, 0.4), (80, 0.25), (40, 0.15), (120, 0.5)])
        return nq("Con una chiave lunga %s cm applichi una forza perpendicolare di %d N. Quanto vale il momento?" % (num(b * 100), f), f * b, [f / b, f * b * 100, f + b, b / f], "N·m",
                  "M = F × b = %d × %s = %s N·m." % (f, num(b), num(f * b)))
    if k == "leva":
        r, br, bp = R.choice([(600, 0.4, 1.2), (900, 0.3, 1.5), (240, 0.5, 2), (1500, 0.2, 1), (420, 0.6, 1.8), (800, 0.25, 2)])
        return nq("Con una leva sollevi un carico di %d N posto a %s m dal fulcro. Tu spingi a %s m dal fulcro. Quale forza serve?" % (r, num(br), num(bp)), r * br / bp,
                  [r * bp / br, r * br * bp, r / bp, r], "N", "Equilibrio dei momenti: F × %s = %d × %s → F = %s N." % (num(bp), r, num(br), num(r * br / bp)))
    if k == "inc":
        m, a = R.choice([(10, 30), (20, 30), (5, 30), (50, 30), (8, 30), (30, 30)])
        return nq("Un corpo di %d kg è su un piano inclinato liscio di 30°. Quale forza parallela al piano serve per tenerlo fermo? (g = 9,8 N/kg)" % m, m * G * 0.5,
                  [m * G, m * G * math.sqrt(3) / 2, m * 0.5, m * G * 2], "N", "F = m g sen 30° = %d × 9,8 × 0,5 = %s N." % (m, num(m * G * 0.5)))
    if k == "inc2":
        p, h, l = R.choice([(600, 1, 4), (500, 2, 5), (800, 1.5, 6), (300, 0.5, 2), (1000, 2, 8), (450, 1, 3)])
        return nq("Spingi una cassa di peso %d N su una rampa liscia lunga %s m e alta %s m. Quale forza parallela alla rampa serve per l’equilibrio?" % (p, num(l), num(h)), p * h / l,
                  [p * l / h, p, p * h, p / l], "N", "F = P × h : l = %d × %s : %s = %s N." % (p, num(h), num(l), num(p * h / l)))
    a, b, d = R.choice([(2, 3, 1), (4, 1, 1), (3, 5, 0.8), (6, 2, 2), (1, 4, 1.5), (5, 5, 2)])
    x = b * d / (a + b)
    return nq("Due masse di %d kg e %d kg sono agli estremi di un’asta leggera lunga %s m. A quale distanza dalla massa di %d kg si trova il baricentro?" % (a, b, num(d), a), x,
              [a * d / (a + b), d / 2 if abs(x - d / 2) > 0.01 else d / 3, x * 2, d - x / 2], "m", "x = m₂ × d : (m₁ + m₂) = %d × %s : %d = %s m." % (b, num(d), a + b, num(x)))


def f_fluidi(R):
    k = R.choice(["p", "stev", "pasc", "arch", "gall", "atm"])
    if k == "p":
        f, s = R.choice([(700, 0.035), (1200, 0.06), (50, 0.0025), (25000, 0.5), (900, 0.045), (600, 0.002)])
        return nq("Una forza di %s N agisce su %s m². Quanto vale la pressione?" % (num(f), num(s)), f / s, [f * s, s / f, f / s / 1000, f], "Pa", "p = F : S = %s Pa." % num(f / s))
    if k == "stev":
        d, h, n = R.choice([(1000, 4, "acqua"), (1030, 10, "acqua di mare"), (800, 2, "olio"), (13600, 0.76, "mercurio"), (1000, 25, "acqua"), (1030, 50, "acqua di mare")])
        return nq("Quanto vale la pressione dovuta a una colonna di %s (d = %s kg/m³) alta %s m? (g = 9,8 m/s²)" % (n, num(d), num(h)), d * G * h, [d * h, d * G / h, G * h, d * G * h / 1000], "Pa",
                  "p = d g h = %s × 9,8 × %s = %s Pa." % (num(d), num(h), num(d * G * h)))
    if k == "pasc":
        f1, s1, s2 = R.choice([(100, 0.01, 0.5), (50, 0.002, 0.1), (200, 0.004, 0.2), (80, 0.01, 1), (150, 0.003, 0.09)])
        return nq("In un torchio idraulico spingi con %d N su un pistone di %s m². Il pistone grande ha %s m². Quale forza si ottiene?" % (f1, num(s1), num(s2)), f1 * s2 / s1,
                  [f1 * s1 / s2, f1, f1 * s2, f1 / s1], "N", "F₂ = F₁ × S₂ : S₁ = %d × %s : %s = %s N." % (f1, num(s2), num(s1), num(f1 * s2 / s1)))
    if k == "arch":
        v, d = R.choice([(0.002, 1000), (0.0005, 1000), (0.01, 1030), (0.003, 800), (0.04, 1000), (0.0015, 1030)])
        return nq("Un corpo di volume %s m³ è completamente immerso in un liquido di densità %s kg/m³. Quanto vale la spinta di Archimede? (g = 9,8 m/s²)" % (num(v), num(d)), d * v * G,
                  [d * v, v * G, d * G, d * v * G / 1000], "N", "S = d V g = %s × %s × 9,8 = %s N." % (num(d), num(v), num(d * v * G)))
    if k == "gall":
        dc, dl = R.choice([(600, 1000), (920, 1030), (800, 1000), (250, 1000), (700, 1000), (900, 1030)])
        return nq("Un cubo di legno di densità %d kg/m³ galleggia in un liquido di densità %d kg/m³. Quale frazione del volume è immersa (in percentuale)?" % (dc, dl), dc / dl * 100,
                  [dl / dc * 100, 100 - dc / dl * 100, dc / 10, 50 if abs(dc / dl * 100 - 50) > 1 else 40], "%", "Frazione immersa = %d : %d = %s %%." % (dc, dl, num(dc / dl * 100)))
    h = R.choice([0.76, 0.5, 0.7, 0.74])
    return nq("Nell’esperimento di Torricelli il mercurio (13 600 kg/m³) sale di %s m. Quanto vale la pressione atmosferica? (g = 9,8 m/s²)" % num(h), 13600 * G * h,
              [13600 * h, 13600 * G, 1000 * G * h, 13600 * G * h / 100], "Pa", "p = d g h = 13 600 × 9,8 × %s = %s Pa." % (num(h), num(13600 * G * h)))


def f_chim(R):
    k = R.choice(["lav", "prou", "prou2", "conc", "dens", "perc"])
    if k == "lav":
        a, b, c = R.choice([(12, 32, 44), (2.4, 6.4, 8.8), (5.6, 3.2, 8.8), (4, 32, 36), (23, 35.5, 58.5), (6.5, 3.2, 9.7)])
        return nq("Si fanno reagire completamente %s g di un elemento con %s g di un altro e si forma un unico composto. Quanti grammi di composto si ottengono?" % (num(a), num(b)), c,
                  [abs(a - b), a * b, c / 2, max(a, b)], "g", "Legge di Lavoisier: %s + %s = %s g." % (num(a), num(b), num(c)))
    if k == "prou":
        r, a = R.choice([((7, 4), 14), ((3, 8), 9), ((1, 8), 5), ((7, 4), 21), ((3, 4), 6), ((1, 8), 3)])
        b = a * r[1] / r[0]
        return nq("Nel composto il rapporto tra le masse dei due elementi è %d : %d. Con %d g del primo, quanti grammi del secondo reagiscono?" % (r[0], r[1], a), b,
                  [a * r[0] / r[1], a + b, b * 2, a], "g", "Legge di Proust: %d × %d : %d = %s g." % (a, r[1], r[0], num(b)))
    if k == "prou2":
        a, b = R.choice([(7, 4), (3, 8), (1, 8), (3, 4), (2, 1)])
        m = R.choice([22, 44, 66, 110, 33])
        tot = a + b
        return nq("In un composto il rapporto in massa è %d : %d. Quanti grammi del primo elemento ci sono in %d g di composto?" % (a, b, m), m * a / tot, [m * b / tot, m * a / b, m / a, m / 2], "g",
                  "Il primo elemento è %d parti su %d: %d × %d : %d = %s g." % (a, tot, m, a, tot, num(m * a / tot)))
    if k == "conc":
        s, v = R.choice([(25, 0.5), (9, 1), (40, 0.25), (3, 0.15), (60, 2), (12, 0.4)])
        return nq("Sciogli %s g di soluto in acqua fino a %s l di soluzione. Qual è la concentrazione?" % (num(s), num(v)), s / v, [s * v, v / s, s / v / 1000, s], "g/l",
                  "c = m : V = %s : %s = %s g/l." % (num(s), num(v), num(s / v)))
    if k == "dens":
        m, v = R.choice([(39.5, 5), (54, 20), (113, 10), (7.8, 10), (19.3, 1), (92, 100)])
        return nq("Un campione ha massa %s g e volume %s cm³. Qual è la densità?" % (num(m), num(v)), m / v, [m * v, v / m, m / v * 1000, m - v], "g/cm³",
                  "d = m : V = %s g/cm³." % num(m / v))
    s, w = R.choice([(15, 135), (20, 80), (5, 95), (12, 188), (30, 120), (8, 72)])
    return nq("Sciogli %d g di sale in %d g d’acqua. Qual è la percentuale in massa (%% m/m)?" % (s, w), s * 100 / (s + w), [s * 100 / w, s, w / s, s / (s + w)], "%",
              "%% m/m = %d : (%d + %d) × 100 = %s %%." % (s, s, w, num(s * 100 / (s + w))))


def f_terra(R):
    k = R.choice(["fuso", "fuso2", "lat", "ombra", "lun"])
    if k == "fuso":
        c, d, h = R.choice([("New York", -6, 12), ("Tokyo", 8, 10), ("Mosca", 2, 9), ("Londra", -1, 15), ("Pechino", 7, 8), ("Los Angeles", -9, 18), ("Sydney", 9, 7)])
        t = (h + d) % 24
        return nq("A Roma sono le %d:00. A %s la differenza di fuso è %s%d ore. Che ora è là (in ore, da 0 a 23)?" % (h, c, "+" if d > 0 else "−", abs(d)), t,
                  [(h - d) % 24, (h + 2 * d) % 24, (t + 1) % 24, (t + 12) % 24], "", "%d %s %d = %d (ora locale)." % (h, "+" if d > 0 else "−", abs(d), t))
    if k == "fuso2":
        g = R.choice([15, 30, 45, 60, 90, 120, 75])
        return nq("Due città hanno longitudine diversa di %d°. Quante ore di differenza ci sono, più o meno, tra i loro orari solari?" % g, g / 15, [g / 24, g * 15, g / 10, 24 - g / 15], "h",
                  "La Terra ruota di 15° ogni ora: %d : 15 = %s h." % (g, num(g / 15)))
    if k == "lat":
        l = R.choice([10, 20, 30, 45, 60, 25, 40])
        return nq("Un punto ha latitudine %d° Nord. A quale altezza sull’orizzonte si vede, più o meno, la Stella Polare?" % l, l, [90 - l, l + 23, 2 * l, 90 + l if l < 0 else l + 10], "°",
                  "L’altezza della Stella Polare è uguale alla latitudine: %d°." % l)
    if k == "ombra":
        l = R.choice([40, 45, 38, 42, 37, 44])
        return nq("A mezzogiorno dell’equinozio, a quale altezza sull’orizzonte si trova il Sole a una latitudine di %d° Nord?" % l, 90 - l, [l, 90 + l, 90 - l + 23, 90 - l - 23], "°",
                  "All’equinozio il Sole è allo zenit all’equatore: altezza = 90° − %d° = %d°." % (l, 90 - l))
    l = R.choice([40, 45, 38, 42, 37, 44])
    return nq("A mezzogiorno del solstizio d’estate, a quale altezza sull’orizzonte si trova il Sole a una latitudine di %d° Nord? (asse inclinato di 23,5°)" % l, 90 - l + 23.5,
              [90 - l, 90 - l - 23.5, l + 23.5, 90 - 23.5], "°", "Altezza = 90° − %d° + 23,5° = %s°." % (l, num(90 - l + 23.5)))


def UNITS(grade):
    return [
        H("FI", "grandezze-e-misure", "Grandezze fisiche, misure ed errori", "Grandezze e misure",
          "Lo studente conosce le grandezze del Sistema Internazionale, usa la notazione scientifica e le cifre significative, stima l’errore assoluto e relativo e rappresenta i dati.",
          "grandezze fondamentali e derivate, SI, multipli e sottomultipli, notazione scientifica, ordine di grandezza, cifre significative, errore assoluto e relativo, errori casuali e sistematici",
          "Ogni misura ha un valore e un errore", "Si scrive (valore medio ± errore) unità di misura.",
          ["Le grandezze fondamentali del SI sono sette (lunghezza, massa, tempo, temperatura, corrente, quantità di sostanza, intensità luminosa); le altre sono derivate.",
           "La notazione scientifica scrive un numero come a × 10ⁿ con 1 ≤ a < 10.", "L’errore assoluto è la semidispersione; l’errore relativo è errore : valore medio."],
          [("Quanto vale l’errore relativo di (20,0 ± 0,5) cm?", ["εr = 0,5 : 20,0.", "0,025 × 100 = 2,5 %."], "2,5 %.")],
          [("Più cifre si scrivono, più la misura è precisa.", "Le cifre significative devono rispecchiare la sensibilità dello strumento."), ("Gli errori sistematici si eliminano ripetendo la misura.", "Si eliminano correggendo lo strumento o il metodo; ripetere riduce quelli casuali.")],
          [("Che cos’è la sensibilità di uno strumento?", "La più piccola variazione che lo strumento riesce a misurare."), ("Che cos’è l’ordine di grandezza?", "La potenza di 10 più vicina al numero.")],
          [("Prefissi", [("kilo", "10³"), ("mega", "10⁶"), ("giga", "10⁹"), ("milli", "10⁻³"), ("micro", "10⁻⁶"), ("nano", "10⁻⁹"), ("centi", "10⁻²"), ("deci", "10⁻¹"), ("etto", "10²")],
            "Quale potenza di 10 indica il prefisso {k}?", "Quale prefisso indica {v}?"),
           ("Concetti", [("grandezza fondamentale", "definita da un campione, come il metro"), ("grandezza derivata", "ottenuta da altre grandezze, come la velocità"), ("errore casuale", "varia a caso a ogni misura"),
                         ("errore sistematico", "sposta tutte le misure nello stesso verso"), ("sensibilità", "la più piccola variazione misurabile"), ("portata", "il valore massimo che lo strumento misura"),
                         ("errore relativo", "errore assoluto diviso valore medio"), ("cifre significative", "le cifre certe più la prima incerta")],
            "Che cos’è: {k}?", D),
           ("Grandezze", {"le grandezze fondamentali del SI": ["lunghezza", "massa", "tempo", "temperatura", "intensità di corrente", "quantità di sostanza"],
                          "le grandezze derivate": ["velocità", "densità", "forza", "pressione", "area", "volume"],
                          "le grandezze vettoriali": ["spostamento", "forza peso", "accelerazione", "quantità di moto"]})],
          ["Il metro è un’unità fondamentale.", "La velocità è una grandezza derivata.", "Ripetere le misure riduce gli errori casuali.", "Il prefisso micro vale 10⁻⁶.", "La forza è una grandezza vettoriale.",
           "In notazione scientifica 0,002 si scrive 2 × 10⁻³.", "L’errore relativo non ha unità di misura."],
          [("La velocità è una grandezza fondamentale.", "È derivata."), ("Il prefisso mega vale 10³.", "Vale 10⁶."), ("L’errore relativo si misura in metri.", "È un numero puro."),
           ("Ripetere elimina gli errori sistematici.", "Riduce quelli casuali."), ("La massa è un vettore.", "È uno scalare.")],
          "le misure", "working-scientifically", calc=f_misure),

        H("FI", "vettori-e-forze", "Vettori e forze", "Vettori e forze",
          "Lo studente distingue grandezze scalari e vettoriali, somma vettori con la regola del parallelogramma, scompone le forze e studia forza peso, forza elastica (legge di Hooke) e attrito.",
          "scalari e vettori, modulo, direzione, verso, somma di vettori, regola del parallelogramma, scomposizione, forza peso, legge di Hooke, attrito statico e dinamico",
          "Le forze si sommano come vettori", "Legge di Hooke: F = k x. Attrito: F = μ × forza premente.",
          ["Un vettore ha modulo, direzione e verso. Due forze si sommano con la regola del parallelogramma.", "La forza peso è P = m g; la forza elastica è F = k x (legge di Hooke).",
           "L’attrito statico massimo è F = μs × forza premente; quello dinamico è un po’ minore."],
          [("Due forze perpendicolari di 6 N e 8 N. Quanto vale la risultante?", ["Si usa il teorema di Pitagora.", "√(36 + 64) = 10."], "10 N.")],
          [("Le forze si sommano sempre come numeri.", "Solo se hanno la stessa direzione e lo stesso verso."), ("L’attrito dipende dall’area di contatto.", "In prima approssimazione dipende dalla forza premente e dai materiali.")],
          [("Che cosa indica la costante elastica?", "Quanto è rigida una molla: più è grande, più forza serve per allungarla."), ("Perché è più facile far scivolare una cassa già in moto?", "L’attrito dinamico è minore di quello statico.")],
          [("Scalari e vettori", [("massa", "scalare"), ("tempo", "scalare"), ("temperatura", "scalare"), ("energia", "scalare"), ("volume", "scalare"), ("forza", "vettore"),
                                  ("velocità", "vettore"), ("spostamento", "vettore"), ("accelerazione", "vettore"), ("peso", "vettore")],
            "Questa grandezza è scalare o vettoriale: {k}?", None, ("adimensionale", "derivata solo dal tempo")),
           ("Forze", [("forza peso", "attrazione gravitazionale della Terra"), ("forza elastica", "proporzionale all’allungamento della molla"), ("attrito statico", "impedisce a un corpo fermo di scivolare"),
                      ("attrito dinamico", "si oppone a un corpo che scivola"), ("reazione vincolare", "forza di un piano che sostiene un corpo"), ("tensione", "forza trasmessa da una fune"),
                      ("forza risultante", "somma vettoriale di tutte le forze")],
            "Che cos’è: {k}?", D),
           ("Caratteristiche", {"le caratteristiche di un vettore": ["modulo", "direzione", "verso", "punto di applicazione"], "gli strumenti per misurare le forze": ["dinamometro", "bilancia a molla", "cella di carico"],
                                "le cose da cui dipende l’attrito radente": ["forza premente", "natura delle superfici", "lisciatura delle superfici", "presenza di lubrificante"]})],
          ["La forza è un vettore.", "P = m g.", "F = k x è la legge di Hooke.", "L’attrito dinamico è minore di quello statico.", "La massa è uno scalare.", "Il dinamometro misura le forze.",
           "Due forze opposte si sottraggono."],
          [("La temperatura è un vettore.", "È uno scalare."), ("Due forze si sommano sempre come numeri.", "Si sommano come vettori."), ("La legge di Hooke è F = k : x.", "È F = k x."),
           ("L’attrito statico è sempre minore di quello dinamico.", "È maggiore."), ("Il peso non dipende da g.", "P = m g.")],
          "vettori e forze", "forces-and-motion", calc=f_forze),

        H("FI", "equilibrio-dei-solidi", "L’equilibrio dei solidi", "Equilibrio dei solidi",
          "Lo studente studia l’equilibrio del punto materiale e del corpo rigido, il momento di una forza, le leve, il piano inclinato e il baricentro.",
          "punto materiale, corpo rigido, equilibrio, momento di una forza, coppia, leve, piano inclinato, baricentro, equilibrio stabile, instabile, indifferente",
          "Equilibrio: forze e momenti nulli", "M = F × b; sul piano inclinato serve F = P × h : l.",
          ["Un punto materiale è in equilibrio se la somma delle forze è zero.", "Un corpo rigido è in equilibrio se sono nulle anche la somma dei momenti: M = F × b (braccio).",
           "Sul piano inclinato liscio la forza per l’equilibrio è F = P × h : l = P sen α."],
          [("Su una rampa liscia alta 1 m e lunga 4 m, quale forza tiene ferma una cassa da 400 N?", ["F = P × h : l.", "400 × 1 : 4 = 100."], "100 N.")],
          [("Il momento dipende solo dalla forza.", "Dipende anche dal braccio."), ("Il baricentro è sempre al centro geometrico.", "Coincide con il centro solo nei corpi omogenei e simmetrici.")],
          [("Perché le maniglie sono lontane dai cardini?", "Con un braccio grande basta una forza piccola per avere lo stesso momento."), ("Quando un corpo appoggiato è in equilibrio?", "Quando la verticale del baricentro cade nella base d’appoggio.")],
          [("Concetti", [("momento di una forza", "prodotto della forza per il braccio"), ("braccio", "distanza della retta della forza dal punto di rotazione"), ("coppia di forze", "due forze uguali e opposte su rette diverse"),
                         ("baricentro", "punto di applicazione del peso"), ("corpo rigido", "corpo che non si deforma"), ("equilibrio stabile", "il corpo spostato torna nella posizione iniziale"),
                         ("equilibrio instabile", "il corpo spostato si allontana"), ("base d’appoggio", "poligono formato dai punti di appoggio")],
            "Che cos’è: {k}?", D),
           ("Leve", [("forbici", "primo genere"), ("tenaglia", "primo genere"), ("altalena a bilico", "primo genere"), ("carriola", "secondo genere"), ("schiaccianoci", "secondo genere"),
                     ("remo", "secondo genere"), ("pinzetta", "terzo genere"), ("braccio umano", "terzo genere"), ("canna da pesca", "terzo genere")],
            "Di che genere è questa leva: {k}?", None, ("quarto genere",)),
           ("Equilibrio", {"i corpi in equilibrio stabile": ["pendolo fermo", "lampadario appeso", "pallina in fondo a una ciotola", "bilancia a riposo"],
                           "i corpi in equilibrio instabile": ["matita in piedi sulla punta", "pallina in cima a una cupola", "bastone in equilibrio sul dito", "moneta in piedi"],
                           "i corpi in equilibrio indifferente": ["pallina su un tavolo piano", "ruota su un asse centrale", "cilindro sdraiato sul piano", "sfera omogenea appoggiata"]})],
          ["M = F × b.", "La carriola è una leva di secondo genere.", "Un lampadario appeso è in equilibrio stabile.", "Sul piano inclinato liscio F = P × h : l.", "Il momento si misura in N·m.",
           "Una coppia di forze fa ruotare.", "Il baricentro di un anello è fuori dal materiale."],
          [("Il momento si misura in newton.", "Si misura in N·m."), ("Le pinzette sono di primo genere.", "Sono di terzo genere."), ("Una matita sulla punta è in equilibrio stabile.", "È instabile."),
           ("Il braccio non influisce sul momento.", "Il momento è F × b."), ("Il baricentro è sempre dentro il corpo.", "In un anello non lo è.")],
          "l’equilibrio", "forces-and-motion", calc=f_equil),

        H("FI", "equilibrio-dei-fluidi", "L’equilibrio dei fluidi", "Equilibrio dei fluidi",
          "Lo studente definisce la pressione e la applica a liquidi e gas: legge di Stevino, principio di Pascal, vasi comunicanti, principio di Archimede e pressione atmosferica.",
          "pressione, pascal, legge di Stevino, principio di Pascal, torchio idraulico, vasi comunicanti, principio di Archimede, galleggiamento, pressione atmosferica, Torricelli",
          "Stevino: p = d g h", "Spinta di Archimede: S = d V g del liquido spostato.",
          ["La pressione è p = F : S, in pascal. Nei liquidi cresce con la profondità: p = d g h (Stevino).",
           "Pascal: una pressione applicata a un liquido si trasmette uguale in ogni punto. Così funziona il torchio idraulico.",
           "Archimede: un corpo immerso riceve una spinta verso l’alto uguale al peso del liquido spostato. La pressione atmosferica al livello del mare è circa 101 300 Pa."],
          [("Un cubo di legno (600 kg/m³) galleggia in acqua. Quale frazione è immersa?", ["La frazione immersa è dcorpo : dliquido.", "600 : 1000."], "Il 60 %.")],
          [("La spinta di Archimede dipende dalla densità del corpo.", "Dipende dalla densità del liquido e dal volume immerso."), ("La pressione in un liquido dipende dalla forma del recipiente.", "Dipende solo dalla profondità (paradosso idrostatico).")],
          [("Perché in quota le orecchie si tappano?", "La pressione esterna diminuisce."), ("Come fa un sottomarino a immergersi?", "Riempie d’acqua i serbatoi e aumenta la sua densità media.")],
          [("Leggi", [("legge di Stevino", "la pressione cresce con la profondità"), ("principio di Pascal", "la pressione si trasmette uguale in tutto il fluido"), ("principio di Archimede", "spinta uguale al peso del fluido spostato"),
                      ("principio dei vasi comunicanti", "il liquido si porta allo stesso livello"), ("esperienza di Torricelli", "misura la pressione atmosferica con il mercurio"),
                      ("paradosso idrostatico", "la pressione sul fondo non dipende dalla forma del recipiente"), ("legge di Boyle", "a temperatura costante p × V è costante")],
            "Che cosa afferma: {k}?", D),
           ("Unità e valori", [("1 atmosfera", "circa 101 300 Pa"), ("1 bar", "100 000 Pa"), ("1 mmHg", "circa 133 Pa"), ("1 hPa", "100 Pa"), ("760 mmHg", "1 atmosfera"),
                               ("densità dell’acqua", "1000 kg/m³"), ("densità dell’acqua di mare", "circa 1030 kg/m³"), ("densità del mercurio", "13 600 kg/m³")],
            "Quanto vale: {k}?", "A che cosa corrisponde: {v}?"),
           ("Applicazioni", {"le applicazioni del principio di Pascal": ["torchio idraulico", "freni dell’auto", "martinetto idraulico", "poltrona del dentista"],
                             "le applicazioni del principio di Archimede": ["galleggiamento delle navi", "sottomarino", "mongolfiera", "densimetro", "salvagente"],
                             "le applicazioni dei vasi comunicanti": ["livella ad acqua", "acquedotto", "serbatoio sul tetto", "annaffiatoio", "fontana"]})],
          ["p = d g h.", "La pressione si misura in pascal.", "Un corpo galleggia se è meno denso del liquido.", "I freni dell’auto usano il principio di Pascal.", "1 atm vale circa 101 300 Pa.",
           "La spinta di Archimede è verso l’alto.", "Torricelli misurò la pressione atmosferica."],
          [("La pressione diminuisce con la profondità.", "Aumenta."), ("La spinta di Archimede è verso il basso.", "È verso l’alto."), ("1 bar vale 1 Pa.", "Vale 100 000 Pa."),
           ("Un corpo più denso del liquido galleggia.", "Affonda."), ("La pressione dipende dalla forma del recipiente.", "Dipende solo dalla profondità.")],
          "i fluidi", "forces-and-motion", calc=f_fluidi),

        H("CH", "materia-miscugli-e-sostanze", "La materia: stati, miscugli e sostanze pure", "Miscugli e sostanze",
          "Lo studente descrive gli stati della materia con il modello particellare, i passaggi di stato e le curve di riscaldamento, distingue miscugli e sostanze pure e le tecniche di separazione.",
          "stati di aggregazione, modello particellare, passaggi di stato, curva di riscaldamento, sosta termica, miscugli omogenei ed eterogenei, sostanze pure, elementi, composti, separazione",
          "Sostanze pure e miscugli", "Una sostanza pura ha temperatura di fusione ed ebollizione fisse.",
          ["Nei solidi le particelle sono ordinate e vicine; nei liquidi scorrono; nei gas sono lontane e veloci.", "Durante un passaggio di stato la temperatura resta costante (sosta termica): l’energia serve a rompere i legami.",
           "Un miscuglio può essere omogeneo (soluzione) o eterogeneo; le sostanze pure sono elementi o composti."],
          [("L’acqua di rubinetto è una sostanza pura?", ["Contiene sali disciolti.", "Bolle a una temperatura un po’ diversa da 100 °C."], "No, è un miscuglio omogeneo.")],
          [("In una sosta termica non si fornisce calore.", "Si fornisce calore, ma serve a cambiare stato."), ("Una lega metallica è una sostanza pura.", "È un miscuglio omogeneo solido.")],
          [("Come si separa l’alcol dall’acqua?", "Con la distillazione, perché bollono a temperature diverse."), ("Che cos’è un’emulsione?", "Un miscuglio eterogeneo di due liquidi, come la maionese.")],
          [("Tipi di miscuglio", [("acqua salata", "soluzione"), ("aria", "soluzione gassosa"), ("acciaio", "lega"), ("bronzo", "lega"), ("latte", "colloide"), ("nebbia", "aerosol"),
                                  ("maionese", "emulsione"), ("acqua e sabbia", "sospensione"), ("fumo", "aerosol"), ("panna montata", "schiuma")],
            "Che tipo di miscuglio è: {k}?", None),
           ("Separazione", [("filtrazione", "separa un solido non disciolto da un liquido"), ("distillazione", "separa liquidi con temperature di ebollizione diverse"), ("cromatografia", "separa i pigmenti di un inchiostro"),
                            ("centrifugazione", "separa per densità facendo ruotare velocemente"), ("decantazione", "lascia depositare il solido sul fondo"), ("cristallizzazione", "recupera un solido disciolto facendo evaporare il solvente"),
                            ("imbuto separatore", "separa liquidi che non si mescolano"), ("separazione magnetica", "separa il ferro con una calamita")],
            "Che cosa fa: {k}?", "Quale tecnica {v}?"),
           ("Sostanze", {"gli elementi": ["ossigeno", "ferro", "elio", "mercurio", "carbonio"], "i composti": ["acqua", "cloruro di sodio", "anidride carbonica", "glucosio", "ammoniaca"],
                         "i miscugli omogenei": ["aria", "acqua di mare", "acciaio", "vino", "ottone"]})],
          ["Durante la fusione la temperatura resta costante.", "L’acqua è un composto.", "L’aria è un miscuglio omogeneo.", "La distillazione separa liquidi con diversa temperatura di ebollizione.",
           "L’acciaio è una lega.", "Nei gas le particelle sono lontane.", "Una sostanza pura ha punto di fusione definito."],
          [("L’acqua è un elemento.", "È un composto."), ("Durante la fusione la temperatura sale.", "Resta costante."), ("L’acciaio è una sostanza pura.", "È una lega."),
           ("La filtrazione separa il sale dall’acqua.", "Il sale disciolto passa nel filtro."), ("Nei solidi le particelle sono disordinate.", "Sono ordinate.")],
          "la materia", "matter", calc=f_chim),

        H("CH", "leggi-ponderali-e-teoria-atomica", "Leggi ponderali e teoria atomica di Dalton", "Leggi ponderali",
          "Lo studente applica le leggi di Lavoisier, Proust e Dalton, descrive la teoria atomica di Dalton e il passaggio da atomi a molecole e formule.",
          "legge di Lavoisier, legge di Proust, legge di Dalton, proporzioni definite e multiple, teoria atomica, atomi, molecole, formule, Avogadro",
          "Lavoisier, Proust e Dalton", "In un composto gli elementi stanno sempre nello stesso rapporto in massa.",
          ["Lavoisier: in una reazione la massa totale si conserva.", "Proust: un composto contiene sempre gli stessi elementi nello stesso rapporto in massa (acqua: 1 g H ogni 8 g O).",
           "Dalton: la materia è fatta di atomi indivisibili; gli atomi di un elemento sono uguali tra loro e si combinano in rapporti semplici."],
          [("Nel solfuro di ferro Fe:S = 7:4. Quanti g di zolfo reagiscono con 14 g di ferro?", ["14 : 7 = 2.", "2 × 4 = 8."], "8 g.")],
          [("Se metto più ossigeno ottengo più acqua.", "L’ossigeno in eccesso resta: il rapporto è fisso."), ("Dalton sapeva che l’atomo è divisibile.", "Per Dalton l’atomo era indivisibile.")],
          [("Che cosa dice la legge di Dalton delle proporzioni multiple?", "Se due elementi formano più composti, le masse di uno che si combinano con la stessa massa dell’altro stanno in rapporti semplici."),
           ("Che cosa propose Avogadro?", "Volumi uguali di gas, a parità di pressione e temperatura, contengono lo stesso numero di molecole.")],
          [("Scienziati e leggi", [("Lavoisier", "conservazione della massa"), ("Proust", "proporzioni definite"), ("Dalton", "teoria atomica e proporzioni multiple"), ("Avogadro", "volumi uguali, ugual numero di molecole"),
                                   ("Gay-Lussac", "rapporti semplici tra i volumi dei gas"), ("Democrito", "prima idea di atomo nell’antichità"), ("Cannizzaro", "masse atomiche relative")],
            "A quale idea è legato: {k}?", "Chi è legato a: {v}?"),
           ("Formule", [("H₂O", "2 atomi di idrogeno e 1 di ossigeno"), ("CO₂", "1 atomo di carbonio e 2 di ossigeno"), ("NH₃", "1 atomo di azoto e 3 di idrogeno"), ("CH₄", "1 atomo di carbonio e 4 di idrogeno"),
                        ("O₃", "3 atomi di ossigeno"), ("H₂SO₄", "2 di idrogeno, 1 di zolfo e 4 di ossigeno"), ("NaCl", "1 di sodio e 1 di cloro"), ("C₂H₆", "2 atomi di carbonio e 6 di idrogeno")],
            "Che cosa indica la formula {k}?", "Quale formula indica {v}?"),
           ("Molecole", {"le sostanze fatte di molecole biatomiche": ["ossigeno O₂", "azoto N₂", "idrogeno H₂", "cloro Cl₂", "fluoro F₂"],
                         "i gas nobili, fatti di atomi singoli": ["elio", "neon", "argon", "kripton", "xeno"],
                         "i composti": ["acqua", "metano", "ammoniaca", "anidride carbonica", "acido solforico"]})],
          ["La massa si conserva nelle reazioni.", "Nell’acqua il rapporto H:O in massa è 1:8.", "Per Dalton gli atomi sono indivisibili.", "L’ossigeno gassoso è O₂.", "L’elio è fatto di atomi singoli.",
           "Proust enunciò la legge delle proporzioni definite.", "NH₃ contiene tre atomi di idrogeno."],
          [("In una reazione la massa aumenta.", "Si conserva."), ("Il rapporto tra gli elementi in un composto cambia.", "È sempre lo stesso."), ("Lavoisier propose la teoria atomica.", "La propose Dalton."),
           ("L’ossigeno gassoso è O.", "È O₂."), ("CO₂ ha due atomi di carbonio.", "Ha un carbonio e due ossigeni.")],
          "le leggi ponderali", "matter", calc=f_chim),

        H("BI", "caratteristiche-dei-viventi", "Le caratteristiche dei viventi e le biomolecole", "I viventi e le biomolecole",
          "Lo studente descrive le caratteristiche comuni dei viventi, i livelli di organizzazione, l’acqua e le biomolecole: carboidrati, lipidi, proteine e acidi nucleici.",
          "caratteristiche dei viventi, omeostasi, metabolismo, livelli di organizzazione, acqua, legame idrogeno, carboidrati, lipidi, proteine, amminoacidi, enzimi, acidi nucleici",
          "Carboidrati, lipidi, proteine e acidi nucleici", "Le proteine sono catene di amminoacidi; il DNA è fatto di nucleotidi.",
          ["I viventi sono fatti di cellule, hanno un metabolismo, mantengono l’omeostasi, crescono, si riproducono e rispondono agli stimoli.",
           "L’acqua è polare e forma legami a idrogeno: per questo è un ottimo solvente.", "Le biomolecole sono carboidrati (energia), lipidi (riserva e membrane), proteine (struttura ed enzimi) e acidi nucleici (informazione)."],
          [("Di che monomeri è fatto l’amido?", ["L’amido è un polisaccaride.", "È una catena di glucosio."], "Di glucosio.")],
          [("Gli enzimi si consumano nella reazione.", "Gli enzimi accelerano le reazioni e restano invariati."), ("I grassi servono solo come riserva.", "I fosfolipidi formano anche le membrane.")],
          [("Perché il ghiaccio galleggia?", "Per i legami a idrogeno l’acqua solida è meno densa di quella liquida."), ("Che cos’è l’omeostasi?", "La capacità di mantenere costanti le condizioni interne.")],
          [("Biomolecole", [("glucosio", "carboidrati"), ("amido", "carboidrati"), ("cellulosa", "carboidrati"), ("glicogeno", "carboidrati"), ("trigliceridi", "lipidi"), ("colesterolo", "lipidi"),
                            ("fosfolipidi", "lipidi"), ("emoglobina", "proteine"), ("collagene", "proteine"), ("amilasi", "proteine"), ("DNA", "acidi nucleici"), ("RNA", "acidi nucleici")],
            "A quale classe di biomolecole appartiene: {k}?", None),
           ("Monomeri", [("proteine", "amminoacidi"), ("amido", "glucosio"), ("acidi nucleici", "nucleotidi"), ("trigliceridi", "glicerolo e acidi grassi"), ("cellulosa", "glucosio legato in modo diverso"),
                         ("saccarosio", "glucosio e fruttosio"), ("lattosio", "glucosio e galattosio")],
            "Da quali unità è formato: {k}?", "Che cosa è formato da {v}?"),
           ("Funzioni", {"le biomolecole che danno energia rapida": ["glucosio", "saccarosio", "fruttosio", "glicogeno", "amido"], "le biomolecole con funzione strutturale": ["collagene", "cheratina", "cellulosa", "chitina", "fosfolipidi"],
                         "le caratteristiche dei viventi": ["metabolismo", "omeostasi", "riproduzione", "crescita", "risposta agli stimoli"]})],
          ["Le proteine sono fatte di amminoacidi.", "L’amido è un polimero del glucosio.", "Gli enzimi sono proteine.", "L’acqua è una molecola polare.", "Il DNA è un acido nucleico.",
           "I fosfolipidi formano le membrane.", "I viventi mantengono l’omeostasi."],
          [("Le proteine sono fatte di glucosio.", "Sono fatte di amminoacidi."), ("Gli enzimi si consumano.", "Restano invariati."), ("L’acqua è apolare.", "È polare."), ("La cellulosa è una proteina.", "È un carboidrato."),
           ("Il DNA è un lipide.", "È un acido nucleico.")],
          "i viventi e le biomolecole", "living-things-and-ecosystems"),

        H("ST", "la-terra-nel-sistema-solare", "La Terra nel Sistema solare: forma e moti", "La Terra e i suoi moti",
          "Lo studente descrive la forma della Terra, il reticolato geografico, le coordinate, i moti di rotazione e rivoluzione e le loro conseguenze, i fusi orari e la Luna.",
          "geoide, reticolato geografico, latitudine, longitudine, meridiano di Greenwich, rotazione, rivoluzione, equinozi, solstizi, fusi orari, Luna, eclissi, maree",
          "Latitudine, longitudine e fusi orari", "Ogni 15° di longitudine l’ora cambia di 1 ora.",
          ["La Terra ha la forma di un geoide, schiacciata ai poli. Latitudine e longitudine individuano ogni punto.", "La rotazione (circa 24 h) causa il dì e la notte e i fusi orari: 360° : 24 = 15° ogni ora.",
           "La rivoluzione con l’asse inclinato di 23,5° causa le stagioni: equinozi (21 marzo, 23 settembre) e solstizi (21 giugno, 22 dicembre)."],
          [("Quante ore di differenza ci sono tra due città separate da 45° di longitudine?", ["La Terra ruota di 15° ogni ora.", "45 : 15 = 3."], "3 ore.")],
          [("All’equatore la latitudine è 90°.", "È 0°; ai poli è 90°."), ("Le stagioni dipendono dalla distanza dal Sole.", "Dipendono dall’inclinazione dell’asse.")],
          [("Perché si vede sempre la stessa faccia della Luna?", "La Luna ruota su sé stessa nello stesso tempo in cui gira intorno alla Terra."), ("Che cos’è la forza di Coriolis?", "L’effetto della rotazione terrestre che devia venti e correnti.")],
          [("Concetti", [("latitudine", "distanza angolare dall’equatore"), ("longitudine", "distanza angolare dal meridiano di Greenwich"), ("meridiano", "semicerchio che va da polo a polo"),
                         ("parallelo", "cerchio parallelo all’equatore"), ("geoide", "forma reale della Terra"), ("solstizio", "giorno con il dì più lungo o più corto"), ("equinozio", "giorno con dì e notte uguali"),
                         ("perielio", "punto dell’orbita più vicino al Sole")],
            "Che cos’è: {k}?", D),
           ("Paralleli e date", [("equatore", "0° di latitudine"), ("tropico del Cancro", "23,5° Nord"), ("tropico del Capricorno", "23,5° Sud"), ("circolo polare artico", "66,5° Nord"),
                                 ("circolo polare antartico", "66,5° Sud"), ("polo Nord", "90° Nord"), ("meridiano di Greenwich", "0° di longitudine"), ("linea del cambiamento di data", "circa 180° di longitudine")],
            "Dove si trova: {k}?", "Che cosa si trova a {v}?"),
           ("Moti", {"le conseguenze della rotazione": ["dì e notte", "fusi orari", "schiacciamento ai poli", "deviazione dei venti"], "le conseguenze della rivoluzione con l’asse inclinato": ["stagioni", "diversa durata del dì nell’anno", "zone astronomiche", "sole di mezzanotte ai poli"],
                     "i fenomeni dovuti alla Luna": ["maree", "eclissi di Sole", "fasi lunari", "rallentamento della rotazione terrestre"]})],
          ["Ogni 15° di longitudine l’ora cambia di un’ora.", "All’equatore la latitudine è 0°.", "L’asse terrestre è inclinato di 23,5°.", "La rotazione causa il dì e la notte.",
           "Le stagioni dipendono dall’inclinazione dell’asse.", "La Luna causa le maree.", "La Terra è schiacciata ai poli."],
          [("All’equatore la latitudine è 90°.", "È 0°."), ("Le stagioni dipendono dalla distanza dal Sole.", "Dipendono dall’asse inclinato."), ("Ogni 30° l’ora cambia di un’ora.", "Ogni 15°."),
           ("La Terra è una sfera perfetta.", "È un geoide."), ("La rivoluzione dura 24 ore.", "Dura un anno.")],
          "la Terra", "earth-and-space", calc=f_terra),

        H("ST", "idrosfera-e-atmosfera", "Idrosfera e atmosfera", "Idrosfera e atmosfera",
          "Lo studente descrive le acque marine e continentali, il ciclo dell’acqua, la composizione e la struttura dell’atmosfera, la pressione, i venti, l’umidità e l’effetto serra.",
          "idrosfera, salinità, correnti, onde, maree, fiumi, laghi, falde, atmosfera, troposfera, stratosfera, ozono, pressione, venti, umidità, nubi, effetto serra",
          "L’aria si muove dalle alte alle basse pressioni", "Il vento soffia dall’anticiclone verso il ciclone.",
          ["Il 97 % dell’acqua è negli oceani (salinità media 35 ‰); l’acqua dolce è soprattutto nei ghiacciai.", "L’atmosfera è divisa in troposfera, stratosfera (con l’ozono), mesosfera, termosfera ed esosfera.",
           "Il vento va dalle alte pressioni (anticicloni) alle basse (cicloni). L’effetto serra naturale mantiene la Terra a circa 15 °C."],
          [("Che vento c’è di giorno sulla costa?", ["La terra si scalda più del mare.", "Sulla terra l’aria sale e la pressione cala."], "La brezza di mare, dal mare verso la terra.")],
          [("L’effetto serra è solo dannoso.", "Quello naturale rende la Terra abitabile; il problema è il suo aumento."), ("Salendo in montagna la temperatura sale.", "Nella troposfera cala di circa 6,5 °C ogni km.")],
          [("Che cos’è l’umidità relativa?", "Il rapporto tra il vapore presente e il massimo che l’aria può contenere a quella temperatura."), ("Perché il mare è salato?", "Le acque portano al mare i sali delle rocce e l’evaporazione li concentra.")],
          [("Strati", [("troposfera", "temperatura che cala con la quota e fenomeni meteo"), ("stratosfera", "strato di ozono che assorbe gli ultravioletti"), ("mesosfera", "le meteore bruciano"),
                       ("termosfera", "aurore polari e temperature altissime"), ("esosfera", "passaggio graduale allo spazio"), ("tropopausa", "limite tra troposfera e stratosfera")],
            "Che cosa caratterizza: {k}?", "Quale strato ha {v}?", ("nucleo esterno",)),
           ("Fenomeni", [("brezza di mare", "di giorno, dal mare verso la terra"), ("brezza di terra", "di notte, dalla terra verso il mare"), ("anticiclone", "zona di alta pressione con tempo stabile"),
                         ("ciclone", "zona di bassa pressione con nubi e piogge"), ("monsone", "vento stagionale che cambia direzione"), ("rugiada", "vapore che condensa al suolo di notte"),
                         ("corrente del Golfo", "corrente calda dell’Atlantico"), ("marea", "innalzamento e abbassamento periodico del mare")],
            "Che cos’è: {k}?", D),
           ("Acque e gas", {"i gas serra": ["anidride carbonica", "metano", "vapore acqueo", "protossido di azoto", "ozono troposferico"],
                            "le acque continentali": ["fiumi", "laghi", "falde acquifere", "ghiacciai", "paludi"],
                            "gli strumenti della meteorologia": ["barometro", "igrometro", "anemometro", "pluviometro", "radiosonda"]})],
          ["Il vento va dalle alte alle basse pressioni.", "L’ozono è nella stratosfera.", "La salinità media del mare è 35 per mille.", "La troposfera si raffredda salendo.", "L’effetto serra naturale rende la Terra abitabile.",
           "Il barometro misura la pressione.", "Di giorno soffia la brezza di mare."],
          [("Il vento va dalle basse alle alte pressioni.", "Va dalle alte alle basse."), ("L’ozono è nella troposfera.", "Lo strato di ozono è nella stratosfera."), ("Di notte soffia la brezza di mare.", "Di notte soffia la brezza di terra."),
           ("Salendo nella troposfera fa più caldo.", "Fa più freddo."), ("L’effetto serra non esiste in natura.", "Esiste ed è necessario.")],
          "l’idrosfera e l’atmosfera", "earths-systems"),
    ]
