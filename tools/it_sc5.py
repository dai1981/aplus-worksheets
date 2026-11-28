# -*- coding: utf-8 -*-
"""Italia / Scienze: classe quinta della scuola primaria"""
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"


def f_corpo(R):
    k = R.choice(["battiti", "respiri", "sangue", "ossa", "passi"])
    if k == "battiti":
        b, m = R.choice([(18, 4), (20, 4), (22, 4), (17, 4), (35, 2), (40, 2), (19, 4), (24, 4)])
        return nq("Conti %d battiti del cuore in %d secondi. Quanti battiti al minuto sono?" % (b, 60 // m), b * m, [b + m, b * m // 2, b * 60, b * m + 10], "",
                  "Un minuto ha 60 secondi: %d × %d = %d battiti al minuto." % (b, m, b * m))
    if k == "respiri":
        r, t = R.choice([(16, 5), (18, 10), (14, 3), (20, 2), (15, 4), (12, 6)])
        return nq("Un bambino fa %d respiri al minuto. Quanti respiri fa in %d minuti?" % (r, t), r * t, [r + t, r * t // 2, r * 60, r * (t + 1)], "",
                  "%d × %d = %d respiri." % (r, t, r * t))
    if k == "sangue":
        kg = R.choice([30, 35, 40, 50, 60, 70, 80])
        return nq("Nel corpo c’è circa 1 litro di sangue ogni 13 kg. Quanti litri di sangue ha, più o meno, una persona di %d kg?" % kg, round(kg / 13, 1),
                  [kg / 10, kg * 13 / 100, kg / 13 * 2, kg / 26], "l", "%d : 13 ≈ %s litri." % (kg, num(round(kg / 13, 1))), d=2)
    if k == "ossa":
        return it("Quante ossa ha, più o meno, lo scheletro di un adulto?", "206", ["106", "300", "52"], "Lo scheletro di un adulto ha circa 206 ossa.")
    p, c = R.choice([(1200, 60), (1500, 50), (900, 45), (2000, 50), (1800, 60), (1000, 40)])
    return nq("Camminando fai %d passi lunghi %d cm. Quanti metri percorri?" % (p, c), p * c / 100, [p * c, p * c / 10, p + c, p * c / 1000], "m",
              "%d × %d cm = %d cm = %s m." % (p, c, p * c, num(p * c / 100)))


def f_energia(R):
    k = R.choice(["watt", "kwh", "pannello", "luce"])
    if k == "watt":
        w, h = R.choice([(100, 5), (60, 4), (10, 8), (1000, 2), (2000, 1), (500, 3), (40, 6)])
        return nq("Una lampadina da %d W resta accesa %d ore. Quanta energia consuma in wattora (Wh)?" % (w, h), w * h, [w + h, w * h * 2, w // h if w // h else 3, w * h // 10], "Wh",
                  "Energia = potenza × tempo = %d W × %d h = %d Wh." % (w, h, w * h))
    if k == "kwh":
        w, h = R.choice([(2000, 2), (1000, 3), (1500, 2), (500, 4), (3000, 1), (2500, 2)])
        return nq("Un forno da %d W funziona per %d ore. Quanti kilowattora (kWh) consuma?" % (w, h), w * h / 1000, [w * h, w * h / 100, w / 1000, w * h / 10], "kWh",
                  "%d W × %d h = %d Wh = %s kWh." % (w, h, w * h, num(w * h / 1000)))
    if k == "pannello":
        p, n = R.choice([(300, 4), (250, 6), (400, 5), (350, 3), (200, 8)])
        return nq("Un pannello solare produce %d Wh in un giorno di sole. Quanti Wh producono %d pannelli?" % (p, n), p * n, [p + n, p * n // 2, p * (n - 1), p * n * 10], "Wh",
                  "%d × %d = %d Wh." % (p, n, p * n))
    a, b = R.choice([(60, 8), (100, 12), (40, 6), (75, 10)])
    return nq("Una lampadina vecchia da %d W fa la stessa luce di una lampadina LED da %d W. Quanti watt si risparmiano?" % (a, b), a - b, [a + b, a, b, (a - b) * 2], "W",
              "%d − %d = %d W in meno." % (a, b, a - b))


def f_spazio(R):
    k = R.choice(["luce", "anni", "giorni", "luna"])
    if k == "luce":
        return it("La luce del Sole impiega circa quanto tempo per arrivare sulla Terra?", "8 minuti", ["8 secondi", "8 ore", "8 giorni"],
                  "Il Sole è a circa 150 milioni di km: la luce impiega circa 8 minuti.")
    if k == "anni":
        p, a = R.choice([("Mercurio", "88 giorni"), ("Marte", "circa 2 anni"), ("Giove", "circa 12 anni"), ("Saturno", "circa 29 anni"), ("Venere", "225 giorni")])
        w = [x for x in ["88 giorni", "circa 2 anni", "circa 12 anni", "circa 29 anni", "225 giorni"] if x != a]
        return it("Quanto dura un giro intorno al Sole per %s?" % p, a, R.sample(w, 3), "%s impiega %s per girare intorno al Sole." % (p, a))
    if k == "giorni":
        return it("Quanto impiega la Terra a fare un giro intorno al Sole?", "365 giorni e 6 ore circa", ["24 ore", "28 giorni circa", "12 ore"],
                  "La rivoluzione della Terra dura circa 365 giorni e 6 ore: per questo ogni 4 anni c’è l’anno bisestile.")
    return it("Quanto dura più o meno il ciclo delle fasi della Luna?", "29 giorni e mezzo", ["7 giorni", "365 giorni", "24 ore"], "Dalla luna nuova alla successiva passano circa 29,5 giorni.")


def UNITS(grade):
    return [
        H("U", "la-cellula-e-il-corpo-umano", "La cellula e l’organizzazione del corpo umano", "La cellula e il corpo",
          "L’alunno sa che il corpo è fatto di cellule, che cellule simili formano tessuti, i tessuti organi e gli organi apparati, e conosce lo scheletro e i muscoli.",
          "cellula, nucleo, membrana, tessuti, organi, apparati, sistemi, scheletro, muscoli, articolazioni",
          "Cellule → tessuti → organi → apparati", "Lo scheletro sostiene il corpo e i muscoli lo muovono.",
          ["La cellula è la più piccola parte viva del corpo: ha una membrana, il citoplasma e il nucleo.", "Cellule uguali formano un tessuto; più tessuti formano un organo; più organi lavorano insieme in un apparato.",
           "Lo scheletro, con circa 206 ossa, sostiene e protegge; i muscoli, tirando le ossa, permettono il movimento."],
          [("Il cuore è un tessuto, un organo o un apparato?", ["È fatto di diversi tessuti.", "Lavora con vasi e sangue nell’apparato circolatorio."], "Un organo.")],
          [("Le ossa sono parti morte.", "Le ossa sono vive: crescono e si riparano."), ("I muscoli spingono le ossa.", "I muscoli possono solo tirare, lavorando in coppia.")],
          [("Quante cellule ha il corpo?", "Moltissime: migliaia di miliardi."), ("Che cos’è un’articolazione?", "Il punto in cui due ossa si incontrano e si muovono, come il ginocchio.")],
          [("Dal piccolo al grande", [("globulo rosso", "cellula"), ("neurone", "cellula"), ("cellula della pelle", "cellula"), ("tessuto muscolare", "tessuto"), ("tessuto osseo", "tessuto"),
                                      ("cuore", "organo"), ("stomaco", "organo"), ("polmone", "organo"), ("cervello", "organo"), ("apparato digerente", "apparato"), ("apparato respiratorio", "apparato"),
                                      ("sistema nervoso", "apparato")],
            "Che livello di organizzazione è: {k}?", None, ("organismo",)),
           ("Le ossa", [("cranio", "protegge il cervello"), ("costole", "proteggono cuore e polmoni"), ("colonna vertebrale", "sostiene il corpo e protegge il midollo"), ("femore", "è l’osso più lungo, nella coscia"),
                        ("bacino", "sostiene gli organi della pancia"), ("staffa", "è l’osso più piccolo, nell’orecchio"), ("rotula", "protegge il ginocchio")],
            "A che cosa serve o com’è questo osso: {k}?", D),
           ("Parti", {"le parti della cellula": ["nucleo", "membrana", "citoplasma", "mitocondrio"], "le articolazioni": ["ginocchio", "gomito", "spalla", "anca", "caviglia"],
                      "i muscoli": ["bicipite", "tricipite", "quadricipite", "polpaccio", "diaframma"]})],
          ["Il corpo è fatto di cellule.", "Il cuore è un organo.", "Lo scheletro ha circa 206 ossa.", "Il cranio protegge il cervello.", "I muscoli tirano le ossa.",
           "Il femore è l’osso più lungo.", "Cellule simili formano un tessuto."],
          [("Le ossa sono morte.", "Sono vive e crescono."), ("Il cuore è un apparato.", "È un organo."), ("I muscoli spingono le ossa.", "Possono solo tirare."),
           ("Lo scheletro ha 50 ossa.", "Ne ha circa 206."), ("Le costole proteggono il cervello.", "Proteggono cuore e polmoni.")],
          "il corpo umano", "living-things-and-ecosystems", calc=f_corpo),

        H("U", "apparato-digerente-e-respiratorio", "Apparato digerente e respiratorio", "Digestione e respirazione",
          "L’alunno descrive il viaggio del cibo nell’apparato digerente, il ruolo dei nutrienti per una dieta equilibrata e il percorso dell’aria nell’apparato respiratorio.",
          "bocca, esofago, stomaco, intestino, fegato, nutrienti, piramide alimentare, trachea, bronchi, polmoni, alveoli",
          "Il cibo si digerisce, l’aria si respira", "Nei polmoni l’ossigeno passa nel sangue; nell’intestino passano i nutrienti.",
          ["Il cibo passa da bocca, esofago, stomaco, intestino tenue e crasso: qui viene sminuzzato e trasformato.", "Nell’intestino tenue i nutrienti passano nel sangue.",
           "L’aria entra dal naso, scende per trachea e bronchi fino agli alveoli dei polmoni, dove l’ossigeno passa nel sangue."],
          [("Dove passano i nutrienti nel sangue?", ["Lo stomaco rimescola il cibo.", "L’intestino tenue ha i villi che assorbono."], "Nell’intestino tenue.")],
          [("La digestione avviene solo nello stomaco.", "Comincia in bocca e finisce nell’intestino."), ("Espiriamo solo ossigeno.", "Espiriamo più anidride carbonica e vapore.")],
          [("Perché bisogna masticare bene?", "Perché i pezzi piccoli si digeriscono meglio e la saliva inizia il lavoro."), ("Che cosa fa il diaframma?", "È il muscolo che, abbassandosi, fa entrare l’aria nei polmoni.")],
          [("Gli organi", [("bocca", "mastica e inizia la digestione con la saliva"), ("esofago", "porta il cibo allo stomaco"), ("stomaco", "rimescola il cibo con i succhi gastrici"),
                           ("intestino tenue", "assorbe i nutrienti"), ("intestino crasso", "assorbe l’acqua e forma le feci"), ("fegato", "produce la bile"),
                           ("trachea", "porta l’aria ai bronchi"), ("alveoli", "scambiano ossigeno e anidride carbonica"), ("diaframma", "fa entrare e uscire l’aria")],
            "Che cosa fa: {k}?", D),
           ("Nutrienti", [("pasta", "carboidrati"), ("pane", "carboidrati"), ("riso", "carboidrati"), ("carne", "proteine"), ("legumi", "proteine"), ("uova", "proteine"),
                          ("olio d’oliva", "grassi"), ("burro", "grassi"), ("arance", "vitamine"), ("verdura", "fibre"), ("latte", "calcio")],
            "Quale nutriente è più presente in questo cibo: {k}?", None),
           ("Apparato", {"gli organi dell’apparato digerente": ["esofago", "stomaco", "intestino", "fegato", "pancreas"], "gli organi dell’apparato respiratorio": ["trachea", "bronchi", "polmoni", "laringe", "alveoli"],
                         "le buone abitudini a tavola": ["masticare bene", "mangiare frutta e verdura", "bere acqua", "fare colazione", "limitare i dolci"]})],
          ["La digestione comincia in bocca.", "Nell’intestino tenue si assorbono i nutrienti.", "L’ossigeno passa nel sangue negli alveoli.", "Il fegato produce la bile.",
           "La pasta contiene carboidrati.", "Il diaframma aiuta a respirare.", "I legumi contengono proteine."],
          [("La digestione comincia nello stomaco.", "Comincia in bocca."), ("L’esofago assorbe i nutrienti.", "Lo fa l’intestino tenue."), ("Espiriamo solo ossigeno.", "Espiriamo anidride carbonica."),
           ("L’olio contiene soprattutto proteine.", "Contiene grassi."), ("La trachea porta il cibo allo stomaco.", "Porta l’aria ai bronchi.")],
          "digestione e respirazione", "living-things-and-ecosystems"),

        H("U", "circolazione-ed-escrezione", "Apparato circolatorio ed escretore", "Circolazione ed escrezione",
          "L’alunno descrive il cuore, i vasi sanguigni e le parti del sangue, e spiega come reni e pelle eliminano le sostanze di scarto.",
          "cuore, arterie, vene, capillari, globuli rossi e bianchi, piastrine, plasma, reni, urina, sudore",
          "Il cuore pompa il sangue in tutto il corpo", "Le arterie partono dal cuore, le vene ci tornano. I reni puliscono il sangue.",
          ["Il cuore è un muscolo che pompa il sangue: le arterie lo portano dal cuore al corpo, le vene lo riportano al cuore.",
           "Il sangue porta ossigeno e nutrienti e raccoglie gli scarti. È fatto di plasma, globuli rossi, globuli bianchi e piastrine.",
           "I reni filtrano il sangue e producono l’urina; anche la pelle elimina scarti con il sudore."],
          [("Che cosa fanno i globuli bianchi?", ["Ci sono germi in una ferita.", "I globuli bianchi li attaccano."], "Difendono il corpo dai germi.")],
          [("Le vene portano sempre sangue senza ossigeno.", "Le vene polmonari portano sangue ricco di ossigeno al cuore."), ("Il cuore è a sinistra del petto.", "È al centro, un po’ spostato a sinistra.")],
          [("Perché dopo una corsa il cuore batte più forte?", "I muscoli hanno bisogno di più ossigeno."), ("Quanta urina si produce in un giorno?", "Circa un litro e mezzo per un adulto.")],
          [("Il sangue", [("globuli rossi", "trasportano l’ossigeno"), ("globuli bianchi", "difendono dai germi"), ("piastrine", "fermano le emorragie"), ("plasma", "è la parte liquida del sangue"),
                          ("arterie", "portano il sangue dal cuore al corpo"), ("vene", "riportano il sangue al cuore"), ("capillari", "sono i vasi più sottili"), ("emoglobina", "lega l’ossigeno nei globuli rossi")],
            "Che cosa fa: {k}?", D),
           ("Gli scarti", [("reni", "filtrano il sangue"), ("vescica", "raccoglie l’urina"), ("ureteri", "portano l’urina alla vescica"), ("pelle", "elimina acqua e sali con il sudore"),
                           ("polmoni", "eliminano l’anidride carbonica"), ("intestino crasso", "elimina i resti del cibo"), ("uretra", "porta fuori l’urina")],
            "Come aiuta a eliminare gli scarti: {k}?", "Quale organo {v}?"),
           ("Sangue con o senza ossigeno", {"i vasi con sangue ricco di ossigeno": ["aorta", "vene polmonari", "arterie del braccio", "arterie della gamba", "arteria carotide", "arterie coronarie", "arteria renale"],
                                            "i vasi con sangue povero di ossigeno": ["arterie polmonari", "vena cava", "vene del braccio", "vene della gamba", "vena giugulare", "vena renale", "vena porta"]})],
          ["Il cuore è un muscolo.", "Le arterie partono dal cuore.", "I globuli rossi trasportano l’ossigeno.", "I reni filtrano il sangue.", "Le piastrine fermano il sangue.",
           "Il sudore elimina acqua e sali.", "I capillari sono i vasi più sottili."],
          [("Le vene partono dal cuore.", "Le arterie partono dal cuore."), ("I globuli bianchi trasportano ossigeno.", "Difendono dai germi."), ("I reni producono la bile.", "Producono l’urina."),
           ("Il cuore è un osso.", "Il cuore è un muscolo."), ("Il plasma è solido.", "È la parte liquida del sangue.")],
          "circolazione ed escrezione", "living-things-and-ecosystems"),

        H("U", "sistema-nervoso-e-sensi", "Il sistema nervoso e gli organi di senso", "Sistema nervoso e sensi",
          "L’alunno descrive cervello, midollo spinale e nervi, distingue movimenti volontari e riflessi e spiega come funzionano occhio e orecchio.",
          "neurone, cervello, cervelletto, midollo spinale, nervi, riflessi, occhio, retina, pupilla, orecchio, timpano",
          "Il cervello comanda, i nervi trasmettono", "I sensi raccolgono informazioni e i nervi le portano al cervello.",
          ["Il sistema nervoso è fatto di neuroni. Il cervello e il midollo spinale formano il sistema nervoso centrale.", "I nervi portano i messaggi dai sensi al cervello e dal cervello ai muscoli.",
           "Il riflesso è una risposta rapida e automatica: togli la mano dal fuoco prima di pensarci."],
          [("Togliere la mano da una pentola che scotta è volontario?", ["È rapidissimo.", "Lo comanda il midollo spinale."], "No, è un riflesso.")],
          [("Vediamo con la pupilla.", "La pupilla fa entrare la luce; l’immagine si forma sulla retina."), ("Il cervelletto pensa.", "Il cervelletto coordina movimenti ed equilibrio.")],
          [("Perché la pupilla si stringe al sole?", "Per far entrare meno luce e proteggere l’occhio."), ("Come sentiamo un suono?", "Il suono fa vibrare il timpano e i nervi portano il messaggio al cervello.")],
          [("Le parti", [("cervello", "pensa, ricorda e comanda"), ("cervelletto", "coordina l’equilibrio"), ("midollo spinale", "comanda i riflessi"), ("nervi", "trasmettono i messaggi"),
                         ("neurone", "è la cellula nervosa"), ("retina", "riceve l’immagine nell’occhio"), ("pupilla", "fa entrare la luce"), ("timpano", "vibra con i suoni"),
                         ("cristallino", "mette a fuoco le immagini")],
            "Che cosa fa: {k}?", D),
           ("Volontario o riflesso?", [("scrivere una lettera", "volontario"), ("calciare un pallone", "volontario"), ("alzare la mano per parlare", "volontario"), ("salire le scale", "volontario"),
                                       ("chiudere gli occhi se arriva qualcosa", "riflesso"), ("starnutire", "riflesso"), ("togliere la mano dal fuoco", "riflesso"), ("la gamba che scatta dal martelletto", "riflesso"),
                                       ("la pupilla che si stringe alla luce", "riflesso"), ("disegnare", "volontario")],
            "Questo movimento è volontario o un riflesso: {k}?", None, ("involontario del cuore", "un sogno")),
           ("Organi di senso", {"le parti dell’occhio": ["iride", "pupilla", "cristallino", "retina", "cornea"], "le parti dell’orecchio": ["padiglione", "timpano", "martello", "staffa", "coclea"],
                                "le parti del sistema nervoso centrale": ["cervello", "cervelletto", "midollo spinale", "tronco encefalico"]})],
          ["Il cervello comanda il corpo.", "I nervi trasmettono i messaggi.", "Starnutire è un riflesso.", "La retina riceve l’immagine.", "Il timpano vibra con i suoni.",
           "Il cervelletto controlla l’equilibrio.", "Il neurone è una cellula nervosa."],
          [("Starnutire è un movimento volontario.", "È un riflesso."), ("Il cervelletto controlla la vista.", "Controlla l’equilibrio."), ("I nervi trasportano il sangue.", "Trasmettono i messaggi."),
           ("L’immagine si forma sulla pupilla.", "Si forma sulla retina."), ("Il timpano è nell’occhio.", "È nell’orecchio.")],
          "il sistema nervoso", "living-things-and-ecosystems"),

        H("O", "l-energia", "L’energia e le sue fonti", "L’energia",
          "L’alunno riconosce le forme dell’energia e le sue trasformazioni, distingue fonti rinnovabili e non rinnovabili e propone comportamenti per risparmiarla.",
          "energia, forme, trasformazioni, fonti rinnovabili, non rinnovabili, solare, eolica, idroelettrica, fossili, risparmio",
          "L’energia non si crea: si trasforma", "Sole, vento e acqua sono fonti rinnovabili; petrolio e carbone no.",
          ["L’energia permette di fare un lavoro: muovere, scaldare, illuminare.", "L’energia cambia forma: il ferro da stiro trasforma energia elettrica in calore.",
           "Le fonti rinnovabili (Sole, vento, acqua) non finiscono; quelle non rinnovabili (petrolio, carbone, gas) finiscono e inquinano."],
          [("Che trasformazione fa una lampadina?", ["Riceve energia elettrica.", "Dà luce e un po’ di calore."], "Da elettrica a luminosa (e termica).")],
          [("Il petrolio è rinnovabile.", "Si è formato in milioni di anni: non è rinnovabile."), ("L’energia sparisce quando la usiamo.", "Si trasforma in altre forme, spesso calore.")],
          [("Che cos’è un kilowattora?", "L’energia usata da un apparecchio da 1000 W acceso per un’ora."), ("Perché l’energia solare è pulita?", "Perché non produce fumo e non finisce.")],
          [("Le fonti", [("Sole", "rinnovabile"), ("vento", "rinnovabile"), ("acqua dei fiumi", "rinnovabile"), ("calore della Terra", "rinnovabile"), ("biomasse", "rinnovabile"),
                         ("petrolio", "non rinnovabile"), ("carbone", "non rinnovabile"), ("gas naturale", "non rinnovabile"), ("uranio", "non rinnovabile")],
            "Questa fonte è rinnovabile o no: {k}?", None, ("magnetica", "trasparente")),
           ("Trasformazioni", [("lampadina", "da elettrica a luminosa"), ("frullatore", "da elettrica a movimento"), ("pannello solare", "da luminosa a elettrica"), ("pala eolica", "da movimento a elettrica"),
                               ("stufa a legna", "da chimica a termica"), ("pila della torcia", "da chimica a elettrica"), ("altoparlante", "da elettrica a sonora"), ("corpo che corre", "da chimica a movimento")],
            "Quale trasformazione fa: {k}?", "Che cosa trasforma l’energia {v}?"),
           ("Risparmiare", {"le abitudini che fanno risparmiare energia": ["spegnere le luci", "usare lampadine LED", "chiudere le finestre col riscaldamento", "usare la bicicletta", "staccare i caricatori"],
                            "gli sprechi di energia": ["lasciare la TV in standby", "frigorifero aperto a lungo", "luci accese di giorno", "finestre aperte col riscaldamento", "auto per 300 metri"],
                            "le centrali rinnovabili": ["centrale idroelettrica", "parco eolico", "impianto fotovoltaico", "centrale geotermica", "centrale a biomasse"]})],
          ["Il Sole è una fonte rinnovabile.", "Il petrolio non è rinnovabile.", "La pala eolica produce energia elettrica.", "L’energia si trasforma.", "Le lampadine LED consumano meno.",
           "Il carbone inquina l’aria.", "Il pannello solare usa la luce."],
          [("Il carbone è rinnovabile.", "Non è rinnovabile."), ("L’energia si distrugge.", "Si trasforma."), ("Il pannello solare usa il vento.", "Usa la luce del Sole."),
           ("La TV in standby non consuma.", "Consuma un po’ di energia."), ("Il gas naturale non finisce mai.", "Prima o poi finisce.")],
          "l’energia", "energy", calc=f_energia),

        H("O", "luce-e-suono", "La luce e il suono", "Luce e suono",
          "L’alunno osserva come la luce si propaga in linea retta, si riflette e si rifrange, forma le ombre e i colori, e come il suono nasce da vibrazioni e si propaga nei materiali.",
          "luce, ombra, riflessione, rifrazione, colori, prisma, corpi trasparenti e opachi, suono, vibrazioni, eco, altezza, intensità",
          "La luce va dritta, il suono è una vibrazione", "Il suono ha bisogno di un materiale; nel vuoto non si propaga.",
          ["La luce viaggia in linea retta: quando incontra un corpo opaco si forma l’ombra.", "Lo specchio riflette la luce; l’acqua la piega (rifrazione). Il prisma divide la luce bianca nei colori.",
           "Il suono nasce da una vibrazione e viaggia nell’aria, nell’acqua e nei solidi, ma non nel vuoto."],
          [("Perché vediamo prima il lampo e poi il tuono?", ["La luce è velocissima.", "Il suono è molto più lento."], "Perché la luce viaggia più veloce del suono.")],
          [("Il suono viaggia nello spazio vuoto.", "Nel vuoto non c’è materia che vibri."), ("La luce bianca è un solo colore.", "È fatta di tutti i colori dell’arcobaleno.")],
          [("Che cos’è l’eco?", "Il suono che rimbalza su una parete e torna indietro."), ("Perché la cannuccia nel bicchiere sembra spezzata?", "Per la rifrazione: la luce cambia direzione passando dall’acqua all’aria.")],
          [("Trasparente, traslucido, opaco", [("vetro della finestra", "trasparente"), ("acqua limpida", "trasparente"), ("aria", "trasparente"), ("carta oleata", "traslucido"),
                                               ("vetro smerigliato", "traslucido"), ("tenda leggera", "traslucido"), ("legno", "opaco"), ("muro", "opaco"), ("cartone", "opaco"), ("metallo", "opaco")],
            "Come si comporta con la luce: {k}?", None, ("luminoso", "elastico")),
           ("Fenomeni", [("ombra", "un corpo opaco ferma la luce"), ("riflessione", "la luce rimbalza su uno specchio"), ("rifrazione", "la luce si piega passando nell’acqua"),
                         ("arcobaleno", "la luce del Sole si divide nelle gocce di pioggia"), ("eco", "il suono rimbalza su una parete"), ("suono acuto", "la vibrazione è veloce"),
                         ("suono grave", "la vibrazione è lenta"), ("suono forte", "la vibrazione è ampia")],
            "Che cos’è: {k}?", D),
           ("Sorgenti", {"le sorgenti di luce": ["Sole", "lampadina accesa", "candela accesa", "fiamma del fornello", "lucciola"],
                         "i corpi che riflettono la luce": ["Luna", "specchio", "pianeta Venere", "neve", "cucchiaio lucido"],
                         "le sorgenti di suono": ["corda di chitarra", "tamburo", "corde vocali", "campanello", "diapason"]})],
          ["La luce viaggia in linea retta.", "Il suono nasce da una vibrazione.", "Il suono non viaggia nel vuoto.", "La luce è più veloce del suono.", "Lo specchio riflette la luce.",
           "La Luna riflette la luce del Sole.", "La luce bianca contiene tutti i colori."],
          [("La Luna produce luce.", "Riflette la luce del Sole."), ("Il suono viaggia nel vuoto.", "Ha bisogno di un materiale."), ("Il suono è più veloce della luce.", "La luce è molto più veloce."),
           ("Il legno è trasparente.", "Il legno è opaco."), ("La luce viaggia a zigzag.", "Viaggia in linea retta.")],
          "la luce e il suono", "waves-and-light"),

        H("S", "il-sistema-solare", "Il Sistema solare, la Terra e la Luna", "Il Sistema solare",
          "L’alunno descrive il Sole e gli otto pianeti, i movimenti della Terra (rotazione e rivoluzione) e le fasi della Luna.",
          "Sole, pianeti, satelliti, rotazione, rivoluzione, dì e notte, stagioni, fasi lunari, eclissi",
          "La Terra gira su sé stessa e intorno al Sole", "La rotazione dà il dì e la notte; la rivoluzione dura un anno.",
          ["Il Sole è una stella. Intorno girano otto pianeti: Mercurio, Venere, Terra, Marte, Giove, Saturno, Urano e Nettuno.",
           "La Terra ruota su sé stessa in 24 ore (dì e notte) e gira intorno al Sole in un anno (rivoluzione).",
           "Le stagioni dipendono dall’inclinazione dell’asse terrestre. La Luna gira intorno alla Terra e mostra le fasi."],
          [("Perché d’estate le giornate sono lunghe?", ["L’asse della Terra è inclinato.", "Il nostro emisfero è rivolto verso il Sole."], "Per l’inclinazione dell’asse terrestre.")],
          [("D’estate la Terra è più vicina al Sole.", "Le stagioni dipendono dall’inclinazione dell’asse, non dalla distanza."), ("La Luna fa luce propria.", "Riflette la luce del Sole.")],
          [("Perché vediamo le fasi della Luna?", "Perché, girando intorno alla Terra, ci mostra ogni giorno una parte diversa illuminata dal Sole."),
           ("Plutone è un pianeta?", "Dal 2006 è considerato un pianeta nano.")],
          [("I pianeti", [("Mercurio", "il più vicino al Sole"), ("Venere", "il più caldo"), ("Terra", "l’unico con acqua liquida e vita conosciuta"), ("Marte", "il pianeta rosso"),
                          ("Giove", "il più grande"), ("Saturno", "ha anelli molto visibili"), ("Urano", "ruota quasi sdraiato"), ("Nettuno", "il più lontano dal Sole")],
            "Quale caratteristica ha: {k}?", "Quale pianeta è {v}?"),
           ("Movimenti", [("rotazione", "il dì e la notte"), ("rivoluzione", "l’anno"), ("inclinazione dell’asse", "le stagioni"), ("Luna intorno alla Terra", "le fasi lunari"),
                          ("Luna tra Sole e Terra", "l’eclissi di Sole"), ("Terra tra Sole e Luna", "l’eclissi di Luna"), ("attrazione della Luna", "le maree")],
            "Che cosa provoca: {k}?", "Che cosa causa {v}?"),
           ("Tipi", {"i pianeti rocciosi": ["Mercurio", "Venere", "Terra", "Marte"], "i pianeti gassosi": ["Giove", "Saturno", "Urano", "Nettuno"],
                     "le fasi della Luna": ["luna nuova", "primo quarto", "luna piena", "ultimo quarto", "luna crescente"]})],
          ["Il Sole è una stella.", "I pianeti sono otto.", "Giove è il pianeta più grande.", "La rotazione della Terra dura 24 ore.", "La Luna riflette la luce del Sole.",
           "Marte è chiamato pianeta rosso.", "Le stagioni dipendono dall’inclinazione dell’asse."],
          [("Il Sole è un pianeta.", "È una stella."), ("I pianeti sono nove.", "Sono otto."), ("La rotazione dura un anno.", "Dura 24 ore."),
           ("D’estate siamo più vicini al Sole.", "Le stagioni dipendono dall’asse inclinato."), ("Mercurio è il pianeta più lontano.", "È il più vicino al Sole.")],
          "il Sistema solare", "earth-and-space"),
    ]
