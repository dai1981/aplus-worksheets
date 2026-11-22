# -*- coding: utf-8 -*-
"""
France Maths 5e : Premières équations (x + b = c et ax = c)
  python3 tools/gen_fr_maths_5e_premieres_equations.py
La lettre comme inconnue, tester une solution, résoudre x + b = c et ax = c (méthodes arithmétiques), mettre en équation.
Erreurs : x + 7 = 12 donc x = 19, 4x = 20 donc x = 16, 4x = 20 donc x = 80.
"""
import random
from fr_c4 import *

R = random.Random(60207)
K = Kids(R)


def s1():
    x = R.randint(-5, 12)
    a, b = R.randint(2, 6), R.randint(-9, 9)
    c = a * x + b
    cand = R.choice([x, x + 1, x - 1, -x if x else 2])
    ok = cand == x
    return M("Le nombre %s est-il solution de l’équation %dx %s %d = %s ?" % (d(cand), a, "+" if b >= 0 else "−", abs(b), d(c)), "oui" if ok else "non", ["non" if ok else "oui", "on ne peut pas savoir", "seulement si x est positif"],
             "Pour x = %s : %d × %s %s %d = %s, %s %s : <b>%s</b>." % (d(cand), a, par(cand), "+" if b >= 0 else "−", abs(b), d(a * cand + b), "égal à" if ok else "différent de", d(c), "oui" if ok else "non"))


def s2():
    b, x = R.randint(-15, 20), R.randint(-10, 25)
    if b == 0:
        return None
    c = x + b
    if R.random() < 0.6:
        return M("Résous : x %s %d = %s" % ("+" if b > 0 else "−", abs(b), d(c)), "x = %s" % d(x), ["x = %s" % d(c + b), "x = %s" % d(-x) if x else "x = 1", "x = %s" % d(x + 1)],
                 "On cherche le nombre qui, %s %d, donne %s : x = %s %s %d = <b>%s</b>." % ("augmenté de" if b > 0 else "diminué de", abs(b), d(c), d(c), "−" if b > 0 else "+", abs(b), d(x)))
    return M("Résous : %d + x = %s" % (b, d(c)) if b > 0 else "Résous : x − %d = %s" % (-b, d(c)), "x = %s" % d(x), ["x = %s" % d(c + b), "x = %s" % d(b - c), "x = %s" % d(x - 1)],
             "x = %s %s %d = <b>%s</b>." % (d(c), "−" if b > 0 else "+", abs(b), d(x)))


def s3():
    a = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
    x = R.choice([R.randint(2, 15), Fr(R.randint(1, 9), 2) if a % 2 == 0 else R.randint(2, 15)])
    x = Fr(x)
    c = a * x
    if c.denominator != 1:
        return None
    return M("Résous : %dx = %s" % (a, d(c)), "x = %s" % d(x), ["x = %s" % d(c - a), "x = %s" % d(c * a), "x = %s" % d(x + 1)],
             "On cherche le nombre qui, multiplié par %d, donne %s : x = %s ÷ %d = <b>%s</b>." % (a, d(c), d(c), a, d(x)))


def s4():
    p = K.next()
    k = R.choice(["somme", "prix", "age", "perim"])
    if k == "somme":
        b, x = R.randint(5, 40), R.randint(5, 60)
        return M("%s pense à un nombre. Il ajoute %d et trouve %d. Quelle équation traduit la situation ?" % (p[0], b, x + b) if p[1] == "il" else
                 "%s pense à un nombre. Elle ajoute %d et trouve %d. Quelle équation traduit la situation ?" % (p[0], b, x + b), "x + %d = %d" % (b, x + b), ["%dx = %d" % (b, x + b), "x = %d + %d" % (x + b, b), "x − %d = %d" % (b, x + b)],
                 "Le nombre inconnu est x ; « ajoute %d » donne x + %d : <b>x + %d = %d</b>, donc x = %d." % (b, b, b, x + b, x))
    if k == "prix":
        n, u = R.randint(3, 9), R.randint(2, 15)
        return M("%d places de cinéma coûtent %d €. On note x le prix d’une place. Quelle équation traduit la situation ?" % (n, n * u), "%dx = %d" % (n, n * u), ["x + %d = %d" % (n, n * u), "x = %d × %d" % (n, n * u), "%d + x = %d" % (n * u, n)],
                 "<b>%dx = %d</b>, donc x = %d ÷ %d = %d €." % (n, n * u, n * u, n, u))
    if k == "age":
        a, dd = R.randint(8, 14), R.randint(20, 35)
        return M("La mère %s a %d ans de plus %s ; elle a %d ans. On note x l’âge %s. Quelle équation convient ?" % (de_n(p[0]), dd, "que lui" if p[1] == "il" else "qu’elle", a + dd, de_n(p[0])), "x + %d = %d" % (dd, a + dd), ["x − %d = %d" % (dd, a + dd), "%dx = %d" % (dd, a + dd), "x = %d + %d" % (a + dd, dd)],
                 "<b>x + %d = %d</b>, donc x = %d ans." % (dd, a + dd, a))
    c = R.randint(3, 25)
    return M("Le périmètre d’un carré est %d cm. On note c son côté. Quelle équation traduit la situation ?" % (4 * c), "4c = %d" % (4 * c), ["c + 4 = %d" % (4 * c), "c² = %d" % (4 * c), "c = 4 × %d" % (4 * c)],
             "<b>4c = %d</b>, donc c = %d cm." % (4 * c, c))


def s5():
    p = K.next()
    k = R.choice(["billes", "achat", "partage", "train"])
    if k == "billes":
        b, x = R.randint(5, 30), R.randint(10, 80)
        return M("%s gagne %d billes et en a maintenant %d. Combien en avait-%s au départ ?" % (p[0], b, x + b, p[1]), str(x), [str(x + 2 * b), str(b), str(x + 1)],
                 "x + %d = %d, donc x = %d − %d = <b>%d</b>." % (b, x + b, x + b, b, x))
    if k == "achat":
        n, u = R.randint(3, 8), Fr(R.randint(15, 90), 10)
        t = n * u
        return M("%s achète %d stylos identiques pour %s €. Combien coûte un stylo ?" % (p[0], n, em(t)), euro(u), [euro(t - n), euro(t * n), euro(u + 1)],
                 "%dx = %s, donc x = %s ÷ %d = <b>%s</b>." % (n, em(t), em(t), n, euro(u)))
    if k == "partage":
        n, x = R.randint(3, 8), R.randint(4, 25)
        return M("On partage équitablement %d bonbons entre %d enfants. Combien chaque enfant reçoit-il ?" % (n * x, n), str(x), [str(n * x - n), str(n * x * n), str(x + 1)],
                 "%dx = %d, donc x = <b>%d</b>." % (n, n * x, x))
    v, t = R.choice([60, 80, 90, 100, 120]), R.randint(2, 5)
    return M("Un train roule à %d km/h. Combien de temps lui faut-il pour parcourir %d km ?" % (v, v * t), "%d h" % t, ["%d h" % (v * t - v), "%d h" % (v * t * v // 100), "%d h" % (t + 1)],
             "%d × t = %d, donc t = %d ÷ %d = <b>%d h</b>." % (v, v * t, v * t, v, t))


def main():
    seen = set()
    sets = [("Tester une solution", mix(R, seen, [(s1, 20)])), ("Résoudre x + b = c", mix(R, seen, [(s2, 20)])),
            ("Résoudre ax = c", mix(R, seen, [(s3, 20)])), ("Mettre en équation", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans une <b>équation</b>, la lettre est un nombre inconnu. Une <b>solution</b> est un nombre qui rend l’égalité vraie.",
              "x + 7 = 12 : quel nombre plus 7 fait 12 ? x = 12 − 7 = 5.",
              "4x = 20 : quel nombre multiplié par 4 fait 20 ? x = 20 ÷ 4 = 5. On vérifie en remplaçant x."],
             [("3x = 27", ["27 ÷ 3"], "x = 9")],
             [["x + 7 = 12 donc x = 19", "On fait l’opération inverse : 12 − 7 = 5."],
              ["4x = 20 donc x = 16", "4x veut dire 4 × x : on divise, x = 5."],
              ["Oublier de vérifier", "On remplace x par la solution : 4 × 5 = 20, c’est juste."]])
    faq = [("Comment vérifier une solution ?", "On remplace la lettre par le nombre trouvé et on regarde si les deux membres sont égaux."),
           ("Pourquoi mettre un problème en équation ?", "Pour traduire la situation par une égalité qu’on sait résoudre.")]
    unit("5e", R, "premieres-equations", "A",
         "Donner à la lettre le statut d’inconnue ; tester si un nombre est solution ; modéliser un problème et résoudre des équations du type ax = c et x + b = c par des méthodes arithmétiques",
         "Premières équations", "Premières équations",
         "Fiches de maths 5e sur les premières équations : tester une solution, résoudre x + b = c et ax = c, mettre en équation et problèmes. 100 exercices corrigés.",
         "x + 7 = 12 → x = 12 − 7", "4x = 20 → x = 20 ÷ 4", body, faq, sets, 7)


if __name__ == "__main__":
    main()
