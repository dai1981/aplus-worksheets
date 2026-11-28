# -*- coding: utf-8 -*-
"""Italia / Scienze: terza media（scuola secondaria di primo grado）"""
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"
G = 9.8


def f_gen(R):
    k = R.choice(["cruce", "fen", "sangue", "sesso", "cromo"])
    if k == "cruce":
        p1, p2, tr, dom, rec = R.choice([("Aa", "Aa", "semi di pisello", "gialli", "verdi"), ("Aa", "aa", "semi di pisello", "lisci", "rugosi"), ("Aa", "Aa", "fiori", "viola", "bianchi"),
                                         ("Aa", "aa", "occhi", "scuri", "chiari"), ("Aa", "Aa", "pelo della cavia", "nero", "bianco"), ("Aa", "aa", "fiori di pisello", "viola", "bianchi")])
        pr = (25 if p2 == "Aa" else 50)
        return nq("Si incrociano %s × %s per il colore dei %s (%s dominante su %s). Quale percentuale dei figli avrà %s %s?" % (p1, p2, tr, dom, rec, tr, rec), pr,
                  [100 - pr, pr / 2, 100 if pr == 50 else 50, 75 if pr == 50 else 100], "%", "Solo gli aa mostrano il carattere recessivo: %d %% dei figli." % pr)
    if k == "fen":
        p1, p2 = R.choice([("AA", "aa"), ("Aa", "Aa"), ("Aa", "aa"), ("AA", "Aa")])
        dom = {("AA", "aa"): 100, ("Aa", "Aa"): 75, ("Aa", "aa"): 50, ("AA", "Aa"): 100}[(p1, p2)]
        het = {("AA", "aa"): 100, ("Aa", "Aa"): 50, ("Aa", "aa"): 50, ("AA", "Aa"): 50}[(p1, p2)]
        if R.random() < 0.5:
            return nq("Nell’incrocio %s × %s, quale percentuale dei figli sarà eterozigote (Aa)?" % (p1, p2), het, [25, 75, 100 if het != 100 else 50], "%",
                      "Il quadrato di Punnett mostra che il %d %% è Aa." % het)
        return nq("Nell’incrocio %s × %s (A dominante), quale percentuale mostrerà il carattere dominante?" % (p1, p2), dom, [25, 50 if dom != 50 else 75, 100 if dom != 100 else 75], "%",
                  "Mostrano il carattere dominante AA e Aa: %d %%." % dom)
    if k == "sangue":
        a, b, ans, w = R.choice([("IᴬIᴬ", "ii", "A", ["0", "AB", "B"]), ("IᴬIᴮ", "ii", "A e B", ["AB e 0", "solo AB", "A, B, AB e 0"]), ("IᴬIᴬ", "IᴮIᴮ", "AB", ["A e B", "0", "solo A"]),
                                 ("ii", "ii", "0", ["A", "AB", "A e 0"]), ("Iᴬi", "Iᴮi", "A, B, AB e 0", ["solo AB", "A e B", "AB e 0"]), ("Iᴬi", "ii", "A e 0", ["solo A", "solo 0", "AB"])])
        return it("Un padre %s e una madre %s. Quali gruppi sanguigni possono avere i figli?" % (a, b), ans, w,
                  "Gli alleli Iᴬ e Iᴮ sono codominanti e dominanti su i: i figli possono essere %s." % ans)
    if k == "sesso":
        return it("Un uomo (XY) e una donna (XX) aspettano un figlio. Qual è la probabilità che sia una femmina?", "50 %", ["25 %", "75 %", "100 %"],
                  "La madre dà sempre X; il padre dà X o Y con la stessa probabilità: 50 %.")
    n, t = R.choice([(46, "cellula della pelle"), (23, "spermatozoo"), (23, "cellula uovo"), (46, "neurone"), (46, "cellula del fegato"), (23, "gamete femminile")])
    return nq("Quanti cromosomi ha una %s umana?" % t, n, [n * 2, n // 2 if n == 46 else 44, 48 if n == 46 else 24], "",
              "Le cellule del corpo hanno 46 cromosomi; i gameti 23." if n == 46 else "I gameti hanno la metà dei cromosomi: 23.")


def f_elet(R):
    k = R.choice(["V", "I", "R", "P", "E", "serie", "par"])
    if k == "V":
        i, r = R.choice([(2, 6), (0.5, 20), (3, 4), (1.5, 8), (0.2, 50), (4, 3)])
        return nq("In un resistore da %s Ω passa una corrente di %s A. Qual è la tensione ai capi?" % (num(r), num(i)), i * r, [r / i, i / r, i + r, i * r * 2], "V",
                  "V = R × I = %s × %s = %s V." % (num(r), num(i), num(i * r)))
    if k == "I":
        v, r = R.choice([(12, 4), (9, 3), (6, 12), (230, 46), (4.5, 9), (24, 8)])
        return nq("Una pila da %s V alimenta un resistore da %s Ω. Quale corrente passa?" % (num(v), num(r)), v / r, [v * r, r / v, v - r if v > r else v + r, v / r * 10], "A",
                  "I = V : R = %s : %s = %s A." % (num(v), num(r), num(v / r)))
    if k == "R":
        v, i = R.choice([(12, 2), (9, 0.5), (230, 2), (6, 0.3), (4.5, 1.5), (24, 3)])
        return nq("Con %s V passa una corrente di %s A. Qual è la resistenza?" % (num(v), num(i)), v / i, [v * i, i / v, v - i, v / i / 10], "Ω",
                  "R = V : I = %s : %s = %s Ω." % (num(v), num(i), num(v / i)))
    if k == "P":
        v, i = R.choice([(230, 2), (12, 3), (230, 10), (9, 0.5), (230, 0.5), (6, 2)])
        return nq("Un apparecchio funziona a %s V con %s A. Qual è la potenza?" % (num(v), num(i)), v * i, [v / i, v + i, i / v, v * i / 10], "W",
                  "P = V × I = %s × %s = %s W." % (num(v), num(i), num(v * i)))
    if k == "E":
        p, h = R.choice([(2000, 2), (100, 5), (1500, 3), (60, 10), (1000, 0.5), (800, 2)])
        return nq("Un apparecchio da %d W resta acceso %s ore. Quanti kWh consuma?" % (p, num(h)), p * h / 1000, [p * h, p / 1000, p * h / 100, h / p], "kWh",
                  "E = P × t = %s kW × %s h = %s kWh." % (num(p / 1000), num(h), num(p * h / 1000)))
    if k == "serie":
        a, b = R.choice([(4, 6), (10, 20), (3, 9), (15, 5), (2, 8), (12, 18)])
        return nq("Due resistori da %d Ω e %d Ω sono collegati in serie. Quanto vale la resistenza totale?" % (a, b), a + b, [a * b / (a + b), a * b, abs(a - b), (a + b) / 2], "Ω",
                  "In serie le resistenze si sommano: %d + %d = %d Ω." % (a, b, a + b))
    a, b = R.choice([(6, 6), (4, 12), (10, 10), (3, 6), (20, 20), (12, 24)])
    return nq("Due resistori da %d Ω e %d Ω sono in parallelo. Quanto vale la resistenza equivalente?" % (a, b), a * b / (a + b), [a + b, a * b, (a + b) / 2, abs(a - b) if a != b else a * 2], "Ω",
              "In parallelo: R = (%d × %d) : (%d + %d) = %s Ω." % (a, b, a, b, num(a * b / (a + b))))


def f_ener(R):
    k = R.choice(["ec", "ep", "lav", "pot", "rend"])
    if k == "ec":
        m, v = R.choice([(2, 3), (1000, 10), (60, 5), (0.5, 4), (80, 6), (1200, 20)])
        return nq("Un corpo di %s kg si muove a %s m/s. Qual è la sua energia cinetica?" % (num(m), num(v)), 0.5 * m * v * v, [m * v, m * v * v, 0.5 * m * v, m * v * v * 2], "J",
                  "Ec = ½ × m × v² = 0,5 × %s × %s² = %s J." % (num(m), num(v), num(0.5 * m * v * v)))
    if k == "ep":
        m, h = R.choice([(2, 5), (10, 3), (50, 2), (0.5, 10), (70, 4), (5, 20)])
        return nq("Un oggetto di %s kg è a %s m di altezza. Qual è la sua energia potenziale? (g = 9,8 m/s²)" % (num(m), num(h)), m * G * h, [m * h, m * G, m * G * h / 2, G * h], "J",
                  "Ep = m × g × h = %s × 9,8 × %s = %s J." % (num(m), num(h), num(m * G * h)))
    if k == "lav":
        f, s = R.choice([(50, 10), (20, 5), (100, 3), (300, 2), (15, 40), (80, 12)])
        return nq("Spingi un carrello con una forza di %d N per %d m nella stessa direzione. Quanto lavoro compi?" % (f, s), f * s, [f / s, f + s, s / f, f * s / 2], "J",
                  "L = F × s = %d × %d = %d J." % (f, s, f * s))
    if k == "pot":
        l, t = R.choice([(600, 10), (1200, 60), (500, 5), (3000, 20), (900, 30), (2400, 8)])
        return nq("Un motore compie un lavoro di %d J in %d s. Qual è la potenza?" % (l, t), l / t, [l * t, t / l, l - t, l / t * 2], "W", "P = L : t = %d : %d = %s W." % (l, t, num(l / t)))
    u, e = R.choice([(30, 100), (90, 100), (25, 200), (45, 150), (60, 80), (18, 60)])
    return nq("Un motore riceve %d J e ne trasforma %d J in lavoro utile. Qual è il rendimento?" % (e, u), u * 100 / e, [e * 100 / u, u, e - u, u / e], "%",
              "η = %d : %d × 100 = %s %%." % (u, e, num(u * 100 / e)))


def f_onde(R):
    k = R.choice(["v", "f", "lam", "eco", "tuono"])
    if k == "v":
        f, l = R.choice([(2, 3), (5, 0.5), (440, 0.78), (10, 2), (50, 0.4), (100, 3.4)])
        return nq("Un’onda ha frequenza %s Hz e lunghezza d’onda %s m. Qual è la sua velocità?" % (num(f), num(l)), f * l, [f / l, l / f, f + l, f * l * 10], "m/s",
                  "v = λ × f = %s × %s = %s m/s." % (num(l), num(f), num(f * l)))
    if k == "f":
        t = R.choice([0.5, 0.2, 0.1, 2, 0.25, 0.05])
        return nq("Un’onda ha periodo %s s. Qual è la frequenza?" % num(t), 1 / t, [t, 1 / t / 2, t * 10, 1 / t * 3], "Hz", "f = 1 : T = 1 : %s = %s Hz." % (num(t), num(1 / t)))
    if k == "lam":
        v, f = R.choice([(340, 170), (340, 680), (1500, 300), (340, 85), (1500, 750), (340, 34)])
        return nq("Un suono si propaga a %d m/s con frequenza %d Hz. Qual è la lunghezza d’onda?" % (v, f), v / f, [v * f, f / v, v - f, v / f * 2], "m",
                  "λ = v : f = %d : %d = %s m." % (v, f, num(v / f)))
    if k == "eco":
        t = R.choice([1, 2, 0.5, 3, 4, 1.5])
        return nq("Gridi davanti a una parete di roccia e senti l’eco dopo %s s. A che distanza è la parete? (v = 340 m/s)" % num(t), 340 * t / 2, [340 * t, 340 / t, 340 * t * 2, 340 * t / 4], "m",
                  "Il suono va e torna: d = 340 × %s : 2 = %s m." % (num(t), num(340 * t / 2)))
    t = R.choice([3, 5, 6, 2, 9, 4])
    return nq("Vedi un lampo e senti il tuono dopo %d s. A che distanza è il temporale? (v suono = 340 m/s)" % t, 340 * t, [340 * t / 2, 340 / t, 300000 * t, 340 * t * 2], "m",
              "La luce arriva subito; il suono impiega %d s: 340 × %d = %d m." % (t, t, 340 * t))


def UNITS(grade):
    return [
        H("B", "sistema-nervoso-e-ormoni", "Sistema nervoso e sistema endocrino", "Nervi e ormoni",
          "L’alunno descrive il neurone e l’impulso nervoso, il sistema nervoso centrale e periferico, gli organi di senso e le ghiandole endocrine con i loro ormoni.",
          "neurone, dendriti, assone, sinapsi, encefalo, midollo spinale, sistema nervoso periferico, autonomo, arco riflesso, ghiandole endocrine, ormoni, insulina",
          "Nervi veloci, ormoni lenti e duraturi", "I neuroni trasmettono impulsi elettrici; gli ormoni viaggiano nel sangue.",
          ["Il neurone riceve segnali con i dendriti e li trasmette con l’assone; tra due neuroni c’è la sinapsi.", "Il sistema nervoso centrale è formato da encefalo e midollo spinale; i nervi formano il periferico.",
           "Le ghiandole endocrine versano gli ormoni nel sangue: l’insulina del pancreas abbassa la glicemia."],
          [("Quale ghiandola produce l’adrenalina?", ["Sta sopra i reni.", "Si attiva nello spavento."], "Il surrene.")],
          [("Il cervello comanda anche i riflessi.", "Molti riflessi passano solo per il midollo spinale."), ("Gli ormoni viaggiano nei nervi.", "Viaggiano nel sangue.")],
          [("Che cos’è il diabete?", "Una malattia in cui l’insulina manca o funziona male e lo zucchero nel sangue resta alto."), ("Che cosa fa il sistema nervoso autonomo?", "Controlla cuore, respiro e digestione senza la nostra volontà.")],
          [("Ghiandole", [("ipofisi", "ormone della crescita"), ("tiroide", "tiroxina"), ("pancreas", "insulina"), ("surrene", "adrenalina"), ("ovaie", "estrogeni"), ("testicoli", "testosterone"),
                          ("epifisi", "melatonina"), ("paratiroidi", "paratormone")],
            "Quale ormone produce: {k}?", "Quale ghiandola produce: {v}?"),
           ("Parti del sistema nervoso", [("dendriti", "ricevono i segnali"), ("assone", "trasmette l’impulso"), ("sinapsi", "punto di contatto tra due neuroni"), ("cervelletto", "coordina equilibrio e movimenti"),
                                          ("tronco encefalico", "controlla respiro e battito"), ("midollo spinale", "collega encefalo e nervi e comanda i riflessi"), ("corteccia cerebrale", "pensiero, linguaggio e memoria"),
                                          ("guaina mielinica", "isola l’assone e velocizza l’impulso")],
            "Che funzione ha: {k}?", D),
           ("Centrale o periferico", {"le parti del sistema nervoso centrale": ["cervello", "cervelletto", "tronco encefalico", "midollo spinale"],
                                      "le parti del sistema nervoso periferico": ["nervi cranici", "nervi spinali", "gangli", "nervo ottico", "nervo sciatico"],
                                      "gli ormoni": ["insulina", "adrenalina", "tiroxina", "melatonina", "testosterone"]})],
          ["L’insulina abbassa lo zucchero nel sangue.", "Gli ormoni viaggiano nel sangue.", "Il midollo spinale fa parte del sistema nervoso centrale.", "La sinapsi collega due neuroni.",
           "Il cervelletto coordina l’equilibrio.", "La tiroide produce la tiroxina.", "L’assone trasmette l’impulso nervoso."],
          [("Gli ormoni viaggiano nei nervi.", "Viaggiano nel sangue."), ("L’insulina alza la glicemia.", "La abbassa."), ("Il cervelletto controlla il linguaggio.", "Coordina equilibrio e movimenti."),
           ("I nervi fanno parte del sistema nervoso centrale.", "Fanno parte del periferico."), ("La tiroide produce l’adrenalina.", "La produce il surrene.")],
          "nervi e ormoni", "living-things-and-ecosystems"),

        H("B", "riproduzione-e-genetica", "Riproduzione, DNA ed ereditarietà", "Riproduzione e genetica",
          "L’alunno descrive l’apparato riproduttore, mitosi e meiosi, il DNA, i cromosomi e le leggi di Mendel, e calcola probabilità con il quadrato di Punnett.",
          "apparato riproduttore, gameti, fecondazione, mitosi, meiosi, DNA, geni, cromosomi, alleli, dominante, recessivo, Mendel, Punnett, gruppi sanguigni",
          "Ogni carattere dipende da due alleli", "Nell’incrocio Aa × Aa un quarto dei figli è aa.",
          ["Le cellule umane hanno 46 cromosomi; i gameti (spermatozoi e cellule uovo) ne hanno 23, prodotti con la meiosi.", "Il DNA contiene i geni; ogni gene ha due versioni (alleli), una dal padre e una dalla madre.",
           "Un allele dominante (A) copre quello recessivo (a): il carattere recessivo appare solo in aa."],
          [("Aa × aa: quale percentuale dei figli è aa?", ["Il quadrato di Punnett ha 4 caselle.", "2 caselle su 4 sono aa."], "50 %.")],
          [("Il figlio eredita tutto dal padre.", "Riceve metà dei cromosomi dal padre e metà dalla madre."), ("Un carattere dominante è il più frequente.", "Dominante vuol dire che copre l’altro allele.")],
          [("Chi era Gregor Mendel?", "Un monaco che studiò gli incroci delle piante di pisello nell’Ottocento."), ("Che differenza c’è tra mitosi e meiosi?", "La mitosi fa due cellule uguali; la meiosi quattro gameti con metà cromosomi.")],
          [("Termini", [("gene", "tratto di DNA che porta un carattere"), ("allele", "una delle versioni di un gene"), ("omozigote", "con due alleli uguali"), ("eterozigote", "con due alleli diversi"),
                        ("genotipo", "insieme degli alleli di un individuo"), ("fenotipo", "carattere visibile"), ("cromosoma", "DNA avvolto e compatto"), ("mutazione", "cambiamento del DNA")],
            "Che cos’è: {k}?", D),
           ("Riproduzione", [("testicoli", "producono gli spermatozoi"), ("ovaie", "producono le cellule uovo"), ("utero", "accoglie l’embrione"), ("tube di Falloppio", "luogo della fecondazione"),
                             ("placenta", "nutre il feto"), ("mitosi", "divisione che dà due cellule uguali"), ("meiosi", "divisione che forma i gameti"), ("fecondazione", "unione di spermatozoo e cellula uovo")],
            "Che cosa fa o che cos’è: {k}?", D),
           ("Genotipi", {"i genotipi omozigoti": ["AA", "aa", "BB", "bb", "ii"], "i genotipi eterozigoti": ["Aa", "Bb", "Cc", "Dd", "Iᴬi"],
                         "le cellule con 23 cromosomi": ["spermatozoo", "cellula uovo", "gamete maschile", "gamete femminile"]})],
          ["Le cellule umane hanno 46 cromosomi.", "I gameti si formano con la meiosi.", "Un eterozigote ha due alleli diversi.", "Mendel studiò i piselli.", "Aa × Aa dà un quarto di aa.",
           "La fecondazione avviene nelle tube.", "Il carattere recessivo appare solo negli omozigoti."],
          [("I gameti hanno 46 cromosomi.", "Ne hanno 23."), ("La mitosi forma i gameti.", "Li forma la meiosi."), ("Aa è omozigote.", "È eterozigote."), ("Il fenotipo sono gli alleli.", "Il fenotipo è il carattere visibile."),
           ("Il figlio riceve i cromosomi solo dalla madre.", "Metà dal padre e metà dalla madre.")],
          "la genetica", "living-things-and-ecosystems", calc=f_gen),

        H("B", "evoluzione", "L’evoluzione dei viventi", "L’evoluzione",
          "L’alunno descrive le prove dell’evoluzione, la teoria di Darwin della selezione naturale, la formazione di nuove specie e l’evoluzione dell’essere umano.",
          "evoluzione, fossili, Lamarck, Darwin, selezione naturale, variabilità, adattamento, speciazione, estinzione, organi omologhi, ominidi",
          "La selezione naturale premia i più adatti", "Chi è più adatto all’ambiente sopravvive e ha più figli.",
          ["Le specie cambiano nel tempo: le prove sono i fossili, gli organi omologhi e il DNA.", "Darwin: gli individui sono diversi tra loro; quelli più adatti all’ambiente sopravvivono e lasciano più figli.",
           "Lamarck pensava che i caratteri acquisiti si ereditassero: oggi sappiamo che non è così."],
          [("Perché le giraffe hanno il collo lungo, secondo Darwin?", ["C’erano giraffe con colli diversi.", "Quelle con il collo più lungo mangiavano di più e avevano più figli."], "Per selezione naturale.")],
          [("Un animale si adatta perché lo vuole.", "La variabilità nasce dal caso; l’ambiente seleziona."), ("L’uomo discende dalla scimmia di oggi.", "Uomo e scimmie hanno un antenato comune.")],
          [("Che cosa sono gli organi omologhi?", "Organi con la stessa origine ma usi diversi, come il braccio umano e l’ala del pipistrello."), ("Che cos’è un fossile?", "Un resto o un’impronta di un vivente conservato nelle rocce.")],
          [("Idee", [("Darwin", "selezione naturale"), ("Lamarck", "ereditarietà dei caratteri acquisiti"), ("Mendel", "leggi dell’ereditarietà"), ("Linneo", "nomenclatura binomia"),
                     ("Wallace", "selezione naturale scoperta insieme a Darwin"), ("Cuvier", "studio dei fossili e delle estinzioni"), ("Watson e Crick", "struttura a doppia elica del DNA")],
            "A quale idea è legato questo scienziato: {k}?", "Quale scienziato è legato a: {v}?"),
           ("Concetti", [("selezione naturale", "sopravvive e si riproduce chi è più adatto"), ("variabilità", "differenze tra individui della stessa specie"), ("adattamento", "carattere utile in un ambiente"),
                         ("speciazione", "formazione di una nuova specie"), ("estinzione", "scomparsa di una specie"), ("fossile guida", "fossile che indica l’età di una roccia"),
                         ("organi omologhi", "stessa origine, funzioni diverse"), ("organi analoghi", "stessa funzione, origine diversa")],
            "Che cos’è: {k}?", D),
           ("Esempi", {"gli organi omologhi": ["braccio umano e ala del pipistrello", "pinna della balena e zampa del cane", "zampa del cavallo e braccio della scimmia"],
                       "gli organi analoghi": ["ala della farfalla e ala dell’uccello", "occhio del polpo e occhio umano", "pinna dello squalo e pinna del delfino"],
                       "le prove dell’evoluzione": ["fossili", "somiglianze del DNA", "organi omologhi", "embrioni simili", "organi vestigiali"]})],
          ["Le specie cambiano nel tempo.", "Darwin propose la selezione naturale.", "I fossili sono prove dell’evoluzione.", "La variabilità è la base della selezione.", "Uomo e scimmie hanno un antenato comune.",
           "L’ala del pipistrello e il braccio umano sono omologhi.", "Molte specie si sono estinte."],
          [("Le specie non cambiano mai.", "Cambiano nel tempo."), ("L’uomo discende dallo scimpanzé di oggi.", "Hanno un antenato comune."), ("Lamarck propose la selezione naturale.", "La propose Darwin."),
           ("I caratteri acquisiti si ereditano.", "Non si ereditano."), ("L’ala della farfalla e quella dell’uccello sono omologhe.", "Sono analoghe.")],
          "l’evoluzione", "living-things-and-ecosystems"),

        H("FC", "elettricita", "Elettricità e circuiti", "Elettricità",
          "L’alunno descrive cariche elettriche e corrente, costruisce circuiti in serie e in parallelo, usa la legge di Ohm e calcola potenza ed energia elettrica.",
          "carica elettrica, elettrizzazione, conduttori, isolanti, corrente, tensione, resistenza, legge di Ohm, circuiti in serie e in parallelo, potenza, kWh, sicurezza",
          "Legge di Ohm: V = R × I", "La potenza è P = V × I; l’energia si paga in kWh.",
          ["Le cariche dello stesso segno si respingono, quelle di segno opposto si attraggono.", "La corrente (A) scorre in un circuito chiuso spinta dalla tensione (V); la resistenza (Ω) la frena: V = R × I.",
           "In serie le lampadine sono in fila: se una si rompe si spengono tutte; in parallelo restano accese."],
          [("Una lampadina da 6 Ω è collegata a una pila da 12 V. Quale corrente passa?", ["I = V : R.", "12 : 6 = 2."], "2 A.")],
          [("La corrente si consuma nella lampadina.", "La corrente è uguale prima e dopo; si trasforma l’energia."), ("In casa le prese sono in serie.", "Sono in parallelo.")],
          [("Perché non si tocca un filo scoperto?", "La corrente può attraversare il corpo e causare folgorazione."), ("A che cosa serve il salvavita?", "Interrompe la corrente se c’è una dispersione pericolosa.")],
          [("Grandezze", [("intensità di corrente", "ampere"), ("tensione", "volt"), ("resistenza", "ohm"), ("potenza", "watt"), ("energia elettrica in bolletta", "kilowattora"), ("carica elettrica", "coulomb")],
            "In che unità si misura: {k}?", "Quale grandezza si misura in {v}?"),
           ("Componenti", [("generatore", "fornisce la tensione"), ("interruttore", "apre e chiude il circuito"), ("amperometro", "misura la corrente"), ("voltmetro", "misura la tensione"),
                           ("resistore", "limita la corrente"), ("fusibile", "si interrompe se la corrente è troppo alta"), ("lampadina", "trasforma energia elettrica in luce"), ("filo di rame", "collega i componenti")],
            "Che funzione ha: {k}?", D),
           ("Conduttori e isolanti", {"i conduttori elettrici": ["rame", "alluminio", "argento", "acqua salata", "grafite"], "gli isolanti elettrici": ["gomma", "plastica", "vetro", "legno secco", "ceramica"],
                                       "le regole di sicurezza": ["non toccare prese con le mani bagnate", "non usare fili scoperti", "staccare la spina tirando la spina", "non sovraccaricare le ciabatte", "far riparare gli impianti a un tecnico"]})],
          ["V = R × I.", "Le cariche uguali si respingono.", "La resistenza si misura in ohm.", "In parallelo le lampadine restano accese se una si rompe.", "Il rame è un buon conduttore.",
           "La gomma è un isolante.", "P = V × I."],
          [("Le cariche uguali si attraggono.", "Si respingono."), ("La tensione si misura in ampere.", "Si misura in volt."), ("In serie le lampadine restano accese se una si rompe.", "Si spengono tutte."),
           ("Il vetro è un conduttore.", "È un isolante."), ("V = R : I.", "V = R × I.")],
          "l’elettricità", "energy", calc=f_elet),

        H("FC", "magnetismo", "Magnetismo ed elettromagnetismo", "Magnetismo",
          "L’alunno descrive i magneti e i poli, il campo magnetico terrestre e la bussola, l’esperienza di Oersted, l’elettrocalamita, il motore elettrico e l’induzione.",
          "magnete, polo nord e sud, campo magnetico, linee di forza, bussola, magnetismo terrestre, Oersted, elettrocalamita, motore elettrico, induzione, alternatore, trasformatore",
          "Poli uguali si respingono", "Una corrente crea un campo magnetico; un magnete in movimento crea corrente.",
          ["Ogni magnete ha un polo nord e un polo sud: poli uguali si respingono, opposti si attraggono.", "La Terra è un grande magnete: l’ago della bussola si orienta verso il nord.",
           "Oersted scoprì che una corrente crea un campo magnetico; Faraday che un magnete in movimento produce corrente (induzione)."],
          [("Se spezzi una calamita in due, che cosa ottieni?", ["Ogni pezzo ha due poli.", "Non si isola mai un solo polo."], "Due calamite più piccole.")],
          [("Il magnete attira tutti i metalli.", "Attira ferro, nichel e cobalto; non alluminio o rame."), ("Si può avere un solo polo.", "I poli sono sempre in coppia.")],
          [("Come funziona un’elettrocalamita?", "Una bobina di filo con nucleo di ferro diventa magnete quando passa corrente."), ("Che cosa fa un trasformatore?", "Cambia la tensione della corrente alternata.")],
          [("Dispositivi", [("bussola", "indica il nord magnetico"), ("elettrocalamita", "magnete che si accende con la corrente"), ("motore elettrico", "trasforma energia elettrica in movimento"),
                            ("alternatore", "trasforma movimento in energia elettrica"), ("trasformatore", "cambia la tensione"), ("dinamo della bicicletta", "accende la luce pedalando"),
                            ("campanello elettrico", "usa un’elettrocalamita per battere"), ("altoparlante", "usa un magnete per far vibrare una membrana")],
            "Che cosa fa: {k}?", D),
           ("Concetti", [("polo nord", "estremità che punta verso il nord geografico"), ("linee di forza", "mostrano la forma del campo magnetico"), ("esperienza di Oersted", "la corrente devia l’ago della bussola"),
                         ("induzione elettromagnetica", "un magnete che si muove crea corrente"), ("materiali ferromagnetici", "ferro, nichel e cobalto"), ("magnetosfera", "il campo magnetico intorno alla Terra"),
                         ("aurora polare", "luce prodotta dalle particelle del Sole guidate dal campo terrestre")],
            "Che cos’è: {k}?", D),
           ("Attratti o no", {"i materiali attratti dal magnete": ["ferro", "acciaio", "nichel", "cobalto", "magnetite"], "i materiali non attratti dal magnete": ["rame", "alluminio", "oro", "plastica", "legno"],
                              "i dispositivi che usano il magnetismo": ["motore elettrico", "bussola", "risonanza magnetica", "treno a levitazione magnetica", "disco rigido"]})],
          ["Poli uguali si respingono.", "La bussola si orienta verso il nord.", "La corrente crea un campo magnetico.", "Il magnete attira il ferro.", "Ogni magnete ha due poli.",
           "Il motore elettrico produce movimento.", "Faraday scoprì l’induzione."],
          [("Poli opposti si respingono.", "Si attraggono."), ("Il magnete attira l’alluminio.", "Non lo attira."), ("Spezzando un magnete si separano i poli.", "Ogni pezzo ha due poli."),
           ("La corrente non ha effetti magnetici.", "Crea un campo magnetico."), ("L’alternatore trasforma luce in corrente.", "Trasforma movimento in corrente.")],
          "il magnetismo", "energy"),

        H("FC", "energia-e-fonti", "Energia, lavoro e fonti energetiche", "Energia e fonti",
          "L’alunno calcola lavoro, potenza, energia cinetica e potenziale, applica la conservazione dell’energia e il rendimento, e valuta le fonti rinnovabili e non rinnovabili.",
          "lavoro, joule, potenza, watt, energia cinetica, energia potenziale, conservazione dell’energia, rendimento, fonti rinnovabili, combustibili fossili, effetto serra",
          "L’energia si conserva e si trasforma", "Ec = ½ m v²; Ep = m g h; lavoro L = F × s.",
          ["Il lavoro è L = F × s; la potenza è il lavoro diviso il tempo (watt).", "Energia cinetica: Ec = ½ m v². Energia potenziale: Ep = m g h.",
           "L’energia totale si conserva; una parte diventa calore. Il rendimento dice quanta energia diventa utile."],
          [("Un vaso di 2 kg è su uno scaffale a 1,5 m. Quanta energia potenziale ha?", ["Ep = m × g × h.", "2 × 9,8 × 1,5 = 29,4."], "29,4 J.")],
          [("Raddoppiando la velocità l’energia cinetica raddoppia.", "Diventa quattro volte più grande (v²)."), ("Le centrali producono energia dal nulla.", "Trasformano un’altra forma di energia.")],
          [("Perché i combustibili fossili causano l’effetto serra?", "Bruciando liberano anidride carbonica che trattiene il calore."), ("Che cos’è l’energia geotermica?", "Il calore che viene dall’interno della Terra.")],
          [("Centrali", [("centrale idroelettrica", "energia potenziale dell’acqua"), ("parco eolico", "energia cinetica del vento"), ("impianto fotovoltaico", "luce del Sole"), ("centrale geotermica", "calore interno della Terra"),
                         ("centrale termoelettrica", "combustione di combustibili fossili"), ("centrale nucleare", "fissione dell’uranio"), ("centrale a biomasse", "combustione di legna e scarti vegetali")],
            "Quale energia usa: {k}?", "Quale centrale usa: {v}?"),
           ("Concetti", [("energia cinetica", "energia di un corpo in movimento"), ("energia potenziale", "energia dovuta alla posizione"), ("lavoro", "forza per spostamento"), ("potenza", "lavoro fatto in un secondo"),
                         ("rendimento", "parte dell’energia che diventa utile"), ("joule", "unità di misura dell’energia"), ("watt", "unità di misura della potenza"), ("effetto serra", "i gas trattengono il calore della Terra")],
            "Che cos’è: {k}?", D),
           ("Fonti", {"le fonti rinnovabili": ["solare", "eolica", "idroelettrica", "geotermica", "biomasse"], "le fonti non rinnovabili": ["petrolio", "carbone", "gas naturale", "uranio"],
                      "le trasformazioni in cui l’energia potenziale diventa cinetica": ["sasso che cade", "sciatore in discesa", "acqua della cascata", "pallina che rotola giù dal tavolo", "montagne russe in discesa"]})],
          ["L’energia si conserva.", "Ec = ½ m v².", "Ep = m g h.", "Il watt è l’unità di potenza.", "Il petrolio non è rinnovabile.", "La centrale eolica usa il vento.", "Bruciare il carbone libera anidride carbonica."],
          [("L’energia si distrugge.", "Si trasforma."), ("Il joule misura la potenza.", "Misura l’energia."), ("L’uranio è una fonte rinnovabile.", "Non è rinnovabile."),
           ("Raddoppiando v, Ec raddoppia.", "Diventa quattro volte."), ("La centrale idroelettrica brucia carbone.", "Usa l’acqua.")],
          "l’energia", "energy", calc=f_ener),

        H("FC", "onde-luce-e-suono", "Onde, suono e luce", "Onde, suono e luce",
          "L’alunno descrive le onde con frequenza, periodo e lunghezza d’onda, le caratteristiche del suono e della luce, riflessione, rifrazione, lenti e lo spettro elettromagnetico.",
          "onde, ampiezza, frequenza, periodo, lunghezza d’onda, velocità, suono, altezza, intensità, timbro, eco, luce, riflessione, rifrazione, lenti, spettro",
          "v = lunghezza d’onda × frequenza", "Il suono nell’aria va a 340 m/s; la luce a 300 000 km/s.",
          ["Un’onda trasporta energia senza trasportare materia. Si descrive con ampiezza, frequenza (Hz) e lunghezza d’onda: v = λ × f.",
           "Il suono è un’onda meccanica: serve un mezzo. L’altezza dipende dalla frequenza, l’intensità dall’ampiezza.",
           "La luce si propaga anche nel vuoto a 300 000 km/s; si riflette, si rifrange e le lenti la concentrano o la allargano."],
          [("Vedi un lampo e senti il tuono dopo 3 s. Quanto è lontano il temporale?", ["La luce arriva quasi subito.", "340 × 3 = 1020."], "Circa 1 km.")],
          [("Il suono viaggia nel vuoto.", "Ha bisogno di un mezzo."), ("Un suono più acuto è più forte.", "Acuto vuol dire frequenza alta; forte vuol dire ampiezza grande.")],
          [("Perché vediamo i colori?", "Gli oggetti riflettono alcuni colori della luce bianca e assorbono gli altri."), ("Che cosa sono gli ultrasuoni?", "Suoni con frequenza oltre 20 000 Hz, che non sentiamo.")],
          [("Caratteristiche", [("altezza", "dipende dalla frequenza"), ("intensità", "dipende dall’ampiezza"), ("timbro", "distingue strumenti diversi"), ("eco", "suono riflesso da una parete"),
                                ("frequenza", "numero di oscillazioni al secondo"), ("periodo", "tempo di una oscillazione"), ("lunghezza d’onda", "distanza tra due creste"), ("decibel", "unità dell’intensità sonora")],
            "Che cos’è o da che cosa dipende: {k}?", D),
           ("Luce", [("riflessione", "la luce rimbalza su una superficie"), ("rifrazione", "la luce cambia direzione cambiando mezzo"), ("lente convergente", "concentra i raggi in un fuoco"),
                     ("lente divergente", "allarga i raggi"), ("prisma", "scompone la luce bianca nei colori"), ("specchio piano", "dà un’immagine simmetrica"), ("miopia", "si corregge con lenti divergenti"),
                     ("ipermetropia", "si corregge con lenti convergenti")],
            "Che cos’è: {k}?", D),
           ("Spettro e suoni", {"le onde elettromagnetiche": ["onde radio", "microonde", "infrarossi", "luce visibile", "raggi ultravioletti", "raggi X"],
                                "le onde meccaniche": ["suono", "onde del mare", "onde sismiche", "ultrasuoni", "onde in una corda"],
                                "i colori dello spettro visibile": ["rosso", "arancione", "giallo", "verde", "blu", "violetto"]})],
          ["v = λ × f.", "Il suono non si propaga nel vuoto.", "La luce va a circa 300 000 km/s.", "L’altezza del suono dipende dalla frequenza.", "Il prisma scompone la luce bianca.",
           "La miopia si corregge con lenti divergenti.", "Gli ultrasuoni non si sentono."],
          [("Il suono si propaga nel vuoto.", "Ha bisogno di un mezzo."), ("L’altezza dipende dall’ampiezza.", "Dipende dalla frequenza."), ("Il suono è più veloce della luce.", "La luce è molto più veloce."),
           ("La miopia si corregge con lenti convergenti.", "Con lenti divergenti."), ("Le onde trasportano materia.", "Trasportano energia.")],
          "le onde", "waves-and-light", calc=f_onde),

        H("AT", "vulcani-e-terremoti", "Struttura della Terra, vulcani e terremoti", "Vulcani e terremoti",
          "L’alunno descrive gli strati interni della Terra, la tettonica delle placche, i vulcani e i terremoti, le scale di misura e la prevenzione dei rischi in Italia.",
          "crosta, mantello, nucleo, placche, deriva dei continenti, margini, vulcani, magma, lava, terremoti, ipocentro, epicentro, onde sismiche, scala Richter e Mercalli, rischio",
          "La crosta è divisa in placche che si muovono", "Vulcani e terremoti si concentrano ai margini delle placche.",
          ["La Terra ha crosta, mantello e nucleo. La crosta e la parte alta del mantello formano la litosfera, divisa in placche.",
           "Le placche si allontanano, si scontrano o scorrono: ai margini nascono vulcani, catene montuose e terremoti.",
           "Il terremoto parte dall’ipocentro; l’epicentro è il punto in superficie sopra di esso. La magnitudo si misura con la scala Richter."],
          [("Perché in Italia ci sono vulcani e terremoti?", ["L’Italia è dove si incontrano la placca africana e quella euroasiatica.", "Le placche si spingono."], "Perché è al margine tra due placche.")],
          [("Il magma e la lava sono la stessa cosa.", "Il magma è sotto terra; quando esce si chiama lava."), ("La scala Mercalli misura l’energia.", "Misura gli effetti; la Richter misura l’energia (magnitudo).")],
          [("Chi propose la deriva dei continenti?", "Alfred Wegener, nel 1912."), ("Che cosa fare durante un terremoto?", "Ripararsi sotto un tavolo o vicino a un muro portante, lontano da finestre.")],
          [("Strati e parti", [("crosta", "lo strato più esterno e sottile"), ("mantello", "strato di rocce calde che fluiscono lentamente"), ("nucleo esterno", "ferro e nichel liquidi"),
                               ("nucleo interno", "ferro e nichel solidi"), ("litosfera", "crosta più mantello superiore, rigida"), ("astenosfera", "strato plastico su cui scorrono le placche"),
                               ("ipocentro", "punto interno dove nasce il terremoto"), ("epicentro", "punto in superficie sopra l’ipocentro")],
            "Che cos’è: {k}?", D),
           ("Vulcani italiani", [("Etna", "Sicilia"), ("Vesuvio", "Campania"), ("Stromboli", "isole Eolie"), ("Vulcano", "isole Eolie"), ("Campi Flegrei", "Campania"), ("Marsili", "Mar Tirreno, sotto il mare"),
                                 ("Pantelleria", "Canale di Sicilia"), ("Ischia", "Campania")],
            "Dove si trova questo vulcano: {k}?", None, ("Alpi", "Sardegna centrale")),
           ("Margini e rischi", {"gli effetti di placche che si allontanano": ["dorsali oceaniche", "rift", "nuovo fondo oceanico", "vulcani sottomarini"],
                                 "gli effetti di placche che si scontrano": ["catene montuose", "fosse oceaniche", "subduzione", "Himalaya"],
                                 "i comportamenti corretti durante un terremoto": ["ripararsi sotto un tavolo", "stare lontano dalle finestre", "non usare l’ascensore", "uscire solo a scossa finita", "raggiungere un’area aperta"]})],
          ["La crosta è divisa in placche.", "Il magma che esce si chiama lava.", "L’Etna è in Sicilia.", "La scala Richter misura la magnitudo.", "Il nucleo è fatto di ferro e nichel.",
           "Wegener propose la deriva dei continenti.", "Durante un terremoto non si usa l’ascensore."],
          [("La lava resta sotto terra.", "È il magma che resta sotto terra."), ("Il nucleo è fatto di granito.", "È di ferro e nichel."), ("Il Vesuvio è in Sicilia.", "È in Campania."),
           ("La scala Mercalli misura l’energia.", "Misura gli effetti."), ("Le placche sono ferme.", "Si muovono di pochi centimetri all’anno.")],
          "vulcani e terremoti", "earths-systems"),

        H("AT", "rocce-e-minerali", "Rocce e minerali", "Rocce e minerali",
          "L’alunno distingue minerali e rocce, riconosce rocce magmatiche, sedimentarie e metamorfiche, descrive il ciclo delle rocce e usa la scala di Mohs.",
          "minerali, cristalli, durezza, scala di Mohs, rocce magmatiche intrusive ed effusive, sedimentarie, metamorfiche, ciclo delle rocce, fossili",
          "Magmatiche, sedimentarie, metamorfiche", "Le rocce si trasformano l’una nell’altra nel ciclo delle rocce.",
          ["I minerali sono sostanze naturali con struttura cristallina; le rocce sono miscugli di minerali.", "Le rocce magmatiche nascono dal magma; le sedimentarie da detriti compattati; le metamorfiche da rocce trasformate da calore e pressione.",
           "La scala di Mohs va da 1 (talco) a 10 (diamante)."],
          [("Il marmo di Carrara che tipo di roccia è?", ["Nasce dal calcare.", "Calore e pressione l’hanno trasformato."], "Metamorfica.")],
          [("Rocce e minerali sono la stessa cosa.", "La roccia è un insieme di minerali."), ("I fossili si trovano nel granito.", "Si trovano soprattutto nelle rocce sedimentarie.")],
          [("Perché il granito ha cristalli grandi?", "Il magma si è raffreddato lentamente in profondità."), ("Che cos’è la durezza?", "La resistenza di un minerale a essere graffiato.")],
          [("Tipi di roccia", [("granito", "magmatica intrusiva"), ("basalto", "magmatica effusiva"), ("pomice", "magmatica effusiva"), ("ossidiana", "magmatica effusiva"), ("calcare", "sedimentaria"),
                               ("arenaria", "sedimentaria"), ("argilla", "sedimentaria"), ("marmo", "metamorfica"), ("ardesia", "metamorfica"), ("gneiss", "metamorfica")],
            "Che tipo di roccia è: {k}?", None),
           ("Scala di Mohs", [("talco", "1"), ("gesso", "2"), ("calcite", "3"), ("fluorite", "4"), ("apatite", "5"), ("ortoclasio", "6"), ("quarzo", "7"), ("topazio", "8"), ("corindone", "9"), ("diamante", "10")],
            "Quale durezza ha nella scala di Mohs: {k}?", "Quale minerale ha durezza {v} nella scala di Mohs?"),
           ("Processi", {"i processi che formano rocce sedimentarie": ["erosione", "trasporto", "deposito", "compattazione", "cementazione"],
                         "i processi che formano rocce magmatiche": ["fusione delle rocce", "risalita del magma", "raffreddamento del magma", "eruzione", "cristallizzazione del magma"],
                         "i minerali": ["quarzo", "feldspato", "mica", "calcite", "pirite"]})],
          ["Il granito è una roccia magmatica intrusiva.", "Il marmo è una roccia metamorfica.", "I fossili si trovano nelle rocce sedimentarie.", "Il diamante ha durezza 10.", "Il talco ha durezza 1.",
           "Il basalto è una roccia effusiva.", "Le rocce sono fatte di minerali."],
          [("Il marmo è una roccia sedimentaria.", "È metamorfica."), ("Il talco è il minerale più duro.", "È il più tenero."), ("I fossili sono nel granito.", "Sono nelle rocce sedimentarie."),
           ("Il basalto è intrusivo.", "È effusivo."), ("Il quarzo ha durezza 2.", "Ha durezza 7.")],
          "le rocce", "earths-systems"),

        H("AT", "universo-e-sistema-solare", "L’Universo e il Sistema solare", "Universo e Sistema solare",
          "L’alunno descrive stelle, galassie e l’origine dell’Universo, il Sistema solare e le leggi di Keplero, i moti della Terra e della Luna con le loro conseguenze.",
          "Universo, Big Bang, galassie, Via Lattea, stelle, anno luce, Sole, pianeti, satelliti, Keplero, rotazione, rivoluzione, stagioni, fasi lunari, eclissi, maree",
          "Il Sole è una delle miliardi di stelle", "La Terra ruota in 24 ore e gira intorno al Sole in 365 giorni.",
          ["L’Universo è nato circa 13,8 miliardi di anni fa con il Big Bang; contiene miliardi di galassie. La nostra è la Via Lattea.",
           "Il Sole è una stella media. Intorno girano otto pianeti su orbite ellittiche (Keplero).",
           "La rotazione della Terra dà dì e notte; la rivoluzione con l’asse inclinato dà le stagioni. La Luna mostra le fasi e causa le maree."],
          [("Che cos’è un anno luce?", ["La luce fa 300 000 km al secondo.", "Si misura la strada fatta in un anno."], "La distanza percorsa dalla luce in un anno.")],
          [("L’anno luce è una misura di tempo.", "È una misura di distanza."), ("D’estate la Terra è più vicina al Sole.", "Le stagioni dipendono dall’inclinazione dell’asse.")],
          [("Perché le stelle brillano?", "Nel loro nucleo l’idrogeno si trasforma in elio con la fusione nucleare."), ("Che cosa provoca le maree?", "Soprattutto l’attrazione della Luna sugli oceani.")],
          [("Oggetti celesti", [("stella", "corpo che produce luce con la fusione nucleare"), ("pianeta", "corpo che gira intorno a una stella"), ("satellite", "corpo che gira intorno a un pianeta"),
                                ("galassia", "enorme insieme di stelle, gas e polveri"), ("cometa", "corpo di ghiaccio e polveri con la coda"), ("asteroide", "corpo roccioso minore"),
                                ("meteorite", "frammento che arriva sulla superficie terrestre"), ("nebulosa", "nube di gas e polveri dove nascono le stelle")],
            "Che cos’è: {k}?", D),
           ("Moti e conseguenze", [("rotazione terrestre", "alternarsi di dì e notte"), ("rivoluzione terrestre", "durata dell’anno"), ("asse inclinato", "stagioni"), ("rivoluzione lunare", "fasi della Luna"),
                                   ("Luna tra Sole e Terra", "eclissi di Sole"), ("Terra tra Sole e Luna", "eclissi di Luna"), ("attrazione lunare", "maree")],
            "Quale conseguenza ha: {k}?", "Che cosa causa: {v}?"),
           ("Gruppi", {"i pianeti interni": ["Mercurio", "Venere", "Terra", "Marte"], "i pianeti esterni": ["Giove", "Saturno", "Urano", "Nettuno"],
                       "i corpi minori del Sistema solare": ["asteroidi", "comete", "meteoroidi", "pianeti nani", "fascia di Kuiper"]})],
          ["Il Sole è una stella.", "La Via Lattea è la nostra galassia.", "L’anno luce misura distanze.", "Le orbite dei pianeti sono ellittiche.", "La rotazione della Terra dura circa 24 ore.",
           "La Luna causa le maree.", "Giove è un pianeta esterno."],
          [("L’anno luce misura il tempo.", "Misura le distanze."), ("Il Sole è un pianeta.", "È una stella."), ("Le stagioni dipendono dalla distanza dal Sole.", "Dipendono dall’inclinazione dell’asse."),
           ("Le orbite sono cerchi perfetti.", "Sono ellissi."), ("Marte è un pianeta gassoso.", "È roccioso.")],
          "l’Universo", "earth-and-space"),
    ]
