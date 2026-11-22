# -*- coding: utf-8 -*-
"""
France Maths 5e : Les nombres relatifs（programme 2026 du cycle 4）
  python3 tools/gen_fr_maths_5e_nombres_relatifs.py
Positif, négatif, opposé, distance à zéro ; droite graduée ; comparer et ranger des relatifs ; situations (températures, altitudes).
Erreurs : −7 &gt; −3 car 7 &gt; 3, oublier que l’opposé de −4 est 4, lire la droite graduée dans le mauvais sens.
"""
import random
from fr_c4 import *

R = random.Random(60201)
K = Kids(R)


def s1():
    k = R.choice(["opp", "opp", "dist", "signe", "voc"])
    a = Fr(R.choice([R.randint(-20, 20), Fr(R.randint(-99, 99), 10)]))
    if a == 0:
        return None
    if k == "opp":
        return M("Quel est l’opposé de %s ?" % d(a), d(-a), [d(a), d(1 / a) if abs(a) != 1 and (1 / a).denominator in (1, 2, 4, 5, 10) else d(a + 1), "0"],
                 "L’opposé d’un nombre a la même distance à zéro, mais le signe contraire : <b>%s</b>." % d(-a))
    if k == "dist":
        return M("Quelle est la distance à zéro de %s ?" % d(a), d(abs(a)), [d(-abs(a)), d(abs(a) + 1), "0"],
                 "La distance à zéro est le nombre sans son signe : <b>%s</b>." % d(abs(a)))
    if k == "signe":
        xs = R.sample([Fr(x) for x in range(-15, 16) if x != 0], 4)
        neg = [x for x in xs if x < 0]
        if not neg or len(neg) == 4:
            return None
        good = d(min(neg)) if False else ", ".join(d(x) for x in neg)
        return M("Parmi %s, quels sont les nombres négatifs ?" % ", ".join(d(x) for x in xs), good, [", ".join(d(x) for x in xs if x > 0), ", ".join(d(x) for x in xs), d(min(xs))],
                 "Les nombres négatifs s’écrivent avec le signe − : <b>%s</b>." % good)
    V = [("Le nombre 0 est-il positif ou négatif ?", "les deux à la fois", ["seulement positif", "seulement négatif", "ni l’un ni l’autre n’existe"]),
         ("Un nombre et son opposé ont…", "la même distance à zéro", ["le même signe", "une somme égale à 1", "un produit égal à 1"]),
         ("Quelle est la somme d’un nombre et de son opposé ?", "0", ["1", "le double du nombre", "−1"]),
         ("Quel est le plus petit des nombres positifs ?", "0", ["1", "−1", "il n’existe pas"])]
    q, an, w = R.choice(V)
    return M(q, an, w, "Réponse : <b>%s</b>." % an)


def s2():
    step = R.choice([1, 1, 2, 5])
    lo = R.choice([-10, -8, -6, -5, -4]) * step
    hi = lo + 10 * step
    v = lo + step * R.randint(1, 9)
    if v == 0:
        return None
    svg = droite(lo, hi, step, marks=[(v, "A")], labels=[lo, 0, hi] if lo < 0 < hi else [lo, hi], every=step * 5)
    return M("<div class='qfig'>%s</div>Quelle est l’abscisse du point A ?" % svg, d(v), [d(-v), d(v + step), d(v - step)],
             "Chaque graduation vaut %d. A est à %s %s de 0 : <b>%s</b>." % (step, pl(abs(v) // step, "graduation"), "à gauche" if v < 0 else "à droite", d(v)))


def s3():
    a, b = R.sample([Fr(x, 10) for x in range(-99, 100) if x != 0], 2)
    if R.random() < 0.5:
        a, b = -abs(a), -abs(b)
    if a == b:
        return None
    if R.random() < 0.6:
        good = "%s &lt; %s" % (d(min(a, b)), d(max(a, b)))
        return M("Quelle écriture est vraie ?", good, ["%s &lt; %s" % (d(max(a, b)), d(min(a, b))), "%s = %s" % (d(a), d(b)), "%s &gt; %s" % (d(min(a, b)), d(max(a, b)))],
                 "Sur la droite graduée, le plus petit est le plus à gauche : <b>%s</b>." % good)
    xs = sorted(R.sample(range(-20, 0), R.choice([2, 3])) + R.sample(range(1, 21), 2))[:4]
    sh = list(xs)
    R.shuffle(sh)
    f = lambda l: " &lt; ".join(d(x) for x in l)
    by_abs = sorted(xs, key=abs)
    neg = [x for x in xs if x < 0]
    pos = [x for x in xs if x > 0]
    cand = []
    for c in (by_abs, neg[::-1] + pos, xs[::-1], [xs[1], xs[0]] + xs[2:]):
        if c != xs and f(c) not in cand:
            cand.append(f(c))
    return M("Range dans l’ordre croissant : %s" % " ; ".join(d(x) for x in sh), f(xs), cand[:3],
             "Les négatifs d’abord, du plus loin de zéro au plus proche : <b>%s</b>." % f(xs))


def s4():
    k = R.choice(["temp", "temp", "alt"])
    if k == "temp":
        a, b = R.sample(range(-15, 16), 2)
        p = K.next()
        lieux = R.sample(["Lille", "Strasbourg", "Brest", "Grenoble", "Moscou", "Oslo", "Québec"], 2)
        col = lieux[0] if a < b else lieux[1]
        return M("Ce matin, il fait %s °C à %s et %s °C à %s. Où fait-il le plus froid ?" % (d(a), lieux[0], d(b), lieux[1]), "à " + col, ["à " + (lieux[1] if col == lieux[0] else lieux[0]), "il fait aussi froid", "on ne peut pas savoir"],
                 "Le plus froid est la température la plus petite : %s &lt; %s, donc <b>à %s</b>." % (d(min(a, b)), d(max(a, b)), col))
    if k == "alt":
        a = R.randint(-400, -10)
        b = Fr(R.randint(-400, -10), 10)
        lo = d(min(Fr(a, 10), b))
        return M("Un plongeur A est à %s m et un plongeur B à %s m (sous le niveau de la mer). Lequel est le plus profond ?" % (d(Fr(a, 10)), d(b)),
                 "le plongeur A" if Fr(a, 10) < b else "le plongeur B", ["le plongeur B" if Fr(a, 10) < b else "le plongeur A", "ils sont à la même profondeur", "on ne peut pas savoir"],
                 "Le plus profond a l’altitude la plus petite : %s m." % lo) if Fr(a, 10) != b else None
    a = Fr(R.randint(-60, 60), 10)
    return M("Quel nombre est compris entre −1 et %s ?" % d(a) if a > -1 else "Quel nombre est compris entre %s et −1 ?" % d(a),
             d((a - 1) / 2) if ((a - 1) / 2) * 100 % 1 == 0 else d(Fr(int((a - 1) * 5), 10)),
             [d(a - 1) if a > -1 else d(a - 1), d(abs(a) + 1), d(-a - 2) if not (min(a, -1) < -a - 2 < max(a, -1)) else d(max(a, -1) + 1)],
             "On cherche un nombre entre les deux sur la droite graduée.") if abs(a + 1) > Fr(2, 10) else None


def s5():
    k = R.choice(["ascenseur", "temp", "compte", "date"])
    if k == "ascenseur":
        a = R.randint(-3, 5)
        b = R.randint(1, 6)
        up = R.random() < 0.5
        r = a + b if up else a - b
        return M("Un ascenseur est à l’étage %s. Il %s de %s. À quel étage arrive-t-il ?" % (d(a), "monte" if up else "descend", pl(b, "étage")), d(r), [d(a - b if up else a + b), d(-r) if r else "1", d(r + 1)],
                 "%s %s %d = <b>%s</b>." % (d(a), "+" if up else "−", b, d(r)))
    if k == "temp":
        a = R.randint(-8, 6)
        b = R.randint(2, 12)
        return M("Il fait %s °C. La température baisse de %d °C. Quelle température fait-il ?" % (d(a), b), "%s °C" % d(a - b), ["%s °C" % d(a + b), "%s °C" % d(b - a), "%s °C" % d(-(a - b)) if a - b else "1 °C"],
                 "On recule de %d sur la droite graduée : %s − %d = <b>%s °C</b>." % (b, d(a), b, d(a - b)))
    if k == "compte":
        a = R.randint(10, 80)
        b = R.randint(a + 5, a + 100)
        return M("Un compte en banque a %d €. On paie %d €. Que devient le solde ?" % (a, b), "%s €" % d(a - b), ["%d €" % (b - a), "%d €" % (a + b), "%s €" % d(a - b - 10)],
                 "%d − %d = <b>%s €</b> : le compte est à découvert." % (a, b, d(a - b)))
    y = R.randint(100, 800)
    n = R.randint(20, 90)
    return M("Un philosophe grec est né en %d av. J.-C. et a vécu %d ans. En quelle année est-il mort ?" % (y, n), "en %d av. J.-C." % (y - n), ["en %d av. J.-C." % (y + n), "en %d apr. J.-C." % (n - y if n > y else y - n), "en %d av. J.-C." % (y - n + 1)],
             "Avant J.-C., les années « reculent » vers 0 : on écrit −%d, puis −%d + %d = −%d, soit <b>%d av. J.-C.</b>" % (y, y, n, y - n, y - n))


def main():
    seen = set()
    sets = [("Positif, négatif, opposé", mix(R, seen, [(s1, 20)])), ("La droite graduée", mix(R, seen, [(s2, 20)])),
            ("Comparer et ranger", mix(R, seen, [(s3, 20)])), ("Relatifs dans la vie", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Un nombre <b>négatif</b> s’écrit avec le signe − : −5. Les nombres positifs et négatifs forment les <b>nombres relatifs</b>.",
              "L’<b>opposé</b> de 5 est −5 ; l’opposé de −3,2 est 3,2. La distance à zéro de −5 est 5.",
              "Sur une droite graduée, le plus petit nombre est le plus à gauche : −7 &lt; −3 &lt; 0 &lt; 2."],
             [("Compare −7 et −3", ["−7 est plus loin de 0, à gauche", "plus à gauche = plus petit"], "−7 &lt; −3")],
             [["Croire que −7 &gt; −3 car 7 &gt; 3", "Pour les négatifs, c’est l’inverse : −7 &lt; −3."],
              ["Oublier que l’opposé de −4 est 4", "On change seulement le signe."],
              ["Lire la droite graduée de gauche à droite pour les négatifs", "À gauche de 0, on compte −1, −2, −3… en s’éloignant de 0."]])
    faq = [("Où rencontre-t-on des nombres négatifs ?", "Pour les températures sous zéro, les altitudes sous le niveau de la mer, les dettes, les étages en sous-sol."),
           ("Comment comparer deux nombres négatifs ?", "Le plus petit est celui qui a la plus grande distance à zéro.")]
    unit("5e", R, "nombres-relatifs", "N",
         "Définir les nombres relatifs, l’opposé et la distance à zéro ; placer et lire des nombres relatifs sur une droite graduée ; comparer et ranger des nombres décimaux relatifs",
         "Les nombres relatifs", "Nombres relatifs",
         "Fiches de maths 5e sur les nombres relatifs : positifs et négatifs, opposé, droite graduée, comparer, ranger et problèmes. 100 exercices corrigés.",
         "−7 &lt; −3 : le plus à gauche est le plus petit.", "L’opposé de −5 est 5.", body, faq, sets, 1)


if __name__ == "__main__":
    main()
