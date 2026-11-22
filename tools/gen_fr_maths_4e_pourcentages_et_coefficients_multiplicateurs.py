# -*- coding: utf-8 -*-
"""
France Maths 4e : Pourcentages et coefficients multiplicateurs
  python3 tools/gen_fr_maths_4e_pourcentages_et_coefficients_multiplicateurs.py
Erreurs : augmenter de 20 % = × 0,2 ou × 20, +10 % puis −10 % = 0 %, retrouver le prix initial en enlevant le pourcentage.
"""
import random
from fr_c4 import *

R = random.Random(60309)
K = Kids(R)
T = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 2, 3, 8, 12, 35]


def pc(t):
    return "%s %%" % d(t)


def s1():
    t = R.choice(T)
    x = R.choice([40, 60, 80, 120, 150, 200, 240, 300, 360, 500, 1200])
    r = Fr(t * x, 100)
    if (r * 100).denominator != 1:
        return None
    k = R.choice(["de", "part"])
    if k == "de":
        return M("Calcule %s de %s." % (pc(t), num(x)), d(r), [d(Fr(x, t)) if (Fr(x, t) * 100).denominator == 1 else d(r * 10), d(x - r), d(t * x)], "%s × %s = %s ÷ 100 × %s = <b>%s</b>." % (pc(t), num(x), d(t), num(x), d(r)))
    tot = R.choice([20, 25, 40, 50, 80, 200, 400])
    n = R.randint(1, tot - 1)
    q = Fr(n * 100, tot)
    if (q * 10).denominator != 1:
        return None
    return M("Quel pourcentage représente %s sur %d ?" % (n, tot), pc(q), [pc(n), pc(Fr(tot, n) * 100) if (Fr(tot, n) * 1000).denominator == 1 and tot != n else pc(q + 10), pc(100 - q)],
             "%d ÷ %d = %s = <b>%s</b>." % (n, tot, d(Fr(n, tot)), pc(q)))


def s2():
    t = R.choice(T)
    up = R.random() < 0.5
    k = R.choice(["coef", "coef", "inv"])
    c = 1 + Fr(t, 100) if up else 1 - Fr(t, 100)
    if k == "coef":
        return M("%s de %s revient à multiplier par…" % ("Augmenter" if up else "Diminuer", pc(t)), d(c), [d(Fr(t, 100)), d(1 - Fr(t, 100)) if up else d(1 + Fr(t, 100)), d(t)],
                 "%s : 1 %s %s = <b>%s</b>." % ("Augmenter" if up else "Diminuer", "+" if up else MINUS, d(Fr(t, 100)), d(c)))
    return M("Multiplier par %s revient à…" % d(c), "%s de %s" % ("augmenter" if up else "diminuer", pc(t)),
             ["%s de %s" % ("diminuer" if up else "augmenter", pc(t)), "%s de %s" % ("augmenter" if up else "diminuer", pc(c * 100)), "prendre %s" % pc(t)],
             "%s = 1 %s %s : on <b>%s de %s</b>." % (d(c), "+" if up else MINUS, d(Fr(t, 100)), "augmente" if up else "diminue", pc(t)))


def s3():
    t = R.choice(T)
    x = R.choice([20, 40, 60, 80, 120, 150, 200, 250, 300, 450, 800])
    up = R.random() < 0.5
    c = 1 + Fr(t, 100) if up else 1 - Fr(t, 100)
    r = x * c
    if (r * 100).denominator != 1:
        return None
    k = R.choice(["fin", "fin", "fin", "init"])
    if k == "fin":
        return M("Un article coûte %s. Son prix %s de %s. Quel est son nouveau prix ?" % (euro(x), "augmente" if up else "baisse", pc(t)), euro(r),
                 [euro(x * Fr(t, 100)), euro(x * (2 - c)), euro(x + t if up else x - t) if x - t > 0 else euro(r + 1)],
                 "%s × %s = <b>%s</b>." % (em(x), d(c), euro(r)))
    w = r * (2 - c)
    return M("Après une %s de %s, un article coûte %s. Quel était son prix de départ ?" % ("hausse" if up else "baisse", pc(t), euro(r)), euro(x),
             [euro(w) if (w * 100).denominator == 1 else euro(x + 1), euro(r - t if up else r + t), euro(r * c) if (r * c * 100).denominator == 1 else euro(x + 2)],
             "Prix de départ × %s = %s, donc prix de départ = %s ÷ %s = <b>%s</b>. (On ne retire pas %s du prix final.)" % (d(c), em(r), em(r), d(c), euro(x), pc(t)))


def s4():
    k = R.choice(["succ", "succ", "evol", "evol", "piege"])
    if k == "succ":
        a, b = R.choice(T[:10]), R.choice(T[:10])
        ua, ub = R.random() < 0.5, R.random() < 0.5
        ca = 1 + Fr(a, 100) if ua else 1 - Fr(a, 100)
        cb = 1 + Fr(b, 100) if ub else 1 - Fr(b, 100)
        c = ca * cb
        t = (c - 1) * 100
        if t == 0 or (t * 100).denominator != 1:
            return None
        naive = (a if ua else -a) + (b if ub else -b)
        ans = "%s de %s" % ("hausse" if t > 0 else "baisse", pc(abs(t)))
        wn = "%s de %s" % ("hausse" if naive > 0 else "baisse", pc(abs(naive))) if naive else "aucune évolution"
        if wn == ans:
            return None
        return M("Un prix %s de %s, puis %s de %s. Quelle est l’évolution globale ?" % ("augmente" if ua else "baisse", pc(a), "augmente" if ub else "baisse", pc(b)), ans,
                 [wn, "%s de %s" % ("baisse" if t > 0 else "hausse", pc(abs(t))), "%s de %s" % ("hausse" if t > 0 else "baisse", pc(abs(c * 100)))],
                 "Coefficient global : %s × %s = %s, soit une <b>%s</b>. (Les pourcentages ne s’additionnent pas.)" % (d(ca), d(cb), d(c), ans))
    if k == "evol":
        x = R.choice([40, 50, 80, 120, 200, 250, 400])
        t = R.choice(T)
        up = R.random() < 0.5
        y = x * (1 + Fr(t, 100) if up else 1 - Fr(t, 100))
        if (y * 100).denominator != 1:
            return None
        ans = "%s de %s" % ("hausse" if up else "baisse", pc(t))
        return M("Un prix passe de %s à %s. Quel est le pourcentage d’évolution ?" % (euro(x), euro(y)), ans,
                 ["%s de %s" % ("hausse" if up else "baisse", pc(abs(y - x))) if abs(y - x) != t else "%s de %s" % ("hausse" if up else "baisse", pc(t * 2)), "%s de %s" % ("baisse" if up else "hausse", pc(t)), "%s de %s" % ("hausse" if up else "baisse", pc(Fr(abs(y - x) * 100, y))) if (Fr(abs(y - x) * 100, y) * 100).denominator == 1 and Fr(abs(y - x) * 100, y) != t else "%s de %s" % ("hausse" if up else "baisse", pc(t + 5))],
                 "Coefficient : %s ÷ %s = %s, soit une <b>%s</b>." % (em(y), em(x), d(y / x), ans))
    V = [("Un prix augmente de 10 % puis baisse de 10 %. Revient-il à son prix de départ ?", "non, il baisse de 1 %", ["oui", "non, il augmente de 1 %", "non, il baisse de 10 %"]),
         ("Un prix augmente de 100 %. Que devient-il ?", "il double", ["il ne change pas", "il est multiplié par 100", "il devient nul"]),
         ("Un prix baisse de 50 % puis de 50 %. Quelle est la baisse totale ?", "75 %", ["100 %", "50 %", "25 %"]),
         ("Un prix est multiplié par 2,5. De quel pourcentage a-t-il augmenté ?", "150 %", ["250 %", "25 %", "2,5 %"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>. On raisonne avec les coefficients multiplicateurs." % a)


def s5():
    p = K.next()
    k = R.choice(["solde", "salaire", "tva", "pop", "eleves"])
    if k == "solde":
        x = R.choice([35, 48, 60, 79, 90, 120])
        t = R.choice([20, 30, 40, 50])
        r = x * (1 - Fr(t, 100))
        return M("Pendant les soldes, un jean à %s est affiché à −%s. Combien %s paie-t-%s ?" % (euro(x), pc(t), p[0], p[1]), euro(r), [euro(x * Fr(t, 100)), euro(x - t), euro(x * (1 + Fr(t, 100)))],
                 "%s × %s = <b>%s</b>." % (em(x), d(1 - Fr(t, 100)), euro(r)))
    if k == "salaire":
        x = R.choice([1500, 1800, 2000, 2400])
        t = R.choice([2, 3, 4, 5])
        r = x * (1 + Fr(t, 100))
        return M("Un salaire de %s augmente de %s. Quel est le nouveau salaire ?" % (euro(x), pc(t)), euro(r), [euro(x + t), euro(x * Fr(t, 100)), euro(x * (1 + Fr(t, 10)))],
                 "%s × %s = <b>%s</b>." % (num(x), d(1 + Fr(t, 100)), euro(r)))
    if k == "tva":
        ht = R.choice([50, 80, 100, 150, 250, 400])
        ttc = ht * Fr(12, 10)
        if R.random() < 0.5:
            return M("Un article coûte %s hors taxes. La TVA est de 20 %%. Quel est son prix TTC ?" % euro(ht), euro(ttc), [euro(ht + 20), euro(ht * Fr(2, 10)), euro(ht * Fr(8, 10))], "%s × 1,2 = <b>%s</b>." % (em(ht), euro(ttc)))
        return M("Un article coûte %s TTC (TVA à 20 %%). Quel est son prix hors taxes ?" % euro(ttc), euro(ht), [euro(ttc * Fr(8, 10)), euro(ttc - 20), euro(ttc * Fr(2, 10))],
                 "Prix HT × 1,2 = %s, donc prix HT = %s ÷ 1,2 = <b>%s</b>." % (em(ttc), em(ttc), euro(ht)))
    if k == "pop":
        x = R.choice([2000, 5000, 8000, 12000, 20000])
        t = R.choice([5, 10, 20])
        r = x * (1 + Fr(t, 100)) ** 2
        if r.denominator != 1:
            return None
        return M("Une ville de %s habitants voit sa population augmenter de %s par an pendant 2 ans. Combien d’habitants a-t-elle ensuite ?" % (num(x), pc(t)), num(r), [num(x * (1 + Fr(2 * t, 100))), num(x * (1 + Fr(t, 100))), num(x + 2 * t)],
                 "%s × %s × %s = <b>%s</b>." % (num(x), d(1 + Fr(t, 100)), d(1 + Fr(t, 100)), num(r)))
    tot = R.choice([400, 500, 600, 800])
    t = R.choice([15, 25, 35, 45, 55])
    n = tot * t // 100
    return M("Un collège a %d élèves dont %d sont demi-pensionnaires. Quel pourcentage cela représente-t-il ?" % (tot, n), pc(t), [pc(n), pc(100 - t), pc(Fr(n, 10)) if Fr(n, 10) != t else pc(t + 5)],
             "%d ÷ %d = %s = <b>%s</b>." % (n, tot, d(Fr(t, 100)), pc(t)))


def main():
    seen = set()
    sets = [("Calculer un pourcentage", mix(R, seen, [(s1, 20)])), ("Coefficients multiplicateurs", mix(R, seen, [(s2, 20)])),
            ("Hausses, baisses et prix de départ", mix(R, seen, [(s3, 20)])), ("Évolutions successives", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Prendre t % d’une quantité, c’est la multiplier par t ÷ 100.",
              "Augmenter de t %, c’est multiplier par <b>1 + t/100</b> ; diminuer de t %, c’est multiplier par <b>1 − t/100</b>.",
              "Pour des évolutions successives, on multiplie les coefficients. Pour retrouver une valeur de départ, on divise par le coefficient."],
             [("Prix 80 €, hausse de 15 %", ["coefficient 1,15", "80 × 1,15"], "92 €"), ("Après −20 %, 64 €", ["64 ÷ 0,8"], "80 €")],
             [["Augmenter de 20 %, c’est multiplier par 0,2", "On multiplie par 1,2."], ["+10 % puis −10 % : on revient au départ", "1,1 × 0,9 = 0,99 : baisse de 1 %."],
              ["Retrouver le prix avant −20 % en ajoutant 20 % au prix final", "On divise par 0,8."]])
    faq = [("Pourquoi utiliser un coefficient multiplicateur ?", "Il fait tout en une seule multiplication et permet d’enchaîner plusieurs évolutions facilement."),
           ("Comment calculer un pourcentage d’évolution ?", "On divise la valeur d’arrivée par la valeur de départ : un coefficient de 1,25 correspond à +25 %, un coefficient de 0,7 à −30 %.")]
    unit("4e", R, "pourcentages-et-coefficients-multiplicateurs", "F",
         "Calculer et appliquer un pourcentage ; associer une augmentation ou une diminution de t % à une multiplication par 1 + t/100 ou 1 − t/100 ; calculer une valeur de départ ; calculer un pourcentage d’évolution et des évolutions successives",
         "Pourcentages et coefficients multiplicateurs", "Pourcentages et coefficients",
         "Fiches de maths 4e sur les pourcentages : calculer un pourcentage, coefficient multiplicateur, hausses et baisses, prix de départ, évolutions successives. 100 exercices corrigés.",
         "+t % → × (1 + t/100) ; −t % → × (1 − t/100)", "Les évolutions successives se multiplient", body, faq, sets, 9)


if __name__ == "__main__":
    main()
