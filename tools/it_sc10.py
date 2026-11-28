# -*- coding: utf-8 -*-
"""Italia / Liceo scientifico: seconda liceo（Fisica e Scienze naturali, primo biennio）"""
import math
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"
G = 9.8


def f_cin(R):
    k = R.choice(["caduta_v", "caduta_t", "frenata", "mua", "incontro", "vmed", "kmh"])
    if k == "caduta_v":
        t = R.choice([1, 2, 3, 1.5, 2.5, 4])
        return nq("Lasci cadere un sasso da fermo. Che velocità ha dopo %s s? (g = 9,8 m/s², senza attrito dell’aria)" % num(t), G * t, [G * t * t, G / t, 0.5 * G * t * t, G], "m/s",
                  "v = g t = 9,8 × %s = %s m/s." % (num(t), num(G * t)))
    if k == "caduta_t":
        t = R.choice([1, 2, 3, 1.5, 2.5])
        h = 0.5 * G * t * t
        return nq("Un oggetto cade da fermo da %s m. Quanto tempo impiega ad arrivare a terra? (g = 9,8 m/s²)" % num(h), t, [h / G, 2 * h / G, math.sqrt(h / G), t * 2], "s",
                  "h = ½ g t² → t = √(2h : g) = √(2 × %s : 9,8) = %s s." % (num(h), num(t)))
    if k == "frenata":
        v0, a = R.choice([(20, 5), (30, 6), (15, 3), (25, 5), (10, 2), (40, 8)])
        return nq("Un’auto a %d m/s frena con decelerazione di %d m/s². Quanto spazio percorre prima di fermarsi?" % (v0, a), v0 * v0 / (2 * a), [v0 * v0 / a, v0 / a, v0 * a, v0 * v0], "m",
                  "v² = v₀² − 2 a s → s = v₀² : (2a) = %d : %d = %s m." % (v0 * v0, 2 * a, num(v0 * v0 / (2 * a))))
    if k == "mua":
        v0, a, t = R.choice([(0, 2, 10), (5, 2, 4), (10, 3, 6), (0, 4, 5), (2, 1, 8), (0, 3, 4)])
        s = v0 * t + 0.5 * a * t * t
        return nq("Un corpo parte a %d m/s con accelerazione %d m/s². Quanto spazio percorre in %d s?" % (v0, a, t), s, [v0 * t + a * t * t, v0 * t, a * t, a * t * t], "m",
                  "s = v₀ t + ½ a t² = %d × %d + 0,5 × %d × %d² = %s m." % (v0, t, a, t, num(s)))
    if k == "incontro":
        d, v1, v2 = R.choice([(300, 20, 10), (1000, 30, 20), (600, 15, 15), (900, 25, 20), (120, 4, 2)])
        return nq("Due ciclisti distanti %d m si vengono incontro a %d m/s e %d m/s. Dopo quanto si incontrano?" % (d, v1, v2), d / (v1 + v2),
                  [d / abs(v1 - v2) if v1 != v2 else d / v1, d / v1, d * (v1 + v2), d / v2], "s", "Le velocità si sommano: t = %d : (%d + %d) = %s s." % (d, v1, v2, num(d / (v1 + v2))))
    if k == "vmed":
        s1, v1, s2, v2 = R.choice([(60, 30, 60, 60), (120, 60, 120, 40), (100, 50, 100, 100), (90, 45, 90, 90)])
        t = s1 / v1 + s2 / v2
        return nq("Un’auto fa %d km a %d km/h e poi %d km a %d km/h. Qual è la velocità media sull’intero percorso?" % (s1, v1, s2, v2), (s1 + s2) / t, [(v1 + v2) / 2, v1 + v2, v2, v1], "km/h",
                  "v = spazio totale : tempo totale = %d : %s = %s km/h (non la media delle velocità)." % (s1 + s2, num(t), num((s1 + s2) / t)))
    v = R.choice([54, 90, 126, 36, 144, 108])
    return nq("Un treno viaggia a %d km/h. Quanti metri percorre in un minuto?" % v, v / 3.6 * 60, [v * 60, v / 60, v / 3.6, v * 1000], "m",
              "%d km/h = %s m/s; × 60 s = %s m." % (v, num(v / 3.6), num(v / 3.6 * 60)))


def f_din(R):
    k = R.choice(["fma", "a", "m", "piano", "attr", "circ", "pend"])
    if k == "fma":
        m, a = R.choice([(1200, 2), (5, 3), (70, 1.5), (0.4, 15), (800, 2.5), (60, 4)])
        return nq("Quale forza risultante serve per dare a %s kg un’accelerazione di %s m/s²?" % (num(m), num(a)), m * a, [m / a, a / m, m + a, m * a * G], "N",
                  "F = m a = %s × %s = %s N." % (num(m), num(a), num(m * a)))
    if k == "a":
        f, m = R.choice([(600, 1200), (50, 10), (24, 8), (300, 60), (90, 45), (7, 2)])
        return nq("Una forza risultante di %d N agisce su una massa di %d kg. Quanto vale l’accelerazione?" % (f, m), f / m, [f * m, m / f, f - m if f > m else f + m, f / m * G], "m/s²",
                  "a = F : m = %d : %d = %s m/s²." % (f, m, num(f / m)))
    if k == "m":
        f, a = R.choice([(200, 4), (30, 6), (1500, 3), (12, 0.5), (84, 7), (450, 9)])
        return nq("Una forza di %d N produce un’accelerazione di %s m/s². Qual è la massa?" % (f, num(a)), f / a, [f * a, a / f, f / G, f - a], "kg", "m = F : a = %s kg." % num(f / a))
    if k == "piano":
        a = R.choice([30, 30, 30])
        th = R.choice([("30°", 0.5), ("90°", 1)])
        return nq("Un corpo scivola senza attrito su un piano inclinato di 30°. Quanto vale la sua accelerazione? (g = 9,8 m/s²)", G * 0.5, [G, G * math.sqrt(3) / 2, G * 2, G / 3], "m/s²",
                  "a = g sen 30° = 9,8 × 0,5 = 4,9 m/s².")
    if k == "attr":
        m, f, mu = R.choice([(10, 50, 0.2), (20, 100, 0.3), (5, 30, 0.4), (40, 200, 0.25), (8, 40, 0.1)])
        a = (f - mu * m * G) / m
        return nq("Tiri orizzontalmente una cassa di %d kg con %d N. Il coefficiente d’attrito dinamico è %s. Quanto vale l’accelerazione? (g = 9,8 m/s²)" % (m, f, num(mu)), a,
                  [f / m, (f + mu * m * G) / m, mu * G, f / m - mu], "m/s²", "a = (F − μ m g) : m = (%d − %s) : %d = %s m/s²." % (f, num(mu * m * G), m, num(a)))
    if k == "circ":
        v, r = R.choice([(10, 50), (20, 100), (5, 10), (15, 45), (30, 300), (8, 16)])
        return nq("Un’auto percorre una curva di raggio %d m a %d m/s. Quanto vale l’accelerazione centripeta?" % (r, v), v * v / r, [v / r, v * r, v * v * r, r / v], "m/s²",
                  "a = v² : r = %d : %d = %s m/s²." % (v * v, r, num(v * v / r)))
    l = R.choice([1, 0.25, 2, 0.5, 4, 9.8])
    return nq("Qual è il periodo di un pendolo semplice lungo %s m? (g = 9,8 m/s²)" % num(l), 2 * math.pi * math.sqrt(l / G), [math.sqrt(l / G), 2 * math.pi * l / G, math.pi * math.sqrt(l / G), 2 * math.pi * math.sqrt(G / l)], "s",
              "T = 2π √(l : g) = 2π √(%s : 9,8) = %s s." % (num(l), num(2 * math.pi * math.sqrt(l / G))))


def f_ott(R):
    k = R.choice(["lente", "ingr", "snell", "spec", "diottrie", "n"])
    if k == "lente":
        f, p = R.choice([(10, 30), (20, 60), (15, 45), (10, 20), (5, 15), (12, 36), (20, 30)])
        q = 1 / (1 / f - 1 / p)
        return nq("Un oggetto è a %d cm da una lente convergente con distanza focale %d cm. A che distanza si forma l’immagine?" % (p, f), q, [p - f, 1 / (1 / f + 1 / p), p + f, f * p], "cm",
                  "1/p + 1/q = 1/f → 1/q = 1/%d − 1/%d → q = %s cm." % (f, p, num(q)))
    if k == "ingr":
        p, q = R.choice([(30, 15), (20, 60), (40, 40), (15, 30), (60, 20), (45, 90)])
        return nq("Un oggetto è a %d cm dalla lente e l’immagine a %d cm. Quanto vale l’ingrandimento?" % (p, q), q / p, [p / q, p * q, q - p if q != p else 2, q / p * 2], "",
                  "G = q : p = %d : %d = %s." % (q, p, num(q / p)))
    if k == "snell":
        n1, n2, i = R.choice([(1, 1.5, 30), (1, 1.33, 30), (1, 1.5, 45), (1.33, 1, 30), (1, 2, 30), (1.5, 1, 20)])
        r = math.degrees(math.asin(n1 * math.sin(math.radians(i)) / n2))
        return nq("Un raggio passa da un mezzo con n = %s a uno con n = %s con angolo di incidenza %d°. Quanto vale l’angolo di rifrazione?" % (num(n1), num(n2), i), r,
                  [i, i * n2 / n1, i * n1 / n2, 90 - r], "°", "n₁ sen i = n₂ sen r → sen r = %s × sen %d° : %s → r = %s°." % (num(n1), i, num(n2), num(r)))
    if k == "spec":
        d = R.choice([1, 2.5, 3, 0.8, 1.5, 4])
        return nq("Sei a %s m da uno specchio piano. A che distanza da te vedi la tua immagine?" % num(d), 2 * d, [d, d / 2, d * 4, d + 1], "m",
                  "L’immagine è dietro lo specchio alla stessa distanza: %s + %s = %s m." % (num(d), num(d), num(2 * d)))
    if k == "diottrie":
        f = R.choice([0.5, 0.25, 0.2, 1, 2, 0.4, -0.5, -0.25])
        return nq("Una lente ha distanza focale %s m. Quanto vale il suo potere diottrico?" % (num(f) if f > 0 else "−" + num(-f)), 1 / f, [f, 1 / f * 10, -1 / f, 1 / f / 2], "diottrie",
                  "Potere diottrico = 1 : f = %s diottrie%s." % (num(1 / f) if f > 0 else "−" + num(-1 / f), " (lente divergente)" if f < 0 else ""), neg=True)
    n = R.choice([(1.33, "acqua"), (1.5, "vetro"), (2.42, "diamante"), (1.31, "ghiaccio")])
    return nq("Quanto vale la velocità della luce nel %s (n = %s)? (c = 3 × 10⁸ m/s)" % (n[1], num(n[0])), 3e8 / n[0], [3e8 * n[0], 3e8, 3e8 / n[0] / 10, 3e5 / n[0]], "m/s",
              "v = c : n = 3 × 10⁸ : %s = %s m/s." % (num(n[0]), num(3e8 / n[0])))


def f_term(R):
    k = R.choice(["q", "c", "mix", "lin", "gas", "lat"])
    if k == "q":
        m, c, dt, n = R.choice([(2, 4186, 20, "acqua"), (0.5, 900, 40, "alluminio"), (3, 450, 30, "ferro"), (1, 385, 50, "rame"), (0.2, 4186, 75, "acqua"), (5, 4186, 10, "acqua")])
        return nq("Quanto calore serve per scaldare %s kg di %s (c = %d J/(kg·K)) di %d K?" % (num(m), n, c, dt), m * c * dt, [m * c, c * dt, m * dt, m * c * dt / 1000], "J",
                  "Q = m c ΔT = %s × %d × %d = %s J." % (num(m), c, dt, num(m * c * dt)))
    if k == "c":
        q, m, dt = R.choice([(9000, 0.5, 20), (13500, 1, 30), (77000, 2, 100), (41860, 1, 10), (3850, 0.1, 100), (18000, 2, 10)])
        return nq("Servono %s J per scaldare %s kg di una sostanza di %d K. Qual è il calore specifico?" % (num(q), num(m), dt), q / (m * dt), [q * m * dt, q / m, q / dt, m * dt / q], "J/(kg·K)",
                  "c = Q : (m ΔT) = %s : (%s × %d) = %s J/(kg·K)." % (num(q), num(m), dt, num(q / (m * dt))))
    if k == "mix":
        m1, t1, m2, t2 = R.choice([(1, 80, 1, 20), (2, 60, 1, 30), (0.5, 90, 1.5, 10), (3, 40, 1, 80), (1, 100, 4, 25)])
        t = (m1 * t1 + m2 * t2) / (m1 + m2)
        return nq("Mescoli %s kg d’acqua a %d °C con %s kg d’acqua a %d °C. Quale temperatura di equilibrio si raggiunge?" % (num(m1), t1, num(m2), t2), t, [(t1 + t2) / 2, t1 + t2, abs(t1 - t2), t1],
                  "°C", "Te = (m₁ t₁ + m₂ t₂) : (m₁ + m₂) = %s °C." % num(t))
    if k == "lin":
        l, a, dt = R.choice([(100, 1.2e-5, 40), (20, 2.4e-5, 50), (1000, 1.2e-5, 30), (50, 1.7e-5, 100), (12, 1.2e-5, 25)])
        return nq("Una sbarra di %d m (λ = %s K⁻¹) si scalda di %d K. Di quanti millimetri si allunga?" % (l, num(a), dt), l * a * dt * 1000, [l * a * dt, l * a * 1000, a * dt * 1000, l * a * dt * 100], "mm",
                  "Δl = λ l ΔT = %s × %d × %d = %s m = %s mm." % (num(a), l, dt, num(l * a * dt), num(l * a * dt * 1000)))
    if k == "gas":
        p, v1, v2 = R.choice([(100000, 2, 1), (200000, 3, 6), (150000, 4, 2), (100000, 5, 10), (300000, 1, 3)])
        return nq("Un gas a temperatura costante ha pressione %s Pa e volume %d l. Se il volume diventa %d l, quanto vale la pressione?" % (num(p), v1, v2), p * v1 / v2, [p * v2 / v1, p, p * v1 * v2, p / v1], "Pa",
                  "Legge di Boyle: p₁V₁ = p₂V₂ → p₂ = %s × %d : %d = %s Pa." % (num(p), v1, v2, num(p * v1 / v2)))
    m = R.choice([0.5, 1, 2, 0.2, 1.5, 3])
    return nq("Quanto calore serve per fondere %s kg di ghiaccio a 0 °C? (calore latente di fusione 334 000 J/kg)" % num(m), m * 334000, [334000 / m, m * 4186, 334000, m * 334000 / 1000], "J",
              "Q = m L = %s × 334 000 = %s J." % (num(m), num(m * 334000)))


def f_mole(R):
    k = R.choice(["mm", "n", "m", "N", "gas", "perc"])
    sub = [("H₂O", 18), ("CO₂", 44), ("NaCl", 58.5), ("CH₄", 16), ("O₂", 32), ("NH₃", 17), ("C₆H₁₂O₆", 180), ("CaCO₃", 100), ("H₂SO₄", 98)]
    f, mm = R.choice(sub)
    if k == "mm":
        return nq("Qual è la massa molare di %s? (H = 1, C = 12, N = 14, O = 16, Na = 23, S = 32, Cl = 35,5, Ca = 40)" % f, mm, [mm / 2, mm + 16, mm - 1, mm * 2], "g/mol",
                  "Si sommano le masse atomiche degli atomi: M(%s) = %s g/mol." % (f, num(mm)))
    if k == "n":
        m = R.choice([2, 3, 5, 0.5, 4, 10]) * mm
        return nq("Quante moli ci sono in %s g di %s (M = %s g/mol)?" % (num(m), f, num(mm)), m / mm, [m * mm, mm / m, m / mm * 2, m - mm], "mol", "n = m : M = %s : %s = %s mol." % (num(m), num(mm), num(m / mm)))
    if k == "m":
        n = R.choice([0.5, 2, 3, 0.25, 1.5, 4])
        return nq("Quanti grammi pesano %s mol di %s (M = %s g/mol)?" % (num(n), f, num(mm)), n * mm, [mm / n, n / mm, n + mm, n * mm * 2], "g", "m = n × M = %s × %s = %s g." % (num(n), num(mm), num(n * mm)))
    if k == "N":
        n = R.choice([2, 0.5, 3, 0.1, 1.5, 10])
        return nq("Quante molecole ci sono in %s mol di %s? (NA = 6,02 × 10²³)" % (num(n), f), n * 6.02e23, [6.02e23 / n, 6.02e23, n * 6.02e22, n * 6.02e24], "",
                  "N = n × NA = %s × 6,02 × 10²³ = %s molecole." % (num(n), num(n * 6.02e23)))
    if k == "gas":
        n = R.choice([2, 0.5, 3, 0.25, 1.5, 4])
        return nq("Che volume occupano %s mol di un gas in condizioni normali (0 °C, 1 atm)?" % num(n), n * 22.4, [22.4 / n, n * 24.5, 22.4, n * 2.24], "l",
                  "A 0 °C e 1 atm una mole di gas occupa 22,4 l: %s × 22,4 = %s l." % (num(n), num(n * 22.4)))
    f, mm, el, me = R.choice([("H₂O", 18, "ossigeno", 16), ("CO₂", 44, "carbonio", 12), ("CH₄", 16, "idrogeno", 4), ("NH₃", 17, "azoto", 14), ("CaCO₃", 100, "calcio", 40), ("NaCl", 58.5, "sodio", 23)])
    return nq("Qual è la percentuale in massa di %s in %s (M = %s g/mol)?" % (el, f, num(mm)), me * 100 / mm, [mm * 100 / me, me, 100 - me * 100 / mm, me / mm], "%",
              "%% = %s : %s × 100 = %s %%." % (num(me), num(mm), num(me * 100 / mm)))


def UNITS(grade):
    return [
        H("FI", "cinematica", "Cinematica: moto rettilineo uniforme e accelerato", "Cinematica",
          "Lo studente descrive il moto rettilineo uniforme e uniformemente accelerato con equazioni e grafici, studia la caduta libera e il moto circolare uniforme.",
          "sistema di riferimento, posizione, spostamento, velocità media e istantanea, accelerazione, moto rettilineo uniforme, uniformemente accelerato, caduta libera, grafici s-t e v-t, moto circolare",
          "s = v₀ t + ½ a t²", "In caduta libera tutti i corpi accelerano di 9,8 m/s².",
          ["Nel moto rettilineo uniforme la velocità è costante: s = s₀ + v t; il grafico s-t è una retta.", "Nel moto uniformemente accelerato v = v₀ + a t e s = v₀ t + ½ a t²; vale anche v² = v₀² + 2 a s.",
           "Senza aria tutti i corpi cadono con la stessa accelerazione g = 9,8 m/s². Nel moto circolare uniforme a = v² : r verso il centro."],
          [("Un’auto parte da ferma con a = 2 m/s². Quanto spazio fa in 5 s?", ["s = ½ a t².", "0,5 × 2 × 25 = 25."], "25 m.")],
          [("I corpi pesanti cadono più in fretta.", "Senza aria cadono con la stessa accelerazione."), ("La velocità media è la media delle velocità.", "È lo spazio totale diviso il tempo totale.")],
          [("Che cosa rappresenta l’area sotto il grafico v-t?", "Lo spazio percorso."), ("Che cosa indica la pendenza del grafico s-t?", "La velocità.")],
          [("Grafici", [("retta orizzontale nel grafico s-t", "corpo fermo"), ("retta inclinata nel grafico s-t", "moto uniforme"), ("parabola nel grafico s-t", "moto uniformemente accelerato"),
                        ("retta orizzontale nel grafico v-t", "velocità costante"), ("retta inclinata verso l’alto nel grafico v-t", "accelerazione positiva costante"),
                        ("retta inclinata verso il basso nel grafico v-t", "decelerazione costante"), ("area sotto il grafico v-t", "spazio percorso"), ("pendenza del grafico v-t", "accelerazione")],
            "Che cosa indica: {k}?", D),
           ("Formule", [("velocità media", "Δs : Δt"), ("accelerazione media", "Δv : Δt"), ("legge oraria del moto uniforme", "s = s₀ + v t"), ("velocità nel moto accelerato", "v = v₀ + a t"),
                        ("legge oraria del moto accelerato", "s = s₀ + v₀ t + ½ a t²"), ("accelerazione centripeta", "a = v² : r"), ("periodo del moto circolare", "T = 2π r : v")],
            "Quale formula esprime: {k}?", "Che cosa esprime la formula {v}?"),
           ("Moti", {"gli esempi di moto uniformemente accelerato": ["sasso in caduta libera", "auto che parte al semaforo", "sciatore su una pista liscia", "treno che frena in modo regolare"],
                     "gli esempi di moto rettilineo uniforme": ["auto a velocità costante in autostrada", "nastro trasportatore", "scala mobile", "nave in mare calmo a velocità costante"],
                     "gli esempi di moto circolare uniforme": ["lancetta dei secondi", "giostra a velocità costante", "punto sul bordo di un CD", "satellite in orbita circolare"]})],
          ["In caduta libera a = 9,8 m/s².", "La pendenza del grafico s-t è la velocità.", "L’area sotto il grafico v-t è lo spazio.", "Nel moto uniforme v è costante.", "a = v² : r nel moto circolare.",
           "La velocità media è spazio totale diviso tempo totale.", "Nel vuoto una piuma e un martello cadono insieme."],
          [("I corpi pesanti cadono più veloci nel vuoto.", "Cadono insieme."), ("L’area sotto v-t è l’accelerazione.", "È lo spazio."), ("Nel moto uniforme a è costante e non nulla.", "a = 0."),
           ("La velocità media è la media delle velocità.", "È Δs : Δt."), ("Nel moto circolare uniforme non c’è accelerazione.", "C’è l’accelerazione centripeta.")],
          "la cinematica", "forces-and-motion", calc=f_cin),

        H("FI", "dinamica", "I principi della dinamica", "Dinamica",
          "Lo studente applica i tre principi della dinamica, la relazione F = m a, studia il moto su piano inclinato e con attrito, la forza centripeta e il pendolo.",
          "inerzia, sistemi inerziali, secondo principio, F = m a, terzo principio, azione e reazione, piano inclinato, attrito, forza centripeta, pendolo, moto armonico",
          "F = m a", "A ogni azione corrisponde una reazione uguale e contraria su un altro corpo.",
          ["Primo principio (inerzia): se la risultante è nulla, il corpo resta fermo o in moto rettilineo uniforme.", "Secondo principio: F = m a. Un newton dà a 1 kg un’accelerazione di 1 m/s².",
           "Terzo principio: le forze nascono a coppie, uguali e opposte, applicate a corpi diversi."],
          [("Una forza di 30 N agisce su 6 kg. Quanto vale a?", ["a = F : m.", "30 : 6 = 5."], "5 m/s².")],
          [("Azione e reazione si annullano.", "Agiscono su corpi diversi, quindi non si annullano."), ("Per stare in moto serve una forza.", "Serve per cambiare il moto, non per mantenerlo.")],
          [("Perché in un’auto in curva ci sentiamo spinti verso l’esterno?", "Per inerzia il corpo tende ad andare dritto; l’auto ci spinge verso il centro."), ("Da che cosa dipende il periodo del pendolo?", "Dalla lunghezza e da g, non dalla massa.")],
          [("Principi", [("cintura di sicurezza in frenata", "primo principio"), ("disco da hockey che scivola sul ghiaccio", "primo principio"), ("passeggero che sbanda in curva", "primo principio"),
                         ("calcio più forte, palla più veloce", "secondo principio"), ("camion carico che accelera piano", "secondo principio"), ("rinculo del fucile", "terzo principio"),
                         ("razzo nello spazio", "terzo principio"), ("barca che si allontana quando salti sul molo", "terzo principio")],
            "Quale principio spiega: {k}?", None, ("principio di Archimede", "principio di Pascal")),
           ("Concetti", [("inerzia", "tendenza a mantenere lo stato di moto"), ("massa inerziale", "misura dell’inerzia di un corpo"), ("sistema inerziale", "sistema in cui vale il primo principio"),
                         ("newton", "forza che dà a 1 kg un’accelerazione di 1 m/s²"), ("forza centripeta", "forza diretta verso il centro della curva"), ("moto armonico", "moto del pendolo per piccole oscillazioni"),
                         ("forza d’attrito dinamico", "si oppone al moto di un corpo che scivola"), ("peso apparente", "peso misurato in un ascensore che accelera")],
            "Che cos’è: {k}?", D),
           ("Forze", {"le coppie azione-reazione": ["piede che spinge il suolo e suolo che spinge il piede", "Terra che attira la Luna e Luna che attira la Terra", "remo che spinge l’acqua e acqua che spinge il remo", "razzo che spinge i gas e gas che spingono il razzo", "mano che spinge il muro e muro che spinge la mano"],
                      "le forze centripete in natura": ["gravità per la Luna", "tensione della fune per la fionda", "attrito delle gomme in curva", "forza elettrica per l’elettrone", "reazione del binario sulla ruota del treno in curva"],
                      "le grandezze da cui dipende il periodo del pendolo": ["lunghezza del filo", "accelerazione di gravità", "valore di g nel luogo"]})],
          ["F = m a.", "Azione e reazione agiscono su corpi diversi.", "Il periodo del pendolo non dipende dalla massa.", "Un newton è 1 kg × 1 m/s².", "Senza forze un corpo mantiene il suo moto.",
           "La forza centripeta è diretta verso il centro.", "Su un piano inclinato liscio a = g sen α."],
          [("Azione e reazione si annullano.", "Sono su corpi diversi."), ("Il periodo del pendolo dipende dalla massa.", "Non dipende dalla massa."), ("F = m : a.", "F = m a."),
           ("Per muoversi a velocità costante serve una forza risultante.", "La risultante è nulla."), ("La forza centripeta è verso l’esterno.", "È verso il centro.")],
          "la dinamica", "forces-and-motion", calc=f_din),

        H("FI", "ottica-geometrica", "L’ottica geometrica", "Ottica geometrica",
          "Lo studente studia la propagazione rettilinea della luce, le leggi della riflessione e della rifrazione, la riflessione totale, gli specchi e le lenti con l’equazione dei punti coniugati.",
          "raggio luminoso, riflessione, specchi piani e curvi, rifrazione, indice di rifrazione, legge di Snell, riflessione totale, lenti convergenti e divergenti, fuoco, ingrandimento, diottrie",
          "1/p + 1/q = 1/f", "Legge di Snell: n₁ sen i = n₂ sen r.",
          ["La luce si propaga in linea retta. Nella riflessione l’angolo di incidenza è uguale a quello di riflessione.", "Nella rifrazione vale n₁ sen i = n₂ sen r; n = c : v.",
           "Per le lenti sottili vale 1/p + 1/q = 1/f; l’ingrandimento è G = q : p. Il potere diottrico è 1 : f (in diottrie)."],
          [("Un oggetto è a 30 cm da una lente con f = 10 cm. Dove si forma l’immagine?", ["1/q = 1/10 − 1/30 = 2/30.", "q = 15 cm."], "A 15 cm, dall’altra parte.")],
          [("Lo specchio piano ingrandisce.", "L’immagine è uguale e simmetrica."), ("Passando nell’acqua la luce accelera.", "Rallenta: v = c : n.")],
          [("Come funziona la fibra ottica?", "La luce resta dentro la fibra per riflessione totale."), ("Che lenti usa un miope?", "Lenti divergenti, con diottrie negative.")],
          [("Strumenti", [("lente d’ingrandimento", "lente convergente con oggetto dentro il fuoco"), ("macchina fotografica", "lente convergente che forma un’immagine reale"), ("fibra ottica", "riflessione totale"),
                          ("periscopio", "due specchi piani"), ("occhiali per miopi", "lenti divergenti"), ("occhiali per ipermetropi", "lenti convergenti"), ("specchietto retrovisore curvo", "specchio convesso"),
                          ("faro dell’auto", "specchio concavo")],
            "Su che cosa si basa: {k}?", "Quale strumento usa {v}?"),
           ("Concetti", [("indice di rifrazione", "rapporto c : v"), ("angolo limite", "angolo oltre il quale c’è riflessione totale"), ("fuoco", "punto in cui convergono i raggi paralleli"),
                         ("immagine reale", "si può proiettare su uno schermo"), ("immagine virtuale", "si vede ma non si proietta"), ("diottria", "unità del potere diottrico, 1 : m"),
                         ("legge di Snell", "n₁ sen i = n₂ sen r"), ("dispersione", "i colori si separano perché n dipende dal colore")],
            "Che cos’è: {k}?", D),
           ("Mezzi", {"i mezzi con indice di rifrazione maggiore di quello dell’acqua": ["vetro", "diamante", "zaffiro", "quarzo"], "i fenomeni dovuti alla rifrazione": ["matita che sembra spezzata in acqua", "arcobaleno", "miraggio", "piscina che sembra meno profonda"],
                      "i fenomeni dovuti alla riflessione": ["immagine nello specchio", "eco luminosa del lago", "riflesso sulla vetrina", "luce della Luna"]})],
          ["Angolo di incidenza e di riflessione sono uguali.", "n = c : v.", "La fibra ottica usa la riflessione totale.", "La lente d’ingrandimento è convergente.", "Il miope usa lenti divergenti.",
           "L’immagine di uno specchio piano è virtuale.", "1/p + 1/q = 1/f."],
          [("Nell’acqua la luce è più veloce che nell’aria.", "È più lenta."), ("Il miope usa lenti convergenti.", "Usa lenti divergenti."), ("Lo specchio piano dà immagini reali.", "Dà immagini virtuali."),
           ("L’angolo di riflessione è il doppio di quello di incidenza.", "Sono uguali."), ("Il diamante ha n minore dell’acqua.", "Ha n = 2,42, molto maggiore.")],
          "l’ottica", "waves-and-light", calc=f_ott),

        H("FI", "temperatura-e-calore", "Temperatura, calore e gas", "Temperatura e calore",
          "Lo studente distingue temperatura e calore, usa le scale termometriche, la dilatazione, il calore specifico, i cambiamenti di stato con il calore latente e le leggi dei gas.",
          "temperatura, scala Kelvin, dilatazione lineare e volumica, calore, capacità termica, calore specifico, equilibrio termico, calore latente, conduzione, convezione, irraggiamento, legge di Boyle",
          "Q = m c ΔT", "Durante un cambiamento di stato Q = m L, e la temperatura resta costante.",
          ["La temperatura misura l’agitazione delle particelle; T(K) = t(°C) + 273,15.", "Il calore è energia in transito: Q = m c ΔT. In equilibrio termico il calore ceduto è uguale a quello assorbito.",
           "Durante fusione ed ebollizione Q = m L. Per un gas a temperatura costante p V è costante (Boyle)."],
          [("Quanto calore serve per scaldare 2 kg d’acqua di 10 K?", ["Q = m c ΔT.", "2 × 4186 × 10."], "83 720 J.")],
          [("Il ghiaccio a 0 °C e l’acqua a 0 °C hanno la stessa energia.", "L’acqua ha in più il calore latente di fusione."), ("Un corpo caldo contiene calore.", "Ha energia interna; il calore è l’energia che passa.")],
          [("Perché d’estate la sabbia scotta più dell’acqua?", "La sabbia ha un calore specifico molto più piccolo."), ("Che cos’è lo zero assoluto?", "0 K = −273,15 °C, la temperatura più bassa possibile.")],
          [("Calori specifici", [("acqua", "4186 J/(kg·K)"), ("alluminio", "900 J/(kg·K)"), ("ferro", "450 J/(kg·K)"), ("rame", "385 J/(kg·K)"), ("ghiaccio", "2090 J/(kg·K)"), ("piombo", "128 J/(kg·K)")],
            "Qual è più o meno il calore specifico di: {k}?", "Quale sostanza ha calore specifico di circa {v}?"),
           ("Concetti", [("capacità termica", "calore per scaldare un corpo di 1 K"), ("calore specifico", "calore per scaldare 1 kg di 1 K"), ("calore latente", "calore per cambiare stato a temperatura costante"),
                         ("equilibrio termico", "due corpi a contatto arrivano alla stessa temperatura"), ("legge di Boyle", "p V costante a temperatura costante"), ("legge di Gay-Lussac", "V proporzionale a T a pressione costante"),
                         ("zero assoluto", "0 kelvin"), ("dilatazione lineare", "Δl = λ l ΔT")],
            "Che cos’è: {k}?", D),
           ("Propagazione", {"gli esempi di conduzione": ["manico della pentola che si scalda", "cucchiaio nel tè caldo", "piedi sul pavimento freddo", "ferro da stiro sulla stoffa"],
                             "gli esempi di convezione": ["aria calda del termosifone che sale", "brezze marine", "acqua che gira nella pentola", "correnti nel mantello terrestre"],
                             "gli esempi di irraggiamento": ["calore del Sole", "stufa a infrarossi", "brace del camino", "lampada riscaldante"]})],
          ["Q = m c ΔT.", "L’acqua ha un calore specifico alto.", "Durante la fusione la temperatura resta costante.", "Lo zero assoluto è 0 K.", "Per Boyle p V è costante a T costante.",
           "Il Sole scalda la Terra per irraggiamento.", "I metalli si dilatano scaldandosi."],
          [("Il calore specifico dell’acqua è basso.", "È molto alto."), ("Durante la fusione la temperatura sale.", "Resta costante."), ("0 K = 0 °C.", "0 K = −273,15 °C."),
           ("Per Boyle p V aumenta se il volume diminuisce.", "p V resta costante."), ("La convezione avviene nei solidi.", "Avviene nei fluidi.")],
          "temperatura e calore", "energy", calc=f_term),

        H("CH", "la-mole", "La mole e la quantità di sostanza", "La mole",
          "Lo studente usa la massa atomica e molecolare relativa, il concetto di mole e il numero di Avogadro, il volume molare dei gas e la composizione percentuale dei composti.",
          "unità di massa atomica, massa atomica relativa, massa molecolare, mole, numero di Avogadro, massa molare, volume molare, composizione percentuale, formula minima",
          "Una mole contiene 6,02 × 10²³ particelle", "n = m : M; a 0 °C e 1 atm una mole di gas occupa 22,4 l.",
          ["La massa atomica relativa si misura in unità di massa atomica (u). La massa molecolare è la somma delle masse atomiche.", "Una mole contiene il numero di Avogadro di particelle: NA = 6,02 × 10²³.",
           "La massa molare M (g/mol) è uguale alla massa molecolare: n = m : M."],
          [("Quante moli ci sono in 36 g d’acqua?", ["M(H₂O) = 2 × 1 + 16 = 18 g/mol.", "36 : 18 = 2."], "2 mol.")],
          [("Una mole di ogni sostanza pesa uguale.", "Una mole ha lo stesso numero di particelle, non la stessa massa."), ("Il volume molare vale per liquidi e solidi.", "Vale solo per i gas.")],
          [("Perché si usa la mole?", "Per contare gli atomi pesando: il numero di particelle è enorme."), ("Che cos’è la formula minima?", "Il rapporto più semplice tra gli atomi di un composto.")],
          [("Masse molari", [("H₂O", "18 g/mol"), ("CO₂", "44 g/mol"), ("O₂", "32 g/mol"), ("CH₄", "16 g/mol"), ("NaCl", "58,5 g/mol"), ("NH₃", "17 g/mol"), ("CaCO₃", "100 g/mol"), ("C₆H₁₂O₆", "180 g/mol")],
            "Qual è la massa molare di {k}?", "Quale sostanza ha massa molare {v}?"),
           ("Concetti", [("mole", "quantità con 6,02 × 10²³ particelle"), ("numero di Avogadro", "6,02 × 10²³ particelle per mole"), ("massa molare", "massa di una mole in grammi"),
                         ("unità di massa atomica", "un dodicesimo della massa del carbonio-12"), ("volume molare", "22,4 l per una mole di gas a 0 °C e 1 atm"), ("formula minima", "rapporto più semplice tra gli atomi"),
                         ("formula molecolare", "numero reale di atomi nella molecola"), ("composizione percentuale", "percentuale in massa di ogni elemento")],
            "Che cos’è: {k}?", D),
           ("Formule", {"le formule molecolari uguali alla formula minima": ["H₂O", "CO₂", "NH₃", "CH₄", "NaCl"], "le formule molecolari diverse dalla formula minima": ["C₆H₁₂O₆", "H₂O₂", "C₂H₆", "C₂H₄", "N₂O₄"],
                        "le sostanze gassose a temperatura ambiente": ["ossigeno", "azoto", "anidride carbonica", "metano", "ammoniaca"]})],
          ["Una mole contiene 6,02 × 10²³ particelle.", "n = m : M.", "M(H₂O) = 18 g/mol.", "Una mole di gas a 0 °C e 1 atm occupa 22,4 l.", "La massa molare si misura in g/mol.",
           "La formula minima del glucosio è CH₂O.", "36 g d’acqua sono 2 mol."],
          [("Una mole di ogni sostanza ha la stessa massa.", "Ha lo stesso numero di particelle."), ("n = m × M.", "n = m : M."), ("M(CO₂) = 28 g/mol.", "È 44 g/mol."),
           ("Il volume molare vale per i solidi.", "Vale per i gas."), ("NA = 6,02 × 10²⁰.", "NA = 6,02 × 10²³.")],
          "la mole", "matter", calc=f_mole),

        H("BI", "la-cellula-e-le-membrane", "La cellula: struttura e trasporti", "Cellula e membrane",
          "Lo studente descrive la teoria cellulare, cellule procariote ed eucariote, gli organuli, la membrana a mosaico fluido e i trasporti passivi e attivi.",
          "teoria cellulare, procarioti, eucarioti, organuli, nucleo, reticolo endoplasmatico, apparato di Golgi, mitocondri, cloroplasti, membrana, mosaico fluido, diffusione, osmosi, trasporto attivo",
          "La membrana regola tutti gli scambi", "Nell’osmosi l’acqua va verso la soluzione più concentrata.",
          ["Teoria cellulare: ogni vivente è fatto di cellule e ogni cellula nasce da un’altra cellula.", "Le eucariote hanno nucleo e organuli con membrana; le procariote no.",
           "La membrana è un doppio strato di fosfolipidi con proteine (mosaico fluido). Diffusione e osmosi sono passive; il trasporto attivo consuma ATP."],
          [("Un globulo rosso in acqua distillata che cosa fa?", ["Fuori è meno concentrato che dentro.", "L’acqua entra per osmosi."], "Si gonfia e può scoppiare.")],
          [("L’osmosi è il passaggio dei sali.", "È il passaggio dell’acqua attraverso una membrana semipermeabile."), ("Le cellule vegetali non hanno mitocondri.", "Hanno sia mitocondri sia cloroplasti.")],
          [("Che cosa fa l’apparato di Golgi?", "Modifica, impacchetta e smista le proteine."), ("Che cos’è la pompa sodio-potassio?", "Una proteina che con l’ATP porta Na⁺ fuori e K⁺ dentro la cellula.")],
          [("Organuli", [("nucleo", "contiene il DNA"), ("ribosomi", "sintetizzano le proteine"), ("reticolo endoplasmatico ruvido", "produce proteine con i ribosomi"), ("reticolo endoplasmatico liscio", "produce lipidi"),
                         ("apparato di Golgi", "impacchetta e smista le molecole"), ("mitocondri", "respirazione cellulare e ATP"), ("cloroplasti", "fotosintesi"), ("lisosomi", "digeriscono le sostanze"),
                         ("citoscheletro", "dà forma e permette i movimenti")],
            "Che funzione ha: {k}?", D),
           ("Trasporti", [("diffusione semplice", "passaggio di piccole molecole secondo gradiente"), ("diffusione facilitata", "passaggio secondo gradiente con proteine canale"), ("osmosi", "passaggio dell’acqua"),
                          ("trasporto attivo", "passaggio contro gradiente con consumo di ATP"), ("endocitosi", "la cellula ingloba materiale con la membrana"), ("esocitosi", "la cellula espelle materiale con vescicole"),
                          ("soluzione ipertonica", "più concentrata della cellula"), ("soluzione ipotonica", "meno concentrata della cellula")],
            "Che cos’è: {k}?", D),
           ("Tipi di cellule", {"le strutture solo delle cellule vegetali": ["parete di cellulosa", "cloroplasti", "grande vacuolo centrale", "plasmodesmi"],
                                "le strutture comuni a procarioti ed eucarioti": ["membrana plasmatica", "ribosomi", "citoplasma", "DNA"],
                                "le strutture solo delle cellule eucariote": ["nucleo", "mitocondri", "apparato di Golgi", "reticolo endoplasmatico", "lisosomi"]})],
          ["Ogni cellula nasce da un’altra cellula.", "I procarioti non hanno nucleo.", "I mitocondri producono ATP.", "Nell’osmosi passa l’acqua.", "Il trasporto attivo consuma ATP.",
           "La membrana è un doppio strato di fosfolipidi.", "Le cellule vegetali hanno anche mitocondri."],
          [("I batteri hanno il nucleo.", "Sono procarioti."), ("L’osmosi è il passaggio dei sali.", "È il passaggio dell’acqua."), ("La diffusione consuma ATP.", "È passiva."),
           ("Le cellule vegetali non hanno mitocondri.", "Li hanno."), ("I ribosomi producono lipidi.", "Producono proteine.")],
          "la cellula", "living-things-and-ecosystems"),

        H("BI", "mitosi-e-meiosi", "Il ciclo cellulare, la mitosi e la meiosi", "Mitosi e meiosi",
          "Lo studente descrive il ciclo cellulare, le fasi della mitosi e della meiosi, la differenza tra cellule diploidi e aploidi e il significato della variabilità genetica.",
          "ciclo cellulare, interfase, duplicazione del DNA, cromosomi, cromatidi, mitosi, profase, metafase, anafase, telofase, citodieresi, meiosi, diploide, aploide, crossing-over",
          "Mitosi: 2 cellule uguali. Meiosi: 4 gameti", "La meiosi dimezza i cromosomi e crea variabilità con il crossing-over.",
          ["Nel ciclo cellulare l’interfase (G1, S, G2) prepara la divisione: in S il DNA si duplica.", "La mitosi (profase, metafase, anafase, telofase) forma due cellule figlie uguali, diploidi (2n).",
           "La meiosi forma quattro cellule aploidi (n) diverse: il crossing-over e l’assortimento casuale creano variabilità."],
          [("Una cellula con 2n = 46 fa la meiosi. Quanti cromosomi hanno i gameti?", ["La meiosi dimezza il numero.", "46 : 2 = 23."], "23 cromosomi.")],
          [("La mitosi produce i gameti.", "Li produce la meiosi; la mitosi serve per crescere e riparare."), ("Il DNA si duplica durante la mitosi.", "Si duplica prima, nella fase S dell’interfase.")],
          [("Che cos’è il crossing-over?", "Lo scambio di pezzi tra cromosomi omologhi nella profase I."), ("Perché il cancro è legato al ciclo cellulare?", "Le cellule tumorali si dividono senza controllo.")],
          [("Fasi della mitosi", [("profase", "i cromosomi si condensano"), ("metafase", "i cromosomi si allineano all’equatore"), ("anafase", "i cromatidi si separano verso i poli"), ("telofase", "si formano due nuclei"),
                                  ("citodieresi", "il citoplasma si divide"), ("fase S", "il DNA si duplica"), ("fase G1", "la cellula cresce dopo la divisione"), ("fase G2", "la cellula si prepara alla mitosi")],
            "Che cosa succede nella {k}?", "In quale fase {v}?"),
           ("Mitosi o meiosi", [("produce due cellule uguali", "mitosi"), ("serve alla crescita dell’organismo", "mitosi"), ("ripara le ferite", "mitosi"), ("produce cellule 2n", "mitosi"),
                                ("produce quattro cellule", "meiosi"), ("produce cellule aploidi", "meiosi"), ("produce i gameti", "meiosi"), ("ha il crossing-over", "meiosi"), ("ha due divisioni successive", "meiosi")],
            "Quale divisione {k}?", None, ("fissione nucleare", "fecondazione")),
           ("Aploide o diploide", {"le cellule diploidi": ["cellula della pelle", "neurone", "cellula del fegato", "zigote", "globulo bianco"], "le cellule aploidi": ["spermatozoo", "cellula uovo", "spora delle felci", "polline"],
                                   "le strutture del cromosoma": ["centromero", "cromatidi fratelli", "telomeri", "DNA", "istoni"]})],
          ["La mitosi produce due cellule uguali.", "La meiosi produce gameti aploidi.", "Il DNA si duplica nella fase S.", "Il crossing-over aumenta la variabilità.", "In metafase i cromosomi sono all’equatore.",
           "Lo zigote è diploide.", "Nell’uomo i gameti hanno 23 cromosomi."],
          [("La mitosi produce gameti.", "Li produce la meiosi."), ("I gameti sono diploidi.", "Sono aploidi."), ("Il DNA si duplica in anafase.", "Si duplica nella fase S."),
           ("La meiosi ha una sola divisione.", "Ne ha due."), ("Il crossing-over avviene nella mitosi.", "Avviene nella meiosi.")],
          "mitosi e meiosi", "living-things-and-ecosystems"),

        H("BI", "biodiversita-ed-evoluzione", "Biodiversità ed evoluzione", "Biodiversità ed evoluzione",
          "Lo studente descrive la classificazione dei viventi nei domini e nei regni, la teoria di Darwin e la sintesi moderna, le prove dell’evoluzione e la speciazione.",
          "biodiversità, specie, tassonomia, domini Bacteria, Archaea, Eukarya, regni, Lamarck, Darwin, selezione naturale, adattamento, prove dell’evoluzione, speciazione, deriva genetica",
          "Tre domini: Batteri, Archei, Eucarioti", "La selezione naturale agisce sulla variabilità genetica.",
          ["I viventi si classificano in tre domini (Bacteria, Archaea, Eukarya); gli eucarioti comprendono protisti, funghi, piante e animali.",
           "Darwin: c’è variabilità ereditaria, nascono più individui di quanti sopravvivono, i più adatti si riproducono di più.",
           "Le prove dell’evoluzione sono fossili, anatomia comparata, embriologia e DNA. Una nuova specie nasce spesso per isolamento geografico."],
          [("Perché i batteri diventano resistenti agli antibiotici?", ["Alcuni batteri sono già resistenti per caso.", "Sopravvivono e si moltiplicano."], "Per selezione naturale.")],
          [("Gli individui si adattano durante la vita e lo trasmettono.", "È l’idea di Lamarck, smentita."), ("L’evoluzione ha uno scopo.", "Non ha uno scopo: dipende da variabilità e ambiente.")],
          [("Che cos’è la deriva genetica?", "Un cambiamento casuale delle frequenze degli alleli, forte nelle piccole popolazioni."), ("Che cos’è l’isolamento riproduttivo?", "La situazione in cui due popolazioni non possono più incrociarsi.")],
          [("Domini e regni", [("Escherichia coli", "Bacteria"), ("streptococco", "Bacteria"), ("archei delle sorgenti calde", "Archaea"), ("archei metanogeni", "Archaea"), ("ameba", "Eukarya, protisti"),
                               ("lievito", "Eukarya, funghi"), ("felce", "Eukarya, piante"), ("lupo", "Eukarya, animali"), ("alga bruna", "Eukarya, protisti"), ("muffa", "Eukarya, funghi")],
            "Dove si classifica: {k}?", None),
           ("Concetti", [("selezione naturale", "sopravvive e si riproduce di più chi è più adatto"), ("adattamento", "carattere che aumenta la sopravvivenza"), ("speciazione", "nascita di una nuova specie"),
                         ("deriva genetica", "variazione casuale delle frequenze alleliche"), ("isolamento geografico", "barriera che separa due popolazioni"), ("convergenza evolutiva", "specie lontane diventano simili"),
                         ("organi vestigiali", "organi ridotti senza funzione evidente"), ("selezione artificiale", "scelta fatta dall’uomo negli allevamenti")],
            "Che cos’è: {k}?", D),
           ("Prove", {"le prove dell’evoluzione": ["fossili", "organi omologhi", "somiglianza degli embrioni", "confronto del DNA", "organi vestigiali"],
                      "le idee di Darwin": ["variabilità tra individui", "lotta per l’esistenza", "selezione naturale", "discendenza comune", "evoluzione graduale"],
                      "le idee di Lamarck": ["uso e disuso degli organi", "ereditarietà dei caratteri acquisiti", "spinta verso la complessità"]})],
          ["I domini sono tre.", "Darwin propose la selezione naturale.", "I fossili sono prove dell’evoluzione.", "La deriva genetica è casuale.", "Il lievito è un fungo.",
           "La resistenza agli antibiotici è un esempio di selezione.", "L’isolamento geografico può portare a nuove specie."],
          [("I caratteri acquisiti si ereditano.", "Non si ereditano."), ("I domini sono cinque.", "Sono tre."), ("L’evoluzione ha uno scopo.", "Non ha uno scopo."), ("Gli archei sono eucarioti.", "Sono procarioti."),
           ("La deriva genetica dipende dall’adattamento.", "È casuale.")],
          "l’evoluzione", "living-things-and-ecosystems"),
    ]
