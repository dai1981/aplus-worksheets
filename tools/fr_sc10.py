# -*- coding: utf-8 -*-
"""France / Physique-chimie et SVT : seconde générale et technologique"""
import math
from fr_sci import H, nq, num

NA = 6.02e23


def f_conc(R):
    k = R.choice(["Cm", "Cm", "m", "dil", "dilV", "rho"])
    if k == "Cm":
        m, V = R.choice([(5, 0.25), (2, 0.1), (12, 0.5), (0.5, 0.05), (30, 2), (9, 0.2), (1.5, 0.25)])
        return nq("On dissout %s g de soluté pour préparer %s L de solution. Quelle est la concentration en masse ?" % (num(m), num(V)), m / V,
                  [m * V, V / m, m / V / 1000], "g/L", "Cm = m : V = %s : %s = %s g/L." % (num(m), num(V), num(m / V)))
    if k == "m":
        c, V = R.choice([(9, 0.5), (20, 0.25), (50, 0.1), (2.5, 2), (100, 0.05)])
        return nq("Quelle masse de soluté faut-il peser pour préparer %s L d’une solution à %s g/L ?" % (num(V), num(c)), c * V, [c / V, V / c, c + V], "g",
                  "m = Cm × V = %s × %s = %s g." % (num(c), num(V), num(c * V)))
    if k == "dil":
        c0, V0, V1 = R.choice([(10, 10, 100), (50, 20, 200), (2, 5, 50), (100, 25, 500), (8, 50, 200)])
        return nq("On prélève %s mL d’une solution mère à %s g/L et on complète à %s mL avec de l’eau. Concentration de la solution fille ?" % (num(V0), num(c0), num(V1)), c0 * V0 / V1,
                  [c0 * V1 / V0, c0, c0 * V0], "g/L", "Cf = Cm × V0 : Vf = %s × %s : %s = %s g/L." % (num(c0), num(V0), num(V1), num(c0 * V0 / V1)))
    if k == "dilV":
        c0, c1, V1 = R.choice([(10, 1, 100), (20, 2, 50), (5, 0.5, 200), (12, 3, 100), (50, 5, 250)])
        return nq("On veut %s mL de solution à %s g/L à partir d’une solution mère à %s g/L. Quel volume de solution mère faut-il prélever ?" % (num(V1), num(c1), num(c0)), c1 * V1 / c0,
                  [c0 * V1 / c1, V1, c1 * V1], "mL", "V0 = Cf × Vf : Cm = %s × %s : %s = %s mL. Facteur de dilution : %s." % (num(c1), num(V1), num(c0), num(c1 * V1 / c0), num(c0 / c1)))
    m, V = R.choice([(27, 10), (158, 20), (39.5, 50), (79, 100), (226, 20)])
    return nq("Un échantillon de %s g occupe %s mL. Quelle est sa masse volumique en g/mL ?" % (num(m), num(V)), m / V, [V / m, m * V, m - V], "g/mL", "ρ = m : V = %s g/mL." % num(m / V))


def f_atome(R):
    els = [("carbone", "C", 6, 12), ("oxygène", "O", 8, 16), ("sodium", "Na", 11, 23), ("aluminium", "Al", 13, 27), ("chlore", "Cl", 17, 35), ("fer", "Fe", 26, 56), ("azote", "N", 7, 14),
           ("magnésium", "Mg", 12, 24), ("soufre", "S", 16, 32), ("calcium", "Ca", 20, 40)]
    n, s, Z, A = R.choice(els)
    k = R.choice(["N", "N", "e", "nuc", "mass"])
    if k == "N":
        return nq("Combien de neutrons contient le noyau de l’atome de %s %s (Z = %d, A = %d) ?" % (n, s, Z, A), A - Z, [A, Z, A + Z], "", "N = A − Z = %d − %d = %d." % (A, Z, A - Z))
    if k == "e":
        return nq("Combien d’électrons possède l’atome de %s (Z = %d, A = %d) ?" % (n, Z, A), Z, [A, A - Z, Z + 2], "", "L’atome est neutre : autant d’électrons que de protons, soit %d." % Z)
    if k == "nuc":
        return nq("Combien de nucléons contient le noyau de %s (Z = %d, A = %d) ?" % (n, Z, A), A, [Z, A - Z, A + Z], "", "Le nombre de nucléons est A = %d." % A)
    mA = A * 1.67e-27
    return nq("La masse d’un nucléon est environ 1,67 × 10⁻²⁷ kg. Quelle est la masse approchée d’un atome de %s (A = %d) ?" % (n, A), mA, [1.67e-27 * Z, 1.67e-27, mA * 1000], "kg",
              "m ≈ A × m(nucléon) = %d × 1,67 × 10⁻²⁷ = %s kg (les électrons sont négligeables)." % (A, num(mA)))


def f_mole(R):
    sp = [("d’eau H₂O", 18), ("de dioxyde de carbone CO₂", 44), ("de glucose C₆H₁₂O₆", 180), ("de chlorure de sodium NaCl", 58.5), ("de méthane CH₄", 16), ("de fer Fe", 56), ("d’éthanol C₂H₆O", 46)]
    nm, M = R.choice(sp)
    k = R.choice(["n", "n", "m", "N", "Nn"])
    if k == "n":
        m = R.choice([36, 9, 88, 90, 117, 32, 112, 23, 4.5])
        return nq("Quelle quantité de matière contiennent %s g %s (M = %s g/mol) ?" % (num(m), nm, num(M)), m / M, [m * M, M / m, m / M * NA], "mol", "n = m : M = %s : %s = %s mol." % (num(m), num(M), num(m / M)))
    if k == "m":
        n = R.choice([0.5, 2, 0.1, 0.25, 3, 1.5])
        return nq("Quelle masse correspond à %s mol %s (M = %s g/mol) ?" % (num(n), nm, num(M)), n * M, [n / M, M / n, n + M], "g", "m = n × M = %s × %s = %s g." % (num(n), num(M), num(n * M)))
    if k == "N":
        n = R.choice([2, 0.5, 0.1, 3, 0.25])
        return nq("Combien d’entités contiennent %s mol ? (NA = 6,02 × 10²³ mol⁻¹)" % num(n), n * NA, [n / NA, NA, n * NA * 10], "", "N = n × NA = %s × 6,02 × 10²³ = %s." % (num(n), num(n * NA)))
    N = R.choice([1.204e24, 3.01e23, 6.02e22, 1.806e24, 6.02e24])
    return nq("Un échantillon contient %s molécules. Quelle est sa quantité de matière ? (NA = 6,02 × 10²³ mol⁻¹)" % num(N), N / NA, [N * NA, NA / N, N / NA * 10], "mol",
              "n = N : NA = %s : 6,02 × 10²³ = %s mol." % (num(N), num(N / NA)))


def f_lim(R):
    # 2 H2 + O2 -> 2 H2O ; C + O2 -> CO2 ; CH4 + 2 O2 -> CO2 + 2 H2O
    k = R.choice(["h2", "h2", "ch4", "c"])
    if k == "h2":
        a, b = R.choice([(4, 3), (6, 2), (2, 2), (10, 4), (8, 5), (3, 3), (5, 1), (12, 5), (7, 4), (4, 4), (9, 2)])
        prod = min(a, 2 * b)
        lim = "H₂" if a < 2 * b else ("O₂" if a > 2 * b else "aucun (proportions stœchiométriques)")
        return nq("2 H₂ + O₂ → 2 H₂O. On mélange %d mol de H₂ et %d mol de O₂. Quelle quantité d’eau peut-on obtenir au maximum ?" % (a, b), prod, [a + b, 2 * b if 2 * b != prod else b, a / 2], "mol",
                  "Il faut 2 mol de H₂ pour 1 mol de O₂. Réactif limitant : %s. On obtient %d mol d’eau." % (lim, prod))
    if k == "ch4":
        a, b = R.choice([(1, 4), (2, 2), (3, 4), (2, 5), (1, 1), (4, 6), (5, 8), (3, 10), (2, 8)])
        x = min(a, b / 2)
        return nq("CH₄ + 2 O₂ → CO₂ + 2 H₂O. On brûle %d mol de méthane avec %d mol de dioxygène. Quelle quantité de CO₂ se forme au maximum ?" % (a, b), x, [a, b, 2 * x, a + b], "mol",
                  "Avancement maximal : min(%d ; %d : 2) = %s mol, donc %s mol de CO₂." % (a, b, num(x), num(x)))
    a, b = R.choice([(3, 2), (1, 4), (5, 5), (2, 6), (4, 1), (7, 3), (2, 9), (6, 4)])
    return nq("C + O₂ → CO₂. On fait réagir %d mol de carbone et %d mol de dioxygène. Quelle quantité de CO₂ obtient-on ?" % (a, b), min(a, b), [a + b, max(a, b), abs(a - b) if abs(a - b) != min(a, b) else a * b], "mol",
              "Les coefficients sont 1 : 1. Le réactif limitant est celui en plus petite quantité : %d mol de CO₂." % min(a, b))


def f_mvt(R):
    k = R.choice(["v", "v", "kmh", "d", "P"])
    if k == "v":
        d, t = R.choice([(0.12, 0.04), (0.3, 0.1), (5, 2), (100, 9.8), (1.8, 0.6), (42.2e3, 7200)])
        return nq("Un mobile parcourt %s m en %s s. Quelle est la valeur de sa vitesse moyenne ?" % (num(d), num(t)), d / t, [d * t, t / d, d / t * 3.6], "m/s", "v = d : Δt = %s m/s." % num(d / t))
    if k == "kmh":
        v = R.choice([15, 25, 30, 8, 12.5, 40])
        return nq("Convertis %s m/s en km/h." % num(v), v * 3.6, [v / 3.6, v * 60, v * 1000], "km/h", "%s × 3,6 = %s km/h." % (num(v), num(v * 3.6)))
    if k == "d":
        v, t = R.choice([(340, 0.5), (3e8, 1.28), (12, 15), (8, 0.25), (1500, 0.4)])
        return nq("Un signal se déplace à %s m/s pendant %s s. Quelle distance parcourt-il ?" % (num(v), num(t)), v * t, [v / t, t / v, v + t], "m", "d = v × Δt = %s m." % num(v * t))
    m = R.choice([0.2, 1.5, 70, 0.45, 12, 1000])
    return nq("Quelle est la valeur du poids d’un objet de %s kg sur Terre ? (g = 9,81 N/kg)" % num(m), m * 9.81, [m / 9.81, m, m * 98.1], "N", "P = m × g = %s × 9,81 = %s N." % (num(m), num(m * 9.81)))


def f_onde(R):
    k = R.choice(["f", "f", "T", "lam", "snell", "nv"])
    if k == "f":
        T = R.choice([0.002, 0.005, 0.01, 0.0025, 0.02, 0.001])
        return nq("Un signal sonore a une période de %s s. Quelle est sa fréquence ?" % num(T), 1 / T, [T, 1 / T / 10, T * 1000], "Hz", "f = 1 : T = 1 : %s = %s Hz." % (num(T), num(1 / T)))
    if k == "T":
        f = R.choice([440, 1000, 50, 200, 2500, 125])
        return nq("Quelle est la période d’un son de fréquence %s Hz ?" % num(f), 1 / f, [f, 1 / f * 1000, 2 / f], "s", "T = 1 : f = %s s." % num(1 / f))
    if k == "lam":
        f = R.choice([340, 680, 170, 100, 1700, 85])
        return nq("Quelle est la longueur d’onde d’un son de %s Hz dans l’air (v = 340 m/s) ?" % num(f), 340 / f, [f / 340, 340 * f, 340 / f / 2], "m", "λ = v : f = 340 : %s = %s m." % (num(f), num(340 / f)))
    if k == "snell":
        i1, n2 = R.choice([(30, 1.33), (45, 1.5), (60, 1.33), (20, 1.5), (40, 1.33), (50, 1.5)])
        r = math.degrees(math.asin(math.sin(math.radians(i1)) / n2))
        return nq("Un rayon passe de l’air (n = 1) dans un milieu d’indice %s avec un angle d’incidence de %d°. Quel est l’angle de réfraction ?" % (num(n2), i1), round(r, 1),
                  [round(i1 * n2, 1), round(i1 / n2, 1), round(90 - r, 1)], "°", "sin i₂ = sin %d° : %s, donc i₂ ≈ %s°." % (i1, num(n2), num(round(r, 1))))
    n = R.choice([1.33, 1.5, 2.42, 1.2])
    return nq("Quelle est la vitesse de la lumière dans un milieu d’indice %s ? (c = 3,00 × 10⁸ m/s)" % num(n), 3e8 / n, [3e8 * n, 3e8, n / 3e8], "m/s", "v = c : n = %s m/s." % num(3e8 / n))


def f_elec(R):
    k = R.choice(["U", "I", "R", "P", "ctn"])
    if k == "U":
        r, i = R.choice([(150, 0.02), (1000, 0.0045), (47, 0.1), (330, 0.015), (2200, 0.002)])
        return nq("Un conducteur ohmique de %s Ω est traversé par %s A. Tension à ses bornes ?" % (num(r), num(i)), r * i, [r / i, i / r, r + i], "V", "U = R × I = %s V." % num(r * i))
    if k == "I":
        u, r = R.choice([(5, 220), (12, 470), (9, 1000), (3.3, 100), (6, 150)])
        return nq("Une tension de %s V est appliquée à un conducteur ohmique de %s Ω. Intensité ?" % (num(u), num(r)), u / r, [u * r, r / u, u / r * 1000], "A", "I = U : R = %s A." % num(u / r))
    if k == "R":
        u, i = R.choice([(4, 0.02), (10, 0.05), (6, 0.012), (2.2, 0.01), (9, 0.03)])
        return nq("La caractéristique d’un dipôle passe par U = %s V pour I = %s A. S’il est ohmique, que vaut R ?" % (num(u), num(i)), u / i, [u * i, i / u, u - i], "Ω", "R = U : I = %s Ω." % num(u / i))
    if k == "P":
        u, i = R.choice([(230, 0.5), (12, 2), (5, 0.8), (230, 6), (9, 0.3)])
        return nq("Un appareil fonctionne sous %s V et consomme %s A. Quelle est sa puissance ?" % (num(u), num(i)), u * i, [u / i, i / u, u + i], "W", "P = U × I = %s W." % num(u * i))
    t = R.choice([(20, 10000), (40, 5000), (60, 2500), (0, 20000), (80, 1250)])
    return nq("Une thermistance (CTN) vaut %s Ω à %d °C et sa résistance est divisée par 2 tous les 20 °C. Combien vaut-elle à %d °C ?" % (num(t[1]), t[0], t[0] + 20), t[1] / 2, [t[1] * 2, t[1], t[1] / 4], "Ω",
              "Quand la température augmente de 20 °C, R est divisée par 2 : %s Ω." % num(t[1] / 2))


def f_freq(R):
    k = R.choice(["f", "f", "hw", "pct"])
    if k == "f":
        a, n = R.choice([(30, 200), (45, 150), (12, 80), (90, 300), (64, 400), (18, 120), (50, 500), (36, 240), (120, 400)])
        return nq("Dans une population de %d individus, on compte %d allèles du gène, dont %d allèles B. Quelle est la fréquence de l’allèle B ?" % (n // 2, n, a), a / n,
                  [a / (n // 2), n / a, 1 - a / n], "", "f(B) = %d : %d = %s." % (a, n, num(a / n)))
    if k == "pct":
        p0, d = R.choice([(0.6, 0.1), (0.3, 0.05), (0.8, 0.2), (0.5, 0.15), (0.25, 0.1), (0.1, 0.3), (0.4, 0.25)])
        return nq("La fréquence d’un allèle passe de %s à %s en dix générations. De combien a-t-elle varié ?" % (num(p0), num(p0 + d)), d, [p0 + d, p0, d * 10], "", "%s − %s = %s." % (num(p0 + d), num(p0), num(d)))
    p = R.choice([0.7, 0.6, 0.9, 0.8, 0.55, 0.35, 0.95, 0.15])
    return nq("Un gène a deux allèles. La fréquence de l’allèle A est %s. Quelle est celle de l’allèle a ?" % num(p), round(1 - p, 2), [p, 1 + p, p / 2], "", "f(a) = 1 − %s = %s." % (num(p), num(round(1 - p, 2))))


def UNITS(grade):
    return [
        H("P", "corps-purs-melanges-et-solutions", "Corps purs, mélanges et solutions aqueuses", "Solutions aqueuses",
          "Les élèves identifient corps purs et mélanges, déterminent une masse volumique, préparent une solution par dissolution ou dilution et calculent une concentration en masse.",
          "corps pur, mélange, composition de l’air, masse volumique, solution, soluté, solvant, concentration en masse, dissolution, dilution, dosage par étalonnage",
          "Cm = m(soluté) : V(solution)", "Lors d’une dilution, la masse de soluté se conserve : Cm × V0 = Cf × Vf.",
          ["Un corps pur ne contient qu’une espèce chimique, il a une température de changement d’état fixe. Un mélange en contient plusieurs. L’air : 78 % de N₂, 21 % de O₂.",
           "Une solution aqueuse contient un soluté dissous dans l’eau (solvant). Concentration en masse : Cm = m : V, en g/L. À ne pas confondre avec la masse volumique ρ = m : V de la solution.",
           "Dilution : on prélève un volume V0 de solution mère (pipette jaugée), on complète à Vf (fiole jaugée). La masse de soluté se conserve : Cm × V0 = Cf × Vf. Le facteur de dilution est F = Cm : Cf = Vf : V0."],
          [("Préparer 100 mL à 2 g/L à partir d’une solution à 10 g/L.", ["F = 10 : 2 = 5.", "V0 = 100 : 5 = 20 mL."], "Prélever 20 mL et compléter à 100 mL.")],
          [("On confond concentration en masse et masse volumique.", "Cm concerne le soluté, ρ concerne toute la solution."), ("On remplit la fiole jaugée jusqu’en haut.", "On complète jusqu’au trait de jauge, bas du ménisque sur le trait.")],
          [("Qu’est-ce qu’un dosage par étalonnage ?", "On compare une grandeur (couleur, absorbance) à celle de solutions de concentrations connues."), ("Quelle verrerie pour un volume précis ?", "La pipette jaugée et la fiole jaugée.")],
          [("Verrerie", [("la fiole jaugée", "contient un volume précis"), ("la pipette jaugée", "prélève un volume précis"), ("l’éprouvette graduée", "mesure un volume avec peu de précision"), ("le bécher", "récipient, pas pour mesurer"),
                         ("la balance électronique", "mesure une masse"), ("la pissette", "contient de l’eau distillée"), ("la propipette", "aspire le liquide dans la pipette")],
            "À quoi sert {k} ?", "Quelle verrerie {v} ?"),
           ("Corps pur ou mélange ?", {"des corps purs": ["l’eau distillée", "le dioxygène", "le cuivre", "le saccharose", "le chlorure de sodium solide", "le diazote"],
                                       "des mélanges": ["l’air", "l’eau minérale", "le sérum physiologique", "le laiton", "l’essence", "le vinaigre"]}),
           ("Vocabulaire", [("la concentration en masse", "masse de soluté par litre de solution"), ("la masse volumique", "masse d’un litre de solution"), ("le facteur de dilution", "rapport Cm : Cf"), ("la solution mère", "solution de départ, la plus concentrée"),
                            ("la solution fille", "solution obtenue après dilution"), ("le soluté", "espèce dissoute"), ("la solubilité", "concentration maximale possible")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Cm = m : V.", "Lors d’une dilution, la masse de soluté se conserve.", "L’air est un mélange.", "La fiole jaugée contient un volume précis.",
           "Un corps pur a une température de fusion fixe.", "Le facteur de dilution est Cm : Cf.", "Une solution fille est moins concentrée que la solution mère."],
          [("La concentration et la masse volumique sont la même chose.", "Cm concerne le soluté, ρ la solution."), ("Diluer augmente la concentration.", "Diluer la diminue."), ("L’air est un corps pur.", "C’est un mélange."),
           ("Le bécher sert à mesurer un volume précis.", "On utilise la fiole jaugée."), ("La masse de soluté diminue lors d’une dilution.", "Elle se conserve.")],
          "les solutions", "matter", calc=f_conc),

        H("P", "atome-et-tableau-periodique", "L’atome et le tableau périodique", "Atome et tableau périodique",
          "Les élèves décrivent le noyau (Z protons, A nucléons), le cortège électronique et sa configuration, relient la position dans le tableau périodique à la stabilité des gaz nobles et à la formation des ions.",
          "noyau, protons, neutrons, notation ᴬZX, isotopes, électrons, configuration électronique, couche de valence, familles, gaz nobles, ions monoatomiques",
          "Z = nombre de protons, A = nombre de nucléons", "Les atomes gagnent ou perdent des électrons pour ressembler au gaz noble le plus proche.",
          ["Le noyau contient Z protons et N = A − Z neutrons. Deux isotopes ont le même Z mais un A différent. L’atome, neutre, a Z électrons. Il est environ 100 000 fois plus grand que son noyau.",
           "Configuration électronique : 1s² 2s² 2p⁶ 3s² 3p⁶… Les électrons de la dernière couche (valence) déterminent les propriétés chimiques.",
           "Dans le tableau, les éléments d’une même colonne forment une famille (alcalins, halogènes, gaz nobles). Les gaz nobles ont une couche de valence pleine : ils sont stables. Na perd un électron (Na⁺), Cl en gagne un (Cl⁻)."],
          [("Configuration électronique du sodium (Z = 11) ?", ["On remplit 1s, 2s, 2p puis 3s.", "1s² 2s² 2p⁶ 3s¹."], "1s² 2s² 2p⁶ 3s¹ : un électron de valence, il forme Na⁺.")],
          [("A est le nombre de neutrons.", "A est le nombre de nucléons, N = A − Z."), ("Les isotopes ont des Z différents.", "Ils ont le même Z, des nombres de neutrons différents.")],
          [("Pourquoi l’hélium ne réagit-il presque pas ?", "Sa couche de valence est pleine (1s²) : c’est un gaz noble."), ("Pourquoi les halogènes forment-ils des ions X⁻ ?", "Ils ont 7 électrons de valence et en gagnent un.")],
          [("Familles", [("le lithium", "alcalin"), ("le sodium", "alcalin"), ("le potassium", "alcalin"), ("le fluor", "halogène"), ("le chlore", "halogène"), ("le brome", "halogène"),
                         ("l’hélium", "gaz noble"), ("le néon", "gaz noble"), ("l’argon", "gaz noble"), ("le magnésium", "alcalino-terreux"), ("le calcium", "alcalino-terreux")],
            "À quelle famille appartient {k} ?", None, ("métal de transition",)),
           ("Ions monoatomiques", [("le sodium", "Na⁺"), ("le chlore", "Cl⁻"), ("le magnésium", "Mg²⁺"), ("l’oxygène", "O²⁻"), ("l’aluminium", "Al³⁺"), ("le potassium", "K⁺"), ("le fluor", "F⁻"), ("le calcium", "Ca²⁺"), ("le soufre", "S²⁻")],
            "Quel ion forme {k} ?", "Quel élément donne l’ion {v} ?"),
           ("Vocabulaire", [("le numéro atomique Z", "nombre de protons"), ("le nombre de masse A", "nombre de nucléons"), ("les isotopes", "même Z, A différents"), ("la couche de valence", "dernière couche occupée"),
                            ("un gaz noble", "couche de valence complète"), ("un nucléon", "proton ou neutron"), ("un électron de valence", "électron de la dernière couche")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Z est le nombre de protons.", "N = A − Z.", "Les isotopes ont le même Z.", "Les gaz nobles ont une couche de valence pleine.",
           "Le sodium forme l’ion Na⁺.", "Le chlore est un halogène.", "L’atome est beaucoup plus grand que son noyau."],
          [("A est le nombre de neutrons.", "A est le nombre de nucléons."), ("Les isotopes ont des Z différents.", "Ils ont le même Z."), ("Le chlore forme l’ion Cl⁺.", "Il forme Cl⁻."),
           ("Les gaz nobles réagissent très facilement.", "Ils sont très stables."), ("Le noyau a la même taille que l’atome.", "Il est 100 000 fois plus petit.")],
          "l’atome", "matter", calc=f_atome),

        H("P", "la-quantite-de-matiere", "La quantité de matière : la mole", "La mole",
          "Les élèves définissent la mole et la constante d’Avogadro, calculent des quantités de matière à partir d’une masse et d’une masse molaire, et dénombrent des entités.",
          "entité chimique, mole, constante d’Avogadro NA, quantité de matière n, masse molaire M, n = m : M, N = n × NA",
          "n = m : M et N = n × NA", "Une mole contient 6,02 × 10²³ entités.",
          ["Une mole est un paquet de 6,02 × 10²³ entités (atomes, molécules, ions). NA = 6,02 × 10²³ mol⁻¹ est la constante d’Avogadro.",
           "La quantité de matière n (en mol) se calcule : n = N : NA à partir d’un nombre d’entités, ou n = m : M à partir d’une masse.",
           "La masse molaire M (g/mol) d’une molécule est la somme des masses molaires de ses atomes : M(H₂O) = 2 × 1 + 16 = 18 g/mol."],
          [("Combien de moles dans 54 g d’eau ?", ["M(H₂O) = 18 g/mol.", "n = 54 : 18 = 3."], "3 mol.")],
          [("On multiplie la masse par la masse molaire.", "n = m : M."), ("Une mole de fer et une mole d’eau ont la même masse.", "Elles ont le même nombre d’entités, pas la même masse.")],
          [("Pourquoi utiliser la mole ?", "Les entités sont si petites qu’on les compte par paquets de 6,02 × 10²³."), ("Comment trouver M(CO₂) ?", "M(C) + 2 × M(O) = 12 + 2 × 16 = 44 g/mol.")],
          [("Masses molaires", [("H₂O", "18 g/mol"), ("CO₂", "44 g/mol"), ("O₂", "32 g/mol"), ("CH₄", "16 g/mol"), ("NaCl", "58,5 g/mol"), ("C₆H₁₂O₆", "180 g/mol"), ("N₂", "28 g/mol"), ("C₂H₆O", "46 g/mol")],
            "Quelle est la masse molaire de {k} ?", "Quelle espèce a une masse molaire de {v} ?"),
           ("Grandeurs", [("la quantité de matière n", "s’exprime en mol"), ("la masse molaire M", "s’exprime en g/mol"), ("la masse m", "s’exprime en g"), ("la constante d’Avogadro NA", "vaut 6,02 × 10²³ mol⁻¹"),
                          ("le nombre d’entités N", "n’a pas d’unité"), ("le volume V", "s’exprime en L"), ("la concentration en quantité de matière c", "s’exprime en mol/L")],
            "Que sais-tu de {k} ?", "Quelle grandeur {v} ?"),
           ("Relations", [("la quantité de matière à partir de la masse", "n = m : M"), ("la masse à partir de la quantité de matière", "m = n × M"), ("le nombre d’entités à partir de la quantité de matière", "N = n × NA"), ("la quantité de matière à partir du nombre d’entités", "n = N : NA"),
                          ("la masse molaire d’une molécule", "somme des masses molaires des atomes"), ("concentration en quantité de matière", "c = n : V")],
            "Quelle relation donne {k} ?", None)],
          ["Une mole contient 6,02 × 10²³ entités.", "n = m : M.", "N = n × NA.", "M(H₂O) = 18 g/mol.",
           "La masse molaire s’exprime en g/mol.", "La masse molaire d’une molécule est la somme de celles de ses atomes.", "M(CO₂) = 44 g/mol."],
          [("n = m × M.", "n = m : M."), ("Une mole de fer et une mole d’eau ont la même masse.", "Elles ont le même nombre d’entités."), ("NA = 6,02 × 10²³ g.", "NA s’exprime en mol⁻¹."),
           ("M(H₂O) = 10 g/mol.", "M(H₂O) = 18 g/mol."), ("La masse molaire s’exprime en mol/g.", "En g/mol.")],
          "la quantité de matière", "matter", calc=f_mole),

        H("P", "transformations-chimiques", "Transformations chimiques et réactif limitant", "Transformations chimiques",
          "Les élèves modélisent une transformation chimique par une équation de réaction ajustée, identifient le réactif limitant et distinguent transformations physique, chimique et nucléaire.",
          "réactifs, produits, équation de réaction, coefficients stœchiométriques, réactif limitant, mélange stœchiométrique, synthèse, transformation endothermique et exothermique",
          "Le réactif limitant est entièrement consommé", "L’équation ajustée donne les proportions dans lesquelles les réactifs réagissent.",
          ["Une équation de réaction indique les réactifs, les produits et les coefficients stœchiométriques. Elle conserve les éléments et les charges.",
           "Le réactif limitant est celui qui disparaît en premier : il fixe la quantité de produit formée. Si les réactifs sont dans les proportions de l’équation, le mélange est stœchiométrique.",
           "Une transformation physique change l’état, une transformation chimique change les espèces, une transformation nucléaire change les noyaux. Une transformation exothermique libère de l’énergie."],
          [("2 H₂ + O₂ → 2 H₂O, avec 6 mol de H₂ et 2 mol de O₂. Limitant ?", ["2 mol de O₂ demandent 4 mol de H₂.", "Il reste 2 mol de H₂."], "O₂ est limitant, on forme 4 mol d’eau.")],
          [("Le réactif limitant est celui en plus petite quantité.", "Il faut tenir compte des coefficients."), ("Les coefficients s’ajoutent aux indices.", "On ne modifie jamais les indices d’une formule.")],
          [("Une combustion est-elle exothermique ?", "Oui, elle libère de l’énergie sous forme de chaleur."), ("Qu’est-ce qu’une espèce spectatrice ?", "Une espèce présente qui ne réagit pas et n’apparaît pas dans l’équation.")],
          [("Type de transformation", [("la fusion de la glace", "physique"), ("la combustion du bois", "chimique"), ("la fission de l’uranium", "nucléaire"), ("la dissolution du sucre", "physique"),
                                       ("la rouille du fer", "chimique"), ("la fusion de l’hydrogène dans le Soleil", "nucléaire"), ("la vaporisation de l’eau", "physique"), ("la cuisson d’un œuf", "chimique")],
            "Quel type de transformation est {k} ?", None, ("biologique",)),
           ("Équations ajustées", [("combustion du carbone", "C + O₂ → CO₂"), ("formation de l’eau", "2 H₂ + O₂ → 2 H₂O"), ("combustion du méthane", "CH₄ + 2 O₂ → CO₂ + 2 H₂O"),
                                   ("acide et fer", "Fe + 2 H⁺ → Fe²⁺ + H₂"), ("précipitation de l’hydroxyde de cuivre", "Cu²⁺ + 2 HO⁻ → Cu(OH)₂"), ("combustion du propane", "C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O")],
            "Quelle équation ajustée correspond à {k} ?", "Que décrit l’équation {v} ?"),
           ("Vocabulaire", [("le réactif limitant", "entièrement consommé"), ("le mélange stœchiométrique", "réactifs dans les proportions de l’équation"), ("l’espèce spectatrice", "présente mais ne réagit pas"),
                            ("exothermique", "libère de l’énergie thermique"), ("endothermique", "absorbe de l’énergie thermique"), ("la synthèse", "fabrication d’une espèce chimique"), ("le coefficient stœchiométrique", "nombre placé devant une formule")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Le réactif limitant est entièrement consommé.", "Une équation conserve les éléments.", "Une combustion est exothermique.", "La fission de l’uranium est une transformation nucléaire.",
           "On ne modifie jamais les indices pour ajuster.", "La dissolution est une transformation physique.", "Une espèce spectatrice ne réagit pas."],
          [("Le réactif limitant est toujours en plus petite quantité.", "Il faut tenir compte des coefficients."), ("On ajuste en changeant les indices.", "On change les coefficients."), ("Une combustion absorbe de l’énergie.", "Elle en libère."),
           ("La rouille est une transformation physique.", "C’est une transformation chimique."), ("Une équation peut créer des atomes.", "Elle conserve les éléments.")],
          "les transformations chimiques", "matter", calc=f_lim),

        H("P", "transformations-nucleaires", "Transformations nucléaires", "Transformations nucléaires",
          "Les élèves identifient isotopes et transformations nucléaires (fission, fusion, désintégration), écrivent des équations de réaction nucléaire avec conservation de A et Z et relient ces transformations aux applications.",
          "isotopes, noyaux instables, radioactivité α et β, fission, fusion, conservation du nombre de nucléons et de la charge, énergie libérée, applications",
          "Une réaction nucléaire conserve A et Z", "La fission casse des noyaux lourds, la fusion unit des noyaux légers.",
          ["Les isotopes d’un élément ont le même nombre de protons (Z) mais pas le même nombre de neutrons. Certains noyaux sont instables : ils se désintègrent (radioactivité).",
           "Dans une réaction nucléaire, le nombre total de nucléons (A) et le nombre total de charges (Z) se conservent.",
           "Fission : un noyau lourd (uranium 235) se casse sous l’impact d’un neutron (centrales). Fusion : des noyaux légers s’unissent (Soleil). Ces réactions libèrent beaucoup plus d’énergie que les réactions chimiques."],
          [("²³⁵U + ¹n → ⁹⁴Sr + ¹⁴⁰Xe + x ¹n. Que vaut x ?", ["Nucléons : 235 + 1 = 94 + 140 + x.", "x = 236 − 234."], "x = 2.")],
          [("Une réaction nucléaire change seulement les électrons.", "Elle modifie les noyaux, les éléments changent."), ("Fusion et fission, c’est pareil.", "La fission casse un gros noyau, la fusion unit des petits.")],
          [("Pourquoi la fusion est-elle difficile sur Terre ?", "Il faut des températures de plusieurs millions de degrés."), ("Qu’est-ce qu’une particule α ?", "Un noyau d’hélium 4 (2 protons et 2 neutrons).")],
          [("Vocabulaire", [("la fission", "un noyau lourd se casse"), ("la fusion", "des noyaux légers s’unissent"), ("la particule α", "noyau d’hélium 4"), ("la particule β⁻", "électron émis par le noyau"),
                            ("le rayonnement γ", "rayonnement électromagnétique très énergétique"), ("un noyau instable", "se désintègre spontanément"), ("la réaction en chaîne", "les neutrons libérés provoquent d’autres fissions")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Applications", [("la centrale nucléaire", "fission de l’uranium"), ("le Soleil", "fusion de l’hydrogène"), ("la datation au carbone 14", "désintégration d’un isotope radioactif"), ("la scintigraphie", "traceur radioactif en médecine"),
                             ("la radiothérapie", "rayonnements contre les tumeurs"), ("le projet ITER", "recherche sur la fusion contrôlée")],
            "Quelle transformation nucléaire utilise {k} ?", "Où utilise-t-on {v} ?"),
           ("Isotopes et espèces", [("¹²C et ¹⁴C", "isotopes du carbone"), ("¹H et ²H", "isotopes de l’hydrogène"), ("²³⁵U et ²³⁸U", "isotopes de l’uranium"), ("³⁵Cl et ³⁷Cl", "isotopes du chlore"),
                                    ("¹⁶O et ¹⁸O", "isotopes de l’oxygène"), ("⁴He", "produit de la désintégration α")],
            "Que sont {k} ?", None)],
          ["Une réaction nucléaire conserve A et Z.", "La fission casse un noyau lourd.", "La fusion unit des noyaux légers.", "Le Soleil produit son énergie par fusion.",
           "Les centrales nucléaires utilisent la fission.", "Les isotopes ont le même Z.", "Une particule α est un noyau d’hélium."],
          [("Une réaction nucléaire ne change pas les éléments.", "Elle les change."), ("Les centrales utilisent la fusion.", "Elles utilisent la fission."), ("Les isotopes ont des Z différents.", "Ils ont le même Z."),
           ("La fusion casse un noyau lourd.", "C’est la fission."), ("Une particule α est un électron.", "C’est un noyau d’hélium.")],
          "les transformations nucléaires", "matter"),

        H("P", "mouvement-et-forces", "Mouvement et interactions", "Mouvement et forces",
          "Les élèves décrivent un mouvement par le vecteur vitesse dans un référentiel, modélisent les actions par des forces et relient la variation du vecteur vitesse aux forces (principe d’inertie).",
          "référentiel, trajectoire, vecteur position, vecteur vitesse, mouvement rectiligne uniforme, forces, poids, réaction du support, tension d’un fil, principe d’inertie",
          "Forces compensées : mouvement rectiligne uniforme", "Sinon, le vecteur vitesse varie (principe d’inertie).",
          ["Dans un référentiel, le vecteur vitesse a pour direction la tangente à la trajectoire et pour valeur v = d : Δt.",
           "Les forces usuelles : le poids P = m × g (g = 9,81 N/kg), la réaction du support, la tension d’un fil, les frottements.",
           "Principe d’inertie : si les forces qui s’exercent sur un système se compensent (ou s’il n’y en a pas), il est immobile ou en mouvement rectiligne uniforme, et réciproquement."],
          [("Un palet glisse sur la glace en ligne droite à vitesse constante. Que dire des forces ?", ["Le mouvement est rectiligne uniforme.", "D’après le principe d’inertie…"], "Elles se compensent.")],
          [("Un objet en mouvement subit toujours une force dans le sens du mouvement.", "Sans force (ou forces compensées), il continue tout droit à vitesse constante."), ("Masse et poids, c’est pareil.", "La masse en kg, le poids en N : P = m × g.")],
          [("Pourquoi un passager bascule-t-il en avant au freinage ?", "Par inertie, il tend à conserver sa vitesse."), ("Qu’est-ce qu’un référentiel ?", "L’objet par rapport auquel on étudie le mouvement, muni d’une horloge.")],
          [("Forces", [("le poids", "vertical, vers le bas, P = m × g"), ("la réaction du support", "perpendiculaire au support sans frottements"), ("la tension du fil", "le long du fil, vers le point d’attache"),
                       ("les frottements de l’air", "opposés au mouvement"), ("la poussée d’Archimède", "verticale, vers le haut, dans un fluide"), ("la force électrique", "entre deux charges")],
            "Quelles caractéristiques a {k} ?", "Quelle force : {v} ?"),
           ("Principe d’inertie", [("forces qui se compensent, objet immobile", "il reste immobile"), ("forces qui se compensent, objet en mouvement", "mouvement rectiligne uniforme"), ("forces qui ne se compensent pas", "le vecteur vitesse varie"),
                                   ("parachutiste à vitesse limite", "forces compensées"), ("balle qui ralentit en roulant", "les frottements ne sont pas compensés"), ("satellite en orbite circulaire", "la direction de la vitesse change, une force agit")],
            "Que dit le principe d’inertie : {k} ?", None),
           ("Référentiels", [("le référentiel terrestre", "le sol ou un objet fixe sur Terre"), ("le référentiel géocentrique", "centre de la Terre et étoiles lointaines"), ("le référentiel héliocentrique", "centre du Soleil et étoiles lointaines"),
                             ("la trajectoire", "ensemble des positions successives"), ("le vecteur vitesse", "tangent à la trajectoire"), ("la chronophotographie", "positions à intervalles de temps égaux")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Le poids vaut P = m × g.", "Le vecteur vitesse est tangent à la trajectoire.", "Si les forces se compensent, le mouvement est rectiligne uniforme ou nul.", "Le mouvement dépend du référentiel.",
           "La poussée d’Archimède est verticale vers le haut.", "Un satellite en orbite subit une force.", "Les frottements s’opposent au mouvement."],
          [("Un objet en mouvement subit toujours une force dans son sens.", "Avec des forces compensées, il garde sa vitesse."), ("Le poids se mesure en kilogrammes.", "En newtons."), ("Un satellite en orbite ne subit aucune force.", "La Terre l’attire."),
           ("La réaction du support est verticale vers le bas.", "Elle est perpendiculaire au support, vers l’objet."), ("Le vecteur vitesse est perpendiculaire à la trajectoire.", "Il lui est tangent.")],
          "le mouvement", "forces-and-motion", calc=f_mvt),

        H("P", "ondes-sonores-et-lumiere", "Ondes sonores et lumière", "Sons et lumière",
          "Les élèves caractérisent un son (période, fréquence, niveau d’intensité), exploitent la loi de Snell-Descartes, décrivent les spectres et le fonctionnement d’une lentille mince convergente.",
          "signal périodique, période, fréquence, hauteur, timbre, niveau d’intensité sonore, réfraction, indice, loi de Snell-Descartes, dispersion, spectres, lentille convergente",
          "f = 1 : T et n₁ × sin i₁ = n₂ × sin i₂", "Un milieu plus réfringent rapproche le rayon de la normale.",
          ["Un son périodique a une période T (s) et une fréquence f = 1 : T (Hz) qui fixe sa hauteur. Le timbre dépend de la forme du signal. Le niveau d’intensité sonore s’exprime en décibels.",
           "Lors de la réfraction, n₁ × sin i₁ = n₂ × sin i₂ (angles mesurés par rapport à la normale). L’indice n = c : v. Le prisme disperse la lumière blanche.",
           "Une lentille convergente forme une image réelle d’un objet lointain dans son plan focal. Une lampe à vapeur donne un spectre de raies, un corps chaud un spectre continu."],
          [("Rayon dans l’air (n = 1) à 30° vers l’eau (n = 1,33). Angle de réfraction ?", ["sin i₂ = sin 30° : 1,33 = 0,376.", "i₂ ≈ 22°."], "Environ 22°.")],
          [("On mesure l’angle par rapport à la surface.", "On le mesure par rapport à la normale."), ("Un son grave a une grande fréquence.", "Un son grave a une petite fréquence.")],
          [("Pourquoi une paille semble-t-elle cassée dans l’eau ?", "La lumière est réfractée en passant de l’eau à l’air."), ("Que révèle le spectre d’une étoile ?", "Ses raies d’absorption indiquent les éléments présents dans son atmosphère.")],
          [("Grandeurs", [("la période", "durée d’un motif, en secondes"), ("la fréquence", "nombre de motifs par seconde, en hertz"), ("le niveau d’intensité sonore", "en décibels"), ("l’indice de réfraction", "rapport c : v"),
                          ("la longueur d’onde", "distance parcourue en une période"), ("la distance focale", "distance entre la lentille et le foyer"), ("le timbre", "dépend de la forme du signal")],
            "Que désigne {k} ?", "Quelle grandeur : {v} ?"),
           ("Spectres", [("lampe à vapeur de sodium", "spectre de raies d’émission"), ("filament chauffé à blanc", "spectre continu"), ("lumière blanche traversant un gaz froid", "spectre de raies d’absorption"),
                         ("laser", "une seule raie"), ("étoile très chaude", "spectre continu riche en bleu"), ("étoile peu chaude", "spectre continu riche en rouge")],
            "Quel spectre donne {k} ?", None),
           ("Réfraction et lentilles", [("passage dans un milieu plus réfringent", "le rayon se rapproche de la normale"), ("passage dans un milieu moins réfringent", "le rayon s’écarte de la normale"),
                                        ("rayon parallèle à l’axe d’une lentille convergente", "passe par le foyer image"), ("rayon passant par le centre optique", "n’est pas dévié"), ("le prisme", "disperse la lumière blanche"),
                                        ("incidence normale", "pas de déviation")],
            "Que se passe-t-il : {k} ?", None)],
          ["f = 1 : T.", "Les angles se mesurent par rapport à la normale.", "Un son aigu a une grande fréquence.", "Le prisme disperse la lumière blanche.",
           "Un rayon passant par le centre optique n’est pas dévié.", "Une lampe à vapeur donne un spectre de raies.", "L’indice de réfraction vaut c : v."],
          [("Les angles se mesurent par rapport à la surface.", "Par rapport à la normale."), ("Un son grave a une grande fréquence.", "Il a une petite fréquence."), ("Un corps chaud donne un spectre de raies.", "Il donne un spectre continu."),
           ("f = T.", "f = 1 : T."), ("Dans un milieu plus réfringent, le rayon s’écarte de la normale.", "Il s’en rapproche.")],
          "les ondes", "waves-and-light", calc=f_onde),

        H("P", "signaux-electriques-et-capteurs", "Signaux électriques et capteurs", "Signaux et capteurs",
          "Les élèves exploitent la loi des nœuds, la loi des mailles et la loi d’Ohm, tracent la caractéristique d’un dipôle et utilisent un capteur résistif.",
          "intensité, tension, loi des nœuds, loi des mailles, caractéristique tension-courant, loi d’Ohm, capteur, thermistance, photorésistance, étalonnage",
          "U = R × I pour un conducteur ohmique", "Un capteur résistif convertit une grandeur physique en résistance.",
          ["Loi des nœuds : la somme des intensités qui arrivent à un nœud est égale à la somme de celles qui en partent. Loi des mailles : la somme des tensions dans une maille est nulle.",
           "La caractéristique d’un dipôle est la courbe U = f(I). Pour un conducteur ohmique, c’est une droite passant par l’origine : U = R × I.",
           "Une thermistance (CTN) voit sa résistance diminuer quand la température augmente. Une photorésistance voit la sienne diminuer quand l’éclairement augmente. On étalonne le capteur pour mesurer."],
          [("Un nœud reçoit 0,8 A et une branche en emporte 0,3 A. L’autre branche ?", ["Loi des nœuds.", "0,8 − 0,3."], "0,5 A.")],
          [("Le courant s’use dans les dipôles.", "Dans une branche, l’intensité est la même partout."), ("Tout dipôle suit la loi d’Ohm.", "Seul le conducteur ohmique a une caractéristique linéaire.")],
          [("À quoi sert une courbe d’étalonnage ?", "À convertir une mesure de résistance en température ou en éclairement."), ("Comment brancher un ampèremètre ?", "En série, en entrant par la borne mA ou A.")],
          [("Capteurs", [("la thermistance CTN", "résistance qui diminue quand la température augmente"), ("la photorésistance", "résistance qui diminue avec l’éclairement"), ("le microphone", "convertit un son en tension"),
                         ("la jauge de contrainte", "résistance qui varie avec la déformation"), ("la photodiode", "courant qui dépend de la lumière"), ("le capteur à ultrasons", "mesure une distance par écho")],
            "Que fait {k} ?", "Quel capteur : {v} ?"),
           ("Lois", [("loi des nœuds", "somme des intensités entrantes = somme des sortantes"), ("loi des mailles", "somme algébrique des tensions nulle"), ("loi d’Ohm", "U = R × I"),
                     ("puissance électrique", "P = U × I"), ("intensité dans une branche", "la même en tout point"), ("tensions de dipôles en parallèle", "égales")],
            "Que dit {k} ?", None),
           ("Mesures", [("l’ampèremètre", "se branche en série"), ("le voltmètre", "se branche en dérivation"), ("l’ohmmètre", "mesure une résistance hors tension"), ("la carte Arduino", "acquiert et traite des mesures"),
                        ("la caractéristique", "courbe U en fonction de I"), ("l’étalonnage", "relation entre grandeur mesurée et grandeur physique")],
            "Que sais-tu de {k} ?", "Qu’est-ce qui {v} ?")],
          ["U = R × I pour un conducteur ohmique.", "Dans une branche, l’intensité est la même partout.", "Une CTN voit sa résistance diminuer quand la température monte.", "L’ampèremètre se branche en série.",
           "La caractéristique d’un conducteur ohmique est une droite passant par l’origine.", "Un capteur doit être étalonné.", "La somme des tensions dans une maille est nulle."],
          [("Tout dipôle suit la loi d’Ohm.", "Seul le conducteur ohmique."), ("Le courant s’use dans une lampe.", "Il est le même dans la branche."), ("Le voltmètre se branche en série.", "En dérivation."),
           ("Une CTN voit sa résistance augmenter avec la température.", "Elle diminue."), ("P = U : I.", "P = U × I.")],
          "les signaux électriques", "energy", calc=f_elec),

        H("S", "l-organisme-pluricellulaire", "L’organisme pluricellulaire : cellules et métabolisme", "Cellules et métabolisme",
          "Les élèves décrivent l’organisation d’un organisme pluricellulaire, la structure des cellules, le rôle de l’ADN et le métabolisme contrôlé par des enzymes.",
          "organisme, organes, tissus, cellules, membrane, cytoplasme, noyau, organites, ADN, métabolisme, enzymes, cellules spécialisées",
          "Un organisme est fait de cellules spécialisées", "Toutes les cellules d’un individu ont le même ADN, mais n’expriment pas les mêmes gènes.",
          ["Un organisme pluricellulaire est formé d’organes, eux-mêmes formés de tissus faits de cellules spécialisées (neurones, fibres musculaires, cellules de feuille).",
           "Une cellule eucaryote a une membrane, un cytoplasme, un noyau contenant l’ADN et des organites (mitochondries ; chloroplastes chez les végétaux).",
           "Le métabolisme est l’ensemble des réactions chimiques de la cellule, chacune catalysée par une enzyme. Il dépend de l’ADN et de l’environnement."],
          [("Une cellule de racine n’a pas de chloroplastes, une cellule de feuille si. Pourtant même ADN. Pourquoi ?", ["Chaque cellule n’exprime qu’une partie de ses gènes.", "L’expression dépend de la cellule et du milieu."], "Elles sont spécialisées.")],
          [("Chaque cellule n’a que les gènes dont elle a besoin.", "Toutes ont le même ADN, elles en expriment une partie."), ("Les bactéries ont un noyau.", "Ce sont des procaryotes, sans noyau.")],
          [("Qu’est-ce qu’une enzyme ?", "Une protéine qui accélère une réaction précise du métabolisme."), ("À quoi servent les mitochondries ?", "À la respiration cellulaire qui fournit de l’énergie.")],
          [("Organites", [("le noyau", "contient l’ADN"), ("la mitochondrie", "lieu de la respiration cellulaire"), ("le chloroplaste", "lieu de la photosynthèse"), ("la membrane plasmique", "délimite la cellule"),
                          ("la paroi", "enveloppe rigide des cellules végétales"), ("le ribosome", "fabrique les protéines"), ("la vacuole", "réserve d’eau et de substances")],
            "Quel est le rôle de {k} ?", "Quel organite {v} ?"),
           ("Niveaux d’organisation", [("l’organisme", "ensemble des organes"), ("l’organe", "ensemble de tissus"), ("le tissu", "ensemble de cellules semblables"), ("la cellule", "unité du vivant"),
                                       ("la molécule d’ADN", "support de l’information génétique"), ("le gène", "portion d’ADN")],
            "Que désigne {k} ?", "Quel niveau : {v} ?"),
           ("Métabolisme", [("la photosynthèse", "produit de la matière organique à partir de lumière et de CO₂"), ("la respiration cellulaire", "libère de l’énergie à partir du glucose"), ("la fermentation", "produit de l’énergie sans dioxygène"),
                            ("l’enzyme", "catalyse une réaction précise"), ("le métabolisme", "ensemble des réactions de la cellule"), ("l’autotrophie", "production de sa propre matière organique"), ("l’hétérotrophie", "utilisation de matière organique déjà formée")],
            "Que désigne {k} ?", "Quoi : {v} ?")],
          ["Un organisme est fait de cellules spécialisées.", "Toutes les cellules d’un individu ont le même ADN.", "Les mitochondries réalisent la respiration cellulaire.", "Les enzymes catalysent les réactions.",
           "Les bactéries n’ont pas de noyau.", "Les végétaux chlorophylliens sont autotrophes.", "Le ribosome fabrique les protéines."],
          [("Chaque cellule n’a que ses propres gènes.", "Toutes ont le même ADN."), ("Les bactéries ont un noyau.", "Elles n’en ont pas."), ("Les chloroplastes sont dans toutes les cellules animales.", "Ils sont dans des cellules végétales."),
           ("Les enzymes ralentissent les réactions.", "Elles les accélèrent."), ("L’humain est autotrophe.", "Il est hétérotrophe.")],
          "la cellule", "living-things-and-ecosystems"),

        H("S", "biodiversite-et-evolution", "Biodiversité, sélection et dérive", "Biodiversité et évolution",
          "Les élèves décrivent la biodiversité à différentes échelles, calculent des fréquences d’allèles et expliquent leur évolution par la sélection naturelle et la dérive génétique.",
          "biodiversité des écosystèmes, des espèces et génétique, allèles, fréquence allélique, mutations, sélection naturelle, dérive génétique, espèce, spéciation, crises",
          "La fréquence d’un allèle varie par sélection ou par hasard", "La dérive génétique est plus forte dans les petites populations.",
          ["La biodiversité existe à trois échelles : diversité des écosystèmes, des espèces et diversité génétique (allèles différents au sein d’une espèce).",
           "La fréquence d’un allèle est le nombre de copies de cet allèle divisé par le nombre total de copies du gène. Les fréquences des allèles d’un gène font 1.",
           "La sélection naturelle augmente la fréquence des allèles avantageux dans un milieu. La dérive génétique change les fréquences au hasard, surtout dans les petites populations."],
          [("Une population compte 120 allèles du gène, dont 30 allèles B. Fréquence de B ?", ["f = 30 : 120.", "= 0,25."], "0,25, et 0,75 pour l’autre allèle.")],
          [("La sélection naturelle crée les mutations.", "Les mutations apparaissent au hasard, la sélection trie."), ("La dérive est plus forte dans les grandes populations.", "Elle est plus forte dans les petites.")],
          [("Pourquoi la diversité génétique protège-t-elle une espèce ?", "Certains individus pourront survivre si le milieu change."), ("Qu’est-ce qu’un effet fondateur ?", "Une petite population fondatrice possède peu d’allèles : la dérive est forte.")],
          [("Vocabulaire", [("la dérive génétique", "variation des fréquences due au hasard"), ("la sélection naturelle", "les mieux adaptés ont plus de descendants"), ("l’allèle", "version d’un gène"), ("la mutation", "modification de la séquence d’ADN"),
                            ("la spéciation", "apparition d’une nouvelle espèce"), ("l’effet fondateur", "petite population de départ"), ("la fréquence allélique", "proportion d’un allèle dans la population")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Échelles de biodiversité", [("forêt, récif, prairie", "diversité des écosystèmes"), ("ours, saumon, mésange", "diversité des espèces"), ("couleur des coquilles d’escargots d’une même espèce", "diversité génétique"),
                                        ("groupes sanguins humains", "diversité génétique"), ("mangrove et désert", "diversité des écosystèmes"), ("nombre d’espèces d’oiseaux d’une île", "diversité des espèces"), ("variétés de pommes d’un verger", "diversité génétique"), ("lac, tourbière et rivière d’une région", "diversité des écosystèmes"), ("insectes d’une prairie", "diversité des espèces")],
            "Quelle échelle de biodiversité : {k} ?", None),
           ("Sélection ou dérive ?", {"de la sélection naturelle": ["phalènes sombres dans les villes polluées", "bactéries résistantes aux antibiotiques", "moustiques résistants aux insecticides", "becs des pinsons adaptés aux graines", "allèle de tolérance au lactose en Europe", "pelage blanc des lièvres arctiques"],
                                      "de la dérive génétique": ["allèle rare devenu fréquent sur une petite île par hasard", "perte d’allèles après un goulot d’étranglement", "effet fondateur dans une population isolée", "allèle perdu par hasard en peu de générations", "fréquence qui varie au hasard dans un petit élevage", "maladie rare fréquente dans un village isolé"]})],
          ["La biodiversité existe à trois échelles.", "Les fréquences des allèles d’un gène font 1.", "La dérive est plus forte dans les petites populations.", "Les mutations apparaissent au hasard.",
           "La sélection augmente la fréquence des allèles avantageux.", "Les bactéries résistantes sont un exemple de sélection.", "Un effet fondateur réduit la diversité génétique."],
          [("La sélection crée les mutations.", "Elle trie les variations existantes."), ("La dérive est plus forte dans les grandes populations.", "Dans les petites."), ("Les fréquences des allèles font 100 chacune.", "Leur somme fait 1."),
           ("La dérive favorise toujours les meilleurs allèles.", "Elle agit au hasard."), ("La biodiversité ne concerne que les espèces.", "Aussi les gènes et les écosystèmes.")],
          "la biodiversité", "living-things-and-ecosystems", calc=f_freq),

        H("S", "geosciences-sols-et-agrosystemes", "Sols, agrosystèmes et ressources", "Sols et agrosystèmes",
          "Les élèves décrivent la formation et la fragilité des sols, le fonctionnement d’un agrosystème et les enjeux d’une agriculture durable.",
          "sol, roche mère, humus, horizons, altération, êtres vivants du sol, agrosystème, intrants, rendement, érosion, agroécologie, ressource en eau",
          "Un sol met des milliers d’années à se former", "Un agrosystème exporte de la matière : il faut la compenser sans abîmer le sol.",
          ["Le sol se forme par altération de la roche mère et décomposition de la matière organique par les êtres vivants du sol. Il est organisé en horizons.",
           "Un agrosystème est un écosystème géré par l’humain pour produire. Les récoltes exportent de la matière : on apporte des intrants (engrais, eau, produits phytosanitaires).",
           "L’érosion, le tassement, la pollution menacent les sols. L’agroécologie (couverts végétaux, haies, rotations) préserve la fertilité et la biodiversité."],
          [("Un champ laissé nu en hiver sur une pente perd de la terre. Pourquoi ?", ["La pluie ruisselle sans végétation.", "Elle arrache les particules du sol."], "Érosion : il faut un couvert végétal.")],
          [("Le sol est une ressource inépuisable.", "Il se forme très lentement et peut disparaître vite."), ("Plus d’engrais donne toujours plus de rendement.", "L’excès pollue l’eau sans augmenter le rendement.")],
          [("Qu’est-ce que l’humus ?", "La matière organique décomposée qui rend le sol fertile."), ("Pourquoi planter des haies ?", "Elles limitent l’érosion et abritent les auxiliaires des cultures.")],
          [("Vocabulaire", [("la roche mère", "roche à l’origine du sol"), ("l’humus", "matière organique décomposée"), ("un horizon", "couche du sol"), ("un intrant", "apport extérieur à l’agrosystème"),
                            ("le rendement", "production par hectare"), ("l’agroécologie", "agriculture qui utilise les processus écologiques"), ("un auxiliaire", "être vivant qui aide les cultures")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Pratiques", [("le couvert végétal en hiver", "limite l’érosion"), ("la rotation des cultures", "limite les maladies et entretient la fertilité"), ("les haies", "abritent les auxiliaires"), ("l’excès de nitrates", "pollue les nappes et les rivières"),
                          ("le labour profond répété", "perturbe la vie du sol"), ("les coccinelles", "mangent les pucerons"), ("le compost", "rend de la matière organique au sol")],
            "Quel effet a {k} ?", "Qu’est-ce qui {v} ?"),
           ("Menaces ou protection ?", {"des menaces pour les sols": ["l’artificialisation par le béton", "l’érosion des champs nus", "le tassement par les engins lourds", "la pollution par les métaux", "la perte de matière organique", "le surpâturage"],
                                        "des pratiques qui protègent les sols": ["les cultures intermédiaires", "le paillage", "l’agroforesterie", "le compostage", "le semis direct sous couvert", "les haies en bord de champ"]})],
          ["Un sol met des milliers d’années à se former.", "L’humus rend le sol fertile.", "Un couvert végétal limite l’érosion.", "Un agrosystème reçoit des intrants.",
           "L’excès de nitrates pollue l’eau.", "Les haies abritent des auxiliaires.", "Le sol est organisé en horizons."],
          [("Le sol est inépuisable.", "Il se forme très lentement."), ("Plus d’engrais donne toujours plus de rendement.", "L’excès pollue sans gain."), ("Un champ nu protège le sol.", "Il favorise l’érosion."),
           ("Les coccinelles détruisent les cultures.", "Elles mangent les pucerons."), ("L’humus est une roche.", "C’est de la matière organique.")],
          "les sols", "earths-systems"),

        H("S", "corps-humain-sexualite-et-microbiote", "Sexualité, procréation et microbiote", "Sexualité et microbiote",
          "Les élèves décrivent le contrôle hormonal de la reproduction, les méthodes de contraception et de procréation médicalement assistée, et le rôle du microbiote humain dans la santé.",
          "hormones, testostérone, œstrogènes, progestérone, cycle, hypothalamus, hypophyse, contraception, PMA, infections sexuellement transmissibles, microbiote, santé",
          "La reproduction est contrôlée par des hormones", "Le microbiote, ensemble de micro-organismes, contribue à notre santé.",
          ["Le fonctionnement des testicules et des ovaires est contrôlé par l’hypothalamus et l’hypophyse grâce à des hormones. Chez la femme, le cycle d’environ 28 jours est rythmé par les œstrogènes et la progestérone.",
           "La pilule contient des hormones de synthèse qui bloquent l’ovulation. Le préservatif protège aussi des IST. La PMA aide les couples infertiles (insémination, fécondation in vitro).",
           "Le microbiote intestinal (des milliards de bactéries) aide à digérer, produit des vitamines et protège contre les pathogènes. Les antibiotiques peuvent le perturber."],
          [("Pourquoi la pilule empêche-t-elle une grossesse ?", ["Elle apporte des hormones de synthèse.", "L’hypophyse ne déclenche plus l’ovulation."], "Il n’y a pas d’ovule à féconder.")],
          [("La pilule protège des IST.", "Seul le préservatif protège des IST."), ("Toutes les bactéries du corps sont dangereuses.", "Le microbiote est essentiel à la santé.")],
          [("Qu’est-ce que la FIV ?", "La fécondation in vitro : l’ovule est fécondé au laboratoire puis l’embryon est placé dans l’utérus."), ("Comment préserver son microbiote ?", "Alimentation variée et riche en fibres, antibiotiques seulement si nécessaires.")],
          [("Hormones et organes", [("la testostérone", "produite par les testicules"), ("les œstrogènes", "produits par les ovaires"), ("la progestérone", "prépare l’utérus à la nidation"), ("la LH", "hormone de l’hypophyse qui déclenche l’ovulation"),
                                    ("la GnRH", "hormone de l’hypothalamus"), ("l’hypophyse", "glande sous le cerveau qui contrôle les gonades")],
            "Que sais-tu de {k} ?", "Quoi : {v} ?"),
           ("Contraception et santé", [("le préservatif", "contraception et protection contre les IST"), ("la pilule", "bloque l’ovulation"), ("le stérilet", "empêche la nidation"), ("la contraception d’urgence", "à prendre au plus tôt après un rapport à risque"),
                                       ("le dépistage", "détecte une IST"), ("la FIV", "fécondation en laboratoire"), ("le vaccin HPV", "protège contre des papillomavirus")],
            "À quoi sert {k} ?", "Quel moyen {v} ?"),
           ("Microbiote", [("digestion des fibres", "assurée en partie par les bactéries intestinales"), ("production de vitamine K", "assurée par le microbiote"), ("protection contre les pathogènes", "les bonnes bactéries occupent la place"),
                           ("antibiotiques répétés", "peuvent déséquilibrer le microbiote"), ("alimentation riche en fibres", "favorise un microbiote varié"), ("microbiote cutané", "bactéries de la peau")],
            "Que sais-tu de : {k} ?", None)],
          ["La reproduction est contrôlée par des hormones.", "La pilule bloque l’ovulation.", "Seul le préservatif protège des IST.", "Le microbiote aide à digérer.",
           "Les antibiotiques peuvent perturber le microbiote.", "L’hypophyse contrôle les gonades.", "La FIV est une technique de PMA."],
          [("La pilule protège des IST.", "Seul le préservatif."), ("Toutes les bactéries du corps sont dangereuses.", "Le microbiote est utile."), ("La testostérone est produite par les ovaires.", "Par les testicules."),
           ("Les antibiotiques renforcent toujours le microbiote.", "Ils peuvent le perturber."), ("Le cycle n’est pas contrôlé par des hormones.", "Il est contrôlé par des hormones.")],
          "la reproduction et le microbiote", "living-things-and-ecosystems"),
    ]
