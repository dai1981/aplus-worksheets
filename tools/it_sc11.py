# -*- coding: utf-8 -*-
"""Italia / Liceo scientifico: terza liceo（Fisica e Scienze naturali, secondo biennio）"""
import math
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"
G = 9.8
GU = 6.67e-11


def f_en(R):
    k = R.choice(["lav", "lavang", "ec", "ep", "cons", "pot", "molla"])
    if k == "lav":
        f, s = R.choice([(50, 12), (120, 5), (35, 20), (300, 2.5), (80, 15), (15, 40)])
        return nq("Una forza costante di %d N sposta un corpo di %s m nella sua stessa direzione. Quanto lavoro compie?" % (f, num(s)), f * s, [f / s, f + s, f * s / 2, s / f], "J",
                  "L = F s = %d × %s = %s J." % (f, num(s), num(f * s)))
    if k == "lavang":
        f, s, a, c = R.choice([(100, 10, 60, 0.5), (40, 5, 60, 0.5), (200, 3, 60, 0.5), (50, 8, 90, 0), (80, 6, 60, 0.5), (30, 20, 60, 0.5)])
        if c == 0:
            return it("Una forza di %d N forma un angolo di 90° con lo spostamento di %d m. Quanto lavoro compie?" % (f, s), "0 J", ["%d J" % (f * s), "%d J" % (f * s // 2), "%d J" % f],
                      "L = F s cos 90° = 0: una forza perpendicolare allo spostamento non compie lavoro.")
        return nq("Tiri un carrello con %d N lungo una fune inclinata di %d° rispetto allo spostamento di %d m. Quanto lavoro compi?" % (f, a, s), f * s * c, [f * s, f * s * math.sqrt(3) / 2, f * c, f * s * 2], "J",
                  "L = F s cos α = %d × %d × 0,5 = %s J." % (f, s, num(f * s * c)))
    if k == "ec":
        m, v = R.choice([(1000, 20), (0.06, 30), (70, 8), (2, 15), (1500, 25), (0.5, 40)])
        return nq("Quanto vale l’energia cinetica di una massa di %s kg a %s m/s?" % (num(m), num(v)), 0.5 * m * v * v, [m * v, m * v * v, 0.5 * m * v, 0.25 * m * v * v], "J",
                  "Ec = ½ m v² = 0,5 × %s × %s² = %s J." % (num(m), num(v), num(0.5 * m * v * v)))
    if k == "ep":
        m, h = R.choice([(60, 12), (2, 30), (1000, 50), (0.5, 8), (75, 3), (5, 100)])
        return nq("Quanta energia potenziale gravitazionale acquista una massa di %s kg sollevata di %s m? (g = 9,8 m/s²)" % (num(m), num(h)), m * G * h, [m * h, m * G, m * G * h / 2, G * h], "J",
                  "U = m g h = %s × 9,8 × %s = %s J." % (num(m), num(h), num(m * G * h)))
    if k == "cons":
        h = R.choice([5, 20, 45, 10, 2, 80, 1.25])
        return nq("Un corpo cade da fermo da %s m senza attrito. Con che velocità arriva a terra? (g = 9,8 m/s²)" % num(h), math.sqrt(2 * G * h), [2 * G * h, math.sqrt(G * h), G * h, math.sqrt(2 * h)], "m/s",
                  "m g h = ½ m v² → v = √(2 g h) = √(2 × 9,8 × %s) = %s m/s." % (num(h), num(math.sqrt(2 * G * h))))
    if k == "pot":
        m, h, t = R.choice([(80, 10, 20), (500, 12, 30), (60, 4, 8), (1000, 20, 40), (200, 15, 10), (50, 6, 12)])
        return nq("Un montacarichi solleva %d kg di %d m in %d s. Quale potenza media sviluppa? (g = 9,8 m/s²)" % (m, h, t), m * G * h / t, [m * G * h, m * h / t, m * G * h * t, m * G / t], "W",
                  "P = L : t = m g h : t = %s : %d = %s W." % (num(m * G * h), t, num(m * G * h / t)))
    kk, x = R.choice([(200, 0.1), (500, 0.04), (1000, 0.05), (80, 0.25), (300, 0.2), (50, 0.3)])
    return nq("Una molla di costante %d N/m è compressa di %s m. Quanta energia potenziale elastica immagazzina?" % (kk, num(x)), 0.5 * kk * x * x, [kk * x, kk * x * x, 0.5 * kk * x, kk * x * x * 2], "J",
              "U = ½ k x² = 0,5 × %d × %s² = %s J." % (kk, num(x), num(0.5 * kk * x * x)))


def f_qm(R):
    k = R.choice(["p", "imp", "anel", "rinc", "f", "el"])
    if k == "p":
        m, v = R.choice([(0.16, 25), (1200, 15), (70, 6), (0.05, 300), (2000, 10), (0.43, 20)])
        return nq("Quanto vale la quantità di moto di una massa di %s kg a %s m/s?" % (num(m), num(v)), m * v, [m / v, 0.5 * m * v * v, m * v * v, v / m], "kg·m/s",
                  "p = m v = %s × %s = %s kg·m/s." % (num(m), num(v), num(m * v)))
    if k == "imp":
        f, t = R.choice([(2000, 0.01), (500, 0.02), (1200, 0.05), (300, 0.1), (8000, 0.005), (150, 0.2)])
        return nq("Una forza media di %s N agisce per %s s. Quanto vale l’impulso?" % (num(f), num(t)), f * t, [f / t, t / f, f * t * 10, f], "N·s", "I = F Δt = %s × %s = %s N·s." % (num(f), num(t), num(f * t)))
    if k == "anel":
        m1, v1, m2 = R.choice([(1000, 20, 1000), (2, 6, 1), (1200, 15, 800), (3, 4, 1), (5, 10, 5), (60, 4, 20)])
        v = m1 * v1 / (m1 + m2)
        return nq("Un carrello di %d kg a %d m/s urta un carrello fermo di %d kg e restano attaccati. Con che velocità si muovono?" % (m1, v1, m2), v, [v1, v1 / 2 if abs(v - v1 / 2) > 0.01 else v1 / 3, m2 * v1 / (m1 + m2) if m1 != m2 else v1 * 2, v1 * m1 / m2],
                  "m/s", "Si conserva la quantità di moto: v = m₁ v₁ : (m₁ + m₂) = %s m/s." % num(v))
    if k == "rinc":
        mp, vp, mf = R.choice([(0.01, 400, 4), (0.02, 300, 5), (0.005, 800, 2), (0.05, 200, 10), (0.015, 600, 3)])
        return nq("Un fucile di %d kg spara un proiettile di %s kg a %d m/s. Con che velocità rincula il fucile?" % (mf, num(mp), vp), mp * vp / mf, [vp, mp * vp, mf * vp, vp / mf], "m/s",
                  "0 = m_p v_p − m_f v_f → v_f = %s × %d : %d = %s m/s." % (num(mp), vp, mf, num(mp * vp / mf)))
    if k == "f":
        m, dv, t = R.choice([(0.45, 20, 0.1), (70, 15, 0.2), (1000, 20, 0.5), (0.06, 50, 0.005), (0.16, 30, 0.02)])
        return nq("Una palla di %s kg passa da 0 a %d m/s in un colpo che dura %s s. Quale forza media riceve?" % (num(m), dv, num(t)), m * dv / t, [m * dv, m * dv * t, dv / t, m / t], "N",
                  "F = Δp : Δt = %s × %d : %s = %s N." % (num(m), dv, num(t), num(m * dv / t)))
    m, v = R.choice([(2, 3), (5, 4), (1, 6), (3, 2), (4, 5)])
    return nq("Una pallina di %d kg a %d m/s urta frontalmente in modo elastico una pallina uguale ferma. Con che velocità parte la seconda?" % (m, v), v, [v / 2, 0.5 * v * v, v * 2, m * v], "m/s",
              "Con masse uguali, nell’urto elastico frontale le velocità si scambiano: %d m/s." % v)


def f_grav(R):
    k = R.choice(["f", "g", "orb", "kep", "peso"])
    if k == "f":
        m1, m2, r = R.choice([(1000, 1000, 1), (50, 60, 0.5), (5.97e24, 1000, 6.37e6), (100, 100, 2), (7.35e22, 70, 1.74e6)])
        f = GU * m1 * m2 / r ** 2
        return nq("Quanto vale la forza gravitazionale tra %s kg e %s kg a %s m di distanza? (G = 6,67 × 10⁻¹¹ N·m²/kg²)" % (num(m1), num(m2), num(r)), f,
                  [GU * m1 * m2 / r, f * 2, GU * (m1 + m2) / r ** 2, f / 100], "N", "F = G m₁ m₂ : r² = %s N." % num(f))
    if k == "g":
        pl, m, r = R.choice([("la Luna", 7.35e22, 1.74e6), ("Marte", 6.42e23, 3.39e6), ("la Terra", 5.97e24, 6.37e6), ("Giove", 1.9e27, 6.99e7), ("Mercurio", 3.3e23, 2.44e6)])
        g = GU * m / r ** 2
        return nq("Quanto vale l’accelerazione di gravità sulla superficie di %s (M = %s kg, R = %s m)?" % (pl, num(m), num(r)), g, [GU * m / r, g * 2, GU * m * r, 9.8 if abs(g - 9.8) > 0.2 else 4.9], "m/s²",
                  "g = G M : R² = %s m/s²." % num(g))
    if k == "orb":
        h = R.choice([400e3, 800e3, 2000e3, 20200e3, 35786e3])
        r = 6.37e6 + h
        v = math.sqrt(GU * 5.97e24 / r)
        return nq("Un satellite è in orbita circolare a %s km di quota. Quanto vale la sua velocità? (G M_Terra = 3,98 × 10¹⁴ m³/s², R_Terra = 6370 km)" % num(h / 1000), v,
                  [v * math.sqrt(2), math.sqrt(GU * 5.97e24 / h), v / 2, 7900 if abs(v - 7900) > 300 else 11200], "m/s", "v = √(G M : r), con r = R + h = %s m: v = %s m/s." % (num(r), num(v)))
    if k == "kep":
        a, nm = R.choice([(1.52, "Marte"), (5.2, "Giove"), (9.54, "Saturno"), (0.387, "Mercurio"), (0.723, "Venere"), (19.2, "Urano")])
        t = a ** 1.5
        return nq("%s dista dal Sole %s UA (unità astronomiche). Quanto dura il suo anno, in anni terrestri, per la terza legge di Keplero?" % (nm, num(a)), t, [a, a ** 2, a ** 3, math.sqrt(a)], "anni",
                  "T² = a³ → T = a^(3/2) = %s^(3/2) = %s anni." % (num(a), num(t)))
    m, f = R.choice([(70, 1 / 6), (60, 0.38), (80, 2.53), (50, 1 / 6), (90, 0.38)])
    pl = {1 / 6: "sulla Luna (g circa 1/6 di quello terrestre)", 0.38: "su Marte (g circa 0,38 volte quello terrestre)", 2.53: "su Giove (g circa 2,53 volte quello terrestre)"}[f]
    return nq("Quanto pesa %s una persona di %d kg? (g Terra = 9,8 m/s²)" % (pl, m), m * G * f, [m * G, m * f, m * G / f, m * G * f * 10], "N",
              "P = m g = %d × %s = %s N; la massa resta %d kg." % (m, num(G * f), num(m * G * f), m))


def f_gas(R):
    k = R.choice(["pv", "vt", "pt", "nrt", "ec", "k"])
    if k == "pv":
        p, v1, v2 = R.choice([(100, 6, 2), (200, 3, 12), (150, 4, 6), (300, 2, 5), (120, 10, 4)])
        return nq("Un gas a temperatura costante è a %d kPa in %d l. Se il volume diventa %d l, che pressione avrà?" % (p, v1, v2), p * v1 / v2, [p * v2 / v1, p, p * v1 * v2, p / v1], "kPa",
                  "Boyle: p₂ = p₁ V₁ : V₂ = %d × %d : %d = %s kPa." % (p, v1, v2, num(p * v1 / v2)))
    if k == "vt":
        v, t1, t2 = R.choice([(2, 27, 127), (3, 0, 273), (5, 27, 327), (4, 127, 27), (6, 77, 227)])
        T1, T2 = t1 + 273, t2 + 273
        return nq("A pressione costante un gas occupa %d l a %d °C. Quale volume occupa a %d °C?" % (v, t1, t2), v * T2 / T1, [v * t2 / t1 if t1 else v * 2, v * T1 / T2, v, v * (t2 - t1)], "l",
                  "Gay-Lussac con le temperature assolute: V₂ = %d × %d : %d = %s l." % (v, T2, T1, num(v * T2 / T1)))
    if k == "pt":
        p, t1, t2 = R.choice([(200, 27, 87), (100, 0, 273), (150, 27, 177), (300, 127, 327)])
        T1, T2 = t1 + 273, t2 + 273
        return nq("Una bombola rigida ha pressione %d kPa a %d °C. Che pressione avrà a %d °C?" % (p, t1, t2), p * T2 / T1, [p * T1 / T2, p * t2 / t1 if t1 else p * 3, p, p * (T2 - T1)], "kPa",
                  "A volume costante p ∝ T: p₂ = %d × %d : %d = %s kPa." % (p, T2, T1, num(p * T2 / T1)))
    if k == "nrt":
        n, t, v = R.choice([(1, 273, 0.0224), (2, 300, 0.05), (0.5, 400, 0.01), (3, 250, 0.06), (1, 300, 0.025)])
        p = n * 8.31 * t / v
        return nq("Quale pressione hanno %s mol di gas perfetto a %d K in %s m³? (R = 8,31 J/(mol·K))" % (num(n), t, num(v)), p, [n * 8.31 * t, n * 8.31 / v, p / 1000, n * t / v], "Pa",
                  "p = n R T : V = %s Pa." % num(p))
    if k == "ec":
        t = R.choice([300, 273, 400, 600, 150, 1000])
        e = 1.5 * 1.38e-23 * t
        return nq("Quanto vale l’energia cinetica media di una molecola di gas a %d K? (k_B = 1,38 × 10⁻²³ J/K)" % t, e, [1.38e-23 * t, 3 * 1.38e-23 * t, e / t, 0.5 * 1.38e-23 * t], "J",
                  "E = 3/2 k_B T = 1,5 × 1,38 × 10⁻²³ × %d = %s J." % (t, num(e)))
    c = R.choice([27, 100, -73, 0, 227, -173])
    return nq("Quanti kelvin sono %s °C?" % (("−%d" % -c) if c < 0 else str(c)), c + 273, [c, c - 273 if c > 0 else 273 - c, c + 373], "K", "T = t + 273 = %d K." % (c + 273))


def f_atomo(R):
    k = R.choice(["n", "e", "ione", "massa", "conf"])
    el = [("carbonio", "C", 6, 12), ("ossigeno", "O", 8, 16), ("sodio", "Na", 11, 23), ("cloro", "Cl", 17, 35), ("ferro", "Fe", 26, 56), ("alluminio", "Al", 13, 27),
          ("calcio", "Ca", 20, 40), ("azoto", "N", 7, 14), ("zolfo", "S", 16, 32), ("magnesio", "Mg", 12, 24)]
    nm, s, z, a = R.choice(el)
    if k == "n":
        return nq("Quanti neutroni ha un atomo di %s-%d (Z = %d)?" % (nm, a, z), a - z, [a, z, a + z, a - z + 1], "", "Neutroni = A − Z = %d − %d = %d." % (a, z, a - z))
    if k == "e":
        return nq("Quanti elettroni ha un atomo neutro di %s (Z = %d)?" % (nm, z), z, [a, a - z if a - z != z else z + 1, z * 2, z + 2], "", "In un atomo neutro gli elettroni sono uguali ai protoni: %d." % z)
    if k == "ione":
        nm, s, z, q = R.choice([("sodio", "Na⁺", 11, 1), ("magnesio", "Mg²⁺", 12, 2), ("cloro", "Cl⁻", 17, -1), ("ossigeno", "O²⁻", 8, -2), ("alluminio", "Al³⁺", 13, 3), ("calcio", "Ca²⁺", 20, 2), ("zolfo", "S²⁻", 16, -2)])
        return nq("Quanti elettroni ha lo ione %s (Z = %d)?" % (s, z), z - q, [z, z + q, z - 2 * q, z + 1 if q != -1 else z + 2], "", "Elettroni = Z − carica = %d − (−%d) = %d." % (z, -q, z - q) if q < 0 else "Elettroni = Z − carica = %d − %d = %d." % (z, q, z - q))
    if k == "massa":
        a1, p1, a2, p2, nm2 = R.choice([(35, 75, 37, 25, "cloro"), (63, 69, 65, 31, "rame"), (10, 20, 11, 80, "boro"), (24, 79, 26, 21, "magnesio"), (6, 7.5, 7, 92.5, "litio")])
        m = (a1 * p1 + a2 * p2) / 100
        return nq("Il %s ha due isotopi: massa %d (%s %%) e massa %d (%s %%). Qual è la massa atomica media?" % (nm2, a1, num(p1), a2, num(p2)), m, [(a1 + a2) / 2, a1, a2, (a1 * p2 + a2 * p1) / 100], "u",
                  "Media pesata: (%d × %s + %d × %s) : 100 = %s u." % (a1, num(p1), a2, num(p2), num(m)))
    nm, z, ve = R.choice([("sodio", 11, 1), ("magnesio", 12, 2), ("alluminio", 13, 3), ("silicio", 14, 4), ("fosforo", 15, 5), ("zolfo", 16, 6), ("cloro", 17, 7), ("ossigeno", 8, 6), ("azoto", 7, 5), ("carbonio", 6, 4)])
    return nq("Quanti elettroni di valenza ha un atomo di %s (Z = %d)?" % (nm, z), ve, [8 - ve if 8 - ve != ve else 2, z, z - 2, ve + 2 if ve < 7 else 1], "",
              "Si guarda il gruppo nella tavola periodica (o l’ultimo livello): %d elettroni di valenza." % ve)


def f_gen(R):
    k = R.choice(["mono", "test", "di", "x", "codone", "aa"])
    if k == "mono":
        p1, p2, pr, w = R.choice([("Aa", "Aa", 25, [50, 75, 100]), ("Aa", "aa", 50, [25, 75, 100]), ("AA", "aa", 0, [25, 50, 100]), ("Aa", "AA", 0, [25, 50, 75])])
        if pr == 0:
            return it("Nell’incrocio %s × %s, quale percentuale dei figli sarà aa?" % (p1, p2), "0 %", ["%d %%" % x for x in w], "Nessun figlio può ricevere due alleli a: 0 %.")
        return nq("Nell’incrocio %s × %s, quale percentuale dei figli sarà aa?" % (p1, p2), pr, w, "%", "Dal quadrato di Punnett: %d %% aa." % pr)
    if k == "test":
        return it("Un incrocio di prova (Aa × aa) dà quale rapporto fenotipico?", "1 dominante : 1 recessivo", ["3 : 1", "9 : 3 : 3 : 1", "tutti dominanti"],
                  "Metà dei figli è Aa e metà aa: rapporto 1 : 1.")
    if k == "di":
        q, a, w = R.choice([("dominanti per entrambi i caratteri", 9, [3, 1, 6]), ("recessivi per entrambi i caratteri", 1, [3, 9, 4]), ("dominanti per il primo e recessivi per il secondo", 3, [9, 1, 6])])
        return nq("Nell’incrocio AaBb × AaBb, quanti figli su 16 sono %s?" % q, a, w, "", "Rapporto 9 : 3 : 3 : 1: sono %d su 16." % a)
    if k == "x":
        q, a, w = R.choice([("Una donna portatrice di daltonismo (XᴰXᵈ) e un uomo sano (XᴰY): quale percentuale dei figli maschi sarà daltonica?", "50 %", ["25 %", "0 %", "100 %"]),
                            ("Una donna portatrice di emofilia (XᴴXʰ) e un uomo sano (XᴴY): quale percentuale delle figlie femmine sarà malata?", "0 %", ["25 %", "50 %", "100 %"]),
                            ("Un uomo daltonico (XᵈY) e una donna sana non portatrice (XᴰXᴰ): quale percentuale delle figlie sarà portatrice?", "100 %", ["0 %", "25 %", "50 %"])])
        return it(q, a, w, "Si fa il quadrato di Punnett con i cromosomi X e Y: %s." % a)
    if k == "codone":
        n = R.choice([300, 450, 900, 1200, 600, 150])
        return nq("Una proteina ha %d amminoacidi. Quanti nucleotidi ha, almeno, la parte codificante del suo mRNA (senza il codone di stop)?" % n, n * 3, [n, n / 3, n * 2, n * 4], "",
                  "Ogni amminoacido è codificato da un codone di 3 nucleotidi: %d × 3 = %d." % (n, n * 3))
    s, c = R.choice([("ATG", "UAC"), ("GCA", "CGU"), ("TTA", "AAU"), ("CGT", "GCA"), ("AAC", "UUG"), ("GGT", "CCA")])
    w = sorted({c[::-1], s.replace("T", "U"), s, "".join({"A": "T", "T": "A", "G": "C", "C": "G"}[x] for x in s)} - {c})
    return it("Il filamento stampo del DNA ha la tripletta %s. Quale codone si forma nell’mRNA?" % s, c, w[:3], "Si appaiano A–U, T–A, G–C, C–G: %s → %s." % (s, c))


def UNITS(grade):
    return [
        H("FI", "lavoro-ed-energia", "Lavoro, energia e conservazione", "Lavoro ed energia",
          "Lo studente definisce lavoro e potenza, l’energia cinetica con il teorema dell’energia cinetica, l’energia potenziale gravitazionale ed elastica, le forze conservative e la conservazione dell’energia meccanica.",
          "lavoro, prodotto scalare, potenza, energia cinetica, teorema dell’energia cinetica, energia potenziale gravitazionale ed elastica, forze conservative, conservazione dell’energia meccanica, attrito",
          "L = F s cos α", "Senza attriti l’energia meccanica Ec + U resta costante.",
          ["Il lavoro di una forza costante è L = F s cos α; è nullo se la forza è perpendicolare allo spostamento.", "Teorema dell’energia cinetica: il lavoro totale è uguale alla variazione di Ec = ½ m v².",
           "Con sole forze conservative l’energia meccanica si conserva; l’attrito la trasforma in energia interna."],
          [("Da che altezza deve cadere un corpo per arrivare a 10 m/s?", ["m g h = ½ m v².", "h = v² : (2g) = 100 : 19,6."], "Circa 5,1 m.")],
          [("Portare una valigia in piano a velocità costante compie lavoro sulla valigia.", "La forza è verticale e lo spostamento orizzontale: il lavoro è nullo."), ("L’energia si perde con l’attrito.", "Si trasforma in energia interna (calore).")],
          [("Che cos’è una forza conservativa?", "Una forza il cui lavoro dipende solo dai punti iniziale e finale, come il peso."), ("Che cos’è il kilowattora?", "Un’energia: 1 kWh = 3,6 × 10⁶ J.")],
          [("Formule", [("lavoro", "L = F s cos α"), ("potenza", "P = L : t"), ("energia cinetica", "Ec = ½ m v²"), ("energia potenziale gravitazionale", "U = m g h"),
                        ("energia potenziale elastica", "U = ½ k x²"), ("teorema dell’energia cinetica", "L = ΔEc"), ("energia meccanica", "E = Ec + U")],
            "Quale formula esprime: {k}?", "Che cosa esprime la formula {v}?"),
           ("Concetti", [("forza conservativa", "lavoro indipendente dal percorso"), ("forza dissipativa", "trasforma energia meccanica in calore"), ("joule", "lavoro di 1 N per 1 m"), ("watt", "1 J al secondo"),
                         ("kilowattora", "3,6 × 10⁶ J"), ("lavoro resistente", "lavoro negativo, forza opposta al moto"), ("lavoro motore", "lavoro positivo, forza nel verso del moto"),
                         ("rendimento", "rapporto tra energia utile e energia totale")],
            "Che cos’è: {k}?", D),
           ("Forze", {"le forze conservative": ["forza peso", "forza elastica", "forza gravitazionale", "forza elettrica"], "le forze non conservative": ["attrito radente", "resistenza dell’aria", "attrito viscoso", "forza dei muscoli"],
                      "i casi con lavoro nullo": ["forza perpendicolare allo spostamento", "corpo fermo spinto contro il muro", "forza centripeta nel moto circolare", "peso su un carrello che va in piano"]})],
          ["L = F s cos α.", "Ec = ½ m v².", "Il peso è una forza conservativa.", "L’attrito non è conservativo.", "Una forza perpendicolare allo spostamento non compie lavoro.",
           "Il lavoro totale è uguale alla variazione di energia cinetica.", "1 kWh = 3,6 × 10⁶ J."],
          [("La forza centripeta compie lavoro.", "È perpendicolare allo spostamento: lavoro nullo."), ("L’attrito è conservativo.", "È dissipativo."), ("Ec = m v².", "Ec = ½ m v²."),
           ("Il watt è un’unità di energia.", "È un’unità di potenza."), ("Raddoppiando v, Ec raddoppia.", "Quadruplica.")],
          "lavoro ed energia", "energy", calc=f_en),

        H("FI", "quantita-di-moto-e-urti", "Quantità di moto, impulso e urti", "Quantità di moto",
          "Lo studente definisce quantità di moto e impulso, applica il teorema dell’impulso e la conservazione della quantità di moto a urti elastici e anelastici e al centro di massa.",
          "quantità di moto, impulso, teorema dell’impulso, sistema isolato, conservazione della quantità di moto, urto elastico, urto anelastico, centro di massa, rinculo, propulsione a razzo",
          "p = m v si conserva nei sistemi isolati", "Negli urti si conserva sempre p; l’energia cinetica solo negli urti elastici.",
          ["La quantità di moto è p = m v (vettore). L’impulso è I = F Δt = Δp.", "In un sistema isolato la quantità di moto totale si conserva.",
           "Negli urti elastici si conserva anche l’energia cinetica; negli anelastici no. Nell’urto completamente anelastico i corpi restano uniti."],
          [("Un carrello di 2 kg a 6 m/s urta uno di 1 kg fermo e restano uniti. Velocità finale?", ["p iniziale = 12 kg·m/s.", "v = 12 : 3."], "4 m/s.")],
          [("Negli urti anelastici la quantità di moto non si conserva.", "Si conserva sempre; si perde energia cinetica."), ("L’airbag diminuisce l’impulso.", "Allunga il tempo dell’urto e così diminuisce la forza.")],
          [("Perché un razzo accelera nel vuoto?", "Espelle gas all’indietro: per la conservazione di p il razzo va avanti."), ("Che cos’è il centro di massa?", "Il punto che si muove come se tutta la massa fosse lì.")],
          [("Grandezze", [("quantità di moto", "kg·m/s"), ("impulso", "N·s"), ("forza", "N"), ("energia cinetica", "J"), ("velocità", "m/s"), ("massa", "kg")],
            "In che unità si misura: {k}?", "Quale grandezza si misura in {v}?"),
           ("Urti", [("due auto che si agganciano", "urto completamente anelastico"), ("palle da biliardo che rimbalzano", "urto quasi elastico"), ("proiettile che si conficca nel legno", "urto completamente anelastico"),
                     ("molecole di un gas", "urto elastico"), ("palla di plastilina che si schiaccia al suolo", "urto completamente anelastico"), ("pallina da ping-pong sul tavolo", "urto quasi elastico"),
                     ("pendolo di Newton", "urto quasi elastico")],
            "Che tipo di urto è: {k}?", None, ("esplosione", "nessun urto")),
           ("Applicazioni", {"le applicazioni della conservazione della quantità di moto": ["rinculo del fucile", "propulsione del razzo", "nuotatore che spinge l’acqua", "pattinatori che si spingono"],
                             "i dispositivi che allungano il tempo dell’urto": ["airbag", "casco imbottito", "materassone del salto in alto", "guanti da portiere", "zona di deformazione dell’auto"],
                             "le grandezze conservate in un urto elastico": ["quantità di moto totale", "energia cinetica totale"]})],
          ["p = m v.", "L’impulso è uguale alla variazione di p.", "In un sistema isolato p si conserva.", "Negli urti elastici si conserva anche Ec.", "L’airbag allunga il tempo dell’urto.",
           "La quantità di moto è un vettore.", "Il razzo accelera espellendo gas."],
          [("Negli urti anelastici p non si conserva.", "Si conserva."), ("L’airbag diminuisce l’impulso.", "Diminuisce la forza allungando il tempo."), ("p è uno scalare.", "È un vettore."),
           ("Negli urti elastici Ec si perde.", "Si conserva."), ("Un razzo nel vuoto non può accelerare.", "Accelera per la conservazione di p.")],
          "la quantità di moto", "forces-and-motion", calc=f_qm),

        H("FI", "gravitazione-universale", "La gravitazione universale", "Gravitazione",
          "Lo studente studia le leggi di Keplero, la legge di gravitazione universale di Newton, il campo gravitazionale, il moto dei satelliti e la velocità di fuga.",
          "leggi di Keplero, orbite ellittiche, gravitazione universale, costante G, campo gravitazionale, accelerazione di gravità, satelliti, velocità orbitale, orbita geostazionaria, velocità di fuga",
          "F = G m₁ m₂ : r²", "La forza di gravità diminuisce con il quadrato della distanza.",
          ["Keplero: le orbite sono ellissi con il Sole in un fuoco; il raggio vettore spazza aree uguali in tempi uguali; T² ∝ a³.",
           "Newton: due masse si attraggono con F = G m₁ m₂ : r², con G = 6,67 × 10⁻¹¹ N·m²/kg².",
           "Per un satellite in orbita circolare la gravità fa da forza centripeta: v = √(G M : r)."],
          [("Se la distanza tra due masse raddoppia, come cambia la forza?", ["F dipende da 1 : r².", "1 : 2² = 1/4."], "Diventa un quarto.")],
          [("Gli astronauti in orbita non hanno peso perché non c’è gravità.", "La gravità c’è: sono in caduta libera intorno alla Terra."), ("Un pianeta va sempre alla stessa velocità.", "Va più veloce vicino al Sole (seconda legge).")],
          [("Che cos’è un’orbita geostazionaria?", "Un’orbita a circa 36 000 km in cui il satellite resta sopra lo stesso punto della Terra."), ("Chi misurò G?", "Henry Cavendish, nel 1798, con la bilancia di torsione.")],
          [("Leggi", [("prima legge di Keplero", "orbite ellittiche con il Sole in un fuoco"), ("seconda legge di Keplero", "aree uguali in tempi uguali"), ("terza legge di Keplero", "T² proporzionale ad a³"),
                      ("legge di gravitazione", "F = G m₁ m₂ : r²"), ("esperimento di Cavendish", "misura della costante G"), ("velocità di fuga", "velocità minima per sfuggire alla gravità"),
                      ("orbita geostazionaria", "periodo di 24 ore sopra l’equatore")],
            "Che cosa afferma o indica: {k}?", D),
           ("Come cambia F?", [("la distanza raddoppia", "un quarto"), ("la distanza si dimezza", "quattro volte"), ("una massa raddoppia", "il doppio"), ("entrambe le masse raddoppiano", "quattro volte"),
                               ("la distanza triplica", "un nono"), ("una massa si dimezza", "la metà"), ("la distanza diventa 10 volte", "un centesimo")],
            "Come diventa la forza gravitazionale se {k}?", None, ("non cambia", "il triplo")),
           ("Corpi", {"i satelliti naturali": ["Luna", "Io", "Europa", "Titano", "Fobos"], "i satelliti artificiali": ["Stazione Spaziale Internazionale", "satelliti GPS", "satelliti meteo geostazionari", "telescopio Hubble"],
                      "i pianeti più vicini al Sole della Terra": ["Mercurio", "Venere"]})],
          ["F = G m₁ m₂ : r².", "Le orbite dei pianeti sono ellittiche.", "T² è proporzionale ad a³.", "Se la distanza raddoppia la forza diventa un quarto.", "Gli astronauti in orbita sono in caduta libera.",
           "Cavendish misurò G.", "Un pianeta è più veloce vicino al Sole."],
          [("Se la distanza raddoppia la forza dimezza.", "Diventa un quarto."), ("In orbita non c’è gravità.", "C’è, ma il corpo cade continuamente."), ("Le orbite sono cerchi perfetti.", "Sono ellissi."),
           ("I pianeti vanno più piano vicino al Sole.", "Vanno più veloci."), ("G vale 9,8.", "G = 6,67 × 10⁻¹¹ N·m²/kg².")],
          "la gravitazione", "earth-and-space", calc=f_grav),

        H("FI", "gas-perfetti-e-teoria-cinetica", "I gas perfetti e la teoria cinetica", "Gas e teoria cinetica",
          "Lo studente applica le leggi di Boyle e Gay-Lussac, l’equazione di stato dei gas perfetti e il modello cinetico che collega temperatura ed energia delle molecole.",
          "gas perfetto, legge di Boyle, leggi di Gay-Lussac, temperatura assoluta, equazione di stato, costante R, numero di Avogadro, teoria cinetica, energia cinetica media, costante di Boltzmann",
          "p V = n R T", "La temperatura assoluta misura l’energia cinetica media delle molecole.",
          ["Boyle: a T costante p V è costante. Gay-Lussac: a p costante V ∝ T; a V costante p ∝ T (temperatura in kelvin).", "Equazione di stato: p V = n R T, con R = 8,31 J/(mol·K).",
           "Teoria cinetica: la pressione nasce dagli urti delle molecole; l’energia cinetica media è 3/2 k_B T."],
          [("Un gas a p costante passa da 300 K a 600 K. Come cambia il volume?", ["V ∝ T.", "600 : 300 = 2."], "Raddoppia.")],
          [("Nelle leggi dei gas si usano i gradi Celsius.", "Si usano i kelvin."), ("Allo zero assoluto le molecole sono velocissime.", "Allo zero assoluto l’agitazione è minima.")],
          [("Perché la bombola scoppia nel fuoco?", "A volume costante la pressione cresce con la temperatura."), ("Che cos’è un gas perfetto?", "Un modello di gas in cui le molecole sono puntiformi e interagiscono solo negli urti.")],
          [("Leggi", [("legge di Boyle", "p V costante a T costante"), ("prima legge di Gay-Lussac", "V proporzionale a T a p costante"), ("seconda legge di Gay-Lussac", "p proporzionale a T a V costante"),
                      ("equazione di stato", "p V = n R T"), ("legge di Avogadro", "volumi uguali, stesso numero di molecole"), ("teoria cinetica", "pressione dovuta agli urti delle molecole"),
                      ("legge di Dalton dei gas", "la pressione totale è la somma delle pressioni parziali")],
            "Che cosa afferma: {k}?", D),
           ("Trasformazioni", [("isoterma", "temperatura costante"), ("isobara", "pressione costante"), ("isocora", "volume costante"), ("adiabatica", "nessuno scambio di calore"),
                               ("espansione libera", "il gas si espande nel vuoto"), ("compressione", "il volume diminuisce")],
            "Che cosa resta costante o accade in una trasformazione {k}?", "Quale trasformazione avviene con {v}?"),
           ("Costanti", {"le costanti della teoria dei gas": ["R = 8,31 J/(mol·K)", "k_B = 1,38 × 10⁻²³ J/K", "NA = 6,02 × 10²³ mol⁻¹", "volume molare 22,4 l a 0 °C e 1 atm"],
                         "le grandezze di stato di un gas": ["pressione", "volume", "temperatura", "numero di moli"],
                         "le ipotesi del gas perfetto": ["molecole puntiformi", "urti elastici", "nessuna forza a distanza", "moto casuale"]})],
          ["p V = n R T.", "Nelle leggi dei gas la temperatura è in kelvin.", "A T costante p V è costante.", "L’energia cinetica media è proporzionale a T.", "R = 8,31 J/(mol·K).",
           "In un’isocora il volume è costante.", "La pressione nasce dagli urti delle molecole."],
          [("Nelle leggi dei gas si usano i °C.", "Si usano i kelvin."), ("In un’isobara il volume è costante.", "È costante la pressione."), ("p V = n T.", "p V = n R T."),
           ("Raddoppiando T in kelvin, V dimezza a p costante.", "Raddoppia."), ("Le molecole di un gas perfetto si attraggono.", "Non interagiscono a distanza.")],
          "i gas", "energy", calc=f_gas),

        H("CH", "struttura-dell-atomo", "La struttura dell’atomo", "Struttura dell’atomo",
          "Lo studente descrive le particelle subatomiche, i modelli atomici da Thomson a Bohr al modello quantistico, numero atomico e di massa, isotopi e configurazione elettronica.",
          "elettrone, protone, neutrone, modelli di Thomson, Rutherford, Bohr, modello quantistico, orbitali, numero atomico, numero di massa, isotopi, livelli energetici, configurazione elettronica",
          "Z = protoni; A = protoni + neutroni", "Gli isotopi hanno stesso Z e diverso numero di neutroni.",
          ["L’atomo ha un nucleo con protoni e neutroni e una nuvola di elettroni. Z è il numero di protoni, A = protoni + neutroni.",
           "Thomson: panettone di cariche. Rutherford: nucleo piccolo e denso. Bohr: elettroni su orbite con energia definita. Modello quantistico: orbitali (s, p, d, f).",
           "Gli elettroni riempiono gli orbitali in ordine di energia: 1s 2s 2p 3s 3p 4s 3d …"],
          [("Quanti neutroni ha il carbonio-14 (Z = 6)?", ["Neutroni = A − Z.", "14 − 6 = 8."], "8 neutroni.")],
          [("Gli isotopi hanno numero di protoni diverso.", "Hanno lo stesso Z e diverso numero di neutroni."), ("L’elettrone gira su un’orbita precisa.", "Nel modello quantistico c’è una probabilità: l’orbitale.")],
          [("Che cosa scoprì Rutherford?", "Con le particelle alfa sulla lamina d’oro scoprì il nucleo piccolo e positivo."), ("Perché gli atomi emettono luce di colori precisi?", "Gli elettroni saltano tra livelli di energia definiti.")],
          [("Particelle", [("protone", "carica positiva nel nucleo"), ("neutrone", "particella neutra nel nucleo"), ("elettrone", "carica negativa intorno al nucleo"), ("nucleone", "protone o neutrone"),
                           ("numero atomico Z", "numero di protoni"), ("numero di massa A", "protoni più neutroni"), ("isotopi", "stesso Z, diverso A"), ("ione positivo", "atomo che ha perso elettroni")],
            "Che cos’è: {k}?", D),
           ("Modelli", [("Thomson", "cariche negative in una sfera positiva"), ("Rutherford", "nucleo piccolo e denso con elettroni intorno"), ("Bohr", "orbite con energia quantizzata"),
                        ("Schrödinger", "orbitali come zone di probabilità"), ("Chadwick", "scoperta del neutrone"), ("Dalton", "atomo come sfera indivisibile"), ("Pauli", "al massimo due elettroni per orbitale")],
            "A quale idea è legato: {k}?", "Chi è legato a: {v}?"),
           ("Orbitali", {"gli orbitali che contengono al massimo 2 elettroni": ["1s", "2s", "3s", "4s", "un singolo orbitale 2p"], "i sottolivelli con 6 elettroni al massimo": ["2p", "3p", "4p", "5p"],
                         "gli isotopi dell’idrogeno": ["prozio", "deuterio", "trizio"]})],
          ["Z è il numero di protoni.", "Gli isotopi hanno diverso numero di neutroni.", "Rutherford scoprì il nucleo.", "Un orbitale contiene al massimo due elettroni.", "Il neutrone è neutro.",
           "Bohr introdusse i livelli di energia.", "A = protoni + neutroni."],
          [("Gli isotopi hanno Z diverso.", "Hanno lo stesso Z."), ("Il neutrone è positivo.", "È neutro."), ("Un orbitale contiene 8 elettroni.", "Al massimo 2."), ("Thomson scoprì il nucleo.", "Lo scoprì Rutherford."),
           ("A = Z − neutroni.", "A = Z + neutroni.")],
          "l’atomo", "matter", calc=f_atomo),

        H("CH", "tavola-periodica", "La tavola periodica e le proprietà periodiche", "Tavola periodica",
          "Lo studente legge la tavola periodica per gruppi e periodi, distingue metalli, non metalli e semimetalli e descrive raggio atomico, energia di ionizzazione, affinità elettronica ed elettronegatività.",
          "Mendeleev, gruppi, periodi, blocchi s, p, d, f, metalli, non metalli, semimetalli, gas nobili, alogeni, metalli alcalini, raggio atomico, energia di ionizzazione, elettronegatività",
          "Lungo il gruppo il raggio cresce", "L’elettronegatività cresce verso destra e verso l’alto: il fluoro è il più elettronegativo.",
          ["Gli elementi sono ordinati per Z crescente; nello stesso gruppo hanno gli stessi elettroni di valenza e proprietà simili.",
           "Il raggio atomico cresce scendendo nel gruppo e diminuisce lungo il periodo.", "Energia di ionizzazione ed elettronegatività crescono verso destra e verso l’alto."],
          [("Chi ha raggio atomico maggiore, Na o Cl?", ["Sono nello stesso periodo.", "Lungo il periodo il raggio diminuisce."], "Il sodio.")],
          [("I gas nobili sono molto reattivi.", "Hanno l’ottetto completo e sono quasi inerti."), ("L’elettronegatività cresce scendendo nel gruppo.", "Diminuisce scendendo.")],
          [("Perché Mendeleev lasciò caselle vuote?", "Per elementi non ancora scoperti, di cui previde le proprietà."), ("Che cosa hanno in comune gli alogeni?", "Sette elettroni di valenza e tendenza a formare ioni −1.")],
          [("Gruppi", [("litio", "metalli alcalini"), ("sodio", "metalli alcalini"), ("potassio", "metalli alcalini"), ("magnesio", "metalli alcalino-terrosi"), ("calcio", "metalli alcalino-terrosi"),
                       ("fluoro", "alogeni"), ("cloro", "alogeni"), ("iodio", "alogeni"), ("neon", "gas nobili"), ("argon", "gas nobili"), ("ferro", "metalli di transizione"), ("rame", "metalli di transizione")],
            "A quale famiglia appartiene: {k}?", None),
           ("Proprietà", [("raggio atomico", "cresce scendendo nel gruppo"), ("energia di ionizzazione", "energia per strappare un elettrone"), ("affinità elettronica", "energia liberata quando un atomo acquista un elettrone"),
                          ("elettronegatività", "tendenza ad attrarre gli elettroni di legame"), ("carattere metallico", "cresce verso sinistra e verso il basso"), ("periodo", "riga orizzontale della tavola"),
                          ("gruppo", "colonna verticale della tavola"), ("elettroni di valenza", "elettroni dell’ultimo livello")],
            "Che cos’è o come varia: {k}?", D),
           ("Tipi", {"i metalli": ["sodio", "ferro", "rame", "oro", "alluminio"], "i non metalli": ["ossigeno", "azoto", "zolfo", "fosforo", "cloro"], "i semimetalli": ["silicio", "germanio", "arsenico", "boro", "antimonio"]})],
          ["Gli elementi dello stesso gruppo hanno proprietà simili.", "Il fluoro è l’elemento più elettronegativo.", "Il raggio atomico cresce scendendo nel gruppo.", "I gas nobili sono poco reattivi.",
           "Il sodio è un metallo alcalino.", "Mendeleev ordinò gli elementi lasciando caselle vuote.", "Il silicio è un semimetallo."],
          [("Il raggio cresce lungo il periodo.", "Diminuisce."), ("I gas nobili sono molto reattivi.", "Sono quasi inerti."), ("Il cloro è un metallo.", "È un non metallo."),
           ("L’elettronegatività cresce scendendo.", "Diminuisce scendendo."), ("Il calcio è un alogeno.", "È un metallo alcalino-terroso.")],
          "la tavola periodica", "matter"),

        H("CH", "legami-chimici", "I legami chimici e la forma delle molecole", "Legami chimici",
          "Lo studente descrive la regola dell’ottetto, i legami ionico, covalente puro e polare, metallico, la teoria VSEPR, la polarità delle molecole e i legami intermolecolari.",
          "regola dell’ottetto, simboli di Lewis, legame ionico, covalente puro e polare, doppio e triplo legame, legame metallico, elettronegatività, VSEPR, geometria molecolare, polarità, legame a idrogeno, forze di van der Waals",
          "Ionico, covalente, metallico", "Se la differenza di elettronegatività supera circa 1,9 il legame è ionico.",
          ["Gli atomi si legano per raggiungere l’ottetto. Nel legame ionico un atomo cede elettroni a un altro; nel covalente li condividono.",
           "Il legame covalente è puro tra atomi uguali, polare se le elettronegatività sono diverse. Nel legame metallico gli elettroni sono liberi.",
           "La VSEPR prevede la forma: le coppie di elettroni si allontanano il più possibile (CH₄ tetraedrica, H₂O piegata, CO₂ lineare)."],
          [("Che legame c’è in NaCl?", ["Na cede un elettrone a Cl.", "Si formano Na⁺ e Cl⁻."], "Legame ionico.")],
          [("CO₂ è polare perché ha legami polari.", "È lineare: i dipoli si annullano ed è apolare."), ("Il legame a idrogeno è un legame tra atomi di idrogeno.", "È un’attrazione tra H legato a F, O o N e un altro atomo elettronegativo.")],
          [("Perché il sale fonde a temperatura alta?", "Il reticolo ionico è tenuto da forze elettrostatiche molto forti."), ("Perché i metalli conducono l’elettricità?", "Hanno elettroni liberi di muoversi.")],
          [("Tipi di legame", [("NaCl", "ionico"), ("MgO", "ionico"), ("KBr", "ionico"), ("H₂", "covalente puro"), ("Cl₂", "covalente puro"), ("O₂", "covalente puro"), ("H₂O", "covalente polare"),
                               ("HCl", "covalente polare"), ("NH₃", "covalente polare"), ("rame metallico", "metallico"), ("ferro metallico", "metallico")],
            "Che legame c’è in {k}?", None),
           ("Geometria", [("CH₄", "tetraedrica"), ("H₂O", "piegata"), ("NH₃", "piramidale"), ("CO₂", "lineare"), ("BF₃", "triangolare planare"), ("BeCl₂", "lineare"), ("SF₆", "ottaedrica")],
            "Che geometria ha la molecola {k}?", None, ("cubica",)),
           ("Polarità e forze", {"le molecole polari senza legami a idrogeno": ["HCl", "H₂S", "SO₂", "CHCl₃", "PCl₃"], "le molecole apolari": ["CO₂", "CH₄", "O₂", "N₂", "CCl₄"],
                                 "le sostanze con legami a idrogeno": ["acqua", "ammoniaca", "acido fluoridrico", "etanolo", "DNA"]})],
          ["NaCl ha un legame ionico.", "CO₂ è una molecola apolare.", "H₂O ha forma piegata.", "Nel legame metallico gli elettroni sono liberi.", "CH₄ è tetraedrica.",
           "L’acqua forma legami a idrogeno.", "Il legame tra due atomi di cloro è covalente puro."],
          [("CO₂ è polare.", "È lineare e apolare."), ("H₂O è lineare.", "È piegata."), ("NaCl ha un legame covalente.", "È ionico."), ("CH₄ è planare.", "È tetraedrica."),
           ("Il legame a idrogeno è più forte del covalente.", "È molto più debole.")],
          "i legami chimici", "matter"),

        H("BI", "genetica-mendeliana", "La genetica mendeliana e oltre Mendel", "Genetica",
          "Lo studente applica le leggi di Mendel con il quadrato di Punnett, l’incrocio di prova e il diibrido, la dominanza incompleta, la codominanza, gli alleli multipli e l’eredità legata al sesso.",
          "leggi di Mendel, dominante, recessivo, omozigote, eterozigote, genotipo, fenotipo, quadrato di Punnett, incrocio di prova, diibrido, dominanza incompleta, codominanza, gruppi sanguigni, eredità legata al cromosoma X",
          "Aa × Aa → 3 : 1", "Nel diibrido AaBb × AaBb il rapporto è 9 : 3 : 3 : 1.",
          ["Prima legge (dominanza): incrociando due linee pure, la F1 è uniforme. Seconda (segregazione): in F2 il rapporto fenotipico è 3 : 1.",
           "Terza legge (assortimento indipendente): per due caratteri su cromosomi diversi il rapporto è 9 : 3 : 3 : 1.",
           "Ci sono eccezioni: dominanza incompleta (rosa da rosso × bianco), codominanza (gruppo AB), geni sul cromosoma X (daltonismo, emofilia)."],
          [("Un maschio daltonico da chi eredita l’allele?", ["Il maschio è XY.", "La Y viene dal padre, la X dalla madre."], "Dalla madre.")],
          [("Il carattere dominante è il più frequente.", "Dominante significa che si manifesta anche in eterozigosi."), ("Le malattie legate all’X colpiscono di più le femmine.", "Colpiscono di più i maschi, che hanno una sola X.")],
          [("Che cos’è un incrocio di prova?", "Incrociare un individuo dominante con un omozigote recessivo per scoprire se è AA o Aa."), ("Perché il gruppo 0 è recessivo?", "L’allele i non produce antigeni ed è coperto da Iᴬ e Iᴮ.")],
          [("Concetti", [("omozigote", "due alleli uguali"), ("eterozigote", "due alleli diversi"), ("genotipo", "insieme degli alleli"), ("fenotipo", "caratteristiche osservabili"),
                         ("dominanza incompleta", "l’eterozigote ha un fenotipo intermedio"), ("codominanza", "entrambi gli alleli si manifestano"), ("alleli multipli", "più di due alleli per un gene"),
                         ("linea pura", "individui omozigoti che danno figli uguali")],
            "Che cos’è: {k}?", D),
           ("Leggi ed esempi", [("legge della dominanza", "F1 tutta uguale da due linee pure"), ("legge della segregazione", "rapporto 3 : 1 in F2"), ("legge dell’assortimento indipendente", "rapporto 9 : 3 : 3 : 1"),
                                ("bocca di leone rosa", "dominanza incompleta"), ("gruppo sanguigno AB", "codominanza"), ("daltonismo", "eredità legata all’X"), ("gruppi sanguigni ABO", "alleli multipli")],
            "Che cosa indica o di che cosa è esempio: {k}?", D),
           ("Genotipi", {"i genotipi del gruppo A": ["IᴬIᴬ", "Iᴬi"], "i genotipi del gruppo B": ["IᴮIᴮ", "Iᴮi"], "le malattie legate al cromosoma X": ["emofilia", "daltonismo", "distrofia muscolare di Duchenne"],
                         "le malattie autosomiche recessive": ["fibrosi cistica", "anemia falciforme", "fenilchetonuria", "talassemia"]})],
          ["Aa × Aa dà il rapporto 3 : 1.", "Il gruppo AB è un caso di codominanza.", "Il daltonismo è legato al cromosoma X.", "Un eterozigote ha due alleli diversi.", "Il diibrido dà 9 : 3 : 3 : 1.",
           "Il gruppo 0 ha genotipo ii.", "L’incrocio di prova usa un omozigote recessivo."],
          [("Aa × Aa dà 1 : 1.", "Dà 3 : 1."), ("Il daltonismo colpisce di più le femmine.", "Colpisce di più i maschi."), ("Il gruppo AB è recessivo.", "È codominante."),
           ("Un omozigote ha alleli diversi.", "Ha alleli uguali."), ("Il fenotipo è l’insieme degli alleli.", "È quello che si osserva.")],
          "la genetica", "living-things-and-ecosystems", calc=f_gen),

        H("BI", "dna-e-sintesi-proteica", "Il DNA, la duplicazione e la sintesi delle proteine", "DNA e proteine",
          "Lo studente descrive la struttura del DNA, la duplicazione semiconservativa, la trascrizione, il codice genetico, la traduzione e le mutazioni.",
          "nucleotidi, basi azotate, doppia elica, Watson e Crick, duplicazione semiconservativa, DNA polimerasi, RNA, trascrizione, mRNA, codone, codice genetico, ribosomi, tRNA, traduzione, mutazioni",
          "DNA → RNA → proteina", "Ogni codone di tre basi codifica un amminoacido.",
          ["Il DNA è una doppia elica di nucleotidi: A si appaia con T, G con C. Si duplica in modo semiconservativo.",
           "Nella trascrizione si forma l’mRNA (con U al posto di T). Nei ribosomi i tRNA leggono i codoni e portano gli amminoacidi.",
           "Una mutazione è un cambiamento del DNA: può essere puntiforme, cromosomica o genomica."],
          [("Quale filamento è complementare ad AGCT?", ["A–T, G–C.", "AGCT → TCGA."], "TCGA.")],
          [("L’RNA ha la timina.", "L’RNA ha l’uracile al posto della timina."), ("Ogni mutazione è dannosa.", "Molte sono neutre e alcune utili: sono la base dell’evoluzione.")],
          [("Perché il codice genetico è detto ridondante?", "Più codoni diversi codificano lo stesso amminoacido."), ("Che cosa vuol dire semiconservativa?", "Ogni nuova doppia elica ha un filamento vecchio e uno nuovo.")],
          [("Molecole", [("DNA polimerasi", "costruisce il nuovo filamento di DNA"), ("RNA polimerasi", "trascrive il DNA in RNA"), ("mRNA", "porta il messaggio ai ribosomi"), ("tRNA", "trasporta gli amminoacidi"),
                         ("rRNA", "forma i ribosomi"), ("codone", "tripletta di basi dell’mRNA"), ("anticodone", "tripletta del tRNA complementare al codone"), ("elicasi", "apre la doppia elica")],
            "Che cosa fa o che cos’è: {k}?", D),
           ("Processi", [("duplicazione", "nel nucleo, prima della divisione cellulare"), ("trascrizione", "nel nucleo, DNA in mRNA"), ("traduzione", "nei ribosomi, mRNA in proteina"),
                         ("maturazione dell’mRNA", "eliminazione degli introni"), ("mutazione puntiforme", "cambio di una sola base"), ("delezione", "perdita di un tratto di DNA"),
                         ("traslocazione", "spostamento di un pezzo di cromosoma su un altro")],
            "Che cos’è: {k}?", D),
           ("Basi e codici", {"le basi del DNA": ["adenina", "timina", "guanina", "citosina"], "le basi dell’RNA": ["adenina", "uracile", "guanina", "citosina"], "i codoni di stop": ["UAA", "UAG", "UGA"],
                              "gli scienziati della scoperta del DNA": ["Watson", "Crick", "Rosalind Franklin", "Wilkins"]})],
          ["A si appaia con T nel DNA.", "L’RNA contiene uracile.", "Un codone ha tre basi.", "La traduzione avviene nei ribosomi.", "La duplicazione del DNA è semiconservativa.",
           "AUG è il codone di inizio.", "Rosalind Franklin ottenne le immagini ai raggi X del DNA."],
          [("L’RNA contiene timina.", "Contiene uracile."), ("La traduzione avviene nel nucleo.", "Avviene nei ribosomi."), ("Un codone ha due basi.", "Ne ha tre."), ("Nel DNA A si appaia con G.", "A con T, G con C."),
           ("Tutte le mutazioni sono dannose.", "Molte sono neutre.")],
          "il DNA", "living-things-and-ecosystems", calc=f_gen),

        H("ST", "minerali-e-rocce", "Minerali, rocce e ciclo litogenetico", "Minerali e rocce",
          "Lo studente descrive struttura e proprietà dei minerali, i silicati, la formazione delle rocce magmatiche, sedimentarie e metamorfiche e il ciclo litogenetico.",
          "minerali, reticolo cristallino, abito cristallino, durezza, sfaldatura, silicati, tetraedro SiO₄, rocce magmatiche intrusive ed effusive, sedimentarie clastiche, chimiche e organogene, metamorfismo, ciclo litogenetico",
          "Magma → roccia → sedimento → metamorfismo", "I silicati, basati sul tetraedro SiO₄, sono i minerali più diffusi.",
          ["Un minerale è un solido naturale con composizione definita e struttura cristallina. I più diffusi sono i silicati.",
           "Le rocce magmatiche intrusive (granito) raffreddano lentamente in profondità; le effusive (basalto) in fretta in superficie.",
           "Le sedimentarie nascono da erosione, trasporto, deposito e diagenesi; le metamorfiche da calore e pressione. Tutte si trasformano nel ciclo litogenetico."],
          [("Perché l’ossidiana è vetrosa?", ["La lava si è raffreddata in un attimo.", "Non si sono formati cristalli."], "Per il raffreddamento rapidissimo.")],
          [("Tutte le rocce sono fatte di cristalli visibili.", "Le effusive hanno cristalli piccoli o vetro."), ("Il marmo è una roccia magmatica.", "È metamorfica, deriva dal calcare.")],
          [("Che cos’è la diagenesi?", "L’insieme di compattazione e cementazione che trasforma un sedimento in roccia."), ("Come si riconosce il calcare?", "Fa effervescenza con l’acido cloridrico diluito.")],
          [("Rocce", [("granito", "magmatica intrusiva"), ("gabbro", "magmatica intrusiva"), ("basalto", "magmatica effusiva"), ("pomice", "magmatica effusiva"), ("ossidiana", "magmatica effusiva"),
                      ("arenaria", "sedimentaria clastica"), ("conglomerato", "sedimentaria clastica"), ("travertino", "sedimentaria chimica"), ("carbone", "sedimentaria organogena"),
                      ("marmo", "metamorfica"), ("gneiss", "metamorfica"), ("ardesia", "metamorfica")],
            "Che tipo di roccia è: {k}?", None),
           ("Proprietà", [("durezza", "resistenza alla scalfittura"), ("sfaldatura", "rottura lungo piani regolari"), ("lucentezza", "modo di riflettere la luce"), ("abito cristallino", "forma esterna del cristallo"),
                          ("polimorfismo", "stessa composizione con struttura diversa"), ("isomorfismo", "stessa struttura con composizione diversa"), ("striscio", "colore della polvere del minerale"),
                          ("densità", "massa per unità di volume")],
            "Che cos’è: {k}?", D),
           ("Minerali", {"i silicati": ["quarzo", "feldspato", "mica", "olivina", "pirosseno"], "i carbonati": ["calcite", "dolomite", "aragonite", "malachite"], "gli elementi nativi": ["oro", "diamante", "grafite", "zolfo", "rame nativo"]})],
          ["Il granito è intrusivo.", "Il basalto è effusivo.", "Il marmo è metamorfico.", "I silicati sono i minerali più diffusi.", "Il calcare fa effervescenza con l’acido.",
           "Diamante e grafite sono polimorfi del carbonio.", "La diagenesi trasforma il sedimento in roccia."],
          [("Il basalto è intrusivo.", "È effusivo."), ("Il marmo è magmatico.", "È metamorfico."), ("Il quarzo è un carbonato.", "È un silicato."), ("Diamante e grafite hanno composizione diversa.", "Sono entrambi carbonio."),
           ("Le rocce sedimentarie nascono dal magma.", "Nascono da sedimenti.")],
          "le rocce", "earths-systems"),
    ]
