# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Se repérer et se déplacer
  python3 tools/gen_fr_maths_cp_se_reperer_et_se_deplacer.py
CP : sur, sous, devant, derrière, à côté, à gauche, à droite, entre, au-dessus, en dessous ; déplacements simples sur un quadrillage.
CE1 : repérer une case, se déplacer avec des consignes et des codages de flèches (exercices du générateur CE2 avec un autre tirage).
Erreurs : confondre gauche et droite, sur et au-dessus, compter la case de départ.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, KINDS, le, CHOSE
import k_pics as KP
import gen_fr_maths_ce2_se_reperer_et_se_deplacer as SR

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53016 + 100 * lv)
    K = Kids(R)
    SR.R = R


def s1():
    kind = R.choice(KINDS)
    rel = R.choice(["above", "below", "beside", "beside-left"])
    ans = {"above": "sur la table", "below": "sous la table", "beside": "à droite de la table", "beside-left": "à gauche de la table"}[rel]
    svg = pic(KP.table_scene_svg(kind, rel), "une table et %s" % ("un objet"), lg=True)
    return mcq("<div class='qfig'>%s</div>Où est %s ?" % (svg, le(kind)), ans, [x for x in ["sur la table", "sous la table", "à droite de la table", "à gauche de la table"] if x != ans],
               "On regarde où est l’objet par rapport à la table : <b>%s</b>." % ans)


def s2():
    kind = R.choice(KINDS)
    rel = R.choice(["front", "behind", "beside", "above"])
    ans = {"front": "devant la boîte", "behind": "derrière la boîte", "beside": "à côté de la boîte", "above": "au-dessus de la boîte"}[rel]
    svg = pic(KP.box_scene_svg(kind, rel), "une boîte et un objet", lg=True)
    e = {"front": "On le voit en entier, devant la boîte", "behind": "Il est en partie caché par la boîte", "beside": "Il est à côté", "above": "Il est plus haut que la boîte"}[rel]
    return mcq("<div class='qfig'>%s</div>Où est %s ?" % (svg, le(kind)), ans, [x for x in ["devant la boîte", "derrière la boîte", "à côté de la boîte", "au-dessus de la boîte"] if x != ans],
               "%s : <b>%s</b>." % (e, ans))


def s3():
    n = R.randint(4, 5)
    ks = R.sample(KINDS, n)
    svg = pic(KP.kinds_row_svg(ks), "une rangée d’objets", lg=True)
    k = R.choice(["gauche", "droite", "entre", "premier"])
    if k in ("gauche", "droite"):
        i = R.randint(1, n - 1) if k == "gauche" else R.randint(0, n - 2)
        j = i - 1 if k == "gauche" else i + 1
        others = [le(ks[x]) for x in range(n) if x not in (i, j)]
        return mcq("<div class='qfig'>%s</div>Quel objet est juste à %s %s ?" % (svg, k, ("de l’" + CHOSE[ks[i]][0]) if le(ks[i]).startswith("l’") else ("du " + CHOSE[ks[i]][0]) if le(ks[i]).startswith("le ") else ("de " + le(ks[i]))),
                   le(ks[j]), ([le(ks[2 * i - j])] if 0 <= 2 * i - j < n else []) + others + [le(ks[i])],
                   "Ta gauche est du côté de la main qui ne tient pas le crayon (pour un droitier). Juste à %s : <b>%s</b>." % (k, le(ks[j])))
    if k == "entre":
        i = R.randint(1, n - 2)
        return mcq("<div class='qfig'>%s</div>Quel objet est entre %s et %s ?" % (svg, le(ks[i - 1]), le(ks[i + 1])), le(ks[i]), [le(ks[x]) for x in range(n) if x != i][:3],
                   "Entre les deux, il y a <b>%s</b>." % le(ks[i]))
    first = R.random() < 0.5
    i = 0 if first else n - 1
    return mcq("<div class='qfig'>%s</div>Quel objet est tout à %s ?" % (svg, "gauche" if first else "droite"), le(ks[i]), [le(ks[x]) for x in range(n) if x != i][:3],
               "Tout à %s : <b>%s</b>." % ("gauche" if first else "droite", le(ks[i])))


def s4():
    n = R.randint(3, 4)
    ks = R.sample(KINDS, n)
    svg = pic(KP.shelf_svg(ks), "une étagère avec %d objets" % n, lg=True)
    k = R.choice(["dessus", "dessous", "haut", "bas"])
    if k in ("dessus", "dessous"):
        i = R.randint(1, n - 1) if k == "dessus" else R.randint(0, n - 2)
        j = i - 1 if k == "dessus" else i + 1
        return mcq("<div class='qfig'>%s</div>Quel objet est juste %s %s ?" % (svg, "au-dessus" if k == "dessus" else "en dessous", ("de l’" + CHOSE[ks[i]][0]) if le(ks[i]).startswith("l’") else ("du " + CHOSE[ks[i]][0]) if le(ks[i]).startswith("le ") else ("de " + le(ks[i]))),
                   le(ks[j]), [le(ks[x]) for x in range(n) if x not in (i, j)] + [le(ks[i])],
                   "Juste %s : <b>%s</b>." % ("au-dessus" if k == "dessus" else "en dessous", le(ks[j])))
    i = 0 if k == "haut" else n - 1
    return mcq("<div class='qfig'>%s</div>Quel objet est tout en %s ?" % (svg, k), le(ks[i]), [le(ks[x]) for x in range(n) if x != i][:3],
               "Tout en %s de l’étagère : <b>%s</b>." % (k, le(ks[i])))


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("Sur, sous, à côté", mix(R, seen, [(s1, 20)])), ("Devant, derrière", mix(R, seen, [(s2, 20)])),
                ("À gauche, à droite, entre", mix(R, seen, [(s3, 20)])), ("Au-dessus, en dessous", mix(R, seen, [(s4, 20)])),
                ("Se déplacer sur un quadrillage", mix(R, seen, [(SR.s3, 20)]))]
        th = ["Pour dire où est un objet, on le compare à un autre : <b>sur</b> la table, <b>sous</b> la table, <b>devant</b> la boîte…",
              "À <b>gauche</b>, à <b>droite</b> : on regarde l’image comme si on était devant elle.",
              "Sur un quadrillage, on avance case par case sans compter la case de départ."]
        ex = example("Le ballon est plus haut que la boîte", ["il ne la touche pas"], "au-dessus de la boîte")
        mist = [["Confondre gauche et droite", "Lève la main qui écrit (pour un droitier, c’est la droite)."],
                ["Confondre sur et au-dessus", "Sur : l’objet touche. Au-dessus : il est plus haut."],
                ["Compter la case de départ", "On compte seulement les cases où l’on avance."]]
        faq = [("Comment retenir la gauche et la droite ?", "Avec la main gauche, le pouce et l’index forment un L : L comme… gauche ! On peut aussi repérer la main qui écrit."),
               ("Quelle est la différence entre sur et au-dessus ?", "Sur la table, l’objet touche la table ; au-dessus, il est plus haut sans la toucher.")]
        std = "Se repérer dans l’espace et utiliser le vocabulaire de position (sur, sous, devant, derrière, à gauche, à droite, entre, au-dessus, en dessous) ; se déplacer sur un quadrillage"
        meta = "Fiches de maths CP pour se repérer : sur, sous, devant, derrière, gauche, droite, entre, au-dessus, en dessous et déplacements sur quadrillage. 100 exercices corrigés."
    else:
        sets = [("Trouver la case", mix(R, seen, [(SR.s1, 20)])), ("Que trouve-t-on dans la case ?", mix(R, seen, [(SR.s2, 20)])),
                ("Se déplacer avec des consignes", mix(R, seen, [(SR.s3, 20)])), ("Suivre un codage", mix(R, seen, [(SR.s4, 20)])),
                ("Écrire un codage et se situer", mix(R, seen, [(SR.s5, 20)]))]
        th = ["Sur un quadrillage, une case se repère par une <b>lettre</b> (colonne) et un <b>nombre</b> (ligne) : B3.",
              "Un codage de flèches dit comment avancer : → droite, ← gauche, ↑ haut, ↓ bas.",
              "On ne compte pas la case de départ."]
        ex = example("Le robot part de A1 et fait → → ↑", ["A1 → B1 → C1 ↑ C2"], "C2")
        mist = [["Écrire 3B au lieu de B3", "On écrit d’abord la lettre de la colonne."],
                ["Compter la case de départ", "On compte seulement les cases où l’on avance."],
                ["Confondre gauche et droite", "→ va vers la droite."]]
        faq = [("Dans quel ordre lit-on une case ?", "D’abord la lettre de la colonne, puis le numéro de la ligne."),
               ("Qu’est-ce qu’un codage ?", "Une suite de flèches qui décrit un trajet case par case.")]
        std = "Se repérer sur un quadrillage (repérage d’une case) ; coder et décoder des déplacements ; utiliser le vocabulaire de position"
        meta = "Fiches de maths CE1 pour se repérer sur un quadrillage : trouver une case, suivre des consignes, codages de flèches et vocabulaire. 100 exercices corrigés."
    unit(lv, R, "se-reperer-et-se-deplacer", "E", std, "Se repérer et se déplacer", "Se repérer et se déplacer", meta,
         "On dit où est un objet par rapport à un autre." if lv == 0 else "Une case : lettre puis nombre (B3).", "Sur, sous, devant, derrière, à gauche, à droite." if lv == 0 else "→ ← ↑ ↓ : un codage de déplacements.",
         lesson(th, [ex], mist), faq, sets, 16)


if __name__ == "__main__":
    build(0)
