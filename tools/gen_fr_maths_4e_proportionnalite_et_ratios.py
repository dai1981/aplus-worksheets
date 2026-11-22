# -*- coding: utf-8 -*-
"""
France Maths 4e : Proportionnalité, quatrième proportionnelle, ratios et vitesses
  python3 tools/gen_fr_maths_4e_proportionnalite_et_ratios.py
Erreurs : produit en croix mal placé, ajouter au lieu de multiplier, partager 2:3 en moitiés, 60 km/h = 1 km/s.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60308)
K = Kids(R)


def s1():
    a = R.randint(2, 12)
    b = a * R.choice([2, 3, 4, 5, Fr(3, 2), Fr(5, 2)])
    if Fr(b).denominator != 1:
        return None
    c = R.randint(2, 20)
    x = Fr(b * c, a)
    if (x * 100).denominator != 1 or c == a:
        return None
    k = R.choice(["tab", "mot"])
    if k == "tab":
        tb = table(["Quantité", d(a), d(c)], [["Prix (€)", d(b), "?"]])
        return M("%s<br>Ce tableau est un tableau de proportionnalité. Quel nombre remplace « ? » ?" % tb, d(x), [d(b + c - a), d(Fr(a * c, b)) if (Fr(a * c, b) * 100).denominator == 1 else d(x + 1), d(Fr(a * b, c)) if (Fr(a * b, c) * 100).denominator == 1 and Fr(a * b, c) != x else d(x - 1)],
                 "Produit en croix : ? = %s × %s ÷ %s = <b>%s</b>." % (d(b), d(c), d(a), d(x)))
    return M("%s cahiers coûtent %s. Combien coûtent %s cahiers ?" % (a, euro(b), c), euro(x), [euro(b + c - a), euro(Fr(a * c, b)) if (Fr(a * c, b) * 100).denominator == 1 else euro(x + 1), euro(b * c)],
             "Le prix est proportionnel au nombre de cahiers : %s × %d ÷ %d = <b>%s</b>." % (em(b), c, a, euro(x)))


def s2():
    k = R.choice(["tab", "tab", "graph", "graph"])
    if k == "tab":
        m = R.randint(2, 9)
        xs = sorted(R.sample(range(1, 13), 3))
        prop = R.random() < 0.5
        ys = [m * x for x in xs]
        if not prop:
            i = R.randrange(3)
            ys[i] += R.choice([1, 2, -1])
        tb = table(["x"] + [str(x) for x in xs], [["y"] + [str(y) for y in ys]])
        ans = "oui" if prop else "non"
        return M("%s<br>Ce tableau est-il un tableau de proportionnalité ?" % tb, ans, ["non" if prop else "oui", "oui, car les nombres augmentent", "on ne peut pas savoir"],
                 "On calcule y ÷ x : %s. %s." % (" ; ".join(d(Fr(y, x)) if Fr(y, x).denominator in (1, 2, 4, 5, 10) else "%s" % fq(Fr(y, x)) for x, y in zip(xs, ys)), "Toujours le même quotient : <b>oui</b>" if prop else "Les quotients ne sont pas tous égaux : <b>non</b>"))
    kind = R.choice(["prop", "droite_non", "courbe"])
    if kind == "prop":
        m = R.choice([Fr(1, 2), 1, 2, Fr(3, 2)])
        lines, ans = [(m, 0, BLUE, "")], "oui : c’est une droite qui passe par l’origine"
    elif kind == "droite_non":
        m, b = R.choice([Fr(1, 2), 1]), R.randint(1, 3)
        lines, ans = [(m, b, BLUE, "")], "non : la droite ne passe pas par l’origine"
    else:
        pts = [(x, y) for x, y in [(0, 0), (1, 1), (2, 4), (3, 9)] if y <= 10]
        svg = relabel(de_k8.kosy(pts=[(x, y, "") for x, y in pts], lo=0, hi=10, u=22), "points dans un repère")
        return M("<div class='qfig'>%s</div>Ces points représentent-ils une situation de proportionnalité ?" % svg, "non : les points ne sont pas alignés", ["oui : ils passent par l’origine", "oui : y augmente quand x augmente", "non : il y a trop peu de points"],
                 "Une situation de proportionnalité se représente par des points <b>alignés avec l’origine</b>.")
    svg = relabel(de_k8.kosy(lines=lines, lo=0, hi=10, u=22), "droite dans un repère")
    opts = ["oui : c’est une droite qui passe par l’origine", "non : la droite ne passe pas par l’origine", "oui : c’est une droite", "non : une droite ne représente jamais la proportionnalité"]
    return M("<div class='qfig'>%s</div>Ce graphique représente-t-il une situation de proportionnalité ?" % svg, ans, [o for o in opts if o != ans], "Proportionnalité ⇔ points alignés <b>avec l’origine</b> du repère.")


def s3():
    a, b = R.randint(1, 7), R.randint(1, 7)
    from math import gcd
    if gcd(a, b) != 1 or a == b:
        return None
    k = R.choice(["part", "part", "simpl", "tot"])
    u = R.randint(2, 12)
    t = (a + b) * u
    if k == "part":
        p, q = K.two()
        return M("%s et %s se partagent %d bonbons dans le ratio %d : %d. Combien en reçoit %s ?" % (p[0], q[0], t, a, b, p[0]), str(a * u), [str(t // 2) if t % 2 == 0 else str(a * u + 1), str(b * u), str(Fr(t * a, b)) if Fr(t * a, b).denominator == 1 else str(a * u + u)],
                 "%d + %d = %d parts ; une part = %d ÷ %d = %d ; %s reçoit %d × %d = <b>%d</b>." % (a, b, a + b, t, a + b, u, p[0], a, u, a * u))
    if k == "simpl":
        m = R.randint(2, 9)
        return M("Simplifie le ratio %d : %d." % (a * m, b * m), "%d : %d" % (a, b), ["%d : %d" % (b, a), "%d : %d" % (a * m - b * m, 1) if a > b else "%d : %d" % (1, b * m - a * m), "%d : %d" % (a + 1, b + 1)],
                 "On divise les deux nombres par %d : <b>%d : %d</b>." % (m, a, b))
    return M("Dans une classe, le ratio filles : garçons est %d : %d. Il y a %d filles. Combien y a-t-il d’élèves en tout ?" % (a, b, a * u), str(t), [str(b * u), str(a * u + b), str(a * u * 2)],
             "Une part = %d ÷ %d = %d ; total = %d × %d = <b>%d</b>." % (a * u, a, u, a + b, u, t))


def s4():
    k = R.choice(["dist", "temps", "vitesse", "conv", "conv2"])
    v = R.choice([30, 45, 60, 80, 90, 100, 120])
    if k == "dist":
        t = R.choice([Fr(1, 2), Fr(3, 2), 2, Fr(1, 4), Fr(3, 4), 3])
        dd = v * t
        tt = {Fr(1, 2): "30 min", Fr(3, 2): "1 h 30 min", 2: "2 h", Fr(1, 4): "15 min", Fr(3, 4): "45 min", 3: "3 h"}[t]
        if dd.denominator != 1:
            return None
        return M("Une voiture roule à %d km/h pendant %s. Quelle distance parcourt-elle ?" % (v, tt), "%s km" % d(dd), ["%s km" % d(v * int(tt.split()[0]) if "min" in tt and "h" not in tt else v * 2 if t == 2 else v * 3 if t == 3 else dd + 10), "%s km" % d(Fr(v, 2)) if Fr(v, 2) != dd else "%s km" % d(dd * 2), "%s km" % d(v + t)],
                 "d = v × t = %d × %s = <b>%s km</b>." % (v, d(t), d(dd)))
    if k == "temps":
        dd = v * R.choice([2, 3, Fr(1, 2), Fr(3, 2)])
        t = dd / v
        h, m = int(t), int((t - int(t)) * 60)
        tt = ("%d h" % h if h else "") + (" %d min" % m if m else "")
        return M("Un train parcourt %s km à %d km/h. Combien de temps dure le trajet ?" % (d(dd), v), tt.strip(), ["%s h" % d(t) if m else "%d h" % (h + 1), "%d h %d min" % (h, int(dd) % 60) if int(dd) % 60 else "%d h 30 min" % h, "%d h" % (h + 2)],
                 "t = d ÷ v = %s ÷ %d = %s h = <b>%s</b>." % (d(dd), v, d(t), tt.strip()))
    if k == "vitesse":
        t = R.choice([2, 3, 4])
        dd = v * t
        return M("Un car parcourt %d km en %d h. Quelle est sa vitesse moyenne ?" % (dd, t), "%d km/h" % v, ["%d km/h" % (dd * t), "%d km/h" % (dd - t), "%s km/h" % d(Fr(t, dd)) if (Fr(t, dd) * 1000).denominator == 1 else "%d km/h" % (v + 10)],
                 "v = d ÷ t = %d ÷ %d = <b>%d km/h</b>." % (dd, t, v))
    if k == "conv":
        ms = R.choice([5, 10, 15, 20, 25, 30])
        return M("Convertis %d m/s en km/h." % ms, "%s km/h" % d(ms * Fr(36, 10)), ["%s km/h" % num(ms * 60), "%s km/h" % d(Fr(ms * 10, 36)) if (Fr(ms * 10, 36) * 10).denominator == 1 else "%d km/h" % (ms * 10), "%s km/h" % num(ms * 3600)],
                 "%d m en 1 s, donc %d × 3 600 = %s m en 1 h, soit <b>%s km/h</b>." % (ms, ms, num(ms * 3600), d(ms * Fr(36, 10))))
    kmh = R.choice([18, 36, 54, 72, 90, 108])
    return M("Convertis %d km/h en m/s." % kmh, "%d m/s" % (kmh * 10 // 36), ["%s m/s" % d(Fr(kmh * 1000, 60)) if (Fr(kmh * 1000, 60) * 10).denominator == 1 else "%d m/s" % kmh, "%s m/s" % d(kmh * Fr(36, 10)), "%d m/s" % (kmh // 3)],
             "%d km/h = %s m en 3 600 s ; %s ÷ 3 600 = <b>%d m/s</b>." % (kmh, num(kmh * 1000), num(kmh * 1000), kmh * 10 // 36))


def s5():
    p = K.next()
    k = R.choice(["recette", "carburant", "echelle", "melange", "debit"])
    if k == "recette":
        n, m = R.choice([(4, 6), (4, 10), (6, 9), (6, 15), (8, 12)])
        f = R.choice([200, 250, 300, 120])
        r = Fr(f * m, n)
        return M("Une recette pour %d personnes demande %d g de farine. Quelle masse faut-il pour %d personnes ?" % (n, f, m), "%s g" % d(r), ["%d g" % (f + m - n), "%s g" % d(Fr(f * n, m)) if (Fr(f * n, m) * 10).denominator == 1 else "%d g" % (f * 2), "%d g" % (f * m)],
                 "%d × %d ÷ %d = <b>%s g</b>." % (f, m, n, d(r)))
    if k == "carburant":
        c = R.choice([5, 6, Fr(13, 2), 7, 8])
        dd = R.choice([150, 250, 300, 450, 600])
        r = c * dd / 100
        return M("Une voiture consomme %s L pour 100 km. Combien consomme-t-elle pour %d km ?" % (d(c), dd), "%s L" % d(r), ["%s L" % d(c + dd - 100), "%s L" % d(c * dd), "%s L" % d(Fr(dd, c)) if (Fr(dd, c) * 10).denominator == 1 else "%s L" % d(r + 2)],
                 "%s × %d ÷ 100 = <b>%s L</b>." % (d(c), dd, d(r)))
    if k == "echelle":
        e = R.choice([25000, 50000, 100000, 200000])
        cm = R.randint(2, 12)
        km = Fr(cm * e, 100000)
        return M("Sur une carte à l’échelle 1/%s, deux villes sont à %d cm. Quelle est la distance réelle ?" % (num(e), cm), "%s km" % d(km), ["%s km" % d(km * 10), "%s km" % d(km / 10), "%s km" % num(cm * e)],
                 "%d × %s = %s cm = <b>%s km</b>." % (cm, num(e), num(cm * e), d(km)))
    if k == "melange":
        a, b = R.choice([(1, 3), (1, 4), (2, 3), (1, 5), (3, 2)])
        u = R.randint(2, 10) * 10
        return M("Pour faire une boisson, on mélange sirop et eau dans le ratio %d : %d. Avec %d cL de sirop, quelle quantité d’eau faut-il ?" % (a, b, a * u), "%d cL" % (b * u), ["%d cL" % (a * u + b), "%d cL" % (a * u * b), "%d cL" % ((a + b) * u)],
                 "Une part = %d ÷ %d = %d cL ; eau = %d × %d = <b>%d cL</b>." % (a * u, a, u, b, u, b * u))
    q = R.choice([12, 15, 20, 24])
    t = R.choice([5, 10, 15, 20])
    return M("Un robinet a un débit de %d L par minute. Combien de temps faut-il pour remplir une baignoire de %d L ?" % (q, q * t), "%d min" % t, ["%s min" % num(q * t * q), "%d min" % (q * t - q), "%s min" % d(Fr(q, q * t)) if (Fr(q, q * t) * 100).denominator == 1 else "%d min" % (t + 5)],
             "%d ÷ %d = <b>%d min</b>." % (q * t, q, t))


def main():
    seen = set()
    sets = [("Quatrième proportionnelle", mix(R, seen, [(s1, 20)])), ("Reconnaître la proportionnalité", mix(R, seen, [(s2, 20)])),
            ("Ratios", mix(R, seen, [(s3, 20)])), ("Vitesses", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Deux grandeurs sont <b>proportionnelles</b> si on passe de l’une à l’autre en multipliant toujours par le même nombre (le coefficient de proportionnalité).",
              "Quatrième proportionnelle : si a correspond à b, alors c correspond à b × c ÷ a (produit en croix). Graphiquement : points alignés avec l’origine.",
              "Un <b>ratio</b> a : b partage une quantité en a + b parts égales. Vitesse : d = v × t."],
             [("3 kg coûtent 7,50 €. Prix de 5 kg ?", ["7,50 × 5 ÷ 3"], "12,50 €"), ("Partager 40 dans le ratio 3 : 5", ["3 + 5 = 8 parts", "une part = 5"], "15 et 25")],
             [["Ajouter au lieu de multiplier (3 → 7,50 donc 5 → 9,50)", "On utilise le coefficient ou le produit en croix."], ["Partager 3 : 5 en deux moitiés", "Il y a 8 parts : 3 parts et 5 parts."],
              ["1 h 30 min = 1,30 h", "1 h 30 min = 1,5 h."]])
    faq = [("Qu’est-ce que le produit en croix ?", "Dans un tableau de proportionnalité, a/b = c/d donne a × d = b × c, ce qui permet de calculer un nombre manquant."),
           ("Comment passer de m/s à km/h ?", "On multiplie par 3,6 (car 1 m/s = 3 600 m/h = 3,6 km/h).")]
    unit("4e", R, "proportionnalite-et-ratios", "F",
         "Reconnaître une situation de proportionnalité (tableau, graphique) ; calculer une quatrième proportionnelle ; utiliser des ratios pour partager ; calculer des vitesses, des distances et des durées ; résoudre des problèmes de proportionnalité",
         "Proportionnalité, quatrième proportionnelle et ratios", "Proportionnalité et ratios",
         "Fiches de maths 4e sur la proportionnalité : quatrième proportionnelle, reconnaître la proportionnalité, ratios, vitesses et problèmes. 100 exercices corrigés.",
         "Quatrième proportionnelle : x = b × c ÷ a", "Proportionnalité ⇔ points alignés avec l’origine", body, faq, sets, 8)


if __name__ == "__main__":
    main()
