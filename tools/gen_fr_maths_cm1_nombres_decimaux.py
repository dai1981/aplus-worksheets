# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les nombres décimaux (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_nombres_decimaux.py
CM1 : jusqu’aux centièmes. CM2 : jusqu’aux millièmes. Lire et écrire, valeur des chiffres, partie entière, arrondi à l’entier,
comparer, ranger, encadrer, intercaler, problèmes.
Erreurs : 2,15 &gt; 2,7 « car 15 &gt; 7 », chiffre des dixièmes et centièmes inversés, 3,6 arrondi à 3.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, dz

R = K = None
L = 1
RG = {1: "dixièmes", 2: "centièmes", 3: "millièmes"}


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52112 + 100 * lv)
    K = Kids(R)


def km():
    return 2 if L == 1 else 3


def rv(k=None):
    k = k or R.randint(1, km())
    v = R.randint(10 ** k, 999 * 10 ** k)
    if v % 10 == 0:
        return None, k
    return v, k


def s1():
    v, k = rv(km())
    if not v:
        return None
    s = dz(v, k).split(",")
    if R.random() < 0.5:
        i = R.randint(1, k)
        d = s[1][i - 1]
        return mcq("Dans %s, quel est le chiffre des %s ?" % (dz(v, k), RG[i]), d, [s[1][j] for j in range(k) if j != i - 1] + [s[0][-1], str((int(d) + 1) % 10)],
                   "Après la virgule : dixièmes, centièmes%s. Le chiffre des %s est <b>%s</b>." % ("" if k == 2 else ", millièmes", RG[i], d))
    ip = v // 10 ** k
    return mcq("Quelle est la partie entière de %s ?" % dz(v, k), num(ip), [s[1].lstrip("0") or "0", num(ip + 1), num(int(dz(v, k).replace(",", "").replace("\u00a0", "")[:-1])) if len(s[1]) > 1 else num(ip * 10)],
               "La partie entière est le nombre avant la virgule : <b>%s</b>." % num(ip))


WORDS = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]


def s1b():
    k = R.randint(1, km())
    e = R.randint(1, 60)
    f = R.randint(1, 10 ** k - 1)
    v = e * 10 ** k + f
    from fr_c3 import lettres_big
    ew = lettres_big(e)
    if ew.endswith("un"):
        ew += "e"
    q = "%s unité%s et %s %s" % (ew, "s" if e > 1 else "", lettres_big(f), RG[k] if f > 1 else RG[k][:-1])
    return mcq("Comment s’écrit « %s » ?" % q, dz(v, k), [dz(e * 10 ** (len(str(f))) + f, len(str(f))) if len(str(f)) != k else dz(v, k + 1), dz(v * 10, k + 1) if k < 3 else "%d,%d" % (f, e), "%d,%d" % (e, f * 10)],
               "%s %s = %s. Résultat : <b>%s</b>." % (lettres_big(f), RG[k], dz(f, k), dz(v, k)))


def s2():
    k1, k2 = R.randint(1, km()), R.randint(1, km())
    if k1 == k2:
        k2 = km() if k1 != km() else 1
    a = R.randint(1, 30)
    va = a * 10 ** k1 + R.randint(1, 10 ** k1 - 1)
    vb = a * 10 ** k2 + R.randint(1, 10 ** k2 - 1)
    if va % 10 == 0 or vb % 10 == 0:
        return None
    A, B = dz(va, k1), dz(vb, k2)
    fa, fb = va / 10 ** k1, vb / 10 ** k2
    if fa == fb:
        return None
    sg = "&lt;" if fa < fb else "&gt;"
    return mcq("Quel signe faut-il mettre : %s … %s ?" % (A, B), sg, ["&gt;" if sg == "&lt;" else "&lt;", "=", "on ne peut pas savoir"],
               "On compare la partie entière, puis les dixièmes, puis les centièmes… (on peut compléter avec des 0) : %s <b>%s</b> %s." % (A, sg, B))


def s3():
    k = km()
    base = R.randint(1, 20)
    xs = set()
    while len(xs) < 4:
        kk = R.randint(1, k)
        v = base * 10 ** kk + R.randint(1, 10 ** kk - 1)
        if v % 10:
            xs.add((v / 10 ** kk, dz(v, kk)))
    xs = sorted(xs)
    R.shuffle(xs)
    good = [s for _, s in sorted(xs)]
    by_len = [s for _, s in sorted(xs, key=lambda t: (len(t[1]), t[1]))]
    rev = good[::-1]
    sw = good[:]
    sw[1], sw[2] = sw[2], sw[1]
    f = lambda l: " &lt; ".join(l)
    return mcq("Range dans l’ordre croissant : %s" % " ; ".join(s for _, s in xs), f(good), [f(by_len), f(rev), f(sw), f(good[1:] + good[:1])],
               "On compare la partie entière, puis les dixièmes, les centièmes… : <b>%s</b>." % f(good))


def s4():
    k = R.randint(1, km())
    v = R.randint(10 ** k, 99 * 10 ** k)
    if v % 10 == 0:
        return None
    t = R.choice(["arr", "enc", "inter"])
    e = v // 10 ** k
    if t == "arr":
        fd = v % 10 ** k
        if fd * 2 == 10 ** k:
            return None
        r = e + (1 if fd * 2 > 10 ** k else 0)
        return mcq("Quel est l’arrondi à l’unité de %s ?" % dz(v, k), num(r), [num(e if r != e else e + 1), dz(v // 10 ** (k - 1), 1) if k > 1 else num(e * 10 + fd), num(r + 1)],
                   "%s est entre %d et %d. Le chiffre des dixièmes est %d : %s de <b>%d</b>." % (dz(v, k), e, e + 1, v // 10 ** (k - 1) % 10, "on est plus près" if True else "", r))
    if t == "enc":
        return mcq("Encadre %s entre deux nombres entiers consécutifs." % dz(v, k), "%d &lt; %s &lt; %d" % (e, dz(v, k), e + 1),
                   ["%d &lt; %s &lt; %d" % (e - 1, dz(v, k), e), "%d &lt; %s &lt; %d" % (e + 1, dz(v, k), e + 2), "%s &lt; %s &lt; %s" % (dz(v // 10 ** (k - 1), 1), dz(v, k), dz(v // 10 ** (k - 1) + 1, 1)) if k > 1 else "%d &lt; %s &lt; %d" % (e, dz(v, k), e + 10)],
                   "La partie entière est %d : <b>%d &lt; %s &lt; %d</b>." % (e, e, dz(v, k), e + 1))
    a = R.randint(10, 99) * 10 ** (km() - 1)
    lo, hi = dz(a, km()), dz(a + 10 ** (km() - 1), km())
    mid = a + 10 ** (km() - 1) // 2
    return mcq("Quel nombre est compris entre %s et %s ?" % (lo, hi), dz(mid, km()), [dz(a // 10 ** (km() - 1) * 10 ** (km() - 1) - 10 ** (km() - 1) // 2, km()), dz(a + 10 ** km(), km()), dz(mid, km() + 1)],
                   "%s &lt; <b>%s</b> &lt; %s." % (lo, dz(mid, km()), hi))


def s5():
    p, o = K.two()
    k = R.choice(["saut", "course", "masse", "prix"])
    if k in ("saut", "course"):
        kk = 2 if k == "saut" else km()
        base = R.randint(3, 4) if k == "saut" else R.randint(9, 14)
        vs = [base * 10 ** kk + R.randint(1, 10 ** kk - 1) for _ in range(3)]
        if len(set(vs)) < 3:
            return None
        names = [p[0], o[0], K.next()[0]]
        if len(set(names)) < 3:
            return None
        if k == "saut":
            best = names[vs.index(max(vs))]
            return mcq("Saut en longueur : %s." % ", ".join("%s %s m" % (n, dz(v, kk)) for n, v in zip(names, vs)) + " Qui a sauté le plus loin ?", best, [n for n in names if n != best] + ["ils sont à égalité"],
                       "On compare les dixièmes puis les centièmes : <b>%s</b>." % best)
        best = names[vs.index(min(vs))]
        return mcq("Course de 100 m : %s." % ", ".join("%s %s s" % (n, dz(v, kk)) for n, v in zip(names, vs)) + " Qui a gagné (le temps le plus court) ?", best, [n for n in names if n != best] + ["ils sont à égalité"],
                   "Le plus petit temps gagne : <b>%s</b>." % best)
    if k == "masse":
        a = R.randint(1, 3) * 1000 + R.randint(1, 999)
        return mcq("Un melon pèse %s kg. Quel est l’arrondi de sa masse au kilogramme près ?" % dz(a, 3), "%d kg" % round(a / 1000), ["%d kg" % (a // 1000 + (0 if round(a / 1000) > a // 1000 else 1)), "%d kg" % (a % 1000 // 100), "%d kg" % (a // 100)],
                   "Le chiffre des dixièmes est %d : <b>%d kg</b>." % (a % 1000 // 100, round(a / 1000)))
    a, b = R.randint(105, 999), R.randint(105, 999)
    if a // 100 == b // 100 or a == b:
        a = b + R.choice([-7, 9, 30])
    cheap = "le cahier A" if a < b else "le cahier B"
    return mcq("Le cahier A coûte %s €, le cahier B coûte %s €. Lequel est le moins cher ?" % (dz(a, 2, True), dz(b, 2, True)), cheap, ["le cahier B" if cheap == "le cahier A" else "le cahier A", "ils ont le même prix", "on ne peut pas savoir"],
               "%s € %s %s € : <b>%s</b>." % (dz(min(a, b), 2, True), "&lt;", dz(max(a, b), 2, True), cheap))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Lire et écrire un décimal", mix(R, seen, [(s1, 12), (s1b, 8)])),
        ("Comparer deux décimaux", mix(R, seen, [(s2, 20)])),
        ("Ranger des décimaux", mix(R, seen, [(s3, 20)])),
        ("Arrondir, encadrer, intercaler", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Dans 12,347 : 12 est la <b>partie entière</b> ; 3 est le chiffre des dixièmes, 4 des centièmes%s." % ("" if lv == 1 else ", 7 des millièmes"),
         "Pour comparer : d’abord la partie entière, puis les dixièmes, puis les centièmes… On peut compléter avec des 0 : 2,7 = 2,70.",
         "Arrondir à l’unité : on regarde le chiffre des dixièmes. 0 à 4 : on garde la partie entière ; 5 à 9 : on ajoute 1."],
        [example("Comparer 2,15 et 2,7", ["2,15 et 2,70", "1 dixième &lt; 7 dixièmes"], "2,15 &lt; 2,7")],
        [["2,15 &gt; 2,7 car 15 &gt; 7", "On compare les dixièmes : 1 &lt; 7, donc 2,15 &lt; 2,7."],
         ["Le chiffre des centièmes de 4,38 est 3", "3 est aux dixièmes, 8 aux centièmes."],
         ["Arrondir 3,6 à 3", "6 dixièmes, c’est plus de la moitié : 4."]])
    faq = [("Un nombre décimal est-il toujours plus grand qu’un entier ?", "Non : 0,8 &lt; 1. Il faut comparer les parties entières."),
           ("Peut-on ajouter des 0 à la fin ?", "Oui, à la fin de la partie décimale : 2,7 = 2,70 = 2,700.")]
    unit(lv, R, "nombres-decimaux", "N",
         "Interpréter, représenter, lire et écrire des nombres décimaux (au plus %s chiffres après la virgule) ; donner la partie entière et l’arrondi à l’entier ; comparer, encadrer, intercaler et ordonner des nombres décimaux" % ("deux" if lv == 1 else "trois"),
         "Les nombres décimaux", "Nombres décimaux",
         "Fiches de maths %s sur les nombres décimaux : lire et écrire, partie entière, comparer, ranger, arrondir à l’unité, encadrer et problèmes. 100 exercices corrigés." % GN(lv),
         "2,15 &lt; 2,7 : on compare les dixièmes (1 &lt; 7).", "On peut écrire des 0 à la fin : 2,7 = 2,70.",
         body, faq, sets, 12)


if __name__ == "__main__":
    build(1)
