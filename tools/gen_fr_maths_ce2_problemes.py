# -*- coding: utf-8 -*-
"""
France Maths CE2 : Résoudre des problèmes (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_problemes.py
Problèmes additifs (état final, état initial, transformation), comparaison (de plus, de moins), « fois plus, fois moins »,
problèmes en deux étapes, produits (combinaisons).
Erreurs : choisir l’opération d’après un mot (« de plus » → +), oublier une étape, additionner dans les combinaisons.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, Kids, FOIS, DIV

R = random.Random(51011)
K = Kids(R)


def que(n):
    return ("qu’" if n[0] in "AEIOUÉÈHaeiou" else "que ") + n


def s1():
    p = K.next()
    k = R.choice(["gagne", "perd", "bus", "monte", "achete"])
    a, b = R.randint(25, 480), R.randint(12, 260)
    if k == "gagne":
        return mcq("%s a %d cartes. %s en gagne %d à la récréation. Combien de cartes a-t-%s maintenant ?" % (p[0], a, p[1].capitalize(), b, p[1]), num(a + b), [num(abs(a - b)), num(a + b + 10), num(a + b - 1)],
                   "%s gagne : on ajoute. %d + %d = <b>%s</b>." % (p[0], a, b, num(a + b)))
    if k == "perd":
        if b >= a:
            return None
        return mcq("%s a %d billes. %s en perd %d. Combien de billes lui reste-t-il ?" % (p[0], a, p[1].capitalize(), b), num(a - b), [num(a + b), num(a - b + 10), num(a - b - 10)],
                   "On enlève : %d − %d = <b>%s</b>." % (a, b, num(a - b)))
    if k == "bus":
        a, b, c = R.randint(20, 45), R.randint(3, 15), R.randint(4, 18)
        return mcq("Dans un bus, il y a %d personnes. À l’arrêt, %d descendent et %d montent. Combien y a-t-il de personnes dans le bus ?" % (a, b, c), a - b + c, [a + b + c, a - b - c, a + b - c],
                   "%d − %d = %d, puis %d + %d = <b>%d</b>." % (a, b, a - b, a - b, c, a - b + c))
    if k == "monte":
        a, b = R.randint(120, 860), R.randint(45, 390)
        return mcq("Une randonneuse monte %d m, puis encore %d m. De combien de mètres est-elle montée en tout ?" % (a, b), "%s m" % num(a + b), ["%s m" % num(abs(a - b)), "%s m" % num(a + b + 100), "%s m" % num(a + b - 10)],
                   "%d + %d = <b>%s m</b>." % (a, b, num(a + b)))
    a, b = R.randint(25, 95), R.randint(6, 22)
    if b >= a:
        return None
    return mcq("%s a %d €. %s achète un jeu à %d €. Combien d’argent lui reste-t-il ?" % (p[0], a, p[1].capitalize(), b), "%s €" % num(a - b), ["%s €" % num(a + b), "%s €" % num(a - b + 10), "%s €" % num(b)],
               "%d − %d = <b>%s €</b>." % (a, b, num(a - b)))


def s2():
    p, o = K.two()
    k = R.choice(["avant", "combien", "deplus", "demoins"])
    a, b = R.randint(30, 400), R.randint(12, 200)
    if k == "avant":
        return mcq("%s a gagné %d images. Maintenant, %s en a %d. Combien d’images avait-%s avant ?" % (p[0], b, p[1], a + b, p[1]), num(a), [num(a + 2 * b), num(b), num(a + 10)],
                   "On cherche le début : %d − %d = <b>%s</b>. Vérifie : %d + %d = %d." % (a + b, b, num(a), a, b, a + b))
    if k == "combien":
        return mcq("La coopérative de l’école avait %d €. Après la kermesse, elle a %d €. Combien d’euros la kermesse a-t-elle rapportés ?" % (a, a + b), "%s €" % num(b), ["%s €" % num(2 * a + b), "%s €" % num(a), "%s €" % num(b + 10)],
                   "On cherche l’écart : %d − %d = <b>%s €</b>." % (a + b, a, num(b)))
    if k == "deplus":
        return mcq("%s a %d timbres. %s en a %d de plus %s. Combien de timbres a %s ?" % (p[0], a, o[0], b, que(p[0]), o[0]), num(a + b), [num(abs(a - b)), num(b), num(a + b + 10)],
                   "%s en a plus : %d + %d = <b>%s</b>." % (o[0], a, b, num(a + b)))
    if a <= b + 5:
        return None
    return mcq("%s a %d timbres. C’est %d de plus %s. Combien de timbres a %s ?" % (p[0], a, b, que(o[0]), o[0]), num(a - b), [num(a + b), num(b), num(a - b + 10)],
               "%s en a %d de moins : %d − %d = <b>%s</b>. Attention : « de plus » ne veut pas toujours dire +." % (o[0], b, a, b, num(a - b)))


def s3():
    p, o = K.two()
    k = R.choice(["fois_plus", "fois_moins", "fois_age", "fois_prix"])
    n, f = R.randint(4, 25), R.randint(2, 5)
    if k == "fois_plus":
        return mcq("%s a %d billes. %s en a %d fois plus. Combien de billes a %s ?" % (p[0], n, o[0], f, o[0]), n * f, [n + f, n * f + n, n * (f - 1) if f > 2 else n + 2 * f],
                   "%d fois plus : %d %s %d = <b>%d</b>." % (f, n, FOIS, f, n * f))
    if k == "fois_moins":
        return mcq("%s a %d autocollants. %s en a %d fois moins. Combien d’autocollants a %s ?" % (p[0], n * f, o[0], f, o[0]), n, [n * f - f, n * f * f if n * f * f < 1000 else n + 1, n + f],
                   "%d fois moins : %d %s %d = <b>%d</b>." % (f, n * f, DIV, f, n))
    if k == "fois_age":
        n = R.randint(5, 12)
        f = R.choice([3, 4, 5]) if n <= 12 else 2
        return mcq("%s a %d ans. Sa mère a %d fois son âge. Quel âge a sa mère ?" % (p[0], n, f), "%d ans" % (n * f), ["%d ans" % (n + f), "%d ans" % (n * f + f), "%d ans" % (n * (f + 1))],
                   "%d %s %d = <b>%d ans</b>." % (n, FOIS, f, n * f))
    n = R.randint(3, 30)
    return mcq("Un cahier coûte %d €. Un livre coûte %d fois plus cher. Combien coûte le livre ?" % (n, f), "%d €" % (n * f), ["%d €" % (n + f), "%d €" % (n * f - n) if f > 2 else "%d €" % (n + 2), "%d €" % (n * f + 1)],
               "%d %s %d = <b>%d €</b>." % (n, FOIS, f, n * f))


def s4():
    p = K.next()
    k = R.choice(["achat", "paquets", "train", "economie", "classe"])
    if k == "achat":
        a, pa, b, pb = R.randint(2, 6), R.randint(2, 9), R.randint(2, 5), R.randint(3, 12)
        t = a * pa + b * pb
        return mcq("%s achète %d stylos à %d € et %d classeurs à %d €. Combien paie-t-%s ?" % (p[0], a, pa, b, pb, p[1]), "%d €" % t, ["%d €" % (a + pa + b + pb), "%d €" % (a * pa), "%d €" % (pa + pb) if pa + pb != t else "%d €" % (t + 1)],
                   "%d %s %d = %d ; %d %s %d = %d ; %d + %d = <b>%d €</b>." % (a, FOIS, pa, a * pa, b, FOIS, pb, b * pb, a * pa, b * pb, t))
    if k == "paquets":
        n, s, m = R.randint(3, 8), R.randint(6, 12), R.randint(3, 15)
        if m >= n * s:
            return None
        return mcq("%s a %d paquets de %d biscuits. %s en mange %d. Combien de biscuits reste-t-il ?" % (p[0], n, s, p[1].capitalize(), m), n * s - m, [n * s, n + s - m if n + s > m else n * s + m, n * (s - m) if s > m else n * s - m + 10],
                   "%d %s %d = %d, puis %d − %d = <b>%d</b>." % (n, FOIS, s, n * s, n * s, m, n * s - m))
    if k == "train":
        a, b, c = R.randint(150, 420), R.randint(40, 120), R.randint(30, 140)
        return mcq("Un train part avec %d voyageurs. À la gare, %d descendent et %d montent. Combien de voyageurs repartent ?" % (a, b, c), num(a - b + c), [num(a + b + c), num(a - b - c), num(a - b)],
                   "%d − %d = %d, puis %d + %d = <b>%s</b>." % (a, b, a - b, a - b, c, num(a - b + c)))
    if k == "economie":
        w, x, cost = R.randint(3, 8), R.randint(4, 9), R.randint(20, 60)
        have = w * x
        if cost <= have:
            return None
        return mcq("%s met %d € de côté chaque semaine pendant %d semaines. %s veut un jeu à %d €. Combien lui manque-t-il ?" % (p[0], x, w, p[1].capitalize(), cost), "%d €" % (cost - have),
                   ["%d €" % have, "%d €" % (cost - x), "%d €" % (cost + have) if cost + have < 200 else "%d €" % (cost - have + 1)],
                   "%d %s %d = %d €, puis %d − %d = <b>%d €</b>." % (w, FOIS, x, have, cost, have, cost - have))
    g, f, absn = R.randint(10, 15), R.randint(9, 15), R.randint(2, 4)
    return mcq("Dans une classe, il y a %d filles et %d garçons. Aujourd’hui, %d élèves sont absents. Combien d’élèves sont présents ?" % (g, f, absn), g + f - absn, [g + f, g + f + absn, g - absn],
               "%d + %d = %d élèves, puis %d − %d = <b>%d</b>." % (g, f, g + f, g + f, absn, g + f - absn))


def s5():
    k = R.choice(["tenue", "menu", "glace", "drapeau", "choix"])
    if k == "tenue":
        a, b = R.randint(2, 6), R.randint(2, 5)
        p = K.next()
        return mcq("%s a %d t-shirts et %d shorts. Combien de tenues différentes (un t-shirt et un short) peut-%s faire ?" % (p[0], a, b, p[1]), a * b, [a + b, a * b - 1, a * b + a],
                   "Chaque t-shirt va avec chaque short : %d %s %d = <b>%d</b> tenues." % (a, FOIS, b, a * b))
    if k == "menu":
        a, b = R.randint(2, 5), R.randint(2, 5)
        return mcq("À la cantine, on choisit une entrée parmi %d et un dessert parmi %d. Combien de menus différents sont possibles ?" % (a, b), a * b, [a + b, a * b + 1, max(a, b)],
                   "%d entrées %s %d desserts = <b>%d</b> menus." % (a, FOIS, b, a * b))
    if k == "glace":
        a, b = R.randint(3, 8), R.randint(2, 4)
        return mcq("Un glacier propose %d parfums et %d sortes de cornets. Combien de glaces différentes à une boule peut-on choisir ?" % (a, b), a * b, [a + b, a * b - b, a * b + 2],
                   "Chaque parfum avec chaque cornet : %d %s %d = <b>%d</b>." % (a, FOIS, b, a * b))
    if k == "drapeau":
        a, b = R.randint(2, 4), R.randint(3, 6)
        return mcq("Pour un sandwich, on choisit un pain parmi %d et une garniture parmi %d. Combien de sandwichs différents peut-on faire ?" % (a, b), a * b, [a + b, a * b + b, a * b - 1],
                   "Chaque pain avec chaque garniture : %d %s %d = <b>%d</b>." % (a, FOIS, b, a * b))
    a, b = R.randint(3, 9), R.randint(3, 9)
    if a == b:
        return None
    p = K.next()
    return mcq("%s veut acheter un livre à %d € et un stylo à %d €. Combien paie-t-%s pour %d livres et %d stylos ?" % (p[0], a, b, p[1], 2, 3), "%d €" % (2 * a + 3 * b),
               ["%d €" % (a + b), "%d €" % (5 * (a + b)), "%d €" % (2 * a + b)],
               "2 %s %d = %d ; 3 %s %d = %d ; %d + %d = <b>%d €</b>." % (FOIS, a, 2 * a, FOIS, b, 3 * b, 2 * a, 3 * b, 2 * a + 3 * b))


def main():
    seen = set()
    sets = [
        ("Ajouter ou enlever", mix(R, seen, [(s1, 20)])),
        ("Chercher le début, l’écart, de plus ou de moins", mix(R, seen, [(s2, 20)])),
        ("Fois plus, fois moins", mix(R, seen, [(s3, 20)])),
        ("Problèmes en deux étapes", mix(R, seen, [(s4, 20)])),
        ("Combinaisons et problèmes variés", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Lis tout l’énoncé. Cherche <b>ce que l’on demande</b> avant de calculer.",
         "Ajouter ou enlever ? On peut faire un schéma : une barre pour le tout, des morceaux pour les parties.",
         "« %d fois plus » se calcule avec %s ; « %d fois moins » avec %s." % (3, FOIS, 3, DIV),
         "Pour les combinaisons (t-shirts et shorts), chaque choix va avec chaque autre : on <b>multiplie</b>.",
         "Dans un problème en deux étapes, on calcule d’abord ce qui manque, puis la réponse."],
        [example("Léo a 34 cartes. C’est 8 de plus que Zoé. Combien Zoé a-t-elle de cartes ?", ["Zoé en a moins que Léo", "34 − 8 = 26"], "26 cartes"),
         example("3 t-shirts et 4 shorts : combien de tenues ?", ["chaque t-shirt avec 4 shorts", "3 %s 4 = 12" % FOIS], "12 tenues")],
        [["Choisir l’opération d’après un mot : « de plus » → +", "Fais un schéma : qui en a le plus ?"],
         ["Oublier une étape", "Relis la question : as-tu répondu à ce qui est demandé ?"],
         ["Additionner les choix : 3 + 4 = 7 tenues", "Chaque t-shirt va avec 4 shorts : 3 %s 4 = 12." % FOIS]])
    faq = [("Comment savoir quelle opération faire ?", "On imagine la situation ou on fait un schéma. Les mots seuls ne suffisent pas toujours."),
           ("Faut-il écrire une phrase réponse ?", "Oui, en classe on écrit une phrase réponse avec l’unité : « Zoé a 26 cartes. »")]
    make_unit(R, "problemes", "N",
              "Résoudre des problèmes additifs et soustractifs (recherche d’un état final, d’un état initial, d’une transformation, comparaison), des problèmes multiplicatifs (fois plus, fois moins, combinaisons) et des problèmes en deux étapes (résumé du programme 2024 du cycle 2).",
              "Résoudre des problèmes", "Problèmes CE2 : fiches et exercices avec corrigé", "Problèmes",
              "Fiches de maths CE2 sur les problèmes : ajouter ou enlever, de plus et de moins, fois plus et fois moins, problèmes en deux étapes et combinaisons. 100 exercices corrigés.",
              "Je cherche d’abord ce que l’on demande.", "« Fois plus » : ×. « Fois moins » : ÷. Combinaisons : ×.",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
