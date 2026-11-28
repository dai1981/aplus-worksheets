# -*- coding: utf-8 -*-
"""Italia / Scienze: seconda media（scuola secondaria di primo grado）"""
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"
G = 9.8


def f_chim(R):
    k = R.choice(["lav", "lav2", "conc", "perc", "ph"])
    if k == "lav":
        a, b = R.choice([(12, 32), (24, 64), (4, 32), (2, 16), (56, 32), (40, 16), (6, 48), (27, 24)])
        return nq("In una reazione %d g di un reagente si combinano con %d g di un altro. Quanto pesano i prodotti (legge di Lavoisier)?" % (a, b), a + b,
                  [abs(a - b) if a != b else a * 3, a * b, max(a, b), (a + b) / 2], "g", "Nulla si crea e nulla si distrugge: %d + %d = %d g." % (a, b, a + b))
    if k == "lav2":
        t, a = R.choice([(100, 56), (44, 12), (18, 2), (80, 32), (64, 32), (36, 4), (58, 23)])
        return nq("Da una reazione si ottengono %d g di prodotti. Uno dei due reagenti pesava %d g. Quanto pesava l’altro?" % (t, a), t - a, [t + a, a, t, (t - a) / 2], "g",
                  "%d − %d = %d g." % (t, a, t - a))
    if k == "conc":
        s, v = R.choice([(20, 500), (10, 250), (36, 1000), (5, 100), (50, 2000), (15, 300), (8, 200)])
        return nq("Sciogli %d g di sale in %d ml di soluzione. Qual è la concentrazione in g/l?" % (s, v), s * 1000 / v, [s / v, s * v, v / s, s], "g/l",
                  "%d ml = %s l; %d : %s = %s g/l." % (v, num(v / 1000), s, num(v / 1000), num(s * 1000 / v)))
    if k == "perc":
        s, m = R.choice([(10, 200), (5, 100), (30, 300), (15, 250), (20, 400), (8, 160)])
        return nq("In %d g di soluzione ci sono %d g di zucchero. Qual è la percentuale in massa?" % (m, s), s * 100 / m, [s * 100 / (m + s), m / s, s, s * 10 / m], "%",
                  "%d : %d × 100 = %s %%." % (s, m, num(s * 100 / m)))
    a = R.choice([(2, "acida"), (3, "acida"), (5, "acida"), (7, "neutra"), (9, "basica"), (11, "basica"), (13, "basica"), (4, "acida"), (12, "basica")])
    w = [x for x in ["acida", "neutra", "basica"] if x != a[1]] + ["salata"]
    return it("Una soluzione ha pH %d. Com’è?" % a[0], a[1], w, "pH minore di 7: acida; 7: neutra; maggiore di 7: basica. Con pH %d è %s." % (a[0], a[1]))


def f_moto(R):
    k = R.choice(["v", "s", "t", "kmh", "a", "ms"])
    if k == "v":
        s, t = R.choice([(100, 20), (400, 50), (1500, 300), (60, 12), (200, 25), (3000, 600), (90, 15)])
        return nq("Un atleta percorre %d m in %d s. Qual è la sua velocità media?" % (s, t), s / t, [s * t, t / s, s - t, s / t * 3.6], "m/s", "v = s : t = %d : %d = %s m/s." % (s, t, num(s / t)))
    if k == "s":
        v, t = R.choice([(80, 3), (60, 2), (90, 4), (120, 2), (50, 5), (70, 3)])
        return nq("Un’auto viaggia a %d km/h per %d ore. Quanti km percorre?" % (v, t), v * t, [v + t, v / t, v * t / 60, v * (t + 1)], "km", "s = v × t = %d × %d = %d km." % (v, t, v * t))
    if k == "t":
        s, v = R.choice([(240, 80), (150, 50), (360, 90), (100, 25), (420, 70), (300, 60)])
        return nq("Un treno deve percorrere %d km a %d km/h. Quante ore impiega?" % (s, v), s / v, [s * v, v / s, s - v, s / v * 60], "h", "t = s : v = %d : %d = %s h." % (s, v, num(s / v)))
    if k == "kmh":
        v = R.choice([36, 72, 54, 90, 108, 18, 126])
        return nq("Quanti m/s sono %d km/h?" % v, v / 3.6, [v * 3.6, v / 60, v * 1000, v / 36], "m/s", "Si divide per 3,6: %d : 3,6 = %s m/s." % (v, num(v / 3.6)))
    if k == "ms":
        v = R.choice([5, 10, 15, 20, 25, 30, 12])
        return nq("Quanti km/h sono %d m/s?" % v, v * 3.6, [v / 3.6, v * 60, v * 36, v * 1000], "km/h", "Si moltiplica per 3,6: %d × 3,6 = %s km/h." % (v, num(v * 3.6)))
    v0, v1, t = R.choice([(0, 20, 5), (10, 30, 4), (0, 12, 6), (5, 25, 10), (0, 27, 9), (20, 0, 4)])
    a = (v1 - v0) / t
    return nq("Una bici passa da %d m/s a %d m/s in %d s. Qual è l’accelerazione?" % (v0, v1, t), a, [(v1 + v0) / t, (v1 - v0) * t, v1 / t + 1, a * 2], "m/s²",
              "a = (v₂ − v₁) : t = (%d − %d) : %d = %s m/s²." % (v1, v0, t, num(a)), neg=True)


def f_forze(R):
    k = R.choice(["peso", "massa", "ris", "ris2", "leva", "leva2", "molla"])
    if k == "peso":
        m = R.choice([2, 5, 10, 0.5, 30, 45, 70, 1.5])
        return nq("Quanto pesa sulla Terra un corpo di massa %s kg? (g = 9,8 N/kg)" % num(m), m * G, [m, m / G, m * 10 * 10, m + G], "N", "P = m × g = %s × 9,8 = %s N." % (num(m), num(m * G)))
    if k == "massa":
        p = R.choice([98, 49, 196, 392, 588, 19.6, 686])
        return nq("Un oggetto pesa %s N sulla Terra. Qual è la sua massa? (g = 9,8 N/kg)" % num(p), p / G, [p * G, p, p / 10 * 2, p - G], "kg", "m = P : g = %s : 9,8 = %s kg." % (num(p), num(p / G)))
    if k == "ris":
        a, b = R.choice([(30, 20), (50, 15), (12, 8), (100, 40), (25, 25), (60, 35)])
        return nq("Due persone tirano una cassa nello stesso verso con %d N e %d N. Quanto vale la forza risultante?" % (a, b), a + b, [abs(a - b) if a != b else a * 3, a * b, max(a, b), (a + b) / 2], "N",
                  "Stesso verso: si sommano, %d + %d = %d N." % (a, b, a + b))
    if k == "ris2":
        a, b = R.choice([(30, 20), (50, 15), (120, 80), (100, 40), (75, 60), (45, 30)])
        return nq("Nel tiro alla fune una squadra tira con %d N e l’altra con %d N in verso opposto. Quanto vale la risultante?" % (a, b), a - b, [a + b, a, b, (a + b) / 2], "N",
                  "Versi opposti: si sottrae, %d − %d = %d N." % (a, b, a - b))
    if k == "leva":
        r, br, bp = R.choice([(200, 1, 2), (300, 2, 3), (600, 1, 4), (120, 3, 2), (400, 0.5, 2), (90, 2, 1), (150, 1, 3)])
        p = r * br / bp
        return nq("Una leva solleva una resistenza di %d N con braccio di %s m. Il braccio della potenza è %s m. Quale forza serve?" % (r, num(br), num(bp)), p,
                  [r * bp / br, r * br * bp, r, r / br], "N", "P × bp = R × br → P = %d × %s : %s = %s N." % (r, num(br), num(bp), num(p)))
    if k == "leva2":
        a, b, w = R.choice([(30, 2, 3), (40, 1.5, 2), (25, 2, 2.5), (60, 1, 3), (35, 2, 1.4)])
        return nq("Sull’altalena a bilico Luca (%d kg) è a %s m dal fulcro. A quale distanza deve sedersi Anna (%s kg) per l’equilibrio?" % (a, num(b), num(a * b / w)), w,
                  [b, a * b, b * 2, a / b], "m", "%d × %s = %s × d → d = %s m." % (a, num(b), num(a * b / w), num(w)))
    k_, x = R.choice([(50, 0.1), (200, 0.05), (100, 0.2), (20, 0.5), (400, 0.02), (80, 0.25)])
    return nq("Una molla ha costante elastica %d N/m e si allunga di %s m. Quale forza la tira?" % (k_, num(x)), k_ * x, [k_ / x, k_ + x, k_ * x * 10, x / k_], "N",
              "F = k × x = %d × %s = %s N." % (k_, num(x), num(k_ * x)))


def f_press(R):
    k = R.choice(["p", "p2", "idro", "arch", "dens"])
    if k == "p":
        f, a = R.choice([(600, 0.03), (500, 0.02), (800, 0.04), (1200, 0.1), (300, 0.01), (700, 0.05)])
        return nq("Una persona di %d N appoggia i piedi su %s m². Che pressione esercita?" % (f, num(a)), f / a, [f * a, a / f, f, f / a / 100], "Pa", "p = F : S = %d : %s = %s Pa." % (f, num(a), num(f / a)))
    if k == "p2":
        f, a = R.choice([(100, 2), (60, 3), (240, 4), (50, 0.5), (900, 3), (150, 0.5)])
        return nq("Una forza di %d N agisce su %s m². Quanto vale la pressione?" % (f, num(a)), f / a, [f * a, a / f, f + a, f], "Pa", "p = F : S = %s Pa." % num(f / a))
    if k == "idro":
        h = R.choice([2, 5, 10, 20, 3, 15])
        return nq("Che pressione esercita l’acqua a %d m di profondità (senza l’atmosfera)? (d = 1000 kg/m³, g = 9,8 N/kg)" % h, 1000 * G * h, [1000 * h, G * h, 1000 * G / h, 100 * G * h], "Pa",
                  "p = d × g × h = 1000 × 9,8 × %d = %s Pa." % (h, num(1000 * G * h)))
    if k == "arch":
        v = R.choice([0.001, 0.002, 0.005, 0.01, 0.003, 0.02])
        return nq("Un corpo di volume %s m³ è tutto immerso in acqua. Quanto vale la spinta di Archimede? (d = 1000 kg/m³, g = 9,8 N/kg)" % num(v), 1000 * v * G, [1000 * v, v * G, 1000 * G / v if v else 1, 100 * v * G], "N",
                  "S = d × V × g = 1000 × %s × 9,8 = %s N." % (num(v), num(1000 * v * G)))
    d, n, a = R.choice([(0.92, "ghiaccio", "galleggia"), (7.9, "ferro", "affonda"), (0.6, "legno di abete", "galleggia"), (2.7, "alluminio", "affonda"), (0.24, "sughero", "galleggia"), (11.3, "piombo", "affonda")])
    return it("Un pezzo di %s ha densità %s g/cm³. Che cosa fa nell’acqua (1 g/cm³)?" % (n, num(d)), a, [x for x in ["galleggia", "affonda"] if x != a] + ["si scioglie", "evapora"],
              "Densità %s dell’acqua: %s." % ("minore" if d < 1 else "maggiore", a))


def UNITS(grade):
    return [
        H("FC", "trasformazioni-chimiche", "Le trasformazioni chimiche", "Trasformazioni chimiche",
          "L’alunno distingue trasformazioni fisiche e chimiche, riconosce elementi, composti, atomi e molecole, legge semplici formule e applica la legge di conservazione della massa.",
          "trasformazioni fisiche e chimiche, reagenti, prodotti, atomi, molecole, elementi, composti, formule chimiche, legge di Lavoisier, combustione",
          "Reagenti → prodotti: nasce una sostanza nuova", "Nulla si crea e nulla si distrugge: la massa totale resta uguale.",
          ["In una trasformazione fisica la sostanza resta la stessa (il ghiaccio che fonde); in una chimica nascono sostanze nuove (il ferro che arrugginisce).",
           "La materia è fatta di atomi. Gli elementi hanno un solo tipo di atomo; i composti più tipi legati in molecole (H₂O).",
           "Legge di Lavoisier: la massa dei reagenti è uguale alla massa dei prodotti."],
          [("4 g di idrogeno reagiscono con 32 g di ossigeno. Quanta acqua si forma?", ["La massa si conserva.", "4 + 32 = 36."], "36 g.")],
          [("Sciogliere lo zucchero è una reazione chimica.", "È una trasformazione fisica: lo zucchero resta zucchero."), ("Nella combustione la massa sparisce.", "Va nei gas prodotti (CO₂ e vapore).")],
          [("Come si capisce che è avvenuta una reazione?", "Cambia il colore, si forma un gas o un solido, cambia la temperatura o si sprigiona luce."), ("Che cosa indica H₂O?", "Una molecola con 2 atomi di idrogeno e 1 di ossigeno.")],
          [("Fisica o chimica?", [("il ghiaccio fonde", "trasformazione fisica"), ("lo zucchero si scioglie", "trasformazione fisica"), ("il vetro si rompe", "trasformazione fisica"), ("l’acqua bolle", "trasformazione fisica"),
                                  ("il legno brucia", "trasformazione chimica"), ("il ferro arrugginisce", "trasformazione chimica"), ("la torta cuoce", "trasformazione chimica"), ("il latte inacidisce", "trasformazione chimica"),
                                  ("l’aceto reagisce con il bicarbonato", "trasformazione chimica"), ("la carta si strappa", "trasformazione fisica")],
            "Che trasformazione è: {k}?", None, ("trasformazione nucleare", "nessuna trasformazione")),
           ("Formule", [("H₂O", "acqua"), ("CO₂", "anidride carbonica"), ("O₂", "ossigeno"), ("NaCl", "cloruro di sodio (sale da cucina)"), ("CH₄", "metano"), ("NH₃", "ammoniaca"),
                        ("C₆H₁₂O₆", "glucosio"), ("Fe", "ferro"), ("N₂", "azoto")],
            "Quale sostanza indica la formula {k}?", "Qual è la formula di: {v}?"),
           ("Elementi e composti", {"gli elementi": ["ossigeno", "ferro", "oro", "carbonio", "azoto", "rame"], "i composti": ["acqua", "sale da cucina", "anidride carbonica", "zucchero", "metano", "ammoniaca"],
                                    "i miscugli": ["aria", "acqua di mare", "latte", "granito", "terra"]})],
          ["Nella reazione chimica si formano sostanze nuove.", "La massa si conserva.", "H₂O è la formula dell’acqua.", "Il ferro è un elemento.", "Bruciare il legno è una trasformazione chimica.",
           "L’acqua è un composto.", "Gli atomi si legano in molecole."],
          [("Sciogliere il sale è una reazione chimica.", "È una trasformazione fisica."), ("La massa dei prodotti è minore.", "È uguale a quella dei reagenti."), ("L’acqua è un elemento.", "È un composto."),
           ("CO₂ è l’ossigeno.", "È l’anidride carbonica."), ("Nelle reazioni gli atomi spariscono.", "Gli atomi si riorganizzano.")],
          "le trasformazioni chimiche", "matter", calc=f_chim),

        H("FC", "acidi-e-basi", "Acidi, basi e pH", "Acidi e basi",
          "L’alunno riconosce acidi e basi con gli indicatori, usa la scala del pH, descrive la neutralizzazione e calcola concentrazioni di soluzioni.",
          "acidi, basi, sali, pH, indicatori, cartina al tornasole, neutralizzazione, soluzione, soluto, solvente, concentrazione",
          "pH 7 neutro, sotto acido, sopra basico", "Acido + base → sale + acqua: è la neutralizzazione.",
          ["La scala del pH va da 0 a 14: sotto 7 acido, 7 neutro, sopra 7 basico.", "Gli indicatori cambiano colore: la cartina al tornasole diventa rossa con gli acidi e blu con le basi.",
           "Acido e base si neutralizzano formando sale e acqua. In una soluzione il soluto si scioglie nel solvente."],
          [("Il succo di limone ha pH 2. È acido o basico?", ["2 è minore di 7.", "Più è basso, più è acido."], "Acido.")],
          [("Le basi non sono pericolose.", "La soda caustica corrode come un acido forte."), ("pH 8 è acido.", "Sopra 7 è basico.")],
          [("Perché un antiacido calma il bruciore di stomaco?", "Perché è una base debole che neutralizza l’acido dello stomaco."), ("Che cos’è il soluto?", "La sostanza che si scioglie, come lo zucchero nell’acqua.")],
          [("Acido, neutro o basico?", [("succo di limone", "acido"), ("aceto", "acido"), ("succo gastrico", "acido"), ("coca cola", "acido"), ("acqua distillata", "neutro"), ("acqua pura", "neutro"),
                                        ("bicarbonato in acqua", "basico"), ("sapone", "basico"), ("candeggina", "basico"), ("ammoniaca", "basico"), ("pomodoro", "acido")],
            "Com’è questa sostanza: {k}?", None, ("magnetico", "metallico")),
           ("Concetti", [("acido", "sostanza con pH minore di 7"), ("base", "sostanza con pH maggiore di 7"), ("neutralizzazione", "reazione tra acido e base che dà sale e acqua"),
                         ("indicatore", "sostanza che cambia colore secondo il pH"), ("soluto", "sostanza che si scioglie"), ("solvente", "sostanza in cui si scioglie il soluto"),
                         ("soluzione satura", "soluzione che non scioglie altro soluto"), ("cartina al tornasole", "carta che diventa rossa con gli acidi")],
            "Che cos’è: {k}?", D),
           ("Indicatori e usi", {"gli indicatori": ["cartina al tornasole", "cavolo rosso", "fenolftaleina", "indicatore universale", "succo di mirtillo"],
                                 "gli acidi": ["acido citrico", "acido acetico", "acido cloridrico", "acido solforico", "acido lattico"],
                                 "le basi": ["idrossido di sodio", "ammoniaca", "bicarbonato di sodio", "idrossido di calcio", "calce"]})],
          ["Il limone è acido.", "Il sapone è basico.", "L’acqua pura ha pH 7.", "Acido e base si neutralizzano.", "Il tornasole diventa rosso con gli acidi.", "Il soluto si scioglie nel solvente.",
           "Il pH va da 0 a 14."],
          [("L’aceto è basico.", "È acido."), ("pH 10 è acido.", "È basico."), ("L’acqua pura ha pH 1.", "Ha pH 7."), ("Il tornasole diventa blu con gli acidi.", "Diventa rosso."),
           ("Acido e base non reagiscono.", "Si neutralizzano.")],
          "acidi e basi", "matter", calc=f_chim),

        H("FC", "il-moto", "Il moto: velocità e accelerazione", "Il moto",
          "L’alunno descrive il moto con traiettoria, spazio e tempo, calcola la velocità media, distingue moto uniforme e accelerato e legge grafici spazio-tempo.",
          "sistema di riferimento, traiettoria, spazio, tempo, velocità media, m/s e km/h, moto rettilineo uniforme, accelerazione, grafico spazio-tempo",
          "Velocità = spazio : tempo", "Per passare da km/h a m/s si divide per 3,6.",
          ["Un corpo si muove se cambia posizione rispetto a un sistema di riferimento.", "La velocità media è v = s : t; si misura in m/s o km/h (1 m/s = 3,6 km/h).",
           "Nel moto uniforme la velocità è costante; nel moto accelerato cambia: a = Δv : t."],
          [("Un ciclista percorre 30 km in 2 ore. Qual è la velocità media?", ["v = s : t.", "30 : 2 = 15."], "15 km/h.")],
          [("km/h e m/s sono la stessa cosa.", "1 m/s = 3,6 km/h."), ("Se la velocità diminuisce non c’è accelerazione.", "C’è un’accelerazione negativa (decelerazione).")],
          [("Che cosa mostra un grafico spazio-tempo con una retta?", "Un moto uniforme: lo spazio cresce allo stesso modo ogni secondo."), ("Il passeggero sul treno è fermo?", "Rispetto al treno sì, rispetto ai binari no.")],
          [("Grandezze", [("velocità", "metri al secondo"), ("accelerazione", "metri al secondo quadrato"), ("spazio", "metri"), ("tempo", "secondi"), ("velocità di un’auto", "kilometri orari"),
                          ("frequenza dei giri", "giri al minuto")],
            "In che unità si misura di solito: {k}?", "Quale grandezza si misura in {v}?"),
           ("Tipi di moto", [("auto a velocità costante in autostrada", "moto rettilineo uniforme"), ("sasso che cade", "moto accelerato"), ("auto che frena al semaforo", "moto decelerato"),
                             ("giostra che gira sempre uguale", "moto circolare uniforme"), ("pendolo", "moto oscillatorio"), ("lancetta dei secondi", "moto circolare uniforme"),
                             ("treno che parte dalla stazione", "moto accelerato"), ("altalena", "moto oscillatorio"), ("bici che rallenta in salita", "moto decelerato")],
            "Che tipo di moto è: {k}?", None),
           ("Concetti", {"le grandezze del moto": ["traiettoria", "spazio percorso", "tempo", "velocità", "accelerazione"], "le cose ferme rispetto alla Terra": ["casa", "albero", "semaforo", "montagna", "lampione"],
                         "le cose in moto rispetto alla Terra": ["auto in corsa", "aereo in volo", "nave che salpa", "corridore", "nuvola spinta dal vento"]})],
          ["v = s : t.", "1 m/s corrisponde a 3,6 km/h.", "Nel moto uniforme la velocità è costante.", "Il moto dipende dal sistema di riferimento.", "Un corpo che frena ha accelerazione negativa.",
           "Un sasso che cade accelera.", "Il pendolo ha un moto oscillatorio."],
          [("v = s × t.", "v = s : t."), ("1 m/s = 1 km/h.", "1 m/s = 3,6 km/h."), ("Nel moto uniforme la velocità cambia.", "Resta costante."), ("Un sasso che cade va a velocità costante.", "Accelera."),
           ("Il moto è uguale per ogni osservatore.", "Dipende dal sistema di riferimento.")],
          "il moto", "forces-and-motion", calc=f_moto),

        H("FC", "le-forze", "Le forze e i principi della dinamica", "Le forze",
          "L’alunno rappresenta le forze come vettori, misura con il dinamometro, distingue massa e peso, calcola la risultante e conosce i tre principi della dinamica.",
          "forza, vettore, newton, dinamometro, peso, massa, risultante, attrito, forza elastica, principi della dinamica, inerzia, azione e reazione",
          "La forza si misura in newton", "Peso = massa × g; sulla Terra g = 9,8 N/kg.",
          ["Una forza può deformare un corpo o cambiarne il moto. Si rappresenta con un vettore e si misura in newton (N).",
           "Il peso è la forza con cui la Terra attira un corpo: P = m × g. La massa non cambia, il peso sì (sulla Luna è circa 1/6).",
           "Primo principio: senza forze un corpo resta fermo o in moto uniforme. Secondo: F = m × a. Terzo: a ogni azione corrisponde una reazione uguale e contraria."],
          [("Quanto pesa sulla Terra una massa di 10 kg?", ["P = m × g.", "10 × 9,8 = 98."], "98 N.")],
          [("Massa e peso sono uguali.", "La massa si misura in kg, il peso in N."), ("Serve una forza per mantenere un corpo in moto.", "Senza attrito il corpo continua da solo (inerzia).")],
          [("Perché in auto si mette la cintura?", "Per l’inerzia: se l’auto frena, il corpo continua ad andare avanti."), ("Come fa a salire un razzo?", "Spinge i gas verso il basso e i gas spingono il razzo verso l’alto.")],
          [("Esempi di principi", [("in frenata il corpo va avanti", "primo principio"), ("la tovaglia tirata via di scatto lascia i piatti", "primo principio"),
                                   ("una forza maggiore dà più accelerazione", "secondo principio"), ("un carrello pieno accelera meno di uno vuoto", "secondo principio"),
                                   ("il razzo spinge i gas e sale", "terzo principio"), ("il nuotatore spinge l’acqua indietro e va avanti", "terzo principio"),
                                   ("il fucile rincula quando spara", "terzo principio"), ("un disco sul ghiaccio scivola a lungo", "primo principio")],
            "Quale principio della dinamica spiega questo: {k}?", None, ("legge di Lavoisier", "principio di Archimede")),
           ("Tipi di forze", [("peso", "attrazione della Terra"), ("attrito", "si oppone allo scivolamento"), ("forza elastica", "molla che torna alla sua forma"), ("forza magnetica", "attrazione della calamita sul ferro"),
                              ("spinta di Archimede", "spinta verso l’alto di un fluido"), ("forza elettrica", "attrazione tra cariche opposte"), ("reazione vincolare", "il tavolo che sostiene il libro")],
            "Che cos’è: {k}?", D),
           ("Attrito utile o dannoso?", {"i casi in cui l’attrito è utile": ["freni della bici", "suole delle scarpe", "pneumatici sull’asfalto", "fiammifero che si accende", "matita sulla carta"],
                                         "i casi in cui l’attrito è dannoso": ["usura dei motori", "scarpe consumate", "ingranaggi che si scaldano", "pneumatici che si consumano", "cardini che cigolano"],
                                         "i modi per ridurre l’attrito": ["olio lubrificante", "cuscinetti a sfera", "superfici lisce", "ruote", "forma aerodinamica"]})],
          ["La forza si misura in newton.", "Il peso è P = m × g.", "La massa non cambia sulla Luna.", "L’attrito si oppone al moto.", "A ogni azione corrisponde una reazione.",
           "Il dinamometro misura le forze.", "F = m × a."],
          [("Il peso si misura in kg.", "Si misura in newton."), ("Sulla Luna la massa diminuisce.", "Diminuisce il peso, non la massa."), ("L’attrito aiuta sempre il moto.", "Si oppone al moto."),
           ("Senza forze un corpo si ferma sempre.", "Continua in moto uniforme."), ("La reazione è più debole dell’azione.", "È uguale e contraria.")],
          "le forze", "forces-and-motion", calc=f_forze),

        H("FC", "leve-ed-equilibrio", "Leve, baricentro ed equilibrio", "Leve ed equilibrio",
          "L’alunno riconosce leve di primo, secondo e terzo genere, applica la legge di equilibrio della leva e descrive baricentro e tipi di equilibrio.",
          "leva, fulcro, potenza, resistenza, bracci, leve di primo, secondo e terzo genere, vantaggiose e svantaggiose, baricentro, equilibrio stabile, instabile, indifferente",
          "Potenza × braccio = resistenza × braccio", "Una leva con il braccio della potenza più lungo è vantaggiosa.",
          ["Una leva ha un fulcro, una potenza (la forza che applichi) e una resistenza (il peso da vincere).", "Equilibrio: P × bp = R × br.",
           "Primo genere: fulcro in mezzo (forbici). Secondo genere: resistenza in mezzo (carriola). Terzo genere: potenza in mezzo (pinzette)."],
          [("Con una leva, bp = 2 m e br = 0,5 m. Quale forza serve per 400 N?", ["P × 2 = 400 × 0,5.", "P = 200 : 2."], "100 N.")],
          [("Tutte le leve sono vantaggiose.", "Le leve di terzo genere sono svantaggiose: servono per la precisione."), ("Il baricentro è sempre dentro il corpo.", "In un anello è al centro, nel vuoto.")],
          [("Perché la torre di Pisa non cade?", "Perché la verticale dal baricentro cade ancora dentro la base."), ("Il braccio umano è una leva?", "Sì: l’avambraccio è una leva di terzo genere con il gomito come fulcro.")],
          [("Genere della leva", [("forbici", "primo genere"), ("altalena a bilico", "primo genere"), ("pinze", "primo genere"), ("bilancia a due piatti", "primo genere"), ("carriola", "secondo genere"),
                                  ("schiaccianoci", "secondo genere"), ("apribottiglie", "secondo genere"), ("pinzette", "terzo genere"), ("canna da pesca", "terzo genere"), ("avambraccio", "terzo genere")],
            "Che leva è: {k}?", None, ("non è una leva",)),
           ("Parti ed equilibrio", [("fulcro", "il punto di appoggio della leva"), ("potenza", "la forza che si applica"), ("resistenza", "la forza da vincere"), ("braccio", "distanza dal fulcro"),
                                    ("baricentro", "il punto in cui si concentra il peso"), ("equilibrio stabile", "il corpo torna nella posizione iniziale"),
                                    ("equilibrio instabile", "il corpo si allontana dalla posizione iniziale"), ("equilibrio indifferente", "il corpo resta in ogni nuova posizione")],
            "Che cos’è: {k}?", D),
           ("Vantaggiose o no", {"le leve sempre vantaggiose": ["carriola", "schiaccianoci", "apribottiglie", "remo della barca", "spremiaglio"],
                                 "le leve sempre svantaggiose": ["pinzette", "canna da pesca", "avambraccio", "scopa", "pinze per il ghiaccio"],
                                 "i corpi in equilibrio stabile": ["lampadario appeso", "pendolo fermo", "pallina in fondo a una ciotola", "quadro appeso al chiodo", "altalena ferma"]})],
          ["La carriola è una leva di secondo genere.", "Le forbici sono una leva di primo genere.", "Le pinzette sono svantaggiose.", "P × bp = R × br.", "Il baricentro è il punto di applicazione del peso.",
           "Un lampadario appeso è in equilibrio stabile.", "L’avambraccio è una leva di terzo genere."],
          [("La carriola è di primo genere.", "È di secondo genere."), ("Le pinzette sono vantaggiose.", "Sono svantaggiose."), ("Il fulcro è la forza applicata.", "È il punto di appoggio."),
           ("P + bp = R + br.", "P × bp = R × br."), ("Un lampadario appeso è in equilibrio instabile.", "È stabile.")],
          "le leve", "forces-and-motion", calc=f_forze),

        H("FC", "pressione-e-galleggiamento", "Pressione e galleggiamento", "Pressione e galleggiamento",
          "L’alunno calcola la pressione, descrive la pressione nei liquidi e atmosferica, il principio di Pascal e il principio di Archimede con il galleggiamento.",
          "pressione, pascal, superficie, pressione idrostatica, pressione atmosferica, principio di Pascal, vasi comunicanti, spinta di Archimede, densità, galleggiamento",
          "Pressione = forza : superficie", "Un corpo galleggia se è meno denso del liquido.",
          ["La pressione è la forza divisa per la superficie: p = F : S, in pascal (Pa).", "Nei liquidi la pressione cresce con la profondità: p = d × g × h.",
           "Un corpo immerso riceve una spinta verso l’alto uguale al peso del liquido spostato (Archimede): galleggia se è meno denso del liquido."],
          [("Perché gli sci non affondano nella neve?", ["Il peso è lo stesso.", "La superficie è molto più grande."], "Perché la pressione è più piccola.")],
          [("Una nave di ferro dovrebbe affondare.", "La nave è piena d’aria: la sua densità media è minore dell’acqua."), ("La pressione dipende solo dalla forza.", "Dipende anche dalla superficie.")],
          [("Perché le orecchie fanno male in fondo alla piscina?", "La pressione dell’acqua cresce con la profondità."), ("Come funziona un sollevatore idraulico?", "Per il principio di Pascal la pressione si trasmette uguale in tutto il liquido.")],
          [("Galleggia o affonda in acqua?", [("sughero", "galleggia"), ("ghiaccio", "galleggia"), ("legno di pino", "galleggia"), ("olio", "galleggia"), ("polistirolo", "galleggia"),
                                              ("ferro", "affonda"), ("sasso", "affonda"), ("piombo", "affonda"), ("moneta", "affonda"), ("vetro pieno", "affonda")],
            "Che cosa fa nell’acqua: {k}?", None, ("si scioglie", "evapora")),
           ("Principi", [("principio di Archimede", "un corpo immerso riceve una spinta verso l’alto"), ("principio di Pascal", "la pressione si trasmette uguale in tutto il liquido"),
                         ("legge di Stevino", "la pressione cresce con la profondità"), ("vasi comunicanti", "il liquido raggiunge lo stesso livello"),
                         ("esperienza di Torricelli", "misura la pressione atmosferica con il mercurio"), ("pressione atmosferica", "il peso dell’aria sopra di noi"),
                         ("densità", "massa divisa per volume")],
            "Che cosa dice o indica: {k}?", D),
           ("Applicazioni", {"le applicazioni del principio di Pascal": ["freni idraulici", "martinetto idraulico", "sollevatore dell’officina", "pressa idraulica"],
                             "le applicazioni del principio di Archimede": ["nave", "sottomarino", "salvagente", "mongolfiera", "densimetro"],
                             "i modi per ridurre la pressione": ["racchette da neve", "cingoli del carro armato", "sci larghi", "zaino con spallacci larghi", "ruote larghe del trattore"]})],
          ["p = F : S.", "Il sughero galleggia sull’acqua.", "La pressione dell’acqua cresce con la profondità.", "La spinta di Archimede è verso l’alto.", "Il ghiaccio galleggia.",
           "Torricelli misurò la pressione atmosferica.", "I freni idraulici usano il principio di Pascal."],
          [("p = F × S.", "p = F : S."), ("Il ferro galleggia nell’acqua.", "Affonda."), ("In profondità la pressione diminuisce.", "Aumenta."), ("La spinta di Archimede è verso il basso.", "È verso l’alto."),
           ("Una superficie più grande aumenta la pressione.", "La diminuisce.")],
          "la pressione", "forces-and-motion", calc=f_press),

        H("B", "apparato-locomotore", "L’apparato locomotore: ossa e muscoli", "Apparato locomotore",
          "L’alunno descrive lo scheletro, la struttura delle ossa, le articolazioni, i muscoli scheletrici, lisci e cardiaco e il loro lavoro in coppia.",
          "scheletro, ossa lunghe, piatte e corte, midollo osseo, articolazioni, cartilagine, legamenti, tendini, muscoli scheletrici, lisci e cardiaco, flessori ed estensori",
          "Ossa e muscoli lavorano insieme", "I muscoli lavorano in coppia: uno si contrae e l’altro si rilassa.",
          ["Lo scheletro sostiene, protegge e produce le cellule del sangue nel midollo osseo rosso.", "Le ossa si uniscono nelle articolazioni: mobili (ginocchio), semimobili (vertebre) e fisse (cranio).",
           "I muscoli scheletrici sono volontari; quelli lisci (stomaco) e il cardiaco (cuore) sono involontari."],
          [("Quando pieghi il braccio, che cosa fa il bicipite?", ["Il bicipite si contrae e si accorcia.", "Il tricipite si rilassa."], "Si contrae.")],
          [("Le ossa sono solo calcio.", "Sono tessuto vivo con cellule, vasi e nervi."), ("Il cuore è un muscolo volontario.", "È involontario.")],
          [("Che cosa sono i tendini?", "Cordoni che uniscono i muscoli alle ossa."), ("Perché i bambini si rompono meno le ossa?", "Le loro ossa sono più elastiche, con più cartilagine.")],
          [("Ossa", [("femore", "osso lungo"), ("omero", "osso lungo"), ("tibia", "osso lungo"), ("scapola", "osso piatto"), ("sterno", "osso piatto"), ("osso frontale", "osso piatto"),
                     ("vertebra", "osso corto"), ("carpo", "osso corto"), ("tarso", "osso corto")],
            "Che tipo di osso è: {k}?", None, ("cartilagine",)),
           ("Parti", [("midollo osseo rosso", "produce le cellule del sangue"), ("cartilagine", "riveste le ossa nelle articolazioni"), ("legamenti", "uniscono le ossa tra loro"),
                      ("tendini", "uniscono i muscoli alle ossa"), ("liquido sinoviale", "lubrifica le articolazioni"), ("periostio", "membrana che riveste l’osso"), ("tessuto spugnoso", "parte leggera all’interno dell’osso")],
            "Che funzione ha: {k}?", D),
           ("Muscoli e articolazioni", {"i muscoli volontari": ["bicipite", "tricipite", "quadricipite", "deltoide", "gluteo"], "i muscoli involontari": ["cuore", "muscoli dello stomaco", "muscoli dell’intestino", "muscoli dei vasi sanguigni"],
                                        "le articolazioni mobili": ["ginocchio", "spalla", "gomito", "anca", "caviglia"], "le articolazioni fisse": ["ossa del cranio", "ossa del bacino saldate"]})],
          ["Il femore è un osso lungo.", "I tendini uniscono muscoli e ossa.", "Il cuore è un muscolo involontario.", "Il midollo rosso produce cellule del sangue.", "I muscoli lavorano in coppia.",
           "Il ginocchio è un’articolazione mobile.", "Le ossa del cranio sono unite in modo fisso."],
          [("Il cuore è un muscolo volontario.", "È involontario."), ("I legamenti uniscono muscoli e ossa.", "Lo fanno i tendini."), ("Le ossa sono materiale morto.", "Sono tessuto vivo."),
           ("Le vertebre sono ossa lunghe.", "Sono ossa corte."), ("I muscoli spingono le ossa.", "Possono solo tirare.")],
          "l’apparato locomotore", "living-things-and-ecosystems"),

        H("B", "alimentazione-e-digestione", "Alimentazione e apparato digerente", "Alimentazione e digestione",
          "L’alunno conosce i principi nutritivi e il loro ruolo, i principi della dieta mediterranea, l’apparato digerente con gli enzimi e calcola il fabbisogno energetico.",
          "carboidrati, proteine, lipidi, vitamine, sali minerali, fibre, kcal, dieta mediterranea, bocca, stomaco, intestino, fegato, pancreas, enzimi, villi",
          "Carboidrati per l’energia, proteine per costruire", "Gli enzimi spezzano il cibo in molecole che passano nel sangue dall’intestino tenue.",
          ["I carboidrati e i lipidi danno energia; le proteine servono a costruire e riparare; vitamine e sali minerali regolano il corpo.", "1 g di carboidrati o proteine dà circa 4 kcal; 1 g di grassi circa 9 kcal.",
           "La digestione comincia in bocca (amilasi salivare), continua nello stomaco (pepsina) e finisce nel duodeno con bile e succo pancreatico; i villi assorbono."],
          [("Quante kcal danno 10 g di olio?", ["L’olio è grasso.", "10 × 9 = 90."], "90 kcal.")],
          [("I grassi vanno eliminati del tutto.", "Servono, ma in quantità moderata."), ("La bile è un enzima.", "Emulsiona i grassi ma non è un enzima.")],
          [("Che cos’è la dieta mediterranea?", "Un modo di mangiare ricco di cereali, legumi, verdura, frutta e olio d’oliva."), ("A che cosa servono le fibre?", "Aiutano l’intestino a funzionare bene.")],
          [("Principi nutritivi", [("pasta", "carboidrati"), ("pane", "carboidrati"), ("patate", "carboidrati"), ("bistecca", "proteine"), ("lenticchie", "proteine"), ("pesce", "proteine"),
                                   ("olio d’oliva", "lipidi"), ("burro", "lipidi"), ("arancia", "vitamine"), ("kiwi", "vitamine"), ("formaggio", "calcio")],
            "Quale principio nutritivo prevale in: {k}?", None),
           ("Organi e succhi", [("bocca", "la saliva inizia a digerire l’amido"), ("stomaco", "il succo gastrico digerisce le proteine"), ("fegato", "produce la bile"), ("cistifellea", "conserva la bile"),
                                ("pancreas", "produce il succo pancreatico"), ("intestino tenue", "assorbe i nutrienti con i villi"), ("intestino crasso", "assorbe l’acqua"), ("esofago", "porta il bolo allo stomaco")],
            "Che cosa fa: {k}?", D),
           ("Funzioni", {"i nutrienti che danno soprattutto energia": ["carboidrati", "lipidi", "zuccheri", "amido"], "i nutrienti che costruiscono il corpo": ["proteine", "calcio", "ferro", "fosforo"],
                         "i nutrienti che regolano e proteggono": ["vitamina C", "vitamina D", "fibre", "acqua", "vitamina A"]})],
          ["La pasta contiene carboidrati.", "Le proteine costruiscono il corpo.", "1 g di grassi dà circa 9 kcal.", "I villi assorbono i nutrienti.", "Il fegato produce la bile.",
           "La digestione comincia in bocca.", "La dieta mediterranea è ricca di legumi e verdura."],
          [("La bile è prodotta dal pancreas.", "La produce il fegato."), ("Le proteine danno 9 kcal per grammo.", "Ne danno circa 4."), ("La digestione comincia nello stomaco.", "Comincia in bocca."),
           ("L’olio contiene proteine.", "Contiene lipidi."), ("L’intestino crasso assorbe i nutrienti.", "Assorbe soprattutto acqua.")],
          "l’alimentazione", "living-things-and-ecosystems"),

        H("B", "respirazione-e-circolazione", "Apparato respiratorio e circolatorio", "Respirazione e circolazione",
          "L’alunno descrive le vie respiratorie, gli scambi negli alveoli, il cuore con atri e ventricoli, la piccola e la grande circolazione, il sangue e i danni del fumo.",
          "vie respiratorie, alveoli, diaframma, scambi gassosi, cuore, atri, ventricoli, valvole, piccola e grande circolazione, arterie, vene, capillari, sangue, fumo",
          "Grande e piccola circolazione", "Nella piccola circolazione il sangue va ai polmoni e prende ossigeno.",
          ["L’aria passa da naso, faringe, laringe, trachea e bronchi agli alveoli, dove avvengono gli scambi gassosi.", "Il cuore ha quattro cavità: due atri e due ventricoli.",
           "Piccola circolazione: dal ventricolo destro ai polmoni e ritorno all’atrio sinistro. Grande circolazione: dal ventricolo sinistro a tutto il corpo e ritorno all’atrio destro."],
          [("Da quale cavità parte l’aorta?", ["L’aorta porta il sangue a tutto il corpo.", "Parte dalla grande circolazione."], "Dal ventricolo sinistro.")],
          [("Le arterie portano sempre sangue ossigenato.", "L’arteria polmonare porta sangue povero di ossigeno."), ("Il fumo fa male solo ai polmoni.", "Danneggia anche cuore e vasi.")],
          [("Perché il ventricolo sinistro ha la parete più spessa?", "Deve spingere il sangue in tutto il corpo."), ("Che cosa fanno le valvole del cuore?", "Impediscono al sangue di tornare indietro.")],
          [("Le vie", [("naso", "filtra e scalda l’aria"), ("laringe", "contiene le corde vocali"), ("trachea", "tubo con anelli di cartilagine"), ("bronchi", "portano l’aria nei polmoni"),
                       ("alveoli", "piccoli sacchetti dove avviene lo scambio dei gas"), ("diaframma", "muscolo che fa entrare l’aria"), ("pleura", "membrana che avvolge i polmoni"), ("epiglottide", "chiude la laringe quando deglutiamo")],
            "Che funzione ha: {k}?", D),
           ("Il cuore", [("atrio destro", "riceve il sangue dalle vene cave"), ("ventricolo destro", "spinge il sangue ai polmoni"), ("atrio sinistro", "riceve il sangue dalle vene polmonari"),
                         ("ventricolo sinistro", "spinge il sangue nell’aorta"), ("aorta", "la grande arteria che parte dal cuore"), ("valvole cardiache", "impediscono il riflusso del sangue"),
                         ("setto", "parete che divide la metà destra del cuore dalla sinistra")],
            "Che funzione ha: {k}?", D),
           ("Sangue e salute", {"i componenti del sangue": ["plasma", "globuli rossi", "globuli bianchi", "piastrine", "emoglobina"],
                                "le sostanze dannose del fumo": ["nicotina", "catrame", "monossido di carbonio", "benzene", "polveri"],
                                "le buone abitudini per cuore e polmoni": ["fare attività fisica", "non fumare", "mangiare poco sale", "dormire bene", "camminare ogni giorno"]})],
          ["Gli scambi gassosi avvengono negli alveoli.", "Il cuore ha due atri e due ventricoli.", "L’aorta parte dal ventricolo sinistro.", "Le valvole impediscono il riflusso.",
           "La piccola circolazione passa per i polmoni.", "Il diaframma aiuta la respirazione.", "Il fumo contiene catrame."],
          [("Il cuore ha due cavità.", "Ne ha quattro."), ("L’aorta parte dal ventricolo destro.", "Parte dal sinistro."), ("Gli scambi avvengono nella trachea.", "Avvengono negli alveoli."),
           ("L’arteria polmonare porta sangue ossigenato.", "Porta sangue povero di ossigeno."), ("Il fumo non danneggia il cuore.", "Danneggia anche cuore e vasi.")],
          "respirazione e circolazione", "living-things-and-ecosystems"),
    ]
