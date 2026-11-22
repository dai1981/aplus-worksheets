# -*- coding: utf-8 -*-
"""
France Maths 6e : Données, tableaux et graphiques
  python3 tools/gen_fr_maths_6e_donnees_et_diagrammes.py
Tableaux à double entrée, diagrammes en barres, graphiques cartésiens, organiser des données d’une enquête, proportions.
Erreurs : lire la mauvaise ligne ou colonne, lire la graduation au-dessus, confondre effectif et valeur.
"""
import random
from fr_c4 import *
import gen_fr_maths_ce2_tableaux_et_diagrammes as TD
import de_k10

R = random.Random(60121)
K = Kids(R)
TD.R = R


def s2():
    t, key, cats, vals, u = TD.data(5, 60)
    q, a, w, e = TD.ask(cats, vals, u, R.choice(["val", "max", "ecart", "tot"]))
    return M("<div class='qfig'>%s</div>%s. %s" % (barres(list(zip(cats, vals)), "nombre %s" % TD.de(u)), t, q), str(a), [str(x) for x in w], e)


def s3():
    hs = [8, 10, 12, 14, 16, 18, 20]
    base = R.randint(8, 16)
    ts = [base + R.randint(-1, 1) + [0, 3, 6, 8, 7, 4, 1][i] for i in range(7)]
    pts = list(zip(hs, ts))
    f = lambda x: next((t for h, t in pts if h == round(x)), None)
    import bisect
    def lin(x):
        for (h1, t1), (h2, t2) in zip(pts, pts[1:]):
            if h1 <= x <= h2:
                return t1 + (t2 - t1) * (x - h1) / (h2 - h1)
        return None
    svg = de_k10.kurve([(lin, BLUE, "")], (8, 20, 2), (0, 28, 4), pts=[(h, t, "") for h, t in pts], W=360, H=260)
    svg = relabel(svg, "graphique de la température en fonction de l’heure")
    k = R.choice(["lire", "max", "quand", "ecart"])
    if k == "lire":
        i = R.randrange(7)
        return M("<div class='qfig'>%s</div>Ce graphique donne la température (en °C) en fonction de l’heure. Quelle température fait-il à %d h ?" % (svg, hs[i]), "%d °C" % ts[i],
                 ["%d °C" % (ts[i] + 2), "%d °C" % hs[i] if hs[i] != ts[i] else "%d °C" % (ts[i] - 2), "%d °C" % (ts[i] - 1)],
                 "On part de %d h sur l’axe horizontal, on monte jusqu’à la courbe et on lit sur l’axe vertical : <b>%d °C</b>." % (hs[i], ts[i]))
    if k == "max":
        m = max(ts)
        if ts.count(m) > 1:
            return None
        i = ts.index(m)
        return M("<div class='qfig'>%s</div>À quelle heure fait-il le plus chaud ?" % svg, "à %d h" % hs[i], ["à %d h" % h for h in hs if h != hs[i]][:3],
                 "Le point le plus haut est à <b>%d h</b> (%d °C)." % (hs[i], m))
    if k == "quand":
        i = R.randrange(7)
        if ts.count(ts[i]) > 1:
            return None
        return M("<div class='qfig'>%s</div>À quelle heure la température est-elle de %d °C ?" % (svg, ts[i]), "à %d h" % hs[i], ["à %d h" % h for h in hs if h != hs[i]][:3],
                 "On part de %d °C sur l’axe vertical, on va jusqu’à la courbe, et on lit l’heure : <b>%d h</b>." % (ts[i], hs[i]))
    i, j = sorted(R.sample(range(7), 2))
    return M("<div class='qfig'>%s</div>De combien de degrés la température a-t-elle changé entre %d h et %d h ?" % (svg, hs[i], hs[j]), "%d °C" % abs(ts[j] - ts[i]),
             ["%d °C" % (ts[i] + ts[j]), "%d °C" % (hs[j] - hs[i]) if hs[j] - hs[i] != abs(ts[j] - ts[i]) else "%d °C" % (abs(ts[j] - ts[i]) + 1), "%d °C" % ts[j]],
             "%d °C à %d h et %d °C à %d h : l’écart est <b>%d °C</b>." % (ts[i], hs[i], ts[j], hs[j], abs(ts[j] - ts[i])))


def s4():
    vals = [R.randint(8, 20) for _ in range(R.randint(10, 14))]
    v = R.choice(vals)
    k = R.choice(["eff", "plus", "freq"])
    lst = ", ".join(map(str, vals))
    if k == "eff":
        n = vals.count(v)
        return M("Voici les notes d’un contrôle : %s. Combien d’élèves ont eu %d ?" % (lst, v), str(n), [str(n + 1), str(v), str(len(vals))],
                 "On compte les %d dans la liste : <b>%d</b> élève%s." % (v, n, "s" if n > 1 else ""))
    if k == "plus":
        s_ = 12
        n = sum(1 for x in vals if x >= s_)
        return M("Voici les notes d’un contrôle : %s. Combien d’élèves ont eu au moins 12 ?" % lst, str(n), [str(n - vals.count(12)) if vals.count(12) else str(n + 1), str(len(vals) - n), str(len(vals))],
                 "« Au moins 12 », c’est 12 ou plus : <b>%d</b>." % n)
    tot = R.choice([20, 25, 50])
    part = R.randint(2, tot - 2)
    return M("Dans une classe de %d élèves, %d viennent à pied. Quelle proportion des élèves vient à pied ?" % (tot, part), fr(part, tot), [fr(tot, part), fr(part, 100), fr(tot - part, tot)],
             "%d sur %d : <b>%s</b> (soit %s %%)." % (part, tot, fr(part, tot), d(Fr(part * 100, tot))))


def s5():
    p = K.next()
    k = R.choice(["moy", "tableau", "barre"])
    if k == "moy":
        t, key, cats, vals, u = TD.data(10, 60, 4)
        tb = table([key.capitalize(), "Nombre %s" % TD.de(u)], [[c, str(v)] for c, v in zip(cats, vals)])
        i, j = R.sample(range(len(cats)), 2)
        return M("%s<br>%s<br>Combien %s en tout pour « %s » et « %s » ?" % (t, tb, TD.de(u), cats[i], cats[j]), str(vals[i] + vals[j]), [str(abs(vals[i] - vals[j])), str(sum(vals)), str(vals[i] + vals[j] + 10)],
                 "%d + %d = <b>%d</b>." % (vals[i], vals[j], vals[i] + vals[j]))
    if k == "tableau":
        return TD.s3()
    return TD.s5()


def main():
    seen = set()
    sets = [("Tableaux à double entrée", mix(R, seen, [(TD.s3, 20)])), ("Diagrammes en barres", mix(R, seen, [(s2, 20)])),
            ("Graphiques cartésiens", mix(R, seen, [(s3, 20)])), ("Organiser des données", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Un <b>tableau à double entrée</b> : on lit une case à la croisée d’une ligne et d’une colonne.",
              "Un <b>diagramme en barres</b> : la hauteur de la barre donne l’effectif. Un <b>graphique cartésien</b> montre comment une grandeur change en fonction d’une autre (température en fonction de l’heure).",
              "Pour une enquête, on organise les réponses dans un tableau d’effectifs."],
             [("Notes : 12, 15, 12, 9, 12", ["on compte les 12"], "effectif de la note 12 : 3")],
             [["Lire la mauvaise ligne ou colonne", "On suit du doigt la ligne et la colonne."],
              ["Lire la graduation au-dessus de la barre", "On lit exactement au niveau du haut de la barre."],
              ["Confondre l’effectif et la valeur", "La valeur est la note ; l’effectif est le nombre d’élèves qui l’ont eue."]])
    faq = [("Quand utiliser un graphique cartésien ?", "Pour montrer l’évolution d’une grandeur, par exemple dans le temps."),
           ("Qu’est-ce qu’un effectif ?", "Le nombre de fois qu’une valeur apparaît dans les données.")]
    unit("6e", R, "donnees-et-diagrammes", "D",
         "Recueillir, organiser et représenter des données ; lire et interpréter des tableaux, des tableaux à double entrée, des diagrammes en barres et des graphiques cartésiens ; planifier une enquête",
         "Données, tableaux et graphiques", "Données et graphiques",
         "Fiches de maths 6e sur les données : tableaux à double entrée, diagrammes en barres, graphiques cartésiens, organiser des données et problèmes. 100 exercices corrigés.",
         "On lit d’abord le titre et les axes.", "Effectif = nombre de fois qu’une valeur apparaît.", body, faq, sets, 21)


if __name__ == "__main__":
    main()
