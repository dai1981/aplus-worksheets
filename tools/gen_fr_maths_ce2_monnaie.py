# -*- coding: utf-8 -*-
"""
France Maths CE2 : La monnaie : euros et centimes (Grandeurs et mesures)
  python3 tools/gen_fr_maths_ce2_monnaie.py
Compter des pièces et des billets, euros et centimes (1 € = 100 c), écrire une somme avec une virgule, comparer,
faire une somme avec des pièces, rendre la monnaie, problèmes d’achat.
Erreurs : compter les pièces au lieu de leur valeur, 1 € = 10 c, 3,5 € lu « 3 € 5 c », rendre la monnaie en additionnant.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, Kids, eur, argent_svg, NB, FOIS

R = random.Random(51015)
K = Kids(R)
COINS = [200, 100, 50, 20, 10, 5, 2, 1]
NOTES = [5000, 2000, 1000, 500]


def euc(c):
    """3 € 50 c"""
    e, r = divmod(c, 100)
    if e and r:
        return "%d%s€ %d%sc" % (e, NB, r, NB)
    if e:
        return "%d%s€" % (e, NB)
    return "%d%sc" % (r, NB)


def s1():
    k = R.choice(["pieces", "pieces", "billets"])
    if k == "pieces":
        items = R.sample(COINS[:7], R.randint(3, 5))
    else:
        items = R.sample(NOTES, R.randint(1, 3)) + R.sample(COINS[:4], R.randint(1, 3))
    t = sum(items)
    return mcq("<div class='qfig'>%s</div>Combien d’argent y a-t-il ?" % argent_svg(items), eur(t), [eur(t + 100), eur(t - min(items)) if t - min(items) > 0 else eur(t + 50), "%d%s€" % (len(items), NB), eur(t + 10)],
               "On additionne la valeur de chaque pièce et de chaque billet : <b>%s</b>." % eur(t))


def s2():
    k = R.choice(["e_c", "ec_c", "c_ec", "virg", "virg2"])
    e, c = R.randint(1, 9), R.choice([5, 10, 20, 25, 30, 45, 50, 60, 75, 80, 95])
    if k == "e_c":
        return mcq("Complète : %d%s€ = … centimes" % (e, NB), num(e * 100), [num(e * 10), num(e * 1000), num(e + 100)], "1 € = 100 c, donc %d € = <b>%s c</b>." % (e, num(e * 100)))
    if k == "ec_c":
        return mcq("Complète : %s = … centimes" % euc(e * 100 + c), num(e * 100 + c), [num(e * 10 + c), num(e + c), num(e * 1000 + c)], "%d € = %d c ; %d + %d = <b>%d c</b>." % (e, e * 100, e * 100, c, e * 100 + c))
    if k == "c_ec":
        n = e * 100 + c
        return mcq("Complète : %d centimes = … € … c" % n, euc(n), [euc(n // 10 * 100 + n % 10) if n // 10 < 100 else euc(n + 100), euc((e + 1) * 100 + c), "%d%s€ %d%sc" % (e, NB, c * 10, NB) if c < 10 else euc(n - 100) if e > 1 else euc(n + 5)],
                   "100 c = 1 €. %d c = %d c + %d c = <b>%s</b>." % (n, e * 100, c, euc(n)))
    if k == "virg":
        return mcq("Comment écrit-on %s avec une virgule ?" % euc(e * 100 + c), eur(e * 100 + c), ["%d,%d%s€" % (e, c, NB) if c < 10 else "%d,%d%s€" % (e, c // 10, NB) if c % 10 == 0 else "%d,%02d%s€" % (e + 1, c, NB), eur(c * 100 + e) if c * 100 + e < 10000 else eur(e * 100 + c + 1), "%d%s€" % (e + c, NB)],
                   "Les deux chiffres après la virgule sont les centimes : <b>%s</b>." % eur(e * 100 + c))
    return mcq("Que veut dire %s ?" % eur(e * 100 + c), euc(e * 100 + c), [euc(e * 100 + c // 10) if c % 10 == 0 and c // 10 else euc(e * 100 + c + 5), "%d%s€ %d%sc" % (c, NB, e, NB), euc((e + 1) * 100 + c)],
               "Avant la virgule, les euros ; après, les centimes : <b>%s</b>." % euc(e * 100 + c))


def s3():
    k = R.choice(["cmp", "nb", "combien"])
    if k == "cmp":
        a = R.randint(1, 9) * 100 + R.choice([5, 50, 20, 75, 90])
        b = a + R.choice([-45, -15, 15, 45, 4, -4]) * (1 if R.random() < 0.5 else 1)
        if b <= 0 or b == a:
            return None
        A, B = eur(a), euc(b)
        big = A if a > b else B
        return mcq("Quelle somme est la plus grande : %s ou %s ?" % (A, B), big, [B if big == A else A, "elles sont égales", "on ne peut pas savoir"],
                   "%s = %s. La plus grande somme est <b>%s</b>." % (A, euc(a), big))
    if k == "nb":
        piece, tot = R.choice([(200, 1000), (200, 2000), (50, 500), (20, 200), (10, 100), (50, 300), (20, 100), (100, 1000), (500, 2000), (1000, 5000)])
        n = tot // piece
        return mcq("Combien de %s de %s faut-il pour faire %s ?" % ("billets" if piece >= 500 else "pièces", eur(piece, c=True), eur(tot)), n, [n * 10 if n * 10 < 200 else n + 2, tot // 100, n + 1, n - 1],
                   "%s %s %d = %s : il faut <b>%d</b> %s." % (eur(piece, c=True), FOIS, n, eur(tot), n, "billets" if piece >= 500 else "pièces"))
    t = R.choice([130, 160, 270, 350, 380, 420, 560, 740, 830, 960, 1250, 1570, 2340])
    best = []
    r = t
    for v in [2000, 1000, 500, 200, 100, 50, 20, 10]:
        while r >= v:
            best.append(v)
            r -= v
    n = len(best)
    return mcq("On veut payer %s avec le moins de pièces et de billets possible. Combien en faut-il ?" % eur(t), n, [n + 1, n + 2, n - 1, t // 100],
               "On prend d’abord les plus grandes valeurs : %s. Il en faut <b>%d</b>." % (" + ".join(eur(v, c=True) for v in best), n))


def s4():
    p = K.next()
    prix = R.randint(1, 18) * 100 + R.choice([0, 20, 50, 75, 30, 90, 40, 60])
    billet = [b for b in [500, 1000, 2000] if b > prix][0]
    r = billet - prix
    wr = [eur(billet + prix), eur(r + 100), eur(r - 10) if r > 10 else eur(r + 10), eur(abs((billet // 100 - prix // 100) * 100 - prix % 100 + 100)) if prix % 100 else eur(r + 50)]
    return mcq("%s achète un article à %s. %s paie avec un billet de %s. Combien la marchande lui rend-elle ?" % (p[0], eur(prix), p[1].capitalize(), eur(billet)), eur(r), [w for w in wr if w != eur(r)],
               "On calcule %s − %s. On peut compléter : de %s à %s, il manque <b>%s</b>." % (eur(billet), eur(prix), eur(prix), eur(billet), eur(r)))


ITEMS = [("un croissant", 120), ("une baguette", 110), ("un cahier", 250), ("un stylo", 180), ("une bande dessinée", 1290), ("un ballon", 875),
         ("une glace", 350), ("un jus de fruits", 225), ("un livre", 690), ("une trousse", 760), ("un pain au chocolat", 135), ("une gourde", 940)]


def s5():
    p = K.next()
    k = R.choice(["deux", "plusieurs", "assez", "reste"])
    if k == "deux":
        (a, pa), (b, pb) = R.sample(ITEMS, 2)
        t = pa + pb
        return mcq("%s achète %s à %s et %s à %s. Combien paie-t-%s ?" % (p[0], a, eur(pa), b, eur(pb), p[1]), eur(t), [eur(abs(pa - pb)), eur(t + 100), eur((pa // 100 + pb // 100) * 100 + (pa % 100 + pb % 100) % 100) if (pa % 100 + pb % 100) >= 100 else eur(t - 10)],
                   "%s + %s = <b>%s</b>." % (eur(pa), eur(pb), eur(t)))
    if k == "plusieurs":
        a, pa = R.choice(ITEMS[:4] + ITEMS[6:8] + ITEMS[10:11])
        n = R.randint(2, 6)
        name = a.split(" ", 1)[1]
        pl = {"croissant": "croissants", "baguette": "baguettes", "cahier": "cahiers", "stylo": "stylos", "glace": "glaces", "jus de fruits": "jus de fruits", "pain au chocolat": "pains au chocolat"}[name]
        return mcq("Un %s coûte %s. Combien coûtent %d %s ?" % (name, eur(pa), n, pl) if a.startswith("un ") else "Une %s coûte %s. Combien coûtent %d %s ?" % (name, eur(pa), n, pl),
                   eur(n * pa), [eur(n + pa), eur(n * pa + pa), eur(n * (pa // 100) * 100)],
                   "%d %s %s = <b>%s</b>." % (n, FOIS, eur(pa), eur(n * pa)))
    if k == "assez":
        a, pa = R.choice(ITEMS)
        have = pa + R.choice([-150, -60, -25, 30, 80, 150])
        if have <= 0:
            return None
        ok = have >= pa
        return mcq("%s a %s. Peut-%s acheter %s à %s ?" % (p[0], eur(have), p[1], a, eur(pa)), "oui, il reste %s" % eur(have - pa) if ok else "non, il manque %s" % eur(pa - have),
                   ["non, il manque %s" % eur(have - pa) if ok else "oui, il reste %s" % eur(pa - have), "oui, il reste %s" % eur(have - pa + 100) if ok else "non, il manque %s" % eur(pa - have + 100), "oui, et il ne reste rien"],
                   "%s − %s : %s." % (eur(max(have, pa)), eur(min(have, pa)), "il reste <b>%s</b>" % eur(have - pa) if ok else "il manque <b>%s</b>" % eur(pa - have)))
    have = R.randint(10, 30) * 100
    (a, pa), (b, pb) = R.sample(ITEMS, 2)
    if pa + pb >= have:
        return None
    r = have - pa - pb
    return mcq("%s a %s. %s achète %s à %s et %s à %s. Combien lui reste-t-il ?" % (p[0], eur(have), p[1].capitalize(), a, eur(pa), b, eur(pb)), eur(r), [eur(pa + pb), eur(have - pa), eur(r + 100)],
               "%s + %s = %s, puis %s − %s = <b>%s</b>." % (eur(pa), eur(pb), eur(pa + pb), eur(have), eur(pa + pb), eur(r)))


def main():
    seen = set()
    sets = [
        ("Compter l’argent", mix(R, seen, [(s1, 20)])),
        ("Euros et centimes", mix(R, seen, [(s2, 20)])),
        ("Comparer et faire une somme", mix(R, seen, [(s3, 20)])),
        ("Rendre la monnaie", mix(R, seen, [(s4, 20)])),
        ("Problèmes d’achat", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["<b>1 € = 100 centimes</b>. Les pièces : 1 c, 2 c, 5 c, 10 c, 20 c, 50 c, 1 €, 2 €. Les billets : 5 €, 10 €, 20 €, 50 €…",
         "Pour compter, on commence par les billets et les pièces qui valent le plus.",
         "%s veut dire 3 € et 50 c. Après la virgule, il y a toujours <b>deux chiffres</b> pour les centimes." % eur(350),
         "Pour rendre la monnaie, on <b>complète</b> jusqu’à la somme donnée, ou on fait une soustraction."],
        [example("Rendre la monnaie sur 10 € pour %s" % eur(670), ["%s → 7 € : 30 c" % eur(670), "7 € → 10 € : 3 €"], eur(330)),
         example("4 € 5 c avec une virgule", ["5 centimes s’écrivent 05"], eur(405))],
        [["Compter les pièces au lieu de leur valeur", "Trois pièces ne font pas 3 € : on additionne ce que vaut chaque pièce."],
         ["Écrire 4 € 5 c : 4,5 €", "4,5 € = 4,50 €. Pour 5 centimes : %s." % eur(405)],
         ["Additionner pour rendre la monnaie", "On rend la différence entre ce qu’on donne et le prix."]])
    faq = [("Combien de centimes dans 1 euro ?", "Il y a 100 centimes dans 1 euro."),
           ("Comment rendre la monnaie sans poser l’opération ?", "On complète le prix jusqu’à la somme donnée : d’abord jusqu’à l’euro rond, puis jusqu’au billet.")]
    make_unit(R, "monnaie", "G",
              "Connaître la valeur des pièces et des billets en euros ; utiliser l’égalité 1 € = 100 c ; écrire une somme d’argent avec une virgule ; comparer des sommes ; calculer un prix, rendre la monnaie (résumé du programme 2024 du cycle 2).",
              "La monnaie : euros et centimes", "Monnaie CE2 : fiches et exercices avec corrigé", "Monnaie",
              "Fiches de maths CE2 sur la monnaie : compter des pièces et des billets, euros et centimes, écrire une somme, rendre la monnaie et problèmes d’achat. 100 exercices corrigés.",
              "1 € = 100 c.", "3,50 € = 3 € et 50 c.",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
