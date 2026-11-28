# -*- coding: utf-8 -*-
"""France / Physique-chimie et SVT : 3e（cycle 4）"""
from fr_sci import H, nq, num


def f_poids(R):
    k = R.choice(["P", "P", "m", "lune", "mars", "g"])
    if k == "P":
        m = R.choice([2, 5, 0.5, 60, 45, 12, 0.25, 80])
        return nq("Quel est le poids sur Terre d’un objet de %s kg ? (g = 9,8 N/kg)" % num(m), m * 9.8, [m / 9.8, m, m * 98], "N", "P = m × g = %s × 9,8 = %s N." % (num(m), num(m * 9.8)))
    if k == "m":
        P = R.choice([49, 98, 588, 4.9, 196, 735])
        return nq("Un objet a un poids de %s N sur Terre (g = 9,8 N/kg). Quelle est sa masse ?" % num(P), P / 9.8, [P * 9.8, P, P / 98], "kg", "m = P : g = %s : 9,8 = %s kg." % (num(P), num(P / 9.8)))
    if k == "lune":
        m = R.choice([60, 90, 10, 75, 30, 120])
        return nq("Un astronaute de %s kg (équipement compris) marche sur la Lune (g = 1,6 N/kg). Quel est son poids ?" % num(m), m * 1.6, [m * 9.8, m, m / 1.6], "N",
                  "P = %s × 1,6 = %s N. Sa masse reste %s kg." % (num(m), num(m * 1.6), num(m)))
    if k == "mars":
        m = R.choice([20, 50, 100, 8, 200])
        return nq("Un robot de %s kg est sur Mars (g = 3,7 N/kg). Quel est son poids ?" % num(m), m * 3.7, [m * 9.8, m / 3.7, m], "N", "P = %s × 3,7 = %s N." % (num(m), num(m * 3.7)))
    m, P = R.choice([(10, 16), (5, 18.5), (2, 49.6), (4, 39.2), (20, 74)])
    return nq("Un objet de %s kg pèse %s N sur un astre. Quelle est l’intensité de la pesanteur ?" % (num(m), num(P)), P / m, [P * m, m / P, P - m], "N/kg", "g = P : m = %s : %s = %s N/kg." % (num(P), num(m), num(P / m)))


def f_ec(R):
    k = R.choice(["Ec", "Ec", "Ec2", "v2", "km"])
    if k == "Ec":
        m, v = R.choice([(1000, 10), (2, 5), (0.5, 20), (60, 4), (1200, 20), (80, 10), (0.06, 50)])
        return nq("Quelle est l’énergie cinétique d’un objet de %s kg qui roule à %s m/s ?" % (num(m), num(v)), 0.5 * m * v * v, [m * v * v, 0.5 * m * v, m * v], "J",
                  "Ec = ½ × m × v² = 0,5 × %s × %s² = %s J." % (num(m), num(v), num(0.5 * m * v * v)))
    if k == "Ec2":
        m, v = R.choice([(1000, 10), (60, 5), (2, 3), (500, 8)])
        e1, e2 = 0.5 * m * v * v, 0.5 * m * (2 * v) ** 2
        return nq("Un objet de %s kg passe de %s m/s à %s m/s. Quelle est sa nouvelle énergie cinétique ?" % (num(m), num(v), num(2 * v)), e2, [2 * e1, e1, e2 / 2 + e1], "J",
                  "Ec = 0,5 × %s × %s² = %s J : vitesse doublée, énergie multipliée par 4." % (num(m), num(2 * v), num(e2)))
    if k == "v2":
        m, E = R.choice([(2, 100), (1000, 50000), (4, 200), (80, 1000), (10, 500)])
        v = (2 * E / m) ** 0.5
        return nq("Un objet de %s kg a une énergie cinétique de %s J. Quelle est sa vitesse ?" % (num(m), num(E)), v, [2 * E / m, E / m, v * 2], "m/s", "v = √(2 × Ec : m) = √(%s) = %s m/s." % (num(2 * E / m), num(v)))
    v = R.choice([36, 72, 90, 54, 108])
    m = R.choice([1000, 1200, 800])
    vs = v / 3.6
    return nq("Une voiture de %s kg roule à %s km/h. Quelle est son énergie cinétique ?" % (num(m), num(v)), 0.5 * m * vs * vs, [0.5 * m * v * v, m * vs * vs, 0.5 * m * vs], "J",
              "On convertit : %s km/h = %s m/s. Ec = 0,5 × %s × %s² = %s J." % (num(v), num(vs), num(m), num(vs), num(0.5 * m * vs * vs)))


def f_puis(R):
    k = R.choice(["P", "P", "E", "kwh", "cout", "I"])
    if k == "P":
        U, I = R.choice([(230, 2), (230, 10), (12, 5), (230, 0.5), (5, 2), (230, 8.7)])
        return nq("Un appareil fonctionne sous %s V et est traversé par %s A. Quelle est sa puissance ?" % (num(U), num(I)), U * I, [U / I, I / U, U + I], "W", "P = U × I = %s × %s = %s W." % (num(U), num(I), num(U * I)))
    if k == "I":
        P, U = R.choice([(2300, 230), (1150, 230), (60, 12), (460, 230), (10, 5), (3450, 230)])
        return nq("Un appareil de %s W est branché sur %s V. Quelle intensité le traverse ?" % (num(P), num(U)), P / U, [P * U, U / P, P - U], "A", "I = P : U = %s : %s = %s A." % (num(P), num(U), num(P / U)))
    if k == "E":
        P, t = R.choice([(2000, 3), (60, 5), (1500, 2), (800, 0.5), (100, 10), (2500, 1.5)])
        return nq("Quelle énergie consomme un appareil de %s W qui fonctionne %s h ? Donne la réponse en Wh." % (num(P), num(t)), P * t, [P / t, P * t / 1000, P + t], "Wh",
                  "E = P × t = %s W × %s h = %s Wh." % (num(P), num(t), num(P * t)))
    if k == "kwh":
        P, t = R.choice([(2000, 3), (1500, 2), (100, 10), (500, 4), (2500, 2), (40, 50)])
        return nq("Un appareil de %s W fonctionne %s h. Combien de kWh consomme-t-il ?" % (num(P), num(t)), P * t / 1000, [P * t, P / t, P * t / 100], "kWh",
                  "E = %s W × %s h = %s Wh = %s kWh." % (num(P), num(t), num(P * t), num(P * t / 1000)))
    E, c = R.choice([(10, 0.25), (6, 0.25), (200, 0.2), (3.5, 0.2), (150, 0.25), (40, 0.2)])
    return nq("Un foyer consomme %s kWh. Le kWh coûte %s €. Quel est le coût ?" % (num(E), num(c)), E * c, [E / c, c / E, E + c], "€", "%s × %s = %s €." % (num(E), num(c), num(E * c)))


def UNITS(grade):
    return [
        H("P", "atomes-ions-et-noyau", "Atome, noyau et ions", "Atomes et ions",
          "Les élèves décrivent la structure de l’atome (noyau de protons et de neutrons, électrons), interprètent la formation des ions et leur charge, et identifient des ions par des tests.",
          "atome, noyau, protons, neutrons, électrons, numéro atomique, neutralité, ions positifs et négatifs, tests des ions, tableau périodique",
          "Un atome est neutre : autant de protons que d’électrons", "Un ion est un atome qui a gagné ou perdu des électrons.",
          ["L’atome est formé d’un noyau (protons positifs, neutrons neutres) et d’électrons négatifs autour. Il est neutre : autant de protons que d’électrons. Le noyau est environ 100 000 fois plus petit que l’atome.",
           "Le numéro atomique Z est le nombre de protons : il caractérise l’élément (Z = 6 pour le carbone).",
           "Un ion positif (cation) a perdu des électrons : Na⁺, Cu²⁺. Un ion négatif (anion) en a gagné : Cl⁻. On identifie les ions par des tests de précipitation."],
          [("L’atome de magnésium (Z = 12) perd 2 électrons. Quel ion obtient-on ?", ["12 protons, il reste 10 électrons.", "Charge : +12 − 10 = +2."], "Mg²⁺")],
          [("Un ion positif a gagné des électrons.", "Il en a perdu : il a plus de protons que d’électrons."), ("Le noyau occupe presque tout l’atome.", "Il est minuscule, l’atome est surtout du vide.")],
          [("Pourquoi l’atome est-il neutre ?", "La charge des protons compense exactement celle des électrons."), ("Comment reconnaître les ions chlorure ?", "Avec du nitrate d’argent : précipité blanc qui noircit à la lumière.")],
          [("Particules", [("le proton", "particule positive du noyau"), ("le neutron", "particule neutre du noyau"), ("l’électron", "particule négative autour du noyau"), ("le noyau", "contient protons et neutrons"),
                           ("le numéro atomique", "nombre de protons"), ("l’ion", "atome ou groupe d’atomes chargé"), ("le nuage électronique", "espace occupé par les électrons")],
            "Que désigne {k} ?", "Qu’est-ce que {v} ?"),
           ("Tests des ions", [("ion cuivre Cu²⁺", "précipité bleu avec la soude"), ("ion fer II Fe²⁺", "précipité vert avec la soude"), ("ion fer III Fe³⁺", "précipité rouille avec la soude"),
                               ("ion chlorure Cl⁻", "précipité blanc avec le nitrate d’argent"), ("ion hydrogène H⁺", "papier pH rouge, solution acide"), ("ion hydroxyde HO⁻", "papier pH bleu, solution basique"), ("ion zinc Zn²⁺", "précipité blanc avec la soude")],
            "Comment identifie-t-on l’{k} ?", "Quel ion donne : {v} ?"),
           ("Ions", [("Na⁺", "a perdu 1 électron"), ("Cu²⁺", "a perdu 2 électrons"), ("Cl⁻", "a gagné 1 électron"), ("Al³⁺", "a perdu 3 électrons"), ("O²⁻", "a gagné 2 électrons"), ("Mg²⁺", "a perdu 2 électrons".replace("2 électrons", "2 électrons (Z = 12)")),
                     ("Fe³⁺", "a perdu 3 électrons (Z = 26)"), ("S²⁻", "a gagné 2 électrons (Z = 16)")],
            "Que sais-tu de l’ion {k} ?", "Quel ion {v} ?")],
          ["Un atome est électriquement neutre.", "Le noyau contient protons et neutrons.", "Un ion positif a perdu des électrons.", "Le numéro atomique est le nombre de protons.",
           "L’atome est surtout constitué de vide.", "Les ions cuivre donnent un précipité bleu avec la soude.", "Cl⁻ a gagné un électron."],
          [("Un ion positif a gagné des électrons.", "Il en a perdu."), ("Le noyau occupe tout l’atome.", "Il est minuscule."), ("Les neutrons sont négatifs.", "Ils sont neutres."),
           ("Le numéro atomique est le nombre de neutrons.", "C’est le nombre de protons."), ("Les ions fer III donnent un précipité bleu.", "Ils donnent un précipité rouille.")],
          "les atomes et les ions", "matter"),

        H("P", "acides-bases-et-ph", "Acides, bases et pH", "Le pH",
          "Les élèves mesurent le pH de solutions, relient l’acidité à la présence d’ions H⁺, étudient la réaction entre l’acide chlorhydrique et le fer et les règles de sécurité.",
          "pH, solution acide, neutre, basique, ions H⁺ et HO⁻, dilution, réaction acide-métal, dihydrogène, pictogrammes de danger",
          "pH sous 7 : acide, 7 : neutre, au-dessus : basique", "Plus le pH est petit, plus la solution est acide.",
          ["Le pH se mesure avec du papier pH ou un pH-mètre, de 0 à 14. Une solution acide contient plus d’ions H⁺ que d’ions HO⁻, une solution basique l’inverse.",
           "Diluer un acide rapproche son pH de 7. Pour diluer, on verse toujours l’acide dans l’eau, jamais l’inverse.",
           "L’acide chlorhydrique réagit avec le fer : il se forme du dihydrogène (petite détonation) et des ions fer II."],
          [("On dilue du vinaigre (pH 3) dans beaucoup d’eau. Le pH ?", ["La solution devient moins acide.", "Le pH augmente vers 7, sans le dépasser."], "Il augmente, mais reste inférieur à 7.")],
          [("Diluer un acide le rend basique.", "Son pH se rapproche de 7 sans le dépasser."), ("On verse l’eau dans l’acide.", "On verse l’acide dans l’eau pour éviter les projections.")],
          [("Pourquoi porter des lunettes ?", "Les acides et les bases concentrés brûlent les yeux et la peau."), ("Que dégage l’acide sur du calcaire ?", "Du dioxyde de carbone : il y a effervescence.")],
          [("pH courants", [("le jus de citron", "acide, pH environ 2"), ("le vinaigre", "acide, pH environ 3"), ("l’eau pure", "neutre, pH 7"), ("l’eau de Javel", "basique, pH environ 12"),
                            ("le soda au cola", "acide, pH environ 2,5"), ("l’eau savonneuse", "basique, pH environ 9"), ("le lait", "légèrement acide, pH environ 6,5"), ("la soude", "très basique, pH environ 14")],
            "Quel pH pour {k} ?", "Quelle solution : {v} ?"),
           ("Acide, neutre ou basique ?", {"des solutions acides": ["pH 2", "pH 4,5", "papier pH rouge", "plus d’ions H⁺ que d’ions HO⁻", "jus de pomme"],
                                           "des solutions basiques": ["pH 11", "pH 8,5", "papier pH bleu foncé", "plus d’ions HO⁻ que d’ions H⁺", "produit pour déboucher l’évier"],
                                           "des solutions neutres": ["pH 7", "eau distillée", "autant d’ions H⁺ que d’ions HO⁻", "eau salée pure"]}),
           ("Sécurité", [("pictogramme corrosif", "brûle la peau et les yeux"), ("pictogramme inflammable", "peut prendre feu"), ("pictogramme toxique", "dangereux en cas d’ingestion"), ("lunettes de protection", "protègent les yeux"),
                         ("blouse en coton", "protège les vêtements et la peau"), ("diluer un acide", "verser l’acide dans l’eau")],
            "Que signifie ou à quoi sert {k} ?", None)],
          ["Une solution de pH 3 est acide.", "L’eau pure a un pH de 7.", "Une solution basique a un pH supérieur à 7.", "On verse l’acide dans l’eau.",
           "Diluer un acide augmente son pH.", "L’acide chlorhydrique et le fer produisent du dihydrogène.", "Le jus de citron est acide."],
          [("Diluer un acide le rend basique.", "Son pH se rapproche de 7."), ("On verse l’eau dans l’acide.", "On verse l’acide dans l’eau."), ("Une solution de pH 10 est acide.", "Elle est basique."),
           ("Plus le pH est grand, plus la solution est acide.", "Plus il est petit, plus elle est acide."), ("L’eau de Javel est acide.", "Elle est basique.")],
          "les acides et les bases", "matter"),

        H("P", "poids-et-gravitation", "Poids, masse et gravitation", "Poids et gravitation",
          "Les élèves distinguent masse et poids, utilisent la relation P = m × g et décrivent la gravitation qui maintient les planètes en orbite.",
          "masse (kg), poids (N), intensité de la pesanteur g, P = m × g, gravitation universelle, attraction entre objets, orbite",
          "P = m × g", "La masse ne change pas d’un astre à l’autre, le poids oui.",
          ["La masse mesure la quantité de matière (kg, balance). Le poids est la force d’attraction de l’astre (N, dynamomètre).",
           "P = m × g. Sur Terre, g ≈ 9,8 N/kg. Sur la Lune, g ≈ 1,6 N/kg : on pèse environ 6 fois moins.",
           "La gravitation est une attraction à distance entre tous les objets qui ont une masse. Elle diminue avec la distance. Elle maintient la Lune autour de la Terre et les planètes autour du Soleil."],
          [("Un sac de 5 kg sur Terre : masse et poids sur la Lune ?", ["La masse reste 5 kg.", "P = 5 × 1,6 = 8 N."], "5 kg et 8 N.")],
          [("On dit « je pèse 40 kg ».", "40 kg est une masse. Le poids est d’environ 392 N."), ("Il n’y a pas de gravitation dans l’espace.", "Elle existe partout, elle diminue avec la distance.")],
          [("Pourquoi les astronautes flottent-ils dans l’ISS ?", "La station et eux tombent ensemble autour de la Terre : ils sont en chute libre."), ("Quelle est la direction du poids ?", "La verticale, vers le centre de la Terre.")],
          [("Masse ou poids ?", {"des propriétés de la masse": ["se mesure en kilogrammes", "se mesure avec une balance", "ne change pas sur la Lune", "quantité de matière", "identique sur Terre et sur Mars", "s’exprime en grammes"],
                                 "des propriétés du poids": ["se mesure en newtons", "se mesure avec un dynamomètre", "plus faible sur la Lune", "force verticale vers le bas", "dépend de l’astre", "plus grand sur Jupiter"]}),
           ("Intensité de la pesanteur", [("sur la Terre", "environ 9,8 N/kg"), ("sur la Lune", "environ 1,6 N/kg"), ("sur Mars", "environ 3,7 N/kg"), ("sur Jupiter", "environ 25 N/kg"),
                                          ("au sommet de l’Everest", "un peu moins de 9,8 N/kg"), ("sur Vénus", "environ 8,9 N/kg")],
            "Quelle est la valeur de g {k} ?", "Où g vaut-il {v} ?"),
           ("Gravitation", [("la Lune tourne autour de la Terre", "attraction de la Terre"), ("les marées", "attraction de la Lune et du Soleil"), ("une pomme tombe", "attraction de la Terre"),
                            ("les planètes tournent autour du Soleil", "attraction du Soleil"), ("plus on s’éloigne de la Terre", "l’attraction diminue"), ("deux objets plus massifs", "s’attirent plus fort")],
            "Qu’est-ce qui explique : {k} ?", None)],
          ["P = m × g.", "La masse ne change pas sur la Lune.", "Le poids se mesure en newtons.", "Sur la Lune, g vaut environ 1,6 N/kg.",
           "La gravitation diminue avec la distance.", "Le Soleil attire les planètes.", "Le poids est vertical et dirigé vers le bas."],
          [("La masse change sur la Lune.", "C’est le poids qui change."), ("Le poids se mesure en kilogrammes.", "En newtons."), ("Il n’y a pas de gravitation dans l’espace.", "Elle existe partout."),
           ("Sur la Lune, g vaut 9,8 N/kg.", "Il vaut environ 1,6 N/kg."), ("La balance mesure le poids.", "Elle mesure la masse.")],
          "le poids", "forces-and-motion", calc=f_poids),

        H("P", "energie-cinetique-et-conservation", "Énergie cinétique et conservation de l’énergie", "Énergie cinétique",
          "Les élèves calculent une énergie cinétique, décrivent les conversions entre énergie de position et énergie cinétique et relient la vitesse à la sécurité routière.",
          "énergie cinétique Ec = ½ m v², énergie de position, énergie mécanique, conversion, conservation, distance de freinage, sécurité routière",
          "Ec = ½ × m × v²", "Si la vitesse double, l’énergie cinétique est multipliée par 4.",
          ["Un objet en mouvement possède une énergie cinétique : Ec = ½ × m × v², avec m en kg, v en m/s et Ec en joules (J).",
           "Un objet en hauteur possède une énergie de position. En tombant, elle se convertit en énergie cinétique. L’énergie se conserve, une partie devient de la chaleur (frottements).",
           "La distance de freinage augmente avec l’énergie cinétique : à 100 km/h, elle est environ 4 fois plus longue qu’à 50 km/h."],
          [("Une voiture de 1 000 kg roule à 20 m/s. Ec ?", ["Ec = 0,5 × 1 000 × 20²", "= 0,5 × 1 000 × 400"], "200 000 J.")],
          [("Si la vitesse double, l’énergie double.", "Elle est multipliée par 4 car la vitesse est au carré."), ("L’énergie disparaît quand on freine.", "Elle se transforme en chaleur dans les freins.")],
          [("Pourquoi la vitesse est-elle limitée près des écoles ?", "À vitesse plus faible, l’énergie cinétique et la distance d’arrêt sont bien plus petites."), ("Que devient l’énergie d’une balle qui rebondit de moins en moins haut ?", "Elle se transforme peu à peu en chaleur et en son.")],
          [("Conversions", [("une pomme qui tombe", "énergie de position → énergie cinétique"), ("une voiture qui freine", "énergie cinétique → chaleur"), ("un barrage hydroélectrique", "énergie de position de l’eau → électricité"),
                            ("une balle lancée vers le haut", "énergie cinétique → énergie de position"), ("un skateur dans une rampe", "échanges entre position et mouvement"), ("une éolienne", "énergie cinétique du vent → électricité")],
            "Quelle conversion : {k} ?", None),
           ("Ce qui change Ec", [("doubler la vitesse", "Ec multipliée par 4"), ("doubler la masse", "Ec multipliée par 2"), ("tripler la vitesse", "Ec multipliée par 9"), ("diviser la vitesse par 2", "Ec divisée par 4"),
                                 ("objet immobile", "Ec nulle"), ("diviser la masse par 2", "Ec divisée par 2")],
            "Que devient l’énergie cinétique si l’on {k} ?".replace("si l’on {k}", "dans ce cas : {k}"), None),
           ("Vocabulaire", [("l’énergie cinétique", "liée à la vitesse"), ("l’énergie de position", "liée à la hauteur"), ("l’énergie mécanique", "somme des énergies cinétique et de position"), ("le joule", "unité d’énergie"),
                            ("la distance de réaction", "parcourue pendant le temps de réaction"), ("la distance de freinage", "parcourue pendant le freinage"), ("la distance d’arrêt", "réaction + freinage")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Ec = ½ × m × v².", "Si la vitesse double, Ec est multipliée par 4.", "L’énergie se mesure en joules.", "En tombant, l’énergie de position devient énergie cinétique.",
           "Un objet immobile a une énergie cinétique nulle.", "En freinant, l’énergie cinétique devient de la chaleur.", "La distance d’arrêt est la somme de la distance de réaction et de freinage."],
          [("Si la vitesse double, Ec double.", "Elle est multipliée par 4."), ("L’énergie disparaît au freinage.", "Elle devient de la chaleur."), ("L’énergie se mesure en newtons.", "En joules."),
           ("Un objet immobile a une grande énergie cinétique.", "Elle est nulle."), ("La masse n’influence pas Ec.", "Ec est proportionnelle à la masse.")],
          "l’énergie cinétique", "energy", calc=f_ec),

        H("P", "puissance-et-energie-electrique", "Puissance et énergie électriques", "Puissance électrique",
          "Les élèves utilisent les relations P = U × I et E = P × t, calculent une consommation en kWh et son coût, et relient la puissance à la sécurité de l’installation.",
          "puissance (W), P = U × I, énergie (J, Wh, kWh), E = P × t, facture d’électricité, compteur, fusible, disjoncteur",
          "P = U × I et E = P × t", "1 kWh = 1 000 Wh : c’est l’unité de la facture d’électricité.",
          ["La puissance d’un appareil (en watts, W) est inscrite sur sa plaque. P = U × I.",
           "L’énergie consommée dépend de la puissance et de la durée : E = P × t. Avec P en W et t en h, E est en Wh. Le fournisseur facture des kWh.",
           "Trop d’appareils puissants sur une même prise augmentent l’intensité : le fusible ou le disjoncteur coupe le circuit."],
          [("Un radiateur de 2 000 W fonctionne 5 h. Énergie en kWh ?", ["E = 2 000 × 5 = 10 000 Wh.", "= 10 kWh."], "10 kWh.")],
          [("Un appareil puissant consomme toujours plus.", "Cela dépend aussi de la durée d’utilisation."), ("On confond W et Wh.", "Le watt mesure une puissance, le wattheure une énergie.")],
          [("Pourquoi les LED économisent-elles l’énergie ?", "Pour la même lumière, leur puissance est bien plus faible."), ("Que fait un appareil en veille ?", "Il consomme un peu d’énergie en permanence.")],
          [("Puissances courantes", [("une lampe LED", "environ 10 W"), ("un téléviseur", "environ 100 W"), ("un four", "environ 2 500 W"), ("un chargeur de téléphone", "environ 10 W".replace("10", "15")),
                                     ("une bouilloire", "environ 2 000 W".replace("2 000", "2 200")), ("un réfrigérateur", "environ 150 W"), ("un sèche-cheveux", "environ 1 500 W")],
            "Quelle puissance pour {k} ?", "Quel appareil a une puissance de {v} ?"),
           ("Grandeurs et unités", [("la puissance", "le watt"), ("l’énergie", "le joule ou le kilowattheure"), ("la tension", "le volt"), ("l’intensité", "l’ampère"), ("la durée", "la seconde ou l’heure"), ("la résistance", "l’ohm")],
            "Quelle unité pour {k} ?", "Quelle grandeur s’exprime en {v} ?"),
           ("Sécurité et installation", [("le disjoncteur", "coupe le courant en cas de surintensité"), ("le fusible", "fond si l’intensité est trop forte"), ("la prise de terre", "protège en cas de fuite de courant"),
                                         ("le compteur", "mesure l’énergie consommée"), ("la multiprise surchargée", "risque d’échauffement"), ("le disjoncteur différentiel", "protège les personnes des fuites")],
            "Quel est le rôle de {k} ?", "Quel élément {v} ?")],
          ["P = U × I.", "E = P × t.", "1 kWh = 1 000 Wh.", "La facture d’électricité est en kWh.",
           "Le disjoncteur coupe le courant en cas de surintensité.", "Le compteur mesure l’énergie consommée.", "Une lampe LED consomme moins qu’une lampe à incandescence."],
          [("Le watt mesure une énergie.", "Il mesure une puissance."), ("1 kWh = 100 Wh.", "1 kWh = 1 000 Wh."), ("P = U : I.", "P = U × I."), ("Un appareil en veille ne consomme rien.", "Il consomme un peu."),
           ("Le compteur mesure la tension.", "Il mesure l’énergie consommée.")],
          "l’énergie électrique", "energy", calc=f_puis),

        H("S", "genetique-adn-et-chromosomes", "ADN, gènes et chromosomes", "Génétique",
          "Les élèves relient les caractères héréditaires aux gènes portés par les chromosomes, décrivent la division cellulaire et la transmission lors de la reproduction sexuée.",
          "caractères héréditaires, ADN, gène, allèle, chromosome, caryotype, 23 paires, mitose, gamètes, fécondation, diversité génétique",
          "Les gènes sont portés par l’ADN des chromosomes", "Chaque cellule humaine contient 23 paires de chromosomes.",
          ["L’information génétique est portée par l’ADN, rangé dans le noyau sous forme de chromosomes. Un gène est une portion d’ADN qui détermine un caractère. Il existe plusieurs versions d’un gène : les allèles.",
           "Une cellule humaine contient 46 chromosomes (23 paires). Le caryotype est leur photographie rangée. Les chromosomes sexuels : XX chez la femme, XY chez l’homme.",
           "Lors de la mitose, une cellule donne deux cellules identiques. Les gamètes n’ont que 23 chromosomes. À la fécondation, l’enfant reçoit un chromosome de chaque paire de chaque parent."],
          [("Combien de chromosomes dans un spermatozoïde humain ?", ["Les gamètes ont un chromosome de chaque paire.", "46 : 2 = 23."], "23.")],
          [("Le gène et le chromosome sont la même chose.", "Un chromosome porte des centaines à des milliers de gènes."), ("Le père décide du sexe par sa volonté.", "Le spermatozoïde porte X ou Y au hasard.")],
          [("Pourquoi les frères et sœurs sont-ils différents ?", "Chaque gamète reçoit une combinaison différente de chromosomes."), ("Qu’est-ce que la trisomie 21 ?", "La présence de trois chromosomes 21 au lieu de deux.")],
          [("Vocabulaire", [("l’ADN", "molécule qui porte l’information génétique"), ("le gène", "portion d’ADN qui détermine un caractère"), ("l’allèle", "version d’un gène"), ("le chromosome", "ADN condensé dans le noyau"),
                            ("le caryotype", "photographie des chromosomes rangés par paires"), ("la mitose", "division donnant deux cellules identiques"), ("le gamète", "cellule reproductrice à 23 chromosomes")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Nombres", [("chromosomes d’une cellule de peau humaine", "46"), ("paires de chromosomes chez l’humain", "23"), ("chromosomes d’un ovule humain", "23 (un de chaque paire)"),
                        ("chromosomes sexuels d’une femme", "XX"), ("chromosomes sexuels d’un homme", "XY"), ("chromosomes 21 dans la trisomie 21", "3")],
            "Combien ou lesquels : {k} ?", None, ("12", "92")),
           ("Héréditaire ou non ?", {"des caractères héréditaires": ["le groupe sanguin", "la couleur naturelle des yeux", "la forme du lobe de l’oreille", "la mucoviscidose", "la couleur de peau d’origine", "le daltonisme"],
                                     "des caractères acquis": ["une cicatrice", "le bronzage", "parler l’anglais", "des muscles développés par le sport", "les cheveux teints", "savoir nager"]})],
          ["Les gènes sont portés par l’ADN.", "Une cellule humaine contient 46 chromosomes.", "Les gamètes ont 23 chromosomes.", "Un allèle est une version d’un gène.",
           "La mitose donne deux cellules identiques.", "Un homme a les chromosomes sexuels XY.", "Le bronzage n’est pas héréditaire."],
          [("Un gène et un chromosome sont la même chose.", "Un chromosome porte de nombreux gènes."), ("Les gamètes ont 46 chromosomes.", "Ils en ont 23."), ("Une femme a les chromosomes XY.", "Elle a XX."),
           ("Le bronzage est héréditaire.", "C’est un caractère acquis."), ("La mitose donne quatre cellules différentes.", "Elle donne deux cellules identiques.")],
          "la génétique", "living-things-and-ecosystems"),

        H("S", "evolution-et-selection-naturelle", "Évolution et sélection naturelle", "Évolution",
          "Les élèves expliquent la parenté des êtres vivants et l’évolution des espèces par la variation génétique, la sélection naturelle et la dérive au cours des temps géologiques.",
          "biodiversité, parenté, ancêtre commun, arbre phylogénétique, mutations, sélection naturelle, dérive génétique, fossiles, crises biologiques",
          "Les espèces évoluent au cours du temps", "La sélection naturelle favorise les individus les mieux adaptés à leur milieu.",
          ["Tous les êtres vivants sont apparentés : ils partagent des ancêtres communs. Les espèces qui partagent le plus de caractères sont les plus proches.",
           "Les mutations créent de nouveaux allèles. Dans un milieu donné, les individus porteurs d’un caractère avantageux survivent et se reproduisent davantage : c’est la sélection naturelle. Le hasard joue aussi (dérive génétique).",
           "Les fossiles montrent que des espèces sont apparues et ont disparu. Il y a eu cinq grandes crises, dont celle d’il y a 66 millions d’années."],
          [("Dans une ville polluée, les phalènes sombres sont plus nombreuses que les claires. Pourquoi ?", ["Sur les troncs noircis, les sombres sont moins visibles.", "Les oiseaux mangent surtout les claires."], "La sélection naturelle favorise les sombres.")],
          [("L’humain descend du chimpanzé.", "Ils ont un ancêtre commun, chacun a évolué de son côté."), ("Un individu évolue pendant sa vie.", "Ce sont les populations qui évoluent au fil des générations.")],
          [("Pourquoi des bactéries résistent-elles aux antibiotiques ?", "Les bactéries porteuses d’une mutation de résistance survivent et se multiplient."), ("Qui a proposé la sélection naturelle ?", "Charles Darwin, en 1859.")],
          [("Vocabulaire", [("la sélection naturelle", "les mieux adaptés laissent plus de descendants"), ("la mutation", "modification de l’ADN"), ("l’ancêtre commun", "espèce dont descendent plusieurs espèces"),
                            ("l’arbre phylogénétique", "représente les liens de parenté"), ("la dérive génétique", "changement dû au hasard"), ("la crise biologique", "disparition massive d’espèces"), ("l’espèce", "individus interféconds")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Exemples", [("les phalènes du bouleau", "sélection par la couleur selon la pollution"), ("les bactéries et les antibiotiques", "sélection des résistantes"), ("les pinsons des Galápagos", "becs adaptés aux graines disponibles"),
                         ("les insectes et les insecticides", "sélection des résistants"), ("la disparition des grands dinosaures", "crise biologique il y a 66 millions d’années"), ("les poissons des grottes", "perte des yeux au fil des générations")],
            "Que montre l’exemple {k} ?".replace("l’exemple {k}", "cet exemple : {k}"), None),
           ("Parenté", [("l’humain et le chimpanzé", "ancêtre commun il y a environ 7 millions d’années"), ("les oiseaux", "descendants de dinosaures"), ("la baleine", "mammifère dont les ancêtres vivaient sur terre"),
                        ("le cheval actuel", "ancêtres plus petits à plusieurs doigts"), ("les membres des vertébrés", "même plan d’organisation des os"), ("tous les êtres vivants", "faits de cellules et d’ADN")],
            "Que sait-on de {k} ?", None)],
          ["Les espèces évoluent au cours du temps.", "La sélection naturelle favorise les individus adaptés.", "Les mutations créent de nouveaux allèles.", "L’humain et le chimpanzé ont un ancêtre commun.",
           "Les oiseaux descendent de dinosaures.", "Les populations évoluent au fil des générations.", "Darwin a proposé la sélection naturelle."],
          [("L’humain descend du chimpanzé.", "Ils ont un ancêtre commun."), ("Un individu évolue pendant sa vie.", "Ce sont les populations qui évoluent."), ("Les espèces ne changent jamais.", "Elles évoluent."),
           ("Les mutations sont toujours voulues par l’organisme.", "Elles se produisent au hasard."), ("Les dinosaures ont disparu il y a 6 000 ans.", "Il y a 66 millions d’années.")],
          "l’évolution", "living-things-and-ecosystems"),

        H("S", "immunite-et-vaccination", "Microbes, immunité et vaccination", "Immunité",
          "Les élèves décrivent la contamination et l’infection, les réactions immunitaires (phagocytose, anticorps, lymphocytes) et le principe de la vaccination et des antibiotiques.",
          "micro-organismes, bactéries, virus, contamination, infection, barrières naturelles, phagocytose, anticorps, lymphocytes, mémoire immunitaire, vaccin, antibiotiques, hygiène",
          "Le vaccin prépare l’organisme à se défendre", "Les antibiotiques agissent sur les bactéries, pas sur les virus.",
          ["Les micro-organismes pathogènes (bactéries, virus) entrent par une blessure ou les muqueuses : c’est la contamination. S’ils se multiplient, c’est l’infection.",
           "La peau et les muqueuses sont des barrières. Les phagocytes avalent les microbes (phagocytose). Les lymphocytes B produisent des anticorps, les lymphocytes T détruisent les cellules infectées.",
           "Le vaccin contient un microbe inactivé ou une partie de microbe : l’organisme fabrique des cellules mémoire et réagit plus vite lors d’une vraie infection. Les antibiotiques tuent les bactéries mais n’ont aucun effet sur les virus."],
          [("Une personne a la grippe (un virus). Faut-il des antibiotiques ?", ["La grippe est causée par un virus.", "Les antibiotiques agissent seulement sur les bactéries."], "Non.")],
          [("Les antibiotiques soignent les rhumes.", "Le rhume est viral, les antibiotiques sont inefficaces."), ("Un vaccin soigne une maladie déjà présente.", "Il prévient la maladie en préparant l’immunité.")],
          [("Pourquoi l’abus d’antibiotiques est-il dangereux ?", "Il sélectionne des bactéries résistantes."), ("Que sont les anticorps ?", "Des molécules produites par les lymphocytes B qui neutralisent un microbe précis.")],
          [("Défenses", [("la peau", "barrière contre les microbes"), ("la phagocytose", "un globule blanc avale un microbe"), ("les anticorps", "neutralisent un microbe précis"), ("les lymphocytes B", "produisent les anticorps"),
                         ("les lymphocytes T", "détruisent les cellules infectées"), ("les cellules mémoire", "permettent une réaction plus rapide"), ("la fièvre", "réaction de l’organisme contre l’infection")],
            "Quel est le rôle de {k} ?", "Qu’est-ce qui {v} ?"),
           ("Bactérie ou virus ?", {"des maladies bactériennes": ["la tuberculose", "le tétanos", "l’angine bactérienne", "la salmonellose", "la coqueluche"], "des maladies virales": ["la grippe", "la rougeole", "le rhume", "la varicelle", "le sida", "la covid-19"]}),
           ("Prévention et soin", [("le vaccin", "prépare l’immunité avant l’infection"), ("l’antibiotique", "tue les bactéries"), ("l’antiseptique", "désinfecte une plaie"), ("le lavage des mains", "limite la contamination"),
                                   ("le masque", "limite la transmission par les gouttelettes"), ("le préservatif", "protège des infections sexuellement transmissibles"), ("la stérilisation", "détruit tous les microbes d’un objet")],
            "À quoi sert {k} ?", "Qu’est-ce qui {v} ?")],
          ["Les antibiotiques agissent sur les bactéries.", "Les antibiotiques n’agissent pas sur les virus.", "Le vaccin prépare l’organisme.", "Les lymphocytes B produisent des anticorps.",
           "La peau est une barrière contre les microbes.", "La grippe est causée par un virus.", "L’abus d’antibiotiques favorise les bactéries résistantes."],
          [("Les antibiotiques soignent la grippe.", "La grippe est virale."), ("Un vaccin soigne une maladie déjà présente.", "Il prévient la maladie."), ("Les anticorps sont produits par la peau.", "Par les lymphocytes B."),
           ("Le tétanos est une maladie virale.", "Il est bactérien."), ("Se laver les mains ne sert à rien.", "Cela limite la contamination.")],
          "l’immunité", "living-things-and-ecosystems"),

        H("S", "systeme-nerveux-et-reflexes", "Système nerveux, réflexes et hygiène de vie", "Système nerveux",
          "Les élèves décrivent le trajet du message nerveux, distinguent réflexe et mouvement volontaire et relient sommeil, drogues et écrans au fonctionnement du cerveau.",
          "récepteur sensoriel, nerf sensitif, centre nerveux, nerf moteur, effecteur, neurones, synapse, réflexe, mouvement volontaire, sommeil, substances psychoactives",
          "Récepteur → centre nerveux → muscle", "Le message suit un nerf sensitif puis un nerf moteur. Un réflexe passe par la moelle épinière.",
          ["Un message nerveux part d’un récepteur (œil, peau), suit un nerf sensitif jusqu’à un centre nerveux (cerveau ou moelle épinière), puis un nerf moteur jusqu’à un effecteur (muscle).",
           "Le système nerveux est fait de neurones qui communiquent par des synapses, à l’aide de neurotransmetteurs. Un réflexe (retirer la main d’une plaque chaude) est commandé par la moelle épinière.",
           "Le sommeil permet au cerveau de récupérer et de mémoriser. L’alcool, le cannabis ou la nicotine perturbent les synapses et ralentissent les réactions."],
          [("On touche une casserole brûlante et on retire la main avant de sentir la douleur. Pourquoi ?", ["Le message va de la peau à la moelle épinière.", "La moelle commande directement le muscle."], "C’est un réflexe médullaire.")],
          [("Le cerveau commande tous les mouvements.", "Les réflexes sont commandés par la moelle épinière."), ("L’alcool rend plus rapide.", "Il ralentit le temps de réaction.")],
          [("Pourquoi éviter les écrans avant de dormir ?", "La lumière bleue retarde l’endormissement."), ("Que se passe-t-il si la moelle épinière est coupée ?", "Les messages ne passent plus entre le cerveau et les membres : paralysie.")],
          [("Trajet du message", [("le récepteur sensoriel", "capte une information"), ("le nerf sensitif", "conduit le message vers le centre nerveux"), ("le centre nerveux", "élabore la réponse"),
                                  ("le nerf moteur", "conduit le message vers le muscle"), ("l’effecteur", "le muscle qui réagit"), ("la synapse", "zone de contact entre deux neurones"), ("le neurotransmetteur", "molécule qui passe le message à la synapse")],
            "Quel est le rôle de {k} ?", "Qu’est-ce qui {v} ?"),
           ("Réflexe ou volontaire ?", {"des réflexes": ["retirer la main d’une plaque chaude", "cligner des yeux devant un objet qui arrive", "le réflexe du genou", "la pupille qui se ferme à la lumière", "éternuer", "tousser quand on avale de travers"],
                                       "des mouvements volontaires": ["écrire son prénom", "lever la main en classe", "tirer un penalty", "jouer du piano", "faire ses lacets", "tourner une page"]}),
           ("Hygiène de vie", [("le sommeil", "fixe les apprentissages"), ("l’alcool", "allonge le temps de réaction"), ("le cannabis", "perturbe la mémoire et la concentration"), ("la nicotine", "crée une forte dépendance"),
                               ("les écrans le soir", "retardent l’endormissement"), ("l’activité physique", "améliore le sommeil et l’humeur"), ("le casque à fort volume", "abîme les cellules de l’oreille")],
            "Quel effet a {k} ?", "Qu’est-ce qui {v} ?")],
          ["Le message nerveux va du récepteur au centre nerveux.", "Un réflexe passe par la moelle épinière.", "Les neurones communiquent par des synapses.", "Le sommeil aide la mémoire.",
           "L’alcool ralentit les réactions.", "Le nerf moteur conduit le message vers le muscle.", "Écrire est un mouvement volontaire."],
          [("Le cerveau commande tous les réflexes.", "La moelle épinière commande les réflexes."), ("L’alcool rend plus rapide.", "Il ralentit les réactions."), ("Le nerf sensitif va vers le muscle.", "C’est le nerf moteur."),
           ("Les écrans le soir aident à dormir.", "Ils retardent l’endormissement."), ("Éternuer est un mouvement volontaire.", "C’est un réflexe.")],
          "le système nerveux", "living-things-and-ecosystems"),
    ]
