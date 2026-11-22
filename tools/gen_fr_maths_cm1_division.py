# -*- coding: utf-8 -*-
"""
France Maths CM1 : La division euclidienne posée — CM2 (build(2)) : La division décimale
  python3 tools/gen_fr_maths_cm1_division.py
CM1 : division euclidienne d’un entier par un nombre à un chiffre (quotient et reste), nombre de chiffres du quotient,
vérification a = b × q + r, problèmes. CM2 : en plus, division décimale d’un entier ou d’un décimal par un nombre à un chiffre.
Erreurs : oublier un 0 au quotient (4 236 ÷ 4 → 159), reste plus grand que le diviseur, oublier la virgule au quotient.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, dz, FOIS, DIV

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52107 + 100 * lv)
    K = Kids(R)


def drop0(q):
    s = str(q)
    return int(s.replace("0", "")) if "0" in s[1:] and s.replace("0", "") else None


def qr(q, r):
    return "q = %s, r = %s" % (num(q), num(r))


def s1():
    d = R.randint(3, 9)
    a = R.randint(100, 999)
    q, r = divmod(a, d)
    if r == 0:
        return None
    return mcq("Calcule %s %s %d : quel est le quotient q et le reste r ?" % (num(a), DIV, d), qr(q, r), [qr(q - 1, r + d), qr(q + 1, 0), qr(q, (r + 1) % d or d - 1) if (r + 1) % d != r else qr(q + 10, r)],
               "%d %s %s = %s et %s − %s = %d. Le reste %d est plus petit que %d : <b>%s</b>." % (d, FOIS, num(q), num(d * q), num(a), num(d * q), r, r, d, qr(q, r)))


def s2():
    d = R.randint(2, 9)
    q = R.randint(102, 2499)
    if R.random() < 0.5:
        q = int(str(q)[:1] + "0" + str(q)[2:]) if len(str(q)) > 2 else q
    r = R.choice([0, 0, R.randint(1, d - 1)])
    a = d * q + r
    if a > 9999:
        return None
    w = [drop0(q), q + 10, q - 1, q * 10 if q * 10 * d <= a * 10 else None]
    return mcq("Calcule en posant la division : %s %s %d (quotient)" % (num(a), DIV, d), num(q), [num(x) for x in w if x and x != q],
               "%s = %d %s %s + %d. N’oublie pas les 0 au quotient quand un chiffre du dividende est plus petit que %d. Quotient : <b>%s</b>." % (num(a), d, FOIS, num(q), r, d, num(q)))


def s3():
    k = R.choice(["nb", "verif", "nb"])
    d = R.randint(3, 9)
    a = R.randint(200, 9999)
    q, r = divmod(a, d)
    if k == "nb":
        n = len(str(q))
        return mcq("Combien de chiffres aura le quotient de %s %s %d ?" % (num(a), DIV, d), str(n), [str(n + 1), str(n - 1) if n > 1 else "5", str(len(str(a)))],
                   "%d %s %s ≤ %s &lt; %d %s %s : le quotient est entre %s et %s, il a <b>%d</b> chiffres." % (d, FOIS, num(10 ** (n - 1)), num(a), d, FOIS, num(10 ** n), num(10 ** (n - 1)), num(10 ** n), n))
    if r == 0:
        return None
    right = "%s = %d %s %s + %d" % (num(a), d, FOIS, num(q), r)
    return mcq("Quelle égalité correspond à la division de %s par %d ?" % (num(a), d), right,
               ["%s = %d %s %s + %d" % (num(a), d, FOIS, num(q - 1), r + d), "%s = %d %s %s − %d" % (num(a), d, FOIS, num(q + 1), d - r), "%s = %d %s %d + %s" % (num(a), d, FOIS, r, num(q))],
               "Dans a = b %s q + r, le reste r doit être plus petit que b : <b>%s</b>." % (FOIS, right))


def s4_dec():
    d = R.choice([2, 4, 5, 8])
    a = R.randint(11, 499)
    if a % d == 0:
        return None
    # quotient décimal exact ou approché au centième
    for k in (1, 2, 3):
        if (a * 10 ** k) % d == 0:
            break
    else:
        k = 2
    qd = a * 10 ** k // d
    exact = (a * 10 ** k) % d == 0
    q = dz(qd, k)
    e = "On pose %s %s %d ; quand il reste quelque chose, on écrit la virgule au quotient et on continue avec des 0 : %s,0… → <b>%s</b>%s." % (num(a), DIV, d, num(a), q, "" if exact else " (valeur approchée au centième)")
    if not exact:
        return None
    return mcq("Calcule %s %s %d (division décimale)" % (num(a), DIV, d), q,
               ["%s reste %d" % (num(a // d), a % d) if not exact else dz(qd, k + 1), dz(qd, k - 1) if k > 1 else num(qd), dz(qd + 10 ** (k - 1), k)], e)


def s4_decdec():
    d = R.randint(2, 9)
    q = R.randint(11, 999)
    k = R.choice([1, 2])
    a = q * d
    if q % 10 == 0:
        return None
    return mcq("Calcule %s %s %d" % (dz(a, k), DIV, d), dz(q, k), [dz(q, k + 1), dz(q * 10, k), dz(q + 10 ** (k - 1), k)],
               "On divise comme pour des entiers et on place la virgule au quotient quand on « descend » le chiffre des dixièmes : %d %s %s = %s. Résultat : <b>%s</b>." % (d, FOIS, dz(q, k), dz(a, k), dz(q, k)))


def s4():
    if L == 2:
        return s4_dec() if R.random() < 0.5 else s4_decdec()
    d = R.randint(3, 9)
    a = R.randint(21, 98) * 100 + R.randint(1, 99)
    e = round(a / d, -2 if a / d > 300 else -1)
    return mcq("Quel est le meilleur ordre de grandeur de %s %s %d ?" % (num(a), DIV, d), num(int(e)), [num(int(e) * 10), num(int(e) // 10), num(a - d)],
               "On cherche un multiple de %d proche de %s : le quotient est environ <b>%s</b> (exactement %s reste %d)." % (d, num(a), num(int(e)), num(a // d), a % d))


def s5():
    p = K.next()
    k = R.choice(["boites", "equipes", "jours"] + (["prix", "ruban"] if L == 2 else ["reste"]))
    if k == "boites":
        d = R.choice([6, 8, 9, 4])
        a = R.randint(150, 990)
        if a % d == 0:
            return None
        q = a // d + 1
        return mcq("Une usine range %d œufs dans des boîtes de %d. Combien de boîtes faut-il pour tous les œufs ?" % (a, d) if d in (6, 4) else
                   "On range %d livres dans des cartons de %d. Combien de cartons faut-il ?" % (a, d), num(q), [num(q - 1), num(a % d), num(q + 1)],
                   "%d %s %d = %d reste %d : il faut une boîte de plus pour le reste, soit <b>%d</b>." % (a, DIV, d, a // d, a % d, q))
    if k == "equipes":
        d = R.randint(3, 8)
        a = d * R.randint(15, 60)
        return mcq("%d élèves se répartissent en %d équipes égales. Combien d’élèves par équipe ?" % (a, d), num(a // d), [num(a - d), num(a // d + 10), num(drop0(a // d) or a // d + 1)],
                   "%d %s %d = <b>%d</b>." % (a, DIV, d, a // d))
    if k == "jours":
        a = R.randint(30, 400)
        if a % 7 == 0:
            return None
        return mcq("Combien de semaines complètes y a-t-il dans %d jours, et combien de jours restent ?" % a, "%d semaines et %s" % (a // 7, "1 jour" if a % 7 == 1 else "%d jours" % (a % 7)),
                   ["%d semaines et %d jours" % (a // 7 - 1, a % 7 + 7), "%d semaines et %d jours" % (a // 7, 7 - a % 7) if 7 - a % 7 != a % 7 else "%d semaines" % (a // 7 + 1), "%d semaines et %d jours" % (a // 10, a % 10)],
                   "%d %s 7 = %d reste %d : <b>%d semaines et %s</b>." % (a, DIV, a // 7, a % 7, a // 7, "1 jour" if a % 7 == 1 else "%d jours" % (a % 7)))
    if k == "reste":
        d = R.randint(3, 9)
        a = R.randint(100, 999)
        if a % d == 0:
            return None
        return mcq("%s partage %d perles entre %d colliers identiques, le plus possible. Combien de perles restent ?" % (p[0], a, d), str(a % d), [str(a // d), str(d - a % d) if d - a % d != a % d else str(d), str(a % 10)],
                   "%d %s %d = %d reste %d : il reste <b>%d</b> perles." % (a, DIV, d, a // d, a % d, a % d))
    if k == "prix":
        d = R.randint(3, 8)
        c = R.randint(105, 999)
        if c % 10 == 0:
            return None
        t = c * d
        return mcq("%d cahiers identiques coûtent %s €. Combien coûte un cahier ?" % (d, dz(t, 2, True)), dz(c, 2, True) + " €", [dz(c * 10, 2, True) + " €", dz(c + 100, 2, True) + " €", dz(t - d * 100, 2, True) + " €"],
                   "%s %s %d = <b>%s €</b>." % (dz(t, 2, True), DIV, d, dz(c, 2, True)))
    d = R.choice([4, 5, 8, 2])
    m = R.randint(3, 25)
    if m % d == 0:
        return None
    return mcq("On coupe un ruban de %d m en %d morceaux égaux. Quelle est la longueur d’un morceau ?" % (m, d), dz(m * 1000 // d, 3) + " m", ["%d m reste %d" % (m // d, m % d), dz(m * 1000 // d, 2) + " m", dz(m * 1000 // d + 100, 3) + " m"],
               "%d %s %d = <b>%s m</b> (on continue la division après la virgule)." % (m, DIV, d, dz(m * 1000 // d, 3)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Quotient et reste", mix(R, seen, [(s1, 20)])),
        ("Poser la division", mix(R, seen, [(s2, 20)])),
        ("Vérifier et prévoir le quotient", mix(R, seen, [(s3, 20)])),
        ("Ordre de grandeur" if lv == 1 else "La division décimale", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Diviser 347 par 6, c’est chercher combien de fois 6 dans 347 : le <b>quotient</b> q, et ce qui reste : le <b>reste</b> r.",
         "On vérifie : 347 = 6 %s 57 + 5. Le reste est toujours <b>plus petit que le diviseur</b>." % FOIS,
         "Pour prévoir le nombre de chiffres du quotient : 6 %s 10 ≤ 347 &lt; 6 %s 100, donc le quotient a 2 chiffres." % (FOIS, FOIS)] +
        (["<b>Division décimale</b> : quand il reste quelque chose, on écrit une virgule au quotient et on continue avec des 0 : 47 ÷ 4 = 11,75."] if lv == 2 else []),
        [example("4 236 %s 4" % DIV, ["4 ÷ 4 = 1 ; 2 ÷ 4 = 0 (on écrit 0)", "23 ÷ 4 = 5 reste 3 ; 36 ÷ 4 = 9"], "1 059")] +
        ([example("25,8 %s 6" % DIV, ["25 ÷ 6 = 4 reste 1 ; on écrit la virgule", "18 ÷ 6 = 3"], "4,3")] if lv == 2 else []),
        [["Oublier un 0 au quotient : 4 236 %s 4 = 159" % DIV, "Quand on ne peut pas diviser, on écrit 0 : 1 059."],
         ["Un reste plus grand que le diviseur", "Si le reste est ≥ au diviseur, le quotient est trop petit."],
         ["Oublier qu’il faut une boîte de plus pour le reste", "50 œufs, boîtes de 6 : 8 boîtes pleines + 1 = 9 boîtes."]])
    faq = [("Comment vérifier une division ?", "On calcule diviseur %s quotient + reste : on doit retrouver le dividende." % FOIS),
           ("Quand s’arrête-t-on dans une division décimale ?", "Quand le reste est 0, ou quand on a assez de chiffres après la virgule (par exemple au centième).")]
    unit(lv, R, "division-euclidienne" if lv == 1 else "division-decimale", "N",
         ("Poser et effectuer des divisions euclidiennes dont le diviseur a un chiffre ; estimer le résultat ; vérifier a = b × q + r" if lv == 1 else
          "Poser et effectuer une division décimale d’un nombre entier ou d’un nombre décimal par un nombre à un chiffre ; estimer le résultat ; vérifier"),
         "La division euclidienne posée" if lv == 1 else "La division décimale", "Division euclidienne" if lv == 1 else "Division décimale",
         ("Fiches de maths CM1 sur la division euclidienne posée : quotient et reste, zéros au quotient, vérification, ordre de grandeur et problèmes. 100 exercices corrigés." if lv == 1 else
          "Fiches de maths CM2 sur la division : division euclidienne et division décimale d’un entier ou d’un décimal par un nombre à un chiffre, problèmes. 100 exercices corrigés."),
         "347 = 6 × 57 + 5 : quotient 57, reste 5.", "Le reste est toujours plus petit que le diviseur.",
         body, faq, sets, 7)


if __name__ == "__main__":
    build(1)
