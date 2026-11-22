# -*- coding: utf-8 -*-
"""
France Maths 5e : Proportionnalité (coefficient, tableaux, graphiques, vitesse moyenne, échelle)
  python3 tools/gen_fr_maths_5e_proportionnalite.py
Erreurs : utiliser une différence au lieu d’un rapport, croire que tout graphique en ligne droite est de proportionnalité (il faut passer par l’origine),
vitesse moyenne = distance + temps.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60208)
K = Kids(R)


def s1():
    k = Fr(R.choice([2, 3, 4, 5, Fr(3, 2), Fr(5, 2), Fr(12, 10), Fr(4, 10)]))
    xs = sorted(R.sample(range(2, 15), 3))
    ys = [k * x for x in xs]
    prop = R.random() < 0.5
    if not prop:
        i = R.randrange(3)
        ys[i] += R.choice([1, 2]) if ys[i] < 3 else R.choice([1, -1, 2])
    tb = table(["x"] + [str(x) for x in xs], [["y"] + [d(y) for y in ys]])
    df = ys[1] - ys[0] if ys[1] - ys[0] > 0 and ys[1] - ys[0] != k else k * 2
    if prop:
        return M("%s<br>Est-ce un tableau de proportionnalité ? Si oui, quel est le coefficient ?" % tb, "oui, coefficient %s" % d(k), ["non", "oui, coefficient %s" % d(df), "oui, coefficient %s" % d(1 / k) if (1 / k).denominator in (1, 2, 4, 5, 10) else "oui, coefficient %s" % d(k + 1)],
                 "%s : on multiplie toujours par <b>%s</b>." % (" ; ".join("%s ÷ %d = %s" % (d(y), x, d(Fr(y) / x)) for x, y in zip(xs, ys)), d(k)))
    return M("%s<br>Est-ce un tableau de proportionnalité ? Si oui, quel est le coefficient ?" % tb, "non", ["oui, coefficient %s" % d(k), "oui, coefficient %s" % d(df), "oui, coefficient 1"],
             "Les quotients y ÷ x ne sont pas tous égaux : <b>non</b>.")


def s2():
    p = K.next()
    k = R.choice(["unit", "vit", "ech"])
    if k == "unit":
        n, u = R.randint(3, 12), Fr(R.randint(15, 120), 10)
        return M("%d kg de pommes coûtent %s €. Quel est le prix d’un kilogramme ?" % (n, em(n * u)), euro(u), [euro(n * u - n), euro(n * u * n), euro(u + 1)],
                 "Coefficient de proportionnalité = prix unitaire : %s ÷ %d = <b>%s</b>." % (em(n * u), n, euro(u)))
    if k == "vit":
        t, v = R.randint(2, 5), R.choice([45, 60, 75, 80, 90, 110])
        return M("Une voiture parcourt %d km en %d h. Quelle est sa vitesse moyenne ?" % (v * t, t), "%d km/h" % v, ["%d km/h" % (v * t + t), "%d km/h" % (v * t - t), "%d km/h" % (v * t * t)],
                 "Vitesse moyenne = distance ÷ durée = %d ÷ %d = <b>%d km/h</b>." % (v * t, t, v))
    c, r = R.randint(2, 12), R.choice([100, 200, 500, 1000, 50000])
    return M("Sur une carte, %d cm représentent %s. Quelle est l’échelle ?" % (c, ("%s m" % num(c * r // 100)) if c * r < 100000 else ("%s km" % d(Fr(c * r, 100000)))), "1/%s" % num(r),
             ["1/%s" % num(r * c), "1/%s" % num(r // 10) if r > 10 else "1/2", "%d/%s" % (c, num(r))],
             "%d cm sur la carte = %s cm en réalité : 1 cm représente %s cm. Échelle <b>1/%s</b>." % (c, num(c * r), num(r), num(r)))


def s3():
    k = Fr(R.choice([3, 4, 5, 6, Fr(3, 2), Fr(5, 2), 8, 12]))
    a, b = R.sample(range(2, 16), 2)
    t = R.choice(["mult", "add", "coef", "q4"])
    if t == "q4":
        ya = k * a
        if ya.denominator != 1 or (k * b).denominator != 1:
            return None
        return M("Quatrième proportionnelle : si %d correspond à %s, à quoi correspond %d ?" % (a, d(ya), b), d(k * b), [d(ya + b - a), d(ya * b), d(k * b + k)],
                 "%s ÷ %d × %d = <b>%s</b> (produit en croix : %s × %d ÷ %d)." % (d(ya), a, b, d(k * b), d(ya), b, a))
    tb = table(["Masse (kg)", str(a), str(b), str(a + b)], [["Prix (€)", d(k * a), d(k * b), "?"]]) if t == "add" else table(["Masse (kg)", str(a), str(3 * a)], [["Prix (€)", d(k * a), "?"]])
    if t in ("add",):
        return M("%s<br>Quel nombre remplace le « ? » ?" % tb, d(k * (a + b)), [d(k * a * b), d(k * (a + b) + 1), d(a + b + k)],
                 "Prix pour %d kg = prix pour %d kg + prix pour %d kg : <b>%s</b>." % (a + b, a, b, d(k * (a + b))))
    return M("%s<br>Quel nombre remplace le « ? » ?" % tb, d(3 * k * a), [d(k * a + 2 * a), d(k * a + 3), d(3 * k * a + k)],
             "La masse est multipliée par 3, donc le prix aussi : <b>%s</b>." % d(3 * k * a))


def s4():
    prop = R.random() < 0.5
    k = Fr(R.choice([1, 2, Fr(1, 2), Fr(3, 2)]))
    xs = sorted(R.sample(range(1, 8), 4))
    b = 0 if prop else R.choice([1, 2])
    lin = R.random() < 0.6 or prop
    pts = []
    for x in xs:
        y = k * x + b if lin else Fr(x * x, 4) + 1
        if y > 9:
            return None
        pts.append((x, y, ""))
    svg = relabel(de_k8.kosy(pts=pts, lo=0, hi=10, u=22), "points dans un repère")
    if prop:
        ans = "oui : les points sont alignés avec l’origine"
    elif lin:
        ans = "non : les points sont alignés, mais pas avec l’origine"
    else:
        ans = "non : les points ne sont pas alignés"
    opts = ["oui : les points sont alignés avec l’origine", "non : les points sont alignés, mais pas avec l’origine", "non : les points ne sont pas alignés", "oui : les points montent"]
    return M("<div class='qfig'>%s</div>Ces points représentent-ils une situation de proportionnalité ?" % svg, ans, [o for o in opts if o != ans],
             "Une situation est de proportionnalité si les points sont alignés avec l’origine du repère : <b>%s</b>." % ans)


def s5():
    p = K.next()
    k = R.choice(["vit", "temps", "recette", "carbu"])
    if k == "vit":
        v = R.choice([4, 5, 6, 15, 18, 20])
        t = R.choice([Fr(1, 2), Fr(3, 2), 2, 3, Fr(5, 2)])
        return M("%s marche à %d km/h de moyenne. Quelle distance parcourt-%s en %s ?" % (p[0], v, p[1], dur(int(t * 60))), "%s km" % d(v * t), ["%s km" % d(v + t), "%s km" % d(v * int(t)) if t.denominator > 1 else "%s km" % d(v * t + v), "%s km" % d(Fr(v, 1) / t)],
                 "Distance = vitesse × durée = %d × %s = <b>%s km</b>." % (v, d(t), d(v * t)))
    if k == "temps":
        v = R.choice([60, 80, 90, 120])
        dd = v * R.choice([Fr(1, 2), Fr(3, 2), Fr(1, 4), 2, Fr(5, 2)])
        t = dd / v
        return M("Un train roule à %d km/h de moyenne. Combien de temps met-il pour parcourir %s km ?" % (v, d(dd)), dur(int(t * 60)), ["%s h" % d(t * 100) if False else dur(int(t * 100)), dur(int(t * 60) + 30), dur(int(v * 60 // dd)) if dd else dur(60)],
                 "Durée = distance ÷ vitesse = %s ÷ %d = %s h = <b>%s</b>." % (d(dd), v, d(t), dur(int(t * 60))))
    if k == "recette":
        a, b, g = R.choice([(4, 6, 300), (6, 9, 450), (4, 10, 200), (8, 12, 600), (3, 5, 150)])
        return M("Pour %d personnes, il faut %d g de pâtes. Combien en faut-il pour %d personnes ?" % (a, g, b), "%s g" % d(Fr(g * b, a)), ["%s g" % d(g + b - a), "%s g" % d(g * b), "%s g" % d(Fr(g, a))],
                 "%d ÷ %d × %d = <b>%s g</b>." % (g, a, b, d(Fr(g * b, a))))
    c = R.choice([5, 6, 7, 8])
    dd = R.choice([150, 250, 350, 400])
    return M("Une voiture consomme %d L pour 100 km. Combien consomme-t-elle pour %d km ?" % (c, dd), "%s L" % d(Fr(c * dd, 100)), ["%s L" % d(c + dd - 100), "%s L" % d(c * dd), "%s L" % d(Fr(dd, c))],
             "%d × %d ÷ 100 = <b>%s L</b>." % (c, dd, d(Fr(c * dd, 100))))


def main():
    seen = set()
    sets = [("Reconnaître et trouver le coefficient", mix(R, seen, [(s1, 20)])), ("Prix unitaire, vitesse, échelle", mix(R, seen, [(s2, 20)])),
            ("Compléter un tableau", mix(R, seen, [(s3, 20)])), ("Représentation graphique", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Deux grandeurs sont proportionnelles si on passe de l’une à l’autre en multipliant par un même nombre : le <b>coefficient de proportionnalité</b>.",
              "Exemples de coefficients : le prix unitaire, la vitesse moyenne (distance = vitesse × durée), l’échelle d’un plan.",
              "Graphiquement, une situation de proportionnalité est représentée par des points <b>alignés avec l’origine</b>."],
             [("4 kg coûtent 10 € ; 6 kg ?", ["coefficient 10 ÷ 4 = 2,5", "6 × 2,5"], "15 €")],
             [["Ajouter la même différence au lieu de multiplier", "On compare les quotients y ÷ x, pas les différences."],
              ["Croire que des points alignés suffisent", "Il faut aussi que la droite passe par l’origine."],
              ["Confondre vitesse et distance", "Vitesse = distance ÷ durée ; distance = vitesse × durée."]])
    faq = [("Comment calculer une quatrième proportionnelle ?", "Avec le coefficient, le passage à l’unité ou le produit en croix : si a correspond à b, alors c correspond à b × c ÷ a."),
           ("Que signifie 60 km/h ?", "En 1 heure, on parcourt 60 km (à vitesse constante).")]
    unit("5e", R, "proportionnalite", "F",
         "Reconnaître une situation de proportionnalité ; utiliser un coefficient de proportionnalité (prix unitaire, vitesse moyenne, échelle) ; représenter la proportionnalité par un tableau ou un graphique ; caractériser graphiquement la proportionnalité",
         "La proportionnalité", "Proportionnalité",
         "Fiches de maths 5e sur la proportionnalité : coefficient, prix unitaire, vitesse moyenne, échelle, tableaux, graphiques et problèmes. 100 exercices corrigés.",
         "y = k × x : k est le coefficient.", "Points alignés avec l’origine = proportionnalité.", body, faq, sets, 8)


if __name__ == "__main__":
    main()
