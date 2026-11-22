# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : La proportionnalité (domaine Proportionnalité)
  python3 tools/gen_fr_maths_cm1_proportionnalite.py
Identifier une situation de proportionnalité, compléter un tableau (coefficient, propriétés additive et multiplicative,
passage par l’unité), recettes, problèmes. CM2 : décimaux et passage par l’unité plus fréquent.
Erreurs : ajouter le même nombre au lieu de multiplier (4 → 6, 8 → 10), croire que l’âge et la taille sont proportionnels.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, dz, table

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52115 + 100 * lv)
    K = Kids(R)


def tab(h1, h2, xs, ys):
    return table([h1] + [str(x) for x in xs], [[h2] + [str(y) for y in ys]])


SIT = [("Le prix de baguettes identiques et leur nombre", True), ("La taille d’un enfant et son âge", False), ("Le périmètre d’un carré et la longueur de son côté", True),
       ("La masse de pommes et leur prix (même prix au kilo)", True), ("La pointure de chaussures et l’âge", False), ("Le nombre de roues et le nombre de vélos", True),
       ("La quantité de farine et le nombre de gâteaux identiques", True), ("La température et l’heure de la journée", False), ("Le prix d’un lot « 3 achetés, 1 offert » et le nombre de lots", True),
       ("Le nombre de pages lues et le temps, si l’on lit toujours à la même vitesse", True), ("La note à un contrôle et le temps passé à réviser", False), ("Le poids d’un bébé et son âge", False)]


def s1():
    if R.random() < 0.45:
        t, ok = R.choice(SIT)
        return mcq("Ces deux grandeurs sont-elles proportionnelles ? %s." % t, "oui" if ok else "non", ["non" if ok else "oui", "on ne peut jamais savoir", "seulement au début"],
                   ("Quand l’une est multipliée par 2, 3…, l’autre aussi : <b>oui</b>." if ok else "Quand l’une double, l’autre ne double pas forcément : <b>non</b>."))
    c = R.randint(2, 9)
    xs = sorted(R.sample(range(1, 12), 4))
    ys = [c * x for x in xs]
    ok = R.random() < 0.5
    if not ok:
        i = R.randint(1, 3)
        ys[i] += R.choice([1, -1, 2])
    return mcq("Ce tableau est-il un tableau de proportionnalité ?" + tab("Quantité", "Prix (€)", xs, ys), "oui, on multiplie par %d" % c if ok else "non",
               ["non" if ok else "oui, on multiplie par %d" % c, "oui, on ajoute %d" % (ys[0] - xs[0]), "oui, on multiplie par %d" % (c + 1)],
               ("Chaque prix est égal à la quantité %s %d : <b>oui</b>." % (FOIS, c)) if ok else ("%d %s %d ≠ %d : ce n’est <b>pas</b> proportionnel." % (xs[i], FOIS, c, ys[i])))


def s2():
    c = R.randint(2, 12) if L == 1 else R.choice([R.randint(2, 15), R.randint(11, 49) / 10.0])
    xs = sorted(R.sample(range(2, 15), 4))
    i = R.randint(1, 3)
    fmt = (lambda v: num(int(round(v)))) if c == int(c) else (lambda v: dz(int(round(v * 10)), 1))
    ys = [fmt(c * x) for x in xs]
    right = ys[i]
    shown = ys[:]
    shown[i] = "?"
    w = [fmt(c * xs[0] + (xs[i] - xs[0])), fmt(c * (xs[i] + 1)), fmt(c * xs[i] + c * 10 if c == int(c) else c * xs[i] * 10)]
    return mcq("Complète le tableau de proportionnalité." + tab("Nombre d’objets", "Prix (€)", xs, shown), right, w,
               "On passe de la première ligne à la deuxième en multipliant par %s : %d %s %s = <b>%s</b>." % (fmt(c) if c == int(c) else dz(int(round(c * 10)), 1), xs[i], FOIS, fmt(c) if c == int(c) else dz(int(round(c * 10)), 1), right))


def s3():
    k = R.choice(["add", "mul", "unit"])
    u = R.randint(2, 12) if L == 1 else R.randint(105, 499)
    p = K.next()
    if k == "add":
        a, b = R.randint(2, 6), R.randint(2, 6)
        if a == b:
            return None
        pa, pb = a * u, b * u
        f = (lambda v: "%s €" % num(v)) if L == 1 else (lambda v: "%s €" % dz(v, 2, True))
        return mcq("%d places de cinéma coûtent %s et %d places coûtent %s. Combien coûtent %d places ?" % (a, f(pa), b, f(pb), a + b), f(pa + pb), [f(pa * pb // u // u) if a * b != a + b else f(pa + pb + u), f(pa + pb - u), f(u * (a + b + 1))],
                       "%d places = %d places + %d places : %s + %s = <b>%s</b>." % (a + b, a, b, f(pa), f(pb), f(pa + pb)))
    if k == "mul":
        a, m = R.randint(2, 5), R.randint(2, 6)
        f = (lambda v: "%s €" % num(v)) if L == 1 else (lambda v: "%s €" % dz(v, 2, True))
        return mcq("%d kg de pommes coûtent %s. Combien coûtent %d kg ?" % (a, f(a * u), a * m), f(a * m * u), [f(a * u + a * m), f(a * u * m * m), f(a * u + m * u)],
                   "%d kg, c’est %d fois %d kg : %s %s %d = <b>%s</b>." % (a * m, m, a, f(a * u), FOIS, m, f(a * m * u)))
    a, b = R.randint(3, 8), R.randint(2, 9)
    if a == b:
        return None
    f = (lambda v: "%s €" % num(v)) if L == 1 else (lambda v: "%s €" % dz(v, 2, True))
    return mcq("%d cahiers coûtent %s. Combien coûtent %d cahiers ?" % (a, f(a * u), b), f(b * u), [f(a * u + (b - a)) if b > a else f(a * u - (a - b)), f(a * u * b), f(b * u + u)],
               "Prix d’un cahier : %s %s %d = %s. Pour %d : %s %s %d = <b>%s</b>." % (f(a * u), DIV, a, f(u), b, f(u), FOIS, b, f(b * u)))


REC = [("farine", "g", 50), ("lait", "mL", 100), ("sucre", "g", 25), ("beurre", "g", 20), ("œufs", "", 1)]


def s4():
    n0 = R.choice([4, 6, 8])
    n1 = R.choice([2, 3, 12, 10, 16, 5]) if L == 2 else R.choice([n0 * 2, n0 * 3, n0 // 2])
    if n1 == n0 or (n1 * 1.0 / n0 * 4) != int(n1 * 4 // n0) and L == 1:
        return None
    ing, u, step = R.choice(REC)
    q0 = step * R.randint(2, 8) * (n0 // 2 if ing == "œufs" else 1)
    q1 = q0 * n1 / n0
    if q1 != int(q1):
        return None
    q1 = int(q1)
    us = (" " + u) if u else ""
    return mcq("Une recette pour %d personnes demande %s%s de %s. Quelle quantité faut-il pour %d personnes ?" % (n0, num(q0), us, ing, n1) if ing != "œufs" else
               "Une recette pour %d personnes demande %d œufs. Combien d’œufs faut-il pour %d personnes ?" % (n0, q0, n1), num(q1) + us,
               [num(q0 + n1 - n0 if q0 + n1 - n0 > 0 else q0 + 1) + us, num(q0 * n1) + us, num(q1 + step) + us],
               "On passe de %d à %d personnes : on multiplie la quantité de la même façon (%s %s %d %s %d) : <b>%s%s</b>." % (n0, n1, num(q0), DIV, n0, FOIS, n1, num(q1), us))


def s5():
    p = K.next()
    k = R.choice(["voiture", "robinet", "pas", "echelle"])
    if k == "voiture":
        c, d = R.randint(4, 8), R.choice([100, 200, 300, 50, 150, 250])
        return mcq("Une voiture consomme %d L d’essence pour 100 km. Combien consomme-t-elle pour %d km ?" % (c, d), "%s L" % (num(c * d // 100) if c * d % 100 == 0 else dz(c * d // 10, 1)),
                   ["%s L" % num(c + d - 100) if c + d > 100 else "%d L" % (c + 1), "%s L" % num(c * d), "%s L" % num(c * 2)], "%d km = %s fois 100 km : %d %s %s = <b>%s L</b>." % (d, dz(d // 10, 1), c, FOIS, dz(d // 10, 1), num(c * d // 100) if c * d % 100 == 0 else dz(c * d // 10, 1)))
    if k == "robinet":
        r, t = R.randint(6, 15), R.randint(3, 12)
        return mcq("Un robinet coule à %d L par minute. Combien de litres en %d minutes ?" % (r, t), "%d L" % (r * t), ["%d L" % (r + t), "%d L" % (r * t + r), "%d L" % (r * (t - 1))], "%d %s %d = <b>%d L</b>." % (r, FOIS, t, r * t))
    if k == "pas":
        n, d = R.randint(10, 20), R.randint(6, 9)
        return mcq("En %d pas, %s parcourt %d m. Quelle distance parcourt-%s en %d pas ?" % (n, p[0], n * d // 10 if (n * d) % 10 == 0 else n * d // 10, p[1], n * 3) if (n * d) % 10 == 0 else
                   "En 10 pas, %s parcourt %d m. Quelle distance parcourt-%s en %d pas ?" % (p[0], d, p[1], 10 * n), "%d m" % (d * n), ["%d m" % (d + 10 * n), "%d m" % (d * 10 * n), "%d m" % (d * n + d)],
                   "%d pas = %d fois 10 pas : %d %s %d = <b>%d m</b>." % (10 * n, n, d, FOIS, n, d * n)) if (n * d) % 10 else None
    e = R.choice([2, 5, 10, 100])
    c = R.randint(2, 12)
    return mcq("Sur un plan, 1 cm représente %d m. Deux maisons sont à %d cm sur le plan. Quelle est la vraie distance ?" % (e, c), "%d m" % (e * c), ["%d m" % (e + c), "%d cm" % (e * c), "%d m" % (e * (c + 1))],
               "%d cm sur le plan : %d %s %d = <b>%d m</b>." % (c, c, FOIS, e, e * c))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Reconnaître la proportionnalité", mix(R, seen, [(s1, 20)])),
        ("Compléter un tableau", mix(R, seen, [(s2, 20)])),
        ("Ajouter, multiplier, passer par l’unité", mix(R, seen, [(s3, 20)])),
        ("Recettes", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Deux grandeurs sont <b>proportionnelles</b> si, quand l’une est multipliée (ou divisée) par un nombre, l’autre l’est aussi par le même nombre.",
         "Dans un tableau de proportionnalité, on passe d’une ligne à l’autre en multipliant toujours par le <b>même nombre</b>.",
         "On peut aussi additionner des colonnes (2 places + 3 places = 5 places) ou passer par l’unité (prix d’un seul objet)."],
        [example("3 cahiers coûtent 6 €. Prix de 7 cahiers ?", ["1 cahier : 6 ÷ 3 = 2 €", "7 cahiers : 2 %s 7" % FOIS], "14 €")],
        [["Ajouter au lieu de multiplier : 4 personnes → 200 g, 6 personnes → 202 g", "6 personnes = 4 personnes %s 1,5 : 300 g." % FOIS],
         ["Croire que tout est proportionnel", "L’âge et la taille ne sont pas proportionnels : à 20 ans, on ne mesure pas deux fois plus qu’à 10 ans."],
         ["Oublier l’unité", "Écris toujours l’unité dans la réponse (€, g, L, m)."]])
    faq = [("Comment vérifier qu’un tableau est proportionnel ?", "On cherche le nombre qui multiplie la première ligne : il doit être le même dans toutes les colonnes."),
           ("Qu’est-ce que « passer par l’unité » ?", "Calculer d’abord la valeur pour 1 objet (1 kg, 1 cahier…), puis multiplier.")]
    unit(lv, R, "proportionnalite", "P",
         "Identifier une situation de proportionnalité ; savoir résoudre un problème de proportionnalité (propriétés de linéarité, coefficient, passage par l’unité)",
         "La proportionnalité", "Proportionnalité",
         "Fiches de maths %s sur la proportionnalité : reconnaître une situation, compléter un tableau, passage par l’unité, recettes et problèmes. 100 exercices corrigés." % GN(lv),
         "Proportionnel : on multiplie toujours par le même nombre.", "On peut additionner des colonnes ou passer par l’unité.",
         body, faq, sets, 15)


if __name__ == "__main__":
    build(1)
