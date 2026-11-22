# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : L’addition posée
  python3 tools/gen_fr_maths_cp_addition_posee.py
CP : 2 ou 3 nombres de 1 ou 2 chiffres (résultat &lt; 100). CE1 : 2 ou 3 nombres jusqu’à 3 chiffres (résultat &lt; 1 000).
Erreurs : oublier la retenue (38 + 25 = 53), mal aligner (34 + 5 = 84), écrire 13 dans une colonne (38 + 25 = 513).
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, posee

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53006 + 100 * lv)
    K = Kids(R)


def top():
    return 100 if L == 0 else 1000


def dg(n):
    return [int(d) for d in str(n).rjust(3, "0")][::-1]


def carries(nums):
    out, c = {}, 0
    for k in range(3):
        s = sum(dg(x)[k] for x in nums) + c
        c = s // 10
        if c and k < 2:
            out[k + 1] = c
    return out


def no_carry(nums):
    return int("".join(str(sum(dg(x)[k] for x in nums) % 10) for k in (2, 1, 0)))


def glued(nums):
    """écrire 13 dans la colonne : 38 + 25 → 513"""
    u = sum(x % 10 for x in nums)
    rest = sum(x // 10 for x in nums)
    return int(str(rest) + str(u)) if u >= 10 else None


def misaligned(nums):
    big = max(nums)
    return sum(x * 10 ** (len(str(big)) - len(str(x))) for x in nums)


def task(nums, need=None):
    r = sum(nums)
    if r >= top() or (need is not None and len(carries(nums)) != need):
        return None
    w = []
    if carries(nums):
        w.append(no_carry(nums))
    if len({len(str(x)) for x in nums}) > 1:
        w.append(misaligned(nums))
    g = glued(nums)
    if g:
        w.append(g)
    w += [r + 10, r - 10, r + 1]
    cs = carries(nums)
    e = "On aligne les unités sous les unités, puis on calcule de droite à gauche."
    if cs:
        e += " Retenue : %s." % ", ".join("%d %s" % (v, {1: "dizaine", 2: "centaine"}[k] + ("s" if v > 1 else "")) for k, v in sorted(cs.items()))
    e += " Résultat : <b>%s</b>." % num(r)
    return mcq(posee([str(x) for x in nums]) + "Calcule : %s" % " + ".join(num(x) for x in nums), num(r), [num(x) for x in w if 0 < x != r], e)


def two(a_lo, a_hi, b_lo, b_hi):
    return [R.randint(a_lo, a_hi), R.randint(b_lo, b_hi)]


def s1():
    return task(two(11, 78, 2, 31) if L == 0 else two(110, 788, 11, 211), 0)


def s2():
    return task(two(15, 69, 5, 29) if L == 0 else two(115, 689, 15, 299), 1)


def s3():
    if L == 0:
        nums = [R.randint(10, 49), R.randint(3, 29), R.randint(2, 19)]
        if not carries(nums):
            return None
        return task(nums)
    if R.random() < 0.5:
        return task(two(156, 589, 156, 389), 2)
    nums = [R.randint(101, 499), R.randint(12, 299), R.randint(5, 99)]
    if not carries(nums):
        return None
    return task(nums)


def s4():
    if L == 0:
        a, b = R.randint(11, 59), R.randint(11, 39)
    else:
        a, b = R.randint(105, 689), R.randint(105, 299)
    r = a + b
    if r >= top():
        return None
    sa = str(a)
    i = R.randrange(len(sa))
    d = sa[i]
    shown = sa[:i] + "□" + sa[i + 1:]
    return mcq("Quel chiffre remplace le □ : %s + %s = %s ?" % (shown, num(b), num(r)), d, [str((int(d) + 1) % 10), str((int(d) + 9) % 10), str((int(d) + 2) % 10)],
               "%s + %s = %s, donc le chiffre caché est <b>%s</b>." % (num(a), num(b), num(r), d))


def s5():
    p = K.next()
    k = R.choice(["billes", "livres", "pas", "eleves", "points"])
    if L == 0:
        a, b = R.randint(12, 58), R.randint(7, 35)
    else:
        a, b = R.randint(120, 580), R.randint(45, 390)
    r = a + b
    if r >= top():
        return None
    w = [num(no_carry([a, b])) if carries([a, b]) else num(r + 10), num(r - 10), num(abs(a - b))]
    if k == "billes":
        return mcq("%s a %s billes. Son frère lui en donne %s. Combien de billes a-t-%s maintenant ?" % (p[0], num(a), num(b), p[1]), num(r), w,
                   "%s + %s = <b>%s</b> billes." % (num(a), num(b), num(r)))
    if k == "livres":
        return mcq("Dans la bibliothèque de la classe, il y a %s albums et %s documentaires. Combien de livres en tout ?" % (num(a), num(b)), num(r), w,
                   "%s + %s = <b>%s</b> livres." % (num(a), num(b), num(r)))
    if k == "pas":
        return mcq("%s fait %s pas le matin et %s pas l’après-midi. Combien de pas en tout ?" % (p[0], num(a), num(b)), num(r), w,
                   "%s + %s = <b>%s</b> pas." % (num(a), num(b), num(r)))
    if k == "eleves":
        return mcq("Une école a %s élèves en maternelle et %s élèves en élémentaire. Combien d’élèves en tout ?" % (num(a), num(b)), num(r), w,
                   "%s + %s = <b>%s</b> élèves." % (num(a), num(b), num(r)))
    return mcq("Au jeu, %s marque %s points, puis %s points. Combien de points a-t-%s ?" % (p[0], num(a), num(b), p[1]), num(r), w,
               "%s + %s = <b>%s</b> points." % (num(a), num(b), num(r)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Sans retenue", mix(R, seen, [(s1, 20)])),
        ("Avec une retenue", mix(R, seen, [(s2, 20)])),
        ("Trois nombres" if lv == 0 else "Plusieurs retenues, trois nombres", mix(R, seen, [(s3, 20)])),
        ("Chiffres manquants", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    ex = example("38 + 25", ["u : 8 + 5 = 13, j’écris 3, je retiens 1", "d : 1 + 3 + 2 = 6"], "63") if lv == 0 else \
        example("367 + 258", ["u : 7 + 8 = 15, j’écris 5, je retiens 1", "d : 1 + 6 + 5 = 12, j’écris 2, je retiens 1", "c : 1 + 3 + 2 = 6"], "625")
    body = lesson(["On <b>aligne les unités</b> : unités sous unités, dizaines sous dizaines.",
                   "On calcule colonne par colonne, <b>de droite à gauche</b>, en commençant par les unités.",
                   "Si une colonne fait 10 ou plus, on écrit les unités et on <b>retient</b> 1 dans la colonne suivante."],
                  [ex], [["Oublier la retenue : 38 + 25 = 53", "8 + 5 = 13 : on écrit 3 et on retient 1 dizaine. 38 + 25 = 63."],
                         ["Mal aligner : 34 + 5 = 84", "Le 5 se met sous le 4 (les unités) : 34 + 5 = 39."],
                         ["Écrire 13 dans une colonne : 38 + 25 = 513", "Dans une colonne, on n’écrit qu’un seul chiffre."]])
    faq = [("Pourquoi commencer par les unités ?", "Parce que la retenue des unités va dans la colonne des dizaines."),
           ("Comment vérifier ?", "On peut calculer un ordre de grandeur : 38 + 25, c’est environ 40 + 25 = 65.")]
    unit(lv, R, "addition-posee", "N",
         ("Calculer en ligne ou en colonnes des additions de deux ou trois nombres d’un ou deux chiffres ; comprendre la retenue" if lv == 0 else
          "Calculer en colonnes des additions de deux ou trois nombres jusqu’à trois chiffres, avec ou sans retenue"),
         "L’addition posée", "Addition posée",
         ("Fiches de maths CP sur l’addition posée : sans retenue, avec une retenue, trois nombres, chiffres manquants et problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 sur l’addition posée jusqu’à 1 000 : sans retenue, avec retenues, trois nombres, chiffres manquants et problèmes. 100 exercices corrigés."),
         "On aligne les unités et on commence à droite.", "8 + 5 = 13 : j’écris 3, je retiens 1.", body, faq, sets, 6)


if __name__ == "__main__":
    build(0)
