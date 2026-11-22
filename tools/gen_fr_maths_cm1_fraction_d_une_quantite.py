# -*- coding: utf-8 -*-
"""
France Maths CM1 : Fraction d’une quantité — CM2 (build(2)) : Fraction d’une quantité et produit d’un entier par une fraction
  python3 tools/gen_fr_maths_cm1_fraction_d_une_quantite.py
CM1 : fraction unitaire comme opérateur (1/4 de 36), fractions simples d’une grandeur (3/4 h, 1/2 kg), retrouver le tout.
CM2 : fraction non unitaire d’une quantité (3/5 de 40), entier × fraction (5 × 2/3), problèmes.
Erreurs : multiplier au lieu de diviser (1/4 de 36 = 144), oublier de multiplier par le numérateur (3/4 de 36 = 9),
5 × 2/3 = 10/15.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, fr, FOIS, DIV, dz

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52110 + 100 * lv)
    K = Kids(R)


def s1():
    d = R.randint(2, 10 if L == 1 else 12)
    q = R.randint(2, 15 if L == 1 else 25)
    n = d * q
    return mcq("Combien vaut %s de %d ?" % (fr(1, d), n), num(q), [num(n * d), num(n - d), num(q + d)],
               "%s de %d, c’est %d partagé en %d : %d %s %d = <b>%d</b>." % (fr(1, d), n, n, d, n, DIV, d, q))


GRAND = [("h", 60, "min", [2, 3, 4, 5, 6, 10, 12]), ("kg", 1000, "g", [2, 4, 5, 10]), ("m", 100, "cm", [2, 4, 5, 10]), ("L", 100, "cL", [2, 4, 5, 10]),
         ("km", 1000, "m", [2, 4, 5, 10]), ("€", 100, "c", [2, 4, 5, 10])]


def s2():
    u, v, su, ds = R.choice(GRAND)
    d = R.choice(ds)
    n = R.randint(1, d - 1) if R.random() < 0.6 else 1
    if __import__("math").gcd(n, d) > 1:
        return None
    r = v * n // d
    art = {"h": "d’heure", "kg": "kg", "m": "m", "L": "L", "km": "km", "€": "€"}[u]
    return mcq("Combien de %s dans %s %s ?" % ({"min": "minutes", "g": "grammes", "cm": "centimètres", "cL": "centilitres", "m": "mètres", "c": "centimes"}[su], fr(n, d), art),
               "%s %s" % (num(r), su), ["%s %s" % (num(v // d), su) if n > 1 else "%s %s" % (num(v * d), su), "%s %s" % (num(r * 10), su), "%s %s" % (num(v * n), su) if v * n != r else "%s %s" % (num(r * 2), su)],
               "1 %s = %s %s ; on prend %s de %s : %s %s %d %s %d = <b>%s %s</b>." % (u, num(v), su, fr(n, d), num(v), num(v), DIV, d, FOIS, n, num(r), su))


def s3():
    d = R.randint(3, 10 if L == 1 else 15)
    n = R.randint(2, d - 1)
    if __import__("math").gcd(n, d) > 1:
        return None
    q = R.randint(2, 12 if L == 1 else 20)
    t = d * q
    r = n * q
    return mcq("Combien vaut %s de %d ?" % (fr(n, d), t), num(r), [num(q), num(t * n // 1 if False else t - n), num(t // n) if t % n == 0 and t // n != r else num(r + n)],
               "%s de %d : %d %s %d = %d (un %s), puis %d %s %d = <b>%d</b>." % (fr(n, d), t, t, DIV, d, q, "part", q, FOIS, n, r))


def s4_cm1():
    d = R.randint(2, 10)
    q = R.randint(3, 15)
    k = R.choice(["classe", "livre", "sac"])
    if k == "classe":
        return mcq("%s des élèves d’une classe portent des lunettes. Ils sont %d. Combien d’élèves y a-t-il dans la classe ?" % (fr(1, d).replace("<span class='fr'>", "<span class='fr'>"), q) if d * q <= 32 else
                   "Le %s d’une collection de timbres fait %d timbres. Combien de timbres a la collection ?" % ({2: "demi", 3: "tiers", 4: "quart"}.get(d, "%s" % ("cinquième sixième septième huitième neuvième dixième".split()[d - 5] if d >= 5 else "")), q),
                   num(d * q), [num(q), num(q + d), num(q * (d - 1))], "Si %s fait %d, le tout fait %d fois plus : %d %s %d = <b>%d</b>." % (fr(1, d), q, d, d, FOIS, q, d * q))
    if k == "livre":
        return mcq("%s a lu %s de son livre, soit %d pages. Combien de pages a le livre ?" % (K.next()[0], fr(1, d), q * 5), num(d * q * 5), [num(q * 5 // d) if q * 5 % d == 0 else num(q * 5 + d), num(q * 5 + d * 5), num(q * 5)],
                       "%s du livre = %d pages, donc le livre en a %d %s %d = <b>%d</b>." % (fr(1, d), q * 5, d, FOIS, q * 5, d * q * 5))
    return mcq("Un sac de billes : %s du sac, c’est %d billes. Combien de billes dans le sac ?" % (fr(1, d), q), num(d * q), [num(q), num(q * d + q), num(q - 1 + d)],
               "%d %s %d = <b>%d</b>." % (d, FOIS, q, d * q))


def s4_cm2():
    if R.random() < 0.3:
        return s4_cm1()
    n = R.randint(2, 12)
    a, d = R.randint(1, 9), R.randint(2, 12)
    if a >= d and R.random() < 0.5:
        return None
    r = n * a
    return mcq("Calcule : %d %s %s" % (n, FOIS, fr(a, d)), fr(r, d), [fr(r, n * d), fr(a, n * d), fr(n + a, d)],
               "%d %s %s, c’est %d fois %s : on multiplie le numérateur par %d. Résultat : <b>%s</b>%s." % (n, FOIS, fr(a, d), n, fr(a, d), n, fr(r, d),
                                                                                                    "" if r < d or r % d else " = %d" % (r // d)))


def s4():
    return s4_cm1() if L == 1 else s4_cm2()


def s5():
    p = K.next()
    k = R.choice(["argent", "trajet", "classe", "temps", "gateaux"])
    if k == "argent":
        d = R.choice([2, 3, 4, 5, 10])
        n = 1 if L == 1 else R.randint(1, d - 1)
        if __import__("math").gcd(n, d) > 1:
            return None
        t = d * R.randint(3, 12) * (1 if L == 1 else 2)
        return mcq("%s a %d €. %s dépense %s de son argent. Combien dépense-t-%s ?" % (p[0], t, p[1].capitalize(), fr(n, d), p[1]), "%d €" % (t * n // d),
                   ["%d €" % (t - t * n // d), "%d €" % (t // d) if n > 1 else "%d €" % (t * d), "%d €" % (t + d)], "%s de %d : %d %s %d %s %d = <b>%d €</b>." % (fr(n, d), t, t, DIV, d, FOIS, n, t * n // d))
    if k == "trajet":
        d = R.choice([2, 3, 4, 5])
        n = R.randint(1, d - 1)
        if __import__("math").gcd(n, d) > 1:
            return None
        t = d * R.randint(4, 30)
        return mcq("Un trajet fait %d km. On en a parcouru %s. Combien de kilomètres reste-t-il ?" % (t, fr(n, d)), "%d km" % (t - t * n // d), ["%d km" % (t * n // d), "%d km" % (t - d), "%d km" % (t // d)],
                   "Parcouru : %s de %d = %d km. Reste : %d − %d = <b>%d km</b>." % (fr(n, d), t, t * n // d, t, t * n // d, t - t * n // d))
    if k == "classe":
        d = R.choice([2, 3, 4])
        t = d * R.randint(6, 8)
        n = 1 if d == 2 else R.randint(1, d - 1)
        return mcq("Dans une classe de %d élèves, %s font du sport le mercredi. Combien d’élèves font du sport ?" % (t, fr(n, d)), str(t * n // d), [str(t // d) if n > 1 else str(t - d), str(t - t * n // d) if t - t * n // d != t * n // d else str(t * n), str(t * d) if t * d < 200 else str(t + d)],
                   "%d %s %d %s %d = <b>%d</b>." % (t, DIV, d, FOIS, n, t * n // d))
    if k == "temps":
        d = R.choice([3, 4, 6])
        n = R.randint(1, d - 1)
        if __import__("math").gcd(n, d) > 1:
            return None
        return mcq("%s s’entraîne pendant %s d’heure. Combien de minutes cela fait-il ?" % (p[0], fr(n, d)), "%d min" % (60 * n // d), ["%d min" % (60 // d), "%d min" % (n * 10 + d), "%d min" % (100 * n // d)],
                   "60 %s %d %s %d = <b>%d min</b>." % (DIV, d, FOIS, n, 60 * n // d))
    n, a, d = R.randint(3, 9), R.randint(1, 3), R.choice([4, 5, 8])
    if L == 1:
        a = 1
    return mcq("Une recette demande %s de kg de farine par gâteau. Quelle masse de farine pour %d gâteaux ?" % (fr(a, d), n), fr(n * a, d) + " kg", [fr(n * a, n * d) + " kg", fr(a, n * d) + " kg", fr(n + a, d) + " kg"],
               "%d %s %s = <b>%s kg</b>%s." % (n, FOIS, fr(a, d), fr(n * a, d), "" if (n * a) % d else " = %d kg" % (n * a // d)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Fraction unitaire d’un nombre", mix(R, seen, [(s1, 20)])),
        ("Fraction d’une grandeur", mix(R, seen, [(s2, 20)])),
        ("Fraction d’un nombre", mix(R, seen, [(s3, 20)])),
        ("Retrouver le tout" if lv == 1 else "Un entier × une fraction", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["%s de 36, c’est 36 partagé en 4 : 36 %s 4 = 9." % (fr(1, 4), DIV),
         "%s de 36 : on prend 3 fois le quart : 9 %s 3 = 27." % (fr(3, 4), FOIS),
         "Pour une grandeur, on passe à une unité plus petite : %s h = 60 min %s 4 %s 3 = 45 min." % (fr(3, 4), DIV, FOIS)] +
        (["%d %s %s, c’est %s + %s + %s + %s + %s = %s : on multiplie le numérateur." % (5, FOIS, fr(2, 3), fr(2, 3), fr(2, 3), fr(2, 3), fr(2, 3), fr(2, 3), fr(10, 3))] if lv == 2 else
         ["Si %s d’un sac fait 7 billes, le sac entier en fait 4 fois plus : 28." % fr(1, 4)]),
        [example("%s de 40" % fr(3, 5), ["40 %s 5 = 8" % DIV, "8 %s 3 = 24" % FOIS], "24")],
        [["Multiplier au lieu de diviser : %s de 36 = 144" % fr(1, 4), "Prendre un quart, c’est partager en 4 : 9."],
         ["Oublier le numérateur : %s de 36 = 9" % fr(3, 4), "9, c’est un quart. Trois quarts : 27."],
         ["5 %s %s = %s" % (FOIS, fr(2, 3), fr(10, 15)), "Les parts restent des tiers : %s." % fr(10, 3)]])
    faq = [("Que veut dire « les trois quarts de » ?", "Partager en 4 parts égales et en prendre 3."),
           ("Pourquoi changer d’unité pour une grandeur ?", "Pour calculer avec des nombres entiers : %s h = 45 min est plus facile à utiliser." % fr(3, 4))]
    unit(lv, R, "fraction-d-une-quantite" if lv == 1 else "fraction-d-une-quantite-et-multiplication", "N",
         ("Déterminer une fraction d’une quantité ou d’une grandeur en utilisant les fractions unitaires comme opérateur" if lv == 1 else
          "Déterminer une fraction d’une quantité ou d’une grandeur en utilisant une fraction comme opérateur ; calculer le produit d’un nombre entier par une fraction"),
         "Fraction d’une quantité" if lv == 1 else "Fraction d’une quantité et entier × fraction", "Fraction d’une quantité" if lv == 1 else "Fraction d’une quantité et multiplication",
         ("Fiches de maths CM1 : calculer la fraction d’un nombre ou d’une grandeur (1/4 de 36, 3/4 h), retrouver le tout et problèmes. 100 exercices corrigés." if lv == 1 else
          "Fiches de maths CM2 : fraction d’un nombre et d’une grandeur, produit d’un entier par une fraction (5 × 2/3) et problèmes. 100 exercices corrigés."),
         "3/4 de 36 : 36 ÷ 4 = 9, puis 9 × 3 = 27.", "Le dénominateur partage, le numérateur multiplie.",
         body, faq, sets, 10)


if __name__ == "__main__":
    build(1)
