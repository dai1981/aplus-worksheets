# -*- coding: utf-8 -*-
"""
France Maths CE2 : Se repérer et se déplacer sur un quadrillage (Espace et géométrie)
  python3 tools/gen_fr_maths_ce2_se_reperer_et_se_deplacer.py
Repérer une case (B3) sur un quadrillage, trouver ce qui est dans une case, se déplacer avec des consignes
(3 cases vers la droite) ou un codage de flèches, écrire un codage, vocabulaire (gauche, droite, au-dessus…).
Erreurs : inverser lettre et chiffre (3B), compter la case de départ, confondre gauche et droite.
"""
import math, random
from fr_common import mcq, lesson, example, make_unit, mix, wrap, text, line, INK, GREEN, RED, BLUE

R = random.Random(51019)
COLS, ROWS, Q = 6, 5, 40
LET = "ABCDEF"
SHAPES = ["l’étoile", "le rond", "le triangle", "le carré", "le losange", "le cœur"]
ARROW = {"→": (1, 0), "←": (-1, 0), "↑": (0, 1), "↓": (0, -1)}


def cell(c):
    return "%s%d" % (LET[c[0]], c[1] + 1)


def sym(kind, cx, cy):
    r = 13
    if kind == "l’étoile":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
        return "<polygon points='%s' fill='#f2c94c' stroke='%s'/>" % (" ".join(pts), INK)
    if kind == "le rond":
        return "<circle cx='%.1f' cy='%.1f' r='%d' fill='#9fc3e8' stroke='%s'/>" % (cx, cy, r - 1, INK)
    if kind == "le triangle":
        return "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#9fd39f' stroke='%s'/>" % (cx, cy - r, cx + r, cy + r * 0.8, cx - r, cy + r * 0.8, INK)
    if kind == "le carré":
        return "<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#e8a0a0' stroke='%s'/>" % (cx - r + 2, cy - r + 2, 2 * r - 4, 2 * r - 4, INK)
    if kind == "le losange":
        return "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#c9a0e8' stroke='%s'/>" % (cx, cy - r, cx + r * 0.75, cy, cx, cy + r, cx - r * 0.75, cy, INK)
    return ("<path d='M%.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f Z' fill='#f08080' stroke='%s'/>"
            % (cx, cy + r, cx - r * 1.4, cy - r * 0.2, cx - r * 0.5, cy - r * 1.3, cx, cy - r * 0.4, cx + r * 0.5, cy - r * 1.3, cx + r * 1.4, cy - r * 0.2, cx, cy + r, INK))


def grille(objs, path=None, start=None):
    x0, y0 = 34, 10
    X = lambda c: x0 + c * Q + Q / 2.0
    Y = lambda r: y0 + (ROWS - 1 - r) * Q + Q / 2.0
    s = []
    for i in range(COLS + 1):
        s.append(line(x0 + i * Q, y0, x0 + i * Q, y0 + ROWS * Q, "#9fb6c4", 1.2))
    for j in range(ROWS + 1):
        s.append(line(x0, y0 + j * Q, x0 + COLS * Q, y0 + j * Q, "#9fb6c4", 1.2))
    for i in range(COLS):
        s.append(text(X(i), y0 + ROWS * Q + 20, LET[i], 15, col=GREEN))
    for j in range(ROWS):
        s.append(text(x0 - 14, Y(j) + 5, str(j + 1), 15, col=GREEN))
    for k, c in objs.items():
        s.append(sym(k, X(c[0]), Y(c[1])))
    if start:
        s.append("<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (X(start[0]), Y(start[1]), RED))
    return wrap(x0 + COLS * Q + 10, y0 + ROWS * Q + 30, "".join(s), "quadrillage : colonnes A à F, lignes 1 à 5", lg=True)


def place(n):
    cells = R.sample([(c, r) for c in range(COLS) for r in range(ROWS)], n)
    kinds = R.sample(SHAPES, n)
    return dict(zip(kinds, cells))


def s1():
    objs = place(R.randint(3, 5))
    k = R.choice(list(objs))
    c = objs[k]
    right = cell(c)
    w = ["%d%s" % (c[1] + 1, LET[c[0]]), "%s%d" % (LET[c[1]], c[0] + 1) if c[1] < COLS and c[0] + 1 <= ROWS and (c[1], c[0]) != c else None,
         "%s%d" % (LET[c[0]], ROWS - c[1]) if ROWS - c[1] != c[1] + 1 else None, "%s%d" % (LET[(c[0] + 1) % COLS], c[1] + 1)]
    return mcq("<div class='qfig'>%s</div>Dans quelle case se trouve %s ?" % (grille(objs), k), right, [x for x in w if x and x != right],
               "On lit d’abord la lettre de la colonne, puis le numéro de la ligne : %s est en <b>%s</b>." % (k, right))


def s2():
    objs = place(4)
    k = R.choice(list(objs))
    c = objs[k]
    others = [x for x in objs if x != k] + ["rien"]
    return mcq("<div class='qfig'>%s</div>Que trouve-t-on dans la case %s ?" % (grille(objs), cell(c)), k, others,
               "Colonne %s, ligne %d : c’est <b>%s</b>." % (LET[c[0]], c[1] + 1, k))


DIRS = {"vers la droite": (1, 0), "vers la gauche": (-1, 0), "vers le haut": (0, 1), "vers le bas": (0, -1)}


def near(cur):
    return [(cur[0] + dx, cur[1] + dy) for dx, dy in ((1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (-1, -1))]


def au(k):
    return "au " + k[3:] if k.startswith("le ") else "à " + k


def ok(c):
    return 0 <= c[0] < COLS and 0 <= c[1] < ROWS


def s3():
    st = (R.randint(0, COLS - 1), R.randint(0, ROWS - 1))
    steps = []
    cur = st
    for _ in range(R.randint(1, 2)):
        d = R.choice(list(DIRS))
        n = R.randint(1, 4)
        nx = (cur[0] + DIRS[d][0] * n, cur[1] + DIRS[d][1] * n)
        if not ok(nx):
            return None
        steps.append((n, d))
        cur = nx
    if cur == st:
        return None
    n0, d0 = steps[0]
    wrong1 = (st[0] + DIRS[d0][0] * (n0 + 1), st[1] + DIRS[d0][1] * (n0 + 1))
    opp = (st[0] - DIRS[d0][0] * n0, st[1] - DIRS[d0][1] * n0)
    for a, b in steps[1:]:
        wrong1 = (wrong1[0] + DIRS[b][0] * a, wrong1[1] + DIRS[b][1] * a)
        opp = (opp[0] + DIRS[b][0] * a, opp[1] + DIRS[b][1] * a)
    w = [cell(x) for x in [wrong1, opp] + near(cur) if ok(x) and x != cur]
    txt = " puis ".join("de %d case%s %s" % (n, "s" if n > 1 else "", d) for n, d in steps)
    return mcq("<div class='qfig'>%s</div>Le robot (point rouge) part de la case %s. Il se déplace %s. Dans quelle case arrive-t-il ?" % (grille({}, start=st), cell(st), txt),
               cell(cur), w, "On ne compte pas la case de départ. Le robot arrive en <b>%s</b>." % cell(cur))


def walk(st, code):
    cur = st
    for a in code:
        cur = (cur[0] + ARROW[a][0], cur[1] + ARROW[a][1])
        if not ok(cur):
            return None
    return cur


def rand_code():
    code = []
    for _ in range(R.randint(2, 3)):
        a = R.choice(list(ARROW))
        if code and ARROW[a][0] == -ARROW[code[-1]][0] and ARROW[a][1] == -ARROW[code[-1]][1]:
            continue
        code += [a] * R.randint(1, 3)
    return code


def s4():
    st = (R.randint(0, COLS - 1), R.randint(0, ROWS - 1))
    code = rand_code()
    end = walk(st, code)
    if not end or end == st:
        return None
    flip = {"→": "←", "←": "→", "↑": "↑", "↓": "↓"}
    w1 = walk(st, [flip[a] for a in code])
    w2 = walk(st, code[:-1])
    w3 = walk(st, code + [code[-1]])
    return mcq("<div class='qfig'>%s</div>Le robot part de %s et suit le code %s. Dans quelle case arrive-t-il ?" % (grille({}, start=st), cell(st), " ".join(code)),
               cell(end), [cell(x) for x in [w1, w2, w3] + near(end) if x and ok(x) and x != end],
               "Chaque flèche fait avancer d’une case. Le robot arrive en <b>%s</b>." % cell(end))


def compress(code):
    out = []
    for a in code:
        out.append(a)
    return " ".join(out)


def s5():
    if R.random() < 0.6:
        st = (R.randint(0, COLS - 1), R.randint(0, ROWS - 1))
        objs = {}
        code = rand_code()
        end = walk(st, code)
        if not end or end == st:
            return None
        k = R.choice(SHAPES)
        objs[k] = end
        dx, dy = end[0] - st[0], end[1] - st[1]
        good = ["→" if dx > 0 else "←"] * abs(dx) + ["↑" if dy > 0 else "↓"] * abs(dy)
        bad1 = ["←" if dx > 0 else "→"] * abs(dx) + ["↑" if dy > 0 else "↓"] * abs(dy)
        bad2 = ["→" if dx > 0 else "←"] * abs(dx) + ["↓" if dy > 0 else "↑"] * abs(dy)
        bad3 = ["→" if dx > 0 else "←"] * (abs(dx) + 1) + ["↑" if dy > 0 else "↓"] * abs(dy)
        if not dx or not dy:
            bad3 = good + [good[-1]]
        opts = [compress(x) for x in (good, bad1, bad2, bad3)]
        if len(set(opts)) < 4:
            return None
        return mcq("<div class='qfig'>%s</div>Quel code conduit le robot de %s jusqu’%s ?" % (grille(objs, start=st), cell(st), au(k)), opts[0], opts[1:],
                   "Il faut %d case%s %s et %d case%s %s : <b>%s</b>." % (abs(dx), "s" if abs(dx) > 1 else "", "vers la droite" if dx > 0 else "vers la gauche",
                                                                        abs(dy), "s" if abs(dy) > 1 else "", "vers le haut" if dy > 0 else "vers le bas", opts[0]))
    objs = place(4)
    a, b = R.sample(list(objs), 2)
    ca, cb = objs[a], objs[b]
    if ca[1] == cb[1] and abs(ca[0] - cb[0]) == 1:
        rel = "juste à gauche" if ca[0] < cb[0] else "juste à droite"
    elif ca[0] == cb[0] and abs(ca[1] - cb[1]) == 1:
        rel = "juste au-dessus" if ca[1] > cb[1] else "juste au-dessous"
    elif ca[1] == cb[1]:
        rel = "sur la même ligne, à gauche" if ca[0] < cb[0] else "sur la même ligne, à droite"
    elif ca[0] == cb[0]:
        rel = "dans la même colonne, au-dessus" if ca[1] > cb[1] else "dans la même colonne, au-dessous"
    else:
        return None
    opp = {"juste à gauche": "juste à droite", "juste à droite": "juste à gauche", "juste au-dessus": "juste au-dessous", "juste au-dessous": "juste au-dessus",
           "sur la même ligne, à gauche": "sur la même ligne, à droite", "sur la même ligne, à droite": "sur la même ligne, à gauche",
           "dans la même colonne, au-dessus": "dans la même colonne, au-dessous", "dans la même colonne, au-dessous": "dans la même colonne, au-dessus"}
    w = [opp[rel]] + [x for x in ["juste au-dessus", "juste à gauche", "dans la même colonne, au-dessous", "sur la même ligne, à droite"] if x not in (rel, opp[rel])]
    return mcq("<div class='qfig'>%s</div>Où se trouve %s par rapport %s ?" % (grille(objs), a, au(b)), rel, w,
               "%s est en %s et %s en %s : %s est <b>%s</b> %s." % (a[0].upper() + a[1:], cell(ca), b, cell(cb), a, rel, "du " + b[3:] if b.startswith("le ") else "de " + b))


def main():
    seen = set()
    sets = [
        ("Trouver la case", mix(R, seen, [(s1, 20)])),
        ("Que trouve-t-on dans la case ?", mix(R, seen, [(s2, 20)])),
        ("Se déplacer avec des consignes", mix(R, seen, [(s3, 20)])),
        ("Suivre un codage", mix(R, seen, [(s4, 20)])),
        ("Écrire un codage et se situer", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Sur un quadrillage, chaque case a un nom : la <b>lettre de la colonne</b>, puis le <b>numéro de la ligne</b>. Exemple : C4.",
         "Pour se déplacer, on compte les cases <b>sans compter la case de départ</b>.",
         "Dans un codage, chaque flèche fait avancer d’une case : → à droite, ← à gauche, ↑ en haut, ↓ en bas.",
         "Pour écrire un codage, on compte combien de cases à droite ou à gauche, puis combien en haut ou en bas."],
        [example("Départ B2, code → → ↑", ["→ → : B2 → C2 → D2", "↑ : D2 → D3"], "D3")],
        [["Écrire le chiffre avant la lettre : 3B", "On écrit la colonne puis la ligne : B3."],
         ["Compter la case de départ", "Le premier pas mène à la case voisine."],
         ["Confondre gauche et droite", "Le sens des flèches suffit : → veut toujours dire vers la droite."]])
    faq = [("Pourquoi apprendre à coder un déplacement ?", "C’est utile pour lire un plan et pour programmer un robot (algorithmique débranchée)."),
           ("Les lignes sont-elles comptées du bas ?", "Sur nos quadrillages, la ligne 1 est en bas, comme sur un graphique. Regarde toujours les numéros écrits sur le bord.")]
    make_unit(R, "se-reperer-et-se-deplacer", "E",
              "Se repérer et repérer des objets sur un quadrillage ; utiliser le vocabulaire de position (gauche, droite, au-dessus, au-dessous) ; programmer et suivre des déplacements avec un codage (résumé du programme 2024 du cycle 2).",
              "Se repérer et se déplacer sur un quadrillage", "Se repérer sur un quadrillage CE2 : fiches et exercices avec corrigé", "Se repérer et se déplacer",
              "Fiches de maths CE2 pour se repérer sur un quadrillage : nommer une case, suivre des consignes et des codages de flèches, écrire un codage et se situer. 100 exercices corrigés.",
              "Une case : la lettre de la colonne, puis le numéro de la ligne.", "On ne compte pas la case de départ.",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
