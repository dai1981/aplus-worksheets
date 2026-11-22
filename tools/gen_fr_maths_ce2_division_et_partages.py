# -*- coding: utf-8 -*-
"""
France Maths CE2 : La division : partages et groupements (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_division_et_partages.py
Partages exacts avec les tables, groupements, quotient et reste, diviser un nombre à 2 ou 3 chiffres en le décomposant,
problèmes (dont « combien de boîtes faut-il ? »).
Erreurs : prendre un reste plus grand que le diviseur, oublier la boîte en plus pour le reste, confondre avec × ou −.
"""
import random
from fr_c2 import pl
from fr_common import mcq, num, lesson, example, make_unit, mix, Kids, FOIS, DIV

R = random.Random(51008)
K = Kids(R)


def s1():
    d, q = R.randint(2, 9), R.randint(2, 10)
    n = d * q
    return mcq("Combien font %d %s %d ?" % (n, DIV, d), q, [q + 1, q - 1, n - d, d + q if d + q != q else None, n * d if n * d < 100 else None],
               "On cherche dans la table de %d : %d %s <b>%d</b> = %d, donc %d %s %d = <b>%d</b>." % (d, d, FOIS, q, n, n, DIV, d, q))


OBJ = [("billes", "sacs"), ("crayons", "pots"), ("œufs", "boîtes"), ("photos", "pages"), ("élèves", "équipes"), ("gâteaux", "assiettes")]


def s2():
    o, g = R.choice(OBJ)
    d, q = R.randint(3, 9), R.randint(3, 9)
    n = d * q
    if R.random() < 0.5:
        p = K.next()
        if o in ("élèves", "œufs"):
            return None
        return mcq("%s partage %d %s en %d parts égales. Combien de %s dans chaque part ?" % (p[0], n, o, d, o), q, [q + 1, n - d, d, q - 1],
                   "%d %s %d = <b>%d</b>, car %d %s %d = %d." % (n, DIV, d, q, d, FOIS, q, n))
    return mcq("On range %d %s par groupes de %d. Combien de groupes obtient-on ?" % (n, o, d), q, [q + 1, n - d, n + d, q - 1],
               "On cherche combien de fois %d dans %d : %d %s %d = %d, donc <b>%d</b> groupes." % (d, n, q, FOIS, d, n, q))


def s3():
    d = R.randint(3, 9)
    q, r = R.randint(3, 9), R.randint(1, d - 1)
    n = d * q + r
    p = K.next()
    o, _ = R.choice(OBJ[:4])
    right = "%d chacun, il en reste %d" % (q, r)
    w = ["%d chacun, il en reste %d" % (q - 1, r + d), "%d chacun, il en reste %d" % (q + 1, 0), "%d chacun, il en reste %d" % (q, d - r if d - r != r else r + 1)]
    return mcq("%s partage %d %s entre %d amis. Combien en reçoit chaque ami, et combien en reste-t-il ?" % (p[0], n, o, d), right, w,
               "%d %s %d = %d et %d − %d = %d. Le reste %d est plus petit que %d : <b>%d chacun, reste %d</b>." % (d, FOIS, q, d * q, n, d * q, r, r, d, q, r))


def s3b():
    d = R.randint(3, 9)
    q, r = R.randint(4, 12), R.randint(1, d - 1)
    n = d * q + r
    right = "%d reste %d" % (q, r)
    return mcq("Dans %d, combien de fois %d ? Quel est le reste ?" % (n, d), right, ["%d reste %d" % (q - 1, r + d), "%d reste %d" % (q + 1, 0), "%d reste %d" % (q, r + 1 if r + 1 < d else r - 1)],
               "%d %s %d = %d, il reste %d − %d = %d. Donc <b>%d %s %d = %d reste %d</b>." % (d, FOIS, q, d * q, n, d * q, r, n, DIV, d, q, r))


def s4():
    d = R.randint(2, 5)
    t = R.choice([10, 20, 30, 40]) * d if d * 40 <= 200 else 10 * d
    u = d * R.randint(1, 9)
    n = t + u
    q = n // d
    return mcq("Calcule %d %s %d en décomposant %d." % (n, DIV, d, n), q, [q + 1, t // d, q + 10, n - d],
               "%d = %d + %d. %d %s %d = %d et %d %s %d = %d. Donc %d %s %d = <b>%d</b>." % (n, t, u, t, DIV, d, t // d, u, DIV, d, u // d, n, DIV, d, q))


def s4_moitie():
    n = R.randint(12, 98) * 2
    k = R.choice(["moitié", "quart"])
    if k == "quart":
        if n % 4:
            return None
        return mcq("Quel est le quart de %d ?" % n, n // 4, [n // 2, n - 4, n // 4 + 2],
                   "Le quart, c’est diviser par 4 (la moitié de la moitié) : %d %s 4 = <b>%d</b>." % (n, DIV, n // 4))
    return mcq("Quelle est la moitié de %d ?" % n, n // 2, [n * 2, n - 2, n // 2 + 10 if n // 2 + 10 < n else n // 2 + 1],
               "La moitié, c’est diviser par 2 : %d %s 2 = <b>%d</b>." % (n, DIV, n // 2))


def s5():
    p = K.next()
    k = R.choice(["boites", "voitures", "prix", "rangs", "gateau"])
    if k == "boites":
        d = R.choice([6, 8, 10, 12])
        n = d * R.randint(3, 8) + R.randint(1, d - 1)
        q = n // d + 1
        return mcq("On range %d œufs dans des boîtes de %d. Combien de boîtes faut-il pour ranger tous les œufs ?" % (n, d), q, [q - 1, n - d, q + 1],
                   "%d %s %d = %d reste %d. Il faut une boîte de plus pour %s : <b>%d boîtes</b>." % (n, DIV, d, n // d, n % d, "le dernier œuf" if n % d == 1 else "les %d derniers œufs" % (n % d), q))
    if k == "voitures":
        n = 4 * R.randint(4, 9) + R.randint(1, 3)
        q = n // 4 + 1
        return mcq("%d enfants vont au stade. Chaque voiture peut emmener 4 enfants. Combien de voitures faut-il ?" % n, q, [q - 1, n - 4, n // 2],
                   "%d %s 4 = %d reste %d. Une voiture de plus pour le reste : <b>%d voitures</b>." % (n, DIV, n // 4, n % 4, q))
    if k == "prix":
        d, q = R.randint(3, 9), R.randint(3, 9)
        return mcq("%s paie %d € pour %d livres qui ont tous le même prix. Combien coûte un livre ?" % (p[0], d * q, d), "%d €" % q, ["%d €" % (d * q - d), "%d €" % (d * q * d) if d * q * d < 1000 else "%d €" % (q + 2), "%d €" % (q + 1)],
                   "%d %s %d = <b>%d €</b>." % (d * q, DIV, d, q))
    if k == "rangs":
        d, q = R.randint(4, 9), R.randint(4, 9)
        return mcq("Le maître place %d chaises en %d rangées égales. Combien de chaises dans chaque rangée ?" % (d * q, d), q, [d * q - d, q + 1, d * q + d],
                   "%d %s %d = <b>%d</b> chaises par rangée." % (d * q, DIV, d, q))
    d = R.randint(3, 8)
    q, r = R.randint(3, 8), R.randint(1, d - 1)
    n = d * q + r
    return mcq("%d bonbons sont partagés entre %d enfants. Chacun en a le même nombre, le plus possible. Combien en reste-t-il ?" % (n, d), r, [q, d - r if d - r != r else r + 1, 0],
               "%d %s %d = %d reste %d : il reste <b>%d</b> bonbon%s." % (n, DIV, d, q, r, r, "s" if r > 1 else ""))


def main():
    seen = set()
    sets = [
        ("Diviser avec les tables", mix(R, seen, [(s1, 20)])),
        ("Partager et grouper", mix(R, seen, [(s2, 20)])),
        ("Quotient et reste", mix(R, seen, [(s3, 10), (s3b, 10)])),
        ("Diviser de plus grands nombres", mix(R, seen, [(s4, 12), (s4_moitie, 8)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Diviser, c’est <b>partager en parts égales</b> ou chercher <b>combien de fois</b> un nombre est dans un autre.",
         "On utilise les tables : 35 %s 5 = 7 car 5 %s 7 = 35." % (DIV, FOIS),
         "Quand le partage ne tombe pas juste, il y a un <b>reste</b>. Le reste est toujours <b>plus petit</b> que le nombre de parts.",
         "Pour un grand nombre, on le décompose : 84 %s 4 = 80 %s 4 + 4 %s 4 = 20 + 1 = 21." % (DIV, DIV, DIV)],
        [example("29 billes pour 4 enfants", ["4 %s 7 = 28" % FOIS, "29 − 28 = 1"], "7 billes chacun, il reste 1 bille")],
        [["Un reste trop grand : 29 %s 4 = 6 reste 5" % DIV, "5 est plus grand que 4 : on peut encore donner 1 bille à chacun. 7 reste 1."],
         ["Oublier le reste dans un rangement", "Pour 26 œufs dans des boîtes de 6, il faut 5 boîtes, pas 4."],
         ["Soustraire au lieu de diviser : 24 %s 4 = 20" % DIV, "24 %s 4 = 6 car 4 %s 6 = 24." % (DIV, FOIS)]])
    faq = [("Quel est le lien entre division et multiplication ?", "Ce sont des opérations inverses : si 6 %s 4 = 24, alors 24 %s 4 = 6 et 24 %s 6 = 4." % (FOIS, DIV, DIV)),
           ("Le reste peut-il être égal au diviseur ?", "Non. S’il est égal ou plus grand, on peut encore faire une part de plus.")]
    make_unit(R, "division-et-partages", "N",
              "Résoudre des problèmes de partage et de groupement ; utiliser les tables pour trouver un quotient ; calculer un quotient et un reste ; diviser un nombre en le décomposant ; utiliser le signe ÷ (résumé du programme 2024 du cycle 2).",
              "La division : partager et grouper", "Division CE2 : fiches et exercices avec corrigé", "Division et partages",
              "Fiches de maths CE2 sur la division : partages, groupements, quotient et reste, moitié et quart, décomposition et problèmes. 100 exercices corrigés.",
              "Diviser, c’est partager en parts égales.", "Le reste est toujours plus petit que le nombre de parts.",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
