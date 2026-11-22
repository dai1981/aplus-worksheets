# -*- coding: utf-8 -*-
"""
France Maths 6e : La division (euclidienne et décimale)
  python3 tools/gen_fr_maths_6e_division.py
Division euclidienne (quotient et reste), ÷ 10, 100, 1 000, division décimale, division d’un décimal par un nombre à deux chiffres,
problèmes de partage et de groupement.
Erreurs : reste plus grand que le diviseur, oublier le 0 au quotient (612 ÷ 6 = 12), mal placer la virgule.
"""
import random
from fr_c4 import *

R = random.Random(60105)
K = Kids(R)


def s1():
    b = R.randint(3, 25)
    q = R.randint(5, 120)
    r = R.randint(1, b - 1)
    a = b * q + r
    k = R.choice(["q", "r", "egal"])
    if k == "q":
        return M("Dans la division euclidienne de %s par %d, quel est le quotient ?" % (num(a), b), num(q), [num(q + 1), num(r), num(q - 1)],
                 "%s = %d %s %s + %d (et %d &lt; %d) : le quotient est <b>%s</b>." % (num(a), b, FOIS, num(q), r, r, b, num(q)))
    if k == "r":
        return M("Dans la division euclidienne de %s par %d, quel est le reste ?" % (num(a), b), str(r), [str(r + b), str(q), str(b - r) if b - r != r else str(r + 1)],
                 "%d %s %s = %s ; %s − %s = <b>%d</b>, et %d &lt; %d." % (b, FOIS, num(q), num(b * q), num(a), num(b * q), r, r, b))
    good = "%s = %d %s %s + %d" % (num(a), b, FOIS, num(q), r)
    bad1 = "%s = %d %s %s + %d" % (num(a), b, FOIS, num(q - 1), r + b)
    return M("Quelle égalité traduit la division euclidienne de %s par %d ?" % (num(a), b), good, [bad1, "%s = %d %s %s − %d" % (num(a), b, FOIS, num(q + 1), b - r), "%s = %d %s %s + %d" % (num(a), r, FOIS, num(q), b)],
             "Dans la division euclidienne, le reste doit être plus petit que le diviseur : <b>%s</b>." % good)


def s2():
    a = Fr(R.randint(1, 99999), 10 ** R.choice([0, 1, 2]))
    m = R.choice([10, 100, 1000])
    r = a / m
    return M("%s %s %s = …" % (d(a), DIV, num(m)), d(r), [d(r * 10), d(r / 10), d(a * m)],
             "Diviser par %s : chaque chiffre devient %s fois plus petit, la virgule se déplace de %d rang%s vers la gauche. <b>%s</b>." % (num(m), num(m), len(str(m)) - 1, "s" if m > 10 else "", d(r)))


def s3():
    b = R.choice([2, 4, 5, 8, 20, 25])
    a = R.randint(11, 300)
    if a % b == 0:
        return None
    r = Fr(a, b)
    try:
        d(r)
    except ValueError:
        return None
    q = a // b
    return M("%s %s %d = …  (division décimale)" % (num(a), DIV, b), d(r), [d(q) + "," + str(a % b) if True else "", d(r * 10), d(q + 1)],
             "On continue la division après la virgule (on ajoute des zéros) : %s = %d %s %s, donc <b>%s</b>." % (num(a), b, FOIS, d(r), d(r)))


def s4():
    b = R.randint(11, 35)
    q = Fr(R.randint(11, 999), 100)
    a = b * q
    if a.denominator > 100 or q.denominator == 1:
        return None
    return M("%s %s %d = …" % (d(a), DIV, b), d(q), [d(q * 10), d(q / 10), d(q + Fr(1, 10))],
             "Ordre de grandeur : %s %s %d ≈ %s. On divise comme pour des entiers et on place la virgule du quotient au moment où l’on abaisse le premier chiffre après la virgule : <b>%s</b>. Vérification : %d %s %s = %s." % (d(a), DIV, b, d(round(a / b)), d(q), b, FOIS, d(q), d(a)))


def s5():
    p = K.next()
    k = R.choice(["bus", "partage", "boites", "prix", "ruban"])
    if k == "bus":
        c = R.choice([45, 50, 55, 60])
        n = R.randint(2, 6) * c + R.randint(1, c - 1)
        return M("%s élèves partent en sortie. Un car a %d places. Combien de cars faut-il au minimum ?" % (num(n), c), str(n // c + 1), [str(n // c), str(n % c), str(n // c + 2)],
                 "%s = %d %s %d + %d : il faut un car de plus pour les %d derniers élèves, donc <b>%d cars</b>." % (num(n), c, FOIS, n // c, n % c, n % c, n // c + 1))
    if k == "partage":
        n = R.randint(3, 8)
        t = Fr(R.randint(1000, 9000), 100) * n
        t = Fr(int(t), 1)
        if (t / n).denominator > 100:
            return None
        return M("%d amis se partagent équitablement une addition de %s €. Combien paie chacun ?" % (n, d(t)), euro(t / n), [euro(t / n + 1), euro(t * n), euro(Fr(int(t / n)))],
                 "%s %s %d = <b>%s €</b>." % (d(t), DIV, n, em(t / n)))
    if k == "boites":
        b = R.choice([6, 8, 12])
        n = R.randint(40, 300)
        if n % b == 0:
            return None
        return M("On range %d œufs dans des boîtes de %d. Combien de boîtes complètes obtient-on ?" % (n, b), str(n // b), [str(n // b + 1), str(n % b), str(n - b)],
                 "%d = %d %s %d + %d : <b>%d</b> boîtes complètes (et %d œufs restent)." % (n, b, FOIS, n // b, n % b, n // b, n % b))
    if k == "prix":
        n = R.randint(3, 12)
        u = Fr(R.randint(50, 500), 100)
        return M("%d bouteilles de jus coûtent %s €. Combien coûte une bouteille ?" % (n, em(u * n)), euro(u), [euro(u * 10), euro(u * n * n), euro(u + 1)],
                 "%s %s %d = <b>%s €</b>." % (em(u * n), DIV, n, em(u)))
    n = R.choice([4, 5, 8])
    l = Fr(R.randint(10, 60), 10) * n
    return M("%s coupe un ruban de %s m en %d morceaux de même longueur. Quelle est la longueur d’un morceau ?" % (p[0], d(l), n), "%s m" % d(l / n), ["%s m" % d(l * n), "%s m" % d(l / n * 10), "%s m" % d(l - n)],
             "%s %s %d = <b>%s m</b>." % (d(l), DIV, n, d(l / n)))


def main():
    seen = set()
    sets = [("Division euclidienne", mix(R, seen, [(s1, 20)])), ("÷ 10, ÷ 100, ÷ 1 000", mix(R, seen, [(s2, 20)])),
            ("Quotient décimal", mix(R, seen, [(s3, 20)])), ("Diviser par un nombre à deux chiffres", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Division euclidienne : a = b × q + r avec r &lt; b (q est le quotient, r le reste).",
              "Pour un quotient décimal, on continue la division après la virgule en ajoutant des zéros.",
              "÷ 10, ÷ 100 : chaque chiffre devient 10, 100 fois plus petit."],
             [("17 ÷ 4", ["17 = 4 × 4 + 1", "on continue : 10 ÷ 4, 20 ÷ 4"], "4,25")],
             [["Un reste plus grand que le diviseur", "Si le reste est trop grand, le quotient peut encore augmenter."],
              ["Oublier un 0 au quotient : 612 ÷ 6 = 12", "6 ÷ 6 = 1, puis 1 ÷ 6 = 0 (on écrit 0), puis 12 ÷ 6 = 2 : 102."],
              ["Mal placer la virgule", "On vérifie avec un ordre de grandeur."]])
    faq = [("Que faire du reste dans un problème ?", "Ça dépend de la question : pour les cars, il faut un car de plus ; pour les boîtes complètes, on ne compte pas le reste."),
           ("Comment vérifier une division ?", "On multiplie le quotient par le diviseur et on ajoute le reste.")]
    unit("6e", R, "division", "N",
         "Effectuer la division euclidienne ; diviser par 10, 100, 1 000 ; calculer un quotient décimal ; diviser un nombre décimal par un nombre entier à deux chiffres ; résoudre des problèmes de partage et de groupement",
         "La division euclidienne et décimale", "Division",
         "Fiches de maths 6e sur la division : division euclidienne, ÷ 10, quotient décimal, diviser par un nombre à deux chiffres et problèmes. 100 exercices corrigés.",
         "a = b × q + r avec r &lt; b", "17 ÷ 4 = 4,25", body, faq, sets, 5)


if __name__ == "__main__":
    main()
