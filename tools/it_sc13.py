# -*- coding: utf-8 -*-
"""Italia / Liceo scientifico: quinta liceo（Fisica e Scienze naturali, quinto anno）"""
import math
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"
C = 3e8
HP = 6.63e-34
EV = 1.6e-19
MU0 = 4 * math.pi * 1e-7


def f_mag(R):
    k = R.choice(["filo", "forza", "lor", "raggio", "sol", "spira"])
    if k == "filo":
        i, r = R.choice([(10, 0.05), (5, 0.02), (20, 0.1), (2, 0.01), (15, 0.03), (8, 0.04)])
        b = MU0 * i / (2 * math.pi * r)
        return nq("Quanto vale il campo magnetico a %s m da un filo rettilineo percorso da %d A? (μ₀ = 4π × 10⁻⁷ T·m/A)" % (num(r), i), b, [MU0 * i / r, b * 2, MU0 * i * r, b / 10], "T",
                  "B = μ₀ I : (2π r) = %s T." % num(b))
    if k == "forza":
        b, i, l = R.choice([(0.5, 2, 0.3), (0.2, 5, 0.1), (1, 3, 0.2), (0.05, 10, 1), (0.8, 4, 0.25)])
        return nq("Un filo lungo %s m, percorso da %d A, è perpendicolare a un campo di %s T. Quale forza subisce?" % (num(l), i, num(b)), b * i * l, [b * i, b * l, i * l, b * i * l * 2], "N",
                  "F = B I L = %s × %d × %s = %s N." % (num(b), i, num(l), num(b * i * l)))
    if k == "lor":
        v, b = R.choice([(2e6, 0.5), (1e5, 0.1), (3e6, 0.2), (5e5, 1), (1e7, 0.05)])
        return nq("Un protone (q = 1,6 × 10⁻¹⁹ C) si muove a %s m/s perpendicolarmente a un campo di %s T. Quanto vale la forza di Lorentz?" % (num(v), num(b)), EV * v * b,
                  [EV * v, EV * b, v * b, EV * v * b * 10], "N", "F = q v B = %s N." % num(EV * v * b))
    if k == "raggio":
        v, b = R.choice([(1e6, 0.01), (2e6, 0.005), (5e5, 0.002), (1e7, 0.1), (3e6, 0.02)])
        r = 9.11e-31 * v / (EV * b)
        return nq("Un elettrone (m = 9,11 × 10⁻³¹ kg) entra a %s m/s perpendicolarmente in un campo di %s T. Quanto vale il raggio della traiettoria?" % (num(v), num(b)), r,
                  [EV * b / (9.11e-31 * v), r * 2, 9.11e-31 * v * v / (EV * b), r / 10], "m", "r = m v : (q B) = %s m." % num(r))
    if k == "sol":
        n, l, i = R.choice([(500, 0.25, 2), (1000, 0.5, 1), (200, 0.1, 3), (800, 0.4, 0.5), (1500, 0.3, 2)])
        b = MU0 * n * i / l
        return nq("Un solenoide lungo %s m ha %d spire ed è percorso da %s A. Quanto vale il campo all’interno? (μ₀ = 4π × 10⁻⁷ T·m/A)" % (num(l), n, num(i)), b, [MU0 * n * i, b / 2, MU0 * i / l, b * n / 100], "T",
                  "B = μ₀ N I : L = %s T." % num(b))
    i, r = R.choice([(5, 0.1), (2, 0.05), (10, 0.2), (1, 0.02), (4, 0.08)])
    b = MU0 * i / (2 * r)
    return nq("Quanto vale il campo al centro di una spira di raggio %s m percorsa da %d A? (μ₀ = 4π × 10⁻⁷ T·m/A)" % (num(r), i), b, [MU0 * i / (2 * math.pi * r), b * 2, MU0 * i * r, b / 4], "T",
              "B = μ₀ I : (2r) = %s T." % num(b))


def f_ind(R):
    k = R.choice(["flusso", "fem", "mov", "trasf", "trasf2", "eff"])
    if k == "flusso":
        b, a = R.choice([(0.2, 0.05), (0.5, 0.01), (1.2, 0.02), (0.05, 0.5), (0.8, 0.04)])
        return nq("Un campo uniforme di %s T attraversa perpendicolarmente una spira di %s m². Quanto vale il flusso?" % (num(b), num(a)), b * a, [b / a, a / b, b * a * 2, b + a], "Wb", "Φ = B S = %s Wb." % num(b * a))
    if k == "fem":
        d, t, n = R.choice([(0.02, 0.1, 100), (0.05, 0.5, 200), (0.01, 0.02, 50), (0.1, 2, 500), (0.03, 0.06, 20)])
        e = n * d / t
        return nq("In una bobina di %d spire il flusso varia di %s Wb in %s s. Quanto vale la fem indotta (in modulo)?" % (n, num(d), num(t)), e, [d / t, n * d * t, e / n / 10 if e / n / 10 else 1, e * 2], "V",
                  "Legge di Faraday-Neumann: |fem| = N ΔΦ : Δt = %d × %s : %s = %s V." % (n, num(d), num(t), num(e)))
    if k == "mov":
        b, l, v = R.choice([(0.5, 0.2, 4), (1, 0.5, 2), (0.2, 1, 10), (0.8, 0.3, 5), (0.4, 0.25, 8)])
        return nq("Una sbarretta lunga %s m si muove a %s m/s perpendicolarmente a un campo di %s T. Quanto vale la fem indotta?" % (num(l), num(v), num(b)), b * l * v, [b * l, b * v, l * v, b * l * v * 2], "V",
                  "fem = B L v = %s V." % num(b * l * v))
    if k == "trasf":
        v1, n1, n2 = R.choice([(230, 1000, 50), (230, 500, 1000), (12, 100, 2000), (230, 2000, 100), (110, 200, 400)])
        return nq("Un trasformatore ha %d spire al primario e %d al secondario. Il primario è a %d V. Quale tensione si ha al secondario?" % (n1, n2, v1), v1 * n2 / n1, [v1 * n1 / n2, v1, v1 * n2, v1 / n2], "V",
                  "V₂ : V₁ = N₂ : N₁ → V₂ = %d × %d : %d = %s V." % (v1, n2, n1, num(v1 * n2 / n1)))
    if k == "trasf2":
        v1, v2, i1 = R.choice([(230, 12, 0.5), (230, 23, 1), (12, 240, 10), (230, 115, 2)])
        return nq("Un trasformatore ideale abbassa la tensione da %d V a %d V; al primario passano %s A. Quale corrente c’è al secondario?" % (v1, v2, num(i1)) if v2 < v1 else
                  "Un trasformatore ideale alza la tensione da %d V a %d V; al primario passano %s A. Quale corrente c’è al secondario?" % (v1, v2, num(i1)), i1 * v1 / v2,
                  [i1 * v2 / v1, i1, i1 * v1, v1 / v2], "A", "Potenza uguale: V₁ I₁ = V₂ I₂ → I₂ = %s A." % num(i1 * v1 / v2))
    v = R.choice([230, 325, 120, 400, 12])
    return nq("Una tensione alternata ha valore di picco %d V. Quanto vale il valore efficace?" % v, v / math.sqrt(2), [v * math.sqrt(2), v / 2, v, v / math.sqrt(3)], "V",
              "Veff = Vmax : √2 = %s V." % num(v / math.sqrt(2)))


def f_rel(R):
    k = R.choice(["gamma", "dil", "contr", "en", "mass", "vel"])
    v = R.choice([0.6, 0.8, 0.5, 0.9, 0.99, 0.28])
    g = 1 / math.sqrt(1 - v * v)
    if k == "gamma":
        return nq("Quanto vale il fattore di Lorentz γ per una velocità di %s c?" % num(v), g, [1 - v * v, 1 / (1 - v), math.sqrt(1 - v * v), g * 2], "", "γ = 1 : √(1 − v²/c²) = 1 : √(1 − %s²) = %s." % (num(v), num(g)))
    if k == "dil":
        t = R.choice([1, 2, 10, 2.2e-6, 5])
        return nq("Un orologio in moto a %s c misura %s s. Quanto tempo passa per un osservatore fermo?" % (num(v), num(t)), g * t, [t / g, t, t * v, t * g * g], "s", "Dilatazione dei tempi: Δt = γ Δt₀ = %s × %s = %s s." % (num(g), num(t), num(g * t)))
    if k == "contr":
        l = R.choice([10, 100, 1, 50, 20])
        return nq("Un’astronave lunga %d m (a riposo) viaggia a %s c. Quanto è lunga per un osservatore fermo?" % (l, num(v)), l / g, [l * g, l, l * v, l * (1 - v)], "m", "Contrazione: L = L₀ : γ = %d : %s = %s m." % (l, num(g), num(l / g)))
    if k == "en":
        m = R.choice([1, 0.001, 1e-6, 2, 0.5])
        return nq("Quanta energia corrisponde a una massa di %s kg? (c = 3 × 10⁸ m/s)" % num(m), m * C * C, [m * C, m * C * C / 2, m * C * C * 10, C * C], "J", "E = m c² = %s J." % num(m * C * C))
    if k == "mass":
        return nq("Un elettrone (energia a riposo 0,511 MeV) viaggia a %s c. Quanto vale la sua energia totale?" % num(v), 0.511 * g, [0.511, 0.511 / g, 0.511 * g * g, 0.511 * v], "MeV",
                  "E = γ m c² = %s × 0,511 = %s MeV." % (num(g), num(0.511 * g)))
    u, w = R.choice([(0.5, 0.5), (0.6, 0.6), (0.8, 0.5), (0.9, 0.9), (0.7, 0.4)])
    s = (u + w) / (1 + u * w)
    return nq("Un’astronave a %s c lancia in avanti una sonda a %s c rispetto a sé. Quanto vale la velocità della sonda per un osservatore fermo (in unità di c)?" % (num(u), num(w)), s,
              [u + w, abs(u - w) if u != w else u / 2, u * w, (u + w) / 2], "c", "Composizione relativistica: (u + v) : (1 + u v / c²) = %s c." % num(s))


def f_q(R):
    k = R.choice(["fot", "fot2", "foto", "soglia", "db", "bohr"])
    if k == "fot":
        f = R.choice([5e14, 6e14, 1e15, 3e14, 7.5e14, 1e18])
        return nq("Quanto vale l’energia di un fotone di frequenza %s Hz? (h = 6,63 × 10⁻³⁴ J·s)" % num(f), HP * f, [HP / f, f / HP, HP * f * 10, HP * f / 2], "J", "E = h f = %s J." % num(HP * f))
    if k == "fot2":
        lam = R.choice([400e-9, 500e-9, 620e-9, 700e-9, 250e-9])
        e = HP * C / lam / EV
        return nq("Quanto vale in elettronvolt l’energia di un fotone con λ = %s nm? (h c = 1,99 × 10⁻²⁵ J·m, 1 eV = 1,6 × 10⁻¹⁹ J)" % num(lam * 1e9), e, [e * 2, HP * C / lam, e / 10, lam * 1e9 / 1240], "eV",
                  "E = h c : λ = %s J = %s eV." % (num(HP * C / lam), num(e)))
    if k == "foto":
        ef, w = R.choice([(4, 2.3), (5, 2.1), (6, 4.3), (3.5, 2.3), (4.5, 2.7), (7, 4.7)])
        return nq("Fotoni di %s eV colpiscono un metallo con lavoro di estrazione %s eV. Qual è l’energia cinetica massima degli elettroni emessi?" % (num(ef), num(w)), ef - w, [ef + w, ef, w, ef / w], "eV",
                  "Effetto fotoelettrico (Einstein): Ec = h f − W = %s − %s = %s eV." % (num(ef), num(w), num(ef - w)))
    if k == "soglia":
        w = R.choice([2.3, 4.3, 2.1, 4.7, 2.7])
        f0 = w * EV / HP
        return nq("Un metallo ha lavoro di estrazione %s eV. Qual è la frequenza di soglia? (h = 6,63 × 10⁻³⁴ J·s, 1 eV = 1,6 × 10⁻¹⁹ J)" % num(w), f0, [HP / (w * EV), w / HP, f0 / 10, f0 * 2], "Hz", "f₀ = W : h = %s Hz." % num(f0))
    if k == "db":
        m, v, n = R.choice([(9.11e-31, 1e6, "un elettrone"), (9.11e-31, 2e6, "un elettrone"), (1.67e-27, 1e5, "un protone"), (0.145, 40, "una palla da baseball"), (9.11e-31, 5e6, "un elettrone")])
        lam = HP / (m * v)
        return nq("Qual è la lunghezza d’onda di de Broglie di %s di massa %s kg a %s m/s?" % (n, num(m), num(v)), lam, [m * v / HP, HP * m * v, lam * 10, HP / m], "m", "λ = h : (m v) = %s m." % num(lam))
    n1, n2 = R.choice([(3, 2), (4, 2), (2, 1), (3, 1), (5, 2)])
    e = 13.6 * (1 / n2 ** 2 - 1 / n1 ** 2)
    return nq("Nell’atomo di idrogeno (En = −13,6 eV : n²) l’elettrone passa da n = %d a n = %d. Quanta energia ha il fotone emesso?" % (n1, n2), e, [13.6 / n1 ** 2, 13.6 / n2 ** 2, 13.6 * (n1 - n2), e * 2], "eV",
              "E = 13,6 × (1/%d² − 1/%d²) = %s eV." % (n2, n1, num(e)))


def f_nucl(R):
    k = R.choice(["dec", "dec2", "att", "dm"])
    if k == "dec":
        t, n = R.choice([(5730, 2), (8, 3), (28, 2), (1600, 4), (12, 3), (30, 5)])
        return nq("Un isotopo ha tempo di dimezzamento %d anni. Che frazione resta (in percentuale) dopo %d anni?" % (t, t * n), 100 / 2 ** n, [100 / n, 100 - 100 / 2 ** n, 50 / n, 100 / 2 ** (n + 1)], "%",
                  "Dopo %d dimezzamenti resta (1/2)^%d = %s %%." % (n, n, num(100 / 2 ** n)))
    if k == "dec2":
        m, n = R.choice([(80, 3), (64, 4), (200, 2), (10, 1), (120, 3)])
        return nq("Un campione di %d g di un isotopo radioattivo attraversa %d tempi di dimezzamento. Quanti grammi restano?" % (m, n), m / 2 ** n, [m / n, m / (2 * n), m - m / 2 ** n, m / 2 ** (n + 1)], "g",
                  "%d : 2^%d = %s g." % (m, n, num(m / 2 ** n)))
    if k == "att":
        z, a, kind = R.choice([(92, 238, "α"), (88, 226, "α"), (6, 14, "β⁻"), (19, 40, "β⁻"), (84, 210, "α"), (55, 137, "β⁻")])
        if kind == "α":
            return it("Un nucleo con Z = %d e A = %d emette una particella α. Quali sono i nuovi Z e A?" % (z, a), "Z = %d, A = %d" % (z - 2, a - 4),
                      ["Z = %d, A = %d" % (z - 4, a - 2), "Z = %d, A = %d" % (z + 1, a), "Z = %d, A = %d" % (z - 2, a)], "Una particella α è un nucleo di elio: Z cala di 2, A di 4.")
        return it("Un nucleo con Z = %d e A = %d fa un decadimento β⁻. Quali sono i nuovi Z e A?" % (z, a), "Z = %d, A = %d" % (z + 1, a),
                  ["Z = %d, A = %d" % (z - 1, a), "Z = %d, A = %d" % (z - 2, a - 4), "Z = %d, A = %d" % (z + 1, a - 1)], "Nel β⁻ un neutrone diventa protone: Z aumenta di 1, A resta uguale.")
    dm = R.choice([0.001, 1e-5, 3e-28, 0.0001, 2.9e-28])
    return nq("In una reazione nucleare la massa diminuisce di %s kg. Quanta energia si libera?" % num(dm), dm * C * C, [dm * C, dm * C * C / 2, dm / C ** 2, dm * C * C * 10], "J", "E = Δm c² = %s J." % num(dm * C * C))


def f_clima(R):
    k = R.choice(["grad", "co2", "fuso", "pres"])
    if k == "grad":
        t, h = R.choice([(20, 2), (15, 3), (25, 1.5), (10, 4), (30, 5), (18, 1)])
        return nq("Al livello del mare ci sono %d °C. Che temperatura c’è circa a %s km di quota? (gradiente 6,5 °C/km)" % (t, num(h)), t - 6.5 * h, [t + 6.5 * h, t - h, t - 10 * h, 6.5 * h], "°C",
                  "t = %d − 6,5 × %s = %s °C." % (t, num(h), num(t - 6.5 * h)), neg=True)
    if k == "co2":
        a, b = R.choice([(280, 420), (315, 420), (280, 350), (350, 420), (300, 410)])
        return nq("La CO₂ atmosferica è passata da %d ppm a %d ppm. Di quanto è aumentata in percentuale?" % (a, b), (b - a) * 100 / a, [(b - a) * 100 / b, b - a, b * 100 / a, (b - a) / a], "%",
                  "(%d − %d) : %d × 100 = %s %%." % (b, a, a, num((b - a) * 100 / a)))
    if k == "fuso":
        v, d = R.choice([(4, 1000), (5, 1500), (2, 800), (3, 600), (6, 2400)])
        return nq("Una placca si muove di %d cm all’anno. Quanti km percorre in %d mila anni?" % (v, d), v * d * 1000 / 100000, [v * d, v * d / 1000, v * d * 1000, v * d / 10], "km",
                  "%d cm × %d 000 = %s cm = %s km." % (v, d, num(v * d * 1000), num(v * d * 1000 / 100000)))
    s, p = R.choice([(3, 0.1), (12, 0.35), (25, 0.7), (40, 1), (8, 0.2)])
    return nq("Un’onda sismica P viaggia a 6 km/s e la S a 3,5 km/s. Una stazione registra %d s di ritardo tra P e S. A che distanza è l’epicentro?" % s, s / (1 / 3.5 - 1 / 6),
              [s * 6, s * 3.5, s * 2.5, s / 2.5], "km", "d = Δt : (1/vS − 1/vP) = %d : (1/3,5 − 1/6) = %s km." % (s, num(s / (1 / 3.5 - 1 / 6))))


def f_em(R):
    k = R.choice(["lam", "f", "t", "fot", "int"])
    if k == "lam":
        f, n = R.choice([(100e6, "una radio FM"), (2.4e9, "il wi-fi"), (900e3, "una radio AM"), (5e14, "la luce gialla"), (3e10, "un radar"), (1.5e9, "il GPS")])
        return nq("Qual è la lunghezza d’onda del segnale di %s, con frequenza %s Hz? (c = 3 × 10⁸ m/s)" % (n, num(f)), C / f, [f / C, C * f, C / f * 10, C / f / 2], "m", "λ = c : f = %s m." % num(C / f))
    if k == "f":
        lam = R.choice([3, 0.12, 300, 0.03, 1500, 0.5])
        return nq("Un’onda elettromagnetica ha λ = %s m nel vuoto. Qual è la frequenza?" % num(lam), C / lam, [lam * C, C / lam / 1000, lam / C, C / lam * 2], "Hz", "f = c : λ = %s Hz." % num(C / lam))
    if k == "t":
        d, n = R.choice([(3.84e8, "dalla Luna alla Terra"), (1.5e11, "dal Sole alla Terra"), (3.6e7, "da un satellite geostazionario"), (2.25e11, "da Marte alla Terra (in media)"), (4e6, "attraverso l’Italia")])
        return nq("Quanto impiega un segnale radio ad arrivare %s, percorrendo %s m? (c = 3 × 10⁸ m/s)" % (n, num(d)), d / C, [d * C, C / d, d / C * 60, d / C / 1000], "s", "t = d : c = %s s." % num(d / C))
    if k == "fot":
        f = R.choice([5e14, 1e15, 1e18, 1e9, 6e14])
        return nq("Quanto vale l’energia di un fotone di frequenza %s Hz? (h = 6,63 × 10⁻³⁴ J·s)" % num(f), HP * f, [HP / f, f / HP, HP * f * 10, HP * C], "J", "E = h f = %s J." % num(HP * f))
    p, r = R.choice([(100, 2), (1000, 10), (60, 1), (500, 5), (2000, 20)])
    return nq("Una sorgente isotropa emette %d W di onde elettromagnetiche. Quanto vale l’intensità a %d m?" % (p, r), p / (4 * math.pi * r * r), [p / (4 * math.pi * r), p / r ** 2, p / (2 * math.pi * r * r), p * r], "W/m²",
              "I = P : (4π r²) = %s W/m²." % num(p / (4 * math.pi * r * r)))


def f_qn(R):
    return f_q(R) if R.random() < 0.5 else f_nucl(R)


def UNITS(grade):
    return [
        H("FI", "campo-magnetico", "Il campo magnetico", "Campo magnetico",
          "Lo studente descrive i fenomeni magnetici, il campo magnetico di fili, spire e solenoidi, la forza su un filo percorso da corrente, la forza di Lorentz e il moto delle cariche.",
          "magneti, linee di campo, esperienze di Oersted, Faraday e Ampère, campo di un filo, legge di Biot-Savart, spira, solenoide, forza su un filo, forza di Lorentz, moto di una carica, motore elettrico",
          "F = q v B e F = B I L", "Una carica in moto perpendicolare a B descrive una circonferenza.",
          ["Una corrente crea un campo magnetico: per un filo B = μ₀ I : (2π r), per un solenoide B = μ₀ N I : L.",
           "Un filo percorso da corrente in un campo subisce F = B I L; due fili paralleli con correnti concordi si attraggono.",
           "Una carica in moto subisce la forza di Lorentz F = q v B, perpendicolare alla velocità: descrive una circonferenza di raggio r = m v : (q B)."],
          [("Un filo di 0,5 m con 2 A in un campo di 0,4 T perpendicolare. Forza?", ["F = B I L.", "0,4 × 2 × 0,5."], "0,4 N.")],
          [("La forza di Lorentz cambia la velocità in modulo.", "È perpendicolare alla velocità: cambia solo la direzione."), ("Il campo magnetico ha poli separabili.", "Non esistono monopoli magnetici: le linee sono chiuse.")],
          [("Come funziona un motore elettrico?", "Una spira percorsa da corrente in un campo magnetico subisce una coppia e ruota."), ("Che cos’è il tesla?", "L’unità del campo magnetico: 1 T = 1 N : (A·m).")],
          [("Leggi", [("legge di Biot-Savart", "B = μ₀ I : (2π r) per un filo"), ("forza di Lorentz", "F = q v B"), ("forza su un filo", "F = B I L"), ("campo del solenoide", "B = μ₀ N I : L"),
                      ("esperienza di Oersted", "la corrente devia l’ago magnetico"), ("esperienza di Ampère", "due fili con correnti concordi si attraggono"), ("raggio della traiettoria", "r = m v : (q B)")],
            "Che cosa esprime: {k}?", "Che cosa esprime la formula {v}?"),
           ("Concetti", [("tesla", "unità del campo magnetico"), ("linee di campo magnetico", "linee chiuse senza inizio né fine"), ("permeabilità magnetica del vuoto", "μ₀ = 4π × 10⁻⁷ T·m/A"),
                         ("materiale ferromagnetico", "si magnetizza molto, come il ferro"), ("materiale diamagnetico", "è debolmente respinto dal campo"), ("spettrometro di massa", "separa gli ioni con un campo magnetico"),
                         ("ciclotrone", "acceleratore che fa girare le particelle in un campo"), ("regola della mano destra", "dà il verso di forza e campo")],
            "Che cos’è: {k}?", D),
           ("Materiali e usi", {"i materiali ferromagnetici": ["ferro", "nichel", "cobalto", "magnetite", "acciaio"], "i dispositivi basati sulla forza magnetica": ["motore elettrico", "altoparlante", "spettrometro di massa", "ciclotrone", "amperometro"],
                                "i fenomeni del campo magnetico terrestre": ["orientamento della bussola", "aurore polari", "fasce di Van Allen", "inversioni dei poli"]})],
          ["F = q v B per una carica perpendicolare a B.", "Le linee di campo magnetico sono chiuse.", "Due fili con correnti concordi si attraggono.", "Il tesla misura il campo magnetico.",
           "La forza di Lorentz non cambia il modulo della velocità.", "Una corrente produce un campo magnetico.", "Il ferro è ferromagnetico."],
          [("Le correnti concordi si respingono.", "Si attraggono."), ("Esistono monopoli magnetici.", "Non sono mai stati osservati."), ("La forza di Lorentz aumenta il modulo della velocità.", "Cambia solo la direzione."),
           ("Il campo di un filo cresce con la distanza.", "Diminuisce come 1 : r."), ("Il rame è ferromagnetico.", "Non lo è.")],
          "il magnetismo", "energy", calc=f_mag),

        H("FI", "induzione-elettromagnetica", "Induzione elettromagnetica e corrente alternata", "Induzione",
          "Lo studente studia il flusso del campo magnetico, la legge di Faraday-Neumann-Lenz, l’autoinduzione, l’alternatore, la corrente alternata, il trasformatore e la produzione di energia elettrica.",
          "flusso magnetico, weber, fem indotta, legge di Faraday-Neumann, legge di Lenz, correnti di Foucault, autoinduzione, induttanza, alternatore, corrente alternata, valore efficace, trasformatore",
          "fem = − ΔΦ : Δt", "La corrente indotta si oppone alla variazione che l’ha prodotta (Lenz).",
          ["Il flusso è Φ = B S cos θ (weber). Se il flusso cambia nasce una fem indotta: fem = − N ΔΦ : Δt.",
           "Legge di Lenz: la corrente indotta ha verso tale da opporsi alla variazione del flusso (il segno meno).",
           "L’alternatore produce corrente alternata; il trasformatore cambia la tensione: V₂ : V₁ = N₂ : N₁. Il valore efficace è Vmax : √2."],
          [("Primario 1000 spire a 230 V, secondario 50 spire. Tensione in uscita?", ["V₂ = V₁ × N₂ : N₁.", "230 × 50 : 1000."], "11,5 V.")],
          [("Un magnete fermo vicino a una bobina produce corrente.", "Serve una variazione del flusso."), ("Il trasformatore funziona con la corrente continua.", "Funziona solo con corrente variabile.")],
          [("Perché l’energia elettrica viaggia ad alta tensione?", "A parità di potenza la corrente è minore e si perde meno energia per effetto Joule."), ("Che cosa sono le correnti di Foucault?", "Correnti indotte nei conduttori massicci che li scaldano e li frenano.")],
          [("Leggi e grandezze", [("flusso magnetico", "Φ = B S cos θ"), ("legge di Faraday-Neumann", "fem = − N ΔΦ : Δt"), ("legge di Lenz", "la corrente indotta si oppone alla variazione"),
                                  ("fem di una sbarretta in moto", "fem = B L v"), ("rapporto del trasformatore", "V₂ : V₁ = N₂ : N₁"), ("valore efficace", "Veff = Vmax : √2"), ("weber", "unità del flusso magnetico")],
            "Che cosa esprime: {k}?", "Che cosa esprime {v}?"),
           ("Dispositivi", [("alternatore", "trasforma energia meccanica in elettrica"), ("trasformatore", "cambia la tensione alternata"), ("dinamo", "produce corrente con un magnete che ruota"),
                            ("piano a induzione", "scalda la pentola con correnti indotte"), ("freno elettromagnetico", "frena con le correnti di Foucault"), ("caricabatterie wireless", "trasferisce energia per induzione"),
                            ("metal detector", "rileva metalli con il campo indotto")],
            "Come funziona: {k}?", D),
           ("Situazioni", {"le situazioni con corrente indotta": ["magnete che entra in una bobina", "spira che ruota in un campo", "campo che aumenta in una bobina", "sbarretta che scorre su binari in un campo"],
                           "le situazioni senza corrente indotta": ["magnete fermo dentro la bobina", "spira ferma in un campo costante", "spira che scorre in un campo uniforme senza cambiare flusso"],
                           "le centrali che usano l’alternatore": ["centrale idroelettrica", "centrale termoelettrica", "parco eolico", "centrale geotermica", "centrale nucleare"]})],
          ["Una variazione di flusso produce una fem.", "La corrente indotta si oppone alla variazione (Lenz).", "Il trasformatore funziona con corrente alternata.", "Veff = Vmax : √2.", "L’alternatore produce corrente alternata.",
           "Il flusso si misura in weber.", "Le linee ad alta tensione riducono le perdite."],
          [("Un magnete fermo induce corrente.", "Serve una variazione di flusso."), ("Il trasformatore funziona in corrente continua.", "Solo con corrente variabile."), ("Veff = Vmax × √2.", "Veff = Vmax : √2."),
           ("La corrente indotta favorisce la variazione.", "Si oppone."), ("Il flusso si misura in tesla.", "Si misura in weber.")],
          "l’induzione", "energy", calc=f_ind),

        H("FI", "onde-elettromagnetiche", "Le equazioni di Maxwell e le onde elettromagnetiche", "Onde elettromagnetiche",
          "Lo studente collega campo elettrico e magnetico con le equazioni di Maxwell, descrive le onde elettromagnetiche, la loro velocità, energia e lo spettro con le applicazioni.",
          "corrente di spostamento, equazioni di Maxwell, onde elettromagnetiche, velocità della luce, campi E e B perpendicolari, energia, intensità, spettro elettromagnetico, antenne, polarizzazione",
          "c = λ f = 3 × 10⁸ m/s", "Nelle onde elettromagnetiche E e B oscillano perpendicolari tra loro e alla direzione di propagazione.",
          ["Maxwell: un campo elettrico variabile crea un campo magnetico e viceversa; insieme si propagano come onda.", "Le onde elettromagnetiche viaggiano nel vuoto a c = 1 : √(ε₀ μ₀) ≈ 3 × 10⁸ m/s.",
           "Lo spettro va dalle onde radio (λ lunghe) ai raggi gamma (λ cortissime); l’energia di un fotone cresce con la frequenza."],
          [("Una radio FM trasmette a 100 MHz. Qual è la lunghezza d’onda?", ["λ = c : f.", "3 × 10⁸ : 10⁸."], "3 m.")],
          [("Le onde radio sono più veloci della luce.", "Tutte le onde elettromagnetiche hanno la stessa velocità nel vuoto."), ("Le microonde sono onde sonore.", "Sono onde elettromagnetiche.")],
          [("Chi dimostrò l’esistenza delle onde elettromagnetiche?", "Heinrich Hertz, nel 1887."), ("Perché i raggi UV sono pericolosi?", "I fotoni hanno abbastanza energia da danneggiare il DNA.")],
          [("Spettro", [("onde radio", "comunicazioni radio e TV"), ("microonde", "forno a microonde e radar"), ("infrarosso", "telecomandi e termocamere"), ("luce visibile", "vista"), ("ultravioletto", "sterilizzazione e abbronzatura"),
                        ("raggi X", "radiografie"), ("raggi gamma", "radioterapia")],
            "A che cosa serve: {k}?", "Quale radiazione si usa per {v}?"),
           ("Concetti", [("corrente di spostamento", "campo elettrico variabile che genera un campo magnetico"), ("equazioni di Maxwell", "descrivono tutti i fenomeni elettromagnetici"), ("onda elettromagnetica", "campi E e B che si propagano"),
                         ("velocità della luce", "1 : √(ε₀ μ₀)"), ("antenna", "emette o riceve onde elettromagnetiche"), ("polarizzazione", "direzione di oscillazione del campo elettrico"), ("Hertz", "scopritore sperimentale delle onde")],
            "Che cos’è: {k}?", D),
           ("Ordine", {"le radiazioni con λ maggiore della luce visibile": ["onde radio", "microonde", "infrarosso", "onde radio AM", "onde del radar"], "le radiazioni con λ minore della luce visibile": ["ultravioletto", "raggi X", "raggi gamma"],
                       "le radiazioni ionizzanti": ["raggi X", "raggi gamma", "ultravioletto lontano"]})],
          ["Tutte le onde elettromagnetiche hanno velocità c nel vuoto.", "E e B sono perpendicolari.", "c = λ f.", "Maxwell previde le onde elettromagnetiche.", "Hertz le produsse in laboratorio.",
           "I raggi gamma hanno la frequenza più alta.", "Le onde elettromagnetiche si propagano nel vuoto."],
          [("Le onde radio sono più veloci della luce.", "Hanno la stessa velocità."), ("Le onde elettromagnetiche servono di un mezzo.", "Si propagano nel vuoto."), ("I raggi X hanno λ più lunga delle onde radio.", "È molto più corta."),
           ("E e B sono paralleli.", "Sono perpendicolari."), ("Le microonde sono onde sonore.", "Sono elettromagnetiche.")],
          "le onde elettromagnetiche", "waves-and-light", calc=f_em),

        H("FI", "relativita-ristretta", "La relatività ristretta", "Relatività ristretta",
          "Lo studente conosce i postulati di Einstein, la relatività della simultaneità, la dilatazione dei tempi, la contrazione delle lunghezze, la composizione delle velocità e l’equivalenza massa-energia.",
          "esperimento di Michelson-Morley, postulati di Einstein, simultaneità, dilatazione dei tempi, contrazione delle lunghezze, fattore di Lorentz, trasformazioni di Lorentz, composizione delle velocità, E = m c², quantità di moto relativistica",
          "γ = 1 : √(1 − v²/c²)", "Nessun corpo con massa raggiunge la velocità della luce; E = m c².",
          ["Postulati: le leggi della fisica sono uguali in tutti i sistemi inerziali; la luce ha la stessa velocità c per tutti.",
           "Un orologio in moto va più lento: Δt = γ Δt₀. Un oggetto in moto è più corto nella direzione del moto: L = L₀ : γ.",
           "Le velocità si compongono con (u + v) : (1 + u v/c²). Massa ed energia sono equivalenti: E = m c²."],
          [("A v = 0,6 c quanto vale γ?", ["1 − 0,36 = 0,64.", "√0,64 = 0,8 → γ = 1 : 0,8."], "1,25.")],
          [("La contrazione è un’illusione ottica.", "È un effetto reale delle misure di lunghezza."), ("Sommando due velocità vicine a c si supera c.", "La composizione relativistica dà sempre meno di c.")],
          [("Perché i muoni arrivano al suolo?", "La dilatazione dei tempi allunga la loro vita media vista da noi."), ("Che cosa dimostrò Michelson-Morley?", "Che non c’è un vento d’etere: la luce ha sempre la stessa velocità.")],
          [("Effetti", [("dilatazione dei tempi", "un orologio in moto va più lento"), ("contrazione delle lunghezze", "un corpo in moto è più corto"), ("relatività della simultaneità", "eventi simultanei per uno non lo sono per un altro"),
                        ("equivalenza massa-energia", "E = m c²"), ("composizione delle velocità", "(u + v) : (1 + u v/c²)"), ("velocità limite", "nessun corpo con massa raggiunge c"), ("tempo proprio", "tempo misurato nel sistema in cui l’orologio è fermo")],
            "Che cos’è: {k}?", D),
           ("Esperimenti e prove", [("Michelson-Morley", "assenza dell’etere"), ("muoni cosmici al suolo", "dilatazione dei tempi"), ("orologi atomici in aereo", "dilatazione dei tempi misurata"),
                                    ("acceleratori di particelle", "le particelle non superano c"), ("difetto di massa dei nuclei", "equivalenza massa-energia"), ("satelliti GPS", "correzioni relativistiche degli orologi")],
            "Che cosa ha mostrato o richiede: {k}?", "Quale esperimento è legato a: {v}?"),
           ("Grandezze", {"le grandezze uguali per tutti gli osservatori inerziali": ["velocità della luce nel vuoto", "massa a riposo", "intervallo spazio-temporale", "carica elettrica"],
                          "le grandezze che dipendono dall’osservatore": ["durata di un intervallo di tempo", "lunghezza di un oggetto", "simultaneità di due eventi", "energia cinetica"],
                          "gli scienziati della relatività": ["Einstein", "Lorentz", "Minkowski", "Poincaré"]})],
          ["La velocità della luce è uguale per tutti gli osservatori inerziali.", "Un orologio in moto va più lento.", "Un corpo in moto è più corto nella direzione del moto.", "E = m c².", "Nessun corpo con massa raggiunge c.",
           "γ vale 1,25 a 0,6 c.", "La simultaneità dipende dall’osservatore."],
          [("La velocità della luce dipende dall’osservatore.", "È uguale per tutti."), ("Un orologio in moto va più veloce.", "Va più lento."), ("Un corpo in moto è più lungo.", "È più corto."),
           ("Si può superare c sommando velocità.", "La composizione dà sempre meno di c."), ("E = m c.", "E = m c².")],
          "la relatività", "forces-and-motion", calc=f_rel),

        H("FI", "fisica-quantistica-e-nucleare", "Fisica quantistica e nucleare", "Fisica quantistica",
          "Lo studente descrive la crisi della fisica classica, il quanto di Planck, l’effetto fotoelettrico, il modello di Bohr, il dualismo onda-particella, il principio di indeterminazione e la radioattività.",
          "corpo nero, quanto di Planck, effetto fotoelettrico, fotone, effetto Compton, modello di Bohr, spettri atomici, de Broglie, dualismo onda-particella, Heisenberg, nucleo, radioattività, dimezzamento, fissione, fusione",
          "E = h f", "Un elettrone è emesso solo se h f supera il lavoro di estrazione.",
          ["Planck: l’energia è scambiata in quanti E = h f. Einstein spiegò l’effetto fotoelettrico con i fotoni: Ec = h f − W.",
           "Bohr: l’elettrone dell’idrogeno sta su livelli En = −13,6 eV : n²; i salti emettono fotoni. De Broglie: anche le particelle hanno λ = h : p.",
           "Heisenberg: posizione e quantità di moto non si conoscono insieme con precisione. I nuclei instabili decadono (α, β, γ) con un tempo di dimezzamento."],
          [("Fotoni di 5 eV su un metallo con W = 2 eV. Energia cinetica massima?", ["Ec = h f − W.", "5 − 2 = 3."], "3 eV.")],
          [("Una luce più intensa emette elettroni più veloci.", "La velocità dipende dalla frequenza; l’intensità cambia il numero di elettroni."), ("Il dimezzamento è il tempo in cui il campione sparisce.", "È il tempo in cui si dimezza.")],
          [("Che cos’è la fissione?", "La rottura di un nucleo pesante, come l’uranio, con liberazione di energia."), ("Che cos’è la fusione?", "L’unione di nuclei leggeri, come nel Sole.")],
          [("Concetti", [("quanto", "pacchetto di energia h f"), ("fotone", "particella della luce"), ("lavoro di estrazione", "energia minima per estrarre un elettrone"), ("lunghezza d’onda di de Broglie", "λ = h : p"),
                         ("principio di indeterminazione", "posizione e quantità di moto non si conoscono insieme"), ("tempo di dimezzamento", "tempo in cui si dimezzano i nuclei"), ("fissione", "rottura di un nucleo pesante"),
                         ("fusione", "unione di nuclei leggeri")],
            "Che cos’è: {k}?", D),
           ("Scienziati", [("Planck", "quanti di energia"), ("Einstein", "spiegazione dell’effetto fotoelettrico"), ("Bohr", "livelli energetici dell’atomo"), ("de Broglie", "onde di materia"),
                           ("Heisenberg", "principio di indeterminazione"), ("Compton", "urto fotone-elettrone"), ("Fermi", "primo reattore nucleare"), ("Marie Curie", "studio della radioattività")],
            "A quale scoperta è legato: {k}?", "Chi è legato a: {v}?"),
           ("Radiazioni", {"le radiazioni nucleari": ["particelle α", "particelle β", "raggi γ", "neutroni"], "gli isotopi radioattivi usati in medicina e datazione": ["carbonio-14", "iodio-131", "tecnezio-99m", "uranio-238", "potassio-40"],
                           "le applicazioni della fisica nucleare": ["datazione al carbonio-14", "radioterapia", "centrali nucleari", "PET in medicina", "sterilizzazione"]})],
          ["E = h f.", "Nell’effetto fotoelettrico conta la frequenza.", "Le particelle hanno anche proprietà ondulatorie.", "Nel decadimento α Z diminuisce di 2.", "Nel Sole avviene la fusione nucleare.",
           "Fermi costruì il primo reattore nucleare.", "Dopo due dimezzamenti resta un quarto del campione."],
          [("Più intensità dà elettroni più veloci.", "Conta la frequenza."), ("Nel decadimento α A diminuisce di 2.", "Diminuisce di 4."), ("Nel Sole avviene la fissione.", "Avviene la fusione."),
           ("Dopo un dimezzamento il campione sparisce.", "Ne resta metà."), ("Gli elettroni sono solo particelle.", "Hanno anche comportamento ondulatorio.")],
          "la fisica quantistica", "energy", calc=f_qn),

        H("CH", "chimica-organica", "La chimica organica", "Chimica organica",
          "Lo studente descrive l’atomo di carbonio e l’ibridazione, idrocarburi saturi e insaturi, isomeria, i principali gruppi funzionali, la nomenclatura IUPAC di base e le reazioni tipiche.",
          "carbonio, ibridazione sp³, sp², sp, alcani, alcheni, alchini, idrocarburi aromatici, benzene, isomeria, gruppi funzionali, alcoli, aldeidi, chetoni, acidi carbossilici, esteri, ammine, polimeri",
          "Il carbonio forma quattro legami", "I gruppi funzionali decidono le proprietà delle molecole organiche.",
          ["Il carbonio ha quattro elettroni di valenza e forma catene e anelli. Ibridazione sp³ (legami singoli), sp² (doppi), sp (tripli).",
           "Alcani CₙH₂ₙ₊₂ (desinenza -ano), alcheni CₙH₂ₙ (-ene), alchini CₙH₂ₙ₋₂ (-ino); il benzene è aromatico.",
           "I gruppi funzionali: –OH alcoli, –CHO aldeidi, –CO– chetoni, –COOH acidi carbossilici, –COO– esteri, –NH₂ ammine."],
          [("Qual è la formula del propano?", ["È un alcano con 3 carboni.", "CₙH₂ₙ₊₂ con n = 3."], "C₃H₈.")],
          [("Gli isomeri hanno formule molecolari diverse.", "Hanno la stessa formula molecolare e struttura diversa."), ("Il benzene è un alchene qualunque.", "È aromatico: gli elettroni sono delocalizzati.")],
          [("Che cos’è un polimero?", "Una macromolecola formata da tante unità ripetute (monomeri), come il polietilene."), ("Perché il metano brucia?", "Con l’ossigeno dà CO₂ e acqua liberando energia (combustione).")],
          [("Gruppi funzionali", [("etanolo", "alcol"), ("metanolo", "alcol"), ("propanone (acetone)", "chetone"), ("etanale", "aldeide"), ("formaldeide", "aldeide"), ("acido acetico", "acido carbossilico"),
                                  ("acido formico", "acido carbossilico"), ("acetato di etile", "estere"), ("metilammina", "ammina"), ("etano", "alcano"), ("etene", "alchene"), ("etino", "alchino")],
            "A quale classe appartiene: {k}?", None),
           ("Formule", [("metano", "CH₄"), ("etano", "C₂H₆"), ("propano", "C₃H₈"), ("butano", "C₄H₁₀"), ("etene", "C₂H₄"), ("etino", "C₂H₂"), ("benzene", "C₆H₆"), ("etanolo", "C₂H₅OH")],
            "Qual è la formula di {k}?", "Quale sostanza ha formula {v}?"),
           ("Ibridazione e reazioni", {"gli idrocarburi con carbonio sp³": ["metano", "etano", "propano", "butano", "cicloesano"], "gli idrocarburi con carbonio sp²": ["etene", "propene", "benzene", "butadiene"],
                                       "le reazioni tipiche degli alcheni": ["addizione di idrogeno", "addizione di bromo", "idratazione", "polimerizzazione"],
                                       "i polimeri": ["polietilene", "PVC", "nylon", "polistirene", "PET"]})],
          ["Il carbonio forma quattro legami.", "Il metano è CH₄.", "L’etanolo è un alcol.", "L’acido acetico contiene il gruppo –COOH.", "Gli isomeri hanno la stessa formula molecolare.",
           "Gli alcheni hanno un doppio legame.", "Il benzene è aromatico."],
          [("Il carbonio forma due legami.", "Ne forma quattro."), ("Gli alcani hanno doppi legami.", "Hanno solo legami singoli."), ("L’acetone è un alcol.", "È un chetone."),
           ("Gli isomeri hanno formule diverse.", "Hanno la stessa formula molecolare."), ("L’etino ha un doppio legame.", "Ha un triplo legame.")],
          "la chimica organica", "matter"),

        H("BI", "biochimica-e-metabolismo", "Biochimica e metabolismo energetico", "Metabolismo",
          "Lo studente descrive struttura e funzione delle biomolecole, gli enzimi, l’ATP, la glicolisi, il ciclo di Krebs, la catena di trasporto degli elettroni, la fermentazione e la fotosintesi.",
          "biomolecole, enzimi, sito attivo, cofattori, ATP, metabolismo, catabolismo, anabolismo, glicolisi, ciclo di Krebs, catena respiratoria, fosforilazione ossidativa, fermentazione, fotosintesi, ciclo di Calvin",
          "Glucosio + O₂ → CO₂ + H₂O + ATP", "La respirazione cellulare produce circa 30–32 ATP per glucosio.",
          ["Gli enzimi accelerano le reazioni abbassando l’energia di attivazione; agiscono sul substrato nel sito attivo.",
           "Respirazione: glicolisi nel citoplasma (glucosio → 2 piruvato, 2 ATP), ciclo di Krebs nei mitocondri, catena respiratoria che produce la maggior parte dell’ATP.",
           "Senza ossigeno avviene la fermentazione (lattica o alcolica). Nella fotosintesi la fase luminosa produce ATP e NADPH, il ciclo di Calvin fissa la CO₂."],
          [("Dove avviene la glicolisi?", ["Non richiede ossigeno.", "Avviene fuori dai mitocondri."], "Nel citoplasma.")],
          [("La fermentazione produce più ATP della respirazione.", "Ne produce solo 2 per glucosio."), ("Le piante non respirano.", "Le piante respirano nei mitocondri, oltre a fare la fotosintesi.")],
          [("Perché i muscoli fanno male dopo uno sforzo intenso?", "Senza abbastanza ossigeno fanno fermentazione lattica."), ("Che cos’è l’ATP?", "La molecola che trasporta energia nella cellula.")],
          [("Fasi", [("glicolisi", "citoplasma"), ("ciclo di Krebs", "matrice mitocondriale"), ("catena di trasporto degli elettroni", "membrana interna del mitocondrio"), ("fase luminosa", "membrane dei tilacoidi"),
                     ("ciclo di Calvin", "stroma del cloroplasto"), ("fermentazione", "citoplasma"), ("sintesi proteica", "ribosomi")],
            "Dove avviene: {k}?", None),
           ("Molecole", [("ATP", "trasporta energia"), ("NADH", "trasporta elettroni alla catena respiratoria"), ("piruvato", "prodotto finale della glicolisi"), ("acetil-CoA", "entra nel ciclo di Krebs"),
                         ("ossigeno", "accettore finale degli elettroni"), ("RuBisCO", "enzima che fissa la CO₂"), ("clorofilla", "assorbe la luce"), ("acido lattico", "prodotto della fermentazione nei muscoli")],
            "Che ruolo ha: {k}?", D),
           ("Processi", {"i processi catabolici": ["glicolisi", "ciclo di Krebs", "digestione dell’amido", "beta-ossidazione dei grassi", "fermentazione"], "i processi anabolici": ["fotosintesi", "sintesi delle proteine", "sintesi del glicogeno", "replicazione del DNA", "ciclo di Calvin"],
                         "i prodotti della fermentazione alcolica": ["etanolo", "anidride carbonica"]})],
          ["La glicolisi avviene nel citoplasma.", "Il ciclo di Krebs avviene nei mitocondri.", "L’ossigeno è l’accettore finale degli elettroni.", "La fermentazione produce poco ATP.", "Gli enzimi abbassano l’energia di attivazione.",
           "Il ciclo di Calvin fissa la CO₂.", "Le piante respirano."],
          [("La glicolisi avviene nei mitocondri.", "Avviene nel citoplasma."), ("La fermentazione richiede ossigeno.", "Avviene senza ossigeno."), ("Le piante non respirano.", "Respirano."),
           ("Gli enzimi si consumano.", "Restano invariati."), ("Il ciclo di Calvin produce ossigeno.", "L’ossigeno viene dalla fase luminosa.")],
          "il metabolismo", "living-things-and-ecosystems"),

        H("BI", "biotecnologie", "Le biotecnologie", "Biotecnologie",
          "Lo studente descrive le tecniche del DNA ricombinante, enzimi di restrizione, PCR, elettroforesi, sequenziamento, clonazione, CRISPR, OGM e le applicazioni in medicina e agricoltura.",
          "biotecnologie, DNA ricombinante, enzimi di restrizione, ligasi, plasmidi, vettori, PCR, elettroforesi su gel, sequenziamento, clonazione, cellule staminali, CRISPR-Cas9, OGM, terapia genica, vaccini a mRNA",
          "Tagliare, copiare e incollare il DNA", "La PCR copia un tratto di DNA milioni di volte in poche ore.",
          ["Gli enzimi di restrizione tagliano il DNA in punti precisi; la ligasi unisce i frammenti; i plasmidi portano geni nei batteri.",
           "La PCR amplifica il DNA con cicli di denaturazione, appaiamento dei primer ed estensione. L’elettroforesi separa i frammenti per lunghezza.",
           "CRISPR-Cas9 modifica un gene in un punto scelto. Le biotecnologie servono per farmaci (insulina), diagnosi, vaccini, piante resistenti."],
          [("Come si produce l’insulina umana con i batteri?", ["Si inserisce il gene dell’insulina in un plasmide.", "Il batterio la produce."], "Con il DNA ricombinante.")],
          [("Nell’elettroforesi i frammenti grandi corrono di più.", "I frammenti piccoli corrono più lontano."), ("Un OGM è sempre un organismo clonato.", "Un OGM ha un DNA modificato; la clonazione fa copie identiche.")],
          [("Che cos’è un primer?", "Un breve filamento di DNA che indica alla polimerasi dove iniziare."), ("Che cos’è la terapia genica?", "Introdurre un gene funzionante per curare una malattia genetica.")],
          [("Tecniche", [("enzima di restrizione", "taglia il DNA in sequenze precise"), ("DNA ligasi", "unisce frammenti di DNA"), ("plasmide", "piccolo DNA circolare usato come vettore"), ("PCR", "amplifica un tratto di DNA"),
                         ("elettroforesi", "separa i frammenti di DNA per dimensione"), ("CRISPR-Cas9", "modifica un gene in un punto preciso"), ("Taq polimerasi", "polimerasi resistente al calore della PCR"),
                         ("sequenziamento", "legge l’ordine delle basi")],
            "Che cosa fa: {k}?", D),
           ("Applicazioni", [("insulina ricombinante", "cura del diabete"), ("mais Bt", "resistenza agli insetti"), ("impronta genetica", "identificazione in medicina legale"), ("vaccino a mRNA", "prevenzione delle infezioni"),
                             ("terapia genica", "cura di malattie genetiche"), ("pecora Dolly", "primo mammifero clonato da una cellula adulta"), ("riso dorato", "più vitamina A")],
            "A che cosa serve o che cos’è: {k}?", D),
           ("Fasi e organismi", {"le fasi di un ciclo di PCR": ["denaturazione", "appaiamento dei primer", "estensione"], "gli strumenti per inserire DNA nelle cellule": ["plasmidi", "virus modificati", "elettroporazione", "microiniezione"],
                                 "gli organismi modello delle biotecnologie": ["Escherichia coli", "lievito", "topo di laboratorio", "moscerino della frutta", "Arabidopsis"]})],
          ["La PCR amplifica il DNA.", "Gli enzimi di restrizione tagliano il DNA.", "Nell’elettroforesi i frammenti piccoli corrono di più.", "I plasmidi sono vettori.", "CRISPR modifica geni.",
           "L’insulina si produce con batteri modificati.", "Dolly fu clonata da una cellula adulta."],
          [("La PCR taglia il DNA.", "Lo amplifica."), ("I frammenti grandi corrono di più.", "Corrono di più quelli piccoli."), ("La ligasi taglia il DNA.", "Lo unisce."),
           ("Dolly era un OGM.", "Era un clone."), ("La Taq polimerasi si distrugge col calore.", "Resiste al calore.")],
          "le biotecnologie", "living-things-and-ecosystems"),

        H("ST", "tettonica-delle-placche", "La tettonica delle placche", "Tettonica delle placche",
          "Lo studente descrive l’interno della Terra con le onde sismiche, la deriva dei continenti, l’espansione dei fondali, i margini di placca, i fenomeni sismici e vulcanici e l’orogenesi.",
          "struttura interna, discontinuità, onde sismiche P e S, litosfera, astenosfera, Wegener, espansione dei fondali, paleomagnetismo, margini divergenti, convergenti e trasformi, subduzione, punti caldi, orogenesi",
          "Le placche si muovono su un mantello che fluisce", "Ai margini divergenti nasce crosta, ai convergenti sprofonda.",
          ["Le onde sismiche mostrano crosta, mantello e nucleo; le onde S non attraversano il nucleo esterno liquido.",
           "Wegener propose la deriva dei continenti; Hess l’espansione dei fondali oceanici, provata dal paleomagnetismo.",
           "Margini divergenti (dorsali), convergenti (subduzione, catene montuose) e trasformi (faglie come quella di San Andreas)."],
          [("Le onde P arrivano 20 s prima delle S. Se vP = 6 e vS = 3,5 km/s, distanza?", ["d = Δt : (1/vS − 1/vP).", "20 : 0,119."], "Circa 168 km.")],
          [("I continenti galleggiano sul magma liquido.", "L’astenosfera è solida ma plastica."), ("Tutti i vulcani sono ai margini.", "Esistono vulcani di punto caldo, come le Hawaii.")],
          [("Perché le Alpi si sono formate?", "Per la collisione tra la placca africana (con l’Adria) e quella euroasiatica."), ("Che cos’è il paleomagnetismo?", "La registrazione nelle rocce del campo magnetico del passato.")],
          [("Margini", [("dorsale medio-atlantica", "margine divergente"), ("Rift Valley africana", "margine divergente"), ("Islanda", "margine divergente"), ("Ande", "margine convergente"),
                        ("Giappone", "margine convergente"), ("Himalaya", "margine convergente"), ("faglia di San Andreas", "margine trasforme"), ("faglia anatolica settentrionale", "margine trasforme"), ("Hawaii", "punto caldo")],
            "Che tipo di struttura è: {k}?", None),
           ("Concetti", [("litosfera", "parte rigida divisa in placche"), ("astenosfera", "mantello plastico sotto la litosfera"), ("subduzione", "una placca scende sotto un’altra"), ("dorsale oceanica", "catena sottomarina dove nasce crosta"),
                         ("fossa oceanica", "depressione profonda dove avviene la subduzione"), ("punto caldo", "risalita di magma dal mantello profondo"), ("orogenesi", "formazione delle catene montuose"),
                         ("discontinuità di Moho", "confine tra crosta e mantello")],
            "Che cos’è: {k}?", D),
           ("Prove e fenomeni", {"le prove della deriva dei continenti": ["forma delle coste", "fossili uguali su continenti lontani", "rocce simili", "tracce di antichi ghiacciai"],
                                 "le prove dell’espansione dei fondali": ["anomalie magnetiche simmetriche", "età delle rocce crescente dalla dorsale", "sedimenti più sottili vicino alla dorsale", "flusso di calore elevato"],
                                 "i vulcani italiani attivi": ["Etna", "Stromboli", "Vesuvio", "Campi Flegrei", "Vulcano"]})],
          ["Le onde S non attraversano il nucleo esterno.", "Wegener propose la deriva dei continenti.", "Alle dorsali nasce nuova crosta.", "Le Hawaii sono un punto caldo.", "L’Himalaya è nato da una collisione.",
           "L’astenosfera è plastica.", "La faglia di San Andreas è un margine trasforme."],
          [("Le onde S attraversano il nucleo esterno.", "Non lo attraversano."), ("Le placche galleggiano su magma liquido.", "L’astenosfera è plastica, non liquida."), ("Le Ande sono un margine divergente.", "Sono convergenti."),
           ("Alle fosse nasce crosta.", "Alle fosse la crosta sprofonda."), ("Le Hawaii sono su un margine.", "Sono su un punto caldo.")],
          "la tettonica", "earths-systems", calc=f_clima),

        H("ST", "atmosfera-e-cambiamenti-climatici", "Atmosfera, clima e cambiamenti climatici", "Atmosfera e clima",
          "Lo studente descrive bilancio energetico, effetto serra, circolazione atmosferica, fenomeni meteorologici, classificazione dei climi, cambiamenti climatici e strategie di mitigazione e adattamento.",
          "bilancio radiativo, albedo, effetto serra, gas serra, circolazione generale, celle di Hadley, venti, cicloni e anticicloni, fronti, climi, ciclo del carbonio, riscaldamento globale, IPCC, mitigazione, adattamento",
          "Più gas serra, più calore trattenuto", "La CO₂ è passata da circa 280 ppm (1750) a oltre 420 ppm.",
          ["La Terra riceve energia dal Sole e la riemette come infrarosso; i gas serra trattengono parte di questa energia.",
           "La circolazione atmosferica (celle di Hadley, Ferrel, polari) e le correnti oceaniche distribuiscono il calore.",
           "Bruciando combustibili fossili la CO₂ aumenta e la temperatura media sale: lo studiano i rapporti dell’IPCC. Si risponde con mitigazione e adattamento."],
          [("Perché lo scioglimento dei ghiacci accelera il riscaldamento?", ["Il ghiaccio riflette molta luce.", "Il mare scuro ne assorbe di più."], "Perché diminuisce l’albedo.")],
          [("Tempo meteorologico e clima sono la stessa cosa.", "Il tempo è di oggi; il clima è la media di almeno 30 anni."), ("Il buco dell’ozono causa il riscaldamento globale.", "Sono problemi diversi; il riscaldamento dipende dai gas serra.")],
          [("Che cos’è l’albedo?", "La frazione di luce solare riflessa da una superficie."), ("Che differenza c’è tra mitigazione e adattamento?", "La mitigazione riduce le emissioni; l’adattamento riduce i danni.")],
          [("Concetti", [("albedo", "frazione della luce riflessa"), ("effetto serra", "gas che trattengono l’infrarosso"), ("cella di Hadley", "circolazione tra equatore e tropici"), ("fronte freddo", "aria fredda che spinge sotto l’aria calda"),
                         ("anticiclone", "alta pressione con tempo stabile"), ("ciclone", "bassa pressione con nubi e precipitazioni"), ("IPCC", "gruppo intergovernativo sul cambiamento climatico"),
                         ("clima", "media del tempo per almeno 30 anni")],
            "Che cos’è: {k}?", D),
           ("Gas serra", [("anidride carbonica", "combustibili fossili e deforestazione"), ("metano", "allevamenti e risaie"), ("protossido di azoto", "fertilizzanti azotati"), ("gas fluorurati", "impianti di refrigerazione"),
                          ("vapore acqueo", "evaporazione naturale"), ("ozono troposferico", "reazioni dello smog")],
            "Qual è una fonte principale di: {k}?", "Quale gas serra viene da {v}?"),
           ("Effetti e risposte", {"gli effetti del riscaldamento globale": ["innalzamento del livello del mare", "ritiro dei ghiacciai", "ondate di calore", "acidificazione degli oceani", "eventi estremi più frequenti"],
                                   "le azioni di mitigazione": ["energie rinnovabili", "efficienza energetica", "trasporto pubblico", "riforestazione", "cattura della CO₂"],
                                   "le azioni di adattamento": ["difese contro le alluvioni", "colture resistenti alla siccità", "verde urbano contro il caldo", "sistemi di allerta", "risparmio idrico"]})],
          ["La CO₂ atmosferica è aumentata dal 1750.", "Il clima è una media di almeno 30 anni.", "Il ghiaccio ha albedo alta.", "Il metano è un gas serra.", "Le rinnovabili sono una forma di mitigazione.",
           "L’IPCC valuta il cambiamento climatico.", "Il vento va dalle alte alle basse pressioni."],
          [("Tempo e clima sono la stessa cosa.", "Il clima è una media di lungo periodo."), ("Il buco dell’ozono causa il riscaldamento globale.", "Sono fenomeni diversi."), ("Il ghiaccio ha albedo bassa.", "Ha albedo alta."),
           ("La CO₂ è diminuita dal 1750.", "È aumentata."), ("La riforestazione è adattamento.", "È mitigazione.")],
          "il clima", "earths-systems", calc=f_clima),
    ]
