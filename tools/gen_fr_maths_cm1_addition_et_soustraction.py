# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Addition et soustraction posées (entiers et décimaux)
  python3 tools/gen_fr_maths_cm1_addition_et_soustraction.py
CM1 : entiers jusqu’à 999 999, décimaux jusqu’aux centièmes. CM2 : grands entiers, décimaux jusqu’aux millièmes.
Erreurs : aligner les chiffres à droite au lieu d’aligner les virgules, oublier la retenue, soustraire le petit chiffre du grand,
oublier les zéros (12 − 3,45).
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, dz, posee

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52105 + 100 * lv)
    K = Kids(R)


def digs(n, k=10):
    return [int(c) for c in str(n).rjust(k, "0")][::-1]


def nocarry(a, b):
    da, db = digs(a), digs(b)
    return int("".join(str((da[i] + db[i]) % 10) for i in range(9, -1, -1)))


def flip(a, b):
    da, db = digs(a), digs(b)
    return int("".join(str(abs(da[i] - db[i])) for i in range(9, -1, -1)))


def rows(vals, k):
    """aligner les virgules : vals en 10^-k, chaque nombre écrit avec ses décimales propres"""
    strs = [dz(v, k) for v in vals]
    mx = max(len(s.split(",")[1]) if "," in s else 0 for s in strs)
    out = []
    for s in strs:
        d = len(s.split(",")[1]) if "," in s else 0
        t = s.replace("\u00a0", "")
        out.append(t + " " * ((mx + 1) if d == 0 else (mx - d)) if mx else t)
    return out


def s1():
    hi = 999999 if L == 1 else 99999999
    a, b = R.randint(hi // 50, hi // 2), R.randint(hi // 200, hi // 2)
    if R.random() < 0.3:
        c = R.randint(100, 99999)
        r = a + b + c
        return mcq(posee([str(a), str(b), str(c)]) + "Calcule en posant l’opération : %s + %s + %s" % (num(a), num(b), num(c)), num(r),
                   [num(r + 1000), num(r - 10), num(nocarry(a, b) + c)], "On aligne les unités et on calcule de droite à gauche avec les retenues : <b>%s</b>." % num(r))
    r = a + b
    if nocarry(a, b) == r:
        return None
    return mcq(posee([str(a), str(b)]) + "Calcule en posant l’opération : %s + %s" % (num(a), num(b)), num(r), [num(nocarry(a, b)), num(r + 100), num(r - 1000)],
               "Chaque fois qu’une colonne fait 10 ou plus, on retient 1 : <b>%s</b>." % num(r))


def s2():
    hi = 999999 if L == 1 else 99999999
    a = R.randint(hi // 10, hi)
    b = R.randint(hi // 100, a - 1)
    if R.random() < 0.3:
        a = R.randint(2, 9) * 10 ** (len(str(hi)) - 1) + R.choice([0, 0, R.randint(1, 9) * 100])
        b = R.randint(10 ** (len(str(hi)) - 2), a - 1)
    r = a - b
    if flip(a, b) == r:
        return None
    return mcq(posee([str(a), str(b)], op="−") + "Calcule en posant l’opération : %s − %s" % (num(a), num(b)), num(r), [num(flip(a, b)), num(r + 1000), num(r - 10)],
               "On calcule de droite à gauche ; si le chiffre du haut est trop petit, on fait une retenue. Vérification : %s + %s = %s. Résultat : <b>%s</b>." % (num(r), num(b), num(a), num(r)))


def dec_pair():
    k = 2 if L == 1 else 3
    ka, kb = R.choice([(1, 2), (2, 1), (2, 2), (0, 2), (1, 1)] if L == 1 else [(1, 3), (3, 2), (2, 3), (0, 3), (3, 1)])
    a = R.randint(10 ** (ka + 1), 10 ** (ka + 3)) * 10 ** (k - ka)
    b = R.randint(10 ** kb, 10 ** (kb + 2)) * 10 ** (k - kb)
    if a % 10 ** (k - ka + 1) == 0 and ka or b % 10 ** (k - kb + 1) == 0 and kb:
        return None
    return a, b, ka, kb, k


def wrong_align(a, b, ka, kb, k):
    """aligner à droite : on additionne les écritures sans virgule"""
    sa, sb = a // 10 ** (k - ka), b // 10 ** (k - kb)
    m = max(ka, kb)
    return dz(sa + sb, m), dz(abs(sa - sb), m)


def s3():
    t = dec_pair()
    if not t:
        return None
    a, b, ka, kb, k = t
    r = a + b
    wa, _ = wrong_align(a, b, ka, kb, k)
    rr = rows([a, b], k)
    return mcq(posee(rr) + "Calcule en posant l’opération : %s + %s" % (dz(a, k), dz(b, k)), dz(r, k), [wa, dz(r + 10 ** k, k), dz(nocarry(a, b), k)],
               "On aligne les virgules (unités sous unités, dixièmes sous dixièmes…). On peut compléter avec des 0. Résultat : <b>%s</b>." % dz(r, k))


def s4():
    t = dec_pair()
    if not t:
        return None
    a, b, ka, kb, k = t
    if a <= b:
        a, b, ka, kb = b, a, kb, ka
    if R.random() < 0.3:
        a = R.randint(5, 60) * 10 ** k
        ka = 0
    r = a - b
    _, wd = wrong_align(a, b, ka, kb, k)
    return mcq(posee(rows([a, b], k), op="−") + "Calcule en posant l’opération : %s − %s" % (dz(a, k), dz(b, k)), dz(r, k), [wd, dz(flip(a, b), k), dz(r + 10 ** k, k)],
               "On aligne les virgules et on complète avec des 0 : %s − %s = <b>%s</b>." % (dz(a, k, keep=True), dz(b, k, keep=True), dz(r, k)))


def s5():
    p = K.next()
    k = R.choice(["courses", "rendre", "saut", "estim", "km"])
    if k == "courses":
        a, b, c = R.randint(1500, 4999), R.randint(500, 1999), R.randint(99, 499)
        r = a + b + c
        return mcq("%s achète un jeu à %s €, un livre à %s € et un stylo à %s €. Combien paie-t-%s ?" % (p[0], dz(a, 2, True), dz(b, 2, True), dz(c, 2, True), p[1]), dz(r, 2, True) + " €",
                   [dz(r + 100, 2, True) + " €", dz(r - 10, 2, True) + " €", dz(nocarry(nocarry(a, b), c), 2, True) + " €"],
                   "%s + %s + %s = <b>%s €</b>." % (dz(a, 2, True), dz(b, 2, True), dz(c, 2, True), dz(r, 2, True)))
    if k == "rendre":
        prix = R.randint(1001, 4899)
        bil = 5000 if prix < 5000 else 10000
        r = bil - prix
        return mcq("Un article coûte %s €. On paie avec un billet de %d €. Combien rend-on ?" % (dz(prix, 2, True), bil // 100), dz(r, 2, True) + " €",
                   [dz(flip(bil, prix), 2, True) + " €", dz(r + 100, 2, True) + " €", dz(r - 10, 2, True) + " €"], "%d − %s = <b>%s €</b>." % (bil // 100, dz(prix, 2, True), dz(r, 2, True)))
    if k == "saut":
        kk = 2 if L == 1 else 3
        a, b = R.randint(250, 480) * 10 ** (kk - 2), R.randint(200, 470) * 10 ** (kk - 2) + R.randint(0, 9) * (1 if kk == 3 else 0)
        if a == b:
            return None
        big, sm = max(a, b), min(a, b)
        return mcq("Au saut en longueur, Léo saute %s m et Hugo %s m. Quel est l’écart entre les deux sauts ?" % (dz(a, kk), dz(b, kk)), dz(big - sm, kk) + " m",
                   [dz(big + sm, kk) + " m", dz(flip(big, sm), kk) + " m", dz(big - sm + 10 ** (kk - 1), kk) + " m"], "%s − %s = <b>%s m</b>." % (dz(big, kk), dz(sm, kk), dz(big - sm, kk)))
    if k == "estim":
        a, b = R.randint(2000, 9000) * (1 if L == 1 else 10) + R.randint(1, 99), R.randint(1000, 8000) * (1 if L == 1 else 10) + R.randint(1, 99)
        st = 1000 if L == 1 else 10000
        e = round(a / st) * st + round(b / st) * st
        return mcq("Quel est le meilleur ordre de grandeur de %s + %s ?" % (num(a), num(b)), num(e), [num(e * 10), num(e // 10), num(e + 5 * st)],
                   "On arrondit %s : %s + %s = <b>%s</b>." % ("au millier" if L == 1 else "à la dizaine de mille", num(round(a / st) * st), num(round(b / st) * st), num(e)))
    a, b = R.randint(1200, 9800), R.randint(900, 7600)
    return mcq("Une voiture affiche %s km. Après les vacances, elle affiche %s km. Combien de kilomètres a-t-elle parcourus ?" % (num(a * 10), num(a * 10 + b)), num(b) + " km",
               [num(a * 10 * 2 + b) + " km", num(flip(a * 10 + b, a * 10)) + " km" if flip(a * 10 + b, a * 10) != b else num(b + 100) + " km", num(b + 1000) + " km"],
               "On cherche l’écart : %s − %s = <b>%s km</b>." % (num(a * 10 + b), num(a * 10), num(b)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Addition posée de grands nombres", mix(R, seen, [(s1, 20)])),
        ("Soustraction posée de grands nombres", mix(R, seen, [(s2, 20)])),
        ("Additionner des décimaux", mix(R, seen, [(s3, 20)])),
        ("Soustraire des décimaux", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["On aligne les <b>unités sous les unités</b>. Pour les décimaux, on aligne les <b>virgules</b>.",
         "On peut compléter avec des 0 pour avoir le même nombre de chiffres après la virgule : 12 = 12,00.",
         "On calcule de droite à gauche, avec les retenues, et on place la virgule du résultat sous les autres.",
         "On vérifie avec un ordre de grandeur, ou une soustraction par une addition."],
        [example("12,5 + 3,47", ["12,50 + 3,47", "on aligne les virgules"], "15,97"), example("12 − 3,45", ["12,00 − 3,45"], "8,55")],
        [["Aligner à droite : 12,5 + 3,47 = 4,72", "On aligne les virgules : 15,97."],
         ["Oublier la retenue", "Écris chaque retenue au-dessus de la colonne suivante."],
         ["12 − 3,45 = 9,45 (« 0 − 5 impossible, j’écris 5 »)", "Complète avec des 0 : 12,00 − 3,45 = 8,55."]])
    faq = [("Pourquoi aligner les virgules ?", "Pour additionner des chiffres de même valeur : dixièmes avec dixièmes, centièmes avec centièmes."),
           ("Peut-on ajouter des zéros après la virgule ?", "Oui, à la fin de la partie décimale : 3,4 = 3,40 = 3,400. Cela ne change pas le nombre.")]
    unit(lv, R, "addition-et-soustraction-posees", "N",
         "Estimer le résultat d’une opération ; poser et effectuer l’addition et la soustraction de nombres entiers et de nombres décimaux (%s)" % ("au plus deux chiffres après la virgule" if lv == 1 else "jusqu’aux millièmes"),
         "Addition et soustraction posées : entiers et décimaux", "Addition et soustraction posées",
         "Fiches de maths %s sur l’addition et la soustraction posées de grands nombres et de nombres décimaux, ordre de grandeur et problèmes. 100 exercices corrigés." % GN(lv),
         "On aligne les virgules.", "On complète avec des 0 : 12 = 12,00.",
         body, faq, sets, 5)


if __name__ == "__main__":
    build(1)
