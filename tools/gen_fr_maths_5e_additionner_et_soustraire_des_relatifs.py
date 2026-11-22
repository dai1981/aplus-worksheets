# -*- coding: utf-8 -*-
"""
France Maths 5e : Additionner et soustraire des nombres relatifs
  python3 tools/gen_fr_maths_5e_additionner_et_soustraire_des_relatifs.py
Erreurs : (−3) + (−5) = 8 ou −2, oublier que soustraire, c’est ajouter l’opposé ((−3) − (−5) = −8), mauvais signe pour la somme de signes contraires.
"""
import random
from fr_c4 import *

R = random.Random(60202)
K = Kids(R)


def rv(dec=False):
    if dec:
        x = Fr(R.randint(-99, 99), 10)
    else:
        x = Fr(R.randint(-20, 20))
    return x if x else Fr(3)


def s1():
    a, b = rv(), rv()
    if a > 0 and b > 0:
        a = -a
    r = a + b
    return M("%s + %s = …" % (par(a), par(b)), d(r), [d(-r) if r else "1", d(abs(a) + abs(b)) if abs(a) + abs(b) != r else d(r + 1), d(a - b)],
             ("Même signe : on ajoute les distances à zéro et on garde le signe : <b>%s</b>." if (a > 0) == (b > 0) else
              "Signes contraires : on soustrait les distances à zéro et on prend le signe du nombre le plus éloigné de zéro : <b>%s</b>.") % d(r))


def s2():
    a, b = rv(), rv()
    r = a - b
    return M("%s − %s = …" % (par(a), par(b)), d(r), [d(a + b), d(-r) if r else "1", d(abs(a) - abs(b)) if abs(a) - abs(b) != r else d(r - 1)],
             "Soustraire un nombre, c’est ajouter son opposé : %s − %s = %s + %s = <b>%s</b>." % (par(a), par(b), par(a), par(-b), d(r)))


def s3():
    xs = [rv(R.random() < 0.4) for _ in range(R.choice([3, 4]))]
    ops = [R.choice(["+", "−"]) for _ in xs[1:]]
    r = xs[0]
    txt = par(xs[0])
    for o, x in zip(ops, xs[1:]):
        r = r + x if o == "+" else r - x
        txt += " %s %s" % (o, par(x))
    wrong = xs[0]
    for o, x in zip(ops, xs[1:]):
        wrong = wrong + x
    return M("Calcule : %s" % txt, d(r), [d(wrong) if wrong != r else d(r + 2), d(-r) if r else "2", d(r + 1)],
             "On transforme les soustractions en additions de l’opposé, puis on regroupe les positifs et les négatifs : <b>%s</b>." % d(r))


def s4():
    a = rv(R.random() < 0.3)
    b = rv(R.random() < 0.3)
    k = R.choice(["plus", "moins", "simpl"])
    if k == "plus":
        return M("Complète : %s + … = %s" % (par(a), d(a + b)), d(b), [d(-b), d(a + b - a + 1), d(2 * a + b) if 2 * a + b != b else d(b + 2)],
                 "On cherche %s − %s = <b>%s</b>." % (d(a + b), par(a), d(b)))
    if k == "moins":
        return M("Complète : %s − … = %s" % (par(a), d(a - b)), d(b), [d(-b), d(2 * a - b) if 2 * a - b != b else d(b + 1), d(b + 1)],
                 "%s − %s = %s, donc le nombre manquant est <b>%s</b>." % (par(a), par(b), d(a - b), d(b)))
    c = rv()
    r = a + b + c
    txt = "%s %s %s %s %s" % (d(a), "+" if b >= 0 else "−", d(abs(b)), "+" if c >= 0 else "−", d(abs(c)))
    return M("Calcule (écriture simplifiée) : %s" % txt, d(r), [d(a - b - c) if a - b - c != r else d(r + 2), d(-r) if r else "1", d(abs(a) + abs(b) + abs(c))],
             "Dans l’écriture simplifiée, chaque nombre garde le signe qui le précède : <b>%s</b>." % d(r))


def s5():
    p = K.next()
    k = R.choice(["temp", "ecart", "alt", "compte", "jeu"])
    if k == "temp":
        a, b = R.randint(-12, 5), R.randint(-15, 8)
        return M("La nuit, il fait %s °C. L’après-midi, il fait %s °C. De combien de degrés la température a-t-elle varié ?" % (d(a), d(b)), "%s °C" % (("+" if b - a > 0 else "") + d(b - a)),
                 ["%s °C" % d(b + a), "%s °C" % (("+" if a - b > 0 else "") + d(a - b)), "%s °C" % d(abs(b) - abs(a))],
                 "Variation = arrivée − départ = %s − %s = <b>%s °C</b>." % (d(b), par(a), d(b - a))) if a != b else None
    if k == "ecart":
        a, b = R.randint(-30, -5), R.randint(5, 40)
        return M("Quel est l’écart entre %s °C et %s °C ?" % (d(a), d(b)), "%d °C" % (b - a), ["%d °C" % (b + a) if b + a > 0 else "%d °C" % (b - a + 10), "%d °C" % b, "%d °C" % (b - a - 1)],
                 "%s − %s = %d + %d = <b>%d °C</b>." % (d(b), par(a), b, -a, b - a))
    if k == "alt":
        a, b = R.randint(500, 4800), R.randint(-400, -20)
        return M("Un sommet culmine à %s m. Le fond d’un lac voisin est à %s m. Quelle est la différence d’altitude ?" % (num(a), d(b)), "%s m" % num(a - b), ["%s m" % num(a + b), "%s m" % num(a), "%s m" % num(a - b + 100)],
                 "%s − %s = %s + %s = <b>%s m</b>." % (num(a), par(b), num(a), num(-b), num(a - b)))
    if k == "compte":
        a, b, c = R.randint(-50, 120), R.randint(30, 150), R.randint(20, 100)
        r = a - b + c
        return M("Le compte %s est à %s €. %s paie %d €, puis reçoit %d €. Quel est le nouveau solde ?" % (de_n(p[0]), d(a), p[1].capitalize(), b, c), "%s €" % d(r), ["%s €" % d(a + b - c), "%s €" % d(-r) if r else "1 €", "%s €" % d(a - b - c)],
                 "%s − %d + %d = <b>%s €</b>." % (d(a), b, c, d(r)))
    xs = [R.randint(-8, 8) for _ in range(4)]
    return M("Au jeu, %s marque successivement %s points. Quel est son score final ?" % (p[0], " ; ".join(d(x) if x <= 0 else "+" + d(x) for x in xs)), d(sum(xs)), [d(sum(abs(x) for x in xs)), d(-sum(xs)) if sum(xs) else "1", d(sum(xs) + 2)],
             "%s = <b>%s</b>." % (" + ".join(par(x) for x in xs), d(sum(xs))))


def main():
    seen = set()
    sets = [("Additionner deux relatifs", mix(R, seen, [(s1, 20)])), ("Soustraire, c’est ajouter l’opposé", mix(R, seen, [(s2, 20)])),
            ("Suites de calculs", mix(R, seen, [(s3, 20)])), ("Compléter et simplifier", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Deux nombres de <b>même signe</b> : on ajoute leurs distances à zéro et on garde le signe. (−3) + (−5) = −8.",
              "Deux nombres de <b>signes contraires</b> : on soustrait les distances à zéro et on prend le signe du plus éloigné de zéro. (−7) + 4 = −3.",
              "<b>Soustraire</b> un nombre, c’est ajouter son opposé : 2 − (−6) = 2 + 6 = 8."],
             [("(−4) − (−9)", ["= (−4) + 9"], "5")],
             [["(−3) + (−5) = 8", "Deux négatifs : le résultat est négatif, −8."],
              ["(−3) − (−5) = −8", "Soustraire −5, c’est ajouter 5 : (−3) + 5 = 2."],
              ["(−7) + 4 = −11", "Signes contraires : 7 − 4 = 3, signe de −7 : −3."]])
    faq = [("Comment savoir le signe d’une somme ?", "Si les signes sont différents, c’est le signe du nombre qui a la plus grande distance à zéro."),
           ("Que veut dire l’écriture simplifiée 5 − 8 + 2 ?", "C’est (+5) + (−8) + (+2) : chaque nombre garde le signe placé devant lui.")]
    unit("5e", R, "additionner-et-soustraire-des-relatifs", "N",
         "Additionner et soustraire des nombres relatifs ; gérer les parenthèses et simplifier l’écriture d’une somme ; résoudre des problèmes (températures, altitudes, soldes)",
         "Additionner et soustraire des relatifs", "Addition et soustraction de relatifs",
         "Fiches de maths 5e pour additionner et soustraire des nombres relatifs : règles des signes, ajouter l’opposé, suites de calculs, écriture simplifiée et problèmes. 100 exercices corrigés.",
         "Soustraire, c’est ajouter l’opposé.", "(−3) + (−5) = −8 ; (−7) + 4 = −3", body, faq, sets, 2)


if __name__ == "__main__":
    main()
