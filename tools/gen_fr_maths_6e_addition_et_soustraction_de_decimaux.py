# -*- coding: utf-8 -*-
"""
France Maths 6e : Addition et soustraction de nombres décimaux
  python3 tools/gen_fr_maths_6e_addition_et_soustraction_de_decimaux.py
Erreurs : aligner les nombres à droite au lieu d’aligner les virgules (12,5 + 3,47 = 4,72), 5 − 2,35 = 3,35, oublier la retenue.
"""
import random
from fr_c4 import *

R = random.Random(60103)
K = Kids(R)


def rv(lo, hi, k):
    return Fr(R.randint(lo * 10 ** k, hi * 10 ** k), 10 ** k)


def misal(a, b, op):
    """aligner à droite sans tenir compte de la virgule"""
    ka, kb = [len(d(x).split(",")[1]) if "," in d(x) else 0 for x in (a, b)]
    k = max(ka, kb)
    A, B = int(a * 10 ** ka), int(b * 10 ** kb)
    r = A + B if op == "+" else A - B
    return Fr(r, 10 ** k) if r > 0 else None


def s1():
    a, b = rv(1, 20, 1), rv(1, 20, 1)
    if (a * 10) % 10 == 0 or (b * 10) % 10 == 0:
        return None
    r = a + b
    return M("%s + %s = …" % (d(a), d(b)), d(r), [d(r - 1) if (a * 10 % 10 + b * 10 % 10) >= 10 else d(r + 1), d(Fr(int(a) + int(b)) + Fr(int(a * 10 % 10 + b * 10 % 10), 100)), d(r + Fr(1, 10))],
             "Unités : %d + %d ; dixièmes : %d + %d. Résultat : <b>%s</b>." % (int(a), int(b), a * 10 % 10, b * 10 % 10, d(r)))


def s2():
    a = rv(5, 300, R.choice([1, 2]))
    b = rv(1, 99, R.choice([2, 3, 1]))
    if a.denominator == 1 or b.denominator == 1 or len(d(a).split(",")[1]) == len(d(b).split(",")[1]):
        return None
    r = a + b
    m = misal(a, b, "+")
    return M("Calcule : %s + %s" % (d(a), d(b)), d(r), [d(m) if m and m != r else d(r + 1), d(r + Fr(1, 10)), d(r - Fr(1, 100)) if r > 1 else d(r + 1)],
             "On aligne les virgules (on peut compléter avec des zéros), puis on calcule de droite à gauche : <b>%s</b>." % d(r))


def s3():
    k = R.choice(["entier", "dec", "dec"])
    if k == "entier":
        a = R.randint(3, 50)
        b = rv(1, a - 1, R.choice([1, 2]))
        if b.denominator == 1:
            return None
        r = a - b
        bad = Fr(int(a) - int(b)) + (b - int(b))
        return M("Calcule : %s − %s" % (d(a), d(b)), d(r), [d(bad), d(r + 1), d(r - Fr(1, 10)) if r > 1 else d(r + Fr(2, 10))],
                 "On écrit %s = %s, puis on soustrait : <b>%s</b>. Vérification : %s + %s = %s." % (d(a), dk(a, len(d(b).split(",")[1])), d(r), d(r), d(b), d(a)))
    a = rv(10, 200, 2)
    b = rv(1, 9, R.choice([1, 2]))
    if b >= a or a.denominator == 1 or b.denominator == 1:
        return None
    r = a - b
    m = misal(a, b, "−")
    return M("Calcule : %s − %s" % (d(a), d(b)), d(r), [d(m) if m and m != r else d(r + 1), d(r + Fr(1, 10)), d(a + b)],
             "On aligne les virgules : %s − %s = <b>%s</b>." % (d(a), d(b), d(r)))


def s4():
    k = R.choice(["unite", "miss", "miss2", "dix"])
    if k == "unite":
        a = rv(0, 0, 2) + Fr(R.randint(1, 99), 100)
        return M("Complète : %s + … = 1" % d(a), d(1 - a), [d(Fr(100 - int(a * 100), 10)) if int(a * 100) % 10 else d(1 - a + Fr(1, 10)), d(1 - a + Fr(1, 10)), d(1 + a)],
                 "%s + %s = 1 (car %d centièmes + %d centièmes = 100 centièmes)." % (d(a), d(1 - a), int(a * 100), 100 - int(a * 100)))
    if k == "dix":
        a = rv(1, 9, 1)
        if a.denominator == 1:
            return None
        return M("Complète : %s + … = 10" % d(a), d(10 - a), [d(10 - a + 1), d(10 - a + Fr(1, 10)), d(Fr(9 - int(a)) + Fr(10 - int(a * 10 % 10), 100))],
                 "%s + %s = 10." % (d(a), d(10 - a)))
    a, b = rv(1, 50, 2), rv(1, 50, 1)
    if k == "miss":
        return M("Complète : %s + … = %s" % (d(a), d(a + b)), d(b), [d(a + a + b), d(b + Fr(1, 10)), d(b - 1) if b > 1 else d(b + 1)],
                 "On calcule %s − %s = <b>%s</b>." % (d(a + b), d(a), d(b)))
    return M("Complète : … − %s = %s" % (d(a), d(b)), d(a + b), [d(abs(b - a)) if a != b else d(b + 1), d(a + b + 1), d(a + b - Fr(1, 10))],
             "On fait l’opération inverse : %s + %s = <b>%s</b>." % (d(b), d(a), d(a + b)))


def s5():
    p = K.next()
    k = R.choice(["courses", "reste", "ruban", "temp", "rando"])
    if k == "courses":
        a, b, c = [Fr(R.randint(80, 1500), 100) for _ in range(3)]
        t = a + b + c
        return M("%s achète un livre à %s €, un cahier à %s € et un stylo à %s €. Combien paie-t-%s ?" % (p[0], d(a), d(b), d(c), p[1]), euro(t), [euro(t + 1), euro(a + b), euro(t - Fr(1, 10))],
                 "%s + %s + %s = <b>%s €</b>." % (d(a), d(b), d(c), em(t)))
    if k == "reste":
        have = R.choice([20, 50])
        a = Fr(R.randint(250, have * 100 - 100), 100)
        return M("%s paie %s € avec un billet de %d €. Combien lui rend-on ?" % (p[0], d(a), have), euro(have - a),
                 [euro(Fr(have - int(a)) + (a - int(a))), euro(have - a + 1), euro(have + a)],
                 "%d − %s = <b>%s €</b>." % (have, d(a), em(have - a)))
    if k == "ruban":
        a = Fr(R.randint(20, 50), 10)
        b = Fr(R.randint(5, 150), 100)
        return M("Un ruban mesure %s m. On en coupe %s m. Quelle longueur reste-t-il ?" % (d(a), d(b)), "%s m" % d(a - b), ["%s m" % d(a + b), "%s m" % d(a - b + 1), "%s m" % d(a - b - Fr(1, 10)) if a - b > 1 else "%s m" % d(a - b + Fr(2, 10))],
                 "%s − %s = <b>%s m</b>." % (d(a), d(b), d(a - b)))
    if k == "temp":
        a = Fr(R.randint(360, 395), 10)
        b = Fr(R.randint(3, 18), 10)
        return M("Le matin, %s a %s °C de fièvre. Le soir, sa température a baissé de %s °C. Quelle est sa température le soir ?" % (p[0], d(a), d(b)), "%s °C" % d(a - b),
                 ["%s °C" % d(a + b), "%s °C" % d(a - b + 1), "%s °C" % d(a - b - Fr(1, 10))], "%s − %s = <b>%s °C</b>." % (d(a), d(b), d(a - b)))
    a, b = Fr(R.randint(25, 150), 10), Fr(R.randint(25, 150), 10)
    return M("Une randonnée se fait en deux étapes : %s km puis %s km. Quelle est la longueur totale ?" % (d(a), d(b)), "%s km" % d(a + b), ["%s km" % d(abs(a - b)) if a != b else "%s km" % d(a + b + 1), "%s km" % d(a + b + 1), "%s km" % d(a + b - Fr(1, 10))],
             "%s + %s = <b>%s km</b>." % (d(a), d(b), d(a + b)))


def main():
    seen = set()
    sets = [("Calcul mental", mix(R, seen, [(s1, 20)])), ("Additionner en alignant les virgules", mix(R, seen, [(s2, 20)])),
            ("Soustraire", mix(R, seen, [(s3, 20)])), ("Compléter", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Pour poser une addition ou une soustraction de décimaux, on <b>aligne les virgules</b> : unités sous unités, dixièmes sous dixièmes.",
              "On peut compléter avec des zéros : 5 = 5,00 ; 3,4 = 3,40.",
              "On vérifie une soustraction avec une addition."],
             [("12,5 + 3,47", ["12,50 + 3,47", "virgule sous virgule"], "15,97")],
             [["Aligner les chiffres à droite : 12,5 + 3,47 = 4,72", "On aligne les virgules : 12,50 + 3,47 = 15,97."],
              ["5 − 2,35 = 3,35", "5 = 5,00 ; 5,00 − 2,35 = 2,65."],
              ["Oublier la retenue", "Quand une colonne dépasse 9, on retient 1 dans la colonne de gauche."]])
    faq = [("Pourquoi aligner les virgules ?", "Pour additionner des chiffres de même rang : les dixièmes avec les dixièmes, les centièmes avec les centièmes."),
           ("Comment vérifier une soustraction ?", "On ajoute le résultat et le nombre enlevé : on doit retrouver le premier nombre.")]
    unit("6e", R, "addition-et-soustraction-de-decimaux", "N",
         "Calculer avec des nombres décimaux : additionner et soustraire mentalement, en ligne et en posant l’opération ; résoudre des problèmes",
         "Addition et soustraction de décimaux", "Addition et soustraction de décimaux",
         "Fiches de maths 6e sur l’addition et la soustraction de nombres décimaux : calcul mental, aligner les virgules, compléter et problèmes. 100 exercices corrigés.",
         "On aligne les virgules.", "5 = 5,00 : on peut ajouter des zéros.", body, faq, sets, 3)


if __name__ == "__main__":
    main()
