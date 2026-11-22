# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Le calcul mental (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_calcul_mental.py
CM1 : + et − 9, 19, 29…, × 10/100/1 000, × et ÷ 10 d’un décimal, × 4, × 8, × 5, dizaines et centaines, distributivité,
fractions usuelles et écriture décimale. CM2 : + et − 99, × et ÷ 10/100/1 000 d’un décimal, double et moitié d’un décimal,
÷ 4, ÷ 8, × 5 et × 50 d’un décimal, sommes de décimaux.
Erreurs : + 9 → + 10 sans retirer 1, « ajouter un 0 » à un décimal (2,5 × 10 = 2,50), confondre double et moitié.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, dz, fr

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52104 + 100 * lv)
    K = Kids(R)


def s1():
    k = R.choice([9, 19, 29, 39, 8, 18, 28, 38] if L == 1 else [9, 19, 29, 39, 49, 59, 99, 98, 69, 79, 89])
    a = R.randint(45, 900 if L == 1 else 9000)
    if R.random() < 0.5:
        r = a + k
        up = (k + 1) if k % 10 == 9 else (k + 2)
        return mcq("Calcule mentalement : %s + %d" % (num(a), k), num(r), [num(a + up), num(r - 2), num(a + k - 10)],
                   "On ajoute %d puis on retire %d : %s + %d − %d = <b>%s</b>." % (up, up - k, num(a), up, up - k, num(r)))
    if a <= k:
        return None
    r = a - k
    up = (k + 1) if k % 10 == 9 else (k + 2)
    return mcq("Calcule mentalement : %s − %d" % (num(a), k), num(r), [num(a - up), num(r + 2), num(a - k + 10)],
               "On enlève %d puis on rajoute %d : %s − %d + %d = <b>%s</b>." % (up, up - k, num(a), up, up - k, num(r)))


def s2():
    k = R.choice(["int", "decx", "decd"] if L == 1 else ["decx", "decd", "decx", "decd", "int"])
    p = R.choice([10, 100, 1000]) if L == 2 or k == "int" else 10
    if k == "int":
        a = R.randint(3, 999)
        r = a * p
        return mcq("Calcule : %s %s %s" % (num(a), FOIS, num(p)), num(r), [num(a * p // 10) if p > 10 else num(a + p), num(r * 10), num(a + p)],
                   "Chaque chiffre prend une valeur %s fois plus grande : <b>%s</b>." % (num(p), num(r)))
    kk = 2 if L == 2 else 1
    a = R.randint(11, 999) if kk == 1 else R.randint(101, 9999)
    if a % 10 == 0:
        return None
    if k == "decx":
        r = a * p
        return mcq("Calcule : %s %s %s" % (dz(a, kk), FOIS, num(p)), dz(r, kk), [dz(a, kk) + "0", dz(r // 10, kk) if p > 10 else dz(a * 100, kk), dz(r * 10, kk)],
                   "Multiplier par %s : chaque chiffre prend une valeur %s fois plus grande (la virgule « se déplace » de %d rang%s vers la droite) : <b>%s</b>." % (num(p), num(p), len(str(p)) - 1, "s" if p > 10 else "", dz(r, kk)))
    sh = len(str(p)) - 1
    r = dz(a, kk + sh)
    return mcq("Calcule : %s %s %s" % (dz(a, kk), DIV, num(p)), r, [dz(a, kk + sh - 1) if sh > 1 else dz(a * 10, kk), dz(a, kk + sh + 1), dz(a * p, kk)],
               "Diviser par %s : chaque chiffre prend une valeur %s fois plus petite : <b>%s</b>." % (num(p), num(p), r))


def s3():
    k = R.choice(["x4", "x8", "x5", "dc"] + (["x50d", "x5d", "div4", "div8"] if L == 2 else []))
    if k == "x4":
        a = R.randint(12, 99)
        return mcq("Calcule mentalement : %d %s 4" % (a, FOIS), num(a * 4), [num(a * 2), num(a * 4 + 4), num(a * 4 - 10)], "%d %s 4, c’est le double du double : %d → %d → <b>%d</b>." % (a, FOIS, a, 2 * a, 4 * a))
    if k == "x8":
        a = R.randint(12, 60)
        return mcq("Calcule mentalement : %d %s 8" % (a, FOIS), num(a * 8), [num(a * 4), num(a * 8 + 8), num(a * 6)], "%d %s 8 : on double trois fois : %d → %d → %d → <b>%d</b>." % (a, FOIS, a, 2 * a, 4 * a, 8 * a))
    if k == "x5":
        a = R.randint(12, 98) * 2
        return mcq("Calcule mentalement : %d %s 5" % (a, FOIS), num(a * 5), [num(a * 10), num(a // 2), num(a * 5 + 5)], "%s 5, c’est %s 10 puis la moitié : %s ÷ 2 = <b>%s</b>." % (FOIS, FOIS, num(a * 10), num(a * 5)))
    if k == "dc":
        a = R.randint(2, 9)
        b = R.randint(2, 9) * R.choice([10, 100] + ([1000] if L == 2 else []))
        if L == 2 and R.random() < 0.5:
            a = a * R.choice([10, 100])
        r = a * b
        return mcq("Calcule mentalement : %s %s %s" % (num(a), FOIS, num(b)), num(r), [num(r // 10), num(r * 10), num(a * b // (b // (b // 10 if b >= 100 else 1)) if b >= 100 else a + b)],
                   "On multiplie les chiffres, puis on ajoute les zéros : <b>%s</b>." % num(r))
    if k == "x5d":
        a = R.randint(11, 99)
        return mcq("Calcule mentalement : %s %s 5" % (dz(a, 1), FOIS), dz(a * 5, 1), [dz(a * 10, 1), dz(a * 5, 2), dz(a * 5 + 10, 1)],
                   "%s 5 = %s 10 puis la moitié : %s ÷ 2 = <b>%s</b>." % (FOIS, FOIS, dz(a * 10, 1), dz(a * 5, 1)))
    if k == "x50d":
        a = R.randint(11, 99)
        return mcq("Calcule mentalement : %s %s 50" % (dz(a, 1), FOIS), dz(a * 50, 1), [dz(a * 5, 1), dz(a * 500, 1), dz(a * 50, 2)],
                   "%s 50 = %s 100 puis la moitié : %s ÷ 2 = <b>%s</b>." % (FOIS, FOIS, dz(a * 100, 1), dz(a * 50, 1)))
    d = 4 if k == "div4" else 8
    q = R.randint(12, 99)
    a = d * q
    return mcq("Calcule mentalement : %s %s %d" % (num(a), DIV, d), num(q), [num(a // 2), num(q * 2), num(q + d)],
               "%s %d, c’est prendre la moitié %s : %s → <b>%s</b>." % (DIV, d, "de la moitié" if d == 4 else "trois fois", " → ".join(num(a // 2 ** i) for i in range(1, 3 if d == 4 else 4)[:-1]) or num(a // 2), num(q)))


def s4():
    k = R.choice(["dist", "dist", "frac"] + (["double", "moitie", "somme"] if L == 2 else ["entdec"]))
    if k == "dist":
        a, b = R.choice([11, 12, 13, 15, 21, 19, 18, 31, 101, 99]), R.randint(3, 9)
        if a in (19, 18, 99):
            c = a + (20 - a % 10 if a < 90 else 100 - a)
            e = "%d %s %d = %d %s %d − %d %s %d = %d − %d = <b>%d</b>." % (a, FOIS, b, c, FOIS, b, c - a, FOIS, b, c * b, (c - a) * b, a * b)
        else:
            t = a // 10 * 10
            e = "%d %s %d = %d %s %d + %d %s %d = %d + %d = <b>%d</b>." % (a, FOIS, b, t, FOIS, b, a - t, FOIS, b, t * b, (a - t) * b, a * b)
        return mcq("Calcule mentalement : %d %s %d" % (a, FOIS, b), num(a * b), [num(a // 10 * 10 * b + a % 10), num(a * b + b), num((a // 10) * b * 10 + (a % 10) * b + 10)], e)
    if k == "frac":
        f = R.choice([(1, 2, 5, 1), (1, 4, 25, 2), (3, 4, 75, 2), (1, 10, 1, 1), (1, 5, 2, 1), (3, 10, 3, 1), (1, 100, 1, 2), (7, 10, 7, 1), (5, 100, 5, 2)] + ([(1, 1000, 1, 3), (2, 5, 4, 1), (1, 8, 125, 3)] if L == 2 else []))
        a, b, v, kk = f
        return mcq("Quelle est l’écriture décimale de %s ?" % fr(a, b), dz(v, kk), [dz(v, kk + 1) if kk < 3 else dz(v * 10, kk), "%d,%d" % (a, b), dz(v * 10, kk) if dz(v * 10, kk) != dz(v, kk) else "1,%d" % b],
                   "%s = <b>%s</b>." % (fr(a, b), dz(v, kk)))
    if k == "entdec":
        a = R.randint(101, 999)
        n = R.randint(1, 9)
        r = a + n * 10
        if a % 10 == 0:
            return None
        return mcq("Calcule : %s + %d" % (dz(a, 1), n), dz(r, 1), [dz(a + n, 1), dz(a + n * 100, 1), dz(r + 1, 1)],
                   "On ajoute %d aux unités, les dixièmes ne changent pas : <b>%s</b>." % (n, dz(r, 1)))
    if k == "double":
        a = R.randint(11, 99)
        return mcq("Quel est le double de %s ?" % dz(a, 1), dz(2 * a, 1), [dz(a * 2 // 10 * 10 + (a % 10) * 2 % 10, 1) if (a % 10) * 2 >= 10 else dz(2 * a + 10, 1), dz(a * 5, 2), dz(2 * a, 2)],
                   "%s + %s = <b>%s</b>." % (dz(a, 1), dz(a, 1), dz(2 * a, 1)))
    if k == "moitie":
        a = R.choice(list(range(3, 16, 2)) + [21, 25, 31, 45, 9])
        return mcq("Quelle est la moitié de %d ?" % a, dz(a * 5, 1), [dz(a * 5, 2), num(a // 2), dz(a * 5 + 10, 1)],
                   "%d = %d + 1 ; la moitié de %d est %d, celle de 1 est 0,5 : <b>%s</b>." % (a, a - 1, a - 1, (a - 1) // 2, dz(a * 5, 1)))
    a, b = R.randint(11, 98), R.randint(11, 98)
    if a % 10 == 0 or b % 10 == 0:
        return None
    return mcq("Calcule mentalement : %s + %s" % (dz(a, 1), dz(b, 1)), dz(a + b, 1), [dz(a // 10 * 10 + b // 10 * 10 + (a % 10 + b % 10) % 10, 1), dz(a + b, 2), dz(a + b + 10, 1)],
               "Unités : %d + %d ; dixièmes : %d + %d = %d. Résultat : <b>%s</b>." % (a // 10, b // 10, a % 10, b % 10, a % 10 + b % 10, dz(a + b, 1)))


def s5():
    p = K.next()
    k = R.choice(["boites", "prix", "pages", "pile", "partage"])
    if k == "boites":
        n, c = R.randint(12, 49), R.choice([4, 8, 5, 25])
        return mcq("Un magasin reçoit %d cartons de %d bouteilles. Combien de bouteilles ?" % (n, c), num(n * c), [num(n + c), num(n * c + c), num(n * (c - 1))], "%d %s %d = <b>%s</b>." % (n, FOIS, c, num(n * c)))
    if k == "prix":
        a = R.randint(11, 99) if L == 2 else R.randint(2, 9) * 10 + 9
        n = R.choice([10, 100] if L == 2 else [10])
        pr = dz(a, 1) + " €" if L == 2 else "%d €" % a
        r = dz(a * n, 1) + " €" if L == 2 else "%s €" % num(a * n)
        return mcq("Un livre coûte %s. Combien coûtent %d livres ?" % (pr, n), r, [(dz(a, 1) + "0 €") if L == 2 else "%d €" % (a + n), (dz(a * n * 10, 1) + " €") if L == 2 else "%s €" % num(a * 100), (dz(a * n, 2) + " €") if L == 2 else "%s €" % num(a * n + n)],
                   "On multiplie par %d : <b>%s</b>." % (n, r))
    if k == "pages":
        a, b = R.randint(120, 480), R.choice([19, 29, 39, 99] if L == 2 else [19, 29, 39])
        return mcq("%s a lu %d pages. %s lit encore %d pages. Combien de pages a-t-%s lues en tout ?" % (p[0], a, p[1].capitalize(), b, p[1]), num(a + b), [num(a + b + 1), num(a + b - 10), num(a + b + 2)],
                   "%d + %d = %d + %d − 1 = <b>%d</b>." % (a, b, a, b + 1, a + b))
    if k == "pile":
        e = R.choice([2, 5, 8, 4]) if L == 1 else R.choice([25, 15, 45])
        n = R.choice([10, 100, 1000])
        if L == 1:
            return mcq("Une feuille mesure %d mm d’épaisseur… non : un livre mesure %d cm d’épaisseur. Quelle est la hauteur d’une pile de %s livres ?" % (e, e, num(n)) if False else
                       "Un livre mesure %d cm d’épaisseur. Quelle est la hauteur d’une pile de %s livres ?" % (e, num(n)), "%s cm" % num(e * n), ["%s cm" % num(e * n // 10), "%s cm" % num(e * n * 10), "%s cm" % num(e + n)],
                       "%d %s %s = <b>%s cm</b>." % (e, FOIS, num(n), num(e * n)))
        return mcq("Un jeton a une épaisseur de %s mm. Quelle est la hauteur d’une pile de %s jetons ?" % (dz(e, 1), num(n)), "%s mm" % dz(e * n, 1), ["%s mm" % (dz(e, 1) + "0" * (len(str(n)) - 1)), "%s mm" % dz(e * n, 2), "%s mm" % dz(e * n * 10, 1)],
                   "%s %s %s = <b>%s mm</b>." % (dz(e, 1), FOIS, num(n), dz(e * n, 1)))
    d = 4 if L == 1 else R.choice([4, 8])
    q = R.randint(12, 60)
    return mcq("%d enfants forment %d équipes égales. Combien d’enfants par équipe ?" % (d * q, d), str(q), [str(d * q // 2), str(q * 2), str(q + 1)],
               "%d %s %d : on prend la moitié %s : <b>%d</b>." % (d * q, DIV, d, "de la moitié" if d == 4 else "trois fois", q))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Ajouter et soustraire 9, 19, 29…" if lv == 1 else "Ajouter et soustraire 9, 19… 99", mix(R, seen, [(s1, 20)])),
        ("Multiplier et diviser par 10, 100, 1 000", mix(R, seen, [(s2, 20)])),
        ("× 4, × 8, × 5 et les zéros" if lv == 1 else "× 5, × 50, ÷ 4, ÷ 8", mix(R, seen, [(s3, 20)])),
        ("Astuces de calcul" if lv == 1 else "Double, moitié et décimaux", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Pour ajouter 9, on ajoute 10 puis on retire 1. Pour ajouter 19, on ajoute 20 puis on retire 1.",
         "Multiplier par 10, 100 ou 1 000 : chaque chiffre prend une valeur 10, 100 ou 1 000 fois plus grande. Pour un décimal, on ne « rajoute pas un zéro » : 2,5 %s 10 = 25." % FOIS,
         "%s 4 : double du double. %s 8 : on double trois fois. %s 5 : %s 10 puis la moitié." % (FOIS, FOIS, FOIS, FOIS),
         "Distributivité : 12 %s 7 = 10 %s 7 + 2 %s 7 = 70 + 14 = 84." % (FOIS, FOIS, FOIS)],
        [example("347 + 29", ["347 + 30 = 377", "377 − 1 = 376"], "376"), example("3,45 %s 100" % FOIS, ["3 unités → 300", "45 centièmes → 45"], "345")],
        [["+ 9 → + 10 en oubliant de retirer 1", "347 + 9 = 347 + 10 − 1 = 356."],
         ["Ajouter un 0 à un décimal : 2,5 %s 10 = 2,50" % FOIS, "2,50 = 2,5. Le bon résultat est 25."],
         ["Confondre %s 4 et %s 2" % (FOIS, FOIS), "%s 4 : on double deux fois." % FOIS]])
    faq = [("Pourquoi faire du calcul mental chaque jour ?", "Pour calculer vite et sans erreur, et vérifier les calculs posés avec un ordre de grandeur."),
           ("Faut-il connaître les tables par cœur ?", "Oui : toutes les astuces de calcul s’appuient sur les tables d’addition et de multiplication.")]
    unit(lv, R, "calcul-mental", "N",
         ("Connaître des faits numériques usuels ; ajouter ou soustraire 8, 9, 18, 19, 28, 29… ; multiplier un entier par 10, 100, 1 000 ; multiplier ou diviser un décimal par 10 ; multiplier par 4, 8 ou 5 ; utiliser la distributivité dans des cas simples" if lv == 1 else
          "Ajouter ou soustraire 8, 9… 99 ; multiplier ou diviser un décimal par 10, 100, 1 000 ; calculer le double et la moitié d’un décimal simple ; diviser un entier par 4 ou 8 ; multiplier un décimal par 5 ou 50 ; ajouter deux décimaux"),
         "Calcul mental : astuces et décimaux", "Calcul mental",
         "Fiches de maths %s de calcul mental : ajouter 9, 19, 29…, multiplier et diviser par 10, 100, 1 000, × 4, × 8, × 5, distributivité%s et problèmes. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", double et moitié des décimaux"),
         "Pour ajouter 9 : + 10, puis − 1.", "2,5 × 10 = 25 : chaque chiffre prend une valeur 10 fois plus grande.",
         body, faq, sets, 4)


if __name__ == "__main__":
    build(1)
