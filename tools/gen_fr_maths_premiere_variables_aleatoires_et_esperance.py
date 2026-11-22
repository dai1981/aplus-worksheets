# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Variables aléatoires et espérance (loi de probabilité, P(X = a), P(X ⩾ a), espérance, jeu équitable, linéarité)
  python3 tools/gen_fr_maths_premiere_variables_aleatoires_et_esperance.py
Erreurs : somme des probabilités ≠ 1, moyenne des valeurs au lieu de l’espérance, gain sans retirer la mise, P(X > a) qui inclut a.
"""
import random
from fr_ly1 import *

R = random.Random(60622)


def law(n=None):
    n = n or R.choice([3, 4, 4, 5])
    xs = sorted(R.sample(range(-5, 11), n))
    cuts = sorted(R.sample(range(1, 20), n - 1))
    ps = [Fr(b - a, 20) for a, b in zip([0] + cuts, cuts + [20])]
    return xs, ps


def E_(xs, ps):
    return sum(x * p for x, p in zip(xs, ps))


def s1():
    xs, ps = law()
    i = R.randrange(len(xs))
    k = R.choice(["miss", "miss", "eq", "ge", "lt"])
    if k == "miss":
        shown = [d(p) if j != i else "p" for j, p in enumerate(ps)]
        return M("Voici la loi de X :%s Que vaut p ?" % loi(xs, shown), d(ps[i]), [d(1 - sum(ps) + ps[i] + Fr(1, 10)) if ps[i] + Fr(1, 10) <= 1 else d(ps[i] / 2), d(sum(ps) - ps[i]), d(Fr(1, len(xs)))],
                 "La somme des probabilités vaut 1 : p = 1 − %s = <b>%s</b>." % (d(1 - ps[i]), d(ps[i])))
    t = R.choice(xs[1:-1]) if len(xs) > 2 else xs[0]
    if k == "eq":
        return M("Voici la loi de X :%s Que vaut P(X = %s) ?" % (loi(xs, ps), d(t)), d(ps[xs.index(t)]), [d(t) if 0 <= t <= 1 else d(sum(ps[:xs.index(t)])) if sum(ps[:xs.index(t)]) else "0", d(sum(ps[xs.index(t):])), d(Fr(1, len(xs)))],
                 "On lit la case sous %s : <b>%s</b>." % (d(t), d(ps[xs.index(t)])))
    if k == "ge":
        v = sum(p for x, p in zip(xs, ps) if x >= t)
        return M("Voici la loi de X :%s Calcule P(X ⩾ %s)." % (loi(xs, ps), d(t)), d(v), [d(v - ps[xs.index(t)]), d(1 - v + ps[xs.index(t)]), d(ps[xs.index(t)])],
                 "On additionne les probabilités des valeurs ⩾ %s : <b>%s</b>." % (d(t), d(v)))
    v = sum(p for x, p in zip(xs, ps) if x < t)
    return M("Voici la loi de X :%s Calcule P(X &lt; %s)." % (loi(xs, ps), d(t)), d(v), [d(v + ps[xs.index(t)]), d(1 - v), d(ps[xs.index(t)]) if ps[xs.index(t)] != v else d(v / 2)],
             "On additionne les probabilités des valeurs strictement inférieures à %s : <b>%s</b>." % (d(t), d(v)))


def s2():
    k = R.choice(["de", "de", "urne", "piece"])
    if k == "de":
        g6, g = R.randint(3, 10), R.randint(0, 2)
        m = R.randint(1, 3)
        xs = sorted(set([g6 - m, g - m]))
        q = "On lance un dé équilibré à 6 faces. Si on obtient 6, on gagne %d € ; sinon, on gagne %s €. La mise est de %d €. X est le gain algébrique (gain − mise). Quelles sont les valeurs de X ?" % (g6, d(g), m)
        ans = "%s et %s" % (d(g - m), d(g6 - m))
        return M(q, ans, ["%s et %s" % (d(g), d(g6)), "%s, %s et %s" % (d(-m), d(g - m), d(g6 - m)) if g else "%s et %s" % (d(g6 - m), d(g6)), "%s et %s" % (d(g + m), d(g6 + m))],
                 "On retire la mise de chaque gain : <b>%s</b>." % ans)
    if k == "urne":
        r, b, v = R.randint(1, 5), R.randint(1, 5), R.randint(1, 5)
        n = r + b + v
        gr, gb = R.randint(2, 10), R.randint(1, 5)
        ans = fq(Fr(r, n))
        return M("Une urne contient %d boules rouges, %d bleues et %d vertes. On gagne %d € pour une rouge, %d € pour une bleue, 0 € pour une verte. X est le gain. Que vaut P(X = %d) ?" % (r, b, v, gr, gb, gr), ans,
                 [fq(Fr(1, 3)) if Fr(r, n) != Fr(1, 3) else fq(Fr(b, n)), fq(Fr(gr, n)) if Fr(gr, n) <= 1 and Fr(gr, n) != Fr(r, n) else fq(Fr(r, n - 1)), fq(Fr(r, b + v))],
                 "X = %d quand on tire une rouge : %d ÷ %d = <b>%s</b>." % (gr, r, n, ans))
    nb = R.choice([2, 3])
    k_ = R.randint(0, nb)
    from math import comb
    v = Fr(comb(nb, k_), 2 ** nb)
    return M("On lance %d pièces équilibrées. X est le nombre de « pile ». Que vaut P(X = %d) ?" % (nb, k_), fq(v), [fq(Fr(1, nb + 1)), fq(Fr(1, 2 ** nb)) if v != Fr(1, 2 ** nb) else fq(Fr(nb, 2 ** nb)), fq(Fr(k_, nb)) if Fr(k_, nb) != v else fq(Fr(1, 2))],
             "%d issues équiprobables, dont %d avec %d pile : <b>%s</b>." % (2 ** nb, comb(nb, k_), k_, fq(v)))


def s3():
    xs, ps = law()
    e = E_(xs, ps)
    return M("Voici la loi de X :%s Calcule l’espérance E(X)." % loi(xs, ps), d(e), [d(Fr(sum(xs), len(xs))) if Fr(sum(xs), len(xs)).denominator in (1, 2, 4, 5) else d(sum(xs)), d(sum(ps)) if e != 1 else "0", d(sum(x * x * p for x, p in zip(xs, ps))) if sum(x * x * p for x, p in zip(xs, ps)) != e else d(e + 1)],
             "E(X) = Σ x<sub>i</sub> × P(X = x<sub>i</sub>) = %s = <b>%s</b> (ce n’est pas la moyenne des valeurs)." % (" + ".join("%s × %s" % (par(x), d(p)) for x, p in zip(xs, ps)), d(e)))


def s4():
    k = R.choice(["equi", "equi", "lin", "lin2"])
    if k == "equi":
        n = R.choice([4, 5, 6, 8, 10])
        win = R.randint(1, n // 2)
        g = R.randint(2, 6)
        # gain algébrique : g − m avec proba win/n, −m sinon. E = g·win/n − m = 0
        m = Fr(g * win, n)
        q = "On tire une carte parmi %d, dont %d gagnante%s. Une carte gagnante rapporte %d € ; la mise est m €. Pour quelle valeur de m le jeu est-il équitable ?" % (n, win, "s" if win > 1 else "", g)
        return M(q, "m = " + euro(m), ["m = " + euro(g), "m = " + euro(Fr(g, n)) if Fr(g, n) != m else "m = " + euro(m + 1), "m = " + euro(g - m)],
                 "Équitable ⇔ E(X) = 0 : %d × %s − m = 0 ⇔ <b>m = %s</b>." % (g, fq(Fr(win, n)), euro(m)))
    xs, ps = law(3)
    e = E_(xs, ps)
    a, b = nz(R, -4, 4), R.randint(-6, 6)
    if k == "lin":
        return M("E(X) = %s. Calcule E(%s)." % (d(e), E((a, "X"), (b, ""))), d(a * e + b), [d(a * e), d(e + b), d(a * (e + b))],
                 "E(aX + b) = aE(X) + b = %s × %s %s = <b>%s</b>." % (d(a), par(e), ("+ %d" % b) if b >= 0 else "− %d" % -b, d(a * e + b)))
    e2 = R.randint(-5, 8)
    return M("Un jeu a un gain moyen E(X) = %s €. On double tous les gains et on ajoute un bonus de %d €. Quel est le nouveau gain moyen ?" % (d(e2), abs(b) + 1), euro(2 * e2 + abs(b) + 1),
             [euro(2 * e2), euro(e2 + abs(b) + 1), euro(2 * (e2 + abs(b) + 1))], "E(2X + %d) = 2 × %s + %d = <b>%s</b>." % (abs(b) + 1, par(e2), abs(b) + 1, euro(2 * e2 + abs(b) + 1)))


def s5():
    k = R.choice(["jeu", "jeu", "assur", "tombola"])
    if k == "jeu":
        mise = R.randint(1, 4)
        g6, g5 = R.randint(5, 15), R.randint(2, 6)
        xs = [g6 - mise, g5 - mise, -mise]
        ps = [Fr(1, 6), Fr(1, 6), Fr(4, 6)]
        e = E_(xs, ps)
        verdict = "favorable au joueur" if e > 0 else "défavorable au joueur" if e < 0 else "équitable"
        return M("On mise %d € puis on lance un dé : 6 rapporte %d €, 5 rapporte %d €, sinon rien. X est le gain algébrique. Calcule E(X) et conclus." % (mise, g6, g5), "E(X) = %s € : jeu %s" % (fq(e), verdict),
                 ["E(X) = %s € : jeu %s" % (fq(Fr(g6 + g5, 6)), "favorable au joueur"), "E(X) = %s € : jeu %s" % (fq(e), "favorable au joueur" if e <= 0 else "défavorable au joueur"), "E(X) = %s € : jeu %s" % (fq(Fr(sum(xs), 3)), "favorable au joueur" if sum(xs) > 0 else "défavorable au joueur")],
                 "E(X) = %s × %s + %s × %s + %s × %s = <b>%s €</b> : jeu %s." % (par(xs[0]), fq(ps[0]), par(xs[1]), fq(ps[1]), par(xs[2]), fq(ps[2]), fq(e), verdict))
    if k == "assur":
        p = R.choice([Fr(1, 100), Fr(2, 100), Fr(5, 1000), Fr(1, 1000)])
        c = R.choice([1000, 2000, 5000, 10000])
        prime = R.choice([30, 50, 80, 100, 120])
        e = prime - p * c
        return M("Une assurance encaisse %d € par client et rembourse %s € avec la probabilité %s. Quel est le gain moyen de l’assurance par client ?" % (prime, num(c), d(p)), euro(e),
                 [euro(prime), euro(p * c), euro(prime + p * c)], "E = %d − %s × %s = <b>%s</b>." % (prime, d(p), num(c), euro(e)))
    n = R.choice([100, 200, 500])
    lots = [(R.choice([50, 100]), 1), (R.choice([10, 20]), R.randint(2, 5)), (R.choice([2, 5]), R.randint(5, 15))]
    prix = R.choice([1, 2, 3])
    tot = sum(v * k_ for v, k_ in lots)
    e = Fr(tot, n) - prix
    return M("Une tombola vend %d billets à %d € : 1 lot de %d €, %d lots de %d € et %d lots de %d €. Quelle est l’espérance du gain algébrique d’un billet ?" % (n, prix, lots[0][0], lots[1][1], lots[1][0], lots[2][1], lots[2][0]), euro(e),
             [euro(Fr(tot, n)), euro(e + prix * 2) if e + 2 * prix != Fr(tot, n) else euro(-prix), euro(Fr(tot, 3) - prix) if Fr(tot, 3).denominator in (1, 2, 4, 5, 10) else euro(-e)],
             "Gain moyen des lots : %d ÷ %d = %s ; on retire le prix du billet : <b>%s</b>." % (tot, n, d(Fr(tot, n)), euro(e)))


def main():
    seen = set()
    sets = [("Loi de probabilité", mix(R, seen, [(s1, 20)])), ("Définir une variable aléatoire", mix(R, seen, [(s2, 20)])),
            ("Calculer l’espérance", mix(R, seen, [(s3, 20)])), ("Jeu équitable et linéarité", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une <b>variable aléatoire</b> X associe un nombre à chaque issue d’une expérience aléatoire. Sa <b>loi</b> donne P(X = x<sub>i</sub>) pour chaque valeur ; la somme de ces probabilités vaut 1.",
              "L’<b>espérance</b> E(X) = x<sub>1</sub>p<sub>1</sub> + x<sub>2</sub>p<sub>2</sub> + … + x<sub>n</sub>p<sub>n</sub> est la valeur moyenne de X sur un grand nombre de répétitions.",
              "Un jeu est <b>équitable</b> si l’espérance du gain algébrique (gain − mise) est nulle. Linéarité : E(aX + b) = aE(X) + b."],
             [("X prend −2, 1, 5 avec les probabilités 0,5 ; 0,3 ; 0,2", ["E(X) = −2 × 0,5 + 1 × 0,3 + 5 × 0,2 = 0,3"], "en moyenne, on gagne 0,30 € par partie")],
             [["E(X) = moyenne des valeurs", "On pondère chaque valeur par sa probabilité."], ["Gain = somme gagnée", "Gain algébrique = somme gagnée − mise."], ["P(X &gt; 2) inclut X = 2", "« &gt; » exclut 2 ; « ⩾ » l’inclut."]])
    faq = [("Que signifie E(X) = −0,5 € pour un jeu ?", "Sur un grand nombre de parties, le joueur perd en moyenne 0,50 € par partie : le jeu est défavorable au joueur."),
           ("L’espérance est-elle une valeur que X peut prendre ?", "Pas forcément : c’est une moyenne. Par exemple, le nombre moyen de « pile » en un lancer est 0,5.")]
    unit("premiere", R, "variables-aleatoires-et-esperance", "S",
         "Variable aléatoire réelle sur un univers fini, loi de probabilité ; calculer P(X = a), P(X ⩽ a) ; espérance d’une variable aléatoire ; linéarité de l’espérance ; jeu équitable",
         "Variables aléatoires, loi et espérance", "Variables aléatoires",
         "Fiches de maths première sur les variables aléatoires : loi de probabilité, P(X = a), espérance, jeu équitable, linéarité et problèmes. 100 exercices corrigés.",
         "E(X) = Σ x × P(X = x)", "Jeu équitable : E(gain) = 0", body, faq, sets, 22)


if __name__ == "__main__":
    main()
