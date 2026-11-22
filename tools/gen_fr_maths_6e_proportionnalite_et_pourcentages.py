# -*- coding: utf-8 -*-
"""
France Maths 6e : Proportionnalité et pourcentages
  python3 tools/gen_fr_maths_6e_proportionnalite_et_pourcentages.py
Reconnaître une situation de proportionnalité, passage par l’unité, propriétés de linéarité, pourcentages simples, problèmes.
Erreurs : ajouter au lieu de multiplier (2 → 6 donc 5 → 9), croire que l’âge et la taille sont proportionnels, 25 % de 80 = 25.
"""
import random
from fr_c4 import *

R = random.Random(60110)
K = Kids(R)


def s1():
    k = R.randint(2, 9)
    xs = sorted(R.sample(range(1, 13), 3))
    prop = R.random() < 0.5
    ys = [k * x for x in xs]
    if not prop:
        i = R.randrange(3)
        ys[i] += R.choice([-1, 1, 2])
    tb = table(["Nombre d’objets"] + [str(x) for x in xs], [["Prix (€)"] + [str(y) for y in ys]])
    if prop:
        return M("%s<br>Ce tableau est-il un tableau de proportionnalité ?" % tb, "oui", ["non", "seulement pour la première colonne", "on ne peut pas savoir"],
                 "On passe de la première ligne à la seconde en multipliant toujours par %d : <b>oui</b>." % k)
    return M("%s<br>Ce tableau est-il un tableau de proportionnalité ?" % tb, "non", ["oui", "seulement si on ajoute une colonne", "on ne peut pas savoir"],
             "%s : on ne multiplie pas toujours par le même nombre, donc <b>non</b>." % " ; ".join("%d → %d" % (x, y) for x, y in zip(xs, ys)))


def s2():
    p = K.next()
    a = R.randint(2, 8)
    u = Fr(R.randint(5, 60), 10)
    b = R.randint(2, 12)
    if b == a:
        return None
    thing = R.choice([("croissants", "€"), ("stylos", "€"), ("kg de pommes", "€"), ("tickets", "€")])
    return M("%d %s coûtent %s €. Combien coûtent %d %s ?" % (a, thing[0], em(a * u), b, thing[0]), euro(b * u),
             [euro(a * u + (b - a)), euro(u), euro(b * u + u)],
             "Un seul coûte %s ÷ %d = %s €, donc %d coûtent %d × %s = <b>%s €</b>." % (em(a * u), a, em(u), b, b, em(u), em(b * u)))


def s3():
    k = R.randint(2, 9)
    a, b = R.sample(range(2, 12), 2)
    kind = R.choice(["somme", "fois"])
    if kind == "somme":
        c = a + b
        tb = table(["Quantité", str(a), str(b), str(c)], [["Prix (€)", str(k * a), str(k * b), "?"]])
        return M("%s<br>Quel nombre remplace le « ? » ?" % tb, str(k * c), [str(k * c + 1), str(c + k * a), str(k * a * b)],
                 "%d = %d + %d, donc le prix est %d + %d = <b>%d</b>." % (c, a, b, k * a, k * b, k * c))
    m = R.randint(2, 5)
    tb = table(["Quantité", str(a), str(a * m)], [["Prix (€)", str(k * a), "?"]])
    return M("%s<br>Quel nombre remplace le « ? » ?" % tb, str(k * a * m), [str(k * a + (a * m - a)), str(k * a + m), str(k * a * m + k)],
             "%d × %d = %d, donc le prix est %d × %d = <b>%d</b>." % (a, m, a * m, k * a, m, k * a * m))


def s4():
    k = R.choice(["de", "de", "prop"])
    if k == "de":
        pc = R.choice([10, 20, 25, 50, 75, 5, 30])
        n = R.choice([20, 40, 60, 80, 120, 200, 300, 400]) if pc != 75 else R.choice([4, 8, 12, 20, 40, 80])
        r = Fr(pc * n, 100)
        if r.denominator != 1:
            return None
        return M("Combien font %d %% de %d ?" % (pc, n), d(r), [str(pc), d(n - r) if n - r != r else d(r + 1), d(Fr(n, pc)) if (Fr(n, pc)).denominator == 1 else d(r * 10)],
                 "%d %% de %d, c’est %s de %d : %d ÷ 100 × %d = <b>%s</b>." % (pc, n, fr(pc, 100), n, n, pc, d(r)))
    tot = R.choice([20, 25, 50, 200])
    pc = R.choice([10, 20, 40, 60, 30, 70, 80])
    part = tot * pc // 100
    if part * 100 != tot * pc:
        return None
    return M("Dans un club de %d enfants, %d font du foot. Quel pourcentage cela représente-t-il ?" % (tot, part), "%d %%" % pc, ["%d %%" % part, "%d %%" % (100 - pc), "%d %%" % (pc // 2 if pc > 10 else pc * 2)],
             "%d sur %d = %s = %s = <b>%d %%</b>." % (part, tot, fr(part, tot), fr(pc, 100), pc))


def s5():
    p = K.next()
    k = R.choice(["recette", "vitesse", "solde", "essence"])
    if k == "recette":
        g = R.choice([100, 125, 150, 200, 250])
        a, b = R.choice([(4, 6), (4, 10), (6, 9), (2, 5), (4, 12), (6, 15)])
        return M("Pour %d personnes, une recette demande %d g de farine. Combien en faut-il pour %d personnes ?" % (a, g, b), "%s g" % d(Fr(g * b, a)),
                 ["%s g" % d(g + (b - a)), "%s g" % d(g * b), "%s g" % d(Fr(g * b, a) + g)],
                 "Pour 1 personne : %d ÷ %d ; pour %d : %d ÷ %d × %d = <b>%s g</b>." % (g, a, b, g, a, b, d(Fr(g * b, a))))
    if k == "vitesse":
        v = R.choice([4, 5, 6, 12, 15, 20])
        h = R.randint(2, 5)
        return M("%s marche à vitesse constante : %d km en 1 h. Quelle distance parcourt-%s en %d h ?" % (p[0], v, p[1], h), "%d km" % (v * h), ["%d km" % (v + h), "%d km" % (v * h + v), "%d km" % (v * (h - 1))],
                 "Distance et durée sont proportionnelles : %d × %d = <b>%d km</b>." % (v, h, v * h))
    if k == "solde":
        pc = R.choice([10, 20, 25, 50])
        n = R.choice([40, 60, 80, 120, 200])
        r = n * pc // 100
        return M("Un manteau coûte %d €. Pendant les soldes, son prix baisse de %d %%. De combien d’euros baisse-t-il ?" % (n, pc), "%d €" % r, ["%d €" % pc, "%d €" % (n - r), "%d €" % (r * 2)],
                 "%d %% de %d = %d ÷ 100 × %d = <b>%d €</b> (le nouveau prix est %d €)." % (pc, n, n, pc, r, n - r))
    a, b = R.choice([(5, 15), (4, 12), (10, 25), (8, 20), (6, 15)])
    c = R.choice([2, 3, 4, 5])
    return M("Une voiture consomme %d L d’essence pour %d km. Combien consomme-t-elle pour %d km ?" % (a, 100, 100 * c), "%d L" % (a * c), ["%d L" % (a + c), "%d L" % (a * c + a), "%d L" % (100 * c // a)],
             "%d km = %d × 100 km, donc %d × %d = <b>%d L</b>." % (100 * c, c, c, a, a * c))


def main():
    seen = set()
    sets = [("Reconnaître la proportionnalité", mix(R, seen, [(s1, 20)])), ("Passer par l’unité", mix(R, seen, [(s2, 20)])),
            ("Compléter un tableau", mix(R, seen, [(s3, 20)])), ("Pourcentages", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Deux grandeurs sont <b>proportionnelles</b> si l’on passe de l’une à l’autre en multipliant toujours par le même nombre.",
              "Méthodes : passer par l’unité (prix d’un objet), ou utiliser les propriétés : si on double la quantité, on double le prix ; prix de 5 = prix de 2 + prix de 3.",
              "Un pourcentage est une proportion sur 100 : 25 % de 80 = 80 ÷ 100 × 25 = 20."],
             [("3 stylos coûtent 4,50 €. Prix de 7 stylos ?", ["1 stylo : 4,50 ÷ 3 = 1,50 €", "7 × 1,50"], "10,50 €")],
             [["Ajouter au lieu de multiplier : 2 → 6, donc 5 → 9", "De 2 à 6, on multiplie par 3 : 5 → 15."],
              ["Croire que tout est proportionnel", "L’âge et la taille ne sont pas proportionnels."],
              ["25 % de 80 = 25", "25 % de 80 = 20 : c’est le quart de 80."]])
    faq = [("Comment savoir si un tableau est de proportionnalité ?", "On vérifie qu’on multiplie toujours par le même nombre pour passer d’une ligne à l’autre."),
           ("Comment calculer 10 % d’un nombre ?", "On le divise par 10 : 10 % de 350 = 35.")]
    unit("6e", R, "proportionnalite-et-pourcentages", "P",
         "Reconnaître et résoudre des problèmes de proportionnalité (passage par l’unité, propriétés de linéarité) ; calculer une proportion et l’exprimer en pourcentage dans des cas simples ; appliquer un pourcentage",
         "Proportionnalité et pourcentages", "Proportionnalité et pourcentages",
         "Fiches de maths 6e sur la proportionnalité et les pourcentages : reconnaître, passer par l’unité, compléter un tableau, calculer un pourcentage et problèmes. 100 exercices corrigés.",
         "On multiplie toujours par le même nombre.", "25 % de 80 = 20", body, faq, sets, 10)


if __name__ == "__main__":
    main()
