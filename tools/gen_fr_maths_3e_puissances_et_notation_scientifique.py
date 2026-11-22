# -*- coding: utf-8 -*-
"""
France Maths 3e : Puissances (règles de calcul) et notation scientifique
  python3 tools/gen_fr_maths_3e_puissances_et_notation_scientifique.py
Erreurs : a³ × a⁴ = a¹², (a²)³ = a⁵, 2⁻³ = −8, 5 × 10³ × 4 × 10² = 20 × 10⁵ laissé tel quel.
"""
import random
from fr_c4 import *

R = random.Random(60402)
K = Kids(R)


def sup(n):
    return "<sup>%s</sup>" % d(n)


def P(a, n):
    return "%s%s" % (a if isinstance(a, str) else par(a), sup(n))


def S(m, e):
    return "%s × 10%s" % (d(m), sup(e))


def sci(x):
    x = Fr(x)
    e = 0
    while abs(x) >= 10:
        x /= 10
        e += 1
    while abs(x) < 1:
        x *= 10
        e -= 1
    return x, e


def s1():
    a = R.choice(["a", "x", "2", "3", "5", "7"])
    m, n = R.randint(-4, 7), R.randint(-4, 7)
    k = R.choice(["prod", "quot", "pow", "prod"])
    if k == "prod":
        return M("Écris sous la forme d’une seule puissance : %s × %s" % (P(a, m), P(a, n)), P(a, m + n), [P(a, m * n), P(a, m - n) if m - n != m + n else P(a, m + n + 1), "%s%s" % (a, sup(m + n + 2))],
                 "a<sup>m</sup> × a<sup>n</sup> = a<sup>m+n</sup> : %s + %s = %s → <b>%s</b>." % (d(m), par(n), d(m + n), P(a, m + n)))
    if k == "quot":
        return M("Écris sous la forme d’une seule puissance : %s" % fr(P(a, m), P(a, n)), P(a, m - n), [P(a, m + n) if m + n != m - n else P(a, m - n + 1), P(a, Fr(m, n)) if n and Fr(m, n).denominator == 1 and Fr(m, n) != m - n else P(a, n - m) if n != m else P(a, 1), P(a, m * n) if m * n not in (m - n, m + n, n - m) else P(a, m - n + 2)],
                 "a<sup>m</sup> ÷ a<sup>n</sup> = a<sup>m−n</sup> : %s − %s = %s → <b>%s</b>." % (d(m), par(n), d(m - n), P(a, m - n)))
    m, n = R.randint(-3, 5), R.randint(2, 4)
    if m in (0, 1):
        return None
    return M("Écris sous la forme d’une seule puissance : (%s)%s" % (P(a, m), sup(n)), P(a, m * n), [P(a, m + n), P(a, m ** n) if m ** n != m * n else P(a, m * n + 1), P(a, m * n - 1)],
             "(a<sup>m</sup>)<sup>n</sup> = a<sup>m×n</sup> : %s × %d = %s → <b>%s</b>." % (d(m), n, d(m * n), P(a, m * n)))


def s2():
    k = R.choice(["neg", "neg", "zero", "mix"])
    if k == "neg":
        a, n = R.randint(2, 5), R.randint(1, 3)
        r = Fr(1, a ** n)
        return M("Écris sous forme de fraction : %s" % P(a, -n), fq(r), [d(-a ** n), d(-a * n), fq(Fr(1, a * n)) if a * n != a ** n else fq(Fr(n, a))],
                 "a<sup>−n</sup> = 1 ÷ a<sup>n</sup> : 1 ÷ %s = <b>%s</b>." % (P(a, n), fq(r)))
    if k == "zero":
        a = R.choice([2, 5, -3, 10, 7])
        return M("Calcule : %s + %s" % (P(a, 0), P(a, 1)), d(1 + a), [d(a), d(2 * a) if 2 * a != 1 + a else "0", d(1)], "%s = 1 et %s = %s : 1 + %s = <b>%s</b>." % (P(a, 0), P(a, 1), d(a), par(a), d(1 + a)))
    a, b = R.randint(2, 4), R.randint(2, 4)
    n = R.randint(2, 3)
    r = (a * b) ** n
    return M("Calcule : %s × %s" % (P(a, n), P(b, n)), num(r), [num((a * b) ** (2 * n)) if (a * b) ** (2 * n) < 10 ** 6 else num(r + 1), num(a ** n + b ** n), num((a + b) ** n)],
             "a<sup>n</sup> × b<sup>n</sup> = (a × b)<sup>n</sup> = %d%s = <b>%s</b>." % (a * b, sup(n), num(r)))


def s3():
    a, b = Fr(R.randint(11, 99), 10), Fr(R.randint(11, 99), 10)
    e, f = R.randint(-8, 9), R.randint(-8, 9)
    k = R.choice(["prod", "prod", "quot", "simpl"])
    if k == "prod":
        m, ee = sci(a * b * Fr(10) ** (e + f))
        raw = "%s × 10%s" % (d(a * b), sup(e + f))
        if raw == S(m, ee):
            return None
        return M("Donne en notation scientifique : (%s) × (%s)" % (S(a, e), S(b, f)), S(m, ee), [raw, S(m, ee + 1) if a * b >= 10 else S(m, ee - 1), S(m, ee - 1) if a * b >= 10 else S(m, ee + 1)],
                 "%s × %s = %s et 10%s × 10%s = 10%s ; on ajuste : <b>%s</b>." % (d(a), d(b), d(a * b), sup(e), sup(f), sup(e + f), S(m, ee)))
    if k == "quot":
        b = Fr(R.choice([2, 4, 5, 8]), R.choice([1, 10]))
        if b < 1:
            return None
        q = a / b
        if (q * 1000).denominator != 1:
            return None
        m, ee = sci(q * Fr(10) ** (e - f))
        return M("Donne en notation scientifique : %s" % fr(S(a, e), S(b, f)), S(m, ee), [S(m, e + f), "%s × 10%s" % (d(q), sup(e - f)) if (q < 1 or q >= 10) else S(m, ee + 1), S(m, ee - 1)],
                 "%s ÷ %s = %s et 10%s ÷ 10%s = 10%s ; on ajuste : <b>%s</b>." % (d(a), d(b), d(q), sup(e), sup(f), sup(e - f), S(m, ee)))
    c = R.choice([Fr(R.randint(11, 999)), Fr(R.randint(1, 99), 1000)])
    m, ee = sci(c * Fr(10) ** e)
    if (c >= 1 and c < 10):
        return None
    return M("Écris en notation scientifique : %s × 10%s" % (d(c), sup(e)), S(m, ee), [S(m, e), S(m, -ee) if ee else S(m, 1), S(c, e - 1) if c < 1 else S(m, ee + (2 if c >= 10 else -2))],
             "%s = %s, donc %s × 10%s = <b>%s</b>." % (d(c), S(m, ee - e), d(c), sup(e), S(m, ee)))


def s4():
    k = R.choice(["ordre", "ordre", "compare", "conv"])
    if k == "ordre":
        m = Fr(R.randint(11, 99), 10)
        e = R.randint(-6, 9)
        oe = e + (1 if m >= 5 else 0)
        return M("Quel est l’ordre de grandeur de %s ?" % S(m, e), "10%s" % sup(oe), ["10%s" % sup(oe - 1 if m >= 5 else oe + 1), "%d × 10%s" % (int(m), sup(e)), "10%s" % sup(-oe) if oe else "10%s" % sup(2)],
                 "On arrondit %s à %s : <b>10%s</b>." % (d(m), "10" if m >= 5 else "1", sup(oe)))
    if k == "compare":
        xs = [(Fr(R.randint(11, 99), 10), R.randint(-3, 5)) for _ in range(3)]
        vals = [m * Fr(10) ** e for m, e in xs]
        if len(set(vals)) < 3:
            return None
        order = [S(*xs[i]) for i in sorted(range(3), key=lambda i: vals[i])]
        byman = [S(*xs[i]) for i in sorted(range(3), key=lambda i: xs[i][0])]
        w = [" &lt; ".join(order[::-1]), " &lt; ".join(byman) if byman != order else " &lt; ".join([order[1], order[0], order[2]]), " &lt; ".join([order[0], order[2], order[1]])]
        return M("Range dans l’ordre croissant : %s." % ", ".join(S(*x) for x in xs), " &lt; ".join(order), w, "On compare d’abord les exposants, puis les nombres devant : <b>%s</b>." % " &lt; ".join(order))
    PF = [("Mo", "octets", 6), ("Go", "octets", 9), ("To", "octets", 12), ("µm", "m", -6), ("nm", "m", -9), ("km", "m", 3)]
    u, b, e = R.choice(PF)
    n = R.randint(2, 900)
    m, ee = sci(n * Fr(10) ** e)
    return M("Convertis %d %s en %s (notation scientifique)." % (n, u, b), S(m, ee) + " " + b, [S(m, ee + 3) + " " + b, S(m, -ee) + " " + b if ee else S(m, 1) + " " + b, S(m, e) + " " + b if e != ee else S(m, ee - 1) + " " + b],
             "1 %s = 10%s %s : %d × 10%s = <b>%s %s</b>." % (u, sup(e), b, n, sup(e), S(m, ee), b))


def s5():
    k = R.choice(["lumiere", "cellules", "disque", "atomes", "eau", "conso", "conso"])
    if k == "conso":
        n = R.choice([100, 120, 140, 150, 160, 180, 200, 250])
        r = Fr(68, 10) * 10 ** 7 * n
        m, e = sci(r)
        return M("Environ 6,8 × 10%s personnes vivent en France. Si chacune utilise %d L d’eau par jour, quel volume est utilisé chaque jour en France ?" % (sup(7), n), S(m, e) + " L", [S(m, e - 1) + " L", S(Fr(68, 10) * n if Fr(68, 10) * n < 10 else Fr(68, 10), 7 + len(str(n)) - 1 if False else 9) + " L" if S(Fr(68, 10), 9) != S(m, e) else S(m, e + 1) + " L", S(m, e + 1) + " L" if S(m, e + 1) != S(Fr(68, 10), 9) else S(m, e + 2) + " L"],
                 "6,8 × 10%s × %d = %s L = <b>%s L</b>." % (sup(7), n, num(r), S(m, e)))
    if k == "lumiere":
        t = R.choice([8, 60, 500, 3600])
        r = 3 * 10 ** 8 * t
        m, e = sci(r)
        return M("La lumière parcourt 3 × 10%s m par seconde. Quelle distance parcourt-elle en %s s ?" % (sup(8), num(t)), S(m, e) + " m", [S(m, e - 1) + " m", S(m, e + 1) + " m", S(3 * t if 3 * t < 10 else 3, 8) + " m" if 3 * t >= 10 else S(m, e + 2) + " m"],
                 "3 × 10%s × %s = %s m = <b>%s m</b>." % (sup(8), num(t), num(r), S(m, e)))
    if k == "cellules":
        return M("Le corps humain contient environ 3 × 10%s cellules, et chacune a environ 2 × 10%s m de diamètre. Si on les alignait, quelle longueur obtiendrait-on ?" % (sup(13), sup(-5)), S(6, 8) + " m", [S(6, -65) + " m", S(5, 8) + " m", S(6, 18) + " m"],
                 "3 × 2 = 6 et 10%s × 10%s = 10%s : <b>6 × 10%s m</b> (600 000 km !)." % (sup(13), sup(-5), sup(8), sup(8)))
    if k == "disque":
        n = R.choice([2, 4, 8, 16])
        f = R.choice([3, 5, 6])
        m, e = sci(Fr(n * 10 ** 12, f * 10 ** 6))
        if (m * 100).denominator != 1:
            return None
        return M("Un disque dur de %d To (1 To = 10%s octets) stocke des photos de %d Mo (1 Mo = 10%s octets). Combien de photos peut-il contenir ?" % (n, sup(12), f, sup(6)), S(m, e), [S(m, e + 6), S(m, e - 1), S(Fr(n * f, 10) if n * f >= 10 else n * f, 6)],
                 "%d × 10%s ÷ (%d × 10%s) = <b>%s</b>." % (n, sup(12), f, sup(6), S(m, e)))
    if k == "atomes":
        g = R.choice([2, 3, 4, 5])
        return M("Une goutte d’eau contient environ 1,5 × 10%s molécules. Combien de molécules dans %d gouttes ?" % (sup(21), g), S(*sci(Fr(15, 10) * g * Fr(10) ** 21)), [S(Fr(15, 10) * g, 21) if Fr(15, 10) * g >= 10 else S(Fr(15, 10) * g, 22), S(Fr(15, 10), 21 * g), S(Fr(15, 10) + g, 21)],
                 "1,5 × %d = %s ; <b>%s</b>." % (g, d(Fr(15, 10) * g), S(*sci(Fr(15, 10) * g * Fr(10) ** 21))))
    v = R.choice([2, 5, 8])
    return M("Un virus mesure %d × 10%s m. Combien de virus faut-il aligner pour faire 1 mm ?" % (v, sup(-8)), S(*sci(Fr(10 ** 5, v))), [S(v, 5), S(*sci(Fr(10 ** 8, v))), S(*sci(Fr(10 ** 4, v)))],
             "1 mm = 10%s m ; 10%s ÷ (%d × 10%s) = <b>%s</b>." % (sup(-3), sup(-3), v, sup(-8), S(*sci(Fr(10 ** 5, v)))))


def main():
    seen = set()
    sets = [("Règles de calcul sur les puissances", mix(R, seen, [(s1, 20)])), ("Exposants négatifs et nuls", mix(R, seen, [(s2, 20)])),
            ("Calculer en notation scientifique", mix(R, seen, [(s3, 20)])), ("Ordres de grandeur et comparaisons", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["a<sup>m</sup> × a<sup>n</sup> = a<sup>m+n</sup> ; a<sup>m</sup> ÷ a<sup>n</sup> = a<sup>m−n</sup> ; (a<sup>m</sup>)<sup>n</sup> = a<sup>m×n</sup> ; a<sup>0</sup> = 1 ; a<sup>−n</sup> = 1 ÷ a<sup>n</sup>.",
              "Notation scientifique : a × 10<sup>n</sup> avec 1 ≤ a &lt; 10. Pour multiplier, on multiplie les nombres devant et on additionne les exposants, puis on ajuste.",
              "L’<b>ordre de grandeur</b> d’un nombre est la puissance de 10 la plus proche."],
             [("(4 × 10<sup>5</sup>) × (5 × 10<sup>−2</sup>)", ["4 × 5 = 20", "10<sup>5</sup> × 10<sup>−2</sup> = 10<sup>3</sup>", "20 × 10<sup>3</sup> = 2 × 10<sup>4</sup>"], "2 × 10<sup>4</sup>")],
             [["a³ × a⁴ = a¹²", "On additionne les exposants : a⁷."], ["2⁻³ = −8", "2⁻³ = 1/8 : un exposant négatif ne rend pas le nombre négatif."],
              ["Laisser 20 × 10³ comme résultat", "20 n’est pas entre 1 et 10 : 2 × 10⁴."]])
    faq = [("Les règles marchent-elles avec des bases différentes ?", "a<sup>m</sup> × a<sup>n</sup> exige la même base. Avec le même exposant : a<sup>n</sup> × b<sup>n</sup> = (ab)<sup>n</sup>."),
           ("À quoi sert l’ordre de grandeur ?", "À vérifier rapidement qu’un résultat est plausible.")]
    unit("3e", R, "puissances-et-notation-scientifique", "N",
         "Utiliser les règles de calcul sur les puissances (produit, quotient, puissance d’une puissance, exposants négatifs) ; calculer en notation scientifique ; estimer un ordre de grandeur ; résoudre des problèmes de sciences",
         "Puissances et notation scientifique", "Puissances et notation scientifique",
         "Fiches de maths 3e sur les puissances : règles de calcul, exposants négatifs, calculs en notation scientifique, ordres de grandeur et problèmes. 100 exercices corrigés.",
         "aᵐ × aⁿ = aᵐ⁺ⁿ ; (aᵐ)ⁿ = aᵐˣⁿ", "Notation scientifique : a × 10ⁿ, 1 ≤ a < 10", body, faq, sets, 2)


if __name__ == "__main__":
    main()
