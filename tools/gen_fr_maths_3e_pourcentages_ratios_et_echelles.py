# -*- coding: utf-8 -*-
"""
France Maths 3e : Pourcentages, ratios, échelles, agrandissements et réductions (k, k², k³)
  python3 tools/gen_fr_maths_3e_pourcentages_ratios_et_echelles.py
Erreurs : additionner des pourcentages successifs, aire × k au lieu de × k², partager a : b : c en trois parts égales, confondre échelle et distance.
"""
import random
from fr_c4 import *

R = random.Random(60407)
K = Kids(R)


def pc(t):
    return "%s %%" % d(t)


def s1():
    k = R.choice(["succ", "succ", "recip", "taux"])
    if k == "succ":
        a, b = R.choice([10, 20, 25, 30, 40, 50]), R.choice([10, 20, 25, 30, 40, 50])
        ua, ub = R.random() < 0.5, R.random() < 0.5
        c = (1 + Fr(a if ua else -a, 100)) * (1 + Fr(b if ub else -b, 100))
        t = (c - 1) * 100
        if t == 0:
            return None
        ans = "%s de %s" % ("hausse" if t > 0 else "baisse", pc(abs(t)))
        nv = (a if ua else -a) + (b if ub else -b)
        wn = "%s de %s" % ("hausse" if nv > 0 else "baisse", pc(abs(nv))) if nv else "aucune évolution"
        if wn == ans:
            return None
        return M("Un prix %s de %s, puis %s de %s. Quelle est l’évolution globale ?" % ("augmente" if ua else "baisse", pc(a), "augmente" if ub else "baisse", pc(b)), ans,
                 [wn, "%s de %s" % ("baisse" if t > 0 else "hausse", pc(abs(t))), "%s de %s" % ("hausse" if t > 0 else "baisse", pc(abs(c * 100)))],
                 "Coefficient global : %s × %s = %s : <b>%s</b>." % (d(1 + Fr(a if ua else -a, 100)), d(1 + Fr(b if ub else -b, 100)), d(c), ans))
    if k == "recip":
        t = R.choice([20, 25, 50, 60])
        r = Fr(100 * t, 100 + t)
        if (r * 100).denominator != 1:
            return None
        return M("Un prix a augmenté de %s. De quel pourcentage doit-il baisser pour revenir au prix de départ ?" % pc(t), pc(r), [pc(t), pc(t * 2), pc(100 - t)],
                 "Il faut multiplier par 1 ÷ %s = %s, soit une baisse de <b>%s</b>." % (d(1 + Fr(t, 100)), d(Fr(100, 100 + t)), pc(r)))
    x = R.choice([40, 50, 80, 120, 200, 250])
    t = R.choice([5, 10, 15, 20, 25, 30, 40])
    up = R.random() < 0.5
    y = x * (1 + Fr(t if up else -t, 100))
    ans = "%s de %s" % ("hausse" if up else "baisse", pc(t))
    return M("Une population passe de %d à %s. Quel est le taux d’évolution ?" % (x, d(y)), ans, ["%s de %s" % ("hausse" if up else "baisse", pc(abs(y - x))) if abs(y - x) != t else "%s de %s" % ("hausse" if up else "baisse", pc(2 * t)), "%s de %s" % ("baisse" if up else "hausse", pc(t)), "%s de %s" % ("hausse" if up else "baisse", pc(Fr(y * 100, x)))],
             "%s ÷ %d = %s : <b>%s</b>." % (d(y), x, d(y / x), ans))


def s2():
    a, b, c = R.randint(1, 6), R.randint(1, 6), R.randint(1, 6)
    if len({a, b, c}) < 2:
        return None
    u = R.randint(2, 12)
    t = (a + b + c) * u
    p, q, r = K.next(), K.next(), K.next()
    if len({p[0], q[0], r[0]}) < 3:
        return None
    k = R.choice(["part", "part", "tot"])
    if k == "part":
        return M("%s, %s et %s se partagent %d € dans le ratio %d : %d : %d. Combien reçoit %s ?" % (p[0], q[0], r[0], t, a, b, c, q[0]), "%d €" % (b * u), ["%s €" % d(Fr(t, 3)), "%d €" % (b * u + u), "%s €" % d(Fr(t * b, a + c)) if (Fr(t * b, a + c) * 100).denominator == 1 else "%d €" % (b * (u + 1))],
                 "%d + %d + %d = %d parts ; une part = %d ; %s reçoit %d × %d = <b>%d €</b>." % (a, b, c, a + b + c, u, q[0], b, u, b * u))
    return M("Dans un mélange, le ratio ciment : sable : gravier est %d : %d : %d. On utilise %d kg de sable. Quelle est la masse totale du mélange ?" % (a, b, c, b * u), "%d kg" % t, ["%d kg" % (b * u * 3), "%d kg" % ((a + c) * u), "%d kg" % (b * u + a + c)],
             "Une part = %d ÷ %d = %d kg ; total = %d × %d = <b>%d kg</b>." % (b * u, b, u, a + b + c, u, t))


def s3():
    k = R.choice(["carte", "carte", "trouve", "plan"])
    if k == "carte":
        e = R.choice([10000, 25000, 50000, 100000, 200000, 1000000])
        cm = R.choice([Fr(R.randint(2, 30), 2)])
        km = cm * e / 100000
        return M("Sur une carte à l’échelle 1/%s, deux villes sont distantes de %s cm. Quelle est la distance réelle ?" % (num(e), d(cm)), "%s km" % d(km), ["%s km" % d(km * 10), "%s km" % d(km / 10), "%s km" % d(km * 100)],
                 "%s × %s = %s cm = <b>%s km</b>." % (d(cm), num(e), num(cm * e), d(km)))
    if k == "trouve":
        cm = R.randint(2, 12)
        km = cm * R.choice([1, 2, 5, 10])
        e = km * 100000 // cm
        return M("Sur une carte, %d cm représentent %d km. Quelle est l’échelle de la carte ?" % (cm, km), "1/%s" % num(e), ["1/%s" % num(e // 10), "1/%s" % num(e * 10), "1/%s" % num(e * 100)],
                 "%d km = %s cm ; %s ÷ %d = %s : échelle <b>1/%s</b>." % (km, num(km * 100000), num(km * 100000), cm, num(e), num(e)))
    e = R.choice([50, 100, 200])
    m = R.randint(3, 12)
    return M("Sur un plan à l’échelle 1/%d, une pièce mesure %s cm de long. Quelle est sa longueur réelle ?" % (e, d(Fr(m * 100, e))), "%d m" % m, ["%s m" % d(Fr(m, 10)), "%d m" % (m * 10), "%s cm" % d(Fr(m * 100, e))],
             "%s × %d = %s cm = <b>%d m</b>." % (d(Fr(m * 100, e)), e, num(m * 100), m))


def s4():
    k = R.choice([2, 3, Fr(1, 2), Fr(3, 2), 4, Fr(1, 3), Fr(2, 3), 5])
    kind = R.choice(["long", "aire", "aire", "vol", "vol"])
    if kind == "long":
        L_ = R.randint(2, 20)
        return M("On %s une figure de rapport %s. Un côté de %d cm devient…" % ("agrandit" if k > 1 else "réduit", fq(k), L_), "%s cm" % fq(k * L_), ["%s cm" % fq(k * k * L_), "%s cm" % fq(L_ + k), "%s cm" % fq(L_ / k)],
                 "Les longueurs sont multipliées par k = %s : <b>%s cm</b>." % (fq(k), fq(k * L_)))
    if kind == "aire":
        A = R.choice([12, 18, 20, 36, 45, 72, 90])
        return M("Une figure d’aire %d cm² est %s de rapport %s. Quelle est l’aire de la nouvelle figure ?" % (A, "agrandie" if k > 1 else "réduite", fq(k)), "%s cm²" % fq(k * k * A), ["%s cm²" % fq(k * A), "%s cm²" % fq(2 * k * A), "%s cm²" % fq(k ** 3 * A)],
                 "Les aires sont multipliées par k² = %s : <b>%s cm²</b>." % (fq(k * k), fq(k * k * A)))
    V = R.choice([24, 27, 54, 108, 120, 216])
    return M("Un solide de volume %d cm³ est %s de rapport %s. Quel est le volume du nouveau solide ?" % (V, "agrandi" if k > 1 else "réduit", fq(k)), "%s cm³" % fq(k ** 3 * V), ["%s cm³" % fq(k * V), "%s cm³" % fq(k * k * V), "%s cm³" % fq(3 * k * V)],
             "Les volumes sont multipliés par k³ = %s : <b>%s cm³</b>." % (fq(k ** 3), fq(k ** 3 * V)))


def s5():
    k = R.choice(["maquette", "pizza", "photo", "prix", "tva"])
    if k == "maquette":
        e = R.choice([100, 200])
        v = R.randint(2, 30)
        V = Fr(v * e ** 3, 10 ** 6)
        return M("La maquette d’un bateau est à l’échelle 1/%d. Son volume est de %d cm³. Quel est le volume du vrai bateau, en m³ ? (1 m³ = 1 000 000 cm³)" % (e, v), "%s m³" % d(V), ["%s m³" % d(Fr(v * e, 10 ** 6)), "%s m³" % d(Fr(v * e * e, 10 ** 6)), "%s m³" % d(V * 10)],
                 "Volumes × %d³ = %s : %d × %s = %s cm³ = <b>%s m³</b>." % (e, num(e ** 3), v, num(e ** 3), num(v * e ** 3), d(V)))
    if k == "pizza":
        d1, d2 = R.choice([(20, 30), (25, 30), (30, 40), (20, 40), (30, 45)])
        kk = Fr(d2, d1)
        return M("Une pizza de %d cm de diamètre coûte %s. Si le prix était proportionnel à l’aire, combien coûterait une pizza de %d cm ?" % (d1, euro(8), d2), euro(8 * kk * kk), [euro(8 * kk), euro(8 + d2 - d1), euro(8 * kk ** 3)],
                 "Rapport k = %s ; aires × k² = %s : 8 × %s = <b>%s</b>." % (fq(kk), fq(kk * kk), fq(kk * kk), euro(8 * kk * kk)))
    if k == "photo":
        a, b = R.choice([(10, 15), (9, 13), (13, 18), (15, 20)])
        kk = R.choice([2, 3])
        return M("Une photo de %d cm × %d cm est agrandie de rapport %d. Combien de fois son aire est-elle multipliée ?" % (a, b, kk), "%d fois" % (kk * kk), ["%d fois" % kk, "%d fois" % (2 * kk), "%d fois" % (kk ** 3)],
                 "Aire × k² = %d² = <b>%d</b>." % (kk, kk * kk))
    if k == "prix":
        x = R.choice([200, 400, 500, 800])
        t = R.choice([10, 20])
        r = x * (1 + Fr(t, 100)) ** 3
        if (r * 100).denominator != 1:
            return None
        return M("Une somme de %s est placée à %s d’intérêts par an (intérêts composés). Combien vaut-elle au bout de 3 ans ?" % (euro(x), pc(t)), euro(r), [euro(x * (1 + Fr(3 * t, 100))), euro(x * (1 + Fr(t, 100))), euro(x + 3 * t)],
                 "%s × %s³ = <b>%s</b>." % (num(x), d(1 + Fr(t, 100)), euro(r)))
    ht = R.choice([40, 75, 120, 250])
    return M("Un objet coûte %s TTC avec une TVA de 20 %%. Quel est son prix hors taxes ?" % euro(ht * Fr(12, 10)), euro(ht), [euro(ht * Fr(12, 10) * Fr(8, 10)), euro(ht * Fr(12, 10) - 20), euro(ht * Fr(12, 10) * Fr(2, 10))],
             "HT × 1,2 = TTC : %s ÷ 1,2 = <b>%s</b>." % (em(ht * Fr(12, 10)), euro(ht)))


def main():
    seen = set()
    sets = [("Évolutions en pourcentage", mix(R, seen, [(s1, 20)])), ("Ratios à plusieurs termes", mix(R, seen, [(s2, 20)])),
            ("Échelles", mix(R, seen, [(s3, 20)])), ("Agrandissements et réductions", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Évolutions successives : on <b>multiplie</b> les coefficients multiplicateurs (on n’additionne pas les pourcentages).",
              "Ratio a : b : c : on partage en a + b + c parts égales. Échelle 1/n : 1 cm sur le plan représente n cm en réalité.",
              "Dans un agrandissement ou une réduction de rapport k : longueurs × k, <b>aires × k²</b>, <b>volumes × k³</b>."],
             [("Réduction de rapport 1/2 d’un cube de 80 cm³", ["volumes × (1/2)³ = 1/8"], "10 cm³")],
             [["+20 % puis +30 % = +50 %", "1,2 × 1,3 = 1,56 : +56 %."], ["Aire × k", "Les aires sont multipliées par k²."],
              ["Confondre 1/50 000 avec 50 000 m pour 1 cm", "1 cm représente 50 000 cm = 500 m."]])
    faq = [("Pourquoi les aires sont-elles multipliées par k² ?", "Une aire est le produit de deux longueurs, chacune multipliée par k."),
           ("Que signifie une échelle 1/25 000 ?", "1 cm sur la carte représente 25 000 cm, soit 250 m, dans la réalité.")]
    unit("3e", R, "pourcentages-ratios-et-echelles", "F",
         "Calculer des évolutions successives et réciproques en pourcentage ; partager selon un ratio à plusieurs termes ; utiliser des échelles ; connaître l’effet d’un agrandissement ou d’une réduction sur les longueurs, les aires et les volumes",
         "Pourcentages, ratios, échelles, agrandissements et réductions", "Pourcentages, ratios et échelles",
         "Fiches de maths 3e : évolutions successives en pourcentage, ratios, échelles, agrandissements et réductions (aires × k², volumes × k³) et problèmes. 100 exercices corrigés.",
         "Agrandissement de rapport k : aires × k², volumes × k³", "Évolutions successives : on multiplie les coefficients", body, faq, sets, 7)


if __name__ == "__main__":
    main()
