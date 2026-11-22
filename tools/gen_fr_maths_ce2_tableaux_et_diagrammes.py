# -*- coding: utf-8 -*-
"""
France Maths CE2 : Tableaux et diagrammes (Organisation et gestion des données)
  python3 tools/gen_fr_maths_ce2_tableaux_et_diagrammes.py
Lire un tableau, un diagramme en barres, un tableau à double entrée ; comparer et calculer à partir des données ;
compter avec des bâtons, compléter un total.
Erreurs : lire la mauvaise ligne ou colonne, lire la graduation au-dessus de la barre, additionner au lieu de chercher l’écart.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, table, barres

R = random.Random(51020)

THEMES = [("Fruits préférés de la classe", "fruit", ["pomme", "banane", "fraise", "orange", "kiwi"], "élèves"),
          ("Animaux de compagnie des élèves", "animal", ["chat", "chien", "lapin", "poisson", "hamster"], "élèves"),
          ("Livres empruntés à la bibliothèque", "jour", ["lundi", "mardi", "jeudi", "vendredi"], "livres"),
          ("Sports pratiqués par les élèves", "sport", ["football", "judo", "danse", "natation", "tennis"], "élèves"),
          ("Couleurs préférées", "couleur", ["rouge", "bleu", "vert", "jaune", "violet"], "élèves"),
          ("Voitures passées devant l’école", "couleur", ["blanche", "noire", "grise", "rouge"], "voitures")]


def data(lo=2, hi=15, n=None):
    t, key, cats, unit_ = R.choice(THEMES)
    cats = cats[: n or R.randint(3, len(cats))]
    vals = R.sample(range(lo, hi + 1), len(cats))
    return t, key, cats, vals, unit_


def de(u):
    return ("d’" if u[0] in "aeéiou" else "de ") + u


def ask(cats, vals, unit_, kind):
    i = R.randrange(len(cats))
    if kind == "val":
        return ("Combien %s pour « %s » ?" % (de(unit_), cats[i]), vals[i], [vals[(i + 1) % len(vals)], vals[i - 1], vals[i] + 1, vals[i] - 1],
                "On lit la valeur de « %s » : <b>%d</b>." % (cats[i], vals[i]))
    if kind == "max":
        m = vals.index(max(vals))
        return ("Quelle catégorie a le plus %s ?" % de(unit_), cats[m], [cats[j] for j in range(len(cats)) if j != m],
                "La plus grande valeur est %d : <b>%s</b>." % (vals[m], cats[m]))
    if kind == "min":
        m = vals.index(min(vals))
        return ("Quelle catégorie a le moins %s ?" % de(unit_), cats[m], [cats[j] for j in range(len(cats)) if j != m],
                "La plus petite valeur est %d : <b>%s</b>." % (vals[m], cats[m]))
    if kind == "ecart":
        a, b = R.sample(range(len(cats)), 2)
        if vals[a] < vals[b]:
            a, b = b, a
        d = vals[a] - vals[b]
        return ("Combien %s de plus pour « %s » que pour « %s » ?" % (de(unit_), cats[a], cats[b]), d, [vals[a] + vals[b], vals[a], d + 1, d - 1 if d > 1 else d + 2],
                "On cherche l’écart : %d − %d = <b>%d</b>." % (vals[a], vals[b], d))
    tot = sum(vals)
    return ("Combien %s en tout ?" % de(unit_), tot, [tot - vals[-1], tot + 1, max(vals) * len(vals), tot - 1],
            "On additionne toutes les valeurs : %s = <b>%d</b>." % (" + ".join(map(str, vals)), tot))


def s1():
    t, key, cats, vals, u = data()
    q, a, w, e = ask(cats, vals, u, R.choice(["val", "val", "max", "min"]))
    tb = table([key.capitalize(), "Nombre %s" % de(u)], [[c, str(v)] for c, v in zip(cats, vals)])
    return mcq("%s<br>%s<br>%s" % (t, tb, q), a, w, e)


def s2():
    t, key, cats, vals, u = data(2, 18)
    q, a, w, e = ask(cats, vals, u, R.choice(["val", "val", "val", "max", "min"]))
    return mcq("<div class='qfig'>%s</div>%s. %s" % (barres(list(zip(cats, vals)), "nombre %s" % de(u)), t, q), a, w,
               e + " On lit en face du haut de la barre, sur l’axe gradué.")


GRID = [("Élèves de l’école qui mangent à la cantine", ["CP", "CE1", "CE2"], ["filles", "garçons"]),
        ("Médailles gagnées par le club", ["or", "argent", "bronze"], ["2024", "2025"]),
        ("Glaces vendues", ["vanille", "chocolat", "fraise"], ["samedi", "dimanche"]),
        ("Billets vendus pour le spectacle", ["adultes", "enfants"], ["vendredi", "samedi", "dimanche"])]


def s3():
    t, rows, cols = R.choice(GRID)
    vals = [[R.randint(4, 35) for _ in cols] for _ in rows]
    tb = table([""] + cols, [[r] + [str(v) for v in vs] for r, vs in zip(rows, vals)])
    i, j = R.randrange(len(rows)), R.randrange(len(cols))
    k = R.choice(["cell", "cell", "row", "col"])
    if k == "cell":
        v = vals[i][j]
        w = [vals[(i + 1) % len(rows)][j], vals[i][(j + 1) % len(cols)], v + 1, sum(vals[i])]
        return mcq("%s<br>%s<br>Combien pour « %s » et « %s » ?" % (t, tb, rows[i], cols[j]), v, w,
                   "On cherche la case à la croisée de la ligne « %s » et de la colonne « %s » : <b>%d</b>." % (rows[i], cols[j], v))
    if k == "row":
        tot = sum(vals[i])
        return mcq("%s<br>%s<br>Combien en tout pour « %s » ?" % (t, tb, rows[i]), tot, [sum(vals[x][0] for x in range(len(rows))), tot + 1, vals[i][0], tot - 1],
                   "On additionne la ligne « %s » : %s = <b>%d</b>." % (rows[i], " + ".join(map(str, vals[i])), tot))
    tot = sum(vals[x][j] for x in range(len(rows)))
    return mcq("%s<br>%s<br>Combien en tout pour « %s » ?" % (t, tb, cols[j]), tot, [sum(vals[0]), tot + 1, vals[0][j], tot - 2],
               "On additionne la colonne « %s » : %s = <b>%d</b>." % (cols[j], " + ".join(str(vals[x][j]) for x in range(len(rows))), tot))


def s4():
    t, key, cats, vals, u = data(3, 20)
    kind = R.choice(["ecart", "ecart", "tot"])
    q, a, w, e = ask(cats, vals, u, kind)
    if R.random() < 0.5:
        return mcq("<div class='qfig'>%s</div>%s. %s" % (barres(list(zip(cats, vals)), "nombre %s" % de(u)), t, q), a, w, e)
    tb = table([key.capitalize(), "Nombre %s" % de(u)], [[c, str(v)] for c, v in zip(cats, vals)])
    return mcq("%s<br>%s<br>%s" % (t, tb, q), a, w, e)


def batons(n):
    g, r = divmod(n, 5)
    return " ".join(["<s>||||</s>"] * g + (["|" * r] if r else []))


def s5():
    k = R.choice(["batons", "manque", "manque"])
    if k == "batons":
        n = R.randint(6, 23)
        return mcq("Pendant un vote, on compte avec des bâtons. Chaque paquet barré vaut 5. Combien de voix ?<br><span style='font-size:1.4em;letter-spacing:2px'>%s</span>" % batons(n), n,
                   [n + 5 if n % 5 else n - 1, n // 5 + n % 5, n - 1, n + 1],
                   "%d paquet%s de 5 et %d bâton%s : %d %s 5 + %d = <b>%d</b>." % (n // 5, "s" if n // 5 > 1 else "", n % 5, "s" if n % 5 > 1 else "", n // 5, "×", n % 5, n))
    t, key, cats, vals, u = data(3, 18, 4)
    i = R.randrange(len(cats))
    tot = sum(vals)
    rows = [[c, "?" if j == i else str(v)] for j, (c, v) in enumerate(zip(cats, vals))] + [["Total", str(tot)]]
    tb = table([key.capitalize(), "Nombre %s" % de(u)], rows)
    known = tot - vals[i]
    return mcq("%s<br>%s<br>Quel nombre manque dans le tableau ?" % (t, tb), vals[i], [tot + known, known, vals[i] + 1, vals[i] - 1],
               "On enlève au total les valeurs connues : %d − %d = <b>%d</b>." % (tot, known, vals[i]))


def main():
    seen = set()
    sets = [
        ("Lire un tableau", mix(R, seen, [(s1, 20)])),
        ("Lire un diagramme en barres", mix(R, seen, [(s2, 20)])),
        ("Le tableau à double entrée", mix(R, seen, [(s3, 20)])),
        ("Comparer et calculer", mix(R, seen, [(s4, 20)])),
        ("Compter et compléter", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Un <b>tableau</b> range des informations en lignes et en colonnes. On lit le titre et le nom des colonnes avant de chercher.",
         "Dans un <b>diagramme en barres</b>, la hauteur de chaque barre donne un nombre : on lit en face du haut de la barre, sur l’axe gradué.",
         "Dans un <b>tableau à double entrée</b>, une case est à la croisée d’une ligne et d’une colonne.",
         "Pour comparer, on calcule un <b>écart</b> (soustraction) ; pour un total, on additionne."],
        [example("Chat : 7, chien : 12. Combien de chiens de plus que de chats ?", ["écart : 12 − 7"], "5")],
        [["Lire la mauvaise ligne", "Suis la ligne avec ton doigt jusqu’à la bonne colonne."],
         ["Lire la graduation au-dessus de la barre", "Lis la graduation exactement à la hauteur du haut de la barre."],
         ["Additionner pour trouver « combien de plus »", "« Combien de plus » : on fait une soustraction."]])
    faq = [("À quoi sert un diagramme ?", "Il permet de comparer des nombres d’un coup d’œil : la barre la plus haute est la plus grande valeur."),
           ("Comment compter avec des bâtons ?", "On trace un bâton par élément et on barre chaque groupe de 5 : on compte ensuite de 5 en 5.")]
    make_unit(R, "tableaux-et-diagrammes", "D",
              "Lire, interpréter et compléter des tableaux, des tableaux à double entrée et des diagrammes en barres ; recueillir des données ; résoudre des problèmes à partir de ces données (résumé du programme 2024 du cycle 2).",
              "Tableaux et diagrammes", "Tableaux et diagrammes CE2 : fiches et exercices avec corrigé", "Tableaux et diagrammes",
              "Fiches de maths CE2 sur les tableaux et les diagrammes en barres : lire, comparer, tableau à double entrée, totaux et comptage avec des bâtons. 100 exercices corrigés.",
              "Je lis le titre, puis la ligne et la colonne.", "Pour « combien de plus », je fais une soustraction.",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
