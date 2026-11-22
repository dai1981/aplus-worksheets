# -*- coding: utf-8 -*-
"""
France Maths Seconde : Proportions, pourcentages de pourcentages, évolutions (variation absolue, relative, coefficient multiplicateur, successives, réciproques)
  python3 tools/gen_fr_maths_seconde_pourcentages_et_evolutions.py
Erreurs : additionner les pourcentages successifs, évolution réciproque = même pourcentage, variation relative divisée par la valeur d’arrivée.
"""
import random
from fr_c4 import *

R = random.Random(60517)
K = Kids(R)


def pc(t):
    return "%s %%" % d(t)


def s1():
    k = R.choice(["prop", "prop", "pp", "eff"])
    if k == "prop":
        n = R.choice([200, 250, 400, 500, 800, 1200])
        m = n * R.choice([5, 12, 15, 24, 35, 40, 64]) // 100
        return M("Dans un lycée de %s élèves, %s sont externes. Quelle est la proportion d’externes, en pourcentage ?" % (num(n), num(m)), pc(Fr(m * 100, n)), [pc(Fr(m, 10)) if Fr(m, 10) != Fr(m * 100, n) else pc(m), pc(100 - Fr(m * 100, n)), pc(Fr(n, m) * 10) if (Fr(n, m) * 100).denominator == 1 else pc(Fr(m * 100, n) + 5)],
                 "p = %s ÷ %s = %s = <b>%s</b>." % (num(m), num(n), d(Fr(m, n)), pc(Fr(m * 100, n))))
    if k == "pp":
        a, b = R.choice([40, 50, 60, 25, 30]), R.choice([10, 20, 25, 30, 40, 50])
        return M("%d %% des élèves sont des filles, et %d %% des filles font du sport en club. Quel pourcentage des élèves sont des filles en club ?" % (a, b), pc(Fr(a * b, 100)), [pc(a + b), pc(Fr(a + b, 2)), pc(Fr(b * 100, a)) if Fr(b * 100, a).denominator == 1 and Fr(b * 100, a) <= 100 else pc(a - b if a > b else b - a)],
                 "%d %% de %d %% = %s × %s = %s = <b>%s</b>." % (b, a, d(Fr(b, 100)), d(Fr(a, 100)), d(Fr(a * b, 10000)), pc(Fr(a * b, 100))))
    p = R.choice([15, 20, 25, 30, 35, 45])
    n = R.choice([20, 40, 60, 80])
    m = n * p // 100
    if n * p % 100:
        return None
    return M("%d élèves représentent %d %% d’une promotion. Combien y a-t-il d’élèves dans la promotion ?" % (m, p), str(n), [str(m * p // 10) if (m * p) % 10 == 0 else str(n + 10), str(m + p), str(Fr(m * 100, 100 - p)) if Fr(m * 100, 100 - p).denominator == 1 else str(n - 5)],
             "Effectif total = %d ÷ %s = <b>%d</b>." % (m, d(Fr(p, 100)), n))


def s2():
    v1 = R.choice([40, 50, 80, 120, 150, 200, 250, 400])
    t = R.choice([5, 10, 15, 20, 25, 30, 40, 60]) * R.choice([1, -1])
    v2 = v1 * (100 + t) // 100
    if v1 * (100 + t) % 100:
        return None
    k = R.choice(["abs", "rel", "rel", "cm"])
    if k == "abs":
        return M("Une valeur passe de %d à %d. Quelle est la variation absolue ?" % (v1, v2), d(v2 - v1), [d(v1 - v2), pc(t), d(Fr(v2, v1))], "V₂ − V₁ = %d − %d = <b>%s</b>." % (v2, v1, d(v2 - v1)))
    if k == "rel":
        return M("Une valeur passe de %d à %d. Quelle est la variation relative (taux d’évolution) ?" % (v1, v2), pc(t), [pc(Fr((v2 - v1) * 100, v2)) if (Fr((v2 - v1) * 100, v2) * 100).denominator == 1 else pc(t * 2), pc(-t), pc(v2 - v1) if v2 - v1 != t else pc(t + 10)],
                 "(V₂ − V₁) ÷ V₁ = %s ÷ %d = %s = <b>%s</b>." % (d(v2 - v1), v1, d(Fr(t, 100)), pc(t)))
    return M("Une valeur passe de %d à %d. Quel est le coefficient multiplicateur ?" % (v1, v2), d(Fr(v2, v1)), [d(Fr(v1, v2)) if (Fr(v1, v2) * 10000).denominator == 1 else d(Fr(t, 100)), d(Fr(t, 100)), d(Fr(abs(t), 100) + 1) if t < 0 else d(1 - Fr(t, 100))],
             "CM = V₂ ÷ V₁ = <b>%s</b> (soit %s)." % (d(Fr(v2, v1)), ("+" if t > 0 else MINUS) + pc(abs(t))))


def s3():
    a, b = R.choice([10, 20, 25, 30, 40, 50]), R.choice([10, 20, 25, 30, 40, 50])
    ua, ub = R.random() < 0.5, R.random() < 0.5
    ca, cb = 1 + Fr(a if ua else -a, 100), 1 + Fr(b if ub else -b, 100)
    c = ca * cb
    t = (c - 1) * 100
    if t == 0:
        return None
    ans = ("+" if t > 0 else MINUS) + pc(abs(t))
    naive = (a if ua else -a) + (b if ub else -b)
    wn = ("+" if naive > 0 else MINUS) + pc(abs(naive)) if naive else "0 %"
    if wn == ans:
        return None
    return M("Un prix évolue de %s%d %%, puis de %s%d %%. Quelle est l’évolution globale ?" % ("+" if ua else MINUS, a, "+" if ub else MINUS, b), ans, [wn, ("+" if t < 0 else MINUS) + pc(abs(t)), ("+" if t > 0 else MINUS) + pc(abs(c * 100))],
             "CM global = %s × %s = %s : <b>%s</b>." % (d(ca), d(cb), d(c), ans))


def s4():
    up = R.random() < 0.5
    t = R.choice([25, 60, 100, 150, 300, 400]) if up else R.choice([20, 50, 75, 80, 60, 36, 90])
    c = 1 + Fr(t if up else -t, 100)
    r = 1 / c
    tr = (r - 1) * 100
    if (tr * 100).denominator != 1:
        return None
    ans = ("+" if tr > 0 else MINUS) + pc(abs(tr))
    return M("Après une évolution de %s%d %%, quelle évolution permet de revenir à la valeur de départ ?" % ("+" if up else MINUS, t), ans, [(MINUS if up else "+") + pc(t), ("+" if tr > 0 else MINUS) + pc(abs(tr) + 5), (MINUS if up else "+") + pc(t * 2) if t * 2 <= 100 else MINUS + "50 %"],
             "CM réciproque = 1 ÷ %s = %s : <b>%s</b>." % (d(c), d(r), ans))


def s4b():
    p0 = R.choice([40, 60, 80, 120, 160, 200, 240, 300, 500])
    t = R.choice([10, 20, 25, 40, 50])
    up = R.random() < 0.5
    p1 = p0 * (1 + Fr(t if up else -t, 100))
    if (p1 * 100).denominator != 1:
        return None
    return M("Après une %s de %d %%, une valeur vaut %s. Quelle était la valeur de départ ?" % ("hausse" if up else "baisse", t, d(p1)), d(p0), [d(p1 * (1 - Fr(t if up else -t, 100))), d(p1 - t if up else p1 + t), d(p1 * (1 + Fr(t if up else -t, 100)))],
             "V₁ = V₂ ÷ CM = %s ÷ %s = <b>%s</b>." % (d(p1), d(1 + Fr(t if up else -t, 100)), d(p0)))


def s5():
    k = R.choice(["solde", "pop", "prix_init", "taux_moy"])
    if k == "solde":
        p = R.choice([60, 80, 120, 150])
        a, b = R.choice([(30, 20), (20, 10), (50, 20), (40, 25)])
        r = p * (1 - Fr(a, 100)) * (1 - Fr(b, 100))
        return M("Un manteau à %d € est soldé de %d %%, puis on applique une remise supplémentaire de %d %%. Quel est le prix final ?" % (p, a, b), euro(r), [euro(p * (1 - Fr(a + b, 100))), euro(p * (1 - Fr(a, 100))), euro(p - a - b)],
                 "%d × %s × %s = <b>%s</b>." % (p, d(1 - Fr(a, 100)), d(1 - Fr(b, 100)), euro(r)))
    if k == "pop":
        n = R.choice([10000, 20000, 50000])
        t = R.choice([2, 5, 10])
        y = R.choice([2, 3])
        r = n * (1 + Fr(t, 100)) ** y
        if r.denominator != 1:
            return None
        return M("Une ville de %s habitants voit sa population augmenter de %d %% par an pendant %d ans. Combien d’habitants a-t-elle ensuite ?" % (num(n), t, y), num(r), [num(n * (1 + Fr(t * y, 100))), num(n * (1 + Fr(t, 100))), num(n + t * y)],
                 "%s × %s<sup>%d</sup> = <b>%s</b>." % (num(n), d(1 + Fr(t, 100)), y, num(r)))
    if k == "prix_init":
        p0 = R.choice([40, 60, 80, 120, 200])
        t = R.choice([10, 20, 25, 50])
        up = R.random() < 0.5
        p1 = p0 * (1 + Fr(t if up else -t, 100))
        return M("Après une %s de %d %%, un article coûte %s. Quel était son prix initial ?" % ("hausse" if up else "baisse", t, euro(p1)), euro(p0), [euro(p1 * (1 - Fr(t if up else -t, 100))), euro(p1 - t if up else p1 + t), euro(p1 * (1 + Fr(t if up else -t, 100)))],
                 "V₁ = V₂ ÷ CM = %s ÷ %s = <b>%s</b>." % (em(p1), d(1 + Fr(t if up else -t, 100)), euro(p0)))
    V = [("Un prix augmente de 10 % puis baisse de 10 %. Que se passe-t-il ?", "il baisse de 1 %", ["il revient au prix initial", "il augmente de 1 %", "il baisse de 10 %"]),
         ("Un prix double. Quel est son taux d’évolution ?", "+100 %", ["+200 %", "+50 %", "×2 %"]),
         ("Un prix est divisé par 2. Quel est son taux d’évolution ?", "−50 %", ["−200 %", "−100 %", "+50 %"]),
         ("Un effectif est multiplié par 1,5 puis par 2. De quel pourcentage a-t-il augmenté au total ?", "+200 %", ["+250 %", "+150 %", "+300 %"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "On raisonne avec les coefficients multiplicateurs : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Proportions et pourcentages de pourcentages", mix(R, seen, [(s1, 20)])), ("Variations et coefficient multiplicateur", mix(R, seen, [(s2, 20)])),
            ("Évolutions successives", mix(R, seen, [(s3, 20)])), ("Évolutions réciproques", mix(R, seen, [(s4, 10), (s4b, 10)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["La proportion d’une sous-population A dans E est p = n<sub>A</sub> ÷ n<sub>E</sub>. Un pourcentage de pourcentage se calcule par un produit.",
              "Pour une évolution de V₁ à V₂ : variation absolue V₂ − V₁, <b>variation relative</b> (V₂ − V₁) ÷ V₁, <b>coefficient multiplicateur</b> CM = V₂ ÷ V₁ = 1 + t.",
              "Évolutions successives : on multiplie les CM. Évolution réciproque : CM′ = 1 ÷ CM."],
             [("+20 % puis −20 %", ["CM = 1,2 × 0,8 = 0,96"], "−4 %"), ("+25 %, réciproque ?", ["1 ÷ 1,25 = 0,8"], "−20 %")],
             [["+20 % puis +30 % = +50 %", "1,2 × 1,3 = 1,56 : +56 %."], ["Réciproque de +25 % : −25 %", "1 ÷ 1,25 = 0,8 : −20 %."], ["Diviser par la valeur d’arrivée", "On divise par la valeur de départ V₁."]])
    faq = [("Quelle différence entre variation absolue et relative ?", "L’absolue est un écart (en unités), la relative un pourcentage de la valeur de départ."),
           ("Pourquoi multiplier les coefficients ?", "Chaque évolution s’applique à la nouvelle valeur, pas à la valeur de départ.")]
    unit("seconde", R, "pourcentages-et-evolutions", "S",
         "Calculer et utiliser des proportions et des pourcentages de pourcentages ; calculer une variation absolue, une variation relative et un coefficient multiplicateur ; calculer des évolutions successives et réciproques",
         "Proportions et évolutions en pourcentage", "Pourcentages et évolutions",
         "Fiches de maths seconde sur l’information chiffrée : proportions, pourcentages de pourcentages, taux d’évolution, coefficient multiplicateur, évolutions successives et réciproques. 100 exercices corrigés.",
         "CM = V₂ ÷ V₁ = 1 + t", "Successives : on multiplie ; réciproque : 1 ÷ CM", body, faq, sets, 17)


if __name__ == "__main__":
    main()
