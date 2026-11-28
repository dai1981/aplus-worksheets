# -*- coding: utf-8 -*-
"""France / Physique-chimie et SVT : enseignement de spécialité de terminale"""
import math
from fr_sci import H, nq, num


def f_ph(R):
    k = R.choice(["pH", "pH", "c", "dil", "pka"])
    if k == "pH":
        c = R.choice([1e-2, 1e-3, 5e-3, 2e-2, 1e-4, 0.1])
        return nq("Quel est le pH d’une solution d’acide fort de concentration %s mol/L ? (pH = −log[H₃O⁺])" % num(c), -math.log10(c), [math.log10(1 / c) + 1, c * 100, 14 + math.log10(c)], "",
                  "[H₃O⁺] = %s mol/L, pH = −log(%s) = %s." % (num(c), num(c), num(-math.log10(c))))
    if k == "c":
        p = R.choice([2, 3, 4.5, 2.5, 5, 1.5])
        return nq("Une solution a un pH de %s. Quelle est la concentration en ions oxonium ?" % num(p), 10 ** -p, [10 ** p, p / 10, 10 ** (p - 14)], "mol/L", "[H₃O⁺] = 10^(−pH) = %s mol/L." % num(10 ** -p))
    if k == "dil":
        p, f = R.choice([(2, 10), (3, 100), (1, 10), (2, 1000), (1.5, 10)])
        return nq("On dilue %s fois une solution d’acide fort de pH %s. Nouveau pH ?" % (num(f), num(p)), p + math.log10(f), [p * f, p - math.log10(f), p + f], "", "Diluer 10 fois augmente le pH de 1 : pH = %s." % num(p + math.log10(f)))
    pka, ratio = R.choice([(4.8, 10), (4.8, 1), (9.2, 0.1), (3.8, 100), (6.4, 1), (9.2, 10)])
    return nq("Pour un couple de pKa %s, le rapport [base] : [acide] vaut %s. Quel est le pH ? (pH = pKa + log([A⁻] : [AH]))" % (num(pka), num(ratio)), pka + math.log10(ratio),
              [pka - math.log10(ratio) if ratio != 1 else pka + 1, pka * ratio, 14 - pka], "", "pH = %s + log %s = %s." % (num(pka), num(ratio), num(pka + math.log10(ratio))), neg=False)


def f_cin(R):
    k = R.choice(["v", "v", "t12", "c", "k"])
    if k == "v":
        c1, c2, t = R.choice([(0.5, 0.3, 40), (1.0, 0.6, 100), (0.08, 0.02, 30), (0.2, 0.15, 10), (2.0, 1.2, 160), (0.4, 0.1, 60), (0.9, 0.45, 90)])
        return nq("La concentration d’un réactif passe de %s à %s mol/L en %s s. Vitesse moyenne de disparition ?" % (num(c1), num(c2), num(t)), (c1 - c2) / t,
                  [(c1 - c2) * t, c1 / t, t / (c1 - c2)], "mol/(L·s)", "v = (%s − %s) : %s = %s mol/(L·s)." % (num(c1), num(c2), num(t), num((c1 - c2) / t)))
    if k == "t12":
        kk = R.choice([0.01, 0.05, 0.002, 0.1, 0.0231, 0.004, 0.02])
        return nq("Une réaction d’ordre 1 a une constante de vitesse k = %s s⁻¹. Temps de demi-réaction ? (t½ = ln 2 : k)" % num(kk), math.log(2) / kk, [1 / kk, kk * math.log(2), 2 / kk], "s",
                  "t½ = 0,693 : %s = %s s." % (num(kk), num(math.log(2) / kk)))
    if k == "c":
        c0, n = R.choice([(0.8, 2), (1.0, 3), (0.5, 1), (0.64, 4), (2.0, 2)])
        return nq("Ordre 1 : la concentration initiale est %s mol/L. Que vaut-elle après %d temps de demi-réaction ?" % (num(c0), n), c0 / 2 ** n, [c0 / (2 * n), c0 - c0 / 2 ** n, c0 / 2 ** (n + 1)], "mol/L",
                  "Elle est divisée par 2 à chaque t½ : %s : 2^%d = %s mol/L." % (num(c0), n, num(c0 / 2 ** n)))
    t12 = R.choice([30, 69.3, 120, 10, 693])
    return nq("Une réaction d’ordre 1 a un temps de demi-réaction de %s s. Constante de vitesse k ?" % num(t12), math.log(2) / t12, [t12 / math.log(2), 1 / t12, 2 / t12], "s⁻¹", "k = ln 2 : t½ = %s s⁻¹." % num(math.log(2) / t12))


def f_pile(R):
    k = R.choice(["Q", "Q", "t", "n", "Qr"])
    F = 96500
    if k == "Q":
        I, t = R.choice([(0.2, 3600), (0.05, 7200), (1, 1800), (0.5, 36000), (2, 600), (0.1, 5400), (0.3, 1200)])
        return nq("Une pile débite %s A pendant %s s. Quelle charge a-t-elle délivrée ?" % (num(I), num(t)), I * t, [I / t, t / I, I * t / F], "C", "Q = I × Δt = %s C." % num(I * t))
    if k == "t":
        Q, I = R.choice([(3600, 0.1), (7200, 0.5), (1800, 0.2), (18000, 1), (900, 0.05), (5400, 0.3), (2400, 0.4)])
        return nq("Une pile de capacité %s C débite %s A. Pendant combien de temps fonctionne-t-elle ?" % (num(Q), num(I)), Q / I, [Q * I, I / Q, Q / I / 60], "s", "Δt = Q : I = %s s." % num(Q / I))
    if k == "n":
        Q = R.choice([965, 9650, 19300, 4825, 96500, 1930, 2895])
        return nq("Une charge de %s C a circulé. Quelle quantité d’électrons a été échangée ? (F = 96 500 C/mol)" % num(Q), Q / F, [Q * F, F / Q, Q / F * 2], "mol", "n(e⁻) = Q : F = %s mol." % num(Q / F))
    a, b, c_, d = R.choice([(0.1, 0.1, 0.01, 0.01), (0.2, 0.05, 0.1, 0.1), (0.5, 0.5, 0.1, 0.2), (0.01, 0.1, 0.1, 0.01)])
    Qr = (c_ * d) / (a * b)
    return nq("Pour A + B ⇄ C + D en solution, [A] = %s, [B] = %s, [C] = %s, [D] = %s mol/L. Quotient de réaction Qr ?" % (num(a), num(b), num(c_), num(d)), Qr,
              [(a * b) / (c_ * d), c_ * d, (c_ + d) / (a + b) if abs((c_ + d) / (a + b) - Qr) > 1e-9 else Qr * 10], "", "Qr = [C][D] : ([A][B]) = %s." % num(Qr))


def f_rdt(R):
    k = R.choice(["r", "r", "mexp", "nth"])
    if k == "r":
        mth, mexp = R.choice([(12.0, 9.0), (5.0, 4.1), (20.0, 13.0), (8.8, 6.6), (3.5, 2.8), (15.0, 13.5)])
        return nq("La masse théorique de produit est %s g, on en obtient %s g. Quel est le rendement ?" % (num(mth), num(mexp)), 100 * mexp / mth, [100 * mth / mexp, mexp / mth, 100 - 100 * mexp / mth], "%",
                  "η = mexp : mth = %s %%." % num(100 * mexp / mth))
    if k == "mexp":
        mth, r = R.choice([(10, 80), (25, 60), (4, 75), (50, 90), (12, 45), (8, 65), (30, 70)])
        return nq("Une synthèse a un rendement de %s %% et une masse théorique de %s g. Quelle masse obtient-on ?" % (num(r), num(mth)), mth * r / 100, [mth * 100 / r, mth - r / 10, mth * r], "g",
                  "m = %s × %s : 100 = %s g." % (num(mth), num(r), num(mth * r / 100)))
    n, M = R.choice([(0.1, 88), (0.05, 180), (0.2, 60), (0.25, 102), (0.02, 130), (0.15, 74), (0.3, 116)])
    return nq("Le réactif limitant permet de former au maximum %s mol d’un ester de masse molaire %s g/mol. Masse théorique ?" % (num(n), num(M)), n * M, [n / M, M / n, n * M / 10], "g", "mth = n × M = %s g." % num(n * M))


def f_newton(R):
    k = R.choice(["a", "a", "tchute", "vchute", "portee", "hmax"])
    g = 9.81
    if k == "a":
        F, m = R.choice([(1500, 1000), (30, 12), (6, 0.2), (2400, 800), (90, 60)])
        return nq("Une force résultante de %s N s’exerce sur un système de %s kg. Valeur de l’accélération ?" % (num(F), num(m)), F / m, [F * m, m / F, F / m / g], "m/s²", "a = ΣF : m = %s m/s²." % num(F / m))
    if k == "tchute":
        h = R.choice([5, 20, 45, 1.25, 80])
        return nq("Un objet est lâché sans vitesse de %s m de haut. Durée de la chute libre ? (g = 9,81 m/s²)" % num(h), math.sqrt(2 * h / g), [2 * h / g, h / g, math.sqrt(h / g)], "s", "t = √(2h : g) = %s s." % num(math.sqrt(2 * h / g)))
    if k == "vchute":
        t = R.choice([1, 2, 3, 0.5, 1.5])
        return nq("Un objet tombe en chute libre sans vitesse initiale. Quelle est sa vitesse au bout de %s s ? (g = 9,81 m/s²)" % num(t), g * t, [g * t * t / 2, g / t, g], "m/s", "v = g × t = %s m/s." % num(g * t))
    if k == "portee":
        v0, a = R.choice([(10, 45), (20, 30), (15, 45), (12, 60), (25, 45)])
        P = v0 * v0 * math.sin(math.radians(2 * a)) / g
        return nq("Un projectile est lancé du sol à %s m/s avec un angle de %d°. Quelle est sa portée (même altitude, sans frottement) ? (g = 9,81 m/s²)" % (num(v0), a), P,
                  [v0 * v0 / g * 2, v0 * math.sin(math.radians(a)) / g, P / 2], "m", "Portée = v₀² × sin(2α) : g = %s m." % num(P))
    v0 = R.choice([10, 15, 8, 20, 5])
    return nq("Une balle est lancée verticalement vers le haut à %s m/s. Hauteur maximale ? (g = 9,81 m/s²)" % num(v0), v0 * v0 / (2 * g), [v0 * v0 / g, v0 / g, v0 * v0 * g], "m", "h = v₀² : (2g) = %s m." % num(v0 * v0 / (2 * g)))


def f_orbite(R):
    G, MT, RT = 6.67e-11, 5.97e24, 6.37e6
    k = R.choice(["v", "v", "T", "kep"])
    if k == "v":
        h = R.choice([400e3, 800e3, 20200e3, 35786e3, 1000e3, 600e3, 1500e3])
        r = RT + h
        return nq("Vitesse d’un satellite en orbite circulaire à %s km d’altitude ? (v = √(GM : r), G = 6,67 × 10⁻¹¹, M = 5,97 × 10²⁴ kg, R = 6 370 km)" % num(h / 1000), math.sqrt(G * MT / r),
                  [G * MT / r, math.sqrt(G * MT / h), math.sqrt(G * MT / r) * 2], "m/s", "r = R + h = %s m, v = %s m/s." % (num(r), num(math.sqrt(G * MT / r))))
    if k == "T":
        h = R.choice([400e3, 800e3, 20200e3, 35786e3, 600e3, 1000e3])
        r = RT + h
        v = math.sqrt(G * MT / r)
        T = 2 * math.pi * r / v
        return nq("Période de révolution d’un satellite à %s km d’altitude ? (même données, T = 2πr : v)" % num(h / 1000), T, [2 * math.pi * h / v, r / v, T / 60], "s", "T = 2πr : v = %s s." % num(T))
    T1, a1, a2 = R.choice([(1, 1, 1.52), (1, 1, 5.2), (1, 1, 0.72), (1, 1, 9.5), (1, 1, 0.39), (1, 1, 19.2), (1, 1, 30.1), (1, 1, 2.8)])
    T2 = T1 * (a2 / a1) ** 1.5
    return nq("D’après la 3e loi de Kepler (T² : a³ constant), quelle est la période d’une planète à %s ua du Soleil ? (Terre : 1 an, 1 ua)" % num(a2), T2, [a2 ** 2, a2, a2 ** 3], "ans",
              "T = a^(3/2) = %s^1,5 = %s ans." % (num(a2), num(T2)))


def f_thermo(R):
    k = R.choice(["Q", "Q", "dT", "m", "P"])
    if k == "Q":
        m, c, dT, n = R.choice([(1, 4180, 20, "d’eau"), (0.5, 4180, 60, "d’eau"), (2, 900, 30, "d’aluminium"), (0.2, 4180, 75, "d’eau"), (5, 450, 100, "de fer")])
        return nq("Quelle énergie faut-il pour chauffer %s kg %s de %s °C ? (c = %s J/(kg·°C))" % (num(m), n, num(dT), num(c)), m * c * dT, [c * dT, m * c, m * c * dT / 1000], "J",
                  "Q = m × c × ΔT = %s J." % num(m * c * dT))
    if k == "dT":
        Q, m = R.choice([(41800, 0.5), (83600, 1), (20900, 0.25), (167200, 2), (12540, 0.1), (62700, 0.3), (250800, 3)])
        return nq("On fournit %s J à %s kg d’eau (c = 4 180 J/(kg·°C)). De combien sa température augmente-t-elle ?" % (num(Q), num(m)), Q / (m * 4180), [Q * m / 4180, Q / 4180, Q / m], "°C",
                  "ΔT = Q : (m × c) = %s °C." % num(Q / (m * 4180)))
    if k == "m":
        Q, dT = R.choice([(418000, 50), (83600, 20), (209000, 25), (125400, 30), (334400, 40), (627000, 75)])
        return nq("On fournit %s J pour élever de %s °C la température d’une masse d’eau (c = 4 180 J/(kg·°C)). Quelle est cette masse ?" % (num(Q), num(dT)), Q / (4180 * dT), [Q * dT / 4180, Q / 4180, dT / Q], "kg",
                  "m = Q : (c × ΔT) = %s kg." % num(Q / (4180 * dT)))
    P, m, dT = R.choice([(2000, 1, 80), (1000, 0.5, 60), (1500, 1.5, 75), (800, 0.25, 50)])
    t = m * 4180 * dT / P
    return nq("Une bouilloire de %s W chauffe %s kg d’eau de %s °C. Durée minimale, sans pertes ? (c = 4 180 J/(kg·°C))" % (num(P), num(m), num(dT)), t, [t / 60, P / (m * 4180 * dT), t * 2], "s",
              "t = m c ΔT : P = %s s." % num(t))


def f_diff(R):
    k = R.choice(["theta", "theta", "a", "i", "dopp"])
    if k == "theta":
        lam, a = R.choice([(633e-9, 0.1e-3), (532e-9, 0.05e-3), (650e-9, 0.2e-3), (450e-9, 0.1e-3), (633e-9, 0.5e-3)])
        return nq("Un laser de %s nm éclaire une fente de largeur %s mm. Écart angulaire θ de la tache centrale ? (θ = λ : a)" % (num(lam * 1e9), num(a * 1000)), lam / a, [a / lam, lam * a, 2 * lam / a], "rad",
                  "θ = λ : a = %s rad." % num(lam / a))
    if k == "a":
        lam, th = R.choice([(633e-9, 0.0063), (532e-9, 0.0053), (650e-9, 0.013), (500e-9, 0.01), (450e-9, 0.009), (600e-9, 0.003)])
        return nq("Une radiation de %s nm donne un écart angulaire de %s rad. Quelle est la largeur de la fente ?" % (num(lam * 1e9), num(th)), lam / th, [th / lam, lam * th, lam / th * 1000], "m", "a = λ : θ = %s m." % num(lam / th))
    if k == "i":
        lam, D, b = R.choice([(633e-9, 2, 0.5e-3), (532e-9, 1.5, 0.2e-3), (650e-9, 1, 0.1e-3), (450e-9, 2, 0.3e-3)])
        return nq("Fentes d’Young : λ = %s nm, D = %s m, b = %s mm. Interfrange ? (i = λD : b)" % (num(lam * 1e9), num(D), num(b * 1000)), lam * D / b, [lam * b / D, lam / (D * b), D * b / lam], "m",
                  "i = λ × D : b = %s m." % num(lam * D / b))
    v, f = R.choice([(20, 1000), (30, 500), (10, 2000), (25, 800), (15, 600), (35, 1200)])
    fr = f * 340 / (340 - v)
    return nq("Une ambulance émet %s Hz et s’approche à %s m/s d’un observateur immobile. Fréquence perçue ? (son à 340 m/s, f’ = f × v : (v − vs))" % (num(f), num(v)), fr,
              [f * 340 / (340 + v), f, f * v / 340], "Hz", "f’ = %s × 340 : (340 − %s) = %s Hz." % (num(f), num(v), num(fr)))


def f_rc(R):
    k = R.choice(["tau", "tau", "q", "u63", "C"])
    if k == "tau":
        Rr, C = R.choice([(1000, 1e-6), (10e3, 100e-6), (4.7e3, 10e-6), (100e3, 1e-6), (220, 470e-6)])
        return nq("Un circuit RC a R = %s Ω et C = %s F. Constante de temps τ ?" % (num(Rr), num(C)), Rr * C, [Rr / C, C / Rr, 5 * Rr * C], "s", "τ = R × C = %s s." % num(Rr * C))
    if k == "q":
        C, U = R.choice([(100e-6, 12), (1e-6, 5), (470e-6, 9), (10e-6, 230), (2.2e-3, 3)])
        return nq("Un condensateur de %s F est chargé sous %s V. Quelle charge porte-t-il ?" % (num(C), num(U)), C * U, [C / U, U / C, C * U * U / 2], "C", "q = C × U = %s C." % num(C * U))
    if k == "u63":
        E = R.choice([5, 12, 9, 6, 10])
        return nq("Un condensateur se charge sous E = %s V. Quelle tension atteint-il au bout d’une durée τ ? (63 %% de E)" % num(E), 0.63 * E, [E, 0.37 * E, 0.5 * E], "V", "u(τ) ≈ 0,63 × E = %s V." % num(0.63 * E))
    tau, Rr = R.choice([(0.1, 1000), (1, 10e3), (0.047, 4.7e3), (0.022, 220)])
    return nq("La constante de temps vaut %s s et R = %s Ω. Capacité du condensateur ?" % (num(tau), num(Rr)), tau / Rr, [tau * Rr, Rr / tau, tau / Rr * 1000], "F", "C = τ : R = %s F." % num(tau / Rr))


def f_radio(R):
    k = R.choice(["N", "N", "t", "A", "age"])
    if k == "N":
        N0, n = R.choice([(1e12, 2), (8e10, 3), (4e9, 1), (1.6e11, 4), (2e15, 5)])
        return nq("Un échantillon contient %s noyaux radioactifs. Combien en reste-t-il après %d demi-vies ?" % (num(N0), n), N0 / 2 ** n, [N0 / (2 * n), N0 - N0 / 2 ** n, N0 / 2 ** (n + 1)], "",
                  "N = N₀ : 2^%d = %s." % (n, num(N0 / 2 ** n)))
    if k == "t":
        t12, n = R.choice([(8, 3), (5730, 2), (30, 4), (1600, 2), (12.3, 3), (3.8, 2), (5.3, 3)])
        return nq("Un radionucléide a une demi-vie de %s ans (ou jours). Au bout de combien de temps reste-t-il 1/%d des noyaux ?" % (num(t12), 2 ** n), n * t12, [2 ** n * t12, t12 / 2 ** n, (n + 1) * t12], "",
                  "1/%d = (½)^%d : il faut %d demi-vies, soit %s." % (2 ** n, n, n, num(n * t12)))
    if k == "A":
        lam, N = R.choice([(1e-3, 1e10), (2.5e-5, 4e12), (1e-8, 6e20), (3.8e-12, 5e22), (2e-6, 3e15), (5e-4, 8e9)])
        return nq("Activité d’un échantillon de %s noyaux de constante radioactive %s s⁻¹ ? (A = λ × N)" % (num(N), num(lam)), lam * N, [N / lam, lam / N, lam * N * 2], "Bq", "A = λ × N = %s Bq." % num(lam * N))
    r = R.choice([0.5, 0.25, 0.125, 0.0625])
    n = int(round(-math.log2(r)))
    return nq("Un fossile contient %s %% du carbone 14 d’un organisme vivant (demi-vie 5 730 ans). Quel est son âge ?" % num(100 * r), n * 5730, [5730 / n, 5730 * r, (n + 1) * 5730], "ans",
              "%s = (½)^%d : %d demi-vies, soit %s ans." % (num(r), n, n, num(n * 5730)))


def f_datation(R):
    k = R.choice(["age", "age", "frac", "t12"])
    if k == "age":
        t12, n, nm = R.choice([(5730, 2, "carbone 14"), (1.25e9, 1, "potassium 40"), (4.47e9, 1, "uranium 238"), (5730, 3, "carbone 14"), (1.25e9, 2, "potassium 40"), (48.8e9, 0.5, "rubidium 87"), (5730, 4, "carbone 14"), (4.47e9, 0.5, "uranium 238"), (1.25e9, 3, "potassium 40"), (5730, 1, "carbone 14")])
        return nq("Une roche (ou un fossile) n’a plus qu’une fraction (½)^%s de son %s initial. Demi-vie : %s ans. Quel est son âge ?" % (num(n), nm, num(t12)), n * t12, [t12 / n, t12, (n + 1) * t12], "ans",
                  "Âge = %s × %s = %s ans." % (num(n), num(t12), num(n * t12)))
    if k == "frac":
        n = R.choice([1, 2, 3, 4, 5, 6])
        return nq("Quelle fraction d’un isotope radioactif reste-t-il après %d demi-vies ? Donne-la en pourcentage." % n, 100 / 2 ** n, [100 / (2 * n), 100 - 100 / 2 ** n, 100 / 2 ** (n + 1)], "%",
                  "(½)^%d = %s %%." % (n, num(100 / 2 ** n)))
    age, n = R.choice([(11460, 2), (17190, 3), (2.5e9, 2), (22920, 4), (3.75e9, 3), (8.94e9, 2), (28650, 5)])
    return nq("Un échantillon âgé de %s ans a subi %d demi-vies. Quelle est la demi-vie de l’isotope ?" % (num(age), n), age / n, [age * n, age / 2 ** n, age], "ans", "T½ = %s : %d = %s ans." % (num(age), n, num(age / n)))


def UNITS(grade):
    return [
        H("P", "acides-bases-ph-et-pka", "Acides, bases, pH et pKa", "pH et pKa",
          "Les élèves définissent acides et bases de Brønsted, calculent un pH, comparent la force des acides par leur pKa et utilisent un diagramme de prédominance et une solution tampon.",
          "acide et base de Brønsted, couple acide/base, ampholyte, pH = −log[H₃O⁺], produit ionique de l’eau, acide fort, acide faible, Ka, pKa, diagramme de prédominance, solution tampon",
          "pH = −log[H₃O⁺]", "Si le pH dépasse le pKa, la base prédomine. Sinon, c’est l’acide.",
          ["Un acide de Brønsted cède un proton H⁺, une base en capte un. Couple AH/A⁻. L’eau est un ampholyte. Ke = [H₃O⁺] × [HO⁻] = 10⁻¹⁴ à 25 °C.",
           "pH = −log[H₃O⁺] et [H₃O⁺] = 10^(−pH). Un acide fort réagit totalement avec l’eau : pH = −log c.",
           "Un acide faible a une constante Ka et un pKa = −log Ka. pH = pKa + log([A⁻] : [AH]). Plus le pKa est petit, plus l’acide est fort. Une solution tampon a un pH qui varie peu."],
          [("Acide éthanoïque (pKa = 4,8) dans une solution de pH 7. Qui prédomine ?", ["pH > pKa.", "La forme basique prédomine."], "L’ion éthanoate CH₃COO⁻.")],
          [("Un pH de 2 est deux fois plus acide qu’un pH de 4.", "[H₃O⁺] est 100 fois plus grande."), ("Un acide faible est un acide dilué.", "Faible veut dire qu’il ne réagit pas totalement avec l’eau.")],
          [("Que vaut le pH du sang ?", "Environ 7,4, maintenu par des systèmes tampons."), ("Qu’est-ce qu’un ampholyte ?", "Une espèce qui est l’acide d’un couple et la base d’un autre, comme l’eau.")],
          [("Couples acide/base", [("CH₃COOH/CH₃COO⁻", "pKa = 4,8"), ("NH₄⁺/NH₃", "pKa = 9,2"), ("H₃O⁺/H₂O", "pKa = 0"), ("H₂O/HO⁻", "pKa = 14"), ("HCOOH/HCOO⁻", "pKa = 3,8"), ("CO₂,H₂O/HCO₃⁻", "pKa = 6,4"),
                                   ("HCO₃⁻/CO₃²⁻", "pKa = 10,3")],
            "Quel est le pKa du couple {k} ?", "Quel couple a un {v} ?"),
           ("Prédominance", [("pH très inférieur au pKa", "la forme acide prédomine"), ("pH très supérieur au pKa", "la forme basique prédomine"), ("pH égal au pKa", "acide et base en concentrations égales"),
                             ("acide fort dans l’eau", "réaction totale"), ("acide faible dans l’eau", "réaction limitée"), ("ajout d’un peu d’acide à un tampon", "pH presque inchangé")],
            "Que se passe-t-il : {k} ?", None),
           ("Vocabulaire", [("l’acide de Brønsted", "cède un proton"), ("la base de Brønsted", "capte un proton"), ("le produit ionique de l’eau", "Ke = 10⁻¹⁴ à 25 °C"), ("le pKa", "−log Ka"),
                            ("la solution tampon", "pH qui varie peu"), ("l’ampholyte", "acide d’un couple et base d’un autre"), ("l’acide fort", "réagit totalement avec l’eau")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["pH = −log[H₃O⁺].", "Si pH > pKa, la base prédomine.", "Plus le pKa est petit, plus l’acide est fort.", "Ke = 10⁻¹⁴ à 25 °C.",
           "L’eau est un ampholyte.", "Une solution tampon a un pH qui varie peu.", "Diluer 10 fois un acide fort augmente son pH de 1."],
          [("Un pH de 2 est deux fois plus acide qu’un pH de 4.", "100 fois plus."), ("Si pH < pKa, la base prédomine.", "L’acide prédomine."), ("Un acide faible est un acide dilué.", "Il réagit partiellement."),
           ("Plus le pKa est grand, plus l’acide est fort.", "C’est l’inverse."), ("Une base cède un proton.", "Elle en capte un.")],
          "les acides et les bases", "matter", calc=f_ph),

        H("P", "cinetique-chimique", "Cinétique chimique", "Cinétique",
          "Les élèves identifient les facteurs cinétiques, définissent la vitesse volumique de disparition, le temps de demi-réaction et la loi de vitesse d’ordre 1, et décrivent un mécanisme réactionnel.",
          "transformation lente, rapide, facteurs cinétiques, catalyseur, vitesse volumique, temps de demi-réaction, loi de vitesse d’ordre 1, mécanisme réactionnel, intermédiaire",
          "t½ = ln 2 : k pour une réaction d’ordre 1", "Température, concentration et catalyseur accélèrent une transformation.",
          ["Une transformation peut être rapide ou lente. Facteurs cinétiques : température, concentrations des réactifs, catalyseur, surface de contact.",
           "Vitesse volumique de disparition : v = −d[A]/dt. Temps de demi-réaction t½ : durée pour que l’avancement atteigne la moitié de sa valeur finale.",
           "Pour une loi d’ordre 1 : v = k × [A], [A] décroît exponentiellement et t½ = ln 2 : k ne dépend pas de la concentration initiale. Un mécanisme décrit les actes élémentaires."],
          [("Une réaction d’ordre 1 a t½ = 20 min. Fraction restante après 1 h ?", ["1 h = 3 t½.", "(½)³ = 1/8."], "1/8 du réactif.")],
          [("Un catalyseur est consommé.", "Il est régénéré à la fin."), ("t½ est la moitié de la durée totale.", "C’est la durée pour atteindre la moitié de l’avancement final.")],
          [("Pourquoi conserve-t-on les aliments au froid ?", "La basse température ralentit les réactions de dégradation."), ("Qu’est-ce qu’un intermédiaire réactionnel ?", "Une espèce formée puis consommée au cours du mécanisme.")],
          [("Facteurs cinétiques", [("augmenter la température", "accélère la transformation"), ("augmenter la concentration des réactifs", "accélère la transformation"), ("ajouter un catalyseur", "accélère sans être consommé"),
                                    ("diviser un solide en poudre", "accélère par une plus grande surface"), ("refroidir dans la glace", "ralentit fortement"), ("diluer le milieu", "ralentit la transformation")],
            "Quel effet a {k} ?", None, ("ne change rien", "inverse la réaction")),
           ("Catalyse", [("le catalyseur homogène", "dans la même phase que les réactifs"), ("le catalyseur hétérogène", "dans une phase différente"), ("l’enzyme", "catalyseur biologique"), ("le pot catalytique", "catalyse hétérogène sur métaux"),
                         ("la sélectivité", "le catalyseur oriente vers un produit"), ("la régénération", "le catalyseur est retrouvé à la fin")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Vocabulaire", [("la vitesse volumique", "variation de concentration par unité de temps"), ("le temps de demi-réaction", "durée pour atteindre la moitié de l’avancement final"), ("l’ordre 1", "vitesse proportionnelle à la concentration"),
                            ("l’acte élémentaire", "étape du mécanisme"), ("l’intermédiaire réactionnel", "formé puis consommé"), ("la trempe", "refroidissement brutal pour bloquer la réaction")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["La température est un facteur cinétique.", "Un catalyseur est régénéré.", "Pour l’ordre 1, t½ = ln 2 : k.", "La trempe ralentit fortement une réaction.",
           "Pour l’ordre 1, t½ ne dépend pas de la concentration initiale.", "Une enzyme est un catalyseur biologique.", "Une poudre réagit plus vite qu’un bloc."],
          [("Un catalyseur est consommé.", "Il est régénéré."), ("Le froid accélère les réactions.", "Il les ralentit."), ("Pour l’ordre 1, t½ dépend de la concentration initiale.", "Il n’en dépend pas."),
           ("t½ est la moitié de la durée totale.", "C’est la durée pour la moitié de l’avancement final."), ("Diluer accélère la transformation.", "Cela la ralentit.")],
          "la cinétique", "matter", calc=f_cin),

        H("P", "evolution-spontanee-et-piles", "Évolution spontanée et piles", "Piles et équilibre",
          "Les élèves prévoient le sens d’évolution d’un système en comparant le quotient de réaction Qr à la constante d’équilibre K et décrivent le fonctionnement d’une pile.",
          "état d’équilibre, quotient de réaction Qr, constante d’équilibre K, sens d’évolution spontanée, pile, électrodes, anode, cathode, pont salin, capacité électrique Q = I × Δt",
          "Qr inférieur à K : évolution dans le sens direct", "Dans une pile, l’oxydation a lieu à l’anode (pôle −).",
          ["Pour aA + bB ⇄ cC + dD, Qr = [C]^c [D]^d : ([A]^a [B]^b). À l’équilibre, Qr = K.",
           "Si Qr < K, le système évolue dans le sens direct. Si Qr > K, dans le sens inverse. Si Qr = K, il est à l’équilibre.",
           "Une pile convertit de l’énergie chimique en énergie électrique. L’anode (oxydation) est le pôle −, la cathode (réduction) le pôle +. Le pont salin assure la neutralité. La pile s’use quand Qr atteint K."],
          [("Pour une pile Zn/Cu, quelle électrode est le pôle − ?", ["Le zinc est oxydé : Zn → Zn²⁺ + 2 e⁻.", "L’oxydation a lieu à l’anode."], "L’électrode de zinc.")],
          [("La pile fournit des électrons venant de nulle part.", "Les électrons viennent de l’oxydation à l’anode."), ("Le pont salin transporte des électrons.", "Il transporte des ions.")],
          [("Pourquoi une pile s’use-t-elle ?", "Le système atteint l’équilibre : Qr = K, plus de courant."), ("Qu’est-ce que la capacité d’une pile ?", "La charge maximale qu’elle peut débiter, Q = I × Δt.")],
          [("Sens d’évolution", [("Qr inférieur à K", "évolution dans le sens direct"), ("Qr supérieur à K", "évolution dans le sens inverse"), ("Qr égal à K", "système à l’équilibre"), ("pile neuve qui débite", "Qr inférieur à K"),
                                 ("pile usée", "Qr égal à K"), ("ajout d’un réactif à un équilibre", "Qr diminue, évolution dans le sens direct")],
            "Que se passe-t-il si {k} ?".replace("si {k}", ": {k}"), None),
           ("La pile", [("l’anode", "lieu de l’oxydation, pôle −"), ("la cathode", "lieu de la réduction, pôle +"), ("le pont salin", "assure la neutralité par des ions"), ("le circuit extérieur", "les électrons y circulent"),
                        ("la force électromotrice", "tension à vide de la pile"), ("la capacité", "charge totale débitable")],
            "Que désigne {k} ?", "Quel élément : {v} ?"),
           ("Vocabulaire", [("le quotient de réaction", "Qr calculé avec les concentrations du moment"), ("la constante d’équilibre", "K, valeur de Qr à l’équilibre"), ("le faraday", "charge d’une mole d’électrons, 96 500 C"),
                            ("l’oxydation", "perte d’électrons"), ("la réduction", "gain d’électrons"), ("l’état d’équilibre", "les concentrations ne varient plus")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Si Qr < K, le système évolue dans le sens direct.", "À l’équilibre, Qr = K.", "L’anode est le lieu de l’oxydation.", "Le pont salin transporte des ions.",
           "Une pile usée est à l’équilibre.", "Q = I × Δt.", "La charge d’une mole d’électrons vaut environ 96 500 C."],
          [("Si Qr < K, le système évolue dans le sens inverse.", "Il évolue dans le sens direct."), ("Le pont salin transporte des électrons.", "Il transporte des ions."), ("La réduction a lieu à l’anode.", "À la cathode."),
           ("Une pile usée a Qr < K.", "Qr = K."), ("La cathode est le pôle −.", "C’est le pôle +.")],
          "les piles", "matter", calc=f_pile),

        H("P", "synthese-organique-et-rendement", "Synthèses organiques et rendement", "Synthèse organique",
          "Les élèves identifient les étapes d’une synthèse (transformation, séparation, purification, analyse), les familles fonctionnelles (esters, amines, amides) et calculent un rendement.",
          "squelette carboné, groupes caractéristiques, ester, amine, amide, estérification, hydrolyse, chauffage à reflux, extraction, recristallisation, CCM, spectroscopie IR, rendement",
          "Rendement = masse obtenue : masse théorique", "On optimise une synthèse par la température, un catalyseur ou un excès de réactif.",
          ["Une synthèse comprend : transformation (souvent chauffage à reflux), isolement (filtration, extraction), purification (recristallisation, distillation) et analyse (CCM, température de fusion, IR).",
           "L’estérification acide carboxylique + alcool ⇄ ester + eau est lente et limitée. On l’accélère avec un catalyseur acide et on déplace l’équilibre avec un excès de réactif ou en éliminant l’eau.",
           "Le rendement η = n(obtenu) : n(théorique) = m(obtenue) : m(théorique), toujours inférieur à 100 %."],
          [("Masse théorique 8 g, masse obtenue 6 g. Rendement ?", ["η = 6 : 8.", "= 0,75."], "75 %.")],
          [("Le chauffage à reflux fait perdre les réactifs.", "Le réfrigérant condense les vapeurs, rien n’est perdu."), ("Un catalyseur augmente le rendement à l’équilibre.", "Il accélère, mais ne change pas l’état final.")],
          [("À quoi sert une CCM ?", "À identifier les espèces et vérifier la pureté d’un produit."), ("Que montre une bande large vers 3 300 cm⁻¹ en IR ?", "Une liaison O–H d’un alcool.")],
          [("Familles", [("R–COO–R’", "ester"), ("R–NH₂", "amine"), ("R–CO–NH₂", "amide"), ("R–COOH", "acide carboxylique"), ("R–OH", "alcool"), ("R–CHO", "aldéhyde"), ("R–CO–R’", "cétone")],
            "Quelle famille : {k} ?", None, ("alcène",)),
           ("Étapes et techniques", [("le chauffage à reflux", "accélère sans perte de matière"), ("l’extraction liquide-liquide", "isole une espèce avec un solvant"), ("la recristallisation", "purifie un solide"), ("la distillation", "sépare des liquides"),
                                     ("la CCM", "identifie des espèces"), ("la spectroscopie IR", "repère des liaisons et des groupes"), ("la filtration sous vide", "récupère un solide rapidement")],
            "À quoi sert {k} ?", "Quelle technique {v} ?"),
           ("Optimisation", [("chauffer", "accélère la transformation"), ("ajouter un catalyseur acide", "accélère l’estérification"), ("mettre un réactif en excès", "augmente le rendement"), ("éliminer l’eau formée", "déplace l’équilibre vers l’ester"),
                             ("refroidir le milieu", "ralentit la transformation"), ("utiliser un réactif plus réactif", "rend la synthèse plus rapide et plus totale")],
            "Quel effet a l’action : {k} ?", None)],
          ["Le rendement est toujours inférieur à 100 %.", "L’estérification est lente et limitée.", "Un catalyseur accélère sans changer l’état final.", "La CCM identifie des espèces.",
           "Le chauffage à reflux évite la perte de matière.", "Éliminer l’eau déplace l’équilibre d’estérification.", "Une amine contient le groupe –NH₂."],
          [("Un catalyseur augmente le rendement à l’équilibre.", "Il ne change pas l’état final."), ("Le rendement peut dépasser 100 %.", "Il est inférieur à 100 %."), ("Le chauffage à reflux fait perdre les réactifs.", "Rien n’est perdu."),
           ("R–COO–R’ est une amine.", "C’est un ester."), ("La distillation purifie un solide.", "Elle sépare des liquides.")],
          "la synthèse organique", "matter", calc=f_rdt),

        H("P", "lois-de-newton-et-mouvements", "Lois de Newton, chute libre et projectiles", "Lois de Newton",
          "Les élèves appliquent la deuxième loi de Newton, établissent les équations horaires d’une chute libre et d’un mouvement de projectile, et étudient un mouvement dans un champ électrique.",
          "vecteur accélération, référentiel galiléen, deuxième loi de Newton ΣF = m a, chute libre, équations horaires, trajectoire parabolique, portée, flèche, mouvement d’une particule chargée",
          "ΣF = m × a", "En chute libre, a = g quel que soit la masse.",
          ["Le vecteur accélération a = dv/dt. Deuxième loi de Newton dans un référentiel galiléen : ΣF = m × a.",
           "En chute libre, seul le poids agit : a = g. Les équations horaires : vz = −g t + v₀z, z = −½ g t² + v₀z t + z₀. La trajectoire d’un projectile est parabolique.",
           "Une particule chargée dans un champ électrique uniforme subit F = q E : son mouvement est analogue à celui d’un projectile."],
          [("Une pierre lâchée de 20 m. Durée de chute ?", ["z = ½ g t².", "t = √(2 × 20 : 9,81)."], "Environ 2,0 s.")],
          [("Les objets lourds tombent plus vite.", "En chute libre, a = g pour tous."), ("Au sommet de la trajectoire, l’accélération est nulle.", "Elle vaut toujours g, vers le bas.")],
          [("Pour quel angle la portée est-elle maximale ?", "45°, sans frottement et au même niveau."), ("Qu’est-ce qu’un référentiel galiléen ?", "Un référentiel où le principe d’inertie est vérifié.")],
          [("Grandeurs", [("le vecteur accélération", "dérivée du vecteur vitesse"), ("la deuxième loi de Newton", "ΣF = m × a"), ("la chute libre", "seul le poids agit"), ("la portée", "distance horizontale parcourue"),
                          ("la flèche", "hauteur maximale atteinte"), ("le référentiel galiléen", "où vaut le principe d’inertie"), ("la troisième loi de Newton", "actions réciproques opposées")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Chute libre", [("accélération", "g, verticale vers le bas"), ("vitesse horizontale d’un projectile", "constante"), ("vitesse verticale", "varie linéairement avec le temps"), ("trajectoire d’un projectile", "parabole"),
                            ("angle de portée maximale", "45°"), ("vitesse au sommet", "seulement horizontale")],
            "Que sais-tu de {k} en chute libre ?", None),
           ("Situations", [("une voiture accélère en ligne droite", "a dans le sens du mouvement"), ("une voiture freine", "a opposé au mouvement"), ("un satellite en orbite circulaire", "a dirigé vers le centre"),
                           ("un mouvement rectiligne uniforme", "a nul"), ("un électron entre deux plaques chargées", "a constant, parallèle au champ"), ("une balle au sommet de sa trajectoire", "a = g vers le bas")],
            "Comment est le vecteur accélération : {k} ?", None)],
          ["ΣF = m × a.", "En chute libre, a = g.", "La vitesse horizontale d’un projectile est constante.", "La trajectoire d’un projectile est une parabole.",
           "Au sommet, l’accélération vaut g.", "La portée est maximale pour 45°.", "Un satellite en orbite circulaire a une accélération centripète."],
          [("Les objets lourds tombent plus vite.", "Tous tombent avec a = g."), ("Au sommet, l’accélération est nulle.", "Elle vaut g."), ("La vitesse horizontale diminue.", "Elle est constante."),
           ("ΣF = m × v.", "ΣF = m × a."), ("Un mouvement rectiligne uniforme a une accélération non nulle.", "Elle est nulle.")],
          "les lois de Newton", "forces-and-motion", calc=f_newton),

        H("P", "orbites-et-lois-de-kepler", "Satellites, planètes et lois de Kepler", "Kepler et orbites",
          "Les élèves étudient le mouvement circulaire uniforme d’un satellite ou d’une planète, établissent la vitesse et la période et utilisent les trois lois de Kepler.",
          "repère de Frenet, accélération centripète, mouvement circulaire uniforme, v = √(GM : r), période T = 2πr : v, satellite géostationnaire, lois de Kepler, troisième loi T² : a³",
          "v = √(G M : r)", "T² : a³ a la même valeur pour tous les satellites d’un même astre.",
          ["Un satellite en orbite circulaire subit la seule force gravitationnelle, dirigée vers le centre : son mouvement est circulaire uniforme, a = v² : r.",
           "La deuxième loi de Newton donne v = √(G M : r) et T = 2π r : v. Plus le satellite est haut, plus il est lent.",
           "Lois de Kepler : 1) orbites elliptiques avec le Soleil à un foyer, 2) loi des aires, 3) T² : a³ = constante = 4π² : (G M)."],
          [("Un satellite géostationnaire a T = 24 h. Que voit-on du sol ?", ["Il tourne avec la Terre.", "Il reste au-dessus du même point."], "Il paraît immobile.")],
          [("Un satellite lourd tourne plus vite.", "v ne dépend pas de la masse du satellite."), ("Plus haut, plus rapide.", "Plus r est grand, plus v est petite.")],
          [("À quelle altitude est un satellite géostationnaire ?", "Environ 36 000 km, au-dessus de l’équateur."), ("Que dit la loi des aires ?", "Le rayon Soleil-planète balaie des aires égales en des durées égales.")],
          [("Lois de Kepler", [("première loi", "orbites elliptiques, astre attracteur à un foyer"), ("deuxième loi", "aires égales balayées en des durées égales"), ("troisième loi", "T² : a³ constant"),
                               ("conséquence de la deuxième loi", "la planète va plus vite près du Soleil"), ("le demi-grand axe", "a, dans la troisième loi"), ("le périhélie", "point de l’orbite le plus proche du Soleil")],
            "Que dit ou que désigne {k} ?", None),
           ("Satellites", [("l’ISS", "environ 400 km d’altitude, tour en 1 h 30"), ("un satellite géostationnaire", "36 000 km, période de 24 h"), ("la Lune", "environ 384 000 km, 27,3 jours"), ("un satellite GPS", "20 200 km, environ 12 h"),
                           ("la Terre autour du Soleil", "1 ua, 1 an"), ("Mars autour du Soleil", "1,52 ua, 1,88 an")],
            "Que sais-tu de {k} ?", "Qui correspond à : {v} ?"),
           ("Orbite basse ou haute ?", {"des orbites basses": ["l’ISS", "le télescope Hubble", "la constellation Starlink", "vitesse proche de 7,7 km/s", "période d’environ 1 h 30", "quelques centaines de km d’altitude"],
                                        "des orbites hautes": ["un satellite géostationnaire", "un satellite GPS", "vitesse d’environ 3 km/s", "période de 24 h", "36 000 km d’altitude", "la Lune, satellite naturel"]})],
          ["v = √(G M : r).", "Plus l’orbite est haute, plus la vitesse est faible.", "La vitesse ne dépend pas de la masse du satellite.", "T² : a³ est constant pour un même astre.",
           "Un satellite géostationnaire a une période de 24 h.", "Les orbites des planètes sont elliptiques.", "La planète va plus vite près du Soleil."],
          [("Un satellite lourd tourne plus vite.", "La vitesse ne dépend pas de sa masse."), ("Plus haut, plus rapide.", "Plus haut, plus lent."), ("Les orbites des planètes sont des cercles parfaits.", "Elles sont elliptiques."),
           ("Un satellite géostationnaire tourne en 12 h.", "En 24 h."), ("La planète va plus vite loin du Soleil.", "Elle va plus vite près du Soleil.")],
          "les orbites", "earth-and-space", calc=f_orbite),

        H("P", "thermodynamique-et-transferts-thermiques", "Énergie interne et transferts thermiques", "Thermodynamique",
          "Les élèves décrivent l’énergie interne d’un système, appliquent le premier principe, calculent une variation d’énergie avec la capacité thermique et décrivent les modes de transfert thermique et le modèle du gaz parfait.",
          "énergie interne, premier principe ΔU = W + Q, capacité thermique massique, Q = m × c × ΔT, conduction, convection, rayonnement, flux thermique, résistance thermique, gaz parfait PV = nRT",
          "Q = m × c × ΔT", "ΔU = W + Q : l’énergie se conserve.",
          ["L’énergie interne U d’un système dépend de sa température. Premier principe : ΔU = W + Q (travail et transfert thermique reçus).",
           "Pour un solide ou un liquide : Q = m × c × ΔT, avec c la capacité thermique massique (eau : 4 180 J/(kg·°C)).",
           "Transferts thermiques : conduction (solides), convection (fluides), rayonnement (même dans le vide). Gaz parfait : P × V = n × R × T, T en kelvins."],
          [("Chauffer 2 kg d’eau de 20 °C à 70 °C ?", ["Q = m c ΔT.", "2 × 4 180 × 50."], "418 000 J.")],
          [("Chaleur et température, c’est pareil.", "La température est une grandeur d’état, le transfert thermique est une énergie échangée."), ("Le froid passe de l’extérieur vers l’intérieur.", "La chaleur va toujours du chaud vers le froid.")],
          [("Pourquoi l’eau met-elle longtemps à chauffer ?", "Sa capacité thermique massique est très grande."), ("Comment passer des °C aux kelvins ?", "T(K) = θ(°C) + 273,15.")],
          [("Modes de transfert", [("la cuillère qui chauffe dans le thé", "conduction"), ("l’air chaud qui monte au-dessus d’un radiateur", "convection"), ("la chaleur du Soleil sur la peau", "rayonnement"), ("la casserole sur une plaque", "conduction"),
                                   ("les courants dans l’eau qui chauffe", "convection"), ("la chaleur d’un feu à distance", "rayonnement"), ("le froid d’une poignée métallique", "conduction")],
            "Quel mode de transfert : {k} ?", None, ("évaporation",)),
           ("Grandeurs", [("l’énergie interne", "énergie microscopique du système"), ("la capacité thermique massique", "énergie pour élever 1 kg de 1 °C"), ("le flux thermique", "énergie transférée par seconde"),
                          ("la résistance thermique", "aptitude d’une paroi à freiner le transfert"), ("le kelvin", "unité de température absolue"), ("la constante R", "8,31 J/(mol·K)")],
            "Que désigne {k} ?", "Quel mot : {v} ?"),
           ("Capacités thermiques", [("l’eau", "4 180 J/(kg·°C)"), ("l’aluminium", "900 J/(kg·°C)"), ("le fer", "450 J/(kg·°C)"), ("le cuivre", "385 J/(kg·°C)"), ("l’huile", "environ 2 000 J/(kg·°C)"), ("la glace", "2 100 J/(kg·°C)")],
            "Quelle est la capacité thermique massique de {k} ?", "Quel matériau a une capacité de {v} ?")],
          ["ΔU = W + Q.", "Q = m × c × ΔT.", "La chaleur va du chaud vers le froid.", "Le rayonnement se propage dans le vide.",
           "L’eau a une grande capacité thermique massique.", "T(K) = θ(°C) + 273,15.", "La convection a lieu dans les fluides."],
          [("Chaleur et température sont la même chose.", "Ce sont deux notions différentes."), ("Le froid passe vers le chaud.", "La chaleur va du chaud vers le froid."), ("La conduction a lieu dans le vide.", "C’est le rayonnement."),
           ("L’eau chauffe très vite.", "Sa capacité thermique est grande."), ("T(K) = θ(°C) − 273,15.", "T(K) = θ(°C) + 273,15.")],
          "la thermodynamique", "energy", calc=f_thermo),

        H("P", "diffraction-interferences-et-doppler", "Diffraction, interférences et effet Doppler", "Ondes : diffraction",
          "Les élèves exploitent la diffraction (θ = λ : a), les interférences (interfrange) et l’effet Doppler, et calculent un niveau d’intensité sonore.",
          "diffraction, écart angulaire, interférences, ondes cohérentes, chemin optique, interfrange, effet Doppler, niveau d’intensité sonore L = 10 log(I : I₀), atténuation",
          "θ = λ : a et i = λ × D : b", "Une source qui s’approche est perçue plus aiguë (effet Doppler).",
          ["La diffraction apparaît quand une onde rencontre une ouverture de taille proche de sa longueur d’onde : θ = λ : a.",
           "Deux ondes cohérentes interfèrent : franges brillantes et sombres. Pour les fentes d’Young, l’interfrange vaut i = λ × D : b.",
           "Effet Doppler : la fréquence perçue augmente quand la source s’approche, diminue quand elle s’éloigne. Niveau d’intensité sonore : L = 10 log(I : I₀), en dB."],
          [("λ = 600 nm, a = 0,1 mm. Écart angulaire ?", ["θ = λ : a.", "600 × 10⁻⁹ : 10⁻⁴."], "6 × 10⁻³ rad.")],
          [("Plus la fente est large, plus la diffraction est forte.", "Plus la fente est étroite, plus θ est grand."), ("Deux lampes ordinaires interfèrent.", "Il faut des sources cohérentes.")],
          [("Comment mesure-t-on la vitesse d’un véhicule par radar ?", "Par l’effet Doppler sur l’onde réfléchie."), ("Que gagne-t-on en dB si l’intensité est multipliée par 10 ?", "10 dB.")],
          [("Phénomènes", [("une onde qui contourne un obstacle", "diffraction"), ("des franges alternées brillantes et sombres", "interférences"), ("la sirène plus aiguë qui s’approche", "effet Doppler"), ("les couleurs d’une bulle de savon", "interférences"),
                           ("le son entendu derrière un mur", "diffraction"), ("le décalage vers le rouge des galaxies", "effet Doppler"), ("les couleurs d’un CD", "interférences")],
            "Quel phénomène : {k} ?", None, ("réfraction",)),
           ("Relations", [("écart angulaire de diffraction", "θ = λ : a"), ("interfrange", "i = λ × D : b"), ("niveau d’intensité sonore", "L = 10 log(I : I₀)"), ("interférences constructives", "différence de marche multiple de λ"),
                          ("interférences destructives", "différence de marche égale à un nombre impair de demi-longueurs d’onde"), ("intensité de référence", "I₀ = 10⁻¹² W/m²")],
            "Quelle relation ou condition pour {k} ?", None),
           ("Effet Doppler", [("source qui s’approche", "fréquence perçue plus grande"), ("source qui s’éloigne", "fréquence perçue plus petite"), ("source immobile", "fréquence perçue égale"), ("galaxie qui s’éloigne", "décalage vers le rouge"),
                              ("étoile qui s’approche", "décalage vers le bleu"), ("radar routier", "mesure la vitesse")],
            "Que perçoit-on : {k} ?", None)],
          ["θ = λ : a.", "Plus la fente est étroite, plus la diffraction est marquée.", "Les interférences demandent des sources cohérentes.", "Une source qui s’approche paraît plus aiguë.",
           "L’interfrange vaut λ × D : b.", "Les galaxies lointaines présentent un décalage vers le rouge.", "Multiplier l’intensité par 10 ajoute 10 dB."],
          [("Une fente large diffracte plus.", "Une fente étroite diffracte plus."), ("Une source qui s’approche paraît plus grave.", "Elle paraît plus aiguë."), ("Deux lampes ordinaires interfèrent.", "Il faut des sources cohérentes."),
           ("Multiplier l’intensité par 10 double le niveau en dB.", "Cela ajoute 10 dB."), ("θ = a : λ.", "θ = λ : a.")],
          "les ondes", "waves-and-light", calc=f_diff),

        H("P", "condensateur-et-circuit-rc", "Condensateur et circuit RC", "Circuit RC",
          "Les élèves décrivent le comportement capacitif, la charge et la décharge d’un condensateur dans un circuit RC et déterminent la constante de temps.",
          "condensateur, capacité C, q = C × u, intensité i = dq/dt, circuit RC, charge, décharge, équation différentielle, constante de temps τ = R × C, capteur capacitif",
          "τ = R × C", "Au bout de τ, le condensateur est chargé à 63 %. Au bout de 5τ, presque à 100 %.",
          ["Un condensateur stocke des charges : q = C × u, avec C en farads. L’intensité i = dq/dt = C × du/dt.",
           "Dans un circuit RC soumis à une tension E, la tension u aux bornes du condensateur suit u = E (1 − e^(−t/τ)) avec τ = R × C.",
           "À t = τ, u ≈ 0,63 E. À t = 5τ, le condensateur est pratiquement chargé. Lors de la décharge, u = E × e^(−t/τ)."],
          [("R = 10 kΩ, C = 100 µF. Constante de temps ?", ["τ = R × C.", "10⁴ × 10⁻⁴ = 1."], "1 s.")],
          [("Un condensateur chargé laisse passer un courant continu.", "Une fois chargé, l’intensité devient nulle."), ("τ est la durée de charge complète.", "La charge est pratiquement complète à 5τ.")],
          [("Où trouve-t-on des condensateurs ?", "Dans les flashs, les écrans tactiles, les alimentations."), ("Comment trouver τ graphiquement ?", "Par la tangente à l’origine ou à 63 % de E.")],
          [("Grandeurs", [("la capacité", "s’exprime en farads"), ("la constante de temps", "τ = R × C, en secondes"), ("la charge du condensateur", "q = C × u"), ("l’intensité dans le circuit", "i = C × du/dt"),
                          ("u à t = τ pendant la charge", "environ 63 % de E"), ("u à t = 5τ", "presque égale à E")],
            "Que sais-tu de {k} ?", None),
           ("Charge ou décharge ?", {"de la charge": ["u augmente vers E", "u = E (1 − e^(−t/τ))", "l’intensité diminue de sa valeur maximale vers 0", "le générateur fournit de l’énergie", "63 % de E au bout de τ", "le condensateur stocke de l’énergie"],
                                     "de la décharge": ["u diminue vers 0", "u = E × e^(−t/τ)", "le condensateur restitue son énergie", "37 % de E au bout de τ", "le flash d’un appareil photo se déclenche", "le courant change de sens"]}),
           ("Si l’on change…", [("R est doublée", "τ est doublée"), ("C est divisée par 2", "τ est divisée par 2"), ("E est doublée", "τ ne change pas"), ("R et C sont doublées", "τ est multipliée par 4"),
                                ("C est multipliée par 10", "τ est multipliée par 10"), ("R est divisée par 4", "τ est divisée par 4")],
            "Que devient τ si {k} ?", None)],
          ["τ = R × C.", "À t = τ, u vaut environ 63 % de E.", "À 5τ, le condensateur est pratiquement chargé.", "q = C × u.",
           "Une fois chargé, l’intensité est nulle.", "La capacité s’exprime en farads.", "τ ne dépend pas de E."],
          [("Un condensateur chargé laisse passer le courant continu.", "L’intensité devient nulle."), ("τ = R : C.", "τ = R × C."), ("À t = τ, le condensateur est chargé à 100 %.", "À 63 %."),
           ("τ dépend de la tension E.", "Il ne dépend que de R et C."), ("La capacité s’exprime en coulombs.", "En farads.")],
          "le condensateur", "energy", calc=f_rc),

        H("P", "radioactivite-et-decroissance", "Radioactivité et décroissance radioactive", "Décroissance radioactive",
          "Les élèves écrivent des équations de désintégration, modélisent la décroissance radioactive par une loi exponentielle et utilisent la demi-vie et l’activité.",
          "noyau, isotopes, désintégrations α, β⁻, β⁺, γ, lois de conservation, activité en becquerels, constante radioactive λ, N(t) = N₀ e^(−λt), demi-vie, datation, radioprotection",
          "N(t) = N₀ × e^(−λt)", "Au bout d’une demi-vie, il reste la moitié des noyaux.",
          ["Les désintégrations conservent le nombre de nucléons A et la charge Z. α : émission de ⁴He. β⁻ : un neutron devient proton (émission d’un électron). β⁺ : un proton devient neutron.",
           "Le nombre de noyaux suit N(t) = N₀ × e^(−λt). L’activité A = λ × N, en becquerels (désintégrations par seconde).",
           "La demi-vie t½ = ln 2 : λ. On l’utilise pour dater (carbone 14 : 5 730 ans). La radioprotection : distance, durée, écran."],
          [("Un isotope de demi-vie 8 jours. Fraction restante après 24 jours ?", ["24 : 8 = 3 demi-vies.", "(½)³."], "1/8.")],
          [("Après deux demi-vies, il ne reste plus rien.", "Il reste un quart des noyaux."), ("La radioactivité dépend de la température.", "Elle ne dépend pas des conditions extérieures.")],
          [("Pourquoi le carbone 14 date-t-il les êtres vivants ?", "Un organisme vivant échange du carbone, à sa mort son ¹⁴C décroît."), ("Qu’est-ce qu’un becquerel ?", "Une désintégration par seconde.")],
          [("Désintégrations", [("désintégration α", "émission d’un noyau d’hélium 4"), ("désintégration β⁻", "un neutron devient un proton"), ("désintégration β⁺", "un proton devient un neutron"), ("émission γ", "photon très énergétique"),
                                ("conservation de A", "le nombre de nucléons se conserve"), ("conservation de Z", "la charge se conserve")],
            "Que se passe-t-il lors de : {k} ?", None),
           ("Demi-vies", [("le carbone 14", "5 730 ans"), ("l’iode 131", "8 jours"), ("le césium 137", "30 ans"), ("l’uranium 238", "4,5 milliards d’années"), ("le radon 222", "3,8 jours"), ("le cobalt 60", "5,3 ans"), ("le potassium 40", "1,25 milliard d’années")],
            "Quelle est la demi-vie de {k} ?", "Quel isotope a une demi-vie de {v} ?"),
           ("Vocabulaire", [("l’activité", "nombre de désintégrations par seconde"), ("le becquerel", "unité d’activité"), ("la constante radioactive", "probabilité de désintégration par seconde"), ("la demi-vie", "durée pour que la moitié des noyaux se désintègre"),
                            ("le sievert", "unité de dose efficace"), ("la radioprotection", "distance, durée, écran")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["La radioactivité conserve A et Z.", "Au bout d’une demi-vie, il reste la moitié des noyaux.", "A = λ × N.", "La demi-vie du carbone 14 est d’environ 5 730 ans.",
           "La radioactivité ne dépend pas de la température.", "Le becquerel est une désintégration par seconde.", "t½ = ln 2 : λ."],
          [("Après deux demi-vies, il ne reste rien.", "Il reste un quart."), ("La radioactivité dépend de la température.", "Elle n’en dépend pas."), ("Lors de β⁻, un proton devient neutron.", "Un neutron devient proton."),
           ("t½ = λ : ln 2.", "t½ = ln 2 : λ."), ("La désintégration α émet un électron.", "Elle émet un noyau d’hélium.")],
          "la radioactivité", "matter", calc=f_radio),

        H("S", "brassages-genetiques-et-meiose", "Méiose, fécondation et brassages génétiques", "Brassages génétiques",
          "Les élèves expliquent le brassage interchromosomique et intrachromosomique (crossing-over) lors de la méiose, la fécondation et leur rôle dans la diversité génétique, à partir de croisements.",
          "méiose, cellules haploïdes et diploïdes, chromosomes homologues, brassage interchromosomique, crossing-over, brassage intrachromosomique, fécondation, croisement test, accidents de méiose, duplication de gènes",
          "Méiose et fécondation créent une diversité infinie", "Le crossing-over échange des portions entre chromosomes homologues.",
          ["La méiose transforme une cellule diploïde (2n) en quatre cellules haploïdes (n). Elle comprend deux divisions.",
           "Brassage interchromosomique : en anaphase I, les chromosomes homologues se répartissent au hasard (2²³ combinaisons chez l’humain). Brassage intrachromosomique : en prophase I, le crossing-over échange des portions de chromatides.",
           "La fécondation réunit deux gamètes au hasard. Un croisement test avec un homozygote récessif révèle les gamètes produits. Des accidents (non-disjonction, duplications) créent aussi de la diversité."],
          [("Croisement test : 4 phénotypes à 25 % chacun. Que conclure ?", ["Quatre types de gamètes équiprobables.", "Les gènes sont indépendants."], "Brassage interchromosomique, gènes sur des chromosomes différents.")],
          [("La méiose donne des cellules identiques.", "Les quatre cellules sont génétiquement différentes."), ("Le crossing-over a lieu en mitose.", "Il a lieu en prophase I de méiose.")],
          [("Combien de gamètes différents sans crossing-over chez l’humain ?", "2²³, environ 8 millions."), ("Qu’est-ce qu’une non-disjonction ?", "Des chromosomes ne se séparent pas : un gamète a un chromosome en trop, comme dans la trisomie 21.")],
          [("Méiose", [("la prophase I", "appariement des homologues et crossing-over"), ("l’anaphase I", "séparation des chromosomes homologues"), ("l’anaphase II", "séparation des chromatides"), ("la fin de la méiose", "quatre cellules haploïdes"),
                       ("la fécondation", "rétablit la diploïdie"), ("la méiose I", "division réductionnelle"), ("la méiose II", "division équationnelle")],
            "Que se passe-t-il pendant {k} ?", "Quelle étape : {v} ?"),
           ("Croisements tests", [("4 phénotypes à 25 % chacun", "gènes indépendants"), ("2 phénotypes parentaux majoritaires et 2 recombinés minoritaires", "gènes liés avec crossing-over"), ("seulement 2 phénotypes parentaux", "gènes liés sans crossing-over"),
                                  ("un seul phénotype en F1", "parents homozygotes"), ("phénotypes recombinés", "issus d’un brassage")],
            "Que conclure : {k} ?", None, ("mutation",)),
           ("Vocabulaire", [("diploïde", "cellule à 2n chromosomes"), ("haploïde", "cellule à n chromosomes"), ("les chromosomes homologues", "paire de chromosomes portant les mêmes gènes"), ("le crossing-over", "échange de portions de chromatides"),
                            ("le brassage interchromosomique", "répartition au hasard des homologues"), ("la non-disjonction", "chromosomes non séparés"), ("la famille multigénique", "gènes issus de duplications")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["La méiose donne quatre cellules haploïdes.", "Le crossing-over a lieu en prophase I.", "En anaphase I, les homologues se séparent au hasard.", "La fécondation rétablit la diploïdie.",
           "Un croisement test utilise un homozygote récessif.", "Une non-disjonction peut causer une trisomie.", "Les gamètes sont génétiquement tous différents."],
          [("La méiose donne des cellules identiques.", "Elles sont différentes."), ("Le crossing-over a lieu en mitose.", "En prophase I de méiose."), ("Les gamètes sont diploïdes.", "Ils sont haploïdes."),
           ("Des gènes indépendants donnent 2 phénotypes en croisement test.", "Ils en donnent 4 à 25 %."), ("La fécondation divise le nombre de chromosomes.", "Elle le rétablit.")],
          "la méiose", "living-things-and-ecosystems"),

        H("S", "evolution-et-histoire-des-especes", "Évolution, sélection et histoire humaine", "Évolution",
          "Les élèves modélisent l’évolution des fréquences alléliques (Hardy-Weinberg, sélection, dérive), expliquent la spéciation et situent l’histoire évolutive de la lignée humaine.",
          "modèle de Hardy-Weinberg, forces évolutives, sélection naturelle, dérive, migrations, spéciation, arbres phylogénétiques, lignée humaine, Homo sapiens, transferts horizontaux, coévolution",
          "Sans force évolutive, les fréquences ne changent pas", "C’est le modèle de Hardy-Weinberg : p² + 2pq + q² = 1.",
          ["Dans une grande population, sans mutation, sélection, migration ni dérive, avec des unions au hasard, les fréquences alléliques restent stables (Hardy-Weinberg).",
           "Les écarts au modèle révèlent les forces évolutives. Une barrière reproductive entre populations conduit à la spéciation.",
           "L’humain est un primate. Homo sapiens est apparu en Afrique il y a environ 300 000 ans. Plusieurs espèces du genre Homo ont coexisté (Néandertal, Denisova)."],
          [("q = 0,1 pour un allèle récessif. Fréquence des homozygotes récessifs ?", ["Sous Hardy-Weinberg, f(aa) = q².", "0,1² = 0,01."], "1 %.")],
          [("L’humain descend du chimpanzé.", "Ils partagent un ancêtre commun."), ("Hardy-Weinberg décrit les populations qui évoluent.", "Il décrit une population sans force évolutive.")],
          [("Pourquoi les Européens ont-ils de l’ADN néandertalien ?", "Il y a eu des métissages entre Homo sapiens et Néandertal."), ("Qu’est-ce que la coévolution ?", "L’évolution conjointe de deux espèces en interaction, comme une fleur et son pollinisateur.")],
          [("Forces évolutives", [("la sélection naturelle", "favorise les allèles avantageux"), ("la dérive génétique", "change les fréquences au hasard"), ("la migration", "apporte des allèles d’autres populations"), ("la mutation", "crée de nouveaux allèles"),
                                  ("l’isolement reproducteur", "mène à la spéciation"), ("la sélection sexuelle", "favorise les caractères attractifs pour les partenaires")],
            "Quel est l’effet de {k} ?", "Quelle force {v} ?"),
           ("Lignée humaine", [("Homo sapiens", "apparu en Afrique il y a environ 300 000 ans"), ("Homo neanderthalensis", "a vécu en Europe jusqu’à environ 40 000 ans"), ("Toumaï", "un des plus anciens fossiles de la lignée humaine, 7 millions d’années"),
                               ("Lucy", "australopithèque d’environ 3,2 millions d’années"), ("Homo erectus", "a quitté l’Afrique il y a environ 1,8 million d’années"), ("l’Homme de Denisova", "connu surtout par son ADN")],
            "Que sais-tu de {k} ?", "Qui correspond à : {v} ?"),
           ("Hardy-Weinberg", [("fréquence des homozygotes dominants", "p²"), ("fréquence des hétérozygotes", "2pq"), ("fréquence des homozygotes récessifs", "q²"), ("somme des fréquences alléliques", "p + q = 1"),
                               ("somme des fréquences génotypiques", "p² + 2pq + q² = 1"), ("condition du modèle", "population grande, sans force évolutive")],
            "Que vaut ou que demande {k} ?", None)],
          ["Sans force évolutive, les fréquences alléliques restent stables.", "f(aa) = q² sous Hardy-Weinberg.", "Homo sapiens est apparu en Afrique.", "L’humain et le chimpanzé ont un ancêtre commun.",
           "La dérive change les fréquences au hasard.", "L’isolement reproducteur mène à la spéciation.", "Néandertal et Homo sapiens se sont métissés."],
          [("L’humain descend du chimpanzé.", "Ils ont un ancêtre commun."), ("Hardy-Weinberg décrit une population qui évolue.", "Il décrit une population stable."), ("Homo sapiens est apparu en Europe.", "En Afrique."),
           ("f(aa) = 2q.", "f(aa) = q²."), ("La dérive favorise les allèles avantageux.", "Elle agit au hasard.")],
          "l’évolution", "living-things-and-ecosystems"),

        H("S", "datation-et-histoire-de-la-terre", "Datation relative, absolue et histoire de la Terre", "Datation",
          "Les élèves utilisent les principes de datation relative, la radiochronologie et reconstituent des épisodes de l’histoire géologique (chaînes de montagnes, crises biologiques).",
          "principe de superposition, de recoupement, d’inclusion, de continuité, fossiles stratigraphiques, échelle des temps géologiques, radiochronologie, demi-vie, chaîne de montagnes, crises biologiques",
          "Les couches du bas sont plus anciennes", "La radiochronologie donne un âge en années grâce à la demi-vie d’un isotope.",
          ["Datation relative : principes de superposition (le bas est plus ancien), de recoupement (ce qui recoupe est plus récent), d’inclusion (les morceaux inclus sont plus anciens), de continuité.",
           "Les fossiles stratigraphiques (ammonites, trilobites) caractérisent une période courte : ils permettent de corréler des couches éloignées.",
           "Datation absolue : on mesure les proportions d’un isotope père et d’un isotope fils, connaissant la demi-vie (potassium-argon, rubidium-strontium, carbone 14 pour moins de 50 000 ans)."],
          [("Un fossile contient 25 % de son ¹⁴C initial. Âge ?", ["25 % = (½)².", "2 × 5 730."], "Environ 11 460 ans.")],
          [("Le carbone 14 date les roches de millions d’années.", "Il ne date que jusqu’à environ 50 000 ans."), ("Une faille est plus ancienne que les couches qu’elle coupe.", "Elle est plus récente (recoupement).")],
          [("Qu’est-ce qu’un fossile stratigraphique ?", "Une espèce répandue qui a vécu peu de temps, utile pour dater les couches."), ("Quand a eu lieu la crise Crétacé-Paléogène ?", "Il y a 66 millions d’années.")],
          [("Principes", [("la superposition", "une couche est plus récente que celle qu’elle recouvre"), ("le recoupement", "ce qui recoupe est plus récent"), ("l’inclusion", "les éléments inclus sont plus anciens"), ("la continuité", "une même couche a le même âge partout"),
                          ("l’identité paléontologique", "mêmes fossiles stratigraphiques, même âge")],
            "Que dit le principe de {k} ?", "Quel principe : {v} ?", ("une couche est toujours horizontale",)),
           ("Isotopes", [("le carbone 14", "jusqu’à environ 50 000 ans"), ("le potassium 40", "roches volcaniques anciennes"), ("le rubidium 87", "roches très anciennes, granites"), ("l’uranium 238", "âge de la Terre"),
                         ("la demi-vie", "durée de désintégration de la moitié des noyaux"), ("l’isotope fils", "produit de la désintégration")],
            "Que sais-tu de {k} ?", None),
           ("Repères", [("la formation de la Terre", "il y a 4,57 milliards d’années"), ("la crise Crétacé-Paléogène", "il y a 66 millions d’années"), ("la crise Permien-Trias", "il y a 252 millions d’années"),
                        ("l’apparition des premiers êtres vivants", "il y a plus de 3,5 milliards d’années"), ("la formation des Alpes", "depuis environ 100 millions d’années"), ("l’apparition d’Homo sapiens", "il y a environ 300 000 ans")],
            "Quand a eu lieu {k} ?", "Qu’est-ce qui date de {v} ?")],
          ["Les couches du bas sont plus anciennes.", "Ce qui recoupe est plus récent.", "Le carbone 14 date jusqu’à environ 50 000 ans.", "La Terre a environ 4,57 milliards d’années.",
           "Les ammonites sont des fossiles stratigraphiques.", "La crise Crétacé-Paléogène date de 66 millions d’années.", "Les éléments inclus sont plus anciens que la roche qui les contient."],
          [("Le carbone 14 date les roches de millions d’années.", "Seulement jusqu’à environ 50 000 ans."), ("Une faille est plus ancienne que les couches qu’elle coupe.", "Elle est plus récente."), ("Les couches du haut sont plus anciennes.", "Celles du bas."),
           ("La Terre a 6 000 ans.", "Environ 4,57 milliards d’années."), ("Les éléments inclus sont plus récents.", "Ils sont plus anciens.")],
          "la datation", "earths-systems", calc=f_datation),

        H("S", "la-plante-et-la-domestication", "La plante productrice et sa domestication", "Plante et domestication",
          "Les élèves relient l’organisation de la plante à sa vie fixée, décrivent la photosynthèse et la reproduction des plantes à fleurs, et la domestication des espèces cultivées.",
          "vie fixée, surfaces d’échange, photosynthèse, chloroplastes, sève brute et élaborée, saccharose, amidon, cellulose, fleur, pollinisation, coévolution, domestication, sélection variétale",
          "La plante fabrique sa matière avec la lumière", "L’humain a domestiqué les plantes en sélectionnant des caractères utiles.",
          ["Fixée au sol, la plante développe de grandes surfaces d’échange : feuilles (lumière, CO₂), racines (eau, ions). Elle se défend chimiquement et s’adapte aux saisons.",
           "La photosynthèse dans les chloroplastes produit du glucose, transformé en saccharose (transporté par la sève élaborée), en amidon (réserve) ou en cellulose (paroi).",
           "La reproduction des plantes à fleurs repose souvent sur la coévolution avec les pollinisateurs. Depuis 10 000 ans, l’humain a domestiqué des plantes (blé, maïs) par sélection, puis par génie génétique."],
          [("Pourquoi le maïs actuel a-t-il de gros épis ?", ["Ses ancêtres, comme la téosinte, avaient de petits épis.", "Les agriculteurs ont choisi les meilleurs grains à semer."], "Par sélection humaine pendant des milliers d’années.")],
          [("La plante tire sa matière du sol.", "L’essentiel de sa matière vient du CO₂ de l’air."), ("La sève brute contient des sucres.", "La sève brute transporte l’eau et les ions, la sève élaborée les sucres.")],
          [("Qu’est-ce que la coévolution ?", "L’évolution conjointe de la fleur et de son pollinisateur."), ("Quel est le risque de la sélection variétale ?", "Une perte de diversité génétique des cultures.")],
          [("Organes et fonctions", [("la feuille", "capte la lumière et le CO₂"), ("la racine", "absorbe l’eau et les ions"), ("le xylème", "conduit la sève brute"), ("le phloème", "conduit la sève élaborée"),
                                     ("le stomate", "permet les échanges gazeux"), ("le chloroplaste", "réalise la photosynthèse"), ("la mycorhize", "association racine et champignon")],
            "Quel est le rôle de {k} ?", "Qu’est-ce qui {v} ?"),
           ("Molécules", [("le glucose", "produit de la photosynthèse"), ("le saccharose", "sucre transporté par la sève élaborée"), ("l’amidon", "réserve dans les tubercules et les graines"), ("la cellulose", "constituant de la paroi"),
                          ("la lignine", "renforce le bois"), ("les tanins", "défense contre les herbivores")],
            "Que sais-tu de {k} ?", "Quelle molécule : {v} ?"),
           ("Domestication", [("le blé", "domestiqué au Proche-Orient il y a environ 10 000 ans"), ("le maïs", "domestiqué au Mexique à partir de la téosinte"), ("le riz", "domestiqué en Asie"), ("la pomme de terre", "domestiquée dans les Andes"),
                              ("la sélection variétale", "choix des plantes aux caractères utiles"), ("le génie génétique", "introduction ciblée de gènes")],
            "Que sais-tu de {k} ?", None)],
          ["La plante fabrique sa matière organique par photosynthèse.", "La sève élaborée transporte les sucres.", "L’amidon est une réserve.", "Le maïs descend de la téosinte.",
           "Les stomates permettent les échanges gazeux.", "La cellulose constitue la paroi.", "La sélection variétale peut réduire la diversité génétique."],
          [("La plante tire sa matière du sol.", "Elle vient surtout du CO₂."), ("La sève brute transporte les sucres.", "Elle transporte l’eau et les ions."), ("Le blé a été domestiqué au Mexique.", "Au Proche-Orient."),
           ("L’amidon constitue la paroi.", "C’est la cellulose."), ("La domestication date du XXe siècle.", "Elle commence il y a environ 10 000 ans.")],
          "la plante", "living-things-and-ecosystems"),

        H("S", "climats-passes-et-futurs", "Les climats de la Terre : passé et futur", "Climats",
          "Les élèves reconstituent les climats passés (glaces, pollens, isotopes), relient les variations climatiques aux causes astronomiques et au CO₂, et analysent le réchauffement actuel et ses conséquences.",
          "climat, glaciations, carottes de glace, rapport isotopique de l’oxygène, pollens, paramètres orbitaux, effet de serre, rétroactions, CO₂, réchauffement actuel, GIEC, atténuation, adaptation",
          "Les glaces et les sédiments gardent la mémoire des climats", "Le réchauffement actuel est causé par les émissions humaines de gaz à effet de serre.",
          ["On reconstitue les climats passés grâce aux bulles d’air des glaces (CO₂ ancien), au rapport isotopique de l’oxygène (δ¹⁸O), aux pollens et aux sédiments.",
           "Sur des dizaines de milliers d’années, les glaciations alternent avec des périodes chaudes sous l’effet des paramètres orbitaux de la Terre, amplifiés par le CO₂ et l’albédo.",
           "Depuis 1850, le CO₂ est passé d’environ 280 à plus de 420 ppm et la température moyenne a augmenté d’environ 1,2 °C. Conséquences : montée des océans, événements extrêmes. Il faut atténuer et s’adapter."],
          [("La glace fond et laisse place à de l’eau sombre. Quel effet sur le climat ?", ["L’eau sombre absorbe plus de lumière.", "L’albédo diminue, la Terre chauffe plus."], "Une rétroaction positive qui amplifie le réchauffement.")],
          [("Le climat a toujours changé, donc l’humain n’y est pour rien.", "Le réchauffement actuel est très rapide et lié aux émissions humaines."), ("La fonte de la banquise fait beaucoup monter les océans.", "La banquise flotte déjà : ce sont les glaciers et la dilatation de l’eau.")],
          [("Que contient une carotte de glace ?", "Des bulles d’air ancien et des isotopes qui renseignent sur la température."), ("Qu’est-ce que l’albédo ?", "La part de lumière solaire réfléchie par une surface.")],
          [("Indices climatiques", [("les bulles d’air des glaces", "teneur en CO₂ du passé"), ("le rapport isotopique de l’oxygène", "température du passé"), ("les pollens fossiles", "végétation et climat du passé"), ("les moraines", "anciennes extensions des glaciers"),
                                    ("les coraux fossiles", "niveau et température de la mer"), ("les cernes des arbres", "climat des derniers siècles")],
            "Que nous apprennent {k} ?", None),
           ("Rétroactions", {"des rétroactions positives (amplifient le réchauffement)": ["la fonte des glaces diminue l’albédo", "un océan plus chaud dissout moins de CO₂", "le dégel du pergélisol libère du méthane", "plus de vapeur d’eau dans un air plus chaud", "les incendies de forêt libèrent du CO₂", "la neige remplacée par de la terre sombre"],
                             "des rétroactions négatives (atténuent le réchauffement)": ["plus de végétation absorbe plus de CO₂", "une Terre plus chaude rayonne plus d’énergie vers l’espace", "l’altération des roches consomme du CO₂", "plus de plancton fixe du carbone", "des forêts qui poussent plus vite grâce au CO₂"]}),
           ("Vocabulaire", [("le GIEC", "experts qui évaluent le climat"), ("l’albédo", "part de lumière réfléchie"), ("l’atténuation", "réduire les émissions"), ("l’adaptation", "se préparer aux effets"),
                            ("une glaciation", "période froide avec de grands glaciers"), ("les paramètres orbitaux", "variations de l’orbite et de l’axe terrestres"), ("le forçage radiatif", "modification du bilan d’énergie de la Terre")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Les glaces gardent la mémoire du CO₂ ancien.", "Les glaciations dépendent des paramètres orbitaux.", "Le CO₂ dépasse aujourd’hui 420 ppm.", "La fonte de la glace diminue l’albédo.",
           "Le réchauffement actuel est lié aux activités humaines.", "La dilatation de l’eau fait monter les océans.", "Le GIEC évalue le climat."],
          [("Le réchauffement actuel est naturel.", "Il est lié aux émissions humaines."), ("La fonte de la banquise fait beaucoup monter les océans.", "Ce sont surtout les glaciers et la dilatation."), ("Plus de glace diminue l’albédo.", "Elle l’augmente."),
           ("Le CO₂ actuel est de 280 ppm.", "Il dépasse 420 ppm."), ("Les pollens ne renseignent pas sur le climat.", "Ils renseignent sur la végétation et le climat.")],
          "les climats", "earths-systems"),

        H("S", "cerveau-comportements-et-stress", "Comportements, cerveau et stress", "Cerveau et stress",
          "Les élèves décrivent le réflexe myotatique, la commande volontaire du mouvement, la plasticité cérébrale et la réponse de l’organisme au stress (système nerveux et hormones).",
          "réflexe myotatique, fuseau neuromusculaire, motoneurone, synapse, neurotransmetteur, intégration, cortex moteur, plasticité cérébrale, stress aigu, adrénaline, cortisol, axe hypothalamo-hypophyso-corticosurrénalien",
          "Le réflexe myotatique passe par la moelle épinière", "Le stress mobilise l’adrénaline puis le cortisol.",
          ["Réflexe myotatique : l’étirement d’un muscle stimule un fuseau neuromusculaire, le message va par un neurone sensoriel à la moelle épinière, qui commande la contraction du même muscle par un motoneurone.",
           "Le mouvement volontaire est commandé par le cortex moteur. Les neurones communiquent par synapses chimiques (neurotransmetteurs). Le cerveau est plastique : il se remodèle avec l’apprentissage.",
           "Face à un stress aigu, l’adrénaline (médullosurrénale) agit en quelques secondes, puis le cortisol (corticosurrénale) mobilise le glucose. Le cortisol freine sa propre production (rétrocontrôle). Le stress chronique nuit à la santé."],
          [("Le médecin frappe le tendon sous le genou et la jambe se tend. Quel réflexe ?", ["Le muscle est étiré.", "Il se contracte en retour, sans le cerveau."], "Le réflexe myotatique.")],
          [("Un réflexe est commandé par le cerveau.", "Le réflexe myotatique est commandé par la moelle épinière."), ("Le cerveau adulte ne change plus.", "Il reste plastique toute la vie.")],
          [("Pourquoi le cœur bat-il vite quand on a peur ?", "L’adrénaline augmente la fréquence cardiaque."), ("Comment limiter le stress chronique ?", "Sommeil, activité physique, liens sociaux, temps de repos.")],
          [("Le circuit du réflexe", [("le fuseau neuromusculaire", "récepteur sensible à l’étirement"), ("le neurone sensoriel", "conduit le message vers la moelle"), ("la moelle épinière", "centre nerveux du réflexe"),
                                      ("le motoneurone", "commande la contraction du muscle"), ("la synapse neuromusculaire", "transmet le message au muscle"), ("l’acétylcholine", "neurotransmetteur de la jonction neuromusculaire")],
            "Quel est le rôle de {k} ?", "Qu’est-ce qui {v} ?"),
           ("Stress", [("l’adrénaline", "agit en quelques secondes"), ("le cortisol", "mobilise le glucose en quelques minutes"), ("l’hypothalamus", "déclenche la réponse hormonale"), ("l’hypophyse", "sécrète l’ACTH"),
                       ("la corticosurrénale", "produit le cortisol"), ("le rétrocontrôle négatif", "le cortisol freine sa propre production"), ("le stress chronique", "affaiblit l’immunité et le sommeil")],
            "Que sais-tu de {k} ?", "Qu’est-ce qui {v} ?"),
           ("Vocabulaire", [("la plasticité cérébrale", "remodelage du cerveau par l’expérience"), ("le cortex moteur", "commande les mouvements volontaires"), ("le neurotransmetteur", "molécule libérée à la synapse"), ("l’intégration", "le neurone additionne les messages reçus"),
                            ("le motoneurone", "neurone qui commande un muscle"), ("le stress aigu", "réponse brève et adaptative")],
            "Que désigne {k} ?", "Quel mot : {v} ?")],
          ["Le réflexe myotatique passe par la moelle épinière.", "Le cortex moteur commande le mouvement volontaire.", "Le cerveau reste plastique toute la vie.", "L’adrénaline agit en quelques secondes.",
           "Le cortisol mobilise le glucose.", "Le cortisol freine sa propre production.", "Le stress chronique nuit à la santé."],
          [("Un réflexe est commandé par le cortex.", "Par la moelle épinière."), ("Le cerveau adulte ne change plus.", "Il reste plastique."), ("Le cortisol agit en quelques secondes.", "C’est l’adrénaline."),
           ("Le stress chronique améliore l’immunité.", "Il l’affaiblit."), ("Le motoneurone conduit le message vers la moelle.", "C’est le neurone sensoriel.")],
          "le cerveau et le stress", "living-things-and-ecosystems"),
    ]
