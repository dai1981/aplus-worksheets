# -*- coding: utf-8 -*-
"""
France Maths 4e : Opérations sur les fractions (relatifs, produit, inverse, quotient, priorités)
  python3 tools/gen_fr_maths_4e_operations_sur_les_fractions.py
Erreurs : additionner numérateurs et dénominateurs, diviser sans prendre l’inverse, mettre au même dénominateur pour multiplier.
"""
import random
from fr_c4 import *

R = random.Random(60302)
K = Kids(R)


def F():
    while True:
        a, b = R.randint(1, 9), R.randint(2, 9)
        if Fr(a, b).denominator != 1:
            return Fr(a * R.choice([1, 1, -1]), b), a, b


def raw(n, d_):
    return (MINUS if n * d_ < 0 else "") + fr(abs(n), abs(d_))


def s1():
    x, a, b = F()
    y, c, e = F()
    if x > 0 and y > 0:
        y = -y
    op = R.choice(["+", "−"])
    r = x + y if op == "+" else x - y
    if r == 0:
        return None
    wrong = Fr(x.numerator + (y.numerator if op == "+" else -y.numerator), x.denominator + y.denominator)
    return M("Calcule et simplifie : %s %s %s" % (fq(x), op, "(%s)" % fq(y) if y < 0 else fq(y)), fq(r), [fq(wrong) if wrong != r else fq(r + 1), fq(-r), fq(x - y if op == "+" else x + y) if (x - y if op == "+" else x + y) != r else fq(r * 2)],
             "On met au même dénominateur, puis on ajoute les numérateurs (règle des signes) : <b>%s</b>." % fq(r))


def s2():
    x, a, b = F()
    y, c, e = F()
    r = x * y
    k = R.choice(["prod", "prod", "simpl", "entier"])
    if k == "entier":
        n = R.choice([-6, -4, -3, 2, 3, 5, 8, 12])
        r = n * x
        return M("Calcule : %s × %s" % (par(n), fq(x)), fq(r), [raw(n * x.numerator, n * x.denominator), fq(-r), fq(Fr(x.numerator, n * x.denominator)) if Fr(x.numerator, n * x.denominator) != r else fq(r + 1)],
                 "%s × %s = %s = <b>%s</b>." % (d(n), fq(x), raw(n * x.numerator, x.denominator), fq(r)))
    if k == "simpl":
        p_ = R.choice([2, 3, 5])
        x = Fr(p_ * R.randint(1, 4), R.randint(2, 7) * R.choice([1, -1]))
        y = Fr(R.randint(1, 7), p_ * R.randint(1, 3))
        r = x * y
    w1 = Fr(x.numerator * y.numerator, x.denominator + y.denominator) if (x.denominator + y.denominator) else r + 1
    return M("Calcule et donne le résultat simplifié : %s × %s" % (fq(x), "(%s)" % fq(y) if y < 0 else fq(y)), fq(r), [fq(w1) if w1 != r else fq(r + 1), fq(-r), fq(x + y) if x + y != r else fq(r * 2)],
             "On multiplie les numérateurs entre eux et les dénominateurs entre eux, puis on simplifie : <b>%s</b>." % fq(r))


def s3():
    k = R.choice(["inv", "inv", "div", "div", "divent"])
    x, a, b = F()
    if k == "inv":
        if R.random() < 0.3:
            n = R.choice([-5, -4, 2, 3, 7, 10])
            return M("Quel est l’inverse de %s ?" % d(n), fq(Fr(1, n)), [d(-n), fq(Fr(-1, n)), "0"],
                     "L’inverse de %s est %s, car %s × %s = 1. (−%s est son opposé.)" % (d(n), fq(Fr(1, n)), d(n), fq(Fr(1, n)), d(abs(n))) if n > 0 else
                     "L’inverse de %s est <b>%s</b> : le produit vaut 1." % (d(n), fq(Fr(1, n))))
        return M("Quel est l’inverse de %s ?" % fq(x), fq(1 / x), [fq(-x), fq(-1 / x), fq(x)],
                 "On échange numérateur et dénominateur (le signe reste) : <b>%s</b>. Vérification : %s × %s = 1." % (fq(1 / x), fq(x), fq(1 / x)))
    y, c, e = F()
    if x == y:
        return None
    if k == "divent":
        n = R.choice([2, 3, 4, 5, -2, -3])
        r = x / n
        return M("Calcule : %s ÷ %s" % (fq(x), par(n)), fq(r), [fq(x * n), fq(Fr(x.numerator, x.denominator) / Fr(1, 1) * -1) if -x != r else fq(r + 1), fq(Fr(x.numerator // n, x.denominator)) if x.numerator % n == 0 and Fr(x.numerator // n, x.denominator) != r else fq(n / x)],
                 "Diviser par %s, c’est multiplier par %s : <b>%s</b>." % (d(n), fq(Fr(1, n)), fq(r)))
    r = x / y
    return M("Calcule : %s ÷ %s" % (fq(x), "(%s)" % fq(y) if y < 0 else fq(y)), fq(r), [fq(x * y), fq(y / x), fq(Fr(x.numerator * (1 if y > 0 else -1), x.denominator) * 0 + Fr(abs(x.numerator) // 1, 1) / abs(y.numerator) * Fr(y.denominator, x.denominator) * (-1 if r > 0 else 1))],
             "Diviser par %s, c’est multiplier par son inverse %s : %s × %s = <b>%s</b>." % (fq(y), fq(1 / y), fq(x), fq(1 / y), fq(r)))


def s4():
    x, _, _ = F()
    y, _, _ = F()
    z, _, _ = F()
    k = R.choice(["1", "2", "3"])
    if k == "1":
        e, r, w = "%s + %s × %s" % (fq(x), fq(abs(y)), fq(abs(z))), x + abs(y) * abs(z), [(x + abs(y)) * abs(z), x * abs(y) + abs(z)]
    elif k == "2":
        e, r, w = "(%s − %s) × %s" % (fq(abs(x)), fq(abs(y)), fq(abs(z))), (abs(x) - abs(y)) * abs(z), [abs(x) - abs(y) * abs(z), (abs(x) + abs(y)) * abs(z)]
    else:
        e, r, w = "%s − %s ÷ %s" % (fq(abs(x)), fq(abs(y)), fq(abs(z))), abs(x) - abs(y) / abs(z), [(abs(x) - abs(y)) / abs(z), abs(x) - abs(y) * abs(z)]
    if r.denominator > 60:
        return None
    w = [fq(v) for v in w if v != r] + [fq(-r)]
    return M("Calcule : %s" % e, fq(r), w, "On respecte les priorités (× et ÷ avant + et −) : <b>%s</b>." % fq(r))


def s5():
    p = K.next()
    k = R.choice(["reste", "partdepart", "frac_of_frac", "bouteilles", "recette"])
    if k == "reste":
        a = Fr(R.randint(1, 3), R.choice([4, 5, 6]))
        b = Fr(1, R.choice([2, 3, 4]))
        tot = (a.denominator * b.denominator) * R.randint(2, 6)
        rest = (1 - a) * (1 - b) * tot
        if rest.denominator != 1:
            return None
        return M("%s a %d €. %s dépense %s de son argent, puis %s de ce qui lui reste. Combien lui reste-t-il ?" % (p[0], tot, p[1].capitalize(), fq(a), fq(b)), euro(rest),
                 [euro(tot - (a + b) * tot) if tot - (a + b) * tot > 0 else euro(rest + 5), euro((1 - a) * tot), euro((a + b) * tot) if (a + b) < 1 else euro(rest * 2)],
                 "Il reste %s × %s = %s de l’argent : %s × %d = <b>%s</b>." % (fq(1 - a), fq(1 - b), fq((1 - a) * (1 - b)), fq((1 - a) * (1 - b)), tot, euro(rest)))
    if k == "partdepart":
        a = Fr(R.randint(1, 4), R.choice([5, 7, 9]))
        n = a.numerator * R.randint(2, 8)
        tot = n / a
        return M("Les %s d’une somme valent %d €. Quelle est la somme totale ?" % (fq(a), n), euro(tot), [euro(n * a) if (n * a).denominator in (1, 2, 4, 5) else euro(tot + a.denominator), euro(n + a.denominator), euro(Fr(n, a.numerator))],
                 "Somme = %d ÷ %s = %d × %s = <b>%s</b>." % (n, fq(a), n, fq(1 / a), euro(tot)))
    if k == "frac_of_frac":
        a, b = Fr(R.randint(1, 3), R.choice([4, 5])), Fr(R.randint(1, 2), 3)
        return M("Dans un collège, %s des élèves sont en 4e, et %s des élèves de 4e font du latin. Quelle fraction des élèves du collège fait du latin en 4e ?" % (fq(a), fq(b)), fq(a * b), [fq(a + b), fq(Fr(a.numerator + b.numerator, a.denominator + b.denominator)), fq(a / b) if a / b != a * b else fq(b - a)],
                 "« %s de %s » se calcule par un produit : %s × %s = <b>%s</b>." % (fq(b), fq(a), fq(b), fq(a), fq(a * b)))
    if k == "bouteilles":
        c = Fr(R.choice([1, 3]), 4) if R.random() < 0.5 else Fr(R.choice([1, 2]), 3)
        v = R.choice([6, 9, 12, 15, 18])
        n = v / c
        if n.denominator != 1:
            return None
        return M("Combien de verres de %s L peut-on remplir avec %d L de jus ?" % (fq(c), v), str(n), [d(v * c) if (v * c).denominator in (1, 2, 4) else str(n - 1), str(v), str(n + c.denominator)],
                 "%d ÷ %s = %d × %s = <b>%s</b>." % (v, fq(c), v, fq(1 / c), n))
    a = Fr(R.randint(2, 5), 4)
    q = R.choice([Fr(1, 2), Fr(2, 3), Fr(3, 2)])
    return M("Une recette demande %s kg de farine. On fait %s de la recette. Quelle masse de farine faut-il ?" % (fq(a), fq(q)), "%s kg" % fq(a * q), ["%s kg" % fq(a + q), "%s kg" % fq(a / q), "%s kg" % fq(a - q) if a > q else "%s kg" % fq(a * q * 2)],
             "%s × %s = <b>%s kg</b>." % (fq(a), fq(q), fq(a * q)))


def main():
    seen = set()
    sets = [("Additionner et soustraire (relatifs)", mix(R, seen, [(s1, 20)])), ("Multiplier des fractions", mix(R, seen, [(s2, 20)])),
            ("Inverse et division", mix(R, seen, [(s3, 20)])), ("Priorités avec des fractions", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Addition et soustraction : on met au <b>même dénominateur</b>, puis on additionne les numérateurs.",
              "Multiplication : numérateur × numérateur et dénominateur × dénominateur (on simplifie si possible).",
              "L’<b>inverse</b> de a/b est b/a. Diviser par une fraction, c’est multiplier par son inverse."],
             [("2/3 ÷ 4/5", ["= 2/3 × 5/4", "= 10/12"], "5/6")],
             [["2/3 + 1/4 = 3/7", "On met au même dénominateur : 8/12 + 3/12 = 11/12."], ["2/3 ÷ 4/5 = 8/15", "On multiplie par l’inverse : 2/3 × 5/4 = 5/6."],
              ["Confondre inverse et opposé", "L’opposé de 3/4 est −3/4 ; son inverse est 4/3."]])
    faq = [("Faut-il le même dénominateur pour multiplier ?", "Non : on multiplie directement numérateurs et dénominateurs."),
           ("0 a-t-il un inverse ?", "Non : aucun nombre multiplié par 0 ne donne 1.")]
    unit("4e", R, "operations-sur-les-fractions", "N",
         "Additionner, soustraire, multiplier et diviser des nombres en écriture fractionnaire (positifs ou négatifs) ; connaître l’inverse d’un nombre ; respecter les priorités ; résoudre des problèmes avec des fractions",
         "Opérations sur les fractions", "Opérations sur les fractions",
         "Fiches de maths 4e : additionner, soustraire, multiplier et diviser des fractions, inverse d’un nombre, priorités et problèmes. 100 exercices corrigés.",
         "a/b ÷ c/d = a/b × d/c", "Diviser, c’est multiplier par l’inverse", body, faq, sets, 2)


if __name__ == "__main__":
    main()
