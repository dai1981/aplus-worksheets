# -*- coding: utf-8 -*-
"""France / Physique-chimie et SVT : enseignement de spécialité de première"""
import math
from fr_sci import H, nq, num


def f_c(R):
    k = R.choice(["c", "c", "n", "cm", "dil"])
    if k == "c":
        n, V = R.choice([(0.01, 0.1), (0.05, 0.25), (0.2, 0.5), (0.002, 0.05), (0.15, 0.3), (0.03, 0.2)])
        return nq("Une solution de %s L contient %s mol de soluté. Quelle est sa concentration en quantité de matière ?" % (num(V), num(n)), n / V, [n * V, V / n, n / V / 1000], "mol/L",
                  "c = n : V = %s : %s = %s mol/L." % (num(n), num(V), num(n / V)))
    if k == "n":
        c, V = R.choice([(0.1, 0.025), (0.5, 0.2), (0.02, 0.1), (1, 0.015), (0.25, 0.04)])
        return nq("Quelle quantité de soluté contient un volume de %s L d’une solution à %s mol/L ?" % (num(V), num(c)), c * V, [c / V, V / c, c + V], "mol", "n = c × V = %s mol." % num(c * V))
    if k == "cm":
        m, M, V = R.choice([(5.85, 58.5, 0.5), (1.8, 180, 0.1), (4, 40, 0.25), (2.94, 98, 0.2), (0.58, 58, 0.1)])
        c = m / M / V
        return nq("On dissout %s g d’un soluté de masse molaire %s g/mol pour obtenir %s L de solution. Concentration en quantité de matière ?" % (num(m), num(M), num(V)), c,
                  [m / V, m * M / V, m / M * V], "mol/L", "n = %s : %s = %s mol, c = n : V = %s mol/L." % (num(m), num(M), num(m / M), num(c)))
    c0, V0, V1 = R.choice([(0.1, 10, 100), (0.5, 20, 250), (1, 5, 50), (0.2, 25, 500)])
    return nq("On dilue %s mL d’une solution à %s mol/L jusqu’à %s mL. Quelle est la concentration finale ?" % (num(V0), num(c0), num(V1)), c0 * V0 / V1, [c0 * V1 / V0, c0, c0 * V0], "mol/L",
              "c₁ = c₀ × V₀ : V₁ = %s mol/L." % num(c0 * V0 / V1))


def f_av(R):
    # aA + bB -> produits
    eqs = [("2 H₂ + O₂ → 2 H₂O", "H₂", "O₂", 2, 1), ("N₂ + 3 H₂ → 2 NH₃", "N₂", "H₂", 1, 3), ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄", "O₂", 1, 2),
           ("2 Al + 3 Cl₂ → 2 AlCl₃", "Al", "Cl₂", 2, 3), ("C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O", "C₃H₈", "O₂", 1, 5), ("Fe + 2 H⁺ → Fe²⁺ + H₂", "Fe", "H⁺", 1, 2)]
    e, A, B, a, b = R.choice(eqs)
    nA, nB = R.choice([(0.6, 0.6), (1.2, 0.9), (0.3, 1.5), (2.0, 2.0), (0.5, 0.4), (1.0, 3.0), (0.8, 2.0)])
    x = min(nA / a, nB / b)
    lim = A if nA / a < nB / b else (B if nB / b < nA / a else "aucun")
    k = R.choice(["x", "x", "reste"])
    if k == "x":
        return nq("%s. État initial : %s mol de %s et %s mol de %s. Quel est l’avancement maximal ?" % (e, num(nA), A, num(nB), B), x, [max(nA / a, nB / b), min(nA, nB), nA + nB], "mol",
                  "xmax = min(%s : %d ; %s : %d) = %s mol. Réactif limitant : %s." % (num(nA), a, num(nB), b, num(x), lim))
    rA, rB = nA - a * x, nB - b * x
    r = rA if rA > 1e-9 else rB
    rn = A if rA > 1e-9 else B
    if r < 1e-9:
        return None
    return nq("%s. État initial : %s mol de %s et %s mol de %s. Quelle quantité de %s reste à l’état final ?" % (e, num(nA), A, num(nB), B, rn), r, [r + x, x, abs(nA - nB) if abs(nA - nB) > 1e-9 and abs(abs(nA - nB) - r) > 1e-9 else r * 2], "mol",
              "xmax = %s mol, il reste %s mol de %s." % (num(x), num(r), rn))


def f_titr(R):
    k = R.choice(["c", "c", "V", "n"])
    if k == "c":
        c2, V2, V1 = R.choice([(0.1, 12.5, 10), (0.05, 18, 20), (0.02, 15, 10), (0.1, 8.4, 20), (0.2, 11, 25), (0.01, 16, 10), (0.05, 13.6, 10), (0.1, 19.2, 20), (0.02, 9.5, 5)])
        return nq("On titre %s mL d’une solution de diiode par une solution de thiosulfate à %s mol/L (réaction 1 : 2). L’équivalence est obtenue pour %s mL. Concentration en diiode ?" % (num(V1), num(c2), num(V2)), c2 * V2 / (2 * V1),
                  [c2 * V2 / V1, 2 * c2 * V2 / V1, c2 * V1 / V2], "mol/L", "À l’équivalence, n(I₂) = n(S₂O₃²⁻) : 2, donc c = %s × %s : (2 × %s) = %s mol/L." % (num(c2), num(V2), num(V1), num(c2 * V2 / (2 * V1))))
    if k == "V":
        c1, V1, c2 = R.choice([(0.05, 20, 0.1), (0.02, 10, 0.01), (0.1, 15, 0.05), (0.04, 25, 0.1), (0.2, 10, 0.1), (0.03, 20, 0.06), (0.08, 12.5, 0.1)])
        return nq("Un réactif à %s mol/L (%s mL) réagit mole à mole avec une solution titrante à %s mol/L. Quel volume équivalent attend-on ?" % (num(c1), num(V1), num(c2)), c1 * V1 / c2,
                  [c2 * V1 / c1, c1 * c2 * V1, V1], "mL", "À l’équivalence : c₁V₁ = c₂VE, VE = %s mL." % num(c1 * V1 / c2))
    c, V = R.choice([(0.1, 12), (0.02, 15.5), (0.05, 9), (0.2, 7.5), (0.1, 17.4), (0.01, 22)])
    return nq("Quelle quantité de réactif titrant a été versée à l’équivalence (%s mL d’une solution à %s mol/L) ?" % (num(V), num(c)), c * V / 1000, [c * V, c / V, c * V / 100], "mol",
              "n = c × V = %s × %s × 10⁻³ = %s mol." % (num(c), num(V), num(c * V / 1000)))


def f_comb(R):
    k = R.choice(["E", "E", "m", "Em"])
    fuels = [("du méthane", "de méthane", 16, 890), ("de l’éthanol", "d’éthanol", 46, 1370), ("du propane", "de propane", 44, 2220), ("du butane", "de butane", 58, 2880), ("de l’octane", "d’octane", 114, 5470)]
    nm, np_, M, Em = R.choice(fuels)
    if k == "E":
        n = R.choice([2, 0.5, 10, 3, 0.25])
        return nq("L’énergie molaire de combustion %s est %s kJ/mol. Quelle énergie libère la combustion de %s mol ?" % (nm, num(Em), num(n)), n * Em, [Em / n, Em, n * Em * 1000], "kJ",
                  "E = n × Em = %s × %s = %s kJ." % (num(n), num(Em), num(n * Em)))
    if k == "m":
        m = R.choice([1000, 160, 46, 88, 580, 228])
        return nq("Quelle énergie libère la combustion de %s g %s (M = %s g/mol, Em = %s kJ/mol) ?" % (num(m), np_, num(M), num(Em)), m / M * Em, [m * Em, m / Em * M, Em / M], "kJ",
                  "n = %s : %s = %s mol, E = %s kJ." % (num(m), num(M), num(m / M), num(m / M * Em)))
    n, E = R.choice([(2, 1780), (0.5, 685), (3, 6660), (4, 11520)])
    return nq("La combustion de %s mol d’un combustible libère %s kJ. Quelle est son énergie molaire de combustion ?" % (num(n), num(E)), E / n, [E * n, n / E, E], "kJ/mol", "Em = E : n = %s kJ/mol." % num(E / n))


def f_champ(R):
    k = R.choice(["grav", "grav", "coul", "E", "g"])
    G, kc = 6.67e-11, 9.0e9
    if k == "grav":
        m1, m2, d = R.choice([(5.97e24, 7.35e22, 3.84e8), (1000, 1000, 1), (5.97e24, 70, 6.37e6), (1.99e30, 5.97e24, 1.5e11), (5.97e24, 1000, 7.0e6)])
        F = G * m1 * m2 / d ** 2
        return nq("Quelle est la force d’attraction gravitationnelle entre deux corps de masses %s kg et %s kg distants de %s m ? (G = 6,67 × 10⁻¹¹ N·m²/kg²)" % (num(m1), num(m2), num(d)), F,
                  [G * m1 * m2 / d, F * 1e3, G * (m1 + m2) / d ** 2], "N", "F = G × m₁ × m₂ : d² = %s N." % num(F))
    if k == "coul":
        q1, q2, d = R.choice([(1e-6, 2e-6, 0.1), (3e-6, 3e-6, 0.3), (1.6e-19, 1.6e-19, 1e-10), (5e-9, 2e-9, 0.01), (2e-6, 4e-6, 0.2)])
        F = kc * q1 * q2 / d ** 2
        return nq("Quelle est la valeur de la force électrostatique entre deux charges de %s C et %s C distantes de %s m ? (k = 9,0 × 10⁹ N·m²/C²)" % (num(q1), num(q2), num(d)), F,
                  [kc * q1 * q2 / d, F / 100, kc * (q1 + q2) / d ** 2], "N", "F = k × q₁ × q₂ : d² = %s N." % num(F))
    if k == "E":
        U, d = R.choice([(1000, 0.05), (200, 0.01), (5000, 0.1), (12, 0.002), (300, 0.03), (600, 0.04), (90, 0.005)])
        return nq("Entre deux plaques parallèles distantes de %s m, la tension est %s V. Valeur du champ électrique ?" % (num(d), num(U)), U / d, [U * d, d / U, U / d / 100], "V/m", "E = U : d = %s V/m." % num(U / d))
    h = R.choice([0, 400e3, 6.37e6, 3.6e7, 1e6])
    g = G * 5.97e24 / (6.37e6 + h) ** 2
    return nq("Quelle est l’intensité du champ de pesanteur terrestre à %s m d’altitude ? (G = 6,67 × 10⁻¹¹ SI, M = 5,97 × 10²⁴ kg, R = 6,37 × 10⁶ m)" % num(h), g,
              [G * 5.97e24 / (6.37e6 + h), 9.81 if abs(g - 9.81) > 0.05 else 9.0, g * 2], "N/kg", "g = G × M : (R + h)² = %s N/kg." % num(g))


def f_dyn(R):
    k = R.choice(["dv", "dv", "F", "a", "v"])
    if k == "dv":
        F, m, t = R.choice([(10, 2, 0.5), (300, 1200, 2), (50, 5, 0.1), (2000, 1000, 3), (6, 0.2, 0.05), (900, 60, 1)])
        return nq("Une force résultante constante de %s N agit sur un système de %s kg pendant %s s. De combien varie la vitesse ?" % (num(F), num(m), num(t)), F * t / m,
                  [F * m * t, F / m, m * t / F], "m/s", "Δv ≈ (ΣF : m) × Δt = %s m/s." % num(F * t / m))
    if k == "F":
        m, dv, t = R.choice([(1200, 10, 5), (70, 3, 0.5), (0.45, 20, 0.01), (1000, 27, 9), (2, 4, 0.2), (80, 6, 2), (1500, 30, 12)])
        return nq("Un système de %s kg voit sa vitesse augmenter de %s m/s en %s s. Quelle force résultante s’exerce sur lui ?" % (num(m), num(dv), num(t)), m * dv / t,
                  [m * dv * t, dv / (m * t), m / t], "N", "ΣF ≈ m × Δv : Δt = %s N." % num(m * dv / t))
    if k == "a":
        dv, t = R.choice([(27, 9), (10, 4), (3, 0.5), (100, 20), (15, 6), (28, 3.5), (9.8, 1)])
        return nq("La vitesse d’un mobile passe de 0 à %s m/s en %s s. Valeur de la variation de vitesse par seconde ?" % (num(dv), num(t)), dv / t, [dv * t, t / dv, dv], "m/s²", "Δv : Δt = %s m/s²." % num(dv / t))
    v0, F, m, t = R.choice([(5, 20, 10, 2), (10, -300, 1000, 5), (0, 50, 25, 3), (2, 6, 3, 1)])
    v = v0 + F * t / m
    if v <= 0:
        return None
    return nq("Un système de %s kg a une vitesse de %s m/s. Une force résultante de %s N l’accélère dans le sens du mouvement pendant %s s. Nouvelle vitesse ?" % (num(m), num(v0), num(abs(F)), num(t)), v,
              [v0, F * t / m, v0 + F / m], "m/s", "v = v₀ + (F : m) × Δt = %s m/s." % num(v)) if F > 0 else None


def f_energie(R):
    k = R.choice(["Ec", "Epp", "W", "v", "h"])
    g = 9.81
    if k == "Ec":
        m, v = R.choice([(0.058, 50), (75, 8), (1200, 25), (0.16, 30), (60, 12)])
        return nq("Énergie cinétique d’un système de %s kg à %s m/s ?" % (num(m), num(v)), 0.5 * m * v * v, [m * v * v, 0.5 * m * v, m * v], "J", "Ec = ½ m v² = %s J." % num(0.5 * m * v * v))
    if k == "Epp":
        m, h = R.choice([(2, 10), (70, 3), (0.5, 20), (1000, 50), (60, 8848)])
        return nq("Énergie potentielle de pesanteur d’un objet de %s kg à %s m d’altitude (origine au sol, g = 9,81 N/kg) ?" % (num(m), num(h)), m * g * h, [m * h, m * g, m * g * h / 1000], "J",
                  "Epp = m × g × h = %s J." % num(m * g * h))
    if k == "W":
        F, d, a = R.choice([(50, 10, 0), (100, 5, 60), (20, 4, 30), (200, 2, 45), (80, 12, 0)])
        W = F * d * math.cos(math.radians(a))
        return nq("Une force de %s N s’exerce sur un déplacement de %s m en faisant un angle de %d° avec lui. Quel est son travail ?" % (num(F), num(d), a), W,
                  [F * d, F * d * math.sin(math.radians(a)) if a else F * d / 2, F / d], "J", "W = F × d × cos %d° = %s J." % (a, num(W)))
    if k == "v":
        h = R.choice([5, 20, 1.8, 45, 10])
        v = math.sqrt(2 * g * h)
        return nq("Un objet tombe sans frottement d’une hauteur de %s m sans vitesse initiale. Quelle est sa vitesse au sol ? (g = 9,81 N/kg)" % num(h), v, [2 * g * h, g * h, v / 2], "m/s",
                  "Conservation de l’énergie mécanique : ½ v² = g h, v = √(2 g h) = %s m/s." % num(v))
    v = R.choice([10, 5, 14, 3, 20])
    return nq("Une balle est lancée verticalement vers le haut à %s m/s. Sans frottement, quelle hauteur maximale atteint-elle ? (g = 9,81 N/kg)" % num(v), v * v / (2 * g),
              [v * v / g, v / g, v * v * 2 * g], "m", "h = v² : (2g) = %s m." % num(v * v / (2 * g)))


def f_onde(R):
    k = R.choice(["v", "v", "lam", "T", "retard"])
    if k == "v":
        d, t = R.choice([(1.7, 0.005), (6, 2), (0.5, 0.25), (1500, 1), (3.4, 0.01)])
        return nq("Une perturbation parcourt %s m en %s s. Quelle est la célérité de l’onde ?" % (num(d), num(t)), d / t, [d * t, t / d, d / t / 10], "m/s", "v = d : Δt = %s m/s." % num(d / t))
    if k == "lam":
        v, f = R.choice([(340, 440), (1500, 50000), (2, 4), (340, 20000), (0.5, 2)])
        return nq("Une onde périodique de fréquence %s Hz se propage à %s m/s. Longueur d’onde ?" % (num(f), num(v)), v / f, [v * f, f / v, v / f * 2], "m", "λ = v : f = %s m." % num(v / f))
    if k == "T":
        lam, v = R.choice([(0.5, 2), (1.7, 340), (0.1, 0.4), (3, 1500), (0.02, 340)])
        return nq("Une onde de longueur d’onde %s m se propage à %s m/s. Quelle est sa période ?" % (num(lam), num(v)), lam / v, [v / lam, lam * v, 2 * lam / v], "s", "T = λ : v = %s s." % num(lam / v))
    d, v = R.choice([(10, 340), (1.5, 340), (300, 1500), (50, 5000), (6800, 340)])
    return nq("Deux récepteurs sont distants de %s m sur le trajet d’une onde à %s m/s. Quel est le retard du second sur le premier ?" % (num(d), num(v)), d / v, [d * v, v / d, d / v / 2], "s", "τ = d : v = %s s." % num(d / v))


def f_photon(R):
    k = R.choice(["E", "E", "eV", "lam", "gr"])
    h, c = 6.63e-34, 3.0e8
    if k == "E":
        lam = R.choice([400e-9, 500e-9, 650e-9, 589e-9, 300e-9, 700e-9])
        return nq("Quelle est l’énergie d’un photon de longueur d’onde %s nm ? (h = 6,63 × 10⁻³⁴ J·s, c = 3,00 × 10⁸ m/s)" % num(lam * 1e9), h * c / lam,
                  [h * lam / c, h * c / (lam * 1e9), c / lam], "J", "E = h × c : λ = %s J." % num(h * c / lam))
    if k == "eV":
        E = R.choice([3.2e-19, 4.8e-19, 2.4e-19, 6.4e-19, 1.6e-18])
        return nq("Convertis %s J en électronvolts (1 eV = 1,60 × 10⁻¹⁹ J)." % num(E), E / 1.6e-19, [E * 1.6e-19, E / 1.6e-18, E * 1e19], "eV", "%s : 1,60 × 10⁻¹⁹ = %s eV." % (num(E), num(E / 1.6e-19)))
    if k == "lam":
        nu = R.choice([5e14, 6e14, 7.5e14, 4.3e14, 1e15])
        return nq("Quelle est la longueur d’onde dans le vide d’une radiation de fréquence %s Hz ? (c = 3,00 × 10⁸ m/s)" % num(nu), c / nu, [nu / c, c * nu, h * nu], "m", "λ = c : ν = %s m." % num(c / nu))
    oa, f = R.choice([(-30, 10), (-20, 5), (-60, 20), (-15, 10), (-40, 8)])
    oai = 1 / (1 / f + 1 / oa)
    g = oai / oa
    return nq("Un objet est placé à %s cm devant une lentille convergente de distance focale %s cm. Où se forme l’image (distance OA’) ? (1/OA’ − 1/OA = 1/f’)" % (num(abs(oa)), num(f)), oai,
              [abs(oa), f, 1 / (1 / f - 1 / oa)], "cm", "1/OA’ = 1/%s + 1/(%s), OA’ = %s cm, grandissement γ = %s." % (num(f), num(oa), num(oai), num(g)), neg=True)


def f_elec(R):
    k = R.choice(["P", "J", "rend", "E", "Q"])
    if k == "P":
        U, I = R.choice([(230, 4), (12, 3.5), (3.7, 1.2), (400, 25), (5, 2.4)])
        return nq("Un dipôle sous %s V est traversé par %s A. Puissance reçue ?" % (num(U), num(I)), U * I, [U / I, U * I * I, I / U], "W", "P = U × I = %s W." % num(U * I))
    if k == "J":
        Rr, I = R.choice([(10, 2), (50, 0.5), (4, 3), (100, 0.2), (2.5, 4)])
        return nq("Puissance dissipée par effet Joule dans une résistance de %s Ω parcourue par %s A ?" % (num(Rr), num(I)), Rr * I * I, [Rr * I, Rr / I, Rr * I * I * 2], "W", "P = R × I² = %s W." % num(Rr * I * I))
    if k == "rend":
        Pu, Pa = R.choice([(450, 500), (36, 60), (1700, 2000), (6, 40), (90, 120)])
        return nq("Un convertisseur reçoit %s W et fournit %s W utiles. Quel est son rendement en pourcentage ?" % (num(Pa), num(Pu)), 100 * Pu / Pa, [100 * Pa / Pu, Pu / Pa, 100 - 100 * Pu / Pa], "%",
                  "η = Pu : Pa = %s %%." % num(100 * Pu / Pa))
    if k == "E":
        P, t = R.choice([(60, 3600), (2000, 600), (5, 7200), (1000, 1800), (100, 60)])
        return nq("Quelle énergie (en J) reçoit un appareil de %s W pendant %s s ?" % (num(P), num(t)), P * t, [P / t, t / P, P * t / 3600], "J", "E = P × Δt = %s J." % num(P * t))
    I, t = R.choice([(2, 3600), (0.5, 7200), (1, 1800), (3, 600), (0.2, 36000)])
    return nq("Une batterie débite %s A pendant %s s. Quelle charge électrique a circulé ?" % (num(I), num(t)), I * t, [I / t, t / I, I * t / 3600], "C", "Q = I × Δt = %s C." % num(I * t))


def UNITS(grade):
    return [
        H("P", "composition-d-un-systeme-chimique", "Composition d’un système chimique", "Concentration molaire",
          "Les élèves déterminent la composition d’un système (quantités de matière, concentrations en quantité de matière), réalisent une dilution et un dosage par spectrophotométrie (loi de Beer-Lambert).",
          "quantité de matière, masse molaire, volume molaire des gaz, concentration en quantité de matière c = n : V, dilution, absorbance, loi de Beer-Lambert, dosage par étalonnage",
          "c = n : V", "L’absorbance est proportionnelle à la concentration : A = k × c.",
          ["La concentration en quantité de matière c = n : V s’exprime en mol/L. Elle se relie à la concentration en masse : Cm = c × M.",
           "Pour un gaz, à température et pression données, n = V : Vm (Vm ≈ 24 L/mol à 20 °C sous 1 bar).",
           "Une solution colorée absorbe la lumière. Loi de Beer-Lambert : A = k × c, pour une longueur d’onde et une cuve donnée. On trace une droite d’étalonnage pour doser une solution inconnue."],
          [("Absorbances : 0,20 pour 1,0 mmol/L, 0,40 pour 2,0 mmol/L. L’inconnue a A = 0,30. Concentration ?", ["A est proportionnelle à c.", "0,30 : 0,20 × 1,0."], "1,5 mmol/L.")],
          [("On oublie de convertir les mL en L.", "c en mol/L demande un volume en litres."), ("On applique Beer-Lambert à n’importe quelle solution.", "La loi vaut pour des solutions diluées, à λ fixée.")],
          [("Pourquoi mesurer à la longueur d’onde où A est maximale ?", "La mesure est plus précise."), ("Quelle relation entre Cm et c ?", "Cm = c × M.")],
          [("Grandeurs", [("la concentration en quantité de matière", "c = n : V, en mol/L"), ("la concentration en masse", "Cm = m : V, en g/L"), ("l’absorbance", "grandeur sans unité mesurée au spectrophotomètre"),
                          ("le volume molaire", "volume d’une mole de gaz"), ("la masse molaire", "masse d’une mole, en g/mol"), ("le coefficient de Beer-Lambert", "k dans A = k × c")],
            "Que désigne {k} ?", "Quelle grandeur : {v} ?"),
           ("Relations", [("c à partir de n et V", "c = n : V"), ("Cm à partir de c et M", "Cm = c × M"), ("n d’un gaz", "n = V : Vm"), ("dilution", "c₀ × V₀ = c₁ × V₁"), ("Beer-Lambert", "A = k × c"), ("n à partir de m", "n = m : M")],
            "Quelle relation pour {k} ?", None),
           ("Matériel et méthodes", [("le spectrophotomètre", "mesure l’absorbance"), ("la gamme étalon", "solutions de concentrations connues"), ("la droite d’étalonnage", "A en fonction de c"), ("la cuve", "contient la solution à analyser"),
                                     ("le blanc", "réglage du zéro avec le solvant"), ("la fiole jaugée", "prépare un volume précis de solution")],
            "À quoi sert {k} ?", "Qu’est-ce qui {v} ?")],
          ["c = n : V.", "Cm = c × M.", "L’absorbance est proportionnelle à la concentration.", "On fait le blanc avec le solvant.",
           "Lors d’une dilution, la quantité de soluté se conserve.", "Le volume molaire est d’environ 24 L/mol à 20 °C.", "On mesure l’absorbance à λ maximale."],
          [("c = n × V.", "c = n : V."), ("L’absorbance est inversement proportionnelle à c.", "Elle est proportionnelle à c."), ("Cm = c : M.", "Cm = c × M."), ("Diluer augmente la quantité de soluté.", "Elle se conserve."),
           ("Beer-Lambert vaut pour toute concentration.", "Pour des solutions diluées.")],
          "la composition d’un système", "matter", calc=f_c),

        H("P", "suivi-d-une-transformation-et-avancement", "Suivi d’une transformation : avancement", "Avancement",
          "Les élèves établissent un tableau d’avancement, déterminent l’avancement maximal et le réactif limitant et décrivent l’état final d’un système.",
          "état initial, état final, avancement x, tableau d’avancement, avancement maximal, réactif limitant, mélange stœchiométrique, transformation totale",
          "xmax = plus petite valeur de n(réactif) : coefficient", "Le réactif limitant est celui qui donne le plus petit xmax.",
          ["L’avancement x (en mol) décrit l’évolution du système. Pour aA + bB → cC + dD, à l’avancement x : n(A) = n₀(A) − a x, n(B) = n₀(B) − b x, n(C) = c x.",
           "Pour une transformation totale, xmax est la plus petite des valeurs n₀(A) : a et n₀(B) : b. Le réactif correspondant est limitant.",
           "Si n₀(A) : a = n₀(B) : b, le mélange initial est stœchiométrique : les deux réactifs sont épuisés ensemble."],
          [("N₂ + 3 H₂ → 2 NH₃ avec 1 mol de N₂ et 2,4 mol de H₂.", ["1 : 1 = 1 et 2,4 : 3 = 0,8.", "xmax = 0,8 mol, H₂ limitant."], "On forme 1,6 mol de NH₃, il reste 0,2 mol de N₂.")],
          [("Le réactif limitant est celui en plus petite quantité.", "On compare n₀ : coefficient."), ("On oublie les coefficients dans le tableau.", "n(B) = n₀(B) − b x.")],
          [("Qu’est-ce qu’une transformation totale ?", "Le réactif limitant est entièrement consommé."), ("Comment suivre une transformation ?", "Par mesure de pression, de volume de gaz, d’absorbance ou de conductivité.")],
          [("Vocabulaire", [("l’avancement", "quantité x qui décrit l’évolution"), ("l’avancement maximal", "valeur de x quand le limitant est épuisé"), ("le réactif limitant", "entièrement consommé"),
                            ("le réactif en excès", "reste à l’état final"), ("le mélange stœchiométrique", "réactifs épuisés en même temps"), ("l’état initial", "système avant la réaction"), ("l’état final", "système à la fin de la réaction")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Tableau d’avancement", [("n(A) à l’avancement x pour aA", "n₀(A) − a x"), ("n(C) formé pour cC", "c x"), ("xmax", "min(n₀(A) : a ; n₀(B) : b)"), ("n(B) restant à l’état final", "n₀(B) − b xmax"),
                                     ("unité de l’avancement", "la mole"), ("n(C) à l’état initial", "0 si C est absent au départ")],
            "Comment s’écrit {k} ?", None),
           ("Suivi expérimental", [("formation d’un gaz", "mesure de pression ou de volume"), ("espèce colorée", "mesure d’absorbance"), ("ions en solution", "mesure de conductivité"), ("acide ou base", "mesure de pH"),
                                   ("précipité", "mesure de masse après filtration"), ("changement de couleur", "repère qualitatif de la fin de réaction")],
            "Quelle mesure pour suivre : {k} ?", None)],
          ["xmax correspond à l’épuisement du réactif limitant.", "On compare n₀ : coefficient pour trouver le limitant.", "L’avancement s’exprime en mol.", "Dans un mélange stœchiométrique, les réactifs sont épuisés ensemble.",
           "n(C) = c × x pour un produit absent au départ.", "Le réactif en excès reste à l’état final.", "On peut suivre une transformation par absorbance."],
          [("Le limitant est celui en plus petite quantité initiale.", "On compare n₀ : coefficient."), ("L’avancement s’exprime en g.", "En mol."), ("Le réactif en excès est épuisé.", "Il en reste."),
           ("n(A) = n₀(A) + a x.", "n(A) = n₀(A) − a x."), ("Dans un mélange stœchiométrique, il reste un réactif.", "Les deux sont épuisés.")],
          "l’avancement", "matter", calc=f_av),

        H("P", "oxydoreduction-et-titrage", "Oxydoréduction et titrage", "Titrage",
          "Les élèves identifient des couples oxydant/réducteur, écrivent des demi-équations et l’équation d’oxydoréduction, et exploitent un titrage colorimétrique à l’équivalence.",
          "oxydant, réducteur, couple Ox/Red, demi-équation électronique, oxydation, réduction, titrage, réactif titrant, réactif titré, équivalence, changement de réactif limitant",
          "Un oxydant capte des électrons, un réducteur en cède", "À l’équivalence, les réactifs ont été introduits dans les proportions stœchiométriques.",
          ["Un couple oxydant/réducteur s’écrit Ox/Red avec la demi-équation Ox + n e⁻ = Red. Exemple : Cu²⁺ + 2 e⁻ = Cu.",
           "Dans une réaction d’oxydoréduction, le réducteur d’un couple cède des électrons à l’oxydant d’un autre couple. Les électrons ne figurent pas dans l’équation bilan.",
           "Lors d’un titrage, on verse le réactif titrant jusqu’à l’équivalence (changement de réactif limitant), repérée par un changement de couleur. Pour aA + bB, à l’équivalence : n(A) : a = n(B) : b."],
          [("Couples Fe³⁺/Fe²⁺ et Ce⁴⁺/Ce³⁺. Équation ?", ["Fe²⁺ = Fe³⁺ + e⁻.", "Ce⁴⁺ + e⁻ = Ce³⁺."], "Fe²⁺ + Ce⁴⁺ → Fe³⁺ + Ce³⁺")],
          [("L’oxydant cède des électrons.", "L’oxydant capte des électrons."), ("À l’équivalence, les quantités sont toujours égales.", "Elles sont dans les proportions stœchiométriques n(A) : a = n(B) : b.")],
          [("Pourquoi le diiode est-il un bon indicateur ?", "Sa couleur disparaît quand il est entièrement consommé."), ("Qu’est-ce qu’une oxydation ?", "Une perte d’électrons par le réducteur.")],
          [("Couples", [("Cu²⁺/Cu", "Cu²⁺ + 2 e⁻ = Cu"), ("Fe²⁺/Fe", "Fe²⁺ + 2 e⁻ = Fe"), ("Zn²⁺/Zn", "Zn²⁺ + 2 e⁻ = Zn"), ("Ag⁺/Ag", "Ag⁺ + e⁻ = Ag"), ("I₂/I⁻", "I₂ + 2 e⁻ = 2 I⁻"),
                        ("H⁺/H₂", "2 H⁺ + 2 e⁻ = H₂"), ("Fe³⁺/Fe²⁺", "Fe³⁺ + e⁻ = Fe²⁺"), ("S₄O₆²⁻/S₂O₃²⁻", "S₄O₆²⁻ + 2 e⁻ = 2 S₂O₃²⁻")],
            "Quelle demi-équation pour le couple {k} ?", "Quel couple : {v} ?"),
           ("Vocabulaire", [("l’oxydant", "espèce qui capte des électrons"), ("le réducteur", "espèce qui cède des électrons"), ("l’oxydation", "perte d’électrons"), ("la réduction", "gain d’électrons"),
                            ("l’équivalence", "changement de réactif limitant"), ("le réactif titrant", "solution de concentration connue dans la burette"), ("le réactif titré", "espèce dont on cherche la quantité")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Oxydant ou réducteur ?", {"des oxydants": ["Cu²⁺", "I₂", "Ag⁺", "MnO₄⁻", "Fe³⁺", "O₂"], "des réducteurs": ["Zn", "Fe", "I⁻", "H₂", "S₂O₃²⁻", "Fe²⁺"]})],
          ["Un oxydant capte des électrons.", "Un réducteur cède des électrons.", "Les électrons n’apparaissent pas dans l’équation bilan.", "À l’équivalence, on change de réactif limitant.",
           "Une oxydation est une perte d’électrons.", "Le réactif titrant est dans la burette.", "Cu²⁺ est l’oxydant du couple Cu²⁺/Cu."],
          [("L’oxydant cède des électrons.", "Il en capte."), ("Les électrons apparaissent dans l’équation bilan.", "Ils n’y apparaissent pas."), ("Une réduction est une perte d’électrons.", "C’est un gain."),
           ("À l’équivalence, il reste du réactif titré.", "Il est entièrement consommé."), ("Zn est un oxydant.", "C’est un réducteur.")],
          "l’oxydoréduction", "matter", calc=f_titr),

        H("P", "structure-des-molecules-et-cohesion", "Structure des molécules et cohésion de la matière", "Molécules et cohésion",
          "Les élèves établissent des schémas de Lewis, prévoient la géométrie et la polarité des molécules, et expliquent la cohésion des solides et la solubilité par les interactions.",
          "schéma de Lewis, doublets liants et non liants, géométrie, électronégativité, liaison polarisée, molécule polaire, interactions de van der Waals, liaison hydrogène, solubilité, miscibilité",
          "Polaire si les charges partielles ne se compensent pas", "Le semblable dissout le semblable : polaire avec polaire.",
          ["Un schéma de Lewis montre les doublets liants (liaisons) et non liants. Les atomes respectent la règle du duet (H) ou de l’octet.",
           "Une liaison entre deux atomes d’électronégativités différentes est polarisée. Une molécule est polaire si les charges partielles ne se compensent pas (H₂O polaire, CO₂ apolaire, linéaire).",
           "La cohésion des solides moléculaires vient des interactions de van der Waals et des liaisons hydrogène. Une espèce polaire est soluble dans un solvant polaire comme l’eau."],
          [("CO₂ a deux liaisons polarisées. Est-il polaire ?", ["La molécule est linéaire.", "Les deux charges partielles se compensent."], "Non, il est apolaire.")],
          [("Une molécule avec des liaisons polarisées est toujours polaire.", "Il faut regarder la géométrie : CO₂ est apolaire."), ("La liaison hydrogène est une liaison covalente.", "C’est une interaction plus faible, entre molécules.")],
          [("Pourquoi l’eau a-t-elle une température d’ébullition élevée ?", "Les liaisons hydrogène entre molécules d’eau sont fortes."), ("Pourquoi l’huile ne se mélange-t-elle pas à l’eau ?", "Elle est apolaire, l’eau est polaire.")],
          [("Géométrie", [("CH₄", "tétraédrique"), ("NH₃", "pyramidale"), ("H₂O", "coudée"), ("CO₂", "linéaire"), ("HCl", "linéaire (diatomique)"), ("BF₃", "plane triangulaire"), ("CCl₄", "tétraédrique (apolaire)")],
            "Quelle est la géométrie de {k} ?", None),
           ("Polaire ou apolaire ?", {"des molécules polaires": ["H₂O", "NH₃", "HCl", "l’éthanol", "le méthanal"], "des molécules apolaires": ["CO₂", "CH₄", "O₂", "le cyclohexane", "CCl₄", "N₂", "H₂"]}),
           ("Vocabulaire", [("l’électronégativité", "aptitude d’un atome à attirer les électrons d’une liaison"), ("un doublet non liant", "paire d’électrons qui ne forme pas de liaison"), ("la liaison hydrogène", "interaction entre un H lié à O ou N et un autre O ou N"),
                            ("les interactions de van der Waals", "interactions faibles entre toutes les molécules"), ("une liaison polarisée", "liaison entre atomes d’électronégativités différentes"), ("la règle de l’octet", "8 électrons sur la couche externe"),
                            ("un solvant polaire", "dissout les espèces polaires et ioniques")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["CO₂ est apolaire.", "H₂O est polaire.", "La molécule d’eau est coudée.", "Le méthane est tétraédrique.",
           "Les liaisons hydrogène expliquent l’ébullition élevée de l’eau.", "Une espèce polaire est soluble dans l’eau.", "L’hydrogène respecte la règle du duet."],
          [("Toute molécule à liaisons polarisées est polaire.", "La géométrie compte."), ("La liaison hydrogène est covalente.", "C’est une interaction intermoléculaire."), ("L’eau est linéaire.", "Elle est coudée."),
           ("Le cyclohexane est polaire.", "Il est apolaire."), ("Le méthane est plan.", "Il est tétraédrique.")],
          "la structure des molécules", "matter"),

        H("P", "chimie-organique-et-combustions", "Molécules organiques et combustions", "Chimie organique",
          "Les élèves identifient les familles fonctionnelles, nomment des molécules simples, écrivent l’équation d’une combustion et calculent l’énergie libérée.",
          "chaîne carbonée, formule semi-développée, squelettique, groupes caractéristiques, alcools, aldéhydes, cétones, acides carboxyliques, combustion complète, énergie molaire de combustion",
          "Le groupe caractéristique donne la famille", "Une combustion complète d’un composé organique donne CO₂ et H₂O.",
          ["La formule semi-développée montre toutes les liaisons sauf celles avec H. La formule topologique (squelettique) ne montre que les liaisons C–C et les hétéroatomes.",
           "Groupes caractéristiques : hydroxyle –OH (alcool), carbonyle C=O (aldéhyde en bout de chaîne, cétone dans la chaîne), carboxyle –COOH (acide carboxylique).",
           "Combustion complète : composé + O₂ → CO₂ + H₂O. Énergie libérée : E = n × Em, avec Em l’énergie molaire de combustion."],
          [("Nom et famille de CH₃–CH₂–OH ?", ["Deux carbones : préfixe éth-.", "Groupe –OH : alcool."], "Éthanol, famille des alcools.")],
          [("Une cétone a son C=O en bout de chaîne.", "Elle a son C=O à l’intérieur de la chaîne, l’aldéhyde en bout."), ("La combustion incomplète est sans danger.", "Elle produit du CO toxique et des suies.")],
          [("Pourquoi les biocarburants ?", "Ils viennent de la biomasse : le CO₂ émis a été capté récemment par les plantes."), ("Que veut dire méth-, éth-, prop-, but- ?", "1, 2, 3, 4 atomes de carbone dans la chaîne.")],
          [("Familles", [("l’éthanol", "alcool"), ("le méthanol", "alcool"), ("l’acide éthanoïque", "acide carboxylique"), ("le propanal", "aldéhyde"), ("la propanone", "cétone"), ("l’éthanal", "aldéhyde"),
                         ("l’acide méthanoïque", "acide carboxylique"), ("la butanone", "cétone"), ("le propan-2-ol", "alcool")],
            "À quelle famille appartient {k} ?", None, ("ester", "amine")),
           ("Groupes caractéristiques", [("–OH", "groupe hydroxyle"), ("–COOH", "groupe carboxyle"), ("C=O en bout de chaîne", "groupe carbonyle d’un aldéhyde"), ("C=O dans la chaîne", "groupe carbonyle d’une cétone"),
                                         ("–COO– entre deux chaînes", "groupe ester"), ("–NH₂", "groupe amine")],
            "Comment s’appelle {k} ?", "Quel groupe : {v} ?"),
           ("Préfixes et nombres de carbones", [("méth-", "1 carbone"), ("éth-", "2 carbones"), ("prop-", "3 carbones"), ("but-", "4 carbones"), ("pent-", "5 carbones"), ("hex-", "6 carbones")],
            "Combien de carbones indique le préfixe {k} ?", "Quel préfixe pour {v} ?")],
          ["L’éthanol est un alcool.", "Une combustion complète donne CO₂ et H₂O.", "Le groupe carboxyle caractérise les acides carboxyliques.", "La propanone est une cétone.",
           "Le préfixe éth- indique deux carbones.", "Une combustion incomplète produit du monoxyde de carbone.", "E = n × Em."],
          [("Une cétone a son C=O en bout de chaîne.", "C’est un aldéhyde."), ("La combustion complète produit du CO.", "Elle produit CO₂ et H₂O."), ("Le préfixe prop- indique 2 carbones.", "Il indique 3 carbones."),
           ("L’acide éthanoïque est un alcool.", "C’est un acide carboxylique."), ("La combustion incomplète est sans danger.", "Elle produit du CO toxique.")],
          "la chimie organique", "matter", calc=f_comb),

        H("P", "interactions-fondamentales-et-champs", "Interactions fondamentales et champs", "Champs et interactions",
          "Les élèves utilisent les lois de Coulomb et de la gravitation universelle et décrivent les champs électrostatique, de gravitation et de pesanteur.",
          "charge électrique, loi de Coulomb, interaction gravitationnelle, constante G, champ électrostatique, condensateur plan, champ de gravitation, champ de pesanteur, lignes de champ",
          "F = k q q’ : d² et F = G m m’ : d²", "Les deux forces diminuent comme le carré de la distance.",
          ["Loi de Coulomb : F = k × |q × q’| : d², k = 9,0 × 10⁹ N·m²/C². Des charges de même signe se repoussent, de signes contraires s’attirent.",
           "Loi de la gravitation universelle : F = G × m × m’ : d², G = 6,67 × 10⁻¹¹ N·m²/kg². Elle est toujours attractive.",
           "Un champ décrit l’action à distance : F = q × E (électrostatique), P = m × g (pesanteur). Entre deux plaques chargées, le champ est uniforme : E = U : d."],
          [("Si la distance entre deux masses double, que devient la force ?", ["F est inversement proportionnelle à d².", "2² = 4."], "Elle est divisée par 4.")],
          [("La force gravitationnelle peut être répulsive.", "Elle est toujours attractive."), ("Si d double, F est divisée par 2.", "Elle est divisée par 4.")],
          [("Pourquoi la gravitation domine-t-elle à grande échelle ?", "Les astres sont électriquement neutres mais très massifs."), ("Que représente une ligne de champ ?", "Une courbe tangente en chaque point au vecteur champ.")],
          [("Constantes et grandeurs", [("la constante de gravitation G", "6,67 × 10⁻¹¹ N·m²/kg²"), ("la constante de Coulomb k", "9,0 × 10⁹ N·m²/C²"), ("la charge élémentaire e", "1,60 × 10⁻¹⁹ C"), ("le champ de pesanteur terrestre g", "environ 9,81 N/kg"),
                                        ("l’unité du champ électrique", "le volt par mètre"), ("l’unité de la charge", "le coulomb")],
            "Quelle valeur ou unité pour {k} ?", "Qu’est-ce qui vaut {v} ?"),
           ("Si l’on change…", [("la distance est doublée", "la force est divisée par 4"), ("la distance est divisée par 2", "la force est multipliée par 4"), ("une des masses est doublée", "la force est doublée"),
                                ("les deux charges changent de signe", "la force garde la même valeur et le même sens"), ("une seule charge change de signe", "l’attraction devient répulsion ou l’inverse"), ("la distance est triplée", "la force est divisée par 9")],
            "Que devient la force si {k} ?", None),
           ("Champs", [("le champ électrostatique", "F = q × E"), ("le champ de pesanteur", "P = m × g"), ("le champ entre deux plaques", "uniforme, E = U : d"), ("le champ autour d’une charge ponctuelle", "radial"),
                       ("le champ de gravitation de la Terre", "dirigé vers le centre de la Terre"), ("les lignes de champ", "tangentes au vecteur champ")],
            "Que sais-tu sur {k} ?", None)],
          ["La force gravitationnelle est toujours attractive.", "Des charges de signes contraires s’attirent.", "Si d double, la force est divisée par 4.", "Entre deux plaques, le champ est uniforme.",
           "F = q × E.", "G = 6,67 × 10⁻¹¹ N·m²/kg².", "Le champ de pesanteur terrestre vaut environ 9,81 N/kg."],
          [("La gravitation peut être répulsive.", "Elle est toujours attractive."), ("Si d double, F est divisée par 2.", "Elle est divisée par 4."), ("Des charges de même signe s’attirent.", "Elles se repoussent."),
           ("E s’exprime en newtons.", "En V/m ou N/C."), ("Le champ entre deux plaques est radial.", "Il est uniforme.")],
          "les interactions", "forces-and-motion", calc=f_champ),

        H("P", "mouvement-et-forces-premiere", "Mouvement d’un système et forces", "Forces et mouvement",
          "Les élèves relient la variation du vecteur vitesse à la somme des forces (approche de la deuxième loi de Newton) et exploitent des chronophotographies.",
          "système, référentiel galiléen, vecteur vitesse, variation du vecteur vitesse, somme des forces, Δv = (ΣF : m) × Δt, principe d’inertie, chute libre",
          "m × Δv ≈ ΣF × Δt", "La variation du vecteur vitesse a la direction et le sens de la somme des forces.",
          ["Dans un référentiel galiléen, si la somme des forces est nulle, le vecteur vitesse est constant (principe d’inertie).",
           "Sinon, le vecteur vitesse varie : m × Δv ≈ ΣF × Δt. La variation Δv a la même direction et le même sens que ΣF.",
           "Une même force produit une variation de vitesse plus petite sur un système plus massif. En chute libre, ΣF = P et Δv est vertical vers le bas."],
          [("Une voiture de 1 000 kg passe de 0 à 20 m/s en 10 s. Somme des forces ?", ["ΣF ≈ m × Δv : Δt.", "1 000 × 20 : 10."], "2 000 N, dans le sens du mouvement.")],
          [("La vitesse a toujours le sens de la force.", "C’est la variation de la vitesse qui a le sens de la force."), ("Un objet lancé vers le haut subit une force vers le haut.", "Seul le poids agit (sans frottement), vers le bas.")],
          [("Pourquoi une balle lancée ralentit-elle en montant ?", "Le poids, vers le bas, fait diminuer la vitesse verticale."), ("Qu’est-ce qu’un référentiel galiléen ?", "Un référentiel où le principe d’inertie est vérifié, comme le référentiel terrestre sur de courtes durées.")],
          [("Situations", [("vitesse constante en ligne droite", "somme des forces nulle"), ("vitesse qui augmente en ligne droite", "somme des forces dans le sens du mouvement"), ("vitesse qui diminue en ligne droite", "somme des forces opposée au mouvement"),
                           ("mouvement circulaire uniforme", "somme des forces vers le centre"), ("chute libre", "seul le poids agit"), ("parachutiste à vitesse limite", "poids et frottements se compensent")],
            "Que dire de la somme des forces : {k} ?", None),
           ("Chronophotographie", [("points également espacés et alignés", "mouvement rectiligne uniforme"), ("points de plus en plus espacés", "mouvement accéléré"), ("points de plus en plus rapprochés", "mouvement ralenti"),
                                   ("vecteurs vitesse de même longueur sur un cercle", "mouvement circulaire uniforme"), ("Δv toujours vertical vers le bas", "chute libre"), ("Δv nul", "forces qui se compensent")],
            "Quel mouvement ou quelle situation : {k} ?", None),
           ("Grandeurs", [("Δv", "variation du vecteur vitesse"), ("ΣF", "somme vectorielle des forces"), ("le référentiel galiléen", "où vaut le principe d’inertie"), ("la masse", "s’oppose à la variation de vitesse"),
                          ("le poids", "force verticale vers le bas"), ("la chute libre", "seul le poids agit")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Δv a le sens de la somme des forces.", "Si ΣF = 0, le vecteur vitesse est constant.", "En chute libre, seul le poids agit.", "Une masse plus grande varie moins de vitesse pour la même force.",
           "Un mouvement circulaire uniforme demande une force vers le centre.", "m × Δv ≈ ΣF × Δt.", "Le parachutiste à vitesse limite subit des forces compensées."],
          [("La vitesse a toujours le sens de la force.", "C’est Δv qui a ce sens."), ("Un objet lancé vers le haut subit une force vers le haut.", "Seul le poids agit."), ("Un mouvement circulaire uniforme ne demande pas de force.", "Il faut une force vers le centre."),
           ("Une masse plus grande accélère plus.", "Elle accélère moins."), ("Si ΣF = 0, l’objet s’arrête forcément.", "Il garde une vitesse constante.")],
          "le mouvement", "forces-and-motion", calc=f_dyn),

        H("P", "energie-mecanique-et-travail", "Travail, énergie cinétique et énergie mécanique", "Énergie mécanique",
          "Les élèves calculent le travail d’une force, appliquent le théorème de l’énergie cinétique et étudient la conservation ou la non-conservation de l’énergie mécanique.",
          "travail d’une force W = F × d × cos α, énergie cinétique, théorème de l’énergie cinétique, énergie potentielle de pesanteur, énergie mécanique, forces conservatives, frottements",
          "Em = Ec + Epp", "Sans frottements, l’énergie mécanique se conserve.",
          ["Le travail d’une force constante sur un déplacement AB : W = F × AB × cos α. Il est moteur si W > 0, résistant si W < 0.",
           "Théorème de l’énergie cinétique : ΔEc = somme des travaux des forces. Ec = ½ m v².",
           "Epp = m × g × z. Em = Ec + Epp. Sans frottements, Em se conserve. Avec frottements, Em diminue : l’énergie perdue devient de la chaleur."],
          [("Un skieur part sans vitesse de 20 m de haut, sans frottement. Vitesse en bas ?", ["Epp devient Ec : g h = ½ v².", "v = √(2 × 9,81 × 20)."], "Environ 19,8 m/s.")],
          [("Le travail du poids dépend du chemin suivi.", "Il ne dépend que de la différence d’altitude."), ("Avec frottements, l’énergie disparaît.", "Elle est convertie en énergie thermique.")],
          [("Quand le travail d’une force est-il nul ?", "Quand la force est perpendiculaire au déplacement."), ("Pourquoi une balle rebondit-elle de moins en moins haut ?", "À chaque choc, une partie de l’énergie mécanique est dissipée.")],
          [("Signe du travail", [("force dans le sens du déplacement", "travail moteur"), ("force opposée au déplacement", "travail résistant"), ("force perpendiculaire au déplacement", "travail nul"),
                                 ("poids lors d’une descente", "travail moteur"), ("poids lors d’une montée", "travail résistant"), ("frottements", "travail résistant"), ("réaction normale du sol sur un plan horizontal", "travail nul")],
            "Quel est le travail de {k} ?", None, ("travail infini",)),
           ("Énergies", [("l’énergie cinétique", "½ m v²"), ("l’énergie potentielle de pesanteur", "m g z"), ("l’énergie mécanique", "Ec + Epp"), ("le travail d’une force", "F × d × cos α"), ("le joule", "unité d’énergie et de travail"),
                         ("le théorème de l’énergie cinétique", "ΔEc = somme des travaux")],
            "Que désigne {k} ?", "Quoi : {v} ?"),
           ("Conservation ou non ?", {"des situations où Em se conserve": ["chute libre sans air", "pendule idéal sans frottement", "glissade sur une glace parfaite", "bille sur un rail sans frottement", "satellite en orbite", "plongeon sans résistance de l’air"],
                                      "des situations où Em diminue": ["voiture qui freine", "balle qui rebondit de moins en moins haut", "parachutiste à vitesse constante", "luge freinée par la neige", "pendule réel qui s’arrête", "cycliste qui roule en roue libre et ralentit"]})],
          ["Em = Ec + Epp.", "Sans frottements, Em se conserve.", "Le travail d’une force perpendiculaire au déplacement est nul.", "Le poids a un travail moteur à la descente.",
           "ΔEc = somme des travaux des forces.", "Les frottements convertissent de l’énergie en chaleur.", "Ec = ½ m v²."],
          [("Le travail du poids dépend du chemin.", "Il dépend de la différence d’altitude."), ("Avec frottements, Em se conserve.", "Elle diminue."), ("Ec = m v².", "Ec = ½ m v²."),
           ("Le poids a un travail résistant à la descente.", "Il est moteur."), ("Une force perpendiculaire au déplacement travaille beaucoup.", "Son travail est nul.")],
          "l’énergie mécanique", "energy", calc=f_energie),

        H("P", "ondes-mecaniques-progressives", "Ondes mécaniques progressives", "Ondes mécaniques",
          "Les élèves décrivent la propagation d’une onde mécanique, calculent une célérité et un retard, et relient période, fréquence et longueur d’onde.",
          "perturbation, milieu matériel, onde transversale, longitudinale, célérité v, retard τ, onde périodique, période T, longueur d’onde λ, λ = v × T",
          "λ = v × T = v : f", "Une onde transporte de l’énergie, pas de matière.",
          ["Une onde mécanique est la propagation d’une perturbation dans un milieu matériel, sans transport de matière. Transversale : la perturbation est perpendiculaire à la direction de propagation (corde). Longitudinale : parallèle (son).",
           "La célérité v = d : Δt. Un point situé à la distance d de la source reproduit son mouvement avec un retard τ = d : v.",
           "Une onde périodique a une période T (temporelle) et une longueur d’onde λ (spatiale) : λ = v × T."],
          [("Une onde sur l’eau a λ = 2 cm et f = 10 Hz. Célérité ?", ["v = λ × f.", "0,02 × 10."], "0,2 m/s.")],
          [("L’onde transporte l’eau avec elle.", "Le bouchon monte et descend sur place : pas de transport de matière."), ("Le son se propage dans le vide.", "Il a besoin d’un milieu matériel.")],
          [("Comment mesurer λ ?", "En mesurant la distance entre deux points qui vibrent en phase."), ("Le son est-il transversal ?", "Non, dans l’air c’est une onde longitudinale.")],
          [("Type d’onde", [("onde le long d’une corde secouée", "transversale"), ("son dans l’air", "longitudinale"), ("compression d’un ressort", "longitudinale"), ("vague à la surface de l’eau", "transversale (en première approche)"),
                            ("ola dans un stade", "transversale"), ("onde sismique P", "longitudinale"), ("onde sismique S", "transversale")],
            "Quel type d’onde : {k} ?", None, ("électromagnétique",)),
           ("Grandeurs", [("la célérité", "vitesse de propagation de l’onde"), ("le retard", "durée entre deux points du milieu"), ("la période", "durée d’un motif"), ("la longueur d’onde", "distance parcourue pendant une période"),
                          ("la fréquence", "nombre de périodes par seconde"), ("l’amplitude", "valeur maximale de la perturbation")],
            "Que désigne {k} ?", "Quelle grandeur : {v} ?"),
           ("Relations", [("célérité à partir de d et Δt", "v = d : Δt"), ("retard", "τ = d : v"), ("longueur d’onde à partir de v et T", "λ = v × T"), ("fréquence", "f = 1 : T"), ("longueur d’onde à partir de v et f", "λ = v : f")],
            "Quelle relation pour {k} ?", None, ("v = λ : T²",))],
          ["Une onde transporte de l’énergie sans transporter de matière.", "Le son dans l’air est une onde longitudinale.", "λ = v × T.", "Le retard vaut τ = d : v.",
           "Une onde mécanique a besoin d’un milieu matériel.", "L’onde le long d’une corde est transversale.", "f = 1 : T."],
          [("L’onde transporte la matière.", "Elle transporte de l’énergie."), ("Le son se propage dans le vide.", "Il a besoin d’un milieu."), ("λ = v : T.", "λ = v × T."),
           ("Le son dans l’air est transversal.", "Il est longitudinal."), ("La période est une distance.", "C’est une durée.")],
          "les ondes mécaniques", "waves-and-light", calc=f_onde),

        H("P", "lumiere-lentilles-et-photon", "Lentilles, couleurs et modèle du photon", "Lumière et photon",
          "Les élèves utilisent la relation de conjugaison et le grandissement d’une lentille mince, expliquent la couleur des objets et utilisent le modèle du photon (E = h × ν).",
          "lentille convergente, distance focale, relation de conjugaison, grandissement, synthèse additive et soustractive, couleur perçue, photon, E = h × ν, électronvolt, niveaux d’énergie",
          "E = h × ν = h × c : λ", "Un atome émet ou absorbe un photon dont l’énergie est l’écart entre deux niveaux.",
          ["Relation de conjugaison : 1/OA’ − 1/OA = 1/f’ (distances algébriques). Grandissement γ = OA’ : OA = A’B’ : AB.",
           "Synthèse additive : rouge + vert + bleu = blanc. Synthèse soustractive : cyan, magenta, jaune. La couleur d’un objet est celle de la lumière qu’il diffuse.",
           "La lumière est faite de photons d’énergie E = h × ν (h = 6,63 × 10⁻³⁴ J·s). Les atomes ont des niveaux d’énergie quantifiés : un photon est émis ou absorbé quand ΔE = h × ν."],
          [("Photon de λ = 600 nm : énergie ?", ["E = h × c : λ.", "6,63 × 10⁻³⁴ × 3,00 × 10⁸ : 600 × 10⁻⁹."], "3,32 × 10⁻¹⁹ J, soit environ 2,1 eV.")],
          [("Un objet rouge émet du rouge.", "Il diffuse le rouge et absorbe les autres couleurs de la lumière reçue."), ("Plus λ est grande, plus le photon est énergétique.", "E est inversement proportionnelle à λ.")],
          [("Pourquoi un objet vert paraît-il noir sous lumière rouge ?", "Il absorbe le rouge et ne reçoit pas de vert à diffuser."), ("Qu’est-ce qu’un électronvolt ?", "1 eV = 1,60 × 10⁻¹⁹ J.")],
          [("Synthèses", [("rouge + vert", "jaune"), ("rouge + bleu", "magenta"), ("vert + bleu", "cyan"), ("rouge + vert + bleu", "blanc"), ("filtre cyan + filtre jaune", "vert"), ("filtre magenta + filtre jaune", "rouge"),
                          ("filtre cyan + filtre magenta", "bleu")],
            "Quelle couleur donne {k} ?", None),
           ("Lentilles", [("la distance focale", "distance du centre optique au foyer"), ("la vergence", "inverse de la distance focale, en dioptries"), ("le grandissement", "rapport A’B’ : AB"), ("une image réelle", "peut être projetée sur un écran"),
                          ("un grandissement négatif", "image renversée"), ("le foyer image", "point où convergent les rayons parallèles à l’axe")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Photons", [("E = h × ν", "énergie d’un photon"), ("h", "constante de Planck"), ("1 eV", "1,60 × 10⁻¹⁹ J"), ("photon ultraviolet", "plus énergétique qu’un photon visible"), ("photon infrarouge", "moins énergétique qu’un photon visible"),
                        ("spectre de raies", "niveaux d’énergie quantifiés")],
            "Que sais-tu de {k} ?", "Qu’est-ce qui correspond à {v} ?")],
          ["E = h × ν.", "Un photon UV est plus énergétique qu’un photon visible.", "Rouge + vert + bleu donnent du blanc.", "Un grandissement négatif signifie une image renversée.",
           "Un objet rouge diffuse le rouge.", "Les niveaux d’énergie d’un atome sont quantifiés.", "1 eV = 1,60 × 10⁻¹⁹ J."],
          [("Plus λ est grande, plus le photon est énergétique.", "C’est l’inverse."), ("Un objet rouge émet du rouge.", "Il diffuse le rouge."), ("Rouge + vert donnent du bleu.", "Ils donnent du jaune."),
           ("Un photon infrarouge est plus énergétique qu’un photon UV.", "C’est l’inverse."), ("Une image virtuelle se projette sur un écran.", "C’est une image réelle qui se projette.")],
          "la lumière", "waves-and-light", calc=f_photon),

        H("P", "energie-electrique-et-rendement", "Énergie électrique, effet Joule et rendement", "Énergie électrique",
          "Les élèves modélisent une source réelle, calculent puissances et énergies électriques, l’effet Joule et le rendement d’un convertisseur.",
          "porteurs de charge, intensité I = Q : Δt, source de tension réelle, puissance P = U × I, effet Joule P = R × I², énergie E = P × Δt, rendement, bilan de puissance",
          "η = puissance utile : puissance reçue", "L’effet Joule transforme de l’énergie électrique en chaleur : P = R × I².",
          ["L’intensité est un débit de charges : I = Q : Δt. Une source réelle de tension a une résistance interne : U = E − r × I.",
           "Puissance électrique P = U × I, énergie E = P × Δt (en J ou en Wh). Dans un conducteur ohmique, la puissance dissipée par effet Joule est P = R × I².",
           "Un convertisseur reçoit une puissance, en restitue une partie sous forme utile et dissipe le reste. Rendement η = Pu : Pa, toujours inférieur à 1."],
          [("Un moteur reçoit 200 W et fournit 150 W mécaniques. Rendement ?", ["η = 150 : 200.", "= 0,75."], "75 %, 50 W sont dissipés.")],
          [("Un rendement peut dépasser 100 %.", "L’énergie utile ne peut pas dépasser l’énergie reçue."), ("L’effet Joule est toujours inutile.", "Il est utile dans un radiateur ou une bouilloire.")],
          [("Pourquoi transporter l’électricité en haute tension ?", "À puissance égale, l’intensité est plus faible, donc les pertes par effet Joule aussi."), ("Que vaut 1 kWh en joules ?", "3,6 × 10⁶ J.")],
          [("Relations", [("puissance électrique", "P = U × I"), ("effet Joule", "P = R × I²"), ("énergie", "E = P × Δt"), ("charge électrique", "Q = I × Δt"), ("rendement", "η = Pu : Pa"), ("source réelle", "U = E − r × I")],
            "Quelle relation pour {k} ?", None, ("P = U : I",)),
           ("Convertisseurs", [("le moteur électrique", "électrique → mécanique, pertes thermiques"), ("la lampe LED", "électrique → lumineuse, peu de pertes"), ("le radiateur", "électrique → thermique, rendement proche de 1"),
                               ("le panneau photovoltaïque", "lumineuse → électrique, rendement d’environ 20 %"), ("l’alternateur", "mécanique → électrique"), ("la batterie en charge", "électrique → chimique")],
            "Que sais-tu de {k} ?", None),
           ("Unités", [("la puissance", "le watt"), ("l’énergie", "le joule"), ("la charge", "le coulomb"), ("l’intensité", "l’ampère"), ("la résistance", "l’ohm"), ("le kilowattheure", "3,6 × 10⁶ J")],
            "Quelle unité ou valeur pour {k} ?", "Qu’est-ce qui correspond à {v} ?")],
          ["P = U × I.", "L’effet Joule vaut P = R × I².", "Un rendement est toujours inférieur à 1.", "1 kWh = 3,6 × 10⁶ J.",
           "La haute tension réduit les pertes par effet Joule.", "I = Q : Δt.", "Une source réelle a une résistance interne."],
          [("Un rendement peut dépasser 100 %.", "Il est toujours inférieur à 100 %."), ("L’effet Joule vaut P = R × I.", "P = R × I²."), ("1 kWh = 1 000 J.", "1 kWh = 3,6 × 10⁶ J."),
           ("La haute tension augmente les pertes.", "Elle les réduit."), ("L’effet Joule est toujours inutile.", "Il est utile dans un radiateur.")],
          "l’énergie électrique", "energy", calc=f_elec),

        H("S", "replication-mitose-et-mutations", "Réplication de l’ADN, mitose et mutations", "Réplication et mitose",
          "Les élèves décrivent la réplication semi-conservative de l’ADN, le cycle cellulaire et la mitose, et l’origine des mutations.",
          "cycle cellulaire, interphase, réplication semi-conservative, ADN polymérase, chromosome à deux chromatides, mitose, clone cellulaire, mutations, agents mutagènes, réparation",
          "La réplication copie l’ADN avant chaque mitose", "Elle est semi-conservative : chaque nouvelle molécule garde un brin ancien.",
          ["Le cycle cellulaire alterne interphase et mitose. Pendant l’interphase, l’ADN est répliqué : chaque chromosome a alors deux chromatides identiques.",
           "La réplication est semi-conservative : les deux brins se séparent, chacun sert de modèle à l’ADN polymérase (A face à T, G face à C).",
           "La mitose (prophase, métaphase, anaphase, télophase) répartit les chromatides : les deux cellules filles sont identiques. Des erreurs de réplication ou des agents mutagènes (UV, tabac) provoquent des mutations."],
          [("Brin modèle : 3’ ATGCCA 5’. Brin formé ?", ["A face à T, G face à C.", "5’ TACGGT 3’."], "TACGGT")],
          [("La mitose produit des cellules différentes.", "Les cellules filles sont génétiquement identiques."), ("Toutes les mutations sont dangereuses.", "Beaucoup sont neutres, certaines sont avantageuses.")],
          [("Qu’est-ce qu’un clone cellulaire ?", "L’ensemble des cellules issues d’une même cellule par mitoses."), ("Pourquoi éviter les coups de soleil ?", "Les UV provoquent des mutations dans les cellules de la peau.")],
          [("Phases de la mitose", [("la prophase", "les chromosomes se condensent"), ("la métaphase", "les chromosomes s’alignent au centre"), ("l’anaphase", "les chromatides se séparent"), ("la télophase", "deux noyaux se reforment"),
                                    ("l’interphase", "l’ADN est répliqué"), ("la cytodiérèse", "le cytoplasme se divise")],
            "Que se passe-t-il pendant {k} ?", "Quelle phase : {v} ?"),
           ("Vocabulaire", [("la réplication", "copie de l’ADN"), ("semi-conservative", "chaque ADN fils garde un brin parental"), ("l’ADN polymérase", "enzyme qui assemble les nucléotides"), ("la chromatide", "une des deux copies d’un chromosome répliqué"),
                            ("une mutation", "modification de la séquence d’ADN"), ("un agent mutagène", "augmente la fréquence des mutations"), ("le centromère", "relie les deux chromatides")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Bases complémentaires", [("A", "T"), ("T", "A"), ("G", "C"), ("C", "G"), ("ATG", "TAC"), ("GGC", "CCG"), ("TTA", "AAT"), ("CAT", "GTA")],
            "Quelle séquence est complémentaire de {k} ?", None, ("U", "AAA"))],
          ["La réplication est semi-conservative.", "La mitose donne deux cellules identiques.", "A est complémentaire de T.", "Les UV sont mutagènes.",
           "L’ADN est répliqué pendant l’interphase.", "Pendant l’anaphase, les chromatides se séparent.", "Beaucoup de mutations sont neutres."],
          [("La mitose produit des cellules différentes.", "Elles sont identiques."), ("La réplication a lieu pendant la mitose.", "Pendant l’interphase."), ("A est complémentaire de G.", "A est complémentaire de T."),
           ("Toutes les mutations sont dangereuses.", "Beaucoup sont neutres."), ("La réplication est conservative.", "Elle est semi-conservative.")],
          "la réplication", "living-things-and-ecosystems"),

        H("S", "expression-du-patrimoine-genetique", "Transcription, traduction et code génétique", "Expression génétique",
          "Les élèves décrivent la transcription de l’ADN en ARN messager, la traduction en protéine selon le code génétique et la relation entre génotype et phénotype.",
          "gène, transcription, ARN polymérase, ARN messager, uracile, épissage, traduction, ribosome, codon, code génétique, acides aminés, phénotype moléculaire, cellulaire, macroscopique",
          "ADN → ARN messager → protéine", "Un codon de trois nucléotides code un acide aminé.",
          ["La transcription a lieu dans le noyau : l’ARN polymérase fabrique un ARN messager complémentaire du brin transcrit (U remplace T). Chez les eucaryotes, l’épissage retire des parties de l’ARN.",
           "La traduction a lieu dans le cytoplasme, sur les ribosomes : chaque codon de l’ARNm correspond à un acide aminé selon le code génétique. AUG est le codon initiateur, UAA, UAG, UGA sont des codons stop.",
           "La séquence d’acides aminés détermine la forme et la fonction de la protéine, donc le phénotype moléculaire, cellulaire et macroscopique."],
          [("Brin transcrit : TAC AAA GGC. ARNm ?", ["On remplace par les complémentaires, U au lieu de T.", "AUG UUU CCG."], "AUG UUU CCG")],
          [("L’ARN contient de la thymine.", "L’ARN contient de l’uracile à la place."), ("La traduction a lieu dans le noyau.", "Elle a lieu dans le cytoplasme, sur les ribosomes.")],
          [("Pourquoi dit-on que le code génétique est redondant ?", "Plusieurs codons codent le même acide aminé."), ("Qu’est-ce que le phénotype ?", "L’ensemble des caractères observables, de la molécule à l’organisme.")],
          [("Étapes", [("la transcription", "ADN → ARN messager dans le noyau"), ("la traduction", "ARN messager → protéine dans le cytoplasme"), ("l’épissage", "élimination de séquences de l’ARN"), ("le codon AUG", "début de la traduction"),
                       ("le codon stop", "fin de la traduction"), ("le ribosome", "lit l’ARNm et assemble les acides aminés"), ("l’ARN polymérase", "fabrique l’ARN messager")],
            "Que désigne {k} ?", "Qu’est-ce qui {v} ?"),
           ("ADN ou ARN ?", {"des propriétés de l’ADN": ["double brin", "contient de la thymine", "contient du désoxyribose", "reste dans le noyau", "molécule très longue et stable", "se réplique avant la mitose"],
                              "des propriétés de l’ARN messager": ["simple brin", "contient de l’uracile", "contient du ribose", "passe dans le cytoplasme", "copie courte d’un gène", "lu par les ribosomes"]}),
           ("Code génétique", [("AUG", "méthionine (codon initiateur)"), ("UUU", "phénylalanine"), ("GGC", "glycine"), ("UAA", "codon stop"), ("UGG", "tryptophane"), ("AAA", "lysine"), ("GCU", "alanine"), ("CCG", "proline")],
            "Que code le codon {k} ?", "Quel codon code : {v} ?")],
          ["La transcription a lieu dans le noyau.", "La traduction a lieu sur les ribosomes.", "L’ARN contient de l’uracile.", "Un codon compte trois nucléotides.",
           "AUG est le codon initiateur.", "Le code génétique est redondant.", "La séquence d’acides aminés détermine la forme de la protéine."],
          [("L’ARN contient de la thymine.", "Il contient de l’uracile."), ("La traduction a lieu dans le noyau.", "Dans le cytoplasme."), ("Un codon compte deux nucléotides.", "Il en compte trois."),
           ("UAA code la méthionine.", "C’est un codon stop."), ("L’ARN messager est double brin.", "Il est simple brin.")],
          "l’expression génétique", "living-things-and-ecosystems"),

        H("S", "enzymes-et-metabolisme", "Enzymes et métabolisme cellulaire", "Enzymes",
          "Les élèves expliquent l’action des enzymes (site actif, spécificité), l’influence de la température et du pH, et l’organisation du métabolisme des cellules.",
          "enzyme, catalyse, substrat, site actif, complexe enzyme-substrat, spécificité, vitesse de réaction, température optimale, pH optimal, dénaturation, métabolisme, voies métaboliques",
          "Une enzyme agit sur un substrat précis", "Chaque enzyme a une température et un pH optimaux.",
          ["Une enzyme est une protéine qui catalyse une réaction : elle l’accélère sans être consommée. Le substrat se fixe sur le site actif, de forme complémentaire.",
           "Une enzyme est spécifique de son substrat et de la réaction. La vitesse dépend de la quantité de substrat, de la température et du pH.",
           "À trop haute température ou à pH extrême, l’enzyme est dénaturée : sa forme change et elle n’agit plus. Le métabolisme est un réseau de réactions enzymatiques."],
          [("L’amylase salivaire agit-elle dans l’estomac (pH 2) ?", ["Son pH optimal est proche de 7.", "À pH 2, elle est inactivée."], "Non, elle cesse d’agir.")],
          [("L’enzyme est consommée pendant la réaction.", "Elle est retrouvée intacte à la fin."), ("Plus il fait chaud, plus l’enzyme agit.", "Au-delà de l’optimum, elle est dénaturée.")],
          [("Pourquoi la fièvre très forte est-elle dangereuse ?", "Des enzymes de l’organisme peuvent être dénaturées."), ("Qu’est-ce qu’une voie métabolique ?", "Une suite de réactions catalysées chacune par une enzyme.")],
          [("Vocabulaire", [("le substrat", "molécule transformée par l’enzyme"), ("le site actif", "partie de l’enzyme où se fixe le substrat"), ("le produit", "molécule formée"), ("la dénaturation", "perte de la forme de l’enzyme"),
                            ("la spécificité", "une enzyme agit sur un substrat précis"), ("le complexe enzyme-substrat", "association temporaire"), ("la catalyse", "accélération d’une réaction")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Enzymes et substrats", [("l’amylase", "amidon"), ("la pepsine", "protéines dans l’estomac"), ("la lipase", "lipides"), ("la lactase", "lactose"), ("la catalase", "eau oxygénée"), ("la saccharase", "saccharose"), ("la trypsine", "protéines dans l’intestin")],
            "Quel substrat transforme {k} ?", "Quelle enzyme agit sur {v} ?"),
           ("Conditions", [("température de 37 °C pour une enzyme humaine", "activité maximale"), ("température de 80 °C pour une enzyme humaine", "dénaturation"), ("température de 0 °C", "activité très ralentie mais réversible"),
                           ("pH 2 pour la pepsine", "activité maximale"), ("pH 2 pour l’amylase salivaire", "activité nulle"), ("plus de substrat, enzyme non saturée", "réaction plus rapide")],
            "Que devient l’activité : {k} ?", None)],
          ["Une enzyme accélère une réaction sans être consommée.", "Le substrat se fixe sur le site actif.", "Une enzyme est spécifique.", "La chaleur excessive dénature les enzymes.",
           "La pepsine agit à pH acide.", "Le métabolisme est un réseau de réactions enzymatiques.", "L’amylase transforme l’amidon."],
          [("L’enzyme est consommée.", "Elle est retrouvée intacte."), ("Plus il fait chaud, plus l’enzyme agit, sans limite.", "Elle est dénaturée au-delà de l’optimum."), ("Une enzyme agit sur tous les substrats.", "Elle est spécifique."),
           ("Le froid détruit définitivement les enzymes.", "Il les ralentit de façon réversible."), ("La lipase digère l’amidon.", "Elle digère les lipides.")],
          "les enzymes", "living-things-and-ecosystems"),

        H("S", "structure-et-dynamique-du-globe", "Structure et dynamique interne de la Terre", "Dynamique du globe",
          "Les élèves décrivent la structure du globe à partir des ondes sismiques, la lithosphère et l’asthénosphère, et la mobilité des plaques (dorsales, subductions).",
          "ondes sismiques P et S, discontinuités, croûte, manteau, noyau, lithosphère, asthénosphère, plaques, dorsales, rifts, subduction, paléomagnétisme, GPS",
          "La lithosphère rigide glisse sur l’asthénosphère ductile", "Les plaques s’écartent aux dorsales et plongent aux zones de subduction.",
          ["Les ondes sismiques changent de vitesse aux discontinuités : Moho (croûte/manteau), Gutenberg (manteau/noyau vers 2 900 km). Les ondes S ne traversent pas le noyau externe liquide.",
           "La lithosphère (croûte + manteau supérieur rigide, environ 100 km) repose sur l’asthénosphère, plus chaude et ductile.",
           "Aux dorsales, de la lithosphère océanique se forme. Aux zones de subduction, elle plonge dans le manteau. Le paléomagnétisme et le GPS mesurent ces déplacements (quelques cm par an)."],
          [("Une bande de basalte est à 120 km de l’axe d’une dorsale et date de 4 millions d’années. Vitesse d’expansion d’un côté ?", ["120 km = 12 000 000 cm.", "12 000 000 : 4 000 000."], "3 cm/an.")],
          [("Le manteau est liquide.", "Il est solide, mais l’asthénosphère est ductile."), ("Les plaques sont la croûte seule.", "Une plaque est un morceau de lithosphère (croûte + manteau supérieur).")],
          [("Pourquoi les ondes S disparaissent-elles au-delà de 2 900 km ?", "Elles ne se propagent pas dans le noyau externe liquide."), ("Comment le GPS montre-t-il la tectonique ?", "Des stations fixes enregistrent des déplacements de quelques cm par an.")],
          [("Couches", [("la croûte continentale", "épaisse d’environ 30 km, granite"), ("la croûte océanique", "mince, basalte et gabbro"), ("le manteau", "péridotite, jusqu’à 2 900 km"), ("le noyau externe", "fer liquide"),
                        ("le noyau interne", "fer solide"), ("l’asthénosphère", "manteau ductile sous la lithosphère"), ("la lithosphère", "croûte et manteau supérieur rigides")],
            "Que sais-tu de {k} ?", "Quelle couche : {v} ?"),
           ("Discontinuités et ondes", [("le Moho", "limite croûte-manteau"), ("la discontinuité de Gutenberg", "limite manteau-noyau"), ("la discontinuité de Lehmann", "limite noyau externe-interne"), ("les ondes P", "les plus rapides, traversent tout"),
                                        ("les ondes S", "ne traversent pas les liquides"), ("la zone d’ombre sismique", "zone sans ondes directes due au noyau")],
            "Que désigne {k} ?", "Quoi : {v} ?"),
           ("Frontières de plaques", [("la dorsale médio-atlantique", "divergence"), ("la fosse du Japon", "subduction"), ("les Andes", "subduction"), ("l’Himalaya", "collision"), ("le rift est-africain", "divergence continentale"),
                                      ("la faille de San Andreas", "coulissage"), ("l’Islande", "divergence")],
            "Quel type de frontière : {k} ?", None, ("point chaud",))],
          ["La lithosphère est rigide.", "L’asthénosphère est ductile.", "Les ondes S ne traversent pas le noyau externe.", "Le Moho sépare la croûte du manteau.",
           "Aux dorsales, de la lithosphère se forme.", "Les plaques bougent de quelques cm par an.", "L’Himalaya résulte d’une collision."],
          [("Le manteau est liquide.", "Il est solide."), ("Une plaque est seulement de la croûte.", "C’est de la lithosphère."), ("Les ondes S traversent le noyau externe.", "Elles ne traversent pas les liquides."),
           ("Aux zones de subduction, de la lithosphère se forme.", "Elle y plonge."), ("Le noyau interne est liquide.", "Il est solide.")],
          "la dynamique du globe", "earths-systems"),

        H("S", "ecosystemes-et-services-ecosystemiques", "Écosystèmes et services écosystémiques", "Écosystèmes",
          "Les élèves décrivent les interactions et les flux de matière et d’énergie dans un écosystème, sa dynamique et les services écosystémiques rendus à l’humanité.",
          "biotope, biocénose, interactions (prédation, compétition, symbiose, parasitisme), réseau trophique, producteurs, consommateurs, décomposeurs, cycle du carbone, résilience, services écosystémiques",
          "Un écosystème = biotope + biocénose", "Les services écosystémiques sont les bénéfices que l’humanité tire des écosystèmes.",
          ["Un écosystème associe un milieu (biotope) et des êtres vivants (biocénose) en interaction : prédation, compétition, mutualisme, symbiose, parasitisme.",
           "La matière circule entre producteurs, consommateurs et décomposeurs. L’énergie, venue du Soleil, se perd en chaleur à chaque niveau trophique.",
           "Un écosystème évolue et peut se rétablir après une perturbation (résilience). Il rend des services : pollinisation, épuration de l’eau, stockage du carbone, protection contre l’érosion."],
          [("Les lichens sont une association entre un champignon et une algue qui en tirent tous deux profit. Type d’interaction ?", ["Bénéfice réciproque.", "Association durable et étroite."], "Une symbiose.")],
          [("L’énergie circule en boucle dans l’écosystème.", "La matière se recycle, l’énergie se dissipe en chaleur."), ("Les décomposeurs sont inutiles.", "Ils recyclent la matière organique en matière minérale.")],
          [("Qu’est-ce que la résilience ?", "La capacité d’un écosystème à retrouver son fonctionnement après une perturbation."), ("Donne un service de régulation.", "Les zones humides limitent les inondations.")],
          [("Interactions", [("le lion et la gazelle", "prédation"), ("deux plantes qui se disputent la lumière", "compétition"), ("l’abeille et la fleur", "mutualisme"), ("le lichen", "symbiose"),
                             ("le ténia dans l’intestin", "parasitisme"), ("les mycorhizes entre champignon et racine", "symbiose"), ("le gui sur un arbre", "parasitisme"), ("le poisson-clown et l’anémone", "mutualisme")],
            "Quelle interaction : {k} ?", None, ("commensalisme",)),
           ("Services écosystémiques", [("la pollinisation par les insectes", "service d’approvisionnement en fruits"), ("l’épuration de l’eau par les zones humides", "service de régulation"), ("le stockage de carbone par les forêts", "régulation du climat"),
                                        ("la beauté d’un paysage", "service culturel"), ("la formation des sols", "service de soutien"), ("la pêche", "service d’approvisionnement"), ("les mangroves contre les tempêtes", "protection des côtes")],
            "Quel service rend {k} ?", None),
           ("Vocabulaire", [("le biotope", "milieu physique et chimique"), ("la biocénose", "ensemble des êtres vivants"), ("le niveau trophique", "place dans le réseau alimentaire"), ("le décomposeur", "transforme la matière organique en minérale"),
                            ("la résilience", "capacité à se rétablir après une perturbation"), ("le producteur primaire", "être vivant chlorophyllien"), ("le réseau trophique", "ensemble des chaînes alimentaires reliées")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Un écosystème associe biotope et biocénose.", "La matière se recycle dans un écosystème.", "L’énergie se dissipe en chaleur.", "Le lichen est une symbiose.",
           "Les décomposeurs recyclent la matière organique.", "Les forêts stockent du carbone.", "Un écosystème peut être résilient."],
          [("L’énergie circule en boucle.", "Elle se dissipe."), ("Les décomposeurs sont inutiles.", "Ils recyclent la matière."), ("Le ténia et l’humain sont en mutualisme.", "C’est du parasitisme."),
           ("Le biotope est l’ensemble des êtres vivants.", "C’est la biocénose."), ("Un écosystème ne change jamais.", "Il évolue.")],
          "les écosystèmes", "living-things-and-ecosystems"),

        H("S", "immunite-innee-et-adaptative", "Immunité innée et immunité adaptative", "Immunité",
          "Les élèves décrivent la réaction inflammatoire, l’immunité adaptative (lymphocytes B et T, anticorps), la mémoire immunitaire et la vaccination.",
          "barrières naturelles, réaction inflammatoire, phagocytose, cellules présentatrices, lymphocytes B et T, plasmocytes, anticorps, complexe immun, lymphocytes T cytotoxiques, mémoire, vaccination, immunité de groupe",
          "Immunité innée : rapide et non spécifique", "Immunité adaptative : plus lente, spécifique et avec mémoire.",
          ["L’immunité innée réagit en quelques heures : réaction inflammatoire (rougeur, chaleur, gonflement, douleur), phagocytose par les macrophages.",
           "L’immunité adaptative cible un antigène précis : les lymphocytes B deviennent des plasmocytes qui sécrètent des anticorps, les lymphocytes T cytotoxiques détruisent les cellules infectées.",
           "Des lymphocytes mémoire persistent : au second contact, la réponse est plus rapide et plus forte. La vaccination provoque cette mémoire sans maladie. L’immunité de groupe protège les personnes non vaccinées."],
          [("Pourquoi la deuxième injection d’un vaccin donne-t-elle plus d’anticorps ?", ["La première a créé des cellules mémoire.", "Elles réagissent plus vite et plus fort."], "C’est la réponse secondaire.")],
          [("Un anticorps agit contre tous les microbes.", "Il est spécifique d’un antigène."), ("L’inflammation est toujours une maladie.", "C’est d’abord une réaction normale de défense.")],
          [("Qu’est-ce qu’un antigène ?", "Une molécule reconnue comme étrangère par le système immunitaire."), ("Qu’est-ce que l’immunité de groupe ?", "Quand assez de personnes sont immunisées, le microbe circule peu et protège les autres.")],
          [("Acteurs", [("le macrophage", "réalise la phagocytose"), ("le lymphocyte B", "se transforme en plasmocyte"), ("le plasmocyte", "sécrète des anticorps"), ("le lymphocyte T cytotoxique", "détruit les cellules infectées"),
                        ("le lymphocyte T auxiliaire", "active les autres lymphocytes"), ("le lymphocyte mémoire", "permet une réponse plus rapide"), ("la cellule dendritique", "présente l’antigène aux lymphocytes")],
            "Quel est le rôle de {k} ?", "Quelle cellule {v} ?"),
           ("Innée ou adaptative ?", {"de l’immunité innée": ["la réaction inflammatoire", "la phagocytose par les macrophages", "la barrière de la peau", "les larmes et le mucus", "une réaction en quelques heures", "la fièvre"],
                                      "de l’immunité adaptative": ["la production d’anticorps", "les lymphocytes T cytotoxiques", "la mémoire immunitaire", "la réponse spécifique d’un antigène", "l’effet d’un rappel de vaccin", "les plasmocytes"]}),
           ("Vocabulaire", [("l’antigène", "molécule reconnue comme étrangère"), ("l’anticorps", "protéine qui neutralise un antigène précis"), ("le complexe immun", "anticorps fixé sur son antigène"), ("la vaccination", "déclenche une mémoire sans maladie"),
                            ("la réponse secondaire", "plus rapide et plus intense"), ("l’immunité de groupe", "protection collective"), ("l’inflammation", "rougeur, chaleur, gonflement, douleur")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["L’immunité innée est rapide et non spécifique.", "Les plasmocytes sécrètent des anticorps.", "Un anticorps est spécifique d’un antigène.", "La réponse secondaire est plus rapide.",
           "La vaccination crée une mémoire immunitaire.", "Les lymphocytes T cytotoxiques détruisent les cellules infectées.", "La réaction inflammatoire est une défense normale."],
          [("Un anticorps agit contre tous les microbes.", "Il est spécifique."), ("L’immunité innée a une mémoire.", "C’est l’immunité adaptative."), ("Les macrophages sécrètent des anticorps.", "Ce sont les plasmocytes."),
           ("La réponse secondaire est plus lente.", "Elle est plus rapide."), ("La vaccination provoque la maladie.", "Elle crée une mémoire sans maladie.")],
          "l’immunité", "living-things-and-ecosystems"),
    ]
