# -*- coding: utf-8 -*-
"""Italia / Scienze: prima media（scuola secondaria di primo grado）"""
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"


def f_misure(R):
    k = R.choice(["dens", "massa", "vol", "conv", "conv2", "media"])
    if k == "dens":
        m, v = R.choice([(540, 200), (270, 100), (79, 10), (180, 20), (96, 120), (113, 10), (390, 50), (46, 50)])
        d = m / v
        return nq("Un oggetto ha massa %d g e volume %d cm³. Qual è la sua densità?" % (m, v), d, [v / m, m * v, m - v, d * 10], "g/cm³",
                  "d = m : V = %d : %d = %s g/cm³." % (m, v, num(d)))
    if k == "massa":
        d, v = R.choice([(2.7, 50), (7.9, 20), (1.0, 250), (0.9, 40), (11.3, 10), (0.8, 100), (19.3, 5)])
        return nq("Un materiale ha densità %s g/cm³. Che massa hanno %d cm³?" % (num(d), v), d * v, [v / d, d + v, d * v / 10, v], "g",
                  "m = d × V = %s × %d = %s g." % (num(d), v, num(d * v)))
    if k == "vol":
        a, b = R.choice([(50, 62), (40, 55), (100, 118), (60, 73), (30, 48), (70, 86), (80, 99)])
        return nq("In un cilindro graduato ci sono %d ml d’acqua. Immergiamo un sasso e il livello sale a %d ml. Qual è il volume del sasso?" % (a, b), b - a,
                  [a + b, b, a, (b - a) * 10], "cm³", "V = %d − %d = %d ml = %d cm³." % (b, a, b - a, b - a))
    if k == "conv":
        x, u1, f, u2 = R.choice([(3.5, "kg", 1000, "g"), (250, "cm", 0.01, "m"), (2.4, "l", 1000, "ml"), (1500, "m", 0.001, "km"), (45, "mm", 0.1, "cm"), (750, "g", 0.001, "kg"),
                                 (1.2, "km", 1000, "m"), (3, "dm³", 1000, "cm³")])
        return nq("Quanto vale %s %s in %s?" % (num(x), u1, u2), x * f, [x / f, x * f * 10, x * f / 10, x], u2,
                  "%s %s = %s %s." % (num(x), u1, num(x * f), u2))
    if k == "conv2":
        a, b = R.choice([(2, 15), (1, 45), (3, 20), (4, 10), (2, 40), (1, 30)])
        return nq("Quanti minuti sono %d h e %d min?" % (a, b), a * 60 + b, [a * 100 + b, a + b, a * 60, a * 60 - b], "min", "%d × 60 + %d = %d minuti." % (a, b, a * 60 + b))
    v = R.choice([(12, 14, 13, 15), (20, 22, 24, 18), (7, 9, 8, 8), (31, 29, 30, 34), (10, 12, 11, 15)])
    m = sum(v) / 4
    return nq("Misuri quattro volte la stessa altezza: %s cm. Qual è il valore medio?" % "; ".join(str(x) for x in v), m, [sum(v), max(v), min(v), (max(v) + min(v)) / 2 + 1], "cm",
              "Si sommano le misure e si divide per 4: %d : 4 = %s cm." % (sum(v), num(m)))


def f_calore(R):
    k = R.choice(["q", "dt", "conv", "k", "mix"])
    if k == "q":
        m, dt = R.choice([(2, 10), (1, 25), (3, 20), (0.5, 40), (4, 5), (1.5, 30)])
        q = 4186 * m * dt
        return nq("Quanta energia serve per scaldare %s kg d’acqua di %d °C? (c = 4186 J/(kg·°C))" % (num(m), dt), q, [4186 * m, 4186 * dt, q / 1000, m * dt], "J",
                  "Q = c × m × ΔT = 4186 × %s × %d = %s J." % (num(m), dt, num(q)))
    if k == "dt":
        a, b = R.choice([(18, 75), (12, 40), (-5, 20), (22, 100), (35, 8), (60, 25), (-8, 14)])
        sa = ("−%d" % -a) if a < 0 else str(a)
        if b > a:
            e = "ΔT = %d − (%s) = %d °C." % (b, sa, b - a) if a < 0 else "ΔT = %d − %d = %d °C." % (b, a, b - a)
        else:
            e = "La temperatura cala: %d − %d = %d °C in meno." % (a, b, a - b)
        return nq("La temperatura passa da %s °C a %d °C. Di quanti gradi varia?" % (sa, b), abs(b - a), [a + b if a + b > 0 else abs(a) + b + 5, b, abs(a), abs(b - a) + 10], "°C", e)
    if k == "conv":
        x, u1, f, u2 = R.choice([(3.5, "kg", 1000, "g"), (250, "cm", 0.01, "m"), (2.4, "l", 1000, "ml"), (1500, "m", 0.001, "km"), (45, "mm", 0.1, "cm"), (750, "g", 0.001, "kg"),
                                 (1.2, "km", 1000, "m"), (3, "dm³", 1000, "cm³")])
        return nq("Quanto vale %s %s in %s?" % (num(x), u1, u2), x * f, [x / f, x * f * 10, x * f / 10, x], u2,
                  "%s %s = %s %s." % (num(x), u1, num(x * f), u2))
    if k == "conv2":
        a, b = R.choice([(2, 15), (1, 45), (3, 20), (4, 10), (2, 40), (1, 30)])
        return nq("Quanti minuti sono %d h e %d min?" % (a, b), a * 60 + b, [a * 100 + b, a + b, a * 60, a * 60 - b], "min", "%d × 60 + %d = %d minuti." % (a, b, a * 60 + b))
    v = R.choice([(12, 14, 13, 15), (20, 22, 24, 18), (7, 9, 8, 8), (31, 29, 30, 34), (10, 12, 11, 15)])
    m = sum(v) / 4
    return nq("Misuri quattro volte la stessa altezza: %s cm. Qual è il valore medio?" % "; ".join(str(x) for x in v), m, [sum(v), max(v), min(v), (max(v) + min(v)) / 2 + 1], "cm",
              "Si sommano le misure e si divide per 4: %d : 4 = %s cm." % (sum(v), num(m)))


def f_calore(R):
    k = R.choice(["q", "dt", "conv", "k", "mix"])
    if k == "q":
        m, dt = R.choice([(2, 10), (1, 25), (3, 20), (0.5, 40), (4, 5), (1.5, 30)])
        q = 4186 * m * dt
        return nq("Quanta energia serve per scaldare %s kg d’acqua di %d °C? (c = 4186 J/(kg·°C))" % (num(m), dt), q, [4186 * m, 4186 * dt, q / 1000, m * dt], "J",
                  "Q = c × m × ΔT = 4186 × %s × %d = %s J." % (num(m), dt, num(q)))
    if k == "dt":
        a, b = R.choice([(18, 75), (12, 40), (-5, 20), (22, 100), (35, 8), (60, 25)])
        return nq("La temperatura passa da %s °C a %d °C. Di quanti gradi varia?" % (("−%d" % -a) if a < 0 else str(a), b), abs(b - a), [a + b, b, abs(a), abs(b - a) + 10], "°C",
                  "ΔT = %d − (%s) = %d °C." % (b, ("−%d" % -a) if a < 0 else str(a), b - a) if b > a else "ΔT = %d − %d = %d °C, cioè cala di %d °C." % (b, a, b - a, a - b), neg=False)
    if k == "conv":
        c = R.choice([0, 25, 37, 100, -20, 15, 50])
        return nq("Quanti kelvin sono %s °C?" % (("−%d" % -c) if c < 0 else str(c)), c + 273, [c - 273 if c > 273 else c + 100, c, 273 - c if c > 0 else c + 373], "K",
                  "T (K) = t (°C) + 273 = %d K." % (c + 273))
    if k == "k":
        t = R.choice([300, 373, 250, 310, 400, 290])
        return nq("Quanti gradi Celsius sono %d K?" % t, t - 273, [t + 273, t, 273 - t if t < 273 else t - 200], "°C", "t = T − 273 = %d °C." % (t - 273), neg=True)
    a, b, ma, mb = R.choice([(20, 80, 1, 1), (10, 70, 1, 2), (30, 90, 2, 1), (40, 60, 1, 1), (20, 50, 2, 1), (15, 75, 1, 3)])
    t = (a * ma + b * mb) / (ma + mb)
    return nq("Mescoli %d kg d’acqua a %d °C con %d kg d’acqua a %d °C. Quale temperatura finale si raggiunge?" % (ma, a, mb, b), t, [(a + b) / 2 if ma != mb else a + b, b - a, a + b, b], "°C",
              "t = (%d × %d + %d × %d) : (%d + %d) = %s °C." % (ma, a, mb, b, ma, mb, num(t)))


def UNITS(grade):
    return [
        H("FC", "metodo-scientifico-e-misure", "Il metodo scientifico e le misure", "Metodo e misure",
          "L’alunno usa il metodo sperimentale, conosce le grandezze fondamentali e le unità del Sistema Internazionale, usa strumenti di misura e calcola massa, volume e densità.",
          "metodo sperimentale, grandezze, Sistema Internazionale, unità di misura, strumenti, sensibilità, errore, massa, volume, densità",
          "Misurare è confrontare con un’unità", "La densità è massa diviso volume: d = m : V.",
          ["Il metodo sperimentale: osservazione, domanda, ipotesi, esperimento, analisi dei dati, conclusione.", "Una grandezza si misura confrontandola con un’unità del Sistema Internazionale: metro, kilogrammo, secondo.",
           "La densità dice quanta massa c’è in un volume: d = m : V. Ogni misura ha un errore."],
          [("Un cubo di 10 cm³ ha massa 27 g. Qual è la densità?", ["d = m : V.", "27 : 10 = 2,7."], "2,7 g/cm³ (alluminio).")],
          [("Massa e peso sono la stessa cosa.", "La massa si misura in kg; il peso è una forza e si misura in newton."), ("Una misura può essere senza errore.", "Ogni misura ha un’incertezza.")],
          [("Perché si ripete una misura più volte?", "Per ridurre l’errore e calcolare il valore medio."), ("Perché il ghiaccio galleggia?", "Perché ha densità minore dell’acqua (circa 0,92 g/cm³).")],
          [("Grandezze e unità", [("lunghezza", "metro"), ("massa", "kilogrammo"), ("tempo", "secondo"), ("temperatura", "kelvin"), ("volume", "metro cubo"), ("densità", "kilogrammo al metro cubo"),
                                  ("forza", "newton"), ("intensità di corrente", "ampere"), ("energia", "joule")],
            "Qual è l’unità del Sistema Internazionale per: {k}?", "Quale grandezza si misura in {v}?"),
           ("Strumenti", [("bilancia", "la massa"), ("dinamometro", "la forza peso"), ("cilindro graduato", "il volume dei liquidi"), ("calibro", "piccoli spessori"), ("cronometro", "il tempo"),
                          ("termometro", "la temperatura"), ("metro a nastro", "la lunghezza"), ("densimetro", "la densità dei liquidi")],
            "Che cosa misura: {k}?", "Quale strumento misura {v}?"),
           ("Le fasi del metodo", {"le fasi del metodo sperimentale": ["osservazione", "ipotesi", "esperimento", "analisi dei dati", "conclusione"],
                                    "le grandezze fondamentali": ["lunghezza", "massa", "tempo", "temperatura", "intensità di corrente"],
                                    "le grandezze derivate": ["area", "volume", "densità", "velocità", "pressione"]})],
          ["La densità è massa diviso volume.", "Il metro è l’unità di lunghezza.", "Ogni misura ha un errore.", "Il dinamometro misura le forze.", "Il ghiaccio è meno denso dell’acqua.",
           "Il volume è una grandezza derivata.", "Nell’esperimento si cambia una variabile alla volta."],
          [("La densità è massa per volume.", "È massa diviso volume."), ("La bilancia misura il volume.", "Misura la massa."), ("Il secondo è un’unità di massa.", "È l’unità di tempo."),
           ("Il volume è una grandezza fondamentale.", "È derivata."), ("Il ghiaccio è più denso dell’acqua.", "È meno denso: galleggia.")],
          "il metodo e le misure", "working-scientifically", calc=f_misure),

        H("FC", "stati-della-materia", "La materia e i passaggi di stato", "Stati della materia",
          "L’alunno descrive la materia come fatta di particelle, gli stati solido, liquido e aeriforme, i passaggi di stato e distingue sostanze pure, miscugli omogenei ed eterogenei.",
          "particelle, stato solido, liquido, aeriforme, fusione, solidificazione, evaporazione, ebollizione, condensazione, sublimazione, miscugli, soluzioni",
          "La materia è fatta di particelle", "Nei solidi le particelle sono vicine e ferme; nei gas lontane e veloci.",
          ["La materia è fatta di particelle piccolissime sempre in movimento.", "Nel solido le particelle vibrano al loro posto; nel liquido scorrono; nell’aeriforme si muovono libere.",
           "Durante un passaggio di stato la temperatura resta costante. Un miscuglio contiene più sostanze."],
          [("Che passaggio è la naftalina che sparisce nell’armadio?", ["Passa da solido a gas.", "Non diventa liquida."], "Sublimazione.")],
          [("Durante l’ebollizione la temperatura sale sempre.", "Resta costante a 100 °C finché c’è acqua."), ("L’evaporazione avviene solo a 100 °C.", "Avviene a ogni temperatura, in superficie.")],
          [("Che differenza c’è tra evaporazione ed ebollizione?", "L’evaporazione è in superficie e a ogni temperatura; l’ebollizione è in tutto il liquido alla temperatura di ebollizione."),
           ("Che cos’è una soluzione?", "Un miscuglio omogeneo, come l’acqua salata.")],
          [("Passaggi", [("solido → liquido", "fusione"), ("liquido → solido", "solidificazione"), ("liquido → aeriforme in superficie", "evaporazione"), ("liquido → aeriforme in tutta la massa", "ebollizione"),
                         ("aeriforme → liquido", "condensazione"), ("solido → aeriforme", "sublimazione"), ("aeriforme → solido", "brinamento")],
            "Come si chiama il passaggio {k}?", "Che passaggio è {v}?"),
           ("Miscugli", [("acqua e sale", "miscuglio omogeneo"), ("aria", "miscuglio omogeneo"), ("acqua e zucchero", "miscuglio omogeneo"), ("acqua e sabbia", "miscuglio eterogeneo"),
                         ("acqua e olio", "miscuglio eterogeneo"), ("granito", "miscuglio eterogeneo"), ("acqua distillata", "sostanza pura"), ("oro puro", "sostanza pura"), ("ossigeno", "sostanza pura")],
            "Che cos’è: {k}?", None, ("una forza",)),
           ("Separare", {"le tecniche per separare un solido non sciolto da un liquido": ["filtrazione", "decantazione", "scolatura con il colino", "centrifugazione"],
                         "le tecniche per separare due liquidi o un liquido da un solido sciolto": ["distillazione", "imbuto separatore", "cromatografia", "cristallizzazione"],
                         "gli esempi di sublimazione o brinamento": ["naftalina che sparisce", "ghiaccio secco che fuma", "brina sui vetri", "neve che sparisce senza fondere"]})],
          ["La materia è fatta di particelle.", "Nei gas le particelle sono lontane.", "Durante la fusione la temperatura resta costante.", "La sublimazione va da solido a gas.",
           "L’acqua salata è un miscuglio omogeneo.", "L’evaporazione avviene a ogni temperatura.", "La filtrazione separa un solido da un liquido."],
          [("Nei solidi le particelle sono ferme del tutto.", "Vibrano al loro posto."), ("L’acqua e l’olio formano un miscuglio omogeneo.", "È eterogeneo."),
           ("La condensazione va da liquido a gas.", "Va da gas a liquido."), ("L’evaporazione avviene solo a 100 °C.", "Avviene a ogni temperatura."), ("L’aria è una sostanza pura.", "È un miscuglio di gas.")],
          "gli stati della materia", "matter"),

        H("FC", "calore-e-temperatura", "Calore e temperatura", "Calore e temperatura",
          "L’alunno distingue calore e temperatura, usa le scale Celsius e Kelvin, descrive conduzione, convezione e irraggiamento, la dilatazione termica e calcola l’energia per scaldare l’acqua.",
          "calore, temperatura, scala Celsius e Kelvin, calore specifico, conduzione, convezione, irraggiamento, dilatazione, equilibrio termico",
          "Il calore è energia che passa", "La temperatura misura l’agitazione delle particelle. T(K) = t(°C) + 273.",
          ["La temperatura misura quanto si agitano le particelle; il calore è energia che passa dal corpo più caldo al più freddo.", "Scala Kelvin: T = t + 273. Lo zero assoluto è 0 K (−273 °C).",
           "Il calore si propaga per conduzione (nei solidi), convezione (nei fluidi) e irraggiamento (anche nel vuoto). Q = c × m × ΔT."],
          [("Quale temperatura si raggiunge mescolando 1 kg d’acqua a 20 °C e 1 kg a 60 °C?", ["Le masse sono uguali.", "La temperatura sta a metà."], "40 °C.")],
          [("Un corpo freddo contiene freddo.", "Il freddo non passa: è il calore che esce."), ("Calore e temperatura sono la stessa grandezza.", "Il calore è energia (J); la temperatura si misura in °C o K.")],
          [("Perché il mare d’estate è più fresco della sabbia?", "L’acqua ha un calore specifico alto: si scalda più lentamente."), ("Che cos’è l’equilibrio termico?", "La situazione in cui due corpi a contatto arrivano alla stessa temperatura.")],
          [("Propagazione", [("cucchiaio nel tè che si scalda", "conduzione"), ("pentola sul fornello", "conduzione"), ("termosifone che scalda la stanza", "convezione"), ("venti e brezze di mare", "convezione"),
                             ("acqua che gira nella pentola", "convezione"), ("Sole che scalda la Terra", "irraggiamento"), ("lampada a infrarossi", "irraggiamento"), ("brace del camino che scalda il viso", "irraggiamento")],
            "Come si propaga il calore: {k}?", None, ("dilatazione",)),
           ("Concetti", [("temperatura", "misura l’agitazione delle particelle"), ("calore", "energia che passa da un corpo caldo a uno freddo"), ("calore specifico", "energia per scaldare 1 kg di 1 °C"),
                         ("dilatazione", "aumento di volume con il caldo"), ("zero assoluto", "0 K, la temperatura più bassa possibile"), ("equilibrio termico", "stessa temperatura dopo il contatto"),
                         ("isolante termico", "materiale che fa passare poco calore")],
            "Che cos’è: {k}?", D),
           ("Materiali", {"i buoni conduttori di calore": ["rame", "alluminio", "argento", "ferro", "acciaio"], "gli isolanti termici": ["polistirolo", "lana", "sughero", "aria ferma", "legno"],
                          "le applicazioni della dilatazione": ["giunti dei binari", "termometro a liquido", "giunti dei ponti", "lamina bimetallica", "fili elettrici allentati d’estate"]})],
          ["T(K) = t(°C) + 273.", "Il calore passa dal caldo al freddo.", "Il vuoto lascia passare l’irraggiamento.", "L’acqua ha un calore specifico alto.", "I metalli si dilatano con il caldo.",
           "Il polistirolo è un isolante.", "Lo zero assoluto è −273 °C."],
          [("Il calore passa dal freddo al caldo.", "Passa dal caldo al freddo."), ("La convezione avviene nei solidi.", "Avviene nei fluidi."), ("0 °C corrisponde a 0 K.", "0 °C sono 273 K."),
           ("Il calore si misura in gradi.", "Il calore si misura in joule."), ("Il rame è un isolante termico.", "È un ottimo conduttore.")],
          "calore e temperatura", "energy", calc=f_calore),

        H("AT", "idrosfera-atmosfera-e-suolo", "Idrosfera, atmosfera e suolo", "Acqua, aria e suolo",
          "L’alunno descrive le caratteristiche dell’idrosfera e il ciclo dell’acqua, gli strati e la composizione dell’atmosfera, la pressione atmosferica e il suolo con i suoi orizzonti.",
          "idrosfera, acque dolci e salate, falda, ciclo dell’acqua, atmosfera, troposfera, stratosfera, ozono, pressione atmosferica, suolo, humus, orizzonti",
          "Acqua, aria e suolo: le sfere della Terra", "L’aria è circa 78 % azoto e 21 % ossigeno; quasi tutta l’acqua è salata.",
          ["Il 97 % dell’acqua della Terra è salata; l’acqua dolce è soprattutto nei ghiacciai e nelle falde.", "L’atmosfera è un miscuglio di gas (78 % azoto, 21 % ossigeno). Nella troposfera avvengono i fenomeni meteo.",
           "Il suolo nasce dalla disgregazione delle rocce e dall’humus; è diviso in orizzonti."],
          [("Perché in montagna l’acqua bolle sotto i 100 °C?", ["In alto c’è meno aria sopra di noi.", "La pressione atmosferica è più bassa."], "Perché la pressione è più bassa.")],
          [("L’ossigeno è il gas più abbondante nell’aria.", "Il più abbondante è l’azoto."), ("Il buco dell’ozono provoca l’effetto serra.", "Sono due problemi diversi.")],
          [("Che cos’è una falda acquifera?", "Acqua che si accumula nel sottosuolo tra rocce permeabili."), ("Con che cosa si misura la pressione atmosferica?", "Con il barometro.")],
          [("Strati dell’atmosfera", [("troposfera", "lo strato più basso, dove si formano le nuvole"), ("stratosfera", "contiene lo strato di ozono"), ("mesosfera", "lo strato dove bruciano le meteore"),
                                      ("termosfera", "lo strato delle aurore polari"), ("esosfera", "lo strato più esterno")],
            "Che cosa caratterizza questo strato: {k}?", "Quale strato è {v}?", ("lo strato sotto la crosta", "lo strato di humus")),
           ("Acque e suolo", [("falda acquifera", "acqua nel sottosuolo"), ("ghiacciaio", "la maggiore riserva di acqua dolce"), ("estuario", "foce larga dove il mare entra nel fiume"),
                              ("delta", "foce a ventaglio formata dai sedimenti"), ("humus", "sostanza organica scura del suolo"), ("roccia madre", "lo strato da cui si forma il suolo"),
                              ("lago glaciale", "lago scavato da un ghiacciaio"), ("sorgente", "punto in cui l’acqua esce dal terreno")],
            "Che cos’è: {k}?", D),
           ("Composizione e pressione", {"i gas dell’atmosfera": ["azoto", "ossigeno", "argon", "anidride carbonica", "vapore acqueo"],
                                         "gli strumenti meteorologici": ["barometro", "anemometro", "igrometro", "pluviometro", "termometro"],
                                         "gli inquinanti dell’aria": ["polveri sottili", "ossidi di azoto", "monossido di carbonio", "anidride solforosa", "smog"]})],
          ["L’azoto è il gas più abbondante nell’aria.", "La maggior parte dell’acqua è salata.", "Il barometro misura la pressione.", "L’ozono si trova nella stratosfera.",
           "In montagna la pressione è più bassa.", "Il suolo contiene humus.", "I ghiacciai contengono molta acqua dolce."],
          [("L’ossigeno è il gas più abbondante.", "È l’azoto."), ("L’acqua dolce è la maggior parte.", "È solo il 3 % circa."), ("Il barometro misura la temperatura.", "Misura la pressione."),
           ("In montagna la pressione è più alta.", "È più bassa."), ("Le nuvole si formano nella stratosfera.", "Si formano nella troposfera.")],
          "acqua, aria e suolo", "earths-systems"),

        H("B", "la-cellula", "La cellula", "La cellula",
          "L’alunno descrive la cellula come unità dei viventi, ne riconosce le parti, distingue cellule procariote ed eucariote, animali e vegetali, e usa il microscopio.",
          "cellula, membrana, citoplasma, nucleo, DNA, mitocondri, cloroplasti, parete cellulare, vacuolo, procarioti, eucarioti, microscopio",
          "Tutti i viventi sono fatti di cellule", "La cellula vegetale ha parete e cloroplasti; quella animale no.",
          ["La cellula è l’unità più piccola dei viventi. Ha membrana, citoplasma e materiale genetico (DNA).", "Le cellule eucariote hanno il nucleo; quelle procariote (batteri) no.",
           "La cellula vegetale ha anche parete cellulare, cloroplasti e un grande vacuolo."],
          [("Una cellula con cloroplasti è animale o vegetale?", ["I cloroplasti fanno la fotosintesi.", "Solo le cellule vegetali li hanno."], "Vegetale.")],
          [("I batteri hanno il nucleo.", "Sono procarioti: il DNA è libero nel citoplasma."), ("Le cellule animali hanno la parete cellulare.", "Solo la membrana; la parete è delle piante e dei funghi.")],
          [("Chi ha scoperto le cellule?", "Robert Hooke nel 1665, osservando il sughero al microscopio."), ("A che cosa servono i mitocondri?", "Producono l’energia per la cellula con la respirazione.")],
          [("Organuli", [("nucleo", "contiene il DNA e controlla la cellula"), ("membrana", "regola ciò che entra ed esce"), ("citoplasma", "liquido in cui stanno gli organuli"),
                         ("mitocondrio", "produce energia"), ("cloroplasto", "fa la fotosintesi"), ("parete cellulare", "dà rigidità alla cellula vegetale"), ("vacuolo", "conserva acqua e sostanze"),
                         ("ribosoma", "costruisce le proteine")],
            "Che funzione ha: {k}?", D),
           ("Il microscopio", [("oculare", "la lente vicino all’occhio"), ("obiettivo", "la lente vicino al preparato"), ("vetrino", "il vetro su cui si mette il campione"),
                               ("tavolino", "il piano che sostiene il vetrino"), ("specchio o lampada", "illumina il preparato"), ("vite macrometrica", "mette a fuoco grossolanamente"),
                               ("vite micrometrica", "mette a fuoco con precisione")],
            "Che cos’è: {k}?", D),
           ("Tipi di cellule", {"le parti di tutte le cellule": ["membrana", "citoplasma", "DNA", "ribosomi"], "le parti solo delle cellule vegetali": ["cloroplasti", "parete di cellulosa", "grande vacuolo"],
                                "gli organismi procarioti": ["batteri", "cianobatteri", "lattobacilli", "escherichia coli", "batteri del suolo"]})],
          ["Tutti i viventi sono fatti di cellule.", "Il nucleo contiene il DNA.", "I mitocondri producono energia.", "I batteri sono procarioti.", "Le cellule vegetali hanno i cloroplasti.",
           "La membrana regola gli scambi.", "Hooke osservò per primo le cellule."],
          [("I batteri hanno il nucleo.", "Sono procarioti."), ("La cellula animale ha la parete.", "Ha solo la membrana."), ("I cloroplasti producono proteine.", "Fanno la fotosintesi."),
           ("I virus sono cellule.", "Non sono cellule."), ("Il nucleo fa la fotosintesi.", "Contiene il DNA.")],
          "la cellula", "living-things-and-ecosystems"),

        H("B", "classificazione-dei-viventi", "La classificazione dei viventi", "Classificazione",
          "L’alunno usa i criteri della classificazione (regno, phylum, classe, ordine, famiglia, genere, specie), la nomenclatura binomia di Linneo e i cinque regni.",
          "classificazione, specie, genere, famiglia, ordine, classe, phylum, regno, Linneo, nomenclatura binomia, cinque regni",
          "Regno, phylum, classe, ordine, famiglia, genere, specie", "Il nome scientifico ha due parti: genere e specie (Homo sapiens).",
          ["Classificare vuol dire raggruppare i viventi secondo le somiglianze.", "Le categorie vanno dalla più ampia alla più piccola: regno, phylum, classe, ordine, famiglia, genere, specie.",
           "Linneo inventò il nome in due parole: Felis catus (gatto), Canis lupus (lupo)."],
          [("Leone e tigre sono dello stesso genere: Panthera leo e Panthera tigris. Sono la stessa specie?", ["La prima parola è il genere.", "La seconda indica la specie."], "No, sono specie diverse dello stesso genere.")],
          [("La specie è la categoria più ampia.", "È la più piccola; la più ampia è il regno."), ("Due animali simili sono sempre della stessa specie.", "Stessa specie vuol dire che possono avere figli fertili.")],
          [("Che cos’è una specie?", "Un gruppo di individui che si incrociano e hanno figli fertili."), ("Perché si usano nomi in latino?", "Per avere un nome uguale in tutto il mondo.")],
          [("Nomi scientifici", [("Homo sapiens", "essere umano"), ("Canis lupus", "lupo"), ("Felis catus", "gatto"), ("Panthera leo", "leone"), ("Quercus robur", "farnia"),
                                 ("Apis mellifera", "ape"), ("Equus caballus", "cavallo"), ("Olea europaea", "olivo")],
            "Quale vivente ha questo nome scientifico: {k}?", "Qual è il nome scientifico di: {v}?"),
           ("Categorie", [("regno", "la categoria più ampia"), ("specie", "la categoria più piccola"), ("genere", "la prima parola del nome scientifico"), ("phylum", "categoria tra regno e classe"),
                          ("famiglia", "categoria tra ordine e genere"), ("classe", "categoria tra phylum e ordine"), ("ordine", "categoria tra classe e famiglia")],
            "Che cosa indica: {k}?", D),
           ("Regni", {"il regno delle piante": ["muschio", "felce", "pino", "girasole", "alga verde pluricellulare"], "il regno dei funghi": ["lievito", "porcino", "muffa", "tartufo", "champignon"],
                      "il regno dei protisti": ["ameba", "paramecio", "euglena", "plasmodio della malaria", "diatomea"], "il regno delle monere": ["salmonella", "lattobacillo", "cianobatterio", "streptococco", "escherichia coli"]})],
          ["La specie è la categoria più piccola.", "Il regno è la categoria più ampia.", "Il nome scientifico ha due parti.", "Linneo inventò la nomenclatura binomia.", "Il lievito è un fungo.",
           "I batteri appartengono alle monere.", "Panthera leo è il leone."],
          [("Il regno è la categoria più piccola.", "È la più ampia."), ("Il nome scientifico ha tre parti.", "Ne ha due: genere e specie."), ("Il lievito è una pianta.", "È un fungo."),
           ("L’ameba è un batterio.", "È un protista."), ("Felis catus è il cane.", "È il gatto.")],
          "la classificazione", "living-things-and-ecosystems"),

        H("B", "le-piante", "Le piante: struttura e riproduzione", "Le piante",
          "L’alunno descrive radice, fusto e foglia, la fotosintesi e la traspirazione, e distingue muschi, felci, gimnosperme e angiosperme e la riproduzione con fiori e semi.",
          "radice, fusto, foglia, fotosintesi, traspirazione, xilema, floema, muschi, felci, gimnosperme, angiosperme, fiore, impollinazione, seme",
          "Muschi, felci, gimnosperme e angiosperme", "Le angiosperme hanno fiori e semi protetti nel frutto.",
          ["La radice assorbe acqua e sali; i vasi legnosi (xilema) portano la linfa grezza, i vasi cribrosi (floema) la linfa elaborata.",
           "Nella foglia avviene la fotosintesi: 6 CO₂ + 6 H₂O + luce → glucosio + 6 O₂.", "Muschi e felci si riproducono con spore; gimnosperme (pino) e angiosperme (melo) con semi."],
          [("Il pino ha il frutto?", ["Il pino ha le pigne.", "I semi sono nudi sulle squame della pigna."], "No, è una gimnosperma: semi nudi.")],
          [("Le felci hanno i fiori.", "Si riproducono con spore."), ("La pianta respira solo con la fotosintesi.", "Respirazione e fotosintesi sono due processi diversi.")],
          [("Che cos’è l’impollinazione?", "Il trasporto del polline dallo stame al pistillo, fatto da insetti, vento o acqua."), ("Perché le foglie traspirano?", "Per far salire la linfa e raffreddare la pianta.")],
          [("Gruppi", [("muschio", "briofite"), ("epatica", "briofite"), ("felce", "pteridofite"), ("equiseto", "pteridofite"), ("pino", "gimnosperme"), ("abete", "gimnosperme"),
                       ("cipresso", "gimnosperme"), ("melo", "angiosperme"), ("rosa", "angiosperme"), ("grano", "angiosperme"), ("quercia", "angiosperme")],
            "A quale gruppo appartiene: {k}?", None),
           ("Il fiore", [("petali", "attirano gli insetti"), ("sepali", "proteggono il bocciolo"), ("stame", "produce il polline"), ("pistillo", "contiene gli ovuli"), ("ovario", "diventa il frutto"),
                         ("ovulo", "diventa il seme"), ("nettare", "liquido zuccherino che attira gli impollinatori"), ("stigma", "riceve il polline")],
            "Che funzione ha: {k}?", D),
           ("Processi", {"le sostanze che servono alla fotosintesi": ["anidride carbonica", "acqua", "luce", "clorofilla"], "le sostanze prodotte dalla fotosintesi": ["glucosio", "ossigeno", "amido"],
                         "i modi di disperdere i semi": ["vento", "animali", "acqua", "esplosione del frutto", "uccelli che mangiano i frutti"]})],
          ["Le felci si riproducono con le spore.", "Il pino è una gimnosperma.", "L’ovario diventa il frutto.", "La fotosintesi produce ossigeno.", "Lo xilema trasporta la linfa grezza.",
           "Lo stame produce il polline.", "Le angiosperme hanno il frutto."],
          [("Le felci hanno i fiori.", "Hanno le spore."), ("Il pino è un’angiosperma.", "È una gimnosperma."), ("L’ovulo diventa il frutto.", "Diventa il seme."),
           ("La fotosintesi consuma ossigeno.", "Produce ossigeno."), ("Lo stame riceve il polline.", "Lo produce; lo stigma lo riceve.")],
          "le piante", "living-things-and-ecosystems"),

        H("B", "gli-animali", "Gli animali: invertebrati e vertebrati", "Gli animali",
          "L’alunno classifica gli animali in invertebrati (poriferi, celenterati, platelminti, anellidi, molluschi, artropodi, echinodermi) e vertebrati (pesci, anfibi, rettili, uccelli, mammiferi).",
          "invertebrati, poriferi, celenterati, anellidi, molluschi, artropodi, echinodermi, vertebrati, pesci, anfibi, rettili, uccelli, mammiferi, omeotermi, eterotermi",
          "Il 95 % degli animali è invertebrato", "Uccelli e mammiferi sono omeotermi: tengono costante la temperatura.",
          ["Gli invertebrati non hanno colonna vertebrale; gli artropodi sono il gruppo più numeroso.", "I vertebrati hanno scheletro interno e si dividono in pesci, anfibi, rettili, uccelli e mammiferi.",
           "Pesci, anfibi e rettili sono eterotermi; uccelli e mammiferi sono omeotermi."],
          [("La medusa è un pesce?", ["Non ha scheletro.", "Ha tentacoli urticanti."], "No, è un celenterato.")],
          [("I serpenti sono a sangue caldo.", "Sono eterotermi: dipendono dal calore esterno."), ("Gli anfibi vivono solo in acqua.", "Vivono in acqua da larve e anche sulla terra da adulti.")],
          [("Che cosa vuol dire omeotermo?", "Che mantiene costante la temperatura del corpo, come noi."), ("Qual è il gruppo di animali più numeroso?", "Gli artropodi, soprattutto gli insetti.")],
          [("Phylum", [("spugna", "poriferi"), ("medusa", "celenterati"), ("corallo", "celenterati"), ("tenia", "platelminti"), ("lombrico", "anellidi"), ("sanguisuga", "anellidi"),
                       ("chiocciola", "molluschi"), ("seppia", "molluschi"), ("cozza", "molluschi"), ("ape", "artropodi"), ("ragno", "artropodi"), ("granchio", "artropodi"), ("riccio di mare", "echinodermi")],
            "A quale gruppo appartiene: {k}?", None),
           ("Vertebrati", [("pesci", "respirano con le branchie e hanno pinne"), ("anfibi", "pelle nuda e larve acquatiche"), ("rettili", "squame cornee e uova con guscio"),
                           ("uccelli", "piume, becco e ossa cave"), ("mammiferi", "peli e ghiandole mammarie")],
            "Che cosa caratterizza: {k}?", "Quale classe ha {v}?", ("esoscheletro e antenne", "tentacoli urticanti", "corpo ad anelli")),
           ("Temperatura e nascita", {"gli animali omeotermi": ["passero", "cane", "pinguino", "delfino", "pipistrello"], "gli animali eterotermi": ["lucertola", "rana", "trota", "serpente", "tartaruga"],
                                      "i mammiferi che depongono uova": ["ornitorinco", "echidna"]})],
          ["Gli artropodi sono il gruppo più numeroso.", "La medusa è un celenterato.", "Gli uccelli sono omeotermi.", "I rettili hanno squame cornee.", "Il lombrico è un anellide.",
           "La seppia è un mollusco.", "L’ornitorinco è un mammifero che depone uova."],
          [("La medusa è un pesce.", "È un celenterato."), ("I serpenti sono omeotermi.", "Sono eterotermi."), ("Il ragno è un insetto.", "È un artropode aracnide."),
           ("I mammiferi non depongono mai uova.", "L’ornitorinco le depone."), ("La seppia è un pesce.", "È un mollusco.")],
          "gli animali", "living-things-and-ecosystems"),

        H("B", "ecosistemi", "Gli ecosistemi", "Ecosistemi",
          "L’alunno descrive gli ecosistemi, i fattori biotici e abiotici, le catene e reti alimentari, la piramide ecologica, i cicli della materia e le relazioni tra viventi.",
          "ecosistema, biotico, abiotico, habitat, nicchia, popolazione, comunità, produttori, consumatori, decompositori, piramide ecologica, simbiosi, parassitismo",
          "Energia che scorre, materia che ricicla", "Da un livello al successivo passa solo il 10 % circa dell’energia.",
          ["Un ecosistema comprende viventi (fattori biotici) e ambiente fisico (fattori abiotici).", "L’energia del Sole entra con i produttori e passa ai consumatori; a ogni livello se ne perde circa il 90 %.",
           "La materia invece ricicla: i decompositori restituiscono i sali minerali al suolo."],
          [("Se le piante di un prato hanno 10 000 kJ di energia, quanta ne arriva agli erbivori?", ["Passa circa il 10 %.", "10 000 × 0,1."], "Circa 1000 kJ.")],
          [("L’energia ricicla come la materia.", "L’energia si disperde in calore; la materia ricicla."), ("Il parassita uccide sempre l’ospite.", "Di solito lo indebolisce senza ucciderlo.")],
          [("Che differenza c’è tra habitat e nicchia ecologica?", "L’habitat è il luogo; la nicchia è il ruolo della specie."), ("Che cos’è una popolazione?", "L’insieme degli individui di una specie in un luogo.")],
          [("Relazioni", [("ape e fiore", "mutualismo"), ("licheni (alga e fungo)", "mutualismo"), ("pesce pagliaccio e anemone", "mutualismo"), ("zecca e cane", "parassitismo"),
                          ("tenia e uomo", "parassitismo"), ("pulce e gatto", "parassitismo"), ("lupo e cervo", "predazione"), ("gufo e topo", "predazione"), ("remora e squalo", "commensalismo")],
            "Che tipo di relazione c’è: {k}?", None, ("competizione",)),
           ("Concetti", [("fattore biotico", "un vivente dell’ecosistema"), ("fattore abiotico", "un elemento fisico come luce o temperatura"), ("habitat", "il luogo dove vive una specie"),
                         ("nicchia ecologica", "il ruolo di una specie nell’ecosistema"), ("popolazione", "individui della stessa specie in un luogo"), ("comunità", "tutte le popolazioni di un luogo"),
                         ("biosfera", "l’insieme di tutti gli ecosistemi della Terra"), ("piramide ecologica", "rappresenta l’energia nei livelli trofici")],
            "Che cos’è: {k}?", D),
           ("Biotico o abiotico", {"i fattori biotici": ["alghe", "batteri", "insetti", "erba", "uccelli"], "i fattori abiotici": ["luce", "temperatura", "acqua", "suolo", "umidità"],
                                    "i decompositori": ["funghi", "batteri del suolo", "lombrichi", "muffe", "porcellini di terra"]})],
          ["I produttori sono le piante.", "Da un livello al successivo passa circa il 10 % dell’energia.", "I decompositori riciclano la materia.", "La luce è un fattore abiotico.",
           "L’ape e il fiore vivono in mutualismo.", "La zecca è un parassita.", "La comunità è l’insieme delle popolazioni."],
          [("L’energia ricicla.", "L’energia si disperde come calore."), ("La temperatura è un fattore biotico.", "È abiotico."), ("La zecca vive in mutualismo con il cane.", "È un parassita."),
           ("Passa il 90 % dell’energia al livello successivo.", "Ne passa circa il 10 %."), ("La popolazione comprende più specie.", "È una sola specie.")],
          "gli ecosistemi", "living-things-and-ecosystems"),
    ]
