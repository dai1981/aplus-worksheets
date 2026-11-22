# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les fractions décimales (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_fractions_decimales.py
CM1 : dixièmes et centièmes. CM2 : jusqu’aux millièmes. Relations entre unités, dixièmes, centièmes (millièmes) ;
fraction décimale ↔ écriture à virgule ; décomposer (entier + fractions décimales) ; demi-droite graduée ; comparer.
Erreurs : 7/100 = 0,7, 3/10 &lt; 25/100 « car 3 &lt; 25 », 2 + 5/100 = 2,5.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, fr, dz, droite_dec

R = K = None
L = 1
UN = {1: "dixième", 2: "centième", 3: "millième"}


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52111 + 100 * lv)
    K = Kids(R)


def kmax():
    return 2 if L == 1 else 3


def s1():
    k = R.choice(["u", "dc", "mix"])
    if k == "u":
        a = R.randint(1, kmax())
        b = R.randint(0, a - 1)
        n = R.randint(2, 9)
        nm_b = "unités" if b == 0 else UN[b] + "s"
        return mcq("Complète : %d %s = … %ss" % (n, nm_b, UN[a]), num(n * 10 ** (a - b)), [num(n * 10 ** (a - b + 1)), num(n * 10 ** (a - b - 1)) if a - b > 1 else str(n), num(n + 10 ** (a - b))],
                   "1 %s = %s %ss, donc %d %s = <b>%s</b> %ss." % ("unité" if b == 0 else UN[b], num(10 ** (a - b)), UN[a], n, nm_b, num(n * 10 ** (a - b)), UN[a]))
    if k == "dc":
        n = R.randint(11, 99) if kmax() == 2 or R.random() < 0.5 else R.randint(101, 999)
        top = 2 if n < 100 else 3
        right = "%d %ss et %d %s%s" % (n // 10, UN[top - 1], n % 10, UN[top], "s" if n % 10 > 1 else "")
        if n % 10 == 0:
            return None
        return mcq("%s %ss, c’est…" % (num(n), UN[top]), right, ["%d %ss et %d %s%s" % (n % 10, UN[top - 1], n // 10, UN[top], "s" if n // 10 > 1 else ""), "%d %ss et %d %s%s" % (n // 10, UN[top - 2] if top > 2 else "unité", n % 10, UN[top], "s" if n % 10 > 1 else ""),
                                                   "%d unités et %d %s%s" % (n // 10, n % 10, UN[top], "s" if n % 10 > 1 else "")],
                   "10 %ss = 1 %s : <b>%s</b>." % (UN[top], UN[top - 1], right))
    a = R.randint(1, 9)
    b = R.randint(1, 9)
    k2 = kmax()
    r = a * 10 ** (k2 - 1) + b
    return mcq("%d %ss et %d %s%s, combien de %ss en tout ?" % (a, UN[k2 - 1], b, UN[k2], "s" if b > 1 else "", UN[k2]), num(r), [num(a + b), num(a * 100 + b) if k2 == 2 else num(a * 10 + b), num(b * 10 + a)],
               "1 %s = 10 %ss : %d %s 10 + %d = <b>%d</b>." % (UN[k2 - 1], UN[k2], a, "×", b, r))


def s2():
    k = R.randint(1, kmax())
    n = R.randint(1, 10 ** (k + 1) - 1)
    if n % 10 == 0:
        return None
    if R.random() < 0.5:
        return mcq("Écris %s avec une virgule." % fr(n, 10 ** k), dz(n, k), [dz(n, k - 1) if k > 1 else num(n), dz(n, k + 1), "%d,%d" % (n, 10 ** k)],
                   "%s : le dernier chiffre est au rang des %ss : <b>%s</b>." % (fr(n, 10 ** k), UN[k], dz(n, k)))
    return mcq("Écris %s sous la forme d’une fraction décimale." % dz(n, k), fr(n, 10 ** k), [fr(n, 10 ** (k + 1)), fr(n, 10 ** (k - 1)) if k > 1 else fr(n, 1), fr(n // 10 if n >= 10 else n, 10 ** k) if n >= 10 else fr(n * 10, 10 ** k)],
               "%s a %d chiffre%s après la virgule : %s. Réponse : <b>%s</b>." % (dz(n, k), k, "s" if k > 1 else "", UN[k] + "s", fr(n, 10 ** k)))


def s3():
    k = kmax()
    e = R.randint(1, 19)
    ds = [R.randint(0, 9) for _ in range(k)]
    if ds[-1] == 0 or (k == 3 and ds[1] == 0 and ds[0] == 0):
        return None
    n = e * 10 ** k + sum(d * 10 ** (k - 1 - i) for i, d in enumerate(ds))
    terms = [str(e)] + [fr(d, 10 ** (i + 1)) for i, d in enumerate(ds) if d]
    if R.random() < 0.5:
        wrong_skip = str(e) + "," + "".join(str(d) for d in ds if d)
        return mcq("Quel nombre est égal à %s ?" % " + ".join(terms), dz(n, k), [wrong_skip if wrong_skip != dz(n, k) else dz(n, k + 1), dz(n, k - 1), "%d,%s" % (e, "".join(str(d) for d in ds[::-1]))],
                   "Chaque fraction donne un chiffre à son rang ; les rangs vides valent 0 : <b>%s</b>." % dz(n, k))
    right = " + ".join(terms)
    return mcq("Décompose %s (écriture à virgule) : %s = …" % (fr(n, 10 ** k), fr(n, 10 ** k)), right,
               [" + ".join([str(e)] + [fr(d, 10) for d in ds if d]), " + ".join([str(e)] + [fr(d, 10 ** (k - i)) for i, d in enumerate(ds) if d]), " + ".join([str(e + 1)] + terms[1:])],
               "%s = %s = <b>%s</b>." % (fr(n, 10 ** k), dz(n, k), right))


def s4():
    k = R.randint(1, kmax())
    if k == 1:
        lo = R.randint(0, 8) * 10
        hi = lo + 20
        step = 1
        v = lo + R.randint(1, 19)
        if v % 10 == 0:
            return None
        pic = droite_dec(lo, hi, step, [(v, "A")], k=1, every=10)
    else:
        lo = R.randint(0, 99) * 10 ** (k - 1)
        hi = lo + 10 ** (k - 1)
        step = 10 ** (k - 2) if k == 3 else 1
        v = lo + R.randint(1, 9) * step
        pic = droite_dec(lo, hi, step, [(v, "A")], k=k, every=10 ** (k - 1))
    if R.random() < 0.5:
        return mcq("<div class='qfig'>%s</div>Quelle fraction décimale repère le point A ?" % pic, fr(v, 10 ** k), [fr(v, 10 ** (k + 1)), fr(v + step, 10 ** k), fr(v - step, 10 ** k) if v - step > 0 else fr(v + 2 * step, 10 ** k)],
                   "Chaque petite graduation vaut %s. A = <b>%s</b> = %s." % (fr(step, 10 ** k), fr(v, 10 ** k), dz(v, k)))
    return mcq("<div class='qfig'>%s</div>Quel nombre décimal repère le point A ?" % pic, dz(v, k), [dz(v, k + 1), dz(v + step, k), dz(v - step, k) if v - step > lo else dz(v + 2 * step, k)],
               "Chaque petite graduation vaut %s. A = <b>%s</b>." % (dz(step, k), dz(v, k)))


def s5():
    p = K.next()
    k = R.choice(["cmp", "cmp", "egal", "euro", "metre"])
    if k == "cmp":
        a = R.randint(1, 9)
        b = R.randint(11, 99)
        if a * 10 == b:
            return None
        va, vb = a * 10, b
        big = fr(a, 10) if va > vb else fr(b, 100)
        return mcq("Quelle est la plus grande fraction : %s ou %s ?" % (fr(a, 10), fr(b, 100)), big, [fr(b, 100) if big == fr(a, 10) else fr(a, 10), "elles sont égales", "on ne peut pas savoir"],
                   "%s = %s. On compare %d et %d centièmes : <b>%s</b>." % (fr(a, 10), fr(a * 10, 100), a * 10, b, big))
    if k == "egal":
        a = R.randint(1, 9)
        return mcq("Quelle fraction est égale à %s ?" % fr(a, 10), fr(a * 10, 100), [fr(a, 100), fr(a + 10, 100), fr(a * 10, 10)],
                   "1 dixième = 10 centièmes : %s = <b>%s</b>." % (fr(a, 10), fr(a * 10, 100)))
    if k == "euro":
        c = R.randint(5, 95)
        return mcq("%d centimes, quelle fraction d’un euro est-ce ?" % c, fr(c, 100), [fr(c, 10), fr(100, c), fr(c, 1000)], "1 € = 100 centimes : %d centimes = <b>%s</b> d’euro = %s €." % (c, fr(c, 100), dz(c, 2, True)))
    if L == 2 and R.random() < 0.6:
        mm = R.randint(1, 999)
        if mm % 10 == 0:
            return None
        return mcq("%s mesure un objet de %d mm. Quelle fraction du mètre est-ce ?" % (p[0], mm), fr(mm, 1000), [fr(mm, 100), fr(mm, 10), fr(1000, mm)],
                   "1 m = 1 000 mm : %d mm = <b>%s</b> m = %s m." % (mm, fr(mm, 1000), dz(mm, 3)))
    cm = R.randint(1, 99)
    return mcq("Un crayon mesure %d cm. Quelle fraction du mètre est-ce ?" % cm, fr(cm, 100), [fr(cm, 10), fr(cm, 1000), fr(100, cm)],
               "1 m = 100 cm : %d cm = <b>%s</b> m = %s m." % (cm, fr(cm, 100), dz(cm, 2)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Dixièmes, centièmes" + ("" if lv == 1 else ", millièmes"), mix(R, seen, [(s1, 20)])),
        ("Fraction décimale et écriture à virgule", mix(R, seen, [(s2, 20)])),
        ("Décomposer", mix(R, seen, [(s3, 20)])),
        ("La demi-droite graduée", mix(R, seen, [(s4, 20)])),
        ("Comparer et problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Une <b>fraction décimale</b> a pour dénominateur 10, 100%s." % ("" if lv == 1 else " ou 1 000"),
         "1 unité = 10 dixièmes = 100 centièmes%s." % ("" if lv == 1 else " = 1 000 millièmes") + " 1 dixième = 10 centièmes.",
         "%s = 3 + %s + %s = 3,47 : chaque chiffre après la virgule a son rang (dixièmes, centièmes%s)." % (fr(347, 100), fr(4, 10), fr(7, 100), "" if lv == 1 else ", millièmes")],
        [example("%s avec une virgule" % fr(7, 100), ["7 centièmes", "0 unité, 0 dixième, 7 centièmes"], "0,07")],
        [["%s = 0,7" % fr(7, 100), "0,7 = 7 dixièmes. 7 centièmes s’écrit 0,07."],
         ["%s &lt; %s car 3 &lt; 25" % (fr(3, 10), fr(25, 100)), "%s = %s : c’est plus grand que %s." % (fr(3, 10), fr(30, 100), fr(25, 100))],
         ["2 + %s = 2,5" % fr(5, 100), "5 centièmes : 2,05."]])
    faq = [("Pourquoi apprendre les fractions décimales ?", "Elles expliquent les nombres à virgule : 3,47 = 3 + 4 dixièmes + 7 centièmes."),
           ("Que vaut un centime ?", "Un centième d’euro : %s €." % fr(1, 100))]
    unit(lv, R, "fractions-decimales", "N",
         "Interpréter, représenter, lire et écrire des fractions décimales ; connaître les relations entre unités, dixièmes, centièmes%s ; passer d’une fraction décimale à une écriture à virgule et inversement ; les placer sur une demi-droite graduée ; les comparer" % ("" if lv == 1 else " et millièmes"),
         "Les fractions décimales", "Fractions décimales",
         "Fiches de maths %s sur les fractions décimales : dixièmes, centièmes%s, écriture à virgule, décomposition, demi-droite graduée et comparaison. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", millièmes"),
         "347/100 = 3 + 4/10 + 7/100 = 3,47.", "1 unité = 10 dixièmes = 100 centièmes.",
         body, faq, sets, 11)


if __name__ == "__main__":
    build(1)
