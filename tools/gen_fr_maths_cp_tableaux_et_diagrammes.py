# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Tableaux et diagrammes
  python3 tools/gen_fr_maths_cp_tableaux_et_diagrammes.py
CP : trier et compter des objets, lire un tableau simple, lire un diagramme en barres, comparer.
CE1 : tableaux, diagrammes en barres, tableaux à double entrée, comparer et calculer, compléter (générateur CE2 avec un autre tirage).
Erreurs : compter deux fois le même objet, lire la mauvaise ligne, additionner au lieu de chercher l’écart.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, KINDS, CHOSE, table, nom, de
import k_pics as KP
import gen_fr_maths_ce2_tableaux_et_diagrammes as TD

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53017 + 100 * lv)
    K = Kids(R)
    TD.R = R


def scene():
    ks = R.sample(KINDS, R.choice([3, 3, 4]))
    cnt = R.sample(range(1, 8), len(ks))
    if sum(cnt) > 24:
        return None
    svg = pic(KP.mixed_svg(list(zip(ks, cnt)), R.randint(1, 10 ** 6)), "des objets mélangés", lg=True)
    return ks, cnt, svg


def s1():
    sc = scene()
    if not sc:
        return None
    ks, cnt, svg = sc
    i = R.randrange(len(ks))
    return mcq("<div class='qfig'>%s</div>Combien y a-t-il %s ?" % (svg, de(ks[i])), str(cnt[i]), [str(cnt[i] + 1), str(cnt[i] - 1) if cnt[i] > 1 else str(cnt[i] + 2), str(sum(cnt))],
               "On compte seulement les %s, en les barrant un par un : <b>%d</b>." % (nom(ks[i]), cnt[i]))


def s5():
    sc = scene()
    if not sc:
        return None
    ks, cnt, svg = sc
    k = R.choice(["plus", "moins", "total", "table"])
    if k in ("plus", "moins"):
        i = cnt.index(max(cnt) if k == "plus" else min(cnt))
        return mcq("<div class='qfig'>%s</div>Quels objets sont les %s nombreux ?" % (svg, k), "les " + nom(ks[i]), ["les " + nom(ks[j]) for j in range(len(ks)) if j != i] + ["ils sont aussi nombreux"],
                   "On compte chaque sorte : %s. Les %s nombreux : <b>les %s</b>." % (", ".join("%d %s" % (c, nom(x, c)) for x, c in zip(ks, cnt)), k, nom(ks[i])))
    if k == "total":
        t = sum(cnt)
        return mcq("<div class='qfig'>%s</div>Combien d’objets y a-t-il en tout ?" % svg, str(t), [str(t + 1), str(t - 1), str(len(ks))],
                   "%s = <b>%d</b>." % (" + ".join(map(str, cnt)), t))
    i = R.randrange(len(ks))
    tb = table(["Objet", "Nombre"], [[nom(x), "?" if j == i else str(c)] for j, (x, c) in enumerate(zip(ks, cnt))])
    return mcq("<div class='qfig'>%s</div>%s<br>Quel nombre faut-il écrire à la place du « ? » ?" % (svg, tb), str(cnt[i]), [str(cnt[i] + 1), str(cnt[i] - 1) if cnt[i] > 1 else str(cnt[i] + 2), str(sum(cnt))],
               "On compte les %s sur l’image : <b>%d</b>." % (nom(ks[i]), cnt[i]))


def s2():
    t, key, cats, vals, u = TD.data(1, 12)
    q, a, w, e = TD.ask(cats, vals, u, R.choice(["val", "val", "max", "min"]))
    tb = table([key.capitalize(), "Nombre %s" % TD.de(u)], [[c, str(v)] for c, v in zip(cats, vals)])
    return mcq("%s<br>%s<br>%s" % (t, tb, q), a, w, e)


def s3():
    t, key, cats, vals, u = TD.data(1, 10)
    q, a, w, e = TD.ask(cats, vals, u, R.choice(["val", "val", "val", "max", "min"]))
    from fr_c2 import barres
    return mcq("<div class='qfig'>%s</div>%s. %s" % (barres(list(zip(cats, vals)), "nombre %s" % TD.de(u)), t, q), a, w,
               e + " On regarde le haut de la barre et on lit le nombre en face.")


def s4():
    t, key, cats, vals, u = TD.data(2, 12, 3)
    q, a, w, e = TD.ask(cats, vals, u, R.choice(["ecart", "tot"]))
    if R.random() < 0.5:
        from fr_c2 import barres
        return mcq("<div class='qfig'>%s</div>%s. %s" % (barres(list(zip(cats, vals)), "nombre %s" % TD.de(u)), t, q), a, w, e)
    tb = table([key.capitalize(), "Nombre %s" % TD.de(u)], [[c, str(v)] for c, v in zip(cats, vals)])
    return mcq("%s<br>%s<br>%s" % (t, tb, q), a, w, e)


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("Trier et compter", mix(R, seen, [(s1, 20)])), ("Lire un tableau", mix(R, seen, [(s2, 20)])),
                ("Lire un diagramme en barres", mix(R, seen, [(s3, 20)])), ("Comparer et calculer", mix(R, seen, [(s4, 20)])),
                ("Compléter un tableau", mix(R, seen, [(s5, 20)]))]
        th = ["Pour compter des objets mélangés, on les <b>trie</b> : on compte une sorte à la fois et on barre ce qu’on a compté.",
              "Un <b>tableau</b> range les nombres en lignes et en colonnes.",
              "Dans un <b>diagramme en barres</b>, plus la barre est haute, plus le nombre est grand."]
        ex = example("Pommes : 5, bananes : 3", ["5 &gt; 3"], "il y a plus de pommes")
        mist = [["Compter deux fois le même objet", "On barre chaque objet compté."],
                ["Lire la mauvaise ligne", "On suit la ligne du doigt jusqu’au nombre."],
                ["Additionner au lieu de chercher l’écart", "« Combien de plus ? » : on fait une soustraction."]]
        faq = [("Comment lire un diagramme en barres ?", "On regarde le haut de la barre et on lit le nombre en face sur le côté."),
               ("Pourquoi trier avant de compter ?", "Pour ne pas oublier d’objet et ne pas en compter deux fois.")]
        std = "Trier et dénombrer des objets ; lire et compléter un tableau simple ; lire un diagramme en barres ; comparer des quantités"
        meta = "Fiches de maths CP sur les tableaux et diagrammes : trier et compter, lire un tableau, un diagramme en barres, comparer et compléter. 100 exercices corrigés."
    else:
        sets = [("Lire un tableau", mix(R, seen, [(TD.s1, 20)])), ("Lire un diagramme en barres", mix(R, seen, [(TD.s2, 20)])),
                ("Le tableau à double entrée", mix(R, seen, [(TD.s3, 20)])), ("Comparer et calculer", mix(R, seen, [(TD.s4, 20)])),
                ("Compter et compléter", mix(R, seen, [(TD.s5, 20)]))]
        th = ["Un <b>tableau</b> range les informations en lignes et en colonnes. On lit d’abord le titre.",
              "Dans un <b>tableau à double entrée</b>, on cherche la case à la croisée d’une ligne et d’une colonne.",
              "Dans un <b>diagramme en barres</b>, on lit la valeur en face du haut de la barre."]
        ex = example("Glaces vendues : vanille 12, chocolat 18", ["18 − 12"], "6 de plus au chocolat")
        mist = [["Lire la mauvaise ligne ou colonne", "On suit la ligne et la colonne du doigt."],
                ["Lire la graduation au-dessus de la barre", "On lit exactement au niveau du haut de la barre."],
                ["Additionner au lieu de chercher l’écart", "« Combien de plus ? » : on fait une soustraction."]]
        faq = [("Qu’est-ce qu’un tableau à double entrée ?", "Un tableau où chaque case dépend d’une ligne et d’une colonne."),
               ("À quoi servent les bâtons ?", "À compter au fur et à mesure ; chaque paquet barré vaut 5.")]
        std = "Lire et utiliser des tableaux, des tableaux à double entrée et des diagrammes en barres ; produire un tableau ; résoudre des problèmes à partir de données"
        meta = "Fiches de maths CE1 sur les tableaux et diagrammes : lire un tableau, un diagramme en barres, un tableau à double entrée, comparer, calculer et compléter. 100 exercices corrigés."
    unit(lv, R, "tableaux-et-diagrammes", "D", std, "Tableaux et diagrammes", "Tableaux et diagrammes", meta,
         "On lit le titre, puis les lignes et les colonnes.", "Barre plus haute = nombre plus grand.", lesson(th, [ex], mist), faq, sets, 17)


if __name__ == "__main__":
    build(0)
