# -*- coding: utf-8 -*-
"""France / Physique-chimie et SVT : 4e（cycle 4）"""
from fr_sci import H, nq, num


def f_rho(R):
    k = R.choice(["rho", "rho", "m", "V", "gL"])
    if k == "rho":
        m, V = R.choice([(540, 200), (158, 20), (45, 50), (386, 20), (250, 250), (113, 10), (92, 100), (27, 10)])
        return nq("Un objet a une masse de %s g et un volume de %s cm³. Quelle est sa masse volumique ?" % (num(m), num(V)), m / V,
                  [V / m, m * V, m - V], "g/cm³", "ρ = m : V = %s : %s = %s g/cm³." % (num(m), num(V), num(m / V)))
    if k == "m":
        r, V = R.choice([(2.7, 30), (7.9, 15), (1, 350), (0.8, 250), (19.3, 2), (11.3, 10)])
        return nq("Un objet a une masse volumique de %s g/cm³ et un volume de %s cm³. Quelle est sa masse ?" % (num(r), num(V)), r * V, [V / r, r / V, r + V], "g",
                  "m = ρ × V = %s × %s = %s g." % (num(r), num(V), num(r * V)))
    if k == "V":
        r, m = R.choice([(2.7, 81), (7.9, 79), (1, 120), (0.8, 40), (19.3, 193), (8.9, 89)])
        return nq("Quel volume occupe un objet de %s g dont la masse volumique est %s g/cm³ ?" % (num(m), num(r)), m / r, [m * r, r / m, m - r], "cm³",
                  "V = m : ρ = %s : %s = %s cm³." % (num(m), num(r), num(m / r)))
    m, V = R.choice([(1.5, 1.25), (3, 2.5), (0.6, 0.5), (12, 10), (2.4, 2)])
    return nq("%s L d’un liquide pèsent %s kg. Quelle est sa masse volumique en kg/L ?" % (num(V), num(m)), m / V, [V / m, m * V, m - V], "kg/L", "ρ = %s : %s = %s kg/L." % (num(m), num(V), num(m / V)))


def f_ohm(R):
    k = R.choice(["U", "U", "I", "R", "serie", "deriv"])
    if k == "U":
        Rr, I = R.choice([(100, 0.05), (220, 0.02), (47, 0.1), (1000, 0.006), (330, 0.03), (10, 0.45), (68, 0.1)])
        return nq("Une résistance de %s Ω est traversée par un courant de %s A. Quelle est la tension à ses bornes ?" % (num(Rr), num(I)), Rr * I, [Rr / I, I / Rr, Rr + I], "V",
                  "U = R × I = %s × %s = %s V." % (num(Rr), num(I), num(Rr * I)))
    if k == "I":
        U, Rr = R.choice([(6, 100), (12, 240), (4.5, 150), (9, 300), (3, 60), (5, 1000)])
        return nq("Une résistance de %s Ω est soumise à %s V. Quelle intensité la traverse ?" % (num(Rr), num(U)), U / Rr, [U * Rr, Rr / U, U - Rr / 100], "A",
                  "I = U : R = %s : %s = %s A." % (num(U), num(Rr), num(U / Rr)))
    if k == "R":
        U, I = R.choice([(6, 0.03), (12, 0.1), (4.5, 0.15), (9, 0.045), (3, 0.01), (10, 0.5)])
        return nq("Sous une tension de %s V, un conducteur ohmique est traversé par %s A. Quelle est sa résistance ?" % (num(U), num(I)), U / I, [U * I, I / U, U + I], "Ω",
                  "R = U : I = %s : %s = %s Ω." % (num(U), num(I), num(U / I)))
    if k == "serie":
        U, u1 = R.choice([(12, 5), (9, 4.5), (6, 2.5), (4.5, 1.5), (230, 80)])
        return nq("Deux lampes sont en série sur un générateur de %s V. La tension aux bornes de la première est %s V. Quelle est celle de la seconde ?" % (num(U), num(u1)), U - u1,
                  [U + u1, U, u1], "V", "Loi d’additivité des tensions en série : %s − %s = %s V." % (num(U), num(u1), num(U - u1)))
    I, i1 = R.choice([(0.5, 0.2), (1.2, 0.7), (0.3, 0.1), (2, 1.5), (0.8, 0.35)])
    return nq("Dans un circuit en dérivation, la branche principale est parcourue par %s A et une branche par %s A. Quelle est l’intensité dans l’autre branche ?" % (num(I), num(i1)), round(I - i1, 3),
              [I + i1, I, i1], "A", "Loi des nœuds : %s − %s = %s A." % (num(I), num(i1), num(round(I - i1, 3))))


def f_son(R):
    k = R.choice(["d", "d", "echo", "t", "f", "orage"])
    if k == "d":
        t = R.choice([2, 3, 5, 0.5, 1.5, 4])
        return nq("Le son se propage dans l’air à 340 m/s. Quelle distance parcourt-il en %s s ?" % num(t), 340 * t, [340 / t, 340 + t, 3.4 * t], "m", "d = v × t = 340 × %s = %s m." % (num(t), num(340 * t)))
    if k == "echo":
        t = R.choice([2, 1, 4, 0.6, 3, 1.2])
        return nq("Tu cries face à une falaise et tu entends l’écho %s s plus tard (son à 340 m/s). À quelle distance est la falaise ?" % num(t), 340 * t / 2,
                  [340 * t, 340 / t, 340 * t * 2], "m", "Le son fait l’aller et le retour : 340 × %s : 2 = %s m." % (num(t), num(340 * t / 2)))
    if k == "t":
        d = R.choice([680, 1700, 170, 3400, 510])
        return nq("Combien de temps met le son pour parcourir %s m dans l’air (340 m/s) ?" % num(d), d / 340, [d * 340, 340 / d, d / 34], "s", "t = d : v = %s : 340 = %s s." % (num(d), num(d / 340)))
    if k == "f":
        n, t = R.choice([(440, 1), (100, 0.5), (50, 0.1), (1000, 2), (20, 0.1), (300, 0.5)])
        return nq("Une membrane fait %s vibrations en %s s. Quelle est la fréquence du son ?" % (num(n), num(t)), n / t, [n * t, t / n, n], "Hz", "f = %s : %s = %s Hz." % (num(n), num(t), num(n / t)))
    t = R.choice([3, 6, 9, 1.5, 12])
    return nq("Pendant un orage, on entend le tonnerre %s s après l’éclair (son à 340 m/s). À quelle distance environ est l’orage ?" % num(t), 340 * t,
              [340 * t / 2, 340 / t, 34 * t], "m", "La lumière arrive presque instantanément : d = 340 × %s = %s m." % (num(t), num(340 * t)))


def UNITS(grade):
    return [
        H("P", "atomes-molecules-et-transformations-chimiques", "Atomes, molécules et transformations chimiques", "Transformations chimiques",
          "Les élèves interprètent une transformation chimique comme un réarrangement d’atomes, écrivent et équilibrent une équation de réaction simple et étudient les combustions.",
          "atome, molécule, formule chimique, réactif, produit, équation de réaction, conservation des atomes et de la masse, combustion du carbone et du méthane",
          "Les atomes se réarrangent, ils ne disparaissent pas", "Au cours d’une transformation chimique, la masse totale se conserve.",
          ["Une molécule est un assemblage d’atomes. Sa formule indique le nombre de chaque atome : H₂O contient 2 atomes d’hydrogène et 1 atome d’oxygène.",
           "Lors d’une transformation chimique, les réactifs disparaissent et des produits apparaissent. Les atomes se réarrangent : on retrouve les mêmes atomes, en même nombre. La masse se conserve.",
           "Combustion du carbone : C + O₂ → CO₂. Combustion du méthane : CH₄ + 2 O₂ → CO₂ + 2 H₂O. Le dioxyde de carbone trouble l’eau de chaux."],
          [("Équilibre : H₂ + O₂ → H₂O.", ["À droite, il y a 1 atome d’oxygène, à gauche 2.", "On met 2 devant H₂O, puis 2 devant H₂."], "2 H₂ + O₂ → 2 H₂O")],
          [("Dans CO₂, il y a 2 atomes de carbone.", "Le 2 en indice porte sur l’oxygène : 1 C et 2 O."), ("Pendant une combustion, la matière disparaît.", "Elle devient des gaz : la masse totale se conserve.")],
          [("Pourquoi une combustion incomplète est-elle dangereuse ?", "Elle produit du monoxyde de carbone (CO), un gaz toxique et inodore."), ("Comment identifier l’eau formée ?", "Le sulfate de cuivre anhydre blanc devient bleu.")],
          [("Formules", [("l’eau", "H₂O"), ("le dioxyde de carbone", "CO₂"), ("le dioxygène", "O₂"), ("le diazote", "N₂"), ("le méthane", "CH₄"), ("le monoxyde de carbone", "CO"), ("le dihydrogène", "H₂"), ("le glucose", "C₆H₁₂O₆")],
            "Quelle est la formule de {k} ?", "Quelle molécule a pour formule {v} ?"),
           ("Compter les atomes", [("H₂O", "3 atomes"), ("CO₂", "3 atomes"), ("CH₄", "5 atomes"), ("O₂", "2 atomes"), ("C₆H₁₂O₆", "24 atomes"), ("NH₃", "4 atomes"), ("C₂H₆O", "9 atomes"), ("C₃H₈", "11 atomes")],
            "Combien d’atomes contient une molécule {k} ?", None, ("1 atome", "6 atomes", "12 atomes")),
           ("Tests chimiques", [("l’eau de chaux se trouble", "dioxyde de carbone"), ("le sulfate de cuivre anhydre bleuit", "eau"), ("une bûchette incandescente se rallume", "dioxygène"),
                                ("une petite détonation près d’une flamme", "dihydrogène"), ("le papier pH devient rouge", "solution acide"), ("l’eau iodée bleuit", "amidon")],
            "Que met en évidence le test : {k} ?", "Quel test met en évidence {v} ?")],
          ["La masse se conserve lors d’une transformation chimique.", "Les atomes se réarrangent.", "H₂O contient trois atomes.", "L’eau de chaux se trouble avec le CO₂.",
           "Le méthane a pour formule CH₄.", "Une combustion incomplète produit du monoxyde de carbone.", "Le dioxygène rallume une bûchette incandescente."],
          [("Les atomes disparaissent pendant la réaction.", "Ils se réarrangent."), ("La masse diminue pendant une combustion.", "Elle se conserve."), ("CO₂ contient deux atomes de carbone.", "Un C et deux O."),
           ("L’eau de chaux se trouble avec le dioxygène.", "Avec le CO₂."), ("Le monoxyde de carbone est sans danger.", "Il est toxique.")],
          "les transformations chimiques", "matter"),

        H("P", "masse-volumique", "La masse volumique", "Masse volumique",
          "Les élèves définissent et calculent la masse volumique d’un matériau, l’utilisent pour identifier une substance et prévoir si un objet flotte.",
          "masse, volume, masse volumique ρ = m : V, g/cm³, kg/L, kg/m³, identification d’un matériau, flottaison",
          "ρ = m : V", "Un objet flotte si sa masse volumique est plus petite que celle du liquide.",
          ["La masse volumique ρ (rho) d’un matériau est la masse d’un volume unité : ρ = m : V. Elle s’exprime en g/cm³, kg/L ou kg/m³.",
           "L’eau a une masse volumique de 1 g/cm³ = 1 kg/L = 1 000 kg/m³. Celle de l’aluminium est 2,7 g/cm³, celle du fer 7,9 g/cm³.",
           "Un objet plein flotte sur un liquide si sa masse volumique est inférieure à celle du liquide."],
          [("Une bague de 9,65 g a un volume de 0,5 cm³. En quoi est-elle ?", ["ρ = 9,65 : 0,5 = 19,3 g/cm³.", "L’or a une masse volumique de 19,3 g/cm³."], "En or.")],
          [("La masse volumique change avec la taille de l’objet.", "Elle dépend du matériau, pas de la taille."), ("On calcule V : m.", "ρ = m : V.")],
          [("Pourquoi l’huile flotte-t-elle sur l’eau ?", "Sa masse volumique (environ 0,9 g/cm³) est plus petite que celle de l’eau."), ("Comment mesurer le volume d’un caillou ?", "Par déplacement d’eau dans une éprouvette graduée.")],
          [("Masses volumiques", [("l’eau", "1 g/cm³"), ("l’aluminium", "2,7 g/cm³"), ("le fer", "7,9 g/cm³"), ("l’or", "19,3 g/cm³"), ("le plomb", "11,3 g/cm³"), ("le cuivre", "8,9 g/cm³"),
                                  ("l’éthanol", "0,79 g/cm³"), ("le liège", "0,24 g/cm³"), ("l’air", "1,2 g/L")],
            "Quelle est la masse volumique de {k} ?", "Quel matériau a une masse volumique de {v} ?"),
           ("Flotte ou coule ?", {"des objets qui flottent sur l’eau": ["un bouchon en liège", "un glaçon", "une bille de polystyrène", "une goutte d’huile", "un morceau de bois de pin", "une balle de ping-pong"],
                                  "des objets qui coulent dans l’eau": ["une bille en verre", "un clou en fer", "une pièce en cuivre", "un plomb de pêche", "une bague en or", "une canette pleine en aluminium"]}),
           ("Unités", [("1 g/cm³", "1 kg/L"), ("1 kg/L", "1 000 kg/m³"), ("1 L", "1 000 cm³"), ("1 mL", "1 cm³"), ("1 m³", "1 000 L"), ("1 kg", "1 000 g")],
            "À quoi est égal {k} ?", "Qu’est-ce qui est égal à {v} ?")],
          ["ρ = m : V.", "La masse volumique de l’eau est 1 g/cm³.", "La masse volumique dépend du matériau.", "Un objet moins dense que l’eau flotte.",
           "1 g/cm³ = 1 kg/L.", "L’or est plus dense que le fer.", "Le liège flotte sur l’eau."],
          [("La masse volumique dépend de la taille.", "Elle dépend du matériau."), ("ρ = V : m.", "ρ = m : V."), ("Le fer flotte sur l’eau.", "Il coule."), ("1 g/cm³ = 1 000 kg/L.", "1 g/cm³ = 1 kg/L."),
           ("L’huile est plus dense que l’eau.", "Elle est moins dense.")],
          "la masse volumique", "matter", calc=f_rho),

        H("P", "tension-intensite-et-loi-d-ohm", "Tension, intensité et loi d’Ohm", "Loi d’Ohm",
          "Les élèves mesurent tensions et intensités, appliquent les lois des circuits en série et en dérivation et la loi d’Ohm.",
          "intensité (A), tension (V), ampèremètre, voltmètre, loi d’unicité, loi d’additivité, loi des nœuds, résistance (Ω), loi d’Ohm U = R × I",
          "U = R × I", "En série, les tensions s’additionnent. En dérivation, les intensités s’additionnent.",
          ["L’intensité I (en ampères, A) se mesure avec un ampèremètre branché en série. La tension U (en volts, V) se mesure avec un voltmètre branché en dérivation.",
           "En série : même intensité partout, la tension du générateur est la somme des tensions. En dérivation : même tension aux bornes des branches, l’intensité principale est la somme des intensités des branches (loi des nœuds).",
           "Pour un conducteur ohmique : U = R × I, avec R en ohms (Ω)."],
          [("Une résistance de 220 Ω est traversée par 0,05 A. Tension ?", ["U = R × I", "220 × 0,05 = 11"], "11 V.")],
          [("On branche le voltmètre en série.", "Le voltmètre se branche en dérivation."), ("Le courant s’use dans les lampes.", "En série, l’intensité est la même partout.")],
          [("Que veut dire 230 V sur une prise ?", "C’est la tension du secteur en France."), ("À quoi sert une résistance ?", "À limiter l’intensité, par exemple pour protéger une DEL.")],
          [("Grandeurs et appareils", [("l’intensité", "se mesure en ampères"), ("la tension", "se mesure en volts"), ("la résistance", "se mesure en ohms"), ("l’ampèremètre", "se branche en série"),
                                       ("le voltmètre", "se branche en dérivation"), ("l’ohmmètre", "mesure une résistance hors circuit"), ("le multimètre", "peut mesurer U, I ou R")],
            "Que sais-tu sur {k} ?", "Qu’est-ce qui {v} ?"),
           ("Lois", [("intensité dans un circuit en série", "la même partout"), ("tensions dans un circuit en série", "elles s’additionnent"), ("tension aux bornes de branches en dérivation", "la même pour chaque branche"),
                     ("intensité dans la branche principale d’une dérivation", "somme des intensités des branches"), ("conducteur ohmique", "U = R × I"), ("tension aux bornes d’un fil", "presque nulle")],
            "Que dit la loi pour {k} ?", None),
           ("Ordres de grandeur", [("une pile plate", "4,5 V"), ("une prise de la maison", "230 V"), ("une batterie de voiture", "12 V"), ("une pile ronde de télécommande", "1,5 V"),
                                   ("le port USB", "5 V"), ("une ligne à haute tension", "400 000 V")],
            "Quelle tension fournit {k} ?", "Qu’est-ce qui fournit {v} ?")],
          ["U = R × I.", "L’ampèremètre se branche en série.", "Le voltmètre se branche en dérivation.", "En série, l’intensité est la même partout.",
           "En dérivation, les intensités des branches s’additionnent.", "La tension se mesure en volts.", "La tension du secteur est 230 V."],
          [("Le voltmètre se branche en série.", "En dérivation."), ("Le courant s’use dans les lampes.", "L’intensité est la même en série."), ("U = R : I.", "U = R × I."),
           ("En série, les intensités s’additionnent.", "Ce sont les tensions."), ("La résistance se mesure en volts.", "En ohms.")],
          "les lois de l’électricité", "energy", calc=f_ohm),

        H("P", "le-son-et-les-signaux", "Le son et les signaux", "Le son",
          "Les élèves décrivent l’émission et la propagation d’un son, calculent des distances avec la vitesse du son et connaissent fréquence et niveau sonore.",
          "vibration, milieu matériel, vitesse du son, fréquence (Hz), son aigu ou grave, infrasons, ultrasons, niveau sonore (dB), écho",
          "Le son est une vibration qui a besoin de matière", "Dans l’air, il va à environ 340 m/s. Il ne se propage pas dans le vide.",
          ["Un son est produit par un objet qui vibre. Il se propage de proche en proche dans un milieu matériel (air, eau, solide). Il ne se propage pas dans le vide.",
           "Vitesse du son : environ 340 m/s dans l’air, 1 500 m/s dans l’eau, plus encore dans les solides.",
           "La fréquence (en hertz) indique le nombre de vibrations par seconde : plus elle est grande, plus le son est aigu. L’humain entend de 20 Hz à 20 000 Hz. Le niveau sonore se mesure en décibels (dB) : au-delà de 85 dB, l’oreille est en danger."],
          [("On voit l’éclair, et on entend le tonnerre 3 s après. Distance ?", ["La lumière arrive presque tout de suite.", "340 × 3 = 1 020 m."], "Environ 1 km.")],
          [("Le son se propage dans l’espace.", "Il n’y a pas d’air dans l’espace : le son ne s’y propage pas."), ("Un son fort est un son aigu.", "Fort concerne le niveau sonore, aigu la fréquence.")],
          [("Comment les chauves-souris s’orientent-elles ?", "Elles émettent des ultrasons et écoutent leur écho."), ("Pourquoi porter des bouchons au concert ?", "Le niveau sonore dépasse souvent 100 dB et abîme l’oreille.")],
          [("Vocabulaire", [("la fréquence", "nombre de vibrations par seconde"), ("le hertz", "unité de fréquence"), ("le décibel", "unité de niveau sonore"), ("les ultrasons", "fréquence supérieure à 20 000 Hz"),
                            ("les infrasons", "fréquence inférieure à 20 Hz"), ("l’écho", "son réfléchi par un obstacle"), ("le sonomètre", "mesure le niveau sonore")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Aigu ou grave ?", {"des sons aigus": ["le sifflet d’un arbitre", "le chant d’une mésange", "un son de 4 000 Hz", "la note la plus à droite du piano", "le cri d’une souris", "une corde de violon très tendue"],
                                "des sons graves": ["le tonnerre lointain", "la corne de brume d’un bateau", "un son de 80 Hz", "la note la plus à gauche du piano", "le grondement d’un camion", "la grosse caisse d’une batterie"]}),
           ("Niveaux sonores", [("une conversation", "environ 60 dB"), ("un concert de rock", "environ 110 dB"), ("une bibliothèque", "environ 30 dB"), ("un avion au décollage", "environ 130 dB"),
                                ("le seuil de danger", "environ 85 dB"), ("le seuil d’audition", "0 dB")],
            "Quel niveau sonore pour {k} ?", "Qu’est-ce qui correspond à {v} ?")],
          ["Le son a besoin d’un milieu matériel.", "Le son ne se propage pas dans le vide.", "Le son va à environ 340 m/s dans l’air.", "Plus la fréquence est grande, plus le son est aigu.",
           "Le niveau sonore se mesure en décibels.", "Au-delà de 85 dB, l’oreille est en danger.", "Les ultrasons ont une fréquence supérieure à 20 000 Hz."],
          [("Le son se propage dans le vide.", "Il ne s’y propage pas."), ("Un son fort est forcément aigu.", "Fort et aigu sont différents."), ("Le son va plus vite que la lumière.", "La lumière est bien plus rapide."),
           ("La fréquence se mesure en décibels.", "En hertz."), ("Le son va moins vite dans l’eau que dans l’air.", "Il va plus vite dans l’eau.")],
          "le son", "waves-and-light", calc=f_son),

        H("P", "forces-et-interactions", "Actions mécaniques et forces", "Forces",
          "Les élèves modélisent une action mécanique par une force (point d’application, direction, sens, valeur) et distinguent actions de contact et à distance.",
          "action de contact, action à distance, force, newton, dynamomètre, diagramme objet-interaction, représentation vectorielle, principe des actions réciproques",
          "Une action mécanique se modélise par une force", "Une force a un point d’application, une direction, un sens et une valeur en newtons.",
          ["Une action mécanique peut mettre en mouvement, modifier un mouvement ou déformer un objet. Elle est de contact (main, sol, fil) ou à distance (poids, aimant).",
           "On la modélise par une force représentée par une flèche : point d’application, direction, sens, valeur (longueur). La valeur se mesure en newtons (N) avec un dynamomètre.",
           "Si A agit sur B, B agit sur A avec une force de même valeur et de sens opposé."],
          [("Un livre est posé sur une table. Quelles actions s’exercent sur lui ?", ["La Terre l’attire vers le bas (à distance).", "La table le soutient vers le haut (contact)."], "Le poids et l’action de la table.")],
          [("Une force a toujours besoin d’un contact.", "Le poids ou l’attraction d’un aimant agissent à distance."), ("Un objet immobile ne subit aucune force.", "Il subit des forces qui se compensent.")],
          [("Que mesure un dynamomètre ?", "La valeur d’une force, en newtons."), ("Pourquoi le skateur recule-t-il en poussant un mur ?", "Le mur exerce sur lui une force opposée.")],
          [("Contact ou distance ?", {"des actions de contact": ["la main qui pousse une porte", "le pied qui frappe un ballon", "le fil qui retient une lampe", "le sol qui soutient une chaise", "le vent sur une voile", "la raquette sur la balle"],
                                      "des actions à distance": ["la Terre qui attire une pomme", "l’aimant qui attire un clou", "la Lune qui attire les océans", "le Soleil qui attire la Terre", "une règle frottée qui attire des papiers", "deux aimants qui se repoussent"]}),
           ("Caractéristiques d’une force", [("le point d’application", "endroit où la force s’exerce"), ("la direction", "droite selon laquelle elle agit"), ("le sens", "vers où elle agit"), ("la valeur", "intensité en newtons"),
                                             ("le newton", "unité de force"), ("le dynamomètre", "mesure une force"), ("la flèche", "représente une force")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Effets d’une action", [("pousser un chariot à l’arrêt", "le met en mouvement"), ("freiner un vélo", "modifie son mouvement"), ("écraser une balle en mousse", "la déforme"), ("taper un ballon de côté", "change sa direction"),
                                    ("tirer un élastique", "le déforme"), ("un aimant près d’une bille d’acier qui roule", "dévie sa trajectoire")],
            "Quel est l’effet : {k} ?", None)],
          ["Une action mécanique se modélise par une force.", "La valeur d’une force se mesure en newtons.", "Le poids est une action à distance.", "Un dynamomètre mesure une force.",
           "Une force peut déformer un objet.", "Si A agit sur B, B agit sur A.", "Un objet immobile peut subir des forces qui se compensent."],
          [("Une force a toujours besoin d’un contact.", "Certaines agissent à distance."), ("Un objet immobile ne subit aucune force.", "Les forces peuvent se compenser."), ("La force se mesure en kilogrammes.", "En newtons."),
           ("Le poids est une action de contact.", "C’est une action à distance."), ("Une force ne peut pas déformer un objet.", "Elle peut le déformer.")],
          "les forces", "forces-and-motion"),

        H("S", "reproduction-sexuee-et-asexuee", "Reproduction sexuée et asexuée des êtres vivants", "Reproduction",
          "Les élèves comparent reproduction sexuée et asexuée chez les végétaux et les animaux et relient la reproduction à la diversité et au peuplement des milieux.",
          "reproduction sexuée, fécondation, gamètes, reproduction asexuée, bouturage, marcottage, stolons, tubercules, clones, diversité",
          "Sexuée : deux parents, enfants tous différents", "Asexuée : un seul parent, descendants identiques (clones).",
          ["La reproduction sexuée fait intervenir deux gamètes (cellules reproductrices) qui fusionnent lors de la fécondation. Les descendants sont tous différents.",
           "La reproduction asexuée part d’un seul individu : bouture, stolon (fraisier), tubercule (pomme de terre), bourgeonnement. Les descendants sont des clones.",
           "Chez les plantes à fleurs, le grain de pollen apporte le gamète mâle, l’ovule contient le gamète femelle : la fleur devient un fruit, l’ovule une graine."],
          [("Un jardinier plante un morceau de tige de géranium qui fait des racines. Quel type de reproduction ?", ["Un seul parent.", "Pas de fécondation."], "Asexuée (bouturage).")],
          [("La reproduction asexuée n’existe que chez les plantes.", "Les hydres, les étoiles de mer ou les pucerons en sont capables."), ("Les graines viennent d’une reproduction asexuée.", "La graine provient d’une fécondation.")],
          [("Pourquoi les agriculteurs utilisent-ils la reproduction asexuée ?", "Pour obtenir rapidement des plantes identiques à une variété intéressante."), ("Quel avantage a la reproduction sexuée ?", "Elle crée de la diversité, utile quand le milieu change.")],
          [("Sexuée ou asexuée ?", {"de la reproduction sexuée": ["la pollinisation puis la graine", "la ponte d’œufs fécondés", "la naissance d’un veau", "la fécondation chez la grenouille", "le grain de pollen sur le pistil"],
                                    "de la reproduction asexuée": ["le stolon du fraisier", "la bouture de géranium", "le tubercule de pomme de terre", "le bourgeonnement de l’hydre", "le bulbe de tulipe", "la marcotte de lierre", "le drageon du framboisier"]}),
           ("Vocabulaire", [("le gamète", "cellule reproductrice"), ("la fécondation", "fusion de deux gamètes"), ("le clone", "individu identique à son parent"), ("le stolon", "tige rampante qui donne une nouvelle plante"),
                            ("le tubercule", "organe de réserve qui peut donner une plante"), ("l’ovule", "contient le gamète femelle de la fleur"), ("le grain de pollen", "apporte le gamète mâle")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Exemples", [("le fraisier", "stolons"), ("la pomme de terre", "tubercules"), ("la tulipe", "bulbes"), ("l’hydre", "bourgeonnement"), ("le saule", "bouturage naturel des branches"),
                         ("le puceron en été", "femelles qui se reproduisent seules"), ("l’étoile de mer", "un bras coupé peut donner un individu")],
            "Comment se reproduit de façon asexuée {k} ?", "Quel être vivant utilise : {v} ?")],
          ["La fécondation fait fusionner deux gamètes.", "La reproduction asexuée donne des clones.", "Le fraisier se multiplie par stolons.", "La graine provient d’une fécondation.",
           "La reproduction sexuée crée de la diversité.", "La pomme de terre se multiplie par tubercules.", "Certains animaux se reproduisent de façon asexuée."],
          [("La reproduction asexuée n’existe que chez les plantes.", "Certains animaux en sont capables."), ("Les clones sont tous différents.", "Ils sont identiques."), ("La graine vient d’une reproduction asexuée.", "D’une fécondation."),
           ("La reproduction sexuée a besoin d’un seul parent.", "Elle en demande deux."), ("Le stolon est un gamète.", "C’est une tige rampante.")],
          "la reproduction", "living-things-and-ecosystems"),

        H("S", "puberte-et-reproduction-humaine", "Puberté et reproduction humaine", "Reproduction humaine",
          "Les élèves décrivent les transformations de la puberté, le fonctionnement des appareils reproducteurs, la fécondation, la grossesse et les moyens de contraception.",
          "puberté, hormones, testicules, spermatozoïdes, ovaires, ovules, cycle menstruel, fécondation, nidation, grossesse, contraception, IST",
          "La puberté rend le corps capable de se reproduire", "La fécondation a lieu dans une trompe, l’embryon se développe dans l’utérus.",
          ["À la puberté, les hormones (testostérone, œstrogènes) déclenchent des transformations : les testicules produisent des spermatozoïdes en continu, les ovaires libèrent environ un ovule par cycle.",
           "Le cycle menstruel dure environ 28 jours. L’ovulation a lieu vers le 14e jour. Sans fécondation, la paroi de l’utérus est éliminée : ce sont les règles.",
           "La fécondation a lieu dans une trompe. L’embryon s’implante dans l’utérus (nidation). La grossesse dure environ 9 mois. Le préservatif protège aussi des infections sexuellement transmissibles (IST)."],
          [("Le cycle commence au premier jour des règles, le 3 mai. Vers quand a lieu l’ovulation (cycle de 28 jours) ?", ["L’ovulation se produit vers le 14e jour.", "3 + 13 = 16."], "Vers le 16 mai.")],
          [("L’ovule se fait féconder dans l’utérus.", "La fécondation a lieu dans une trompe."), ("Tous les contraceptifs protègent des IST.", "Seul le préservatif protège aussi des IST.")],
          [("À quel âge commence la puberté ?", "Entre 8 et 13 ans environ chez les filles, 9 et 14 ans chez les garçons, selon chacun."), ("Combien de spermatozoïdes fécondent l’ovule ?", "Un seul.")],
          [("Organes", [("les testicules", "produisent les spermatozoïdes"), ("les ovaires", "libèrent les ovules"), ("l’utérus", "accueille et nourrit l’embryon"), ("les trompes", "lieu de la fécondation"),
                        ("le placenta", "échanges entre la mère et le fœtus"), ("le canal déférent", "conduit les spermatozoïdes"), ("le vagin", "reçoit les spermatozoïdes lors du rapport sexuel")],
            "Quel est le rôle de {k} ?", "Quel organe {v} ?"),
           ("Vocabulaire", [("la nidation", "l’embryon s’implante dans l’utérus"), ("l’ovulation", "libération d’un ovule"), ("les règles", "élimination de la paroi de l’utérus"), ("le fœtus", "le futur bébé après 3 mois"),
                            ("la contraception", "méthodes pour éviter une grossesse"), ("une IST", "infection sexuellement transmissible"), ("la testostérone", "hormone produite par les testicules")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Contraception et protection", [("le préservatif", "évite la grossesse et protège des IST"), ("la pilule", "bloque l’ovulation"), ("le stérilet", "empêche la nidation"), ("la pilule du lendemain", "contraception d’urgence"),
                                            ("le dépistage", "permet de savoir si l’on a une IST"), ("le vaccin contre le papillomavirus", "protège contre certains cancers")],
            "À quoi sert {k} ?", "Quel moyen {v} ?")],
          ["La fécondation a lieu dans une trompe.", "L’embryon se développe dans l’utérus.", "Les testicules produisent les spermatozoïdes.", "Le préservatif protège des IST.",
           "L’ovulation a lieu vers le milieu du cycle.", "Un seul spermatozoïde féconde l’ovule.", "La grossesse dure environ 9 mois."],
          [("La fécondation a lieu dans l’utérus.", "Dans une trompe."), ("Tous les contraceptifs protègent des IST.", "Seul le préservatif."), ("Les ovaires produisent des spermatozoïdes.", "Ils libèrent des ovules."),
           ("Plusieurs spermatozoïdes fécondent l’ovule.", "Un seul."), ("Les règles ont lieu au moment de l’ovulation.", "Elles arrivent en l’absence de fécondation.")],
          "la reproduction humaine", "living-things-and-ecosystems"),

        H("S", "seismes-volcans-et-tectonique", "Séismes, volcans et tectonique des plaques", "Tectonique des plaques",
          "Les élèves relient la répartition des séismes et des volcans aux mouvements des plaques lithosphériques et étudient les risques associés.",
          "plaques lithosphériques, dorsale, subduction, faille, foyer, épicentre, magnitude, volcan effusif et explosif, risque, prévention",
          "La surface de la Terre est découpée en plaques mobiles", "Séismes et volcans se concentrent aux frontières des plaques.",
          ["La lithosphère est découpée en une douzaine de grandes plaques qui se déplacent de quelques centimètres par an.",
           "Aux dorsales, les plaques s’écartent et du magma remonte. Aux zones de subduction, une plaque plonge sous une autre. Les frottements provoquent des séismes et des volcans.",
           "Un séisme naît au foyer en profondeur. L’épicentre est le point de la surface juste au-dessus. Les volcans effusifs émettent des coulées de lave fluide, les explosifs projettent des cendres et des nuées ardentes."],
          [("Une plaque se déplace de 3 cm par an. Quelle distance en 1 million d’années ?", ["3 cm × 1 000 000 = 3 000 000 cm.", "= 30 km."], "30 km.")],
          [("L’épicentre est en profondeur.", "C’est le foyer qui est en profondeur, l’épicentre est en surface."), ("Les plaques ne bougent plus aujourd’hui.", "Elles bougent toujours, lentement.")],
          [("Pourquoi le Japon a-t-il beaucoup de séismes ?", "Il est situé sur des zones de subduction où plusieurs plaques se rencontrent."), ("Peut-on prévoir un séisme ?", "On connaît les zones à risque, mais pas la date exacte : on mise sur la prévention.")],
          [("Vocabulaire", [("le foyer", "point en profondeur où naît le séisme"), ("l’épicentre", "point de la surface au-dessus du foyer"), ("la magnitude", "énergie libérée par le séisme"), ("le sismographe", "enregistre les ondes sismiques"),
                            ("la dorsale", "zone où les plaques s’écartent"), ("la subduction", "une plaque plonge sous une autre"), ("la faille", "cassure où les roches se déplacent"), ("le magma", "roche fondue en profondeur")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Volcans", [("l’Etna", "volcan en Sicile, souvent effusif"), ("le Piton de la Fournaise", "volcan effusif de La Réunion"), ("la montagne Pelée", "volcan explosif de la Martinique"),
                        ("le Vésuve", "volcan explosif qui a détruit Pompéi"), ("le Kilauea", "volcan effusif d’Hawaï"), ("le mont Saint Helens", "volcan explosif des États-Unis")],
            "Que sais-tu de {k} ?", "Quel volcan : {v} ?"),
           ("Effusif ou explosif ?", {"des volcans effusifs": ["lave fluide", "coulées de lave", "fontaines de lave", "volcan de point chaud comme à Hawaï", "éruption peu dangereuse pour les personnes"],
                                      "des volcans explosifs": ["lave visqueuse", "nuées ardentes", "panache de cendres", "dôme de lave", "volcan de zone de subduction", "éruption très dangereuse pour les populations"]})],
          ["La lithosphère est découpée en plaques.", "Les plaques se déplacent de quelques centimètres par an.", "L’épicentre est à la surface.", "Les séismes sont fréquents aux frontières des plaques.",
           "Aux dorsales, les plaques s’écartent.", "Un volcan explosif émet une lave visqueuse.", "On ne peut pas prévoir la date exacte d’un séisme."],
          [("L’épicentre est en profondeur.", "C’est le foyer."), ("Les plaques ne bougent plus.", "Elles bougent toujours."), ("Les volcans explosifs ont une lave très fluide.", "Leur lave est visqueuse."),
           ("On peut prévoir la date d’un séisme.", "On ne peut pas."), ("Aux dorsales, une plaque plonge sous une autre.", "C’est la subduction.")],
          "la tectonique des plaques", "earths-systems"),

        H("S", "meteo-climat-et-changement-climatique", "Météo, climat et changement climatique", "Climat",
          "Les élèves distinguent météorologie et climat, expliquent l’effet de serre et relient l’activité humaine au réchauffement climatique.",
          "météorologie, climat, zones climatiques, circulation atmosphérique et océanique, effet de serre, gaz à effet de serre, réchauffement, atténuation, adaptation",
          "Plus de gaz à effet de serre, plus de chaleur retenue", "Le CO₂ issu des énergies fossiles est la cause principale du réchauffement actuel.",
          ["La météo décrit le temps d’un jour. Le climat est la moyenne du temps sur au moins 30 ans.",
           "L’effet de serre est naturel : des gaz (vapeur d’eau, CO₂, méthane) retiennent une partie de la chaleur émise par la Terre. Sans lui, il ferait −18 °C en moyenne.",
           "Depuis 1850, l’humain a beaucoup augmenté le CO₂ (charbon, pétrole, gaz, déforestation). La température moyenne a augmenté d’environ 1,2 °C. On agit en réduisant les émissions (atténuation) et en s’adaptant."],
          [("Le CO₂ est passé d’environ 280 ppm à plus de 420 ppm. De combien a-t-il augmenté ?", ["420 − 280 = 140.", "140 : 280 = 0,5."], "D’environ 140 ppm, soit 50 %.")],
          [("L’effet de serre est toujours néfaste.", "L’effet de serre naturel rend la Terre habitable, c’est son renforcement qui pose problème."), ("Le trou de la couche d’ozone cause le réchauffement.", "Ce sont deux problèmes différents.")],
          [("Que veut dire ppm ?", "Partie par million : 420 ppm, c’est 420 molécules de CO₂ sur un million de molécules d’air."), ("Quels gestes réduisent les émissions ?", "Moins de voiture, isoler les logements, manger moins de viande, sobriété énergétique.")],
          [("Sources d’émissions", [("la voiture à essence", "émet du dioxyde de carbone"), ("l’élevage de vaches", "émet du méthane"), ("les engrais azotés", "émettent du protoxyde d’azote"),
                                    ("la centrale à charbon", "émet beaucoup de dioxyde de carbone"), ("la déforestation", "libère le carbone stocké dans les arbres"), ("les climatiseurs qui fuient", "émettent des gaz fluorés"),
                                    ("les rizières inondées", "émettent du méthane"), ("l’éolienne en fonctionnement", "n’émet presque pas de gaz à effet de serre")],
            "Que fait {k} pour le climat ?", "Quelle activité {v} ?"),
           ("Atténuation ou adaptation ?", {"de l’atténuation": ["isoler les maisons", "remplacer le charbon par l’éolien", "prendre le train plutôt que l’avion", "manger moins de viande", "planter des forêts"],
                                            "de l’adaptation": ["construire des digues", "végétaliser les villes contre la chaleur", "cultiver des plantes résistantes à la sécheresse", "créer des zones d’ombre dans les cours", "économiser l’eau l’été", "surélever les maisons en zone inondable"]}),
           ("Vocabulaire", [("le climat", "moyenne du temps sur au moins 30 ans"), ("la météo", "temps qu’il fait un jour donné"), ("l’effet de serre", "gaz qui retiennent la chaleur de la Terre"), ("le GIEC", "experts qui évaluent le climat"),
                            ("la fonte des glaciers", "conséquence du réchauffement"), ("la montée des océans", "due à la fonte des glaces et à la dilatation de l’eau"), ("l’empreinte carbone", "émissions de gaz liées à nos activités")],
            "Que désigne {k} ?", "Quoi : {v} ?")],
          ["Le climat se calcule sur au moins 30 ans.", "L’effet de serre naturel rend la Terre habitable.", "Le CO₂ des énergies fossiles renforce l’effet de serre.", "La température moyenne a augmenté d’environ 1,2 °C.",
           "Le méthane est un gaz à effet de serre.", "Isoler les maisons réduit les émissions.", "Le niveau des océans monte."],
          [("L’effet de serre est toujours néfaste.", "L’effet de serre naturel est indispensable."), ("Le trou de la couche d’ozone cause le réchauffement.", "Ce sont deux problèmes distincts."), ("Une journée froide prouve que le climat se refroidit.", "C’est de la météo."),
           ("Le méthane n’est pas un gaz à effet de serre.", "C’en est un."), ("Le niveau des océans baisse.", "Il monte.")],
          "le climat", "earths-systems"),
    ]
