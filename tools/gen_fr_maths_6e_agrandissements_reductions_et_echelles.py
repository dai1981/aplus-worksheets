# -*- coding: utf-8 -*-
"""
France Maths 6e : Agrandissements, réductions et échelles
  python3 tools/gen_fr_maths_6e_agrandissements_reductions_et_echelles.py
Erreurs : ajouter au lieu de multiplier pour agrandir, oublier de convertir les cm en m ou en km, inverser plan et réalité.
"""
import random
from fr_c4 import *

R = random.Random(60111)
K = Kids(R)


def rect_svg(w, h, lab_w, lab_h, sc=18):
    W, H = w * sc, h * sc
    s = "<rect x='40' y='16' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (W, H, FILL, GREEN)
    s += text(40 + W / 2, 16 + H + 22, lab_w, 15) + text(32, 16 + H / 2 + 5, lab_h, 15, anchor="end")
    return wrap(W + 60, H + 34, s, "un rectangle", lg=True)


def s1():
    w, h = R.randint(2, 8), R.randint(2, 6)
    k = R.choice([2, 3, 4, 5])
    if w == h:
        return None
    if w < h:
        w, h = h, w
    if R.random() < 0.5:
        return M("<div class='qfig'>%s</div>On agrandit ce rectangle : toutes les longueurs sont multipliées par %d. Quelle est la nouvelle longueur du grand côté ?" % (rect_svg(w, h, "%d cm" % w, "%d cm" % h), k),
                 "%d cm" % (w * k), ["%d cm" % (w + k), "%d cm" % (w * h * k), "%d cm" % (h * k)],
                 "%d × %d = <b>%d cm</b>." % (w, k, w * k))
    return M("Un rectangle mesure %d cm sur %d cm. On l’agrandit pour que %d cm devienne %d cm. Que devient %d cm ?" % (w, h, w, w * k, h), "%d cm" % (h * k), ["%d cm" % (h + w * k - w), "%d cm" % (h * w), "%d cm" % (w * k)],
             "De %d à %d, on multiplie par %d. Donc %d × %d = <b>%d cm</b>." % (w, w * k, k, h, k, h * k))


def s2():
    k = R.choice([2, 3, 4, 5, 10])
    w, h = R.randint(2, 9) * k, R.randint(1, 8) * k
    if w == h:
        return None
    return M("Une photo mesure %d cm sur %d cm. On la réduit : toutes les longueurs sont divisées par %d. Quelles sont ses nouvelles dimensions ?" % (w, h, k), "%d cm sur %d cm" % (w // k, h // k),
             ["%d cm sur %d cm" % (w - k, h - k), "%d cm sur %d cm" % (w * k, h * k), "%d cm sur %d cm" % (w // k, h)],
             "%d ÷ %d = %d et %d ÷ %d = %d : <b>%d cm sur %d cm</b>." % (w, k, w // k, h, k, h // k, w // k, h // k))


def s3():
    n = R.choice([100, 200, 500, 1000, 50, 25000, 100000])
    c = R.randint(2, 12)
    real = c * n
    if real >= 100000:
        return M("Sur une carte à l’échelle 1/%s, deux villes sont à %d cm. Quelle est la distance réelle ?" % (num(n), c), "%s km" % d(Fr(real, 100000)),
                 ["%s km" % d(Fr(real, 1000)), "%s m" % d(Fr(real, 1000)), "%s km" % d(Fr(c * n, 10000000))],
                 "%d × %s = %s cm = <b>%s km</b> (1 km = 100 000 cm)." % (c, num(n), num(real), d(Fr(real, 100000))))
    return M("Sur un plan à l’échelle 1/%s, une pièce mesure %d cm. Quelle est sa longueur réelle ?" % (num(n), c), "%s m" % d(Fr(real, 100)),
             ["%s cm" % d(Fr(c, n)) if False else "%s m" % d(Fr(real, 10)), "%s m" % d(Fr(real, 1000)), "%s m" % d(c + n)],
             "%d × %s = %s cm = <b>%s m</b>." % (c, num(n), num(real), d(Fr(real, 100))))


def s4():
    n = R.choice([100, 200, 500, 50])
    real = Fr(R.randint(2, 30), 1) * Fr(n, 100) if False else Fr(R.randint(1, 15) * n // 100 * 100 // 100, 1)
    c = R.randint(2, 15)
    m = Fr(c * n, 100)
    if m.denominator != 1 and m * 10 % 1 or m < 3:
        return None
    return M("Un jardin mesure %s m. On le dessine à l’échelle 1/%d. Quelle longueur aura-t-il sur le plan ?" % (d(m), n), "%d cm" % c,
             ["%s cm" % d(m * n), "%s cm" % d(m * 100), "%s cm" % d(Fr(c, 10))],
             "%s m = %s cm ; %s ÷ %d = <b>%d cm</b>." % (d(m), num(int(m * 100)), num(int(m * 100)), n, c))


def ech_svg(per, u=50):
    s = [line(20, 30, 20 + u, 30, INK, 4), line(20, 22, 20, 38, INK, 2), line(20 + u, 22, 20 + u, 38, INK, 2), text(20 + u / 2, 18, "%s" % per, 14),
         text(20, 56, "0", 12), text(20 + u, 56, "1 cm", 12)]
    return wrap(u + 60, 64, "".join(s), "échelle graphique", lg=False)


def s5():
    p = K.next()
    k = R.choice(["graph", "maquette", "carte", "agr"])
    if k == "graph":
        per = R.choice([("100 m", 100, "m"), ("50 km", 50, "km"), ("2 km", 2, "km"), ("500 m", 500, "m"), ("20 m", 20, "m")])
        c = R.randint(2, 9)
        return M("<div class='qfig'>%s</div>Sur cette carte, 1 cm représente %s. Deux points sont à %d cm. Quelle est la distance réelle ?" % (ech_svg(per[0]), per[0], c), "%s %s" % (num(per[1] * c), per[2]),
                 ["%s %s" % (num(per[1] + c), per[2]), "%s %s" % (num(per[1] * (c + 1)), per[2]), "%d %s" % (c, per[2])],
                 "%d × %d = <b>%s %s</b>." % (c, per[1], num(per[1] * c), per[2]))
    if k == "maquette":
        n = R.choice([10, 20, 50])
        c = R.randint(4, 30)
        return M("Une maquette de voiture est à l’échelle 1/%d. Elle mesure %d cm. Quelle est la longueur de la vraie voiture ?" % (n, c), "%s m" % d(Fr(c * n, 100)),
                 ["%s m" % d(Fr(c + n, 100)), "%s m" % d(Fr(c * n, 10)), "%s m" % d(Fr(c, n))],
                 "%d × %d = %d cm = <b>%s m</b>." % (c, n, c * n, d(Fr(c * n, 100))))
    if k == "carte":
        c = R.randint(2, 9)
        n = R.choice([100000, 200000, 50000])
        return M("Une carte routière est à l’échelle 1/%s. Sur la carte, 1 cm représente…" % num(n), "%s km" % d(Fr(n, 100000)), ["%s km" % d(Fr(n, 1000)), "%s m" % d(Fr(n, 1000)), "%s km" % num(n)],
                 "1 cm sur la carte = %s cm en réalité = <b>%s km</b>." % (num(n), d(Fr(n, 100000))))
    w = R.randint(3, 8)
    k2 = Fr(R.choice([3, 5]), 2)
    return M("%s agrandit un dessin : 4 cm deviennent %s cm. Que devient un segment de %d cm ?" % (p[0], d(4 * k2), 2 * w), "%s cm" % d(2 * w * k2),
             ["%s cm" % d(2 * w + 4 * k2 - 4), "%s cm" % d(2 * w * 2), "%s cm" % d(2 * w * k2 + 1)],
             "4 → %s : on multiplie par %s. %d × %s = <b>%s cm</b>." % (d(4 * k2), d(k2), 2 * w, d(k2), d(2 * w * k2)))


def main():
    seen = set()
    sets = [("Agrandir une figure", mix(R, seen, [(s1, 20)])), ("Réduire une figure", mix(R, seen, [(s2, 20)])),
            ("Du plan à la réalité", mix(R, seen, [(s3, 20)])), ("De la réalité au plan", mix(R, seen, [(s4, 20)])), ("Échelles et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans un <b>agrandissement</b> ou une <b>réduction</b>, toutes les longueurs sont multipliées par le même nombre : c’est une situation de proportionnalité.",
              "Une échelle 1/100 veut dire : 1 cm sur le plan représente 100 cm (1 m) en réalité.",
              "Pour passer du plan à la réalité, on multiplie ; de la réalité au plan, on divise. Attention aux unités."],
             [("Plan au 1/200 : 7 cm", ["7 × 200 = 1 400 cm", "1 400 cm = 14 m"], "14 m")],
             [["Ajouter au lieu de multiplier", "Si 4 cm deviennent 6 cm, on multiplie par 1,5 : 10 cm deviennent 15 cm."],
              ["Oublier de convertir", "1 400 cm = 14 m ; 100 000 cm = 1 km."],
              ["Inverser plan et réalité", "Sur le plan, les longueurs sont plus petites."]])
    faq = [("Que signifie l’échelle 1/50 000 ?", "1 cm sur la carte représente 50 000 cm, soit 500 m, en réalité."),
           ("Un agrandissement change-t-il les angles ?", "Non : les angles restent les mêmes, seules les longueurs sont multipliées.")]
    unit("6e", R, "agrandissements-reductions-et-echelles", "P",
         "Reconnaître et réaliser des agrandissements et des réductions de figures ; utiliser une échelle (1/n ou graphique) pour calculer des longueurs réelles ou sur un plan",
         "Agrandissements, réductions et échelles", "Agrandissements et échelles",
         "Fiches de maths 6e sur les agrandissements, les réductions et les échelles : agrandir, réduire, plan et réalité, échelle graphique et problèmes. 100 exercices corrigés.",
         "Toutes les longueurs sont multipliées par le même nombre.", "1/100 : 1 cm représente 1 m.", body, faq, sets, 11)


if __name__ == "__main__":
    main()
