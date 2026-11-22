# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Suites géométriques (raison, terme général, évolutions en pourcentage, sens de variation, problèmes)
  python3 tools/gen_fr_maths_premiere_suites_geometriques.py
Erreurs : u(n) = u(0) × q × n, (u(0) × q)ⁿ au lieu de u(0) × qⁿ, raison 0,05 au lieu de 1,05 pour +5 %, croire que la suite est croissante dès que q > 1 quel que soit u(0).
"""
import random
from fr_ly1 import *

R = random.Random(60604)


def terms(u0, q, k=4):
    return " ; ".join("%s = %s" % (U(i), fq(u0 * Fr(q) ** i)) for i in range(k))


def s1():
    k = R.choice(["raison", "raison", "est", "suivant"])
    u0, q = nz(R, -6, 8), R.choice([2, 3, -2, -3, Fr(1, 2), 4, 5])
    if Fr(q).denominator == 2 and u0 % 8:
        u0 *= 8
    if k == "raison":
        return M("Une suite géométrique vérifie %s. Quelle est sa raison ?" % terms(u0, q), fq(q), [fq(u0 * q - u0), fq(1 / Fr(q)), fq(-Fr(q)), fq(u0)],
                 "q = %s ÷ %s = <b>%s</b> (terme suivant divisé par terme précédent)." % (U(1), U(0), fq(q)))
    if k == "suivant":
        t = [u0 * Fr(q) ** i for i in range(6)]
        return M("Une suite géométrique a pour premiers termes %s. Que vaut %s ?" % (terms(u0, q, 3), U(4)), fq(t[4]), [fq(t[3]), fq(t[5]), fq(t[2] + 2 * (t[1] - t[0])), fq(t[2] * 2 * q)],
                 "q = %s, donc %s = %s × %s² = <b>%s</b>." % (fq(q), U(4), fq(t[2]), par(q) if Fr(q).denominator == 1 else "(" + fq(q) + ")", fq(t[4])))
    a = R.randint(1, 4)
    qq = R.choice([2, 3])
    good = "%d ; %d ; %d ; %d" % (a, a * qq, a * qq * qq, a * qq ** 3)
    return M("Laquelle de ces listes peut être le début d’une suite géométrique ?", good,
             ["%d ; %d ; %d ; %d" % (a, a + qq, a + 2 * qq, a + 3 * qq), "%d ; %d ; %d ; %d" % (a, a * qq, a * qq + qq, a * qq * qq + qq), "%d ; %d ; %d ; %d" % (a * a, (a + 1) ** 2, (a + 2) ** 2, (a + 3) ** 2)],
             "On multiplie toujours par %d : <b>%s</b>." % (qq, good))


def s2():
    k = R.choice(["u0", "u0", "u1", "expr", "up"])
    u0, q = R.randint(1, 9) * R.choice([1, -1]), R.choice([2, 3, -2, Fr(1, 2), Fr(3, 2)])
    n = R.randint(3, 6)
    if Fr(q).denominator == 2:
        u0 = u0 * 2 ** n
    if k == "u0":
        return M("(u<sub>n</sub>) est géométrique de premier terme %s = %s et de raison %s. Calcule %s." % (U(0), d(u0), fq(q), U(n)), fq(u0 * Fr(q) ** n),
                 [fq(u0 * Fr(q) ** (n - 1)), fq(u0 * q * n), fq((u0 * Fr(q)) ** n) if abs((u0 * Fr(q)) ** n) < 10 ** 5 else None, fq(u0 + n * q), fq(-u0 * Fr(q) ** n), fq(u0 * Fr(q) ** (n + 1))],
                 "%s = %s × q<sup>n</sup> = %s × %s<sup>%d</sup> = <b>%s</b>." % (U("n"), U(0), d(u0), par(q) if Fr(q).denominator == 1 else "(" + fq(q) + ")", n, fq(u0 * Fr(q) ** n)))
    if k == "u1":
        return M("(u<sub>n</sub>) est géométrique avec %s = %s et q = %s (la suite commence à %s). Calcule %s." % (U(1), d(u0), fq(q), U(1), U(n)), fq(u0 * Fr(q) ** (n - 1)),
                 [fq(u0 * Fr(q) ** n), fq(u0 * q * (n - 1)), fq(u0 * Fr(q) ** (n + 1))], "%s = %s × q<sup>n−1</sup> = <b>%s</b>." % (U(n), U(1), fq(u0 * Fr(q) ** (n - 1))))
    if k == "up":
        p = R.randint(2, 4)
        m = p + R.randint(2, 3)
        return M("(u<sub>n</sub>) est géométrique avec %s = %s et q = %s. Calcule %s." % (U(p), d(u0), fq(q), U(m)), fq(u0 * Fr(q) ** (m - p)),
                 [fq(u0 * Fr(q) ** m), fq(u0 * Fr(q) ** (m - p - 1)), fq(u0 * q * (m - p)), fq(u0 * Fr(q) ** (m - p + 1)), fq(u0 + (m - p) * q)], "%s = %s × q<sup>%d − %d</sup> = %s × %s<sup>%d</sup> = <b>%s</b>." % (U(m), U(p), m, p, d(u0), par(q) if Fr(q).denominator == 1 else "(" + fq(q) + ")", m - p, fq(u0 * Fr(q) ** (m - p))))
    qs = d(q) if Fr(q) > 0 else par(q)
    ans = "%s = %s × %s<sup>n</sup>" % (U("n"), d(u0), qs)
    return M("(u<sub>n</sub>) est géométrique de premier terme %s = %s et de raison %s. Quelle est son expression ?" % (U(0), d(u0), d(q) if Fr(q).denominator in (1, 2) else fq(q)), ans,
             ["%s = %s × %s<sup>n</sup>" % (U("n"), qs, d(u0) if u0 > 0 else par(u0)), "%s = %s + %sn" % (U("n"), d(u0), d(q) if Fr(q) > 0 else "(" + d(q) + ")"), "%s = (%s × %s)<sup>n</sup>" % (U("n"), d(u0), qs), "%s = %s × %s<sup>n−1</sup>" % (U("n"), d(u0), qs)],
             "%s = %s × q<sup>n</sup> : <b>%s</b>." % (U("n"), U(0), ans))


def s3():
    k = R.choice(["evol", "evol", "baisse", "find_t", "q2"])
    t = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
    if k == "evol":
        return M("Une quantité augmente de %d %% chaque année. On note %s sa valeur après n années. La suite est géométrique de raison :" % (t, U("n")), d(1 + Fr(t, 100)), [d(Fr(t, 100)), str(t), d(1 - Fr(t, 100)), d(Fr(100 + t, 10))],
                 "Augmenter de %d %% revient à multiplier par 1 + %s = <b>%s</b>." % (t, d(Fr(t, 100)), d(1 + Fr(t, 100))))
    if k == "baisse":
        return M("Une quantité diminue de %d %% chaque mois. Quelle est la raison de la suite géométrique associée ?" % t, d(1 - Fr(t, 100)), [d(Fr(t, 100)), d(1 + Fr(t, 100)), MINUS + d(Fr(t, 100)), d(Fr(100 - t, 10))],
                 "Diminuer de %d %% revient à multiplier par 1 − %s = <b>%s</b>." % (t, d(Fr(t, 100)), d(1 - Fr(t, 100))))
    if k == "find_t":
        q = 1 + Fr(t, 100) * R.choice([1, -1])
        return M("Une suite géométrique a pour raison %s. Quelle évolution en pourcentage cela représente-t-il à chaque étape ?" % d(q), ("+" if q > 1 else MINUS) + " %d %%" % t,
                 [("+" if q > 1 else MINUS) + " %s %%" % d(q * 100), ("+" if q < 1 else MINUS) + " %d %%" % t, ("+" if q > 1 else MINUS) + " %s %%" % d(Fr(t, 10))],
                 "q = %s = 1 %s %s : %s de <b>%d %%</b>." % (d(q), "+" if q > 1 else MINUS, d(Fr(t, 100)), "hausse" if q > 1 else "baisse", t))
    u0 = R.randint(2, 9) * 100
    q = 1 + Fr(t, 100)
    return M("Un capital de %d € augmente de %d %% par an (intérêts composés). Quelle est sa valeur au bout de 2 ans ?" % (u0, t), euro(u0 * q * q),
             [euro(u0 * (1 + Fr(2 * t, 100))), euro(u0 * q), euro(u0 * Fr(t, 100) ** 2 + u0)], "%d × %s² = <b>%s</b> (et non + %d %%)." % (u0, d(q), euro(u0 * q * q), 2 * t))


def s4():
    k = R.choice(["var", "var", "neg", "alt", "expo"])
    u0 = R.randint(1, 9)
    q = R.choice([Fr(1, 2), Fr(3, 4), 2, 3, Fr(3, 2), Fr(9, 10), Fr(11, 10)])
    if k == "var":
        ans = "croissante" if q > 1 else "décroissante"
        return M("(u<sub>n</sub>) est géométrique avec %s = %d &gt; 0 et q = %s. Quel est son sens de variation ?" % (U(0), u0, d(q)), ans, ["décroissante" if q > 1 else "croissante", "constante", "ni croissante ni décroissante"],
                 "u<sub>0</sub> &gt; 0 et q %s 1 : la suite est <b>%s</b>." % ("&gt;" if q > 1 else "&lt;", ans))
    if k == "neg":
        ans = "décroissante" if q > 1 else "croissante"
        return M("(u<sub>n</sub>) est géométrique avec %s = %s &lt; 0 et q = %s. Quel est son sens de variation ?" % (U(0), d(-u0), d(q)), ans, ["croissante" if q > 1 else "décroissante", "constante", "ni croissante ni décroissante"],
                 "u<sub>n+1</sub> − u<sub>n</sub> = u<sub>n</sub>(q − 1) : u<sub>n</sub> &lt; 0 et q − 1 %s 0, donc la suite est <b>%s</b>." % ("&gt;" if q > 1 else "&lt;", ans))
    if k == "alt":
        qq = R.choice([-2, -3, Fr(-1, 2)])
        return M("(u<sub>n</sub>) est géométrique avec %s = %d et q = %s. Quel est son sens de variation ?" % (U(0), u0, d(qq)), "ni croissante ni décroissante", ["croissante", "décroissante", "constante"],
                 "q &lt; 0 : les termes changent de signe à chaque rang, la suite <b>n’est ni croissante ni décroissante</b>.")
    a = R.choice([2, 3, 5, Fr(1, 2)])
    return M("Montre que %s = %d × %s<sup>n</sup> est géométrique : %s ÷ %s vaut" % (U("n"), u0, d(a) if Fr(a).denominator == 1 else "0,5", U("n+1"), U("n")), d(a), [str(u0), d(a * u0), d(a + 1)],
             "%s ÷ %s = (%d × %s<sup>n+1</sup>) ÷ (%d × %s<sup>n</sup>) = <b>%s</b> : raison %s." % (U("n+1"), U("n"), u0, d(a), u0, d(a), d(a), d(a)))


def s5():
    k = R.choice(["pop", "voiture", "bact", "bal", "abonn"])
    if k == "pop":
        u0, t, n = R.randint(10, 60) * 1000, R.choice([2, 3, 5]), R.randint(2, 3)
        q = 1 + Fr(t, 100)
        v = u0 * q ** n
        return M("Une ville compte %s habitants en 2025 et sa population augmente de %d %% par an. Combien d’habitants en %d (arrondi à l’unité) ?" % (num(u0), t, 2025 + n), num(int(v + Fr(1, 2))),
                 [num(int(u0 * (1 + Fr(t * n, 100)))), num(int(u0 * q ** (n - 1) + Fr(1, 2))), num(int(u0 * q ** (n + 1) + Fr(1, 2)))], "%s × %s<sup>%d</sup> ≈ <b>%s</b>." % (num(u0), d(q), n, num(int(v + Fr(1, 2)))))
    if k == "voiture":
        u0, t, n = R.randint(15, 40) * 1000, R.choice([10, 15, 20]), R.randint(2, 3)
        q = 1 - Fr(t, 100)
        v = u0 * q ** n
        return M("Une voiture achetée %s € perd %d %% de sa valeur chaque année. Quelle est sa valeur au bout de %d ans ?" % (num(u0), t, n), euro(v),
                 [euro(u0 * (1 - Fr(t * n, 100))), euro(u0 * q ** (n - 1)), euro(u0 * Fr(t, 100) ** n)], "%s × %s<sup>%d</sup> = <b>%s</b>." % (num(u0), d(q), n, euro(v)))
    if k == "bact":
        u0, h = R.randint(2, 9) * 100, R.randint(3, 8)
        return M("Une population de %d bactéries double toutes les heures. Combien y en a-t-il au bout de %d heures ?" % (u0, h), num(u0 * 2 ** h), [num(u0 * 2 * h), num(u0 * 2 ** (h - 1)), num(u0 + 2 ** h)],
                 "%d × 2<sup>%d</sup> = <b>%s</b>." % (u0, h, num(u0 * 2 ** h)))
    if k == "bal":
        h, p, n = R.choice([1, 2, 3, 4]), R.choice([Fr(1, 2), Fr(3, 4), Fr(4, 5), Fr(3, 5)]), R.randint(2, 4)
        h0 = h * p.denominator ** n
        if h0 > 400:
            return None
        return M("On lâche une balle de %d cm. À chaque rebond, elle remonte aux %s de sa hauteur précédente. Quelle hauteur atteint-elle après le %s rebond ?" % (h0, fq(p), {2: "2<sup>e</sup>", 3: "3<sup>e</sup>", 4: "4<sup>e</sup>"}[n]),
                 d(h0 * p ** n) + NB + "cm", [d(h0 * p ** (n - 1)) + NB + "cm", d(h0 * p ** (n + 1)) + NB + "cm", d(h0 * (1 - p) ** n) + NB + "cm", d(h0 * p) + NB + "cm", d(h0 - n * h0 * (1 - p)) + NB + "cm" if h0 - n * h0 * (1 - p) > 0 else d(h0 * p ** (n + 1)) + NB + "cm", d(h0 * p * n) + NB + "cm" if h0 * p * n < h0 else d(h0 * p ** (n + 1)) + NB + "cm"],
                 "%d × (%s)<sup>%d</sup> = <b>%s cm</b>." % (h0, fq(p), n, d(h0 * p ** n)))
    u0, t = R.randint(2, 8) * 1000, R.choice([10, 20, 25])
    q = 1 + Fr(t, 100)
    return M("Un site a %s abonnés. Le nombre d’abonnés augmente de %d %% par mois. Quelle relation donne %s, le nombre d’abonnés après n mois ?" % (num(u0), t, U("n")), "%s = %s × %s<sup>n</sup>" % (U("n"), num(u0), d(q)),
             ["%s = %s + %dn" % (U("n"), num(u0), t), "%s = %s × %s<sup>n</sup>" % (U("n"), num(u0), d(Fr(t, 100))), "%s = %s × %s × n" % (U("n"), num(u0), d(q))],
             "On multiplie par %s chaque mois : <b>%s = %s × %s<sup>n</sup></b>." % (d(q), U("n"), num(u0), d(q)))


def main():
    seen = set()
    sets = [("Reconnaître une suite géométrique", mix(R, seen, [(s1, 20)])), ("Terme général", mix(R, seen, [(s2, 20)])),
            ("Évolutions en pourcentage", mix(R, seen, [(s3, 20)])), ("Sens de variation", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une suite est <b>géométrique</b> quand on passe d’un terme au suivant en multipliant toujours par le même nombre q (la raison) : u<sub>n+1</sub> = q × u<sub>n</sub>.",
              "Terme général : u<sub>n</sub> = u<sub>0</sub> × q<sup>n</sup>, et u<sub>n</sub> = u<sub>p</sub> × q<sup>n−p</sup>.",
              "Une hausse de t % donne q = 1 + t/100 ; une baisse de t % donne q = 1 − t/100.",
              "Si u<sub>0</sub> &gt; 0 : q &gt; 1 croissante, 0 &lt; q &lt; 1 décroissante. Si q &lt; 0, la suite n’est pas monotone."],
             [("Un capital de 2 000 € placé à 3 % par an", ["u<sub>n</sub> = 2 000 × 1,03<sup>n</sup>", "u<sub>5</sub> = 2 000 × 1,03<sup>5</sup> ≈ 2 318,55"], "environ 2 318,55 € après 5 ans")],
             [["u<sub>n</sub> = u<sub>0</sub> × q × n", "La raison est en exposant : u<sub>0</sub> × q<sup>n</sup>."], ["+ 5 % : q = 0,05", "q = 1,05."],
              ["Deux hausses de 10 % font + 20 %", "1,1² = 1,21 : c’est + 21 %."], ["q &gt; 1 donc croissante, toujours", "Si u<sub>0</sub> &lt; 0 et q &gt; 1, la suite est décroissante."]])
    faq = [("Comment montrer qu’une suite est géométrique ?", "On montre que u<sub>n+1</sub> = q × u<sub>n</sub> pour tout n (ou, si les termes ne s’annulent pas, que u<sub>n+1</sub> ÷ u<sub>n</sub> est constant)."),
           ("Quel lien avec l’exponentielle ?", "u<sub>n</sub> = u<sub>0</sub> × q<sup>n</sup> décrit une croissance (ou décroissance) exponentielle en temps discret : c’est le pendant des fonctions x ↦ a × e<sup>kx</sup>.")]
    unit("premiere", R, "suites-geometriques", "A",
         "Suites géométriques : relation de récurrence, terme général, sens de variation ; lien avec les évolutions en pourcentage successives et la croissance exponentielle ; modéliser une évolution à taux constant",
         "Suites géométriques : raison, terme général et pourcentages", "Suites géométriques",
         "Fiches de maths première sur les suites géométriques : raison, terme général, évolutions en pourcentage, intérêts composés, sens de variation et problèmes. 100 exercices corrigés.",
         "Suite géométrique : u(n) = u(0) × q^n", "Hausse de t % : q = 1 + t/100", body, faq, sets, 4)


if __name__ == "__main__":
    main()
