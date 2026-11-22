# -*- coding: utf-8 -*-
"""
France Maths CE1 : Le sens de la multiplication
  python3 tools/gen_fr_maths_ce1_sens_de_la_multiplication.py
Groupes égaux, quadrillages (tableaux rectangulaires), addition répétée, signe ×, commutativité, × 1, × 0, × 10, problèmes.
Erreurs : additionner les deux nombres (4 × 3 = 7), écrire 3 + 4 pour 3 groupes de 4, croire que 5 × 0 = 5.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, pic, ch, KINDS, nom, FOIS
import k_pics as KP

R = random.Random(53118)
K = Kids(R)


def wr(v, *xs):
    return [str(x) for x in xs if x >= 0 and x != v]


def s1():
    g, n = R.randint(2, 5), R.randint(2, 6)
    kind = R.choice(KINDS)
    svg = pic(KP.groups_svg([(n, kind)] * g), "%d groupes de %s" % (g, ch(kind, n)))
    k = R.choice(["tot", "ecr", "tot"])
    if k == "tot":
        return mcq("<div class='qfig'>%s</div>Combien y a-t-il %s en tout ?" % (svg, ("d’" if nom(kind)[0] in "aeiouéœ" else "de ") + nom(kind)), str(g * n), wr(g * n, g + n, g * n + n, g * n - 1),
                   "%d groupes de %d : %s = %d %s %d = <b>%d</b>." % (g, n, " + ".join([str(n)] * g), g, FOIS, n, g * n))
    return mcq("<div class='qfig'>%s</div>Quelle multiplication correspond à l’image ?" % svg, "%d %s %d" % (g, FOIS, n),
               ["%d + %d" % (g, n), "%d %s %d" % (g, FOIS, n + 1), "%d %s %d" % (g + 1, FOIS, n)],
               "Il y a %d groupes de %d : <b>%d %s %d</b> = %d." % (g, n, g, FOIS, n, g * n))


def s2():
    r, c = R.randint(2, 5), R.randint(2, 7)
    if r == c:
        return None
    kind = R.choice(KINDS)
    svg = pic(KP.array_svg(r, c, kind), "%d rangées de %s" % (r, ch(kind, c)))
    if R.random() < 0.6:
        return mcq("<div class='qfig'>%s</div>Combien y a-t-il d’objets ?" % svg, str(r * c), wr(r * c, r + c, r * c + c, 2 * (r + c)),
                   "%d rangées de %d : %d %s %d = <b>%d</b>." % (r, c, r, FOIS, c, r * c))
    return mcq("<div class='qfig'>%s</div>Quel calcul donne le nombre d’objets ?" % svg, "%d %s %d" % (r, FOIS, c), ["%d + %d" % (r, c), "%d %s %d" % (r, FOIS, r), "%d + %d + %d" % (c, c, c) if r != 3 else "%d + %d" % (c, c)],
               "%d rangées de %d : <b>%d %s %d</b> = %d (ou %d %s %d)." % (r, c, r, FOIS, c, r * c, c, FOIS, r))


def s3():
    n, g = R.randint(2, 9), R.randint(2, 6)
    if R.random() < 0.5:
        return mcq("%s = … ?" % " + ".join([str(n)] * g), "%d %s %d" % (g, FOIS, n), ["%d + %d" % (g, n), "%d %s %d" % (g + 1, FOIS, n), "%d %s %d" % (n, FOIS, n) if g != n else "%d %s %d" % (g, FOIS, n + 1)],
                   "On ajoute %d fois le nombre %d : <b>%d %s %d</b>." % (g, n, g, FOIS, n))
    return mcq("%d %s %d = …" % (g, FOIS, n), str(g * n), wr(g * n, g + n, g * n + n, g * n - g),
               "%d %s %d = %s = <b>%d</b>." % (g, FOIS, n, " + ".join([str(n)] * g), g * n))


def s4():
    k = R.choice(["comm", "un", "zero", "dix", "comm"])
    a, b = R.randint(2, 9), R.randint(2, 9)
    if k == "comm":
        if a == b:
            return None
        return mcq("%d %s %d = %d. Combien font %d %s %d ?" % (a, FOIS, b, a * b, b, FOIS, a), str(a * b), wr(a * b, a * b + a, a + b, a * b - b),
                   "On peut changer l’ordre : %d %s %d = %d %s %d = <b>%d</b>." % (b, FOIS, a, a, FOIS, b, a * b))
    if k == "un":
        return mcq("%d %s 1 = …" % (a, FOIS) if R.random() < 0.5 else "1 %s %d = …" % (FOIS, a), str(a), wr(a, a + 1, 1, 0),
                   "1 fois %d, c’est <b>%d</b>." % (a, a))
    if k == "zero":
        return mcq("%d %s 0 = …" % (a, FOIS) if R.random() < 0.5 else "0 %s %d = …" % (FOIS, a), "0", wr(0, a, 1, a + 1) if a != 1 else ["1", "2", "10"],
                   "0 groupe ou des groupes vides : il n’y a rien, <b>0</b>.")
    a = R.randint(2, 30)
    return mcq("%d %s 10 = …" % (a, FOIS), num(10 * a), [num(a + 10), num(100 * a), num(10 * a + 1)],
               "%d dizaines = <b>%s</b> : on écrit un 0 à droite." % (a, num(10 * a)))


def s5():
    p = K.next()
    k = R.choice(["roues", "boites", "rangees", "pattes", "euros", "paquets"])
    a, b = R.randint(2, 8), R.randint(2, 6)
    if k == "roues":
        return mcq("Un vélo a 2 roues. Combien de roues ont %d vélos ?" % a, str(2 * a), wr(2 * a, a + 2, 2 * a + 2, a), "%d %s 2 = <b>%d</b> roues." % (a, FOIS, 2 * a))
    if k == "pattes":
        return mcq("Un chat a 4 pattes. Combien de pattes ont %d chats ?" % a, str(4 * a), wr(4 * a, a + 4, 4 * a + 4, 4 * a - 1), "%d %s 4 = <b>%d</b> pattes." % (a, FOIS, 4 * a))
    if k == "boites":
        return mcq("%s a %d boîtes de %d crayons. Combien de crayons a-t-%s ?" % (p[0], a, b, p[1]), str(a * b), wr(a * b, a + b, a * b + b, a * b - 1), "%d %s %d = <b>%d</b> crayons." % (a, FOIS, b, a * b))
    if k == "rangees":
        return mcq("Dans la salle, il y a %d rangées de %d chaises. Combien de chaises en tout ?" % (a, b), str(a * b), wr(a * b, a + b, a * b + a, a * b - 1), "%d %s %d = <b>%d</b> chaises." % (a, FOIS, b, a * b))
    if k == "euros":
        return mcq("Un cahier coûte %d €. Combien coûtent %d cahiers ?" % (b, a), "%d €" % (a * b), ["%d €" % (a + b), "%d €" % (a * b + b), "%d €" % b],
                   "%d %s %d = <b>%d €</b>." % (a, FOIS, b, a * b))
    return mcq("Chaque paquet contient 10 biscuits. Combien de biscuits dans %d paquets ?" % a, str(10 * a), wr(10 * a, a + 10, 10 * a + 10, a), "%d %s 10 = <b>%d</b> biscuits." % (a, FOIS, 10 * a))


def main():
    seen = set()
    sets = [("Des groupes égaux", mix(R, seen, [(s1, 20)])), ("Des rangées et des colonnes", mix(R, seen, [(s2, 20)])),
            ("Addition répétée et signe ×", mix(R, seen, [(s3, 20)])), ("Changer l’ordre, × 1, × 0, × 10", mix(R, seen, [(s4, 20)])),
            ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = lesson(["Quand on a plusieurs <b>groupes égaux</b>, on peut multiplier : 3 groupes de 4, c’est 3 × 4.",
                   "3 × 4 = 4 + 4 + 4 = 12. On lit « 3 fois 4 ».",
                   "On peut changer l’ordre : 3 × 4 = 4 × 3. Et n × 1 = n, n × 0 = 0."],
                  [example("5 boîtes de 6 œufs", ["6 + 6 + 6 + 6 + 6", "5 × 6"], "30 œufs")],
                  [["Additionner les deux nombres : 4 × 3 = 7", "4 × 3, c’est 3 + 3 + 3 + 3 = 12."],
                   ["Écrire 3 + 4 pour 3 groupes de 4", "3 groupes de 4 : 4 + 4 + 4 = 3 × 4."],
                   ["Croire que 5 × 0 = 5", "5 groupes de rien, c’est 0."]])
    faq = [("Pourquoi 3 × 4 = 4 × 3 ?", "Un quadrillage de 3 rangées de 4 cases, tourné, devient 4 rangées de 3 : c’est le même nombre de cases."),
           ("Comment lire 6 × 7 ?", "« 6 fois 7 ».")]
    unit(1, R, "sens-de-la-multiplication", "N",
         "Comprendre le sens de la multiplication (groupes égaux, quadrillages, addition répétée) ; utiliser le signe × ; savoir que la multiplication est commutative ; résoudre des problèmes multiplicatifs",
         "Le sens de la multiplication", "Sens de la multiplication",
         "Fiches de maths CE1 sur le sens de la multiplication : groupes égaux, rangées, addition répétée, signe ×, × 1, × 0, × 10 et problèmes. 100 exercices corrigés.",
         "3 × 4 = 4 + 4 + 4", "3 groupes de 4 = 12", body, faq, sets, 18)


if __name__ == "__main__":
    main()
