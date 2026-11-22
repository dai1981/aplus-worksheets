# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : La symétrie axiale (Espace et géométrie)
  python3 tools/gen_fr_maths_cm1_symetrie_axiale.py
Reconnaître des axes de symétrie, compléter ou construire le symétrique d’une figure sur quadrillage par rapport à une droite
verticale ou horizontale (CM2 : aussi une diagonale du quadrillage), symétrique d’un point, nombre d’axes.
Erreurs : faire glisser la figure au lieu de la retourner, compter les carreaux depuis le bord, oublier qu’une diagonale
échange lignes et colonnes.
"""
import random
from fr_c3 import mcq, lesson, example, unit, mix, Kids, GN, wrap, text, line, FILL, GREEN, RED
import gen_fr_maths_ce2_symetrie_axiale as CE

R = K = None
L = 1
N, Q = 6, 15
L4 = "ABCD"


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52122 + 100 * lv)
    K = Kids(R)
    CE.R = R
    CE.DE.R = R


def mir(c, ax):
    x, y = c
    return {"v": (N - 1 - x, y), "h": (x, N - 1 - y), "d": (y, x)}[ax]


def side(c, ax):
    x, y = c
    return {"v": x < N // 2, "h": y < N // 2, "d": x > y}[ax]


def half(ax):
    cells = set()
    n = R.randint(4, 7)
    tries = 0
    while len(cells) < n and tries < 200:
        tries += 1
        c = (R.randint(0, N - 1), R.randint(0, N - 1))
        if side(c, ax) or (ax == "d" and c[0] == c[1] and R.random() < 0.3):
            cells.add(c)
    near = {"v": lambda c: c[0] == N // 2 - 1, "h": lambda c: c[1] == N // 2 - 1, "d": lambda c: abs(c[0] - c[1]) <= 1}[ax]
    if not any(near(c) for c in cells):
        return None
    return cells


def full(h, ax):
    return set(h) | {mir(c, ax) for c in h}


def grid(ox, oy, cells, ax):
    s = []
    for i in range(N + 1):
        s.append(line(ox + i * Q, oy, ox + i * Q, oy + N * Q, "#c9d6df", 0.8))
        s.append(line(ox, oy + i * Q, ox + N * Q, oy + i * Q, "#c9d6df", 0.8))
    for x, y in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='0.8'/>" % (ox + x * Q, oy + y * Q, Q, Q, FILL, GREEN))
    da = " stroke-dasharray='5 3'"
    if ax == "v":
        s.append(line(ox + N * Q / 2.0, oy - 6, ox + N * Q / 2.0, oy + N * Q + 6, RED, 2, da))
    elif ax == "h":
        s.append(line(ox - 6, oy + N * Q / 2.0, ox + N * Q + 6, oy + N * Q / 2.0, RED, 2, da))
    else:
        s.append(line(ox - 4, oy - 4, ox + N * Q + 4, oy + N * Q + 4, RED, 2, da))
    return "".join(s)


def four(figs, ax):
    s = []
    for i, c in enumerate(figs):
        ox = 12 + i * 116
        s.append(grid(ox, 12, c, ax))
        s.append(text(ox + N * Q / 2.0, 12 + N * Q + 24, L4[i], 16, col=GREEN))
    return wrap(12 + 4 * 116, 12 + N * Q + 32, "".join(s), "quatre figures A à D sur quadrillage", lg=True)


def wrongs(h, ax):
    good = full(h, ax)
    sh = {"v": lambda c: (c[0] + N // 2, c[1]), "h": lambda c: (c[0], c[1] + N // 2), "d": lambda c: (N - 1 - c[0], N - 1 - c[1])}[ax]
    other = {"v": "h", "h": "v", "d": "v"}[ax]
    w1 = set(h) | {sh(c) for c in h if 0 <= sh(c)[0] < N and 0 <= sh(c)[1] < N}
    w2 = set(h) | {mir(c, other) for c in h}
    w3 = set(good)
    mov = [c for c in w3 if not side(c, ax) and c not in h]
    if not mov:
        return None
    c = R.choice(mov)
    w3.discard(c)
    cand = [(x, y) for x in range(N) for y in range(N) if not side((x, y), ax) and (x, y) not in w3 and (x, y) not in h and not (ax == "d" and x == y)]
    if not cand:
        return None
    w3.add(R.choice(cand))
    opts = [good, w1, w2, w3]
    if len({frozenset(o) for o in opts}) < 4:
        return None
    return opts


def ask_complete(ax):
    h = half(ax)
    if not h:
        return None
    opts = wrongs(h, ax)
    if not opts:
        return None
    good = opts[0]
    R.shuffle(opts)
    k = opts.index(good)
    pic = wrap(N * Q + 24, N * Q + 24, grid(12, 12, h, ax), "moitié de figure et axe de symétrie")
    where = {"v": "verticale", "h": "horizontale", "d": "diagonale"}[ax]
    return mcq(pic + "Voici une moitié de figure et l’axe de symétrie (droite %s rouge). Quel dessin montre la figure complétée par symétrie ?" % where + four(opts, ax), L4[k], [L4[i] for i in range(4) if i != k],
               ("Chaque carreau est reporté de l’autre côté de l’axe, à la même distance, sur la perpendiculaire à l’axe." if ax != "d" else
                "Avec un axe diagonal, la case (colonne c, ligne l) va en (colonne l, ligne c) : lignes et colonnes s’échangent.") + " C’est le dessin <b>%s</b>." % L4[k])


def ask_which(ax):
    hs = [half(ax) for _ in range(4)]
    if not all(hs):
        return None
    good = full(hs[0], ax)
    bad = []
    for h in hs[1:]:
        w = wrongs(h, ax)
        if not w:
            return None
        bad.append(R.choice(w[1:]))
    figs = bad + [good]
    if any(full({c for c in b if side(c, ax) or (ax == "d" and c[0] == c[1])}, ax) == b for b in bad):
        return None
    R.shuffle(figs)
    k = figs.index(good)
    return mcq(four(figs, ax) + "Quelle figure est symétrique par rapport à la droite rouge ?", L4[k], [L4[i] for i in range(4) if i != k],
               "Seule la figure %s a chaque carreau en face d’un carreau symétrique, à la même distance de l’axe." % L4[k])


def re(it):
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"]) if it else None


def s1():
    return ask_which(R.choice(["v", "h"] + (["d"] if L == 2 else [])))


def s2():
    return re(CE.s2() if R.random() < 0.5 else CE.s5())


def s3():
    return ask_complete(R.choice(["v", "h"]))


def s4():
    if L == 2:
        return ask_complete("d")
    return re(CE.s4())


def point_q():
    ax = R.choice(["v", "h"] + (["d"] if L == 2 else []))
    x, y = R.randint(0, N - 1), R.randint(0, N - 1)
    if not side((x, y), ax):
        return None
    m = mir((x, y), ax)
    s = grid(12, 12, {(x, y)}, ax)
    for i in range(N):
        s += text(12 + i * Q + Q / 2.0, 12 + N * Q + 14, "ABCDEF"[i], 10, weight=600)
        s += text(4, 12 + i * Q + Q / 2.0 + 4, str(i + 1), 10, weight=600)
    pic = wrap(N * Q + 24, N * Q + 30, s, "quadrillage, une case coloriée et un axe")
    nm = lambda c: "%s%d" % ("ABCDEF"[c[0]], c[1] + 1)
    w = [nm(c) for c in [(m[0], y) if ax != "v" else (x, m[1]), (y, x) if ax != "d" else (N - 1 - y, N - 1 - x), (m[0] + 1 if m[0] + 1 < N else m[0] - 1, m[1]), (m[0], m[1] + 1 if m[1] + 1 < N else m[1] - 1)] if nm(c) != nm(m)]
    return mcq(pic + "La case %s est coloriée. Dans quelle case est sa symétrique par rapport à la droite rouge ?" % nm((x, y)), nm(m), w,
               "On compte les carreaux jusqu’à l’axe, puis le même nombre de l’autre côté : <b>%s</b>." % nm(m))


def s5():
    return point_q()


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Figure symétrique ou non ?", mix(R, seen, [(s1, 20)])),
        ("Axes de symétrie", mix(R, seen, [(s2, 20)])),
        ("Compléter : axe vertical ou horizontal", mix(R, seen, [(s3, 20)])),
        ("Le symétrique d’un point" if lv == 1 else "Compléter : axe diagonal", mix(R, seen, [(s4, 20)])),
        ("Trouver la case symétrique", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Deux figures sont <b>symétriques</b> par rapport à une droite si elles se superposent quand on plie le long de cette droite (l’<b>axe</b>).",
         "Un point et son symétrique sont à la <b>même distance</b> de l’axe, sur une même perpendiculaire à l’axe, de chaque côté.",
         "Sur quadrillage, on compte les carreaux <b>à partir de l’axe</b>." + (" Avec un axe en diagonale, on compte les carreaux en diagonale : les lignes deviennent des colonnes." if lv == 2 else "")],
        [example("Une case à 2 carreaux au-dessus d’un axe horizontal", ["même distance : 2 carreaux", "de l’autre côté : en dessous"], "2 carreaux sous l’axe")],
        [["Faire glisser la figure au lieu de la retourner", "Ce qui touche l’axe d’un côté touche l’axe de l’autre côté."],
         ["Compter depuis le bord du quadrillage", "On compte toujours depuis l’axe."],
         ["Croire que la diagonale d’un rectangle est un axe de symétrie", "Seul le carré a ses diagonales comme axes."]])
    faq = [("Comment vérifier une symétrie ?", "On plie le long de l’axe, ou on pose un miroir sur l’axe, ou on utilise un papier calque retourné."),
           ("Combien d’axes de symétrie a un carré ?", "4 : deux médianes et deux diagonales.")]
    unit(lv, R, "symetrie-axiale", "E",
         ("Reconnaître des axes de symétrie ; compléter ou construire une figure symétrique par rapport à une droite horizontale ou verticale sur quadrillage" if lv == 1 else
          "Reconnaître des axes de symétrie ; construire le symétrique d’une figure sur quadrillage par rapport à une droite verticale, horizontale ou à une diagonale du quadrillage"),
         "La symétrie axiale", "Symétrie axiale",
         "Fiches de maths %s sur la symétrie axiale : figures symétriques, axes de symétrie, compléter sur quadrillage (axe vertical, horizontal%s) et cases symétriques. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", diagonal"),
         "Même distance de l’axe, de l’autre côté.", "On compte les carreaux à partir de l’axe.",
         body, faq, sets, 22)


if __name__ == "__main__":
    build(1)
