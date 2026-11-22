# -*- coding: utf-8 -*-
"""
France Maths 5e : Grandeurs en fonction d’une autre — tableaux, graphiques, formules
  python3 tools/gen_fr_maths_5e_fonctions_tableaux_et_graphiques.py
Erreurs : inverser les axes, lire la graduation au mauvais endroit, appliquer la formule sans respecter les priorités.
"""
import random
from fr_c4 import *
import de_k10

R = random.Random(60210)
K = Kids(R)


def s1():
    a, b = R.randint(2, 6), R.randint(1, 15)
    x = R.randint(1, 12)
    k = R.choice(["taxi", "loc", "aire"])
    if k == "taxi":
        return M("Un taxi coûte %d € de prise en charge, plus %d € par kilomètre. Quel est le prix pour %d km ?" % (b, a, x), "%d €" % (b + a * x), ["%d €" % ((b + a) * x), "%d €" % (a * x), "%d €" % (b + a + x)],
                 "Prix = %d + %d × nombre de km = %d + %d × %d = <b>%d €</b>." % (b, a, b, a, x, b + a * x))
    if k == "loc":
        return M("La location d’un vélo coûte %d € par heure, plus %d € d’assurance. Quelle formule donne le prix P en fonction du nombre d’heures h ?" % (a, b), "P = %dh + %d" % (a, b),
                 ["P = %d(h + %d)" % (a, b), "P = %dh + %d" % (b, a), "P = h + %d" % (a + b)], "Chaque heure coûte %d €, et on ajoute %d € une seule fois : <b>P = %dh + %d</b>." % (a, b, a, b))
    return M("Un rectangle a une largeur de %d cm et une longueur x (en cm). Quelle formule donne son aire A en fonction de x ?" % a, "A = %dx" % a, ["A = x + %d" % a, "A = 2(x + %d)" % a, "A = x²"],
             "Aire = longueur × largeur : <b>A = %dx</b>." % a)


def s2():
    a, b = R.choice([2, 3, 4, 5, -2, -3]), R.randint(-5, 10)
    k = R.choice(["lin", "carre"])
    xs = [-2, -1, 0, 1, 2, 3] if R.random() < 0.5 else [0, 1, 2, 3, 4, 5]
    i = R.randrange(len(xs))
    if k == "lin":
        f = lambda x: a * x + b
        form = "y = %s" % expr([(a, "x"), (b, "")])
    else:
        f = lambda x: x * x + b
        form = "y = %s" % expr([(1, "x²"), (b, "")])
    vals = [d(f(x)) if j != i else "?" for j, x in enumerate(xs)]
    tb = table(["x"] + [d(x) for x in xs], [["y"] + vals])
    x = xs[i]
    return M("%s<br>On calcule y avec la formule %s. Quel nombre remplace le « ? » ?" % (tb, form), d(f(x)), [d(f(x) + 1), d(f(-x)) if f(-x) != f(x) else d(f(x) - 2), d(a + x + b) if k == "lin" else d(2 * x + b)],
             "Pour x = %s : <b>%s</b>." % (d(x), d(f(x))))


def courbe():
    hs = list(range(0, 11))
    k = R.choice(["lin", "pente", "creux"])
    if k == "lin":
        a = R.choice([1, 2, 3])
        b = R.randint(0, 6)
        f = lambda x: a * x + b
    elif k == "pente":
        a = R.choice([Fr(1, 2), 1])
        f = lambda x: 20 - 2 * x if x <= 10 else 0
    else:
        f = lambda x: (x - 5) ** 2 / 2 + 2
    pts = [(x, f(x)) for x in hs if 0 <= f(x) <= 30]
    return f, pts


def s3():
    f, pts = courbe()
    pts = [(x, y) for x, y in pts if Fr(y).denominator == 1]
    if len(pts) < 4:
        return None
    ymax = max(y for _, y in pts)
    top = 30 if ymax > 20 else 20
    svg = relabel(de_k10.kurve([(lambda x: float(f(x)), BLUE, "")], (0, 10, 1), (0, top, 2 if top == 20 else 5), W=380, H=270), "courbe dans un repère")
    x, y = R.choice(pts)
    if R.random() < 0.6:
        return M("<div class='qfig'>%s</div>Lis sur le graphique la valeur de y pour x = %d." % (svg, x), d(y), [d(y + 1), d(x), d(y - 2) if y >= 2 else d(y + 3)],
                 "On part de %d sur l’axe horizontal, on monte jusqu’à la courbe et on lit sur l’axe vertical : <b>%s</b>." % (x, d(y)))
    xs = [xx for xx, yy in pts if yy == y]
    ans = " et ".join("x = %d" % xx for xx in xs)
    return M("<div class='qfig'>%s</div>Pour quelle(s) valeur(s) de x a-t-on y = %s ?" % (svg, d(y)), ans, ["x = %s" % d(y) if y != xs[0] else "x = %d" % (xs[0] + 1), "x = %d" % (xs[0] + 1), "x = %d" % (xs[0] - 1 if xs[0] > 0 else xs[0] + 2)],
             "On part de %s sur l’axe vertical, on va jusqu’à la courbe, on lit l’abscisse : <b>%s</b>." % (d(y), ans))


def s4():
    k = R.choice(["vocab", "axes", "fonction"])
    if k == "vocab":
        a, b = R.randint(2, 9), R.randint(1, 9)
        x = R.randint(1, 9)
        return M("On note P le prix (en €) en fonction du nombre n de croissants : P = %d × n. Que vaut P pour n = %d ?" % (a, x), str(a * x), [str(a + x), str(x), str(a * x + a)],
                 "P = %d × %d = <b>%d</b>." % (a, x, a * x))
    if k == "axes":
        return M("Dans un graphique « température en fonction de l’heure », où place-t-on l’heure ?", "sur l’axe horizontal (abscisses)", ["sur l’axe vertical (ordonnées)", "sur les deux axes", "on ne la place pas"],
                 "La grandeur qui varie librement (l’heure) est en <b>abscisses</b> ; celle qui en dépend (la température) en ordonnées.")
    a = R.randint(2, 6)
    return M("Le périmètre P d’un carré est fonction de son côté c. Quelle formule convient ?", "P = 4c", ["P = c²", "P = c + 4", "P = 2c"], "<b>P = 4c</b>.") if R.random() < 0.5 else \
        M("La masse d’une pile de %d livres identiques de m grammes chacun est…" % a, "%dm" % a, ["m + %d" % a, "m²", "%d + m + m" % a], "%d livres de m grammes : <b>%d × m = %dm</b>." % (a, a, a))


def s5():
    p = K.next()
    a1, b1 = R.randint(2, 5), R.randint(5, 20)
    a2, b2 = a1 + R.randint(1, 3), 0
    n = R.randint(2, 15)
    c1, c2 = a1 * n + b1, a2 * n
    if c1 == c2:
        return None
    best = "le tarif A" if c1 < c2 else "le tarif B"
    return M("Piscine : tarif A = %d € la séance + %d € de carte ; tarif B = %d € la séance sans carte. Pour %d séances, quel tarif est le moins cher ?" % (a1, b1, a2, n), best,
             ["le tarif B" if best == "le tarif A" else "le tarif A", "ils coûtent pareil", "on ne peut pas savoir"],
             "A : %d × %d + %d = %d € ; B : %d × %d = %d €. Le moins cher : <b>%s</b>." % (a1, n, b1, c1, a2, n, c2, best))


def main():
    seen = set()
    sets = [("Formules", mix(R, seen, [(s1, 20)])), ("Tableaux de valeurs", mix(R, seen, [(s2, 20)])),
            ("Lire un graphique", mix(R, seen, [(s3, 20)])), ("Vocabulaire et formules", mix(R, seen, [(s4, 20)])), ("Comparer des tarifs", mix(R, seen, [(s5, 20)]))]
    body = L(["Quand une grandeur dépend d’une autre, on dit qu’elle est fonction de cette autre : le prix est fonction du nombre de séances.",
              "On peut décrire cette dépendance par une <b>formule</b> (P = 3n + 10), un <b>tableau de valeurs</b> ou un <b>graphique</b>.",
              "Sur le graphique, la grandeur de départ est en abscisses (horizontal), celle qui en dépend en ordonnées (vertical)."],
             [("P = 3n + 10 pour n = 4", ["3 × 4 = 12", "12 + 10"], "22")],
             [["Inverser les axes", "On lit x sur l’axe horizontal, y sur l’axe vertical."],
              ["Lire la graduation trop vite", "On vérifie la valeur d’un carreau avant de lire."],
              ["Calculer 3n + 10 comme 3(n + 10)", "La multiplication d’abord : 3 × n, puis + 10."]])
    faq = [("Que veut dire « en fonction de » ?", "Qu’une grandeur dépend d’une autre : à chaque valeur de la première correspond une valeur de la seconde."),
           ("Comment comparer deux tarifs ?", "On calcule le prix avec chaque formule pour le même nombre, ou on compare les deux graphiques.")]
    unit("5e", R, "fonctions-tableaux-et-graphiques", "F",
         "Employer l’expression « en fonction de » ; produire et compléter un tableau de valeurs ; lire un graphique ; établir une formule simple ; comparer des situations",
         "Fonctions : tableaux, graphiques et formules", "Tableaux, graphiques et formules",
         "Fiches de maths 5e sur les grandeurs en fonction d’une autre : formules, tableaux de valeurs, lecture de graphiques et comparaison de tarifs. 100 exercices corrigés.",
         "Formule, tableau, graphique : trois façons de décrire une dépendance.", "Abscisses : horizontal ; ordonnées : vertical.", body, faq, sets, 10)


if __name__ == "__main__":
    main()
