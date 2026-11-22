# -*- coding: utf-8 -*-
"""
France Maths CP : Le sens de la soustraction ; CE1 (build(1)) : La soustraction posée
  python3 tools/gen_fr_maths_cp_soustraction.py
Erreurs : enlever le petit chiffre du grand dans chaque colonne (52 − 27 = 35), oublier la retenue,
additionner au lieu de soustraire pour un écart, compter le nombre de départ en reculant.
"""
import random
from fr_c2 import que, pl, mcq, num, lesson, example, unit, mix, Kids, GN, posee, pic, ch, KINDS, nom, de
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53007 + 100 * lv)
    K = Kids(R)


def dg(n):
    return [int(d) for d in str(n).rjust(3, "0")][::-1]


def borrows(a, b):
    da, db = dg(a), dg(b)
    c = n = 0
    for k in range(3):
        if da[k] - db[k] - c < 0:
            n, c = n + 1, 1
        else:
            c = 0
    return n


def flip(a, b):
    da, db = dg(a), dg(b)
    return int("".join(str(abs(da[k] - db[k])) for k in (2, 1, 0)))


def no_borrow(a, b):
    da, db = dg(a), dg(b)
    return int("".join(str((da[k] - db[k]) % 10) for k in (2, 1, 0)))


def task(a, b, need=None):
    if b >= a:
        return None
    n = borrows(a, b)
    if need is not None and (n != need if need < 2 else n < 2):
        return None
    r = a - b
    w = [flip(a, b) if n else None, no_borrow(a, b) if n else None, r + 10, r - 10, r + 1, a + b if a + b < 1000 else None]
    e = "On aligne les unités et on calcule de droite à gauche."
    if n:
        e += " Quand le chiffre du haut est trop petit, on ajoute 10 en haut et 1 au chiffre du bas de la colonne suivante (retenue)."
    e += " %s − %s = <b>%s</b>. Vérification : %s + %s = %s." % (num(a), num(b), num(r), num(r), num(b), num(a))
    return mcq(posee([str(a), str(b)], op="−") + "Calcule : %s − %s" % (num(a), num(b)), num(r), [num(x) for x in w if x and 0 < x != r], e)


def wr(v, *xs):
    return [str(x) for x in xs if x >= 0 and x != v]


# ---------------------------------------------------------------- CP
def c1():
    n = R.randint(4, 15)
    k = R.randint(1, n - 1)
    kind = R.choice(KINDS)
    svg = pic(KP.crossed_row_svg(n, kind, k), "%s, %d sont barrés" % (ch(kind, n), k))
    return mcq("<div class='qfig'>%s</div>On enlève les objets barrés. Combien en reste-t-il ?" % svg, str(n - k), wr(n - k, n, k, n + k, n - k + 1),
               "%d − %d = <b>%d</b>." % (n, k, n - k))


def c2():
    a = R.randint(6, 20)
    b = R.randint(1, min(9, a - 1))
    if R.random() < 0.35 and a <= 10:
        svg = pic(KP.hop_line_svg(a, -b, 0, 10), "droite de 0 à 10 : on part de %d et on recule de %d" % (a, b))
        return mcq("<div class='qfig'>%s</div>On part de %d et on recule de %d. Où arrive-t-on ?" % (svg, a, b), str(a - b), wr(a - b, a - b + 1, a + b, a - b - 1),
                   "%d − %d = <b>%d</b>." % (a, b, a - b))
    return mcq("%d − %d = …" % (a, b), str(a - b), wr(a - b, a - b + 1, a + b, a - b - 1 if a - b > 1 else a - b + 2),
               "%d − %d = <b>%d</b>. On peut vérifier : %d + %d = %d." % (a, b, a - b, a - b, b, a))


def c3():
    a = R.randint(21, 99)
    if R.random() < 0.4:
        d = R.randint(1, a // 10 - 1) * 10 if a >= 20 else 10
        return mcq("%d − %d = …" % (a, d), str(a - d), wr(a - d, a - d // 10, a + d, a - d - 10), "On enlève %s, les unités ne changent pas : <b>%d</b>." % (pl(d // 10, "dizaine"), a - d))
    b = R.randint(11, a - 1)
    if b % 10 > a % 10 or b // 10 >= a // 10:
        return None
    return mcq("%d − %d = …" % (a, b), str(a - b), wr(a - b, a + b if a + b < 100 else a - b + 10, a - b - 10, a - b + 1),
               "Dizaines : %d − %d = %d ; unités : %d − %d = %d. Résultat : <b>%d</b>." % (a // 10, b // 10, a // 10 - b // 10, a % 10, b % 10, a % 10 - b % 10, a - b))


def c4():
    a = R.randint(8, 20)
    b = R.randint(2, min(9, a - 1))
    r = a - b
    k = R.choice(["miss", "lien", "miss2"])
    if k == "miss":
        return mcq("%d − … = %d" % (a, r), str(b), wr(b, a + r, r, b + 1), "%d − <b>%d</b> = %d, car %d + %d = %d." % (a, b, r, r, b, a))
    if k == "miss2":
        return mcq("… − %d = %d" % (b, r), str(a), wr(a, r - b if r > b else r + 1, a + 1, a - 1), "<b>%d</b> − %d = %d, car %d + %d = %d." % (a, b, r, r, b, a))
    return mcq("%d + %d = %d. Alors %d − %d = …" % (r, b, a, a, b), str(r), wr(r, a + b, b, r + 1), "Si %d + %d = %d, alors %d − %d = <b>%d</b>." % (r, b, a, a, b, r))


def c5():
    p, q = K.two()
    k = R.choice(["reste", "ecart", "manque", "perd"])
    if k == "reste":
        a, b = R.randint(12, 40), R.randint(3, 9)
        return mcq("%s a %d bonbons. %s en mange %d. Combien lui en reste-t-il ?" % (p[0], a, p[1].capitalize(), b), str(a - b), wr(a - b, a + b, a - b + 1, b),
                   "%d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "ecart":
        a, b = R.randint(10, 20), R.randint(3, 9)
        return mcq("%s a %d ans. %s a %d ans. Combien d’années de plus a %s ?" % (p[0], a, q[0], b, p[0]), str(a - b), wr(a - b, a + b, a - b + 1, a),
                   "On cherche l’écart : %d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "manque":
        a, b = R.randint(11, 20), R.randint(2, 9)
        if b >= a:
            return None
        return mcq("Il faut %d chaises pour la classe. Il y en a %d. Combien de chaises manque-t-il ?" % (a, b), str(a - b), wr(a - b, a + b, a - b - 1, b),
                   "%d + … = %d : il manque <b>%d</b> chaises." % (b, a, a - b))
    a, b = R.randint(15, 60), R.randint(10, 30)
    if b % 10 > a % 10 or b >= a:
        return None
    return mcq("Dans un bus, il y a %d personnes. Au premier arrêt, %d personnes descendent. Combien de personnes restent dans le bus ?" % (a, b), str(a - b), wr(a - b, a + b if a + b < 100 else a - b + 1, a - b - 10, a - b + 10),
               "%d − %d = <b>%d</b>." % (a, b, a - b))


# ---------------------------------------------------------------- CE1
def e1():
    return task(R.randint(35, 989), R.randint(12, 478), 0)


def e2():
    return task(R.randint(52, 980), R.randint(17, 590), 1)


def e3():
    if R.random() < 0.5:
        a = R.choice(range(100, 1000, 10)) + (0 if R.random() < 0.5 else R.randint(1, 9))
        a = R.choice([a, a // 100 * 100 + R.randint(0, 9)])
        return task(a, R.randint(15, a - 5) if a > 20 else 5, 2)
    return task(R.randint(300, 950), R.randint(108, 299), 2)


def e4():
    a, b = R.randint(120, 950), R.randint(35, 390)
    if b >= a:
        return None
    r = a - b
    k = R.choice(["verif", "miss"])
    if k == "verif":
        return mcq("%s − %s = %s. Quelle addition permet de vérifier ?" % (num(a), num(b), num(r)), "%s + %s = %s" % (num(r), num(b), num(a)),
                   ["%s + %s = %s" % (num(a), num(b), num(a + b)) if a + b < 1000 else "%s − %s = %s" % (num(a), num(r), num(b)), "%s + %s = %s" % (num(r), num(a), num(r + a)) if r + a < 1000 else "%s + %s = %s" % (num(b), num(b), num(2 * b)), "%s − %s = %s" % (num(a), num(b), num(r + 10))],
                   "Différence + nombre enlevé = premier nombre : <b>%s + %s = %s</b>." % (num(r), num(b), num(a)))
    sa = str(r)
    i = R.randrange(len(sa))
    d = sa[i]
    shown = sa[:i] + "□" + sa[i + 1:]
    return mcq("Quel chiffre remplace le □ : %s − %s = %s ?" % (num(a), num(b), shown), d, [str((int(d) + 1) % 10), str((int(d) + 9) % 10), str((int(d) + 2) % 10)],
               "%s − %s = %s, donc le chiffre caché est <b>%s</b>." % (num(a), num(b), num(r), d))


def e5():
    p, q = K.two()
    k = R.choice(["reste", "ecart", "manque", "prix", "page"])
    a, b = R.randint(150, 900), R.randint(48, 399)
    if b >= a:
        return None
    r = a - b
    w = [num(flip(a, b)) if borrows(a, b) else num(r + 10), num(a + b) if a + b < 1000 else num(r - 10), num(r + 100) if r + 100 < 1000 else num(r - 1)]
    if k == "reste":
        return mcq("Un fleuriste a %s roses. Il en vend %s. Combien lui en reste-t-il ?" % (num(a), num(b)), num(r), w, "%s − %s = <b>%s</b> roses." % (num(a), num(b), num(r)))
    if k == "ecart":
        return mcq("%s a %s points. %s a %s points. Combien de points %s a-t-%s de plus %s ?" % (p[0], num(a), q[0], num(b), p[0], p[1], que(q[0])), num(r), w,
                   "On cherche l’écart : %s − %s = <b>%s</b>." % (num(a), num(b), num(r)))
    if k == "manque":
        return mcq("%s veut %s images pour remplir son album. %s en a %s. Combien lui en manque-t-il ?" % (p[0], num(a), p[1].capitalize(), num(b)), num(r), w,
                   "%s + … = %s : il manque <b>%s</b> images (%s − %s)." % (num(b), num(a), num(r), num(a), num(b)))
    if k == "prix":
        return mcq("Un vélo coûte %s €. %s a %s €. Combien lui manque-t-il ?" % (num(a), p[0], num(b)), num(r) + " €", [x + " €" for x in w],
                   "%s − %s = <b>%s €</b>." % (num(a), num(b), num(r)))
    return mcq("Un livre a %s pages. %s en a lu %s. Combien de pages lui reste-t-il à lire ?" % (num(a), p[0], num(b)), num(r), w,
               "%s − %s = <b>%s</b> pages." % (num(a), num(b), num(r)))


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("Enlever des objets", mix(R, seen, [(c1, 20)])), ("Soustraire jusqu’à 20", mix(R, seen, [(c2, 20)])),
                ("Soustraire des dizaines et des unités", mix(R, seen, [(c3, 20)])), ("Le nombre qui manque", mix(R, seen, [(c4, 20)])),
                ("Problèmes", mix(R, seen, [(c5, 20)]))]
        body = lesson(["Soustraire, c’est <b>enlever</b> : on cherche ce qui reste.",
                       "On peut aussi chercher un <b>écart</b> : 9 − 6 = 3, c’est la distance entre 6 et 9.",
                       "Une soustraction se vérifie par une addition : 9 − 6 = 3 car 3 + 6 = 9."],
                      [example("47 − 23", ["dizaines : 4 − 2 = 2", "unités : 7 − 3 = 4"], "24")],
                      [["Additionner au lieu de soustraire", "« Combien en reste-t-il ? » : on enlève."],
                       ["Compter le nombre de départ en reculant", "12 − 3 : on dit 11, 10, 9. Le résultat est 9."],
                       ["Écrire 3 − 9 au lieu de 9 − 3", "On écrit d’abord le plus grand nombre."]])
        faq = [("Quand faut-il soustraire ?", "Quand on cherche ce qui reste, ce qui manque ou un écart entre deux nombres."),
               ("Comment vérifier une soustraction ?", "On ajoute le résultat et le nombre enlevé : on doit retrouver le premier nombre.")]
        unit(lv, R, "sens-de-la-soustraction", "N",
             "Comprendre le sens de la soustraction (retirer, chercher un écart ou un complément) ; calculer des soustractions jusqu’à 20 et de nombres à deux chiffres sans retenue ; utiliser le lien entre addition et soustraction",
             "Le sens de la soustraction", "Soustraction",
             "Fiches de maths CP sur la soustraction : enlever, soustraire jusqu’à 20, dizaines et unités, nombre qui manque et problèmes. 100 exercices corrigés.",
             "Soustraire, c’est enlever.", "9 − 6 = 3 car 3 + 6 = 9.", body, faq, sets, 7)
        return
    sets = [("Sans retenue", mix(R, seen, [(e1, 20)])), ("Avec une retenue", mix(R, seen, [(e2, 20)])),
            ("Plusieurs retenues et zéros", mix(R, seen, [(e3, 20)])), ("Vérifier et chiffres manquants", mix(R, seen, [(e4, 20)])),
            ("Problèmes", mix(R, seen, [(e5, 20)]))]
    body = lesson(["On pose le plus grand nombre en haut et on <b>aligne les unités</b>.",
                   "On calcule de droite à gauche. Si le chiffre du haut est trop petit, on <b>ajoute 10</b> en haut et 1 au chiffre du bas de la colonne suivante.",
                   "On vérifie avec une addition : résultat + nombre enlevé = premier nombre."],
                  [example("352 − 127", ["u : 2 − 7 impossible → 12 − 7 = 5, retenue", "d : 5 − (2 + 1) = 2", "c : 3 − 1 = 2"], "225")],
                  [["Enlever le petit du grand : 352 − 127 = 235", "On enlève toujours le chiffre du bas : 12 − 7 = 5."],
                   ["Oublier la retenue", "Écris la retenue sous le chiffre de la colonne suivante."],
                   ["Mal aligner les nombres", "Unités sous unités, dizaines sous dizaines."]])
    faq = [("Quelle technique utilise-t-on ?", "Ici, la technique par compensation (on ajoute 10 en haut et 1 en bas). Si ta classe emprunte à la colonne voisine, le résultat est le même."),
           ("Comment savoir s’il faut soustraire ?", "Quand on cherche ce qui reste, ce qui manque ou un écart.")]
    unit(lv, R, "soustraction-posee", "N",
         "Calculer en colonnes des soustractions de nombres jusqu’à trois chiffres avec une technique usuelle ; contrôler le résultat par une addition ; résoudre des problèmes de reste, de manque ou d’écart",
         "La soustraction posée", "Soustraction posée",
         "Fiches de maths CE1 sur la soustraction posée jusqu’à 1 000 : sans et avec retenues, zéros, vérification et problèmes. 100 exercices corrigés.",
         "On aligne les unités et on commence à droite.", "On vérifie : résultat + nombre enlevé = premier nombre.", body, faq, sets, 7)


if __name__ == "__main__":
    build(0)
