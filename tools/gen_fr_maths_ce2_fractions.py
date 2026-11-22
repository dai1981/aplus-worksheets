# -*- coding: utf-8 -*-
"""
France Maths CE2 : Les fractions (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_fractions.py
Fractions de dénominateur 2, 3, 4, 5, 6, 8, 10 : lire sur une figure, nommer, placer sur une droite graduée, comparer
(à 1, même dénominateur, même numérateur), fractions égales à 1/2 ou à 1, fraction d’une quantité.
Erreurs : inverser numérateur et dénominateur, compter les parts blanches, croire que 1/8 > 1/4 parce que 8 > 4.
"""
import random
from fr_common import mcq, lesson, example, make_unit, mix, Kids, fr, bande, disque, droite_frac, table

R = random.Random(51009)
K = Kids(R)
DEN = [2, 3, 4, 5, 6, 8, 10]
NOM = {2: ("demi", "demis"), 3: ("tiers", "tiers"), 4: ("quart", "quarts"), 5: ("cinquième", "cinquièmes"),
       6: ("sixième", "sixièmes"), 8: ("huitième", "huitièmes"), 10: ("dixième", "dixièmes")}
NUMW = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze"]


def mot(n, d):
    w = NOM[d][0 if n == 1 else 1]
    return ("un " if n == 1 else NUMW[n] + " ") + w if not (n == 1 and d == 2) else "un demi"


def s1_figure():
    d = R.choice(DEN)
    k = R.randint(1, d - 1)
    pic = bande(d, k) if R.random() < 0.5 else disque(d, k)
    return mcq("<div class='qfig'>%s</div>Quelle fraction de la figure est coloriée ?" % pic, fr(k, d),
               [fr(d, k), fr(d - k, d) if d - k != k else fr(k, d + 1), fr(k, d - k) if d - k != k and d - k > 0 else fr(k + 1, d), fr(k, d + 2)],
               "La figure est partagée en %d parts égales (le dénominateur) ; %d sont coloriées (le numérateur) : <b>%s</b>." % (d, k, fr(k, d)))


def s1_mot():
    d = R.choice(DEN)
    k = R.randint(1, d - 1)
    return mcq("Comment s’écrit « %s » ?" % mot(k, d), fr(k, d), [fr(d, k), fr(k, d + 1) if d + 1 in NOM else fr(k, d - 1), fr(k + 1, d) if k + 1 < d else fr(k - 1, d) if k > 1 else fr(1, d + 2)],
                "« %s » : on partage en %d et on prend %d parts : <b>%s</b>." % (mot(k, d), d, k, fr(k, d)))


def s2_droite():
    d = R.choice([2, 3, 4, 5, 6, 8, 10])
    k = R.randint(1, 2 * d - 1)
    if k % d == 0:
        return None
    pic = droite_frac(d, 2, [(k, "A")])
    return mcq("<div class='qfig'>%s</div>Quelle fraction est repérée par la lettre A ?" % pic, fr(k, d),
               [fr(k, 2 * d), fr(k + 1, d), fr(k - 1, d) if k > 1 else fr(k + 2, d), fr(d, k) if d != k else None],
               "Chaque unité est partagée en %d. A est à %d graduations de 0 : <b>%s</b>." % (d, k, fr(k, d)))


def s3_cmp_un():
    d = R.choice(DEN)
    k = R.choice([x for x in range(1, 2 * d + 1) if x != d])
    right = "plus petite que 1" if k < d else "plus grande que 1"
    return mcq("La fraction %s est-elle plus petite ou plus grande que 1 ?" % fr(k, d), right,
               ["plus grande que 1" if k < d else "plus petite que 1", "égale à 1", "on ne peut pas savoir"],
               "1 = %s. %s %s %s, donc %s est <b>%s</b>." % (fr(d, d), fr(k, d), "&lt;" if k < d else "&gt;", fr(d, d), fr(k, d), right))


def s3_meme_den():
    d = R.choice([4, 5, 6, 8, 10])
    a, b = R.sample(range(1, d), 2)
    g = max(a, b)
    return mcq("Quelle est la plus grande fraction : %s ou %s ?" % (fr(a, d), fr(b, d)), fr(g, d), [fr(min(a, b), d), "elles sont égales", "on ne peut pas savoir"],
               "Même dénominateur : les parts ont la même taille. %d parts, c’est plus que %d : <b>%s</b>." % (g, min(a, b), fr(g, d)))


def s3_meme_num():
    a, b = R.sample(DEN, 2)
    n = 1 if R.random() < 0.6 else R.choice([x for x in range(2, 4) if x < min(a, b)] or [1])
    big = min(a, b)
    return mcq("Quelle est la plus grande fraction : %s ou %s ?" % (fr(n, a), fr(n, b)), fr(n, big), [fr(n, max(a, b)), "elles sont égales", "on ne peut pas savoir"],
               "Même numérateur : plus on partage en beaucoup de parts, plus les parts sont petites. Une part sur %d est plus grande qu’une part sur %d : <b>%s</b>." % (big, max(a, b), fr(n, big)))


def s4_demi():
    d = R.choice([4, 6, 8, 10])
    n = d // 2
    if R.random() < 0.5:
        return mcq("Complète : %s = %s" % (fr(1, 2), fr("…", d)), n, [n + 1, n - 1, d, 2],
                   "%s, c’est la moitié : la moitié de %d parts, c’est <b>%d</b> parts. %s = %s." % (fr(1, 2), d, n, fr(n, d), fr(1, 2)))
    h = R.randint(1, d - 1)
    if h == n:
        return None
    others = [fr(h, d), fr(n, d + 2) if d + 2 <= 10 else fr(n, d - 2), fr(1, d)]
    return mcq("Parmi ces fractions, laquelle est égale à %s : %s, %s ou %s ?" % (fr(1, 2), fr(h, d), fr(n, d), others[1]), fr(n, d), others,
               "La moitié de %d parts, c’est %d parts : <b>%s = %s</b>." % (d, n, fr(n, d), fr(1, 2)))


def s4_un():
    d = R.choice(DEN)
    w = 2 if R.random() < 0.3 else 1
    return mcq("Combien de %s faut-il pour faire %s ?" % (NOM[d][1], "une unité" if w == 1 else "2 unités"), w * d, [d - 1, w * d + 1, 1, w * d * 2],
               "%s une unité = %s. %s" % ("Dans", fr(d, d), "Pour 2 unités : %d + %d = <b>%d</b>." % (d, d, 2 * d) if w == 2 else "Il faut <b>%d</b> %s." % (d, NOM[d][1])))


def s4_decomp():
    d = R.choice([2, 3, 4, 5, 6, 8, 10])
    k = R.randint(1, d - 1)
    n = d + k
    return mcq("Complète : %s = 1 + …" % fr(n, d), fr(k, d), [fr(n, d), fr(k, n), fr(k + 1, d) if k + 1 < d else fr(k - 1, d) if k > 1 else fr(1, d + 1)],
               "%s = %s + %s = 1 + <b>%s</b>." % (fr(n, d), fr(d, d), fr(k, d), fr(k, d)))


def s5_qte():
    d = R.choice([2, 3, 4, 5, 10])
    q = R.randint(2, 9)
    tot = d * q
    p = K.next()
    k = 1 if R.random() < 0.6 or d == 2 else R.randint(2, d - 1)
    if __import__('math').gcd(k, d) > 1:
        return None
    thing = R.choice([("billes", "ses"), ("images", "ses"), ("euros", "ses"), ("bonbons", "ses")])
    right = k * q
    return mcq("%s a %d %s. %s en donne %s à son frère. Combien en donne-t-%s ?" % (p[0], tot, thing[0], p[1].capitalize(), "la moitié" if d == 2 else mot(k, d), p[1]),
               right, [tot - right, q if k > 1 else tot // 2 if d != 2 else tot - 1, tot // k if k > 1 else d, right + q],
               "%s de %d : %d %s %d = %d%s Il en donne <b>%d</b>." % ("La moitié" if d == 2 else "Un %s" % NOM[d][0] if k == 1 else mot(k, d).capitalize(), tot, tot, "÷", d, q,
                                                                    "." if k == 1 else ", puis %d × %d = %d." % (k, q, right), right))


def s5_pizza():
    p, o = K.two()
    d = R.choice([4, 6, 8])
    a, b = R.sample(range(1, d), 2)
    who = p[0] if a > b else o[0]
    return mcq("Deux pizzas identiques sont coupées en %d parts égales. %s mange %s de sa pizza, %s mange %s de la sienne. Qui a mangé le plus ?" % (d, p[0], fr(a, d), o[0], fr(b, d)),
               who, [o[0] if who == p[0] else p[0], "ils ont mangé autant", "on ne peut pas savoir"],
               "Les parts ont la même taille ; %s, c’est plus que %s : c’est <b>%s</b>." % (fr(max(a, b), d), fr(min(a, b), d), who))


def main():
    seen = set()
    sets = [
        ("Lire et écrire une fraction", mix(R, seen, [(s1_figure, 14), (s1_mot, 6)])),
        ("Fractions sur une droite graduée", mix(R, seen, [(s2_droite, 20)])),
        ("Comparer des fractions", mix(R, seen, [(s3_cmp_un, 6), (s3_meme_den, 7), (s3_meme_num, 7)])),
        ("Fractions égales à 1/2 et à 1", mix(R, seen, [(s4_demi, 4), (s4_un, 6), (s4_decomp, 10)])),
        ("Problèmes", mix(R, seen, [(s5_qte, 14), (s5_pizza, 6)])),
    ]
    body = lesson(
        ["Dans %s, le <b>dénominateur</b> 4 dit en combien de parts égales on partage l’unité ; le <b>numérateur</b> 3 dit combien de parts on prend." % fr(3, 4),
         "On lit « trois quarts ». %s = un demi, %s = un tiers, %s = un quart, %s = un cinquième." % (fr(1, 2), fr(1, 3), fr(1, 4), fr(1, 5)),
         "%s = 1 : toutes les parts. Si le numérateur est plus grand que le dénominateur, la fraction est plus grande que 1." % fr(4, 4),
         "Avec le même dénominateur, la plus grande fraction a le plus grand numérateur. Avec le même numérateur, c’est celle qui a le <b>plus petit</b> dénominateur."],
        [example("Une bande est partagée en 5 parts égales ; 2 sont coloriées.", ["5 parts : dénominateur 5", "2 parts : numérateur 2"], fr(2, 5)),
         example("Le quart de 20 billes", ["on partage 20 en 4 : 20 ÷ 4 = 5"], "5 billes")],
        [["Inverser : écrire %s pour 3 parts sur 4" % fr(4, 3), "Le nombre de parts du partage va en bas : %s." % fr(3, 4)],
         ["Compter les parts blanches", "On compte les parts coloriées."],
         ["Croire que %s &gt; %s car 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "En 8 parts, chaque part est plus petite : %s &lt; %s." % (fr(1, 8), fr(1, 4))]])
    faq = [("Quelles fractions étudie-t-on au CE2 ?", "Des fractions de dénominateur 2, 3, 4, 5, 6, 8 et 10, plus petites ou plus grandes que 1."),
           ("Pourquoi les parts doivent-elles être égales ?", "Une fraction parle de parts de même taille. Si les parts sont différentes, on ne peut pas dire « un quart ».")]
    make_unit(R, "fractions", "N",
              "Utiliser les fractions de dénominateur 2, 3, 4, 5, 6, 8 et 10 pour exprimer une partie d’une grandeur ou d’une quantité ; les représenter et les repérer sur une droite graduée ; les comparer à 1 et entre elles ; reconnaître des fractions égales à 1/2 et à 1 (résumé du programme 2024 du cycle 2).",
              "Les fractions", "Fractions CE2 : fiches et exercices avec corrigé", "Fractions",
              "Fiches de maths CE2 sur les fractions : lire une fraction, la placer sur une droite graduée, comparer, fractions égales à 1/2 et à 1, fraction d’une quantité. 100 exercices corrigés.",
              "3/4 : on partage en 4 parts égales et on en prend 3.", "4/4 = 1. Avec le même numérateur, plus le dénominateur est grand, plus la fraction est petite.",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
