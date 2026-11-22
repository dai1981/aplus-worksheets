# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les grands nombres entiers (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_nombres.py
CM1 : jusqu’à 999 999. CM2 : jusqu’à 999 999 999. Lire et écrire en chiffres et en lettres, valeur d’un chiffre,
« chiffre des » et « nombre de », décompositions, relations entre unités de numération, problèmes.
Erreurs : oublier les zéros (quarante mille sept → 4 007), confondre chiffre des centaines et nombre de centaines,
oublier un rang vide dans une décomposition.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, FOIS, lettres_big, RANGS, RANG1, RANGP, GN, table, de, un_zero_de_moins

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52101 + 100 * lv)
    K = Kids(R)


def big():
    """un nombre avec des zéros intérieurs"""
    nd = R.randint(5, 6) if L == 1 else R.randint(7, 9)
    ds = [R.randint(1, 9)] + [R.choice([0, 0, R.randint(1, 9)]) for _ in range(nd - 1)]
    return int("".join(map(str, ds)))


def sans_zeros(n):
    return int(str(n).replace("0", "") or "0")


def s1():
    n = big()
    if "0" not in str(n):
        return None
    k = R.random()
    w = [un_zero_de_moins(n), sans_zeros(n) if sans_zeros(n) > 99 else None, n * 10 if n * 10 < (10 ** 6 if L == 1 else 10 ** 9) else n // 10, n + 10 ** (len(str(n)) - 2)]
    if k < 0.55:
        return mcq("Quel nombre s’écrit « %s » ?" % lettres_big(n), num(n), [num(x) for x in w if x and x != n],
                   "On écrit chaque classe sur 3 chiffres, sans oublier les zéros : <b>%s</b>." % num(n))
    ws = [lettres_big(x) for x in w if x and x != n]
    return mcq("Comment s’écrit %s en lettres ?" % num(n), lettres_big(n), ws, "%s se lit <b>%s</b>." % (num(n), lettres_big(n)))


def s2():
    n = big()
    s = str(n)
    i = R.randrange(len(s))
    pos = len(s) - 1 - i
    if R.random() < 0.6:
        d = s[i]
        wr = [s[j] for j in (i - 1, i + 1) if 0 <= j < len(s)] + [str((int(d) + 1) % 10), str(pos)]
        return mcq("Dans %s, quel est le chiffre des %s ?" % (num(n), RANGS[pos]), d, wr,
                   "On lit de droite à gauche : unités, dizaines, centaines… Le chiffre des %s est <b>%s</b>." % (RANGS[pos], d))
    if pos == 0:
        return None
    nb = n // 10 ** pos
    if nb < 10:
        return None
    return mcq("Combien y a-t-il %s en tout dans %s ?" % (de(RANGP[pos]), num(n)), num(nb),
               [s[i], num(nb * 10), num(nb // 10) if nb >= 10 else num(nb + 1)],
               "Le nombre %s, c’est tout ce qui est écrit jusqu’au rang des %s, ce rang compris : <b>%s</b>." % (de(RANGP[pos]), RANGS[pos], num(nb)))


def s3():
    n = big()
    parts = [(int(d), len(str(n)) - 1 - j) for j, d in enumerate(str(n)) if d != "0"]
    if len(parts) < 3:
        return None
    if R.random() < 0.5:
        q = " + ".join("%d %s %s" % (d, FOIS, num(10 ** p)) if p else str(d) for d, p in parts)
        e = "Chaque produit donne la valeur d’un chiffre. On n’oublie pas les rangs vides (0) : <b>%s</b>." % num(n)
    else:
        q = " + ".join("%d %s" % (d, RANG1[p] if d == 1 else RANGP[p]) for d, p in parts)
        e = "On place chaque chiffre à son rang et on met des 0 dans les rangs vides : <b>%s</b>." % num(n)
    return mcq("Quel nombre est égal à %s ?" % q, num(n), [num(sans_zeros(n)), num(n * 10) if L == 2 and n < 10 ** 8 else num(n + 10 ** parts[-1][1]),
                                                       num(int("".join(str(d) for d, _ in parts)) * 10)], e)


def s4():
    k = R.choice(["mille", "plus", "moins", "rel"])
    if k == "rel":
        a, b = R.sample(range(3, 9 if L == 2 else 6), 2)
        if a <= b:
            a, b = b, a
        return mcq("Combien %s y a-t-il dans 1 %s ?" % (de(RANGP[b]), RANG1[a]), num(10 ** (a - b)), [num(10 ** (a - b + 1)), num(10 ** (a - b - 1)) if a - b > 1 else "100", str(a - b)],
                   "Chaque rang vaut 10 fois le rang à sa droite : 1 %s = <b>%s</b> %s." % (RANG1[a], num(10 ** (a - b)), RANGP[b]))
    n = big()
    st = R.choice([1000, 10000, 100000] + ([1000000] if L == 2 else []))
    if k == "plus":
        r = n + st
        return mcq("Quel nombre obtient-on en ajoutant %s à %s ?" % (num(st), num(n)), num(r), [num(n + st // 10), num(n + st * 10), num(n - st) if n > st else num(r + 1)],
                   "On ajoute 1 au chiffre des %s (avec une retenue si besoin) : <b>%s</b>." % (RANGS[len(str(st)) - 1], num(r)))
    if n <= st:
        return None
    r = n - st
    return mcq("Quel nombre obtient-on en enlevant %s à %s ?" % (num(st), num(n)), num(r), [num(n - st // 10), num(n + st), num(n - st * 10) if n > st * 10 else num(r - 1)],
               "On enlève 1 au chiffre des %s : <b>%s</b>." % (RANGS[len(str(st)) - 1], num(r)))


VILLES = [("Bordeaux", 261804), ("Nantes", 323204), ("Lille", 236710), ("Rennes", 227830), ("Strasbourg", 291313), ("Montpellier", 307101),
          ("Toulouse", 511684), ("Nice", 348085)]


def s5():
    p = K.next()
    k = R.choice(["billets", "pages", "ville", "km"] + (["region"] if L == 2 else []))
    if k == "billets":
        n = R.randint(12, 99) * 1000 + R.randint(1, 9) * 100
        return mcq("Une banque range %s pièces de 1 € en rouleaux de 100. Combien de rouleaux complets obtient-elle ?" % num(n), num(n // 100), [num(n // 1000), num(n // 10), num(n % 1000 // 100)],
                   "Le nombre de centaines de %s est <b>%s</b>." % (num(n), num(n // 100)))
    if k == "pages":
        n = R.randint(20, 90) * 1000 + R.choice([0, 500])
        return mcq("Une imprimerie emballe %s feuilles par paquets de 1 000. Combien de paquets complets fait-elle ?" % num(n), num(n // 1000), [num(n // 100), num(n // 10000), num(n // 1000 + 1)],
                   "Le nombre de milliers de %s est <b>%s</b>." % (num(n), num(n // 1000)))
    if k == "ville":
        v, n = R.choice(VILLES)
        return mcq("%s compte %s habitants. Comment lit-on ce nombre ?" % (v, num(n)), lettres_big(n), [lettres_big(sans_zeros(n)) if sans_zeros(n) != n else lettres_big(n + 1000), lettres_big(n // 1000 * 1000), lettres_big(n + 100000)],
                   "On lit la classe des milliers, puis celle des unités : <b>%s</b>." % lettres_big(n))
    if k == "km":
        a = R.randint(110, 480) * 1000 + R.randint(1, 999)
        return mcq("La Lune est à environ 384 400 km de la Terre. Une sonde a parcouru %s km. Le chiffre des centaines de mille de ce nombre est…" % num(a), str(a // 100000), [str(a // 10000 % 10), str(a // 1000 % 10), str(a % 10)],
                   "%s : le chiffre des centaines de mille est <b>%d</b>." % (num(a), a // 100000))
    n = R.randint(1, 12) * 1000000 + R.randint(100, 999) * 1000
    return mcq("Une région compte %s habitants. Combien de millions d’habitants complets cela fait-il ?" % num(n), str(n // 1000000), [num(n // 1000), num(n // 100000), str(n // 1000000 + 1)],
               "Le nombre de millions de %s est <b>%d</b>." % (num(n), n // 1000000))


TXT = {1: ("nombres-jusqu-a-999-999", "Les nombres jusqu’à 999 999", "Nombres jusqu’à 999 999", "999 999"),
       2: ("nombres-jusqu-a-999-999-999", "Les grands nombres jusqu’à 999 999 999", "Nombres jusqu’au milliard", "999 999 999")}


def build(lv):
    setup(lv)
    slug, title, short, top = TXT[lv]
    seen = set()
    sets = [
        ("Lire et écrire les nombres", mix(R, seen, [(s1, 20)])),
        ("Chiffre des… et nombre de…", mix(R, seen, [(s2, 20)])),
        ("Décomposer un nombre", mix(R, seen, [(s3, 20)])),
        ("Unités de numération", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    cls = "la classe des millions, des milliers et des unités" if lv == 2 else "la classe des milliers et celle des unités"
    body = lesson(
        ["On sépare le nombre en <b>classes de 3 chiffres</b> à partir de la droite : %s." % cls,
         "Chaque rang vaut <b>10 fois</b> le rang à sa droite : 1 millier = 10 centaines, 1 million = 1 000 milliers.",
         "Le <b>chiffre des</b> centaines est un seul chiffre. Le <b>nombre de</b> centaines compte toutes les centaines (on lit tout ce qui est à gauche).",
         "Les zéros marquent les rangs vides : on ne les oublie jamais."],
        [example("Dans 3 482 615", ["chiffre des centaines : 6", "nombre de centaines : 34 826"], "6 et 34 826") if lv == 2 else
         example("Dans 482 615", ["chiffre des centaines : 6", "nombre de centaines : 4 826"], "6 et 4 826"),
         example("« quarante mille sept »", ["40 milliers et 7 unités", "classe des unités : 007"], "40 007")],
        [["Oublier les zéros : quarante mille sept = 4 007", "La classe des unités a 3 chiffres : 40 007."],
         ["Confondre chiffre et nombre de centaines", "Dans 4 826, le chiffre des centaines est 8, le nombre de centaines est 48."],
         ["Mettre un « s » à mille", "Mille est invariable : deux mille, cinq mille."]],
        table(["Classe", "Rangs"], ([["millions", "centaines · dizaines · unités de millions"]] if lv == 2 else []) +
              [["milliers", "centaines · dizaines · unités de mille"], ["unités", "centaines · dizaines · unités"]]))
    faq = [("Quand écrit-on « cents » ou « vingts » avec un s ?", "Quand ils sont multipliés et terminent le nombre : deux cents, quatre-vingts. Mais deux cent trois, quatre-vingt-un, deux cent mille."),
           ("Jusqu’où va-t-on en %s ?" % GN(lv), "Jusqu’à %s." % top)]
    unit(lv, R, slug, "N",
         "Connaître les relations entre les unités de numération et la suite écrite et orale des nombres jusqu’à %s ; connaître la valeur d’un chiffre selon sa position ; passer d’une représentation d’un nombre à une autre" % top,
         title, short,
         "Fiches de maths %s sur les nombres jusqu’à %s : lire et écrire en lettres, chiffre des et nombre de, décompositions, unités de numération et problèmes. 100 exercices corrigés." % (GN(lv), top),
         "Je sépare le nombre en classes de 3 chiffres.", "Chiffre des centaines ≠ nombre de centaines.",
         body, faq, sets, 1)


if __name__ == "__main__":
    build(1)
