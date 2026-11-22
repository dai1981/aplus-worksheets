# -*- coding: utf-8 -*-
"""
France Maths 5e : Pourcentages et proportions
  python3 tools/gen_fr_maths_5e_pourcentages_et_proportions.py
Appliquer un pourcentage, calculer une proportion et l’exprimer en pourcentage, écrire une proportion sous forme de fraction, décimal ou %,
problèmes (votes, soldes, composition).
Erreurs : 30 % de 50 = 30, 12 sur 40 = 12 %, 0,4 = 4 %.
"""
import random
from fr_c4 import *

R = random.Random(60209)
K = Kids(R)


def s1():
    pc = R.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 12, 35])
    n = R.choice([20, 40, 60, 80, 120, 150, 200, 240, 300, 360, 500, 1200])
    r = Fr(pc * n, 100)
    if r.denominator != 1:
        return None
    return M("Calcule %d %% de %s." % (pc, num(n)), d(r), [str(pc), d(n - r) if n - r != r else d(r + 1), d(Fr(n, pc)) if Fr(n, pc).denominator == 1 and Fr(n, pc) != r else d(r * 10)],
             "%d %% de %s = %s × %d ÷ 100 = <b>%s</b>." % (pc, num(n), num(n), pc, d(r)))


def s2():
    tot = R.choice([20, 25, 40, 50, 200, 400, 500, 80])
    pc = R.choice([10, 20, 25, 30, 40, 60, 75, 5, 15, 35, 45, 80])
    part = Fr(pc * tot, 100)
    if part.denominator != 1:
        return None
    return M("%s sur %s %s choisi le théâtre. Quel pourcentage cela représente-t-il ?" % (pl(part, "élève"), num(tot), "a" if part == 1 else "ont"), "%d %%" % pc, ["%s %%" % d(part), "%d %%" % (100 - pc), "%s %%" % d(Fr(tot, part)) if Fr(tot, part).denominator == 1 else "%d %%" % (pc + 10)],
             "%s ÷ %s = %s = <b>%d %%</b>." % (d(part), num(tot), d(Fr(pc, 100)), pc))


def s3():
    k = R.choice(["f2p", "d2p", "p2d", "p2f"])
    fs = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (3, 20)]
    a, b = R.choice(fs)
    pc = Fr(a * 100, b)
    if k == "f2p":
        return M("%s = … %%" % fr(a, b), "%s %%" % d(pc), ["%d %%" % (a * 10 + b) if a * 10 + b != pc else "%d %%" % (pc + 5), "%s %%" % d(Fr(b * 100, a)) if Fr(b * 100, a).denominator == 1 and Fr(b * 100, a) <= 2000 else "%d %%" % a, "%d %%" % a],
                 "%s = %s = <b>%s %%</b>." % (fr(a, b), fr(int(pc), 100), d(pc)))
    if k == "d2p":
        return M("%s = … %%" % d(Fr(a, b)), "%s %%" % d(pc), ["%s %%" % d(Fr(a, b) * 10), "%s %%" % d(Fr(a, b)), "%s %%" % d(pc * 10)],
                 "%s = %s centièmes = <b>%s %%</b>." % (d(Fr(a, b)), d(pc), d(pc)))
    if k == "p2d":
        return M("%s %% = … (écriture décimale)" % d(pc), d(Fr(a, b)), [d(pc), d(Fr(a, b) * 10), d(Fr(a, b) / 10)],
                 "%s %% = %s ÷ 100 = <b>%s</b>." % (d(pc), d(pc), d(Fr(a, b))))
    return M("%s %% = … (fraction la plus simple)" % d(pc), fr(a, b), [fr(int(pc), 10) if pc.denominator == 1 else fr(1, 3), fr(b, a), fr(a, 100)],
             "%s %% = %s = <b>%s</b>." % (d(pc), fr(d(pc), 100), fr(a, b)))


def s4():
    p = K.next()
    k = R.choice(["vote", "classe", "sondage"])
    if k == "vote":
        tot = R.choice([200, 400, 500, 800, 1000, 1200])
        a = R.randint(20, 60) * tot // 100
        pc = Fr(a * 100, tot)
        return M("À une élection, %s personnes ont voté. Une candidate a obtenu %s voix. Quel pourcentage des voix a-t-elle obtenu ?" % (num(tot), num(a)), "%s %%" % d(pc),
                 ["%s %%" % d(Fr(a, 10)), "%s %%" % d(100 - pc), "%s %%" % d(Fr(a, tot))], "%s ÷ %s × 100 = <b>%s %%</b>." % (num(a), num(tot), d(pc)))
    if k == "classe":
        tot = R.choice([20, 25])
        f = R.randint(5, tot - 5)
        pc = Fr(f * 100, tot)
        return M("Dans une classe de %d élèves, il y a %d filles. Quel est le pourcentage de filles ?" % (tot, f), "%s %%" % d(pc), ["%d %%" % f, "%s %%" % d(100 - pc), "%s %%" % d(Fr(f, tot))],
                 "%d ÷ %d = %s = <b>%s %%</b>." % (f, tot, d(Fr(f, tot)), d(pc)))
    tot = R.choice([50, 200, 400, 500])
    pc = R.choice([12, 18, 24, 36, 42, 64])
    return M("Sur %d personnes interrogées, %d %% préfèrent le vélo. Combien de personnes cela fait-il ?" % (tot, pc), d(Fr(tot * pc, 100)), [str(pc), d(Fr(tot * (100 - pc), 100)), d(Fr(tot * pc, 10))],
             "%d × %d ÷ 100 = <b>%s</b>." % (tot, pc, d(Fr(tot * pc, 100))))


def s5():
    p = K.next()
    k = R.choice(["solde", "hausse", "compo", "reste"])
    n = R.choice([20, 40, 50, 60, 80, 120, 150, 200])
    pc = R.choice([10, 20, 25, 30, 50])
    r = Fr(n * pc, 100)
    if k == "solde":
        return M("Un jean coûte %d €. Il est soldé à −%d %%. Quel est son nouveau prix ?" % (n, pc), euro(n - r), [euro(r), euro(n - pc), euro(n + r)],
                 "Réduction : %d %% de %d = %s € ; %d − %s = <b>%s</b>." % (pc, n, d(r), n, d(r), euro(n - r)))
    if k == "hausse":
        return M("Un abonnement coûte %d €. Son prix augmente de %d %%. Quel est son nouveau prix ?" % (n, pc), euro(n + r), [euro(n + pc), euro(r), euro(n - r)],
                 "Hausse : %d %% de %d = %s € ; %d + %s = <b>%s</b>." % (pc, n, d(r), n, d(r), euro(n + r)))
    if k == "compo":
        g = R.choice([200, 250, 400, 500])
        pc = R.choice([10, 20, 30, 40, 5])
        return M("Un yaourt de %d g contient %d %% de fruits. Quelle masse de fruits contient-il ?" % (g, pc), "%s g" % d(Fr(g * pc, 100)), ["%d g" % pc, "%s g" % d(g - Fr(g * pc, 100)), "%s g" % d(Fr(g * pc, 10))],
                 "%d × %d ÷ 100 = <b>%s g</b>." % (g, pc, d(Fr(g * pc, 100))))
    tot = R.choice([300, 400, 500])
    a, b = R.choice([(20, 30), (25, 35), (40, 15), (10, 45)])
    return M("Un livre a %d pages. %s en a lu %d %% lundi et %d %% mardi. Combien de pages lui reste-t-il à lire ?" % (tot, p[0], a, b), str(tot * (100 - a - b) // 100),
             [str(100 - a - b), str(tot * (a + b) // 100), str(tot - a - b)], "%d %% + %d %% = %d %% ; il reste %d %% de %d = <b>%d</b> pages." % (a, b, a + b, 100 - a - b, tot, tot * (100 - a - b) // 100))


def main():
    seen = set()
    sets = [("Appliquer un pourcentage", mix(R, seen, [(s1, 20)])), ("Calculer un pourcentage", mix(R, seen, [(s2, 20)])),
            ("Fraction, décimal, pourcentage", mix(R, seen, [(s3, 20)])), ("Proportions dans une population", mix(R, seen, [(s4, 20)])), ("Hausses, baisses et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["t % d’une quantité, c’est t centièmes de cette quantité : 30 % de 50 = 50 × 30 ÷ 100 = 15.",
              "Pour exprimer une proportion en pourcentage, on divise la partie par le tout puis on multiplie par 100 : 12 sur 40 = 0,3 = 30 %.",
              "Une même proportion s’écrit de plusieurs façons : %s = 0,75 = 75 %%." % fr(3, 4)],
             [("18 élèves sur 24", ["18 ÷ 24 = 0,75"], "75 %")],
             [["30 % de 50 = 30", "30 % de 50 = 15."], ["12 sur 40 = 12 %", "12 ÷ 40 = 0,3 = 30 %."], ["0,4 = 4 %", "0,4 = 40 centièmes = 40 %."]])
    faq = [("Comment calculer 10 % de tête ?", "On divise par 10. Pour 20 %, on double ; pour 5 %, on prend la moitié de 10 %."),
           ("Un pourcentage peut-il dépasser 100 % ?", "Oui, pour une hausse ou une comparaison, mais pas pour une partie d’un tout.")]
    unit("5e", R, "pourcentages-et-proportions", "F",
         "Utiliser les proportions et les pourcentages : appliquer un pourcentage, calculer une proportion et l’exprimer sous forme de fraction, de décimal ou de pourcentage ; résoudre des problèmes",
         "Pourcentages et proportions", "Pourcentages",
         "Fiches de maths 5e sur les pourcentages : appliquer un pourcentage, calculer une proportion, fraction, décimal et pourcentage, soldes et problèmes. 100 exercices corrigés.",
         "t % de N = N × t ÷ 100", "%s = 0,75 = 75 %%" % fr(3, 4), body, faq, sets, 9)


if __name__ == "__main__":
    main()
