# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Sommes de termes et limites de suites (1 + 2 + … + n, sommes arithmétiques, 1 + q + … + qⁿ, sommes géométriques, limite intuitive, seuils)
  python3 tools/gen_fr_maths_premiere_sommes_et_limites_de_suites.py
Erreurs : compter n termes au lieu de n + 1 de u₀ à uₙ, oublier de diviser par 2, (qⁿ − 1)/(q − 1) au lieu de (qⁿ⁺¹ − 1)/(q − 1), croire que qⁿ tend vers 0 pour q > 1.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60605)


def s1():
    k = R.choice(["n", "n", "ab", "pair", "impair"])
    if k == "n":
        n = R.randint(10, 200)
        return M("Calcule 1 + 2 + 3 + … + %d." % n, num(n * (n + 1) // 2), [num(n * n), num(n * (n - 1) // 2), num(n * (n + 1)), num(n * (n + 1) // 2 + n)],
                 "1 + 2 + … + n = n(n + 1) ÷ 2 = %d × %d ÷ 2 = <b>%s</b>." % (n, n + 1, num(n * (n + 1) // 2)))
    if k == "ab":
        a, n = R.randint(5, 30), R.randint(40, 120)
        v = n * (n + 1) // 2 - a * (a - 1) // 2
        return M("Calcule %d + %d + … + %d." % (a, a + 1, n), num(v), [num(n * (n + 1) // 2 - a * (a + 1) // 2), num(n * (n + 1) // 2), num((n - a) * (a + n) // 2)],
                 "Il y a %d − %d + 1 = %d termes ; somme = %d × (%d + %d) ÷ 2 = <b>%s</b>." % (n, a, n - a + 1, n - a + 1, a, n, num(v)))
    if k == "pair":
        n = R.randint(10, 80)
        return M("Calcule 2 + 4 + 6 + … + %d." % (2 * n), num(n * (n + 1)), [num(n * (n + 1) // 2), num(2 * n * (2 * n + 1) // 2), num(n * n)],
                 "2 + 4 + … + 2n = 2(1 + 2 + … + n) = n(n + 1) = %d × %d = <b>%s</b>." % (n, n + 1, num(n * (n + 1))))
    n = R.randint(10, 60)
    return M("Calcule 1 + 3 + 5 + … + %d (les %d premiers nombres impairs)." % (2 * n - 1, n), num(n * n), [num(n * (n + 1)), num((2 * n - 1) * 2 * n // 2), num(n * (n - 1))],
             "%d termes, premier 1, dernier %d : %d × (1 + %d) ÷ 2 = <b>%s</b> (= n²)." % (n, 2 * n - 1, n, 2 * n - 1, num(n * n)))


def s2():
    k = R.choice(["u0", "u0", "u1", "ab"])
    u0, r = R.randint(-10, 30), nz(R, -5, 9)
    n = R.randint(8, 40)
    if k == "u0":
        last = u0 + n * r
        S = (n + 1) * (u0 + last) // 2
        return M("(u<sub>n</sub>) est arithmétique avec %s = %s et r = %s. Calcule %s + %s + … + %s." % (U(0), d(u0), d(r), U(0), U(1), U(n)), num(S) if S >= 0 else d(S),
                 [d(Fr(n * (u0 + last), 2)), d(Fr((n + 1) * (u0 + u0 + (n - 1) * r), 2)), d((n + 1) * (u0 + last)), d(S + last)],
                 "%s = %s ; il y a %d termes : S = %d × (%s + %s) ÷ 2 = <b>%s</b>." % (U(n), d(last), n + 1, n + 1, d(u0), par(last), d(S)))
    if k == "u1":
        last = u0 + (n - 1) * r
        S = Fr(n * (u0 + last), 2)
        return M("(u<sub>n</sub>) est arithmétique avec %s = %s et r = %s. Calcule %s + %s + … + %s." % (U(1), d(u0), d(r), U(1), U(2), U(n)), d(S),
                 [d(Fr((n + 1) * (u0 + last), 2)), d(Fr(n * (u0 + u0 + n * r), 2)), d(n * (u0 + last)), d(S - last)],
                 "%s = %s ; %d termes : S = %d × (%s + %s) ÷ 2 = <b>%s</b>." % (U(n), d(last), n, n, d(u0), par(last), d(S)))
    a, b = R.randint(3, 20), R.randint(3, 9)
    m = R.randint(6, 20)
    last = a + (m - 1) * b
    return M("Calcule la somme %d + %d + %d + … + %d (on ajoute %d à chaque fois)." % (a, a + b, a + 2 * b, last, b), num(m * (a + last) // 2) if m * (a + last) % 2 == 0 else d(Fr(m * (a + last), 2)),
             [d(Fr((m + 1) * (a + last), 2)), d(m * (a + last)), d(Fr((m - 1) * (a + last), 2))],
             "Nombre de termes : (%d − %d) ÷ %d + 1 = %d ; somme = %d × (%d + %d) ÷ 2 = <b>%s</b>." % (last, a, b, m, m, a, last, d(Fr(m * (a + last), 2))))


def s3():
    k = R.choice(["2", "3", "half", "q"])
    n = R.randint(4, 10)
    if k == "2":
        return M("Calcule 1 + 2 + 2² + … + 2<sup>%d</sup>." % n, num(2 ** (n + 1) - 1), [num(2 ** n - 1), num(2 ** (n + 1)), num(2 * n + 1), num(2 ** (n + 1) + 1)],
                 "1 + q + … + q<sup>n</sup> = (q<sup>n+1</sup> − 1) ÷ (q − 1) = 2<sup>%d</sup> − 1 = <b>%s</b>." % (n + 1, num(2 ** (n + 1) - 1)))
    if k == "3":
        n = R.randint(3, 7)
        return M("Calcule 1 + 3 + 3² + … + 3<sup>%d</sup>." % n, num((3 ** (n + 1) - 1) // 2), [num((3 ** n - 1) // 2), num(3 ** (n + 1) - 1), num((3 ** (n + 1) - 1) // 3)],
                 "(3<sup>%d</sup> − 1) ÷ (3 − 1) = (%s − 1) ÷ 2 = <b>%s</b>." % (n + 1, num(3 ** (n + 1)), num((3 ** (n + 1) - 1) // 2)))
    if k == "half":
        n = R.randint(3, 8)
        v = 2 - Fr(1, 2 ** n)
        return M("Calcule 1 + ½ + ¼ + … + (½)<sup>%d</sup>." % n, fq(v), [fq(2 - Fr(1, 2 ** (n + 1))), "2", fq(Fr(n + 1, 2)), fq(1 - Fr(1, 2 ** (n + 1)))],
                 "(1 − (½)<sup>%d</sup>) ÷ (1 − ½) = 2 − (½)<sup>%d</sup> = <b>%s</b>." % (n + 1, n, fq(v)))
    q = R.choice([2, 3, 4, 5, 10])
    n = R.randint(3, 6)
    return M("Quelle formule donne 1 + %d + %d² + … + %d<sup>%d</sup> ?" % (q, q, q, n), "(%d<sup>%d</sup> − 1) ÷ %d" % (q, n + 1, q - 1),
             ["(%d<sup>%d</sup> − 1) ÷ %d" % (q, n, q - 1), "(%d<sup>%d</sup> − 1) ÷ %d" % (q, n + 1, q), "%d × (%d + 1) ÷ 2" % (n, n), "(%d<sup>%d</sup> + 1) ÷ %d" % (q, n + 1, q - 1)],
             "Il y a %d termes (de q⁰ à q<sup>%d</sup>) : (q<sup>n+1</sup> − 1) ÷ (q − 1) = <b>(%d<sup>%d</sup> − 1) ÷ %d</b>." % (n + 1, n, q, n + 1, q - 1))


def s4():
    k = R.choice(["u0", "u0", "epargne", "echiquier", "salaire"])
    if k == "u0":
        u0, q, n = R.randint(1, 6), R.choice([2, 3]), R.randint(3, 7)
        S = u0 * (q ** (n + 1) - 1) // (q - 1)
        return M("(u<sub>n</sub>) est géométrique avec %s = %d et q = %d. Calcule %s + %s + … + %s." % (U(0), u0, q, U(0), U(1), U(n)), num(S),
                 [num(u0 * (q ** n - 1) // (q - 1)), num((q ** (n + 1) - 1) // (q - 1)), num(u0 * q ** n), num(u0 * (q ** (n + 1) - 1))],
                 "S = %s × (q<sup>%d</sup> − 1) ÷ (q − 1) = %d × (%s − 1) ÷ %d = <b>%s</b>." % (U(0), n + 1, u0, num(q ** (n + 1)), q - 1, num(S)))
    if k == "epargne":
        a, n = R.randint(1, 5) * 10, R.randint(4, 7)
        S = a * (2 ** n - 1)
        return M("Tom met %d € de côté le 1<sup>er</sup> mois, puis double la somme chaque mois. Combien a-t-il mis de côté en tout au bout de %d mois ?" % (a, n), euro(S),
                 [euro(a * 2 ** (n - 1)), euro(a * (2 ** (n + 1) - 1)), euro(a * 2 * n), euro(a * 2 ** n)], "%d × (1 + 2 + … + 2<sup>%d</sup>) = %d × (2<sup>%d</sup> − 1) = <b>%s</b>." % (a, n - 1, a, n, euro(S)))
    if k == "echiquier":
        n = R.randint(5, 12)
        return M("On pose 1 grain de riz sur la case 1, 2 sur la case 2, 4 sur la case 3, et on double à chaque case. Combien de grains en tout sur les %d premières cases ?" % n, num(2 ** n - 1),
                 [num(2 ** (n - 1)), num(2 ** n), num(2 ** (n + 1) - 1), num(n * (n + 1) // 2)], "1 + 2 + … + 2<sup>%d</sup> = 2<sup>%d</sup> − 1 = <b>%s</b>." % (n - 1, n, num(2 ** n - 1)))
    a, t, n = R.randint(20, 30) * 1000, R.choice([2, 5, 10]), R.randint(2, 4)
    q = 1 + Fr(t, 100)
    S = a * (q ** n - 1) / (q - 1)
    return M("Un salaire annuel de %s € augmente de %d %% chaque année. Combien gagne-t-on au total sur les %d premières années ?" % (num(a), t, n), euro(S),
             [euro(a * q ** (n - 1)), euro(a * n), euro(a * (q ** (n + 1) - 1) / (q - 1))], "%s × (%s<sup>%d</sup> − 1) ÷ (%s − 1) = <b>%s</b>." % (num(a), d(q), n, d(q), euro(S)))


def s5():
    k = R.choice(["lim", "lim", "lim", "seuil2", "seuil_q", "algo"])
    if k == "lim":
        a = R.randint(1, 9)
        q = R.choice(["0,5", "0,8", "0,9", "1,1", "2", "1,05", "0,3"])
        L_ = [("%d + 1/n" % a, d(a), ["+∞", "0", d(a + 1)]),
              ("%d − 1/n²" % a, d(a), ["+∞", "0", d(a - 1)]),
              ("%s<sup>n</sup>" % q, "0" if q.startswith("0") else "+∞", ["+∞" if q.startswith("0") else "0", "1", q]),
              ("%d × %s<sup>n</sup>" % (a, q), "0" if q.startswith("0") else "+∞", ["+∞" if q.startswith("0") else "0", d(a), q]),
              ("n² − %dn" % a, "+∞", ["0", MINUS + "∞", d(-a)]),
              ("%d − %s<sup>n</sup>" % (a, q) if q.startswith("0") else "%d − n" % a, d(a) if q.startswith("0") else MINUS + "∞", ["0", "+∞", d(a - 1)] if q.startswith("0") else ["0", "+∞", d(a)]),
              ("(−1)<sup>n</sup>", "pas de limite", ["0", "1", MINUS + "1"])]
        ex, ans, w = R.choice(L_)
        return M("Conjecture la limite de la suite %s = %s quand n tend vers +∞." % (U("n"), ex), ans, w,
                 "Avec de grandes valeurs de n (tableur ou calculatrice), %s se rapproche de <b>%s</b>." % (U("n"), ans) if ans != "pas de limite" else "Les termes valent 1, −1, 1, −1… : la suite n’a <b>pas de limite</b>.")
    if k == "seuil2":
        S = R.choice([100, 500, 1000, 5000, 10000, 50000])
        n = math.ceil(math.log(S + 1, 2))
        while 2 ** n <= S:
            n += 1
        return M("Quel est le plus petit entier n tel que 2<sup>n</sup> &gt; %s ?" % num(S), str(n), [str(n - 1), str(n + 1), str(S // 2)],
                 "2<sup>%d</sup> = %s ⩽ %s et 2<sup>%d</sup> = %s &gt; %s : <b>n = %d</b>." % (n - 1, num(2 ** (n - 1)), num(S), n, num(2 ** n), num(S), n))
    if k == "seuil_q":
        q = R.choice([Fr(9, 10), Fr(8, 10), Fr(1, 2), Fr(7, 10)])
        s_ = R.choice([Fr(1, 10), Fr(1, 100), Fr(5, 100)])
        n = 0
        while q ** n >= s_:
            n += 1
        return M("Quel est le plus petit entier n tel que %s<sup>n</sup> &lt; %s ?" % (d(q), d(s_)), str(n), [str(n - 1), str(n + 1), str(int(1 / s_))],
                 "%s<sup>%d</sup> ≈ %s et %s<sup>%d</sup> ≈ %s : <b>n = %d</b>." % (d(q), n - 1, d(round(float(q ** (n - 1)), 4)), d(q), n, d(round(float(q ** n), 4)), n))
    u0, q, s_ = R.randint(1, 9) * 100, R.choice([2, 3]), R.choice([5000, 10000, 20000])
    n, u = 0, u0
    while u <= s_:
        u *= q
        n += 1
    return M("Que renvoie ce programme ?%s" % code("u = %d" % u0, "n = 0", "while u <= %d:" % s_, "    u = %d * u" % q, "    n = n + 1", "print(n)"), str(n), [str(n - 1), str(n + 1), str(u)],
             "u prend les valeurs %s ; la boucle s’arrête quand u &gt; %s : <b>n = %d</b>." % (", ".join(num(u0 * q ** i) for i in range(n + 1)), num(s_), n))


def main():
    seen = set()
    sets = [("1 + 2 + … + n", mix(R, seen, [(s1, 20)])), ("Sommes de termes arithmétiques", mix(R, seen, [(s2, 20)])),
            ("1 + q + … + qⁿ", mix(R, seen, [(s3, 20)])), ("Sommes géométriques en situation", mix(R, seen, [(s4, 20)])), ("Limites et seuils", mix(R, seen, [(s5, 20)]))]
    body = L(["1 + 2 + … + n = n(n + 1) ÷ 2. Pour une suite arithmétique : somme = nombre de termes × (premier + dernier) ÷ 2.",
              "Pour q ≠ 1 : 1 + q + q² + … + q<sup>n</sup> = (q<sup>n+1</sup> − 1) ÷ (q − 1). Pour une suite géométrique : u<sub>0</sub> + … + u<sub>n</sub> = u<sub>0</sub> × (q<sup>n+1</sup> − 1) ÷ (q − 1).",
              "De u<sub>0</sub> à u<sub>n</sub>, il y a <b>n + 1</b> termes. Si q &gt; 1, q<sup>n</sup> tend vers +∞ ; si 0 &lt; q &lt; 1, q<sup>n</sup> tend vers 0."],
             [("1 + 3 + 3² + 3³", ["(3<sup>4</sup> − 1) ÷ (3 − 1) = 80 ÷ 2"], "40"), ("u<sub>0</sub> = 5, r = 2 ; somme de u<sub>0</sub> à u<sub>10</sub>", ["u<sub>10</sub> = 25 ; 11 termes", "11 × (5 + 25) ÷ 2"], "165")],
             [["De u<sub>0</sub> à u<sub>10</sub>, il y a 10 termes", "Il y en a 11."], ["1 + 2 + … + 2<sup>5</sup> = 2<sup>5</sup> − 1", "Il y a 6 termes : 2<sup>6</sup> − 1 = 63."],
              ["0,9<sup>n</sup> tend vers +∞ car on multiplie sans arrêt", "Multiplier par 0,9 fait diminuer : 0,9<sup>n</sup> tend vers 0."]])
    faq = [("Pourquoi 1 + 2 + … + n = n(n + 1) ÷ 2 ?", "On écrit la somme à l’endroit et à l’envers : chaque colonne vaut n + 1 et il y a n colonnes, donc 2S = n(n + 1)."),
           ("Comment trouver un seuil avec Python ?", "Avec une boucle while : tant que la condition n’est pas atteinte, on calcule le terme suivant et on augmente n de 1.")]
    unit("premiere", R, "sommes-et-limites-de-suites", "A",
         "Calculer la somme des n premiers entiers et la somme 1 + q + … + qⁿ ; calculer des sommes de termes de suites arithmétiques et géométriques ; approche intuitive de la limite d’une suite ; déterminer un seuil par un algorithme",
         "Sommes de termes et limites de suites", "Sommes et limites de suites",
         "Fiches de maths première sur les sommes de termes et les limites de suites : 1 + 2 + … + n, sommes arithmétiques et géométriques, limite intuitive et seuils en Python. 100 exercices corrigés.",
         "1 + q + … + q^n = (q^(n+1) − 1) ÷ (q − 1)", "De u(0) à u(n) : n + 1 termes", body, faq, sets, 5)


if __name__ == "__main__":
    main()
