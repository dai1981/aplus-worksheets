# -*- coding: utf-8 -*-
"""
France Maths 6e : Multiples, diviseurs et critères de divisibilité
  python3 tools/gen_fr_maths_6e_multiples_diviseurs_et_criteres.py
Erreurs : confondre multiple et diviseur, croire qu’un nombre qui finit par 3 est divisible par 3, oublier un diviseur.
"""
import random
from fr_c4 import *

R = random.Random(60106)
K = Kids(R)


def divs(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def s1():
    k = R.choice(["mult", "div", "vrai"])
    a = R.randint(3, 12)
    if k == "mult":
        good = a * R.randint(3, 15)
        bad = [good + 1, good + a // 2 if a > 2 else good + 1, good - 1]
        allv = sorted([good] + bad)
        return M("Lequel de ces nombres est un multiple de %d : %s ?" % (a, ", ".join(map(str, allv))), str(good), [str(x) for x in bad],
                 "%d = %d %s %d : <b>%d</b> est dans la table de %d." % (good, a, FOIS, good // a, good, a))
    if k == "div":
        n = R.choice([12, 18, 20, 24, 30, 36, 40, 42, 45, 48, 60, 72])
        good = R.choice([x for x in divs(n) if 1 < x < n])
        bad = [x for x in range(2, 13) if n % x][:6]
        R.shuffle(bad)
        return M("Lequel de ces nombres est un diviseur de %d ?" % n, str(good), [str(x) for x in bad[:2]] + [str(n * 2)],
                 "%d = %d %s %d : <b>%d</b> est un diviseur de %d." % (n, good, FOIS, n // good, good, n))
    b = a * R.randint(2, 9)
    ok = R.random() < 0.5
    if ok:
        return M("%d est-il un multiple de %d ?" % (b, a), "oui, car %d = %d %s %d" % (b, a, FOIS, b // a), ["non, car %d est plus grand que %d" % (b, a), "non, c’est un diviseur de %d" % a, "on ne peut pas savoir"],
                 "%d = %d %s %d : <b>%d est un multiple de %d</b> (et %d est un diviseur de %d)." % (b, a, FOIS, b // a, b, a, a, b))
    return M("%d est-il un diviseur de %d ?" % (b, a), "non, c’est %d qui est un diviseur de %d" % (a, b), ["oui, car %d = %d %s %d" % (b, a, FOIS, b // a), "oui, car %d est plus grand" % b, "on ne peut pas savoir"],
             "%d = %d %s %d : %d est un multiple de %d, et <b>%d est un diviseur de %d</b>." % (b, a, FOIS, b // a, b, a, a, b))


def s2():
    n = R.randint(100, 9999)
    k = R.choice([2, 5, 10])
    yes = n % k == 0
    crit = {2: "se termine par 0, 2, 4, 6 ou 8", 5: "se termine par 0 ou 5", 10: "se termine par 0"}[k]
    if R.random() < 0.5 and not yes:
        n = n - n % k
        yes = True
    return M("%s est-il divisible par %d ?" % (num(n), k), "oui" if yes else "non", ["non" if yes else "oui", "seulement s’il est pair" if k != 2 else "seulement s’il finit par 5", "on ne peut pas savoir sans poser la division"],
             "Un nombre est divisible par %d s’il %s. %s se termine par %d : <b>%s</b>." % (k, crit, num(n), n % 10, "oui" if yes else "non"))


def s3():
    k = R.choice([3, 9])
    n = R.randint(100, 99999)
    if R.random() < 0.5:
        n -= n % k
    sd = sum(int(c) for c in str(n))
    yes = n % k == 0
    if not yes and n % 10 in (3, 9):
        pass
    return M("%s est-il divisible par %d ?" % (num(n), k), "oui" if yes else "non", ["non" if yes else "oui", "oui, s’il se termine par %d" % k, "on ne peut pas savoir sans poser la division"],
             "On additionne les chiffres : %s = %d. %d %s divisible par %d, donc <b>%s</b>." % (" + ".join(str(n)), sd, sd, "est" if sd % k == 0 else "n’est pas", k, "oui" if yes else "non"))


def s4():
    n = R.choice([6, 8, 10, 12, 15, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 60])
    dv = divs(n)
    k = R.choice(["liste", "nb"])
    if k == "nb":
        return M("Combien %d a-t-il de diviseurs ?" % n, str(len(dv)), [str(len(dv) - 1), str(len(dv) - 2), str(len(dv) + 1)],
                 "Diviseurs de %d : %s. Il y en a <b>%d</b>." % (n, ", ".join(map(str, dv)), len(dv)))
    good = ", ".join(map(str, dv))
    miss = ", ".join(map(str, [x for x in dv if x not in (1, n)]))
    miss2 = ", ".join(map(str, [x for x in dv if x != dv[len(dv) // 2]]))
    wrong = ", ".join(map(str, sorted(set(dv[:-1]) | {dv[1] * 2 * 3 if dv[1] * 6 < n and n % (dv[1] * 6) else n - 1})))
    return M("Quelle est la liste de tous les diviseurs de %d ?" % n, good, [miss, miss2, wrong],
             "On cherche les produits qui font %d : %s. Diviseurs : <b>%s</b>." % (n, " ; ".join("%d %s %d" % (a, FOIS, n // a) for a in dv if a * a <= n), good))


def s5():
    p = K.next()
    k = R.choice(["rangs", "paquets", "bus", "jours"])
    if k == "rangs":
        n = R.choice([24, 30, 36, 40, 48, 60])
        r = R.choice([x for x in divs(n) if 2 < x < n // 2])
        return M("%s range %d chaises en rangées égales de %d. Combien de rangées obtient-%s ?" % (p[0], n, r, p[1]), str(n // r), [str(n - r), str(r), str(n // r + 1)],
                 "%d = %d %s %d : <b>%d rangées</b>." % (n, r, FOIS, n // r, n // r))
    if k == "paquets":
        n = R.randint(30, 200)
        k2 = R.choice([3, 9, 5])
        ok = n % k2 == 0
        return M("Peut-on ranger %d billes en paquets de %d sans qu’il en reste ?" % (n, k2), "oui" if ok else "non", ["non" if ok else "oui", "seulement si %d est pair" % n, "on ne peut pas savoir"],
                 "%d %s divisible par %d (%s) : <b>%s</b>." % (n, "est" if ok else "n’est pas", k2, "somme des chiffres : %d" % sum(map(int, str(n))) if k2 != 5 else "dernier chiffre : %d" % (n % 10), "oui" if ok else "non"))
    if k == "bus":
        a, b = R.choice([(6, 8), (4, 6), (10, 15), (6, 9), (12, 18), (8, 12)])
        l = a * b // __import__("math").gcd(a, b)
        return M("Un bus passe toutes les %d minutes et un tram toutes les %d minutes. Ils partent ensemble à 8 h. Dans combien de minutes repartent-ils ensemble ?" % (a, b), "%d min" % l, ["%d min" % (a * b) if a * b != l else "%d min" % (l * 2), "%d min" % (a + b), "%d min" % max(a, b)],
                 "On cherche le plus petit multiple commun à %d et %d : <b>%d min</b>." % (a, b, l))
    n = R.choice([12, 18, 24, 30, 36])
    good = max(x for x in divs(n) if x < n and x <= 12 and x != n)
    return M("%s veut faire des équipes de même taille avec %d élèves, sans personne seul. Lequel de ces nombres d’élèves par équipe convient ?" % (p[0], n), str(good), [str(x) for x in [7, 11, 5, 8, 9] if n % x][:3],
             "%d est un diviseur de %d : <b>%d</b> convient." % (good, n, good))


def main():
    seen = set()
    sets = [("Multiples et diviseurs", mix(R, seen, [(s1, 20)])), ("Divisible par 2, 5 et 10", mix(R, seen, [(s2, 20)])),
            ("Divisible par 3 et 9", mix(R, seen, [(s3, 20)])), ("Trouver tous les diviseurs", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["24 = 6 × 4 : 24 est un <b>multiple</b> de 6 ; 6 est un <b>diviseur</b> de 24 ; 24 est <b>divisible</b> par 6.",
              "Divisible par 2 : dernier chiffre 0, 2, 4, 6, 8. Par 5 : 0 ou 5. Par 10 : 0.",
              "Divisible par 3 (ou 9) : la somme des chiffres est divisible par 3 (ou 9)."],
             [("2 457 est-il divisible par 9 ?", ["2 + 4 + 5 + 7 = 18", "18 est divisible par 9"], "oui")],
             [["Confondre multiple et diviseur", "Le multiple est le plus grand : 24 est un multiple de 6."],
              ["Croire que 213 est divisible par 3 parce qu’il finit par 3", "On additionne les chiffres : 2 + 1 + 3 = 6, donc oui ; mais 23 ne l’est pas."],
              ["Oublier des diviseurs", "On cherche les produits dans l’ordre : 1 × 36, 2 × 18, 3 × 12, 4 × 9, 6 × 6."]])
    faq = [("1 est-il un diviseur de tous les nombres ?", "Oui, et tout nombre est un diviseur de lui-même."),
           ("Comment savoir vite si un nombre est divisible par 3 ?", "On additionne ses chiffres : si la somme est dans la table de 3, le nombre est divisible par 3.")]
    unit("6e", R, "multiples-diviseurs-et-criteres", "N",
         "Connaître les notions de multiple et de diviseur ; connaître et utiliser les critères de divisibilité par 2, 3, 5, 9 et 10 ; résoudre des problèmes",
         "Multiples, diviseurs et critères de divisibilité", "Multiples et diviseurs",
         "Fiches de maths 6e sur les multiples, les diviseurs et les critères de divisibilité par 2, 3, 5, 9 et 10, avec des problèmes. 100 exercices corrigés.",
         "24 = 6 × 4 : 24 est un multiple de 6.", "Par 3 : on additionne les chiffres.", body, faq, sets, 6)


if __name__ == "__main__":
    main()
