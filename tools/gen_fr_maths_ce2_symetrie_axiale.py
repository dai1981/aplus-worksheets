# -*- coding: utf-8 -*-
"""
France Maths CE2 : La symétrie axiale (Espace et géométrie)
  python3 tools/gen_fr_maths_ce2_symetrie_axiale.py
Reconnaître une figure symétrique, lettres symétriques, compléter une figure par symétrie sur quadrillage,
symétrique d’une case ou d’un point, nombre d’axes de symétrie.
Erreurs : faire glisser la moitié au lieu de la retourner, compter les carreaux depuis le bord, croire que la diagonale
d’un rectangle est un axe.
"""
import random
import gen_de_mathe_k3_achsensymmetrie as DE
from fr_common import mcq, lesson, example, make_unit, mix, wrap, text, GREEN

R = random.Random(51018)
DE.R = R
COLS, ROWS, Q = DE.COLS, DE.ROWS, DE.Q
L4 = "ABCD"


def o(n):
    return "1re" if n == 1 else "%de" % n


def four(figs):
    s = []
    for i, c in enumerate(figs):
        ox = 10 + i * 112
        s.append(DE.grid(ox, 10, c, True))
        s.append(text(ox + COLS * Q / 2.0, 10 + ROWS * Q + 24, L4[i], 16, col=GREEN))
    return wrap(10 + 4 * 112, 10 + ROWS * Q + 32, "".join(s), "quatre figures A à D sur quadrillage", lg=True)


def s1():
    hs = [DE.half() for _ in range(4)]
    if not all(hs):
        return None
    good = DE.mirror(hs[0])
    bads = [DE.broken(DE.mirror(hs[1])), DE.shifted(hs[2]), DE.broken(DE.mirror(hs[3]))]
    if not all(bads) or any(b == DE.mirror({(x, y) for x, y in b if x < 3}) for b in bads):
        return None
    figs = bads + [good]
    R.shuffle(figs)
    k = figs.index(good)
    return mcq(four(figs) + "Quelle figure est symétrique par rapport à la droite rouge ?", L4[k], [L4[i] for i in range(4) if i != k],
               "Seule la figure %s a ses carreaux à la même distance de l’axe, de chaque côté : en pliant, les deux moitiés se superposent." % L4[k])


VERT = list("AHIMOTUVWXY")
HORI = list("BCDEHIKOX")
NONE = list("FGJLNPQRSZ")


def s2():
    kind = R.choice(["v", "v", "h", "n"])
    if kind == "v":
        a, w = R.choice(VERT), R.sample(NONE, 3)
        q = "Quelle lettre a un axe de symétrie <b>vertical</b> : %s ?" % ", ".join(sorted([a] + w))
        e = "Si on plie %s le long d’une ligne verticale au milieu, les deux moitiés se superposent : <b>%s</b>." % (a, a)
    elif kind == "h":
        a, w = R.choice([x for x in HORI if x not in VERT]), R.sample(NONE, 3)
        q = "Quelle lettre a un axe de symétrie <b>horizontal</b> : %s ?" % ", ".join(sorted([a] + w))
        e = "Pour %s, la moitié du haut et la moitié du bas se superposent : <b>%s</b>." % (a, a)
    else:
        a, w = R.choice(NONE), R.sample(VERT + [x for x in HORI if x not in VERT], 3)
        q = "Quelle lettre n’a <b>aucun</b> axe de symétrie : %s ?" % ", ".join(sorted([a] + w))
        e = "%s n’a pas d’axe de symétrie ; les autres lettres peuvent se plier en deux moitiés identiques : <b>%s</b>." % (a, a)
    return mcq(q, a, w, e)


def s3():
    h = DE.half()
    if not h:
        return None
    good = DE.mirror(h)
    sh = DE.shifted(h)
    near = DE.broken(good)
    flipped = set(h) | {(COLS - 1 - x, ROWS - 1 - y) for x, y in h}
    opts = [good, sh, near, flipped]
    if not near or len({frozenset(o) for o in opts}) < 4:
        return None
    pic = wrap(COLS * Q + 20, ROWS * Q + 20, DE.grid(10, 10, h), "moitié de figure et axe de symétrie")
    R.shuffle(opts)
    k = opts.index(good)
    return mcq(pic + "Voici la moitié gauche d’une figure. Quel dessin montre la figure complétée par symétrie ?" + four(opts), L4[k], [L4[i] for i in range(4) if i != k],
               "Chaque carreau est reporté de l’autre côté de l’axe, à la même distance. C’est le dessin <b>%s</b>." % L4[k])


def s4():
    kind = R.choice(["cote", "dist", "grille", "grille"])
    if kind == "cote":
        n = R.randint(1, 6)
        side, other = R.choice([("à gauche", "à droite"), ("à droite", "à gauche")])
        ans = "à %d carreau%s %s de l’axe" % (n, "x" if n > 1 else "", other)
        w = ["à %d carreau%s %s de l’axe" % (n, "x" if n > 1 else "", side), "à %d carreaux %s de l’axe" % (n + 1, other), "à %d carreaux %s de l’axe" % (2 * n, other)]
        return mcq("Un point est à %d carreau%s %s d’un axe de symétrie vertical. Où est son symétrique ?" % (n, "x" if n > 1 else "", side), ans, w,
                   "Le symétrique est à la même distance, de l’autre côté : <b>%s</b>." % ans)
    if kind == "dist":
        n = R.randint(1, 7)
        return mcq("Un point est à %d carreau%s de l’axe. Combien de carreaux le séparent de son symétrique ?" % (n, "x" if n > 1 else ""), "%d carreaux" % (2 * n),
                   ["%d carreau%s" % (n, "x" if n > 1 else ""), "%d carreaux" % (n + 1), "%d carreaux" % (2 * n + 2)],
                   "%d jusqu’à l’axe, puis encore %d de l’autre côté : <b>%d carreaux</b>." % (n, n, 2 * n))
    x, y = R.randint(0, 2), R.randint(0, ROWS - 1)
    mx = COLS - 1 - x
    s = DE.grid(10, 10, {(x, y)})
    for i in range(COLS):
        s += text(10 + i * Q + Q / 2.0, 10 + ROWS * Q + 14, str(i + 1), 10, weight=400)
    pic = wrap(COLS * Q + 20, ROWS * Q + 30, s, "quadrillage avec une case coloriée et un axe")
    return mcq(pic + "Dans quelle colonne se trouve la case symétrique ? (Ligne %d ; les colonnes sont numérotées en bas.)" % (y + 1), "colonne %d" % (mx + 1),
               ["colonne %d" % c for c in (x + 4, mx, mx + 2 if mx + 2 <= COLS else x + 1, x + 1) if c != mx + 1 and 1 <= c <= COLS],
               "Depuis l’axe, la case est la %s à gauche. Sa symétrique est la %s à droite : <b>colonne %d</b>." % (o(3 - x), o(3 - x), mx + 1))


AXES = [("un carré", "4"), ("un rectangle qui n’est pas un carré", "2"), ("un triangle équilatéral", "3"), ("un cercle", "une infinité"),
        ("un cœur", "1"), ("un papillon", "1"), ("un hexagone régulier", "6"), ("la lettre H", "2"), ("la lettre A", "1"), ("la lettre F", "aucun"),
        ("le chiffre 8", "2"), ("le chiffre 3", "1"), ("un losange qui n’est pas un carré", "2"), ("la lettre X", "2")]


def s5():
    if R.random() < 0.55:
        thing, ans = R.choice(AXES)
        near = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "une infinité": ["1", "4"], "1": ["2", "aucun"], "6": ["3", "12"], "aucun": ["1", "2"]}[ans]
        rest = [x for x in ["aucun", "1", "2", "3", "4", "6", "une infinité"] if x != ans and x not in near]
        R.shuffle(rest)
        return mcq("Combien d’axes de symétrie a %s ?" % thing, ans, near + rest,
                   "%s a <b>%s</b> axe%s de symétrie." % (thing[0].upper() + thing[1:], ans, "s" if ans not in ("1", "aucun") else ""))
    return s4()


def main():
    seen = set()
    sets = [
        ("Figure symétrique ou non ?", mix(R, seen, [(s1, 20)])),
        ("Les lettres symétriques", mix(R, seen, [(s2, 20)])),
        ("Compléter par symétrie", mix(R, seen, [(s3, 20)])),
        ("Le symétrique d’un point", mix(R, seen, [(s4, 20)])),
        ("Les axes de symétrie", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Une figure est <b>symétrique</b> si on peut la plier en deux et que les deux moitiés se superposent exactement.",
         "La ligne de pliage s’appelle l’<b>axe de symétrie</b>.",
         "Un point et son symétrique sont <b>à la même distance</b> de l’axe, mais de chaque côté. Sur quadrillage, on compte les carreaux <b>à partir de l’axe</b>.",
         "Certaines figures ont plusieurs axes : le carré en a 4, le rectangle 2, le cercle une infinité."],
        [example("Une case est à 2 carreaux à gauche de l’axe. Où est sa symétrique ?", ["même distance : 2 carreaux", "autre côté : à droite"], "à 2 carreaux à droite de l’axe")],
        [["Faire glisser la moitié", "La symétrie retourne la figure : ce qui touche l’axe à gauche touche l’axe à droite."],
         ["Compter depuis le bord de la feuille", "On compte toujours les carreaux depuis l’axe."],
         ["Croire que la diagonale d’un rectangle est un axe", "En pliant sur la diagonale, les coins ne se superposent pas : le rectangle n’a que 2 axes."]])
    faq = [("Comment vérifier qu’une figure est symétrique ?", "On la plie le long de l’axe, ou on place un petit miroir sur l’axe : on doit voir la figure entière."),
           ("Pourquoi utiliser le quadrillage ?", "Il permet de compter les carreaux jusqu’à l’axe et de reporter la même distance de l’autre côté.")]
    make_unit(R, "symetrie-axiale", "E",
              "Reconnaître si une figure présente un axe de symétrie ; compléter une figure par symétrie axiale sur quadrillage ; trouver le symétrique d’un point ou d’une case (résumé du programme 2024 du cycle 2).",
              "La symétrie axiale", "Symétrie CE2 : fiches et exercices avec corrigé", "Symétrie axiale",
              "Fiches de maths CE2 sur la symétrie axiale : figures et lettres symétriques, compléter une figure sur quadrillage, symétrique d’un point et axes de symétrie. 100 exercices corrigés.",
              "Même distance de l’axe, de l’autre côté.", "En pliant sur l’axe, les deux moitiés se superposent.",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
