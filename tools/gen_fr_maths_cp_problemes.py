# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Résoudre des problèmes
  python3 tools/gen_fr_maths_cp_problemes.py
Problèmes additifs (transformation, parties-tout, comparaison), multiplicatifs jusqu’à 30 (groupes égaux, partage),
CP : choisir le bon calcul ; CE1 : problèmes en deux étapes.
Erreurs : additionner parce qu’on lit « de plus », prendre un nombre de l’énoncé comme réponse, oublier une étape.
"""
import random
from fr_c2 import de_n, que, pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, ch, KINDS, nom, FOIS
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53009 + 100 * lv)
    K = Kids(R)


def wr(v, *xs):
    return [num(x) for x in xs if x > 0 and x != v]


def big():
    return (12, 60, 3, 9) if L == 0 else (120, 780, 25, 190)


def s1():
    p = K.next()
    lo, hi, blo, bhi = big()
    a, b = R.randint(lo, hi), R.randint(blo, bhi)
    k = R.choice(["gagne", "perd", "monte", "descend", "avant"])
    if k == "gagne":
        th = R.choice(["billes", "images", "points"])
        return mcq("%s a %s %s. %s en gagne %s. Combien en a-t-%s maintenant ?" % (p[0], num(a), th, p[1].capitalize(), num(b), p[1]), num(a + b), wr(a + b, a - b, a + b + 10, b),
                   "%s gagne : on ajoute. %s + %s = <b>%s</b>." % (p[0], num(a), num(b), num(a + b)))
    if k == "perd":
        th = R.choice(["billes", "cartes", "points"])
        return mcq("%s a %s %s. %s en perd %s. Combien lui en reste-t-il ?" % (p[0], num(a), th, p[1].capitalize(), num(b)), num(a - b), wr(a - b, a + b, a - b + 1, b),
                   "%s perd : on enlève. %s − %s = <b>%s</b>." % (p[0], num(a), num(b), num(a - b)))
    if k in ("monte", "descend") and L == 1:
        a, b = R.randint(40, 90), R.randint(12, 35)
    if k == "monte":
        return mcq("Dans le bus, il y a %s personnes. À l’arrêt, %s personnes montent. Combien de personnes y a-t-il maintenant ?" % (num(a), num(b)), num(a + b), wr(a + b, a - b, a + b - 1, b),
                   "Des personnes montent : %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "descend":
        return mcq("Dans le train, il y a %s personnes. À la gare, %s personnes descendent. Combien en reste-t-il ?" % (num(a), num(b)), num(a - b), wr(a - b, a + b, a - b - 1, b),
                   "Des personnes descendent : %s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    return mcq("%s a gagné %s images à la récréation. Maintenant, %s en a %s. Combien en avait-%s avant ?" % (p[0], num(b), p[1], num(a + b), p[1]), num(a), wr(a, a + 2 * b, b, a + 1),
               "Avant, %s en avait moins : %s − %s = <b>%s</b>." % (p[1], num(a + b), num(b), num(a)))


def s2():
    lo, hi, blo, bhi = big()
    a, b = R.randint(lo // 2 + 3, hi // 2), R.randint(blo + 2, bhi * 2)
    k = R.choice(["tout", "partie", "tout", "partie2"])
    if k == "tout":
        x, y = R.choice([("filles", "garçons", "élèves"), ("albums", "romans", "livres"), ("pommes", "poires", "fruits"), ("voitures rouges", "voitures bleues", "voitures")])
        return mcq("Il y a %s %s et %s %s. Combien de %s en tout ?" % (num(a), x, num(b), y, z) if False else "Dans %s, il y a %s %s et %s %s. Combien de %s en tout ?" % (
            {"élèves": "la classe", "livres": "la bibliothèque", "fruits": "le panier", "voitures": "le parking"}[y if False else ("élèves" if x == "filles" else "livres" if x == "albums" else "fruits" if x == "pommes" else "voitures")],
            num(a), x, num(b), y, "élèves" if x == "filles" else "livres" if x == "albums" else "fruits" if x == "pommes" else "voitures"),
            num(a + b), wr(a + b, abs(a - b), a + b + 10, a), "On réunit les deux parties : %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "partie":
        t = a + b
        return mcq("Dans la classe, il y a %s élèves. %s sont des filles. Combien y a-t-il de garçons ?" % (num(t), num(a)) if L == 0 else
                   "Une école a %s élèves. %s sont des filles. Combien y a-t-il de garçons ?" % (num(t), num(a)), num(b), wr(b, t + a, b + 1, a),
                   "Le tout moins une partie : %s − %s = <b>%s</b>." % (num(t), num(a), num(b)))
    t = a + b
    return mcq("Dans un sac, il y a %s billes rouges et des billes bleues. Il y a %s billes en tout. Combien de billes bleues ?" % (num(a), num(t)), num(b), wr(b, t + a, b - 1, t),
               "%s + … = %s : il y a <b>%s</b> billes bleues." % (num(a), num(t), num(b)))


def s3():
    p, q = K.two()
    lo, hi, blo, bhi = big()
    a, d = R.randint(lo, hi), R.randint(blo, bhi)
    b = a + d
    k = R.choice(["ecart", "deplus", "demoins", "ecart2"])
    if k == "ecart":
        return mcq("%s a %s ans. Sa grand-mère a %s ans. Combien d’années de plus a sa grand-mère ?" % (p[0], num(R.randint(6, 8)), num(R.randint(60, 75))), None, [], "") if False else \
            mcq("%s a %s cartes. %s en a %s. Combien de cartes %s a-t-%s de plus %s ?" % (p[0], num(b), q[0], num(a), p[0], p[1], que(q[0])), num(d), wr(d, a + b, d + 1, a),
                "On cherche l’écart : %s − %s = <b>%s</b>." % (num(b), num(a), num(d)))
    if k == "deplus":
        return mcq("%s a %s billes. %s a %s billes de plus %s. Combien de billes a %s ?" % (p[0], num(a), q[0], num(d), que(p[0]), q[0]), num(b), wr(b, a - d, d, b + 1),
                   "%s en a plus : %s + %s = <b>%s</b>." % (q[0], num(a), num(d), num(b)))
    if k == "demoins":
        return mcq("%s a %s points. %s a %s points de moins %s. Combien de points a %s ?" % (p[0], num(b), q[0], num(d), que(p[0]), q[0]), num(a), wr(a, b + d, d, a + 1),
                   "%s en a moins : %s − %s = <b>%s</b>." % (q[0], num(b), num(d), num(a)))
    return mcq("La tour bleue a %s cubes. La tour rouge en a %s. Combien de cubes faut-il ajouter à la tour bleue pour qu’elle soit aussi haute que la rouge ?" % (num(a), num(b)),
               num(d), wr(d, a + b, b, d - 1), "%s + … = %s : il faut <b>%s</b> cubes." % (num(a), num(b), num(d)))


def s4():
    p = K.next()
    k = R.choice(["groupes", "partage", "paquets", "image"])
    if k == "image":
        g, n = R.randint(2, 5), R.randint(2, 5)
        kind = R.choice(KINDS)
        svg = pic(KP.groups_svg([(n, kind)] * g), "%d groupes de %s" % (g, ch(kind, n)))
        return mcq("<div class='qfig'>%s</div>Il y a %d groupes de %s. Combien y en a-t-il en tout ?" % (svg, g, ch(kind, n)), str(g * n), wr(g * n, g + n, g * n + n, g * n - 1),
                   "%s : %s = <b>%d</b>." % ("+".join([str(n)] * g).replace("+", " + "), " + ".join([str(n)] * g), g * n) if False else
                   "%s = <b>%d</b>." % (" + ".join([str(n)] * g), g * n))
    if k == "groupes":
        g, n = R.randint(2, 6), R.randint(2, 5)
        if g * n > 30:
            return None
        return mcq("%s achète %d boîtes de %d gâteaux. Combien de gâteaux a-t-%s ?" % (p[0], g, n, p[1]), str(g * n), wr(g * n, g + n, g * n + n, g * n - g),
                   "%s = <b>%d</b> gâteaux." % (" + ".join([str(n)] * g), g * n) if L == 0 else "%d %s %d = <b>%d</b> gâteaux." % (g, FOIS, n, g * n))
    if k == "partage":
        n, g = R.randint(2, 6), R.choice([2, 3, 4, 5])
        t = n * g
        if t > 30:
            return None
        return mcq("%s partage %d bonbons entre %d enfants. Chacun a le même nombre. Combien chaque enfant en reçoit-il ?" % (p[0], t, g), str(n), wr(n, t - g, t + g, g if g != n else n + 1),
                   "%s = %d : chaque enfant reçoit <b>%d</b> bonbons." % (" + ".join([str(n)] * g), t, n))
    n, g = R.randint(2, 6), R.choice([2, 3, 5, 10])
    t = n * g
    if t > 30:
        return None
    return mcq("On range %d œufs par boîtes de %d. Combien de boîtes faut-il ?" % (t, g), str(n), wr(n, t - g, t + g, g if g != n else n + 1),
               "%s = %d : il faut <b>%d</b> boîtes." % (" + ".join([str(g)] * n), t, n))


def s5_choix():
    p = K.next()
    a, b = R.randint(12, 40), R.randint(3, 9)
    k = R.choice(["plus", "moins", "reste", "tout"])
    if k in ("plus", "tout"):
        q = "%s a %d billes. %s en gagne %d. Quel calcul donne le nombre de billes %s ?" % (p[0], a, p[1].capitalize(), b, de_n(p[0])) if k == "plus" else \
            "Il y a %d enfants dans la cour et %d dans la classe. Quel calcul donne le nombre d’enfants en tout ?" % (a, b)
        return mcq(q, "%d + %d" % (a, b), ["%d − %d" % (a, b), "%d + %d" % (a, a), "%d − %d" % (a + b, a)], "On réunit ou on ajoute : <b>%d + %d</b> = %d." % (a, b, a + b))
    q = "%s a %d billes. %s en perd %d. Quel calcul donne le nombre de billes %s ?" % (p[0], a, p[1].capitalize(), b, de_n(p[0])) if k == "moins" else \
        "Il y a %d gâteaux. On en mange %d. Quel calcul donne le nombre de gâteaux qui restent ?" % (a, b)
    return mcq(q, "%d − %d" % (a, b), ["%d + %d" % (a, b), "%d − %d" % (b, a) if False else "%d + %d" % (b, b), "%d − %d" % (a, a)], "On enlève : <b>%d − %d</b> = %d." % (a, b, a - b))


def s5_deux():
    p = K.next()
    k = R.choice(["gp", "pg", "achat", "bus", "mult"])
    if k == "gp":
        a, b, c = R.randint(120, 500), R.randint(40, 200), R.randint(20, 90)
        return mcq("%s a %s points. %s gagne %s points, puis en perd %s. Combien de points a-t-%s à la fin ?" % (p[0], num(a), p[1].capitalize(), num(b), num(c), p[1]), num(a + b - c), wr(a + b - c, a + b + c, a + b, a - b + c if a - b + c > 0 else a - c),
                   "%s + %s = %s, puis %s − %s = <b>%s</b>." % (num(a), num(b), num(a + b), num(a + b), num(c), num(a + b - c)))
    if k == "pg":
        a, b, c = R.randint(200, 600), R.randint(40, 150), R.randint(20, 120)
        return mcq("Une boulangerie a %s croissants. Elle en vend %s le matin et %s l’après-midi. Combien en reste-t-il ?" % (num(a), num(b), num(c)), num(a - b - c), wr(a - b - c, a - b + c, a - b, b + c),
                   "%s + %s = %s vendus, puis %s − %s = <b>%s</b>." % (num(b), num(c), num(b + c), num(a), num(b + c), num(a - b - c)))
    if k == "achat":
        a, b, c = R.randint(5, 15), R.randint(5, 15), R.choice([30, 40, 50])
        if a + b >= c:
            return None
        return mcq("%s a %d €. %s achète un livre à %d € et un jeu à %d €. Combien d’argent lui reste-t-il ?" % (p[0], c, p[1].capitalize(), a, b), "%d €" % (c - a - b), ["%d €" % (c - a), "%d €" % (a + b), "%d €" % (c - a + b)],
                   "%d + %d = %d €, puis %d − %d = <b>%d €</b>." % (a, b, a + b, c, a + b, c - a - b))
    if k == "bus":
        a, b, c = R.randint(20, 40), R.randint(5, 15), R.randint(3, 12)
        return mcq("Dans un bus, il y a %d personnes. Au premier arrêt, %d personnes montent. Au deuxième arrêt, %d personnes descendent. Combien de personnes y a-t-il dans le bus ?" % (a, b, c),
                   str(a + b - c), wr(a + b - c, a + b + c, a - b + c, a + b), "%d + %d = %d, puis %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b - c))
    g, n, e = R.randint(2, 5), R.randint(3, 6), R.randint(2, 9)
    if g * n > 30:
        return None
    return mcq("%s a %d paquets de %d cartes et %d cartes seules. Combien de cartes a-t-%s en tout ?" % (p[0], g, n, e, p[1]), str(g * n + e), wr(g * n + e, g + n + e, g * n, g * (n + e)),
               "%d %s %d = %d, puis %d + %d = <b>%d</b>." % (g, FOIS, n, g * n, g * n, e, g * n + e))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Gagner, perdre, avant, après", mix(R, seen, [(s1, 20)])),
        ("Le tout et les parties", mix(R, seen, [(s2, 20)])),
        ("Comparer", mix(R, seen, [(s3, 20)])),
        ("Groupes égaux et partages", mix(R, seen, [(s4, 20)])),
        ("Choisir le bon calcul" if lv == 0 else "Problèmes en deux étapes", mix(R, seen, [(s5_choix, 20)] if lv == 0 else [(s5_deux, 20)])),
    ]
    body = lesson(["Je lis l’énoncé et je cherche la <b>question</b>.",
                   "Je me demande : est-ce qu’on ajoute (on gagne, on réunit), est-ce qu’on enlève (on perd, il reste, combien de plus) ?",
                   "Je peux faire un dessin. Je vérifie que la réponse est possible."],
                  [example("Léa a 8 billes. Tom en a 3 de plus. Combien Tom en a-t-il ?", ["Tom en a plus que Léa", "8 + 3"], "11 billes")],
                  [["Additionner dès qu’on lit « de plus »", "« Combien de plus ? » se calcule avec une soustraction."],
                   ["Répondre avec un nombre de l’énoncé", "La réponse est un nouveau nombre qu’on calcule."],
                   ["Oublier une étape" if lv else "Oublier l’unité dans la réponse", "On fait les deux calculs l’un après l’autre." if lv else "On écrit « 11 billes », pas seulement « 11 »."]])
    faq = [("Comment savoir s’il faut ajouter ou enlever ?", "On imagine l’histoire : si la quantité augmente, on ajoute ; si elle diminue, on enlève."),
           ("Un dessin peut-il aider ?", "Oui : dessiner des ronds ou une barre aide à voir le tout et les parties.")]
    unit(lv, R, "problemes", "N",
         ("Résoudre des problèmes additifs en une étape (transformation, réunion, comparaison) et des problèmes multiplicatifs simples (groupes égaux, partage) jusqu’à 30" if lv == 0 else
          "Résoudre des problèmes additifs (parties-tout, transformation, comparaison) et multiplicatifs, en une ou deux étapes"),
         "Résoudre des problèmes", "Problèmes",
         ("Fiches de maths CP pour résoudre des problèmes : gagner et perdre, tout et parties, comparer, groupes égaux, partages, choisir le calcul. 100 problèmes corrigés." if lv == 0 else
          "Fiches de maths CE1 pour résoudre des problèmes : transformations, tout et parties, comparaisons, groupes égaux et problèmes en deux étapes. 100 problèmes corrigés."),
         "Lire la question, puis choisir le calcul.", "On gagne → + ; on perd → −.", body, faq, sets, 9)


if __name__ == "__main__":
    build(0)
