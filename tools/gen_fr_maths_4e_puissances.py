# -*- coding: utf-8 -*-
"""
France Maths 4e : Puissances (puissances d’un relatif, puissances de 10, préfixes, notation scientifique)
  python3 tools/gen_fr_maths_4e_puissances.py
Erreurs : 2³ = 6, 10⁻³ = −1 000, (−2)⁴ = −16, 10² × 10³ = 10⁶.
"""
import random
from fr_c4 import *

R = random.Random(60303)
K = Kids(R)


def sup(n):
    return "<sup>%s</sup>" % d(n)


def P(a, n):
    return "%s%s" % (par(a) if not isinstance(a, str) else a, sup(n))


def s1():
    k = R.choice(["pos", "neg", "neg2", "zero", "ecrire"])
    if k == "pos":
        a, n = R.randint(2, 9), R.randint(2, 4)
        if a ** n > 10000:
            return None
        return M("Calcule : %s" % P(a, n), num(a ** n), [num(a * n), num(a ** (n - 1)), num(a ** n + a)], "%s = %s = <b>%s</b>." % (P(a, n), " × ".join([str(a)] * n), num(a ** n)))
    if k == "neg":
        a, n = R.randint(2, 5), R.randint(2, 5)
        r = (-a) ** n
        return M("Calcule : %s" % P(-a, n), d(r), [d(-r), d(-a * n), d(r + (1 if r > 0 else -1))], "%d facteurs (−%d) : %s → <b>%s</b>." % (n, a, "nombre pair de signes −" if n % 2 == 0 else "nombre impair de signes −", d(r)))
    if k == "neg2":
        a, n = R.randint(2, 5), 2 * R.randint(1, 2)
        return M("Calcule : −%d%s (attention, pas de parenthèses)" % (a, sup(n)), d(-a ** n), [d(a ** n), d(-a * n), d(a * n)], "L’exposant ne porte que sur %d : −(%d%s) = <b>%s</b>." % (a, a, sup(n), d(-a ** n)))
    if k == "zero":
        a = R.choice([5, 7, 12, -3, 100])
        n = R.choice([0, 1])
        return M("Calcule : %s" % P(a, n), d(a ** n), ["0" if n == 0 else d(a * 10), d(a) if n == 0 else "1", d(a + n) if a + n != a ** n else "10"], "Par convention, a%s = %s : <b>%s</b>." % (sup(n), "1" if n == 0 else "a", d(a ** n)))
    a, n = R.randint(2, 9), R.randint(3, 6)
    return M("Comment écrire %s sous forme de puissance ?" % " × ".join([str(a)] * n), P(a, n), ["%d × %d" % (a, n), P(n, a), P(a, n + 1)], "%s facteurs égaux à %d : <b>%s</b>." % (d(n), a, P(a, n)))


def s2():
    k = R.choice(["pos", "neg", "lire", "lireneg"])
    n = R.randint(1, 7)
    if k == "pos":
        return M("Écris en écriture décimale : 10%s" % sup(n), num(10 ** n), [num(10 * n), num(10 ** (n + 1)), num(10 ** (n - 1)) if n > 1 else "100"], "1 suivi de %s : <b>%s</b>." % (pl(n, "zéro"), num(10 ** n)))
    if k == "neg":
        n = R.randint(1, 5)
        return M("Écris en écriture décimale : 10%s" % sup(-n), d(Fr(1, 10 ** n)), [d(-10 ** n), d(Fr(1, 10 ** (n + 1))), d(Fr(1, 10 ** (n - 1))) if n > 1 else "−10"],
                 "10%s = 1 ÷ 10%s : le 1 est au rang n° %d après la virgule : <b>%s</b>." % (sup(-n), sup(n), n, d(Fr(1, 10 ** n))))
    if k == "lire":
        return M("Écris %s sous forme d’une puissance de 10." % num(10 ** n), "10%s" % sup(n), ["10%s" % sup(n + 1), "10%s" % sup(n - 1) if n > 1 else "10%s" % sup(-1), "%d%s" % (n, sup(10))], "Il y a %s : <b>10%s</b>." % (pl(n, "zéro"), sup(n)))
    n = R.randint(1, 6)
    return M("Écris %s sous forme d’une puissance de 10." % d(Fr(1, 10 ** n)), "10%s" % sup(-n), ["10%s" % sup(n), "10%s" % sup(-n - 1), "10%s" % sup(-n + 1) if n > 1 else "10%s" % sup(0)],
             "Le 1 est au %de rang après la virgule : <b>10%s</b>." % (n, sup(-n)) if n > 1 else "Le 1 est au 1er rang après la virgule : <b>10%s</b>." % sup(-n))


def s3():
    m, n = R.randint(-6, 8), R.randint(-6, 8)
    k = R.choice(["prod", "quot", "puis", "prefix"])
    if k == "prod":
        return M("Écris sous la forme 10<sup>n</sup> : 10%s × 10%s" % (sup(m), sup(n)), "10%s" % sup(m + n), ["10%s" % sup(m * n), "100%s" % sup(m + n), "10%s" % sup(m - n) if m - n != m + n else "10%s" % sup(m + n + 1)],
                 "On additionne les exposants : %s + %s = %s : <b>10%s</b>." % (d(m), par(n), d(m + n), sup(m + n)))
    if k == "quot":
        return M("Écris sous la forme 10<sup>n</sup> : %s" % fr("10%s" % sup(m), "10%s" % sup(n)), "10%s" % sup(m - n), ["10%s" % sup(m + n) if m + n != m - n else "10%s" % sup(m - n + 1), "10%s" % sup(n - m) if n != m else "10%s" % sup(1), "10%s" % sup(m * n) if m * n not in (m - n, m + n, n - m) else "10%s" % sup(m - n + 2)],
                 "On soustrait les exposants : %s − %s = %s : <b>10%s</b>." % (d(m), par(n), d(m - n), sup(m - n)))
    if k == "puis":
        m, n = R.randint(-4, 5), R.randint(2, 4)
        if m in (0, 1):
            return None
        return M("Écris sous la forme 10<sup>n</sup> : (10%s)%s" % (sup(m), sup(n)), "10%s" % sup(m * n), ["10%s" % sup(m + n), "10%s" % sup(m ** n) if m ** n != m * n else "10%s" % sup(m * n + 1), "10%s" % sup(m * n - 1)],
                 "On multiplie les exposants : %s × %d = %s : <b>10%s</b>." % (d(m), n, d(m * n), sup(m * n)))
    PF = [("kilo", 3, "km", "m"), ("méga", 6, "Mo", "octets"), ("giga", 9, "Go", "octets"), ("milli", -3, "mm", "m"), ("micro", -6, "µm", "m"), ("nano", -9, "nm", "m"), ("centi", -2, "cm", "m")]
    nm, e, u, base = R.choice(PF)
    wr = [x[1] for x in PF if x[1] != e]
    R.shuffle(wr)
    return M("Le préfixe « %s » (1 %s = 10<sup>?</sup> %s) correspond à quelle puissance de 10 ?" % (nm, u, base), "10%s" % sup(e), ["10%s" % sup(w) for w in wr[:3]], "%s = <b>10%s</b>." % (nm.capitalize(), sup(e)))


def sci(x):
    """(mantisse décimale, exposant)"""
    x = Fr(x)
    e = 0
    while abs(x) >= 10:
        x /= 10
        e += 1
    while abs(x) < 1:
        x *= 10
        e -= 1
    return x, e


def S(m, e):
    return "%s × 10%s" % (d(m), sup(e))


def s4():
    k = R.choice(["big", "small", "lire", "pasbonne"])
    m = Fr(R.randint(11, 999), 100)
    if m * 10 % 1 == 0 and R.random() < 0.5:
        m = Fr(R.randint(11, 99), 10)
    e = R.randint(3, 8) if k in ("big", "lire") else R.randint(-7, -2)
    x = m * Fr(10) ** e
    if k in ("big", "small"):
        return M("Donne l’écriture scientifique de %s." % d(x), S(m, e), [S(m * 10, e - 1), S(m, -e), S(m / 10, e + 1)],
                 "On écrit un nombre entre 1 et 10 (exclu) : %s, puis on compte les rangs de décalage : <b>%s</b>." % (d(m), S(m, e)))
    if k == "lire":
        return M("Écris en écriture décimale : %s" % S(m, e), d(x), [d(x * 10), d(x / 10), d(m * e)], "On décale la virgule de %s vers la droite : <b>%s</b>." % (pl(e, "rang"), d(x)))
    c = Fr(R.randint(11, 99), 10)
    e = R.randint(-4, 6)
    opts = [S(c, e), S(c * 10, e - 1), S(c / 10, e + 1), S(c * 100, e - 2)]
    ok = opts[0]
    return M("Quelle écriture est une écriture scientifique ?", ok, opts[1:], "Le nombre devant la puissance de 10 doit être entre 1 et 10 (10 exclu) : <b>%s</b>." % ok)


def s5():
    k = R.choice(["terre", "cellule", "prod", "lumiere", "compare"])
    if k == "terre":
        D = [("La distance Terre–Soleil est d’environ 150 000 000 km.", 150000000, "km"), ("La Terre a une masse d’environ 6 000 000 000 000 000 000 000 000 kg.", 6 * 10 ** 24, "kg"),
             ("Il y a environ 8 000 000 000 d’habitants sur Terre.", 8 * 10 ** 9, ""), ("La distance Terre–Lune est d’environ 384 000 km.", 384000, "km")]
        t, v, u = R.choice(D)
        m, e = sci(v)
        uu = (NB + u) if u else ""
        return M("%s Écris ce nombre en notation scientifique." % t, S(m, e) + uu, [S(m * 10, e - 1) + uu, S(m, e + 1) + uu, S(m, e - 1) + uu], "<b>%s</b>." % (S(m, e) + uu))
    if k == "cellule":
        D = [("Un globule rouge mesure environ 0,000 007 m.", Fr(7, 10 ** 6)), ("Un virus mesure environ 0,000 000 1 m.", Fr(1, 10 ** 7)), ("Une bactérie mesure environ 0,000 002 m.", Fr(2, 10 ** 6)),
             ("L’épaisseur d’un cheveu est d’environ 0,000 08 m.", Fr(8, 10 ** 5))]
        t, v = R.choice(D)
        m, e = sci(v)
        return M("%s Écris cette longueur en notation scientifique." % t, S(m, e) + " m", [S(m, -e) + " m", S(m, e - 1) + " m", S(m, e + 1) + " m"], "<b>%s m</b>." % S(m, e))
    if k == "prod":
        a, b = R.randint(2, 4), R.randint(2, 4)
        e, f = R.randint(-5, 8), R.randint(-5, 8)
        m, ee = sci(Fr(a * b) * Fr(10) ** (e + f))
        return M("Calcule et donne le résultat en notation scientifique : (%s) × (%s)" % (S(a, e), S(b, f)), S(m, ee), [S(a * b, e * f) if a * b < 10 else S(Fr(a * b, 10), e * f + 1), S(a + b, e + f), S(m, ee + 1)],
                 "%d × %d = %d et 10%s × 10%s = 10%s, donc <b>%s</b>." % (a, b, a * b, sup(e), sup(f), sup(e + f), S(m, ee)))
    if k == "lumiere":
        t = R.choice([10, 60, 100, 500])
        r = 3 * 10 ** 5 * t
        m, e = sci(r)
        return M("La lumière parcourt environ 3 × 10%s km par seconde. Quelle distance parcourt-elle en %d s ? (notation scientifique)" % (sup(5), t), S(m, e) + " km", [S(m, e - 1) + " km", S(m, e + 1) + " km", S(3, 5) + " km"],
                 "3 × 10%s × %d = %s = <b>%s km</b>." % (sup(5), t, num(r), S(m, e)))
    a, b = Fr(R.randint(11, 99), 10), Fr(R.randint(11, 99), 10)
    e = R.randint(-3, 6)
    f = e + R.choice([-1, 1])
    x, y = a * Fr(10) ** e, b * Fr(10) ** f
    big = S(a, e) if x > y else S(b, f)
    return M("Quel est le plus grand nombre : %s ou %s ?" % (S(a, e), S(b, f)), big, ["ils sont égaux", S(b, f) if big == S(a, e) else S(a, e), "on ne peut pas comparer"],
             "On compare d’abord les puissances de 10 : 10%s &gt; 10%s. Le plus grand est <b>%s</b>." % (sup(max(e, f)), sup(min(e, f)), big))


def main():
    seen = set()
    sets = [("Puissances d’un nombre relatif", mix(R, seen, [(s1, 20)])), ("Puissances de 10", mix(R, seen, [(s2, 20)])),
            ("Calculer avec des puissances de 10", mix(R, seen, [(s3, 20)])), ("Notation scientifique", mix(R, seen, [(s4, 20)])), ("Problèmes : très grands et très petits nombres", mix(R, seen, [(s5, 20)]))]
    body = L(["a<sup>n</sup> est le produit de n facteurs égaux à a. Avec un nombre négatif : exposant pair → positif, impair → négatif.",
              "10<sup>n</sup> = 1 suivi de n zéros ; 10<sup>−n</sup> = 0,0…01 avec le 1 au n-ième rang après la virgule.",
              "10<sup>m</sup> × 10<sup>n</sup> = 10<sup>m+n</sup>. L’<b>écriture scientifique</b> est a × 10<sup>n</sup> avec 1 ≤ a &lt; 10."],
             [("0,000 52", ["5,2 est entre 1 et 10", "on décale la virgule de 4 rangs"], "5,2 × 10<sup>−4</sup>")],
             [["2³ = 6", "2³ = 2 × 2 × 2 = 8."], ["10<sup>−3</sup> = −1 000", "10<sup>−3</sup> = 0,001 : c’est un nombre positif."],
              ["52 × 10<sup>3</sup> est une écriture scientifique", "Le premier nombre doit être entre 1 et 10 : 5,2 × 10<sup>4</sup>."]])
    faq = [("À quoi sert l’écriture scientifique ?", "À écrire et comparer facilement des nombres très grands (distances en astronomie) ou très petits (taille des cellules)."),
           ("Pourquoi (−2)⁴ et −2⁴ sont-ils différents ?", "(−2)⁴ = 16 car l’exposant porte sur −2 ; −2⁴ = −16 car l’exposant ne porte que sur 2.")]
    unit("4e", R, "puissances", "N",
         "Calculer des puissances entières d’un nombre relatif ; utiliser les puissances de 10 d’exposant positif ou négatif et les préfixes (kilo, méga, giga, milli, micro, nano) ; calculer des produits et des quotients de puissances de 10 ; utiliser l’écriture scientifique",
         "Puissances", "Puissances",
         "Fiches de maths 4e sur les puissances : puissances d’un relatif, puissances de 10, préfixes, calculs et écriture scientifique. 100 exercices corrigés.",
         "10ᵐ × 10ⁿ = 10ᵐ⁺ⁿ", "Écriture scientifique : a × 10ⁿ avec 1 ≤ a < 10", body, faq, sets, 3)


if __name__ == "__main__":
    main()
