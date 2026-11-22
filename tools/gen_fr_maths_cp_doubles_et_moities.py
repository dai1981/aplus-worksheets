# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Doubles et moitiés
  python3 tools/gen_fr_maths_cp_doubles_et_moities.py
CP : doubles de 1 à 10 et de 20, 30, 40, 50 ; moitiés des nombres pairs jusqu’à 20 et de 40, 60, 80, 100 ; presque-doubles.
CE1 : doubles jusqu’à 50, de 60…500 et des multiples de 25 ; moitiés jusqu’à 100 et de 200…1 000, de 50, 150.
Erreurs : double de 7 = 9 (ajouter 2), moitié de 16 = 4 (moitié de la moitié), double de 35 = 610.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, ch, KINDS, nom
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53008 + 100 * lv)
    K = Kids(R)


def wr(v, *xs):
    return [num(x) for x in xs if x > 0 and x != v]


def dbl_pool():
    if L == 0:
        return list(range(1, 11)) + [20, 30, 40, 50] + list(range(11, 16))
    return list(range(11, 51)) + [60, 70, 80, 90, 100, 150, 200, 250, 300, 400, 500, 25, 75, 125, 175, 225]


def half_pool():
    if L == 0:
        return list(range(2, 21, 2)) + [40, 60, 80, 100, 30, 50]
    return list(range(22, 101, 2)) + [200, 300, 400, 500, 600, 800, 1000, 50, 150, 250, 350, 450, 30, 70, 90, 110, 130]


def s1():
    n = R.randint(1, 6) if L == 0 else R.randint(6, 10)
    if L == 0:
        if R.random() < 0.5:
            svg = pic(KP.dice_svg([n, n]), "deux dés de %d points" % n)
            q = "<div class='qfig'>%s</div>Le double de %d, c’est combien ?" % (svg, n)
        else:
            kind = R.choice(KINDS)
            svg = pic(KP.two_groups_svg(n, kind, n, kind, word="+"), "%s et %s" % (ch(kind, n), ch(kind, n)))
            q = "<div class='qfig'>%s</div>%d + %d = …" % (svg, n, n)
        return mcq(q, str(2 * n), wr(2 * n, 2 * n + 1, 2 * n - 1, n + 2, n), "Le double de %d, c’est %d + %d = <b>%d</b>." % (n, n, n, 2 * n))
    n = R.randint(2, 10)
    if R.random() < 0.3:
        return mcq("La moitié de %d est …" % (2 * n), str(n), wr(n, 4 * n, n + 1, n - 1), "%d + %d = %d : la moitié de %d est <b>%d</b>." % (n, n, 2 * n, 2 * n, n))
    if R.random() < 0.5:
        return mcq("Le double de %d est …" % n, str(2 * n), wr(2 * n, n + 2, 2 * n + 1, n * n if n * n != 2 * n else 2 * n + 2), "%d + %d = <b>%d</b>." % (n, n, 2 * n))
    return mcq("%d est le double de …" % (2 * n), str(n), wr(n, 2 * n + 2 * n if False else 4 * n, n + 1, 2 * n - 2), "%d + %d = %d : %d est le double de <b>%d</b>." % (n, n, 2 * n, 2 * n, n))


def s2():
    n = R.choice(dbl_pool())
    v = 2 * n
    glued = int(str(2 * (n // 10)) + str(2 * (n % 10))) if n >= 10 and 2 * (n % 10) >= 10 else None
    return mcq(R.choice(["Le double de %s est …", "Quel est le double de %s ?", "%s + %s = …"]).replace("%s + %s", "%s + %s" % (num(n), num(n))).replace("%s", num(n)), num(v),
               wr(v, glued or v + 10, n + 2, v + 1, v - 10 if v > 20 else v + 2),
               ("Double de %s : %s + %s = <b>%s</b>." % (num(n), num(n), num(n), num(v))) if n < 10 or n % 10 == 0 else
               "Double de %s : double de %d = %d et double de %d = %d, donc <b>%s</b>." % (num(n), n // 10 * 10, n // 10 * 20, n % 10, 2 * (n % 10), num(v)))


def s3():
    n = R.choice(half_pool())
    v = n // 2
    if L == 0 and n <= 10 and R.random() < 0.5:
        kind = R.choice(KINDS)
        svg = pic(KP.row_svg(n, kind), ch(kind, n))
        return mcq("<div class='qfig'>%s</div>On partage en 2 parts égales. Combien dans chaque part ?" % svg, str(v), wr(v, n, v + 1, v - 1, 2 * n), "%d = %d + %d : la moitié de %d est <b>%d</b>." % (n, v, v, n, v))
    return mcq(R.choice(["La moitié de %s est …", "Quelle est la moitié de %s ?"]) % num(n), num(v), wr(v, n * 2, v // 2 if v % 2 == 0 else v + 2, v + 1, v + 5 if n % 10 == 0 and n >= 20 and (n // 10) % 2 else v - 1),
               "%s + %s = %s : la moitié de %s est <b>%s</b>." % (num(v), num(v), num(n), num(n), num(v)))


def s4():
    if L == 0:
        n = R.randint(2, 9)
        a, b = (n, n + 1) if R.random() < 0.5 else (n + 1, n)
        if R.random() < 0.5:
            return mcq("%d + %d = …   (aide : double de %d)" % (a, b, n), str(2 * n + 1), wr(2 * n + 1, 2 * n, 2 * n + 2, 2 * n + 3),
                       "Double de %d = %d, plus 1 : <b>%d</b>." % (n, 2 * n, 2 * n + 1))
        return mcq("%d + %d = …   (aide : double de %d)" % (a, b, n + 1), str(2 * n + 1), wr(2 * n + 1, 2 * n + 2, 2 * n, 2 * n + 3),
                   "Double de %d = %d, moins 1 : <b>%d</b>." % (n + 1, 2 * n + 2, 2 * n + 1))
    k = R.choice(["presque", "dbl2", "moitie2"])
    if k == "presque":
        n = R.choice([15, 25, 30, 40, 45, 50, 35, 20, 60, 24, 12, 13])
        e = R.choice([1, 2])
        return mcq("%d + %d = …" % (n, n + e), str(2 * n + e), wr(2 * n + e, 2 * n, 2 * n + e + 10, 2 * n + 2 * e), "Double de %d = %d, plus %d : <b>%d</b>." % (n, 2 * n, e, 2 * n + e))
    if k == "dbl2":
        n = R.choice([5, 10, 15, 20, 25, 50, 100, 12, 15])
        return mcq("Le double du double de %d est …" % n, num(4 * n), wr(4 * n, 2 * n, 3 * n, n + 4), "Double de %d = %d, double de %d = <b>%s</b>." % (n, 2 * n, 2 * n, num(4 * n)))
    n = R.choice([40, 80, 100, 200, 60, 120, 400, 20])
    return mcq("La moitié de la moitié de %d est …" % n, num(n // 4), wr(n // 4, n // 2, n // 3 if n % 3 == 0 else n // 4 + 5, 2 * n), "Moitié de %d = %d, moitié de %d = <b>%s</b>." % (n, n // 2, n // 2, num(n // 4)))


def s5():
    p, q = K.two()
    k = R.choice(["dbl", "half", "dbl", "half", "twin"])
    if k == "dbl":
        n = R.choice(dbl_pool()[:14] if L == 0 else dbl_pool())
        th = R.choice(["images", "billes", "points"])
        return mcq("%s a %s %s. %s en a deux fois plus. Combien %s en a-t-%s ?" % (p[0], num(n), th, q[0], q[0], q[1]), num(2 * n), wr(2 * n, n + 2, n, 2 * n + 1),
                   "Deux fois plus, c’est le double : <b>%s</b>." % num(2 * n))
    if k == "half":
        n = R.choice(half_pool())
        th = R.choice(["bonbons", "cartes", "perles"])
        return mcq("%s et %s se partagent %s %s en parts égales. Combien chaque enfant en a-t-il ?" % (p[0], q[0], num(n), th), num(n // 2), wr(n // 2, 2 * n, n // 2 + 1, n - 2),
                   "On cherche la moitié de %s : <b>%s</b>." % (num(n), num(n // 2)))
    n = R.randint(3, 10) if L == 0 else R.choice([12, 15, 20, 25, 30, 50, 45])
    return mcq("Dans un jeu, %s avance de %d cases, puis encore de %d cases. De combien de cases a-t-%s avancé ?" % (p[0], n, n, p[1]), str(2 * n), wr(2 * n, n + 2, 2 * n + 1, n),
               "%d + %d = double de %d = <b>%d</b>." % (n, n, n, 2 * n))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Doubles avec des images" if lv == 0 else "Doubles et moitiés de petits nombres", mix(R, seen, [(s1, 20)])),
        ("Calculer des doubles", mix(R, seen, [(s2, 20)])),
        ("Calculer des moitiés", mix(R, seen, [(s3, 20)])),
        ("Presque des doubles" if lv == 0 else "Presque-doubles, double du double", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    th = ["Le <b>double</b> d’un nombre, c’est ce nombre ajouté à lui-même : double de 6 = 6 + 6 = 12.",
          "La <b>moitié</b>, c’est partager en deux parts égales : la moitié de 12 est 6.",
          "Pour 6 + 7, on pense au double de 6 : 12 + 1 = 13."]
    if lv == 1:
        th[2] = "Double de 35 : double de 30 = 60 et double de 5 = 10, donc 70. Moitié de 150 : 75."
    body = lesson(th, [example("double de 8", ["8 + 8"], "16")] if lv == 0 else [example("double de 35", ["60 + 10"], "70")],
                  [["Double de 7 = 9", "Double, ce n’est pas + 2 : 7 + 7 = 14."],
                   ["Moitié de 16 = 4", "4 + 4 = 8 : la moitié de 16 est 8."],
                   ["Double de 35 = 610" if lv else "Moitié de 20 = 5", "On écrit 60 + 10 = 70." if lv else "5 + 5 = 10 : la moitié de 20 est 10."]])
    faq = [("Pourquoi apprendre les doubles ?", "Ils aident à calculer vite : 7 + 8, c’est le double de 7 plus 1."),
           ("Quel est le lien entre double et moitié ?", "Si 12 est le double de 6, alors 6 est la moitié de 12.")]
    unit(lv, R, "doubles-et-moities", "N",
         ("Connaître les doubles des nombres de 1 à 10 et de 20, 30, 40, 50 ; connaître les moitiés des nombres pairs jusqu’à 20 et de 40, 60, 80, 100 ; utiliser les presque-doubles" if lv == 0 else
          "Connaître les doubles et les moitiés de nombres d’usage courant (jusqu’à 100, multiples de 25, centaines entières) ; utiliser double et moitié pour calculer"),
         "Doubles et moitiés", "Doubles et moitiés",
         ("Fiches de maths CP sur les doubles et les moitiés : doubles jusqu’à 10 et de 20 à 50, moitiés, presque-doubles et problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 sur les doubles et les moitiés : jusqu’à 100, multiples de 25, centaines, double du double et problèmes. 100 exercices corrigés."),
         "Double de 6 = 12 ; moitié de 12 = 6.", "Double et moitié vont ensemble.", body, faq, sets, 8)


if __name__ == "__main__":
    build(0)
