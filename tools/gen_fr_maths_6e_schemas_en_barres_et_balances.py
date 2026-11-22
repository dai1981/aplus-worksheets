# -*- coding: utf-8 -*-
"""
France Maths 6e : Schémas en barres, balances et suites (pré-algèbre, programme 2025)
  python3 tools/gen_fr_maths_6e_schemas_en_barres_et_balances.py
Modéliser un problème avec un schéma en barres (tout et parties, comparaison), raisonner sur une balance en équilibre,
continuer une suite de motifs, problèmes « deux nombres dont on connaît la somme et la différence ».
Erreurs : ajouter tous les nombres de l’énoncé, enlever seulement d’un côté de la balance, compter de 1 en 1 au lieu de la régularité.
"""
import random
from fr_c4 import *

R = random.Random(60112)
K = Kids(R)


def bars(rows, total=None, unit_w=None):
    """rows : [(nom, [(valeur, texte, couleur)])] — barres à l’échelle"""
    mx = max(sum(v for v, _, _ in parts) for _, parts in rows)
    sc = 300.0 / mx
    s = []
    y = 14
    for nm, parts in rows:
        x = 90
        s.append(text(82, y + 22, nm, 14, anchor="end"))
        for v, t, col in parts:
            w = v * sc
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='1.8'/>" % (x, y, w, col, INK))
            s.append(text(x + w / 2, y + 22, t, 14))
            x += w
        y += 44
    if total:
        x1 = 90 + mx * sc
        s.append(line(90, y + 2, x1, y + 2, INK, 1.5) + line(90, y - 4, 90, y + 8, INK, 1.5) + line(x1, y - 4, x1, y + 8, INK, 1.5))
        s.append(text(90 + mx * sc / 2, y + 22, total, 14))
        y += 30
    return wrap(410, y + 6, "".join(s), "schéma en barres", lg=True)


A, B, C = "#cfe6d6", "#f6d6a8", "#f2c6d0"


def s1():
    a, b = R.randint(12, 90), R.randint(12, 90)
    t = a + b
    p = K.next()
    k = R.choice(["partie", "tout"])
    if k == "partie":
        svg = bars([("", [(a, str(a), A), (b, "?", B)])], total=str(t))
        return M("<div class='qfig'>%s</div>%s a %d cartes. %d sont des cartes de foot, les autres de basket. Combien de cartes de basket ?" % (svg, p[0], t, a), str(b), [str(t + a), str(a), str(b + 10)],
                 "Le tout moins la partie connue : %d − %d = <b>%d</b>." % (t, a, b))
    c = R.randint(10, 60)
    svg = bars([("", [(a, str(a), A), (b, str(b), B), (c, str(c), C)])], total="?")
    return M("<div class='qfig'>%s</div>Quel nombre représente toute la barre ?" % svg, str(a + b + c), [str(a + b), str(a + b + c + 10), str(max(a, b, c) * 3)],
             "%d + %d + %d = <b>%d</b>." % (a, b, c, a + b + c))


def s2():
    p, q = K.two()
    a, dd = R.randint(15, 80), R.randint(5, 40)
    b = a + dd
    k = R.choice(["grand", "petit", "ecart"])
    if k == "grand":
        svg = bars([(p[0], [(a, str(a), A)]), (q[0], [(a, str(a), A), (dd, str(dd), B)])])
        return M("<div class='qfig'>%s</div>%s a %d points. %s a %d points de plus. Combien a %s ?" % (svg, p[0], a, q[0], dd, q[0]), str(b), [str(a - dd) if a > dd else str(b + 1), str(dd), str(b + dd)],
                 "La barre %s est plus longue de %d : %d + %d = <b>%d</b>." % (de_n(q[0]), dd, a, dd, b))
    if k == "petit":
        svg = bars([(p[0], [(a, "?", A), (dd, str(dd), "#ffffff")]), (q[0], [(b, str(b), B)])])
        return M("<div class='qfig'>%s</div>%s a %d billes. %s en a %d de moins. Combien %s en a-t-%s ?" % (svg, q[0], b, p[0], dd, p[0], p[1]), str(a), [str(b + dd), str(dd), str(a - 1)],
                 "%d − %d = <b>%d</b>." % (b, dd, a))
    svg = bars([(p[0], [(a, str(a), A)]), (q[0], [(b, str(b), B)])])
    return M("<div class='qfig'>%s</div>Combien %s a-t-%s de plus %s ?" % (svg, q[0], q[1], que(p[0])), str(dd), [str(a + b), str(b), str(dd + 1)],
             "On cherche la différence des barres : %d − %d = <b>%d</b>." % (b, a, dd))


def balance_svg(nl, cl, cr, label):
    """à gauche : nl boîtes « ? » et cl en masses ; à droite : cr"""
    s = [line(210, 40, 210, 170, INK, 4), "<path d='M180 178 h60 l-10 -10 h-40 Z' fill='%s'/>" % INK, line(40, 40, 380, 40, INK, 4),
         line(60, 40, 60, 92, INK, 1.4), line(140, 40, 140, 92, INK, 1.4), line(280, 40, 280, 92, INK, 1.4), line(360, 40, 360, 92, INK, 1.4),
         "<path d='M30 92 h140 l-12 14 h-116 Z' fill='#dddddd' stroke='%s'/>" % INK, "<path d='M250 92 h140 l-12 14 h-116 Z' fill='#dddddd' stroke='%s'/>" % INK]
    x = 40
    for i in range(nl):
        s.append("<rect x='%d' y='62' width='26' height='30' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, A, GREEN) + text(x + 13, 82, "?", 15, col=RED))
        x += 30
    if cl:
        s.append("<rect x='%d' y='66' width='%d' height='26' rx='4' fill='#bdbdbd' stroke='%s'/>" % (x, 16 + 9 * len(str(cl)), INK) + text(x + 8 + 4.5 * len(str(cl)), 84, str(cl), 13))
    s.append("<rect x='%d' y='66' width='%d' height='26' rx='4' fill='#bdbdbd' stroke='%s'/>" % (300, 16 + 9 * len(str(cr)), INK) + text(308 + 4.5 * len(str(cr)), 84, str(cr), 13))
    return wrap(420, 186, "".join(s), label, lg=True)


def s3():
    x = R.randint(2, 25)
    n = R.randint(1, 4)
    c = R.choice([0, R.randint(1, 30)])
    r = n * x + c
    svg = balance_svg(n, c, r, "balance en équilibre")
    left = ("%d boîte%s" % (n, "s" if n > 1 else "")) + (" et %d g" % c if c else "")
    w = [str((r - c) // n + 1), str(r - c), str(Fr(r, n) if (r % n == 0 and r // n != x) else x + 2), str(r // n if c and r % n == 0 and r // n != x else x - 1 if x > 1 else x + 3)]
    return M("<div class='qfig'>%s</div>La balance est en équilibre. Toutes les boîtes ont la même masse. À gauche : %s ; à droite : %d g. Quelle est la masse d’une boîte ?" % (svg, left, r), "%d g" % x,
             ["%s g" % v for v in w if v != str(x)],
             ("On enlève %d g de chaque côté : %s = %d g. " % (c, "%d boîtes" % n if n > 1 else "1 boîte", r - c) if c else "") + ("Puis %d ÷ %d = <b>%d g</b>." % (r - c, n, x) if n > 1 else "Une boîte pèse <b>%d g</b>." % x))


def s4():
    a, st = R.randint(1, 6), R.randint(2, 6)
    n = R.choice([5, 6, 10, 20])
    seq = [a + st * i for i in range(4)]
    k = R.choice(["next", "n"])
    obj = R.choice(["allumettes", "jetons", "carrés"])
    if k == "next":
        return M("Dans une suite de motifs, il faut %s %s pour les motifs 1, 2, 3, 4. Combien en faut-il pour le motif 5 ?" % (", ".join(map(str, seq)), obj), str(a + st * 4), [str(a + st * 4 + 1), str(seq[-1] + 1), str(seq[-1] * 2)],
                 "On ajoute %d à chaque motif : %d + %d = <b>%d</b>." % (st, seq[-1], st, a + st * 4))
    return M("Dans une suite de motifs, il faut %s %s pour les motifs 1, 2, 3, 4. Combien en faut-il pour le motif %d ?" % (", ".join(map(str, seq)), obj, n), str(a + st * (n - 1)),
             [str(a * n), str(st * n), str(a + st * n)], "On part de %d et on ajoute %d fois %d : %d + %d × %d = <b>%d</b>." % (a, n - 1, st, a, n - 1, st, a + st * (n - 1)))


def s5():
    p, q = K.two()
    small, dd = R.randint(8, 60), R.randint(2, 30)
    t = 2 * small + dd
    k = R.choice(["somdiff", "double", "triple"])
    if k == "somdiff":
        svg = bars([(p[0], [(small, "?", A)]), (q[0], [(small, "?", A), (dd, str(dd), B)])], total=None)
        return M("<div class='qfig'>%s</div>%s et %s ont %d images en tout. %s en a %d de plus %s. Combien %s en a-t-%s ?" % (svg, p[0], q[0], t, q[0], dd, que(p[0]), p[0], p[1]),
                 str(small), [str(t // 2), str(small + dd), str(t - dd)],
                 "On enlève les %d en plus : %d − %d = %d, c’est deux barres égales. %d ÷ 2 = <b>%d</b>." % (dd, t, dd, t - dd, t - dd, small))
    m = 2 if k == "double" else 3
    t = small * (m + 1)
    svg = bars([(p[0], [(small, "?", A)]), (q[0], [(small, "", A)] * m)])
    return M("<div class='qfig'>%s</div>%s et %s ont %d € en tout. %s a %s de %s. Combien a %s ?" % (svg, p[0], q[0], t, q[0], "le double" if m == 2 else "le triple", "ce qu’a " + p[0], p[0]),
             "%d €" % small, ["%d €" % (t // 2), "%d €" % (small * m), "%d €" % (t // m)],
             "Il y a %d parts égales : %d ÷ %d = <b>%d €</b>." % (m + 1, t, m + 1, small))


def main():
    seen = set()
    sets = [("Le tout et les parties", mix(R, seen, [(s1, 20)])), ("Comparer avec des barres", mix(R, seen, [(s2, 20)])),
            ("Balances en équilibre", mix(R, seen, [(s3, 20)])), ("Suites de motifs", mix(R, seen, [(s4, 20)])), ("Problèmes à plusieurs inconnues", mix(R, seen, [(s5, 20)]))]
    body = L(["Un <b>schéma en barres</b> représente les quantités par des barres : le tout est la somme des parties.",
              "Sur une <b>balance en équilibre</b>, on peut enlever la même masse des deux côtés, ou partager chaque côté en parts égales.",
              "Dans une suite de motifs, on cherche ce qui change d’un motif au suivant."],
             [("Léa et Tom ont 50 billes ; Tom en a 8 de plus", ["50 − 8 = 42", "42 ÷ 2 = 21"], "Léa 21, Tom 29")],
             [["Additionner tous les nombres de l’énoncé", "On dessine le schéma pour voir ce qu’on cherche : une partie ou le tout."],
              ["Enlever seulement d’un côté de la balance", "Pour garder l’équilibre, on enlève la même chose des deux côtés."],
              ["Compter tous les motifs un par un", "On repère ce qu’on ajoute à chaque fois : motif 10 = départ + 9 ajouts."]])
    faq = [("À quoi servent les schémas en barres ?", "À voir les relations entre les nombres avant de calculer ; ils préparent l’algèbre."),
           ("Pourquoi une balance ?", "Elle montre une égalité : ce qu’on fait d’un côté, on le fait de l’autre. C’est l’idée des équations.")]
    unit("6e", R, "schemas-en-barres-et-balances", "N",
         "Modéliser des problèmes à l’aide de schémas en barres ; raisonner avec des balances en équilibre ; étudier des suites de motifs évolutives ; préparer l’usage des écritures symboliques",
         "Schémas en barres, balances et suites", "Schémas en barres et balances",
         "Fiches de maths 6e de pré-algèbre : schémas en barres, comparaisons, balances en équilibre, suites de motifs et problèmes. 100 exercices corrigés.",
         "Le tout = la somme des parties.", "Sur une balance, on fait la même chose des deux côtés.", body, faq, sets, 12)


if __name__ == "__main__":
    main()
