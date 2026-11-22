# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Les nombres (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cp_nombres.py
CP : nombres jusqu’à 100, dizaines et unités, lire et écrire en lettres. CE1 : jusqu’à 999, centaines, dizaines, unités.
Erreurs : écrire 407 pour « quarante-sept » (408 → 4 dizaines 8 unités), inverser dizaines et unités (47 → 74),
confondre chiffre des dizaines et nombre de dizaines.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, blocs, lettres, pic, ch, KINDS, table
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53001 + 100 * lv)
    K = Kids(R)


def top():
    return 100 if L == 0 else 999


def s1():
    if L == 0:
        n = R.randint(11, 40)
        kind = R.choice(KINDS)
        k = R.choice(["tf", "row"])
        svg = KP.tenframe_svg(n, frames=(n + 9) // 10, kind=kind if kind in ("dot",) else "dot") if k == "tf" else KP.row_svg(n, kind)
        return mcq("<div class='qfig'>%s</div>Combien y en a-t-il ?" % pic(svg, "des objets à compter", lg=True), str(n), [str(n + 1), str(n - 1), str(n + 10) if n + 10 <= 100 else str(n - 10)],
                   "On compte par dizaines : %s et %s, donc <b>%d</b>." % (pl(n // 10, "dizaine"), pl(n % 10, "unité"), n))
    c, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9)
    n = c * 100 + d * 10 + u
    return mcq("<div class='qfig'>%s</div>Quel nombre est représenté ?" % blocs(0, c, d, u), num(n), [num(c * 100 + u * 10 + d) if u != d else num(n + 10), num(c * 10 + d + u) if d else num(c * 100 + u), num(n + 100) if n + 100 < 1000 else num(n - 100)],
               "%d plaque%s de cent, %d barre%s de dix et %d petit%s cube%s : <b>%s</b>." % (c, "s" if c > 1 else "", d, "s" if d > 1 else "", u, "s" if u > 1 else "", "s" if u > 1 else "", num(n)))


def s2():
    if L == 0:
        d, u = R.randint(1, 9), R.randint(0, 9)
        n = 10 * d + u
        if R.random() < 0.5:
            pv = blocs(0, 0, d, u)
            return mcq("<div class='qfig'>%s</div>Quel nombre est représenté ?" % pv, str(n), [str(10 * u + d) if u and u != d else str(n + 10) if n + 10 < 100 else str(n - 10), "%d%d" % (d, u + 1) if u < 9 else str(n - 1), str(d + u)],
                       "%d barre%s de dix et %d cube%s : <b>%d</b>." % (d, "s" if d > 1 else "", u, "s" if u > 1 else "", n))
        return mcq("%d dizaine%s et %d unité%s, c’est quel nombre ?" % (d, "s" if d > 1 else "", u, "s" if u > 1 else ""), str(n), [str(10 * u + d) if u and u != d else str(n + 1), str(d + u), "%d0%d" % (d, u) if u else str(n + 10)],
                   "%s = %d, plus %d : <b>%d</b>." % (pl(d, "dizaine"), 10 * d, u, n))
    c, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9)
    n = c * 100 + d * 10 + u
    k = R.choice(["cdu", "chiffre", "nombre"])
    if k == "cdu":
        return mcq("%d centaine%s, %d dizaine%s et %d unité%s, c’est quel nombre ?" % (c, "s" if c > 1 else "", d, "s" if d > 1 else "", u, "s" if u > 1 else ""), num(n),
                   [num(u * 100 + d * 10 + c) if u else num(n + 100) if n < 900 else num(n - 100), num(c * 100 + u * 10 + d) if u != d else num(n + 1), "%d%d%d" % (c, d, u) if False else num(c + d + u)],
                   "%s = %d ; %s = %d : %d + %d + %d = <b>%s</b>." % (pl(c, "centaine"), c * 100, pl(d, "dizaine"), d * 10, c * 100, d * 10, u, num(n)))
    if k == "chiffre":
        return mcq("Dans %s, quel est le chiffre des dizaines ?" % num(n), str(d), [str(c), str(u) if u != d else str((d + 1) % 10), str(n // 10) if n // 10 != d else "0"],
                   "%s : %s, %s, %s. Le chiffre des dizaines est <b>%d</b>." % (num(n), pl(c, "centaine"), pl(d, "dizaine"), pl(u, "unité"), d))
    if n // 10 < 10:
        return None
    return mcq("Combien y a-t-il de dizaines en tout dans %s ?" % num(n), str(n // 10), [str(d), str(c), str(n // 10 + 1)],
               "%s = %s et %s. Le nombre de dizaines est <b>%d</b> (le chiffre des dizaines est %d)." % (num(n), pl(n // 10, "dizaine"), pl(u, "unité"), n // 10, d))


def s3():
    n = R.randint(11, 99) if L == 0 else R.randint(101, 999)
    if L == 0 and R.random() < 0.6:
        n = R.choice(list(range(60, 100)) + list(range(11, 20)))
    w = []
    for x in (n + 10 if n + 10 <= top() else n - 10, n + 1 if n % 10 != 9 else n - 1, (n % 10) * 10 + n // 10 if L == 0 and n % 10 else n + 100 if n + 100 <= top() else n - 100):
        if x != n:
            w.append(x)
    if R.random() < 0.5:
        return mcq("Comment s’écrit « %s » en chiffres ?" % lettres(n), num(n), [num(x) for x in w] + ([num(int(str(n // 10 * 10) + str(n % 10)))] if n % 10 and L == 0 and n // 10 * 10 * 10 + n % 10 < 1000 and False else []),
                   "« %s » : <b>%s</b>." % (lettres(n), num(n)))
    return mcq("Comment se lit %s ?" % num(n), lettres(n), [lettres(x) for x in w], "%s se lit <b>%s</b>." % (num(n), lettres(n)))


def s4():
    if L == 0:
        d, u = R.randint(1, 9), R.randint(1, 9)
        n = 10 * d + u
        k = R.choice(["dec", "miss", "dec2"])
        if k == "dec":
            return mcq("Complète : %d = … + %d" % (n, u), str(10 * d), [str(d), str(n + u), str(10 * u) if u != d else str(10 * d + 10)], "%d = %s et %s = <b>%d</b> + %d." % (n, pl(d, "dizaine"), pl(u, "unité"), 10 * d, u))
        if k == "miss":
            return mcq("Complète : %d + … = %d" % (10 * d, n), str(u), [str(d), str(n), str(u + 10)], "%d + <b>%d</b> = %d." % (10 * d, u, n))
        return mcq("Quel nombre est égal à %s + %s ?" % (pl(d, "dizaine"), pl(u, "unité")), str(n), [str(10 * u + d) if u != d else str(n + 1), str(d + u), str(n + 10) if n + 10 < 100 else str(n - 10)], "%s + %s = <b>%d</b>." % (pl(d, "dizaine"), pl(u, "unité"), n))
    c, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(1, 9)
    n = 100 * c + 10 * d + u
    if R.random() < 0.5:
        return mcq("Complète : %s = %d + … + %d" % (num(n), 100 * c, u), str(10 * d), [str(d), str(10 * u) if u != d else str(10 * d + 10), str(100 * d) if d else "1"], "%s = %d + <b>%d</b> + %d." % (num(n), 100 * c, 10 * d, u)) if d else None
    return mcq("Quel nombre est égal à %d + %d + %d ?" % (100 * c, 10 * d, u) if d else "Quel nombre est égal à %d + %d ?" % (100 * c, u), num(n),
               [num(int("%d%d" % (c, u))) if not d else num(100 * c + 10 * u + d) if u != d else num(n + 1), num(c + d + u), num(n + 100) if n < 900 else num(n - 100)], "On place les chiffres : <b>%s</b>." % num(n))


def s5():
    p = K.next()
    if L == 0:
        k = R.choice(["boites", "billes", "oeufs"])
        if k == "boites":
            d, u = R.randint(2, 9), R.randint(1, 9)
            return mcq("%s range ses crayons par boîtes de 10. Il y a %d boîtes pleines et %s en plus. Combien de crayons ?" % (p[0], d, pl(u, "crayon")), str(10 * d + u), [str(d + u), str(10 * u + d) if u != d else str(10 * d + u + 1), str(10 * d)],
                       "%d boîtes de 10 = %d ; %d + %d = <b>%d</b>." % (d, 10 * d, 10 * d, u, 10 * d + u))
        if k == "billes":
            n = R.randint(21, 99)
            return mcq("%s a %d billes. Combien de sachets de 10 billes peut-%s remplir ?" % (p[0], n, p[1]), str(n // 10), [str(n % 10) if n % 10 != n // 10 else str(n // 10 + 1), str(n), str(n // 10 + 1)],
                       "%d = %s et %s : <b>%d</b> sachets pleins." % (n, pl(n // 10, "dizaine"), pl(n % 10, "unité"), n // 10))
        n = R.randint(12, 59)
        return mcq("Il y a %d élèves. Ils forment des équipes de 10. Combien d’équipes complètes ?" % n, str(n // 10), [str(n % 10) if n % 10 != n // 10 else str(n // 10 + 1), str(n // 10 + 1), str(10)],
                   "%d = %s et %d : <b>%d</b> équipes de 10." % (n, pl(n // 10, "dizaine"), n % 10, n // 10))
    k = R.choice(["cartons", "billets", "pages"])
    if k == "cartons":
        c, d, u = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
        return mcq("Une usine a %s de 100 stylos, %s de 10 et %s. Combien de stylos ?" % (pl(c, "carton"), pl(d, "paquet"), pl(u, "stylo seul", "stylos seuls")), num(100 * c + 10 * d + u), [num(c + d + u), num(100 * c + 10 * u + d) if u != d else num(100 * c + 10 * d + u + 10), num(10 * c + d + u)],
                       "%d + %d + %d = <b>%s</b>." % (100 * c, 10 * d, u, num(100 * c + 10 * d + u)))
    if k == "billets":
        n = R.randint(110, 990)
        return mcq("%s a %s €. Combien de billets de 10 € peut-%s avoir au plus ?" % (p[0], num(n), p[1]), str(n // 10), [str(n // 10 % 10), str(n // 100), str(n // 10 + 1)],
                   "%s = %s et %s : <b>%d</b> billets de 10 €." % (num(n), pl(n // 10, "dizaine"), pl(n % 10, "unité"), n // 10))
    n = R.randint(150, 950)
    return mcq("Un livre a %s pages. %s en a lu 100. Combien de pages lui reste-t-il à lire ?" % (num(n), p[0]), num(n - 100), [num(n - 10), num(n + 100), num(n - 1)],
               "Enlever 100, c’est enlever 1 centaine : <b>%s</b>." % num(n - 100))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Compter", mix(R, seen, [(s1, 20)])),
        ("Dizaines et unités" if lv == 0 else "Centaines, dizaines et unités", mix(R, seen, [(s2, 20)])),
        ("Lire et écrire les nombres", mix(R, seen, [(s3, 20)])),
        ("Décomposer un nombre", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    if lv == 0:
        body = lesson(["10 unités font <b>1 dizaine</b>. 47, c’est 4 dizaines et 7 unités.",
                       "Le chiffre de gauche dit les dizaines, celui de droite les unités.",
                       "Pour compter beaucoup d’objets, on fait des paquets de 10."],
                      [example("4 dizaines et 7 unités", ["40 + 7"], "47")],
                      [["Écrire 407 pour « quarante-sept »", "Quarante-sept, c’est 40 + 7 = 47."],
                       ["Inverser : 47 et 74", "Les dizaines s’écrivent à gauche."],
                       ["Oublier soixante-dix, quatre-vingts", "70 = soixante-dix, 80 = quatre-vingts, 90 = quatre-vingt-dix."]])
    else:
        body = lesson(["10 unités = 1 dizaine ; 10 dizaines = <b>1 centaine</b> ; 1 centaine = 100 unités.",
                       "Dans 358 : 3 centaines, 5 dizaines, 8 unités.",
                       "Le <b>chiffre</b> des dizaines de 358 est 5 ; le <b>nombre</b> de dizaines est 35."],
                      [example("3 centaines, 0 dizaine, 8 unités", ["300 + 8"], "308")],
                      [["Oublier le 0 : 300 + 8 = 38", "Il faut 3 chiffres : 308."],
                       ["Confondre chiffre et nombre de dizaines", "358 : chiffre des dizaines 5, nombre de dizaines 35."],
                       ["Écrire « deux-cents-trois »", "On écrit deux cent trois (cent sans s quand il est suivi d’un nombre)."]])
    faq = [("Pourquoi faire des paquets de 10 ?", "Pour compter plus vite et comprendre comment s’écrivent les nombres."),
           ("Jusqu’où compte-t-on en %s ?" % GN(lv), "Jusqu’à %s." % ("100" if lv == 0 else "999"))]
    unit(lv, R, "nombres-jusqu-a-100" if lv == 0 else "nombres-jusqu-a-1000", "N",
         ("Dénombrer des collections en les organisant par dizaines ; connaître les nombres jusqu’à 100 à l’écrit et à l’oral ; comprendre la valeur des chiffres (dizaines, unités) et les différentes écritures d’un nombre" if lv == 0 else
          "Connaître les relations entre unités, dizaines et centaines ; lire et écrire les nombres jusqu’à 999 ; connaître la valeur des chiffres selon leur position ; décomposer un nombre"),
         "Les nombres jusqu’à 100" if lv == 0 else "Les nombres jusqu’à 1 000", "Nombres jusqu’à 100" if lv == 0 else "Nombres jusqu’à 1 000",
         ("Fiches de maths CP sur les nombres jusqu’à 100 : compter, dizaines et unités, lire et écrire les nombres, décomposer et problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 sur les nombres jusqu’à 1 000 : centaines, dizaines, unités, lire et écrire, décomposer et problèmes. 100 exercices corrigés."),
         "10 unités = 1 dizaine." if lv == 0 else "10 dizaines = 1 centaine.", "47 = 4 dizaines et 7 unités." if lv == 0 else "358 = 3 centaines, 5 dizaines, 8 unités.",
         body, faq, sets, 1)


if __name__ == "__main__":
    build(0)
