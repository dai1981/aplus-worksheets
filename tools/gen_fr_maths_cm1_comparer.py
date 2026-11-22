# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Comparer, encadrer et ranger les nombres (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_comparer.py
Comparer avec &lt; et &gt;, ranger, encadrer à la dizaine de mille / centaine de mille / au million, intercaler,
placer sur une demi-droite graduée, arrondir, problèmes.
Erreurs : comparer le premier chiffre sans regarder le nombre de chiffres, inverser &lt; et &gt;, encadrer au mauvais rang.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, droite, RANGS

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52102 + 100 * lv)
    K = Kids(R)


def rnd_n(lo=None):
    hi = 999999 if L == 1 else 999999999
    return R.randint(lo or (10000 if L == 1 else 1000000), hi)


def s1():
    a = rnd_n()
    k = R.choice(["proche", "chiffres", "proche"])
    if k == "proche":
        s = list(str(a))
        i = R.randint(1, len(s) - 1)
        s[i] = str((int(s[i]) + R.choice([1, 2, 3, 7])) % 10)
        b = int("".join(s))
    else:
        b = int(str(a)[:-1]) + 0
        b = int(str(a)[1:] + str(a)[0]) if R.random() < 0.5 else int(str(a)[:-1])
    if a == b or b < 1000:
        return None
    if R.random() < 0.5:
        a, b = b, a
    sg = "&lt;" if a < b else "&gt;"
    return mcq("Quel signe faut-il mettre : %s … %s ?" % (num(a), num(b)), sg, ["&gt;" if sg == "&lt;" else "&lt;", "=", "on ne peut pas savoir"],
               ("Les deux nombres n’ont pas le même nombre de chiffres : le plus long est le plus grand." if len(str(a)) != len(str(b)) else
                "Même nombre de chiffres : on compare de gauche à droite jusqu’au premier chiffre différent.") + " %s <b>%s</b> %s." % (num(a), sg, num(b)))


def s2():
    base = rnd_n()
    xs = set([base])
    while len(xs) < 4:
        s = list(str(base))
        i = R.randint(0, len(s) - 1)
        s[i] = str(R.randint(1 if i == 0 else 0, 9))
        v = int("".join(s))
        if R.random() < 0.25:
            v = int(str(base)[:-1])
        xs.add(v)
    xs = list(xs)
    R.shuffle(xs)
    asc = R.random() < 0.5
    good = sorted(xs, reverse=not asc)
    w1 = sorted(xs, reverse=asc)
    w2 = sorted(xs, key=lambda v: str(v), reverse=not asc)
    w3 = good[:]
    w3[1], w3[2] = w3[2], w3[1]
    w4 = good[:]
    w4[0], w4[1] = w4[1], w4[0]
    w5 = good[:]
    w5[2], w5[3] = w5[3], w5[2]
    f = lambda l: " ; ".join(num(v) for v in l)
    return mcq("Range dans l’ordre %s : %s" % ("croissant (du plus petit au plus grand)" if asc else "décroissant (du plus grand au plus petit)", f(xs)), f(good),
               [f(w1), f(w2), f(w3), f(w4), f(w5)], "On compare d’abord le nombre de chiffres, puis les chiffres de gauche à droite : <b>%s</b>." % f(good))


def s3():
    n = rnd_n()
    p = R.choice([3, 4, 5] if L == 1 else [4, 5, 6, 7])
    st = 10 ** p
    lo = n // st * st
    if lo == n:
        return None
    hi = lo + st
    nm = {3: "au millier", 4: "à la dizaine de mille", 5: "à la centaine de mille", 6: "au million", 7: "à la dizaine de millions"}[p]
    right = "%s &lt; %s &lt; %s" % (num(lo), num(n), num(hi))
    w = ["%s &lt; %s &lt; %s" % (num(n // (st // 10) * (st // 10)), num(n), num(n // (st // 10) * (st // 10) + st // 10)),
         "%s &lt; %s &lt; %s" % (num(lo - st), num(n), num(lo)) if lo >= st else "%s &lt; %s &lt; %s" % (num(lo + st), num(n), num(hi + st)),
         "%s &lt; %s &lt; %s" % (num(n // (st * 10) * st * 10), num(n), num(n // (st * 10) * st * 10 + st * 10))]
    return mcq("Encadre %s %s." % (num(n), nm), right, w, "On garde les chiffres jusqu’au rang des %s et on remplace les autres par des 0 : <b>%s</b>." % (RANGS[p], right))


def s3b():
    n = rnd_n()
    p = R.choice([3, 4] if L == 1 else [3, 5, 6])
    st = 10 ** p
    lo = n // st * st
    r = lo if n - lo < st // 2 else lo + st
    if n - lo == st // 2:
        return None
    nm = {3: "au millier", 4: "à la dizaine de mille", 5: "à la centaine de mille", 6: "au million"}[p]
    return mcq("Quel est l’arrondi de %s %s ?" % (num(n), nm), num(r), [num(lo if r != lo else lo + st), num(n // (st // 10) * (st // 10)), num(r // 10)],
               "%s est entre %s et %s ; il est plus proche de <b>%s</b>." % (num(n), num(lo), num(lo + st), num(r)))


def s4():
    st = 10 ** R.choice([3, 4] if L == 1 else [4, 5, 6])
    lo = R.randint(1, 80) * st * (1 if L == 1 else 1)
    step = st
    k = R.randint(1, 9)
    v = lo + k * step
    if v > (999999 if L == 1 else 999999999):
        return None
    pic = droite(lo, lo + 10 * step, step, [(v, "A")], labels=[lo, lo + 10 * step], width=420)
    return mcq("<div class='qfig'>%s</div>Quel nombre est repéré par la lettre A ?" % pic, num(v), [num(lo + k * step // 10), num(lo + (k + 1) * step), num(lo + (k - 1) * step) if k > 1 else num(v + 2 * step)],
               "Il y a 10 intervalles entre %s et %s : chaque graduation vaut %s. A = %s + %d %s %s = <b>%s</b>." % (num(lo), num(lo + 10 * step), num(step), num(lo), k, "×", num(step), num(v)))


VILLES = ["Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Lille", "Rennes", "Brest", "Dijon"]


def s5():
    k = R.choice(["entre", "pop", "prix", "chiffres"])
    if k == "entre":
        a = rnd_n()
        st = 10 ** R.choice([2, 3])
        b = a + 2 * st
        mid = a + st
        return mcq("Quel nombre est compris entre %s et %s ?" % (num(a), num(b)), num(mid), [num(a - st), num(b + st), num(a + 3 * st)],
                   "%s &lt; <b>%s</b> &lt; %s." % (num(a), num(mid), num(b)))
    if k == "pop":
        v = R.sample(VILLES, 3)
        ps = R.sample(range(20000, 900000) if L == 1 else range(100000, 2000000), 3)
        big = v[ps.index(max(ps))]
        return mcq("%s : %s habitants, %s : %s habitants, %s : %s habitants. Quelle ville a le plus d’habitants ?" % (v[0], num(ps[0]), v[1], num(ps[1]), v[2], num(ps[2])),
                   big, [x for x in v if x != big] + ["on ne peut pas savoir"], "Le plus grand nombre est %s : c’est <b>%s</b>." % (num(max(ps)), big))
    if k == "prix":
        a = R.randint(150, 450) * 1000 + R.randint(0, 9) * 100
        b = a + R.choice([-9000, 9000, -900, 900, 90000])
        rr = "la maison A" if a > b else "la maison B"
        return mcq("La maison A coûte %s €, la maison B coûte %s €. Laquelle est la plus chère ?" % (num(a), num(b)), rr, ["la maison B" if rr == "la maison A" else "la maison A", "elles ont le même prix", "on ne peut pas savoir"],
                   "On compare les chiffres de gauche à droite : %s %s %s. C’est <b>%s</b>." % (num(a), "&gt;" if a > b else "&lt;", num(b), rr))
    d = R.sample(range(1, 10), 4 if L == 1 else 5)
    if R.random() < 0.5:
        r = int("".join(map(str, sorted(d, reverse=True))))
        return mcq("Avec les chiffres %s (chacun une fois), quel est le plus grand nombre possible ?" % ", ".join(map(str, d)), num(r),
                   [num(int("".join(map(str, sorted(d))))), num(int("".join(map(str, d)))), num(int(str(r)[:-2] + str(r)[-1] + str(r)[-2]))],
                   "On place les plus grands chiffres à gauche : <b>%s</b>." % num(r))
    r = int("".join(map(str, sorted(d))))
    return mcq("Avec les chiffres %s (chacun une fois), quel est le plus petit nombre possible ?" % ", ".join(map(str, d)), num(r),
               [num(int("".join(map(str, sorted(d, reverse=True))))), num(int("".join(map(str, d)))), num(int(str(r)[:-2] + str(r)[-1] + str(r)[-2]))],
               "On place les plus petits chiffres à gauche : <b>%s</b>." % num(r))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Comparer deux nombres", mix(R, seen, [(s1, 20)])),
        ("Ranger des nombres", mix(R, seen, [(s2, 20)])),
        ("Encadrer et arrondir", mix(R, seen, [(s3, 12), (s3b, 8)])),
        ("La demi-droite graduée", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Le nombre qui a le <b>plus de chiffres</b> est le plus grand.",
         "S’ils ont autant de chiffres, on compare les chiffres <b>de gauche à droite</b> jusqu’au premier chiffre différent.",
         "&lt; se lit « inférieur à », &gt; se lit « supérieur à ». La pointe est tournée vers le plus petit.",
         "<b>Encadrer</b> au millier : on cherche les deux milliers entiers qui entourent le nombre. L’<b>arrondi</b> est le plus proche des deux."],
        [example("Encadre 437 815 à la dizaine de mille", ["43 dizaines de mille → 430 000", "puis 440 000"], "430 000 &lt; 437 815 &lt; 440 000")],
        [["Comparer seulement le premier chiffre : 98 000 &gt; 120 000", "120 000 a plus de chiffres : il est plus grand."],
         ["Inverser les signes", "La pointe montre le plus petit nombre."],
         ["Encadrer au mauvais rang", "Repère d’abord le rang demandé (milliers, dizaines de mille…)."]])
    faq = [("Que veut dire « encadrer » ?", "Écrire un nombre plus petit et un nombre plus grand, souvent des nombres « ronds », de chaque côté du nombre."),
           ("Quelle différence entre encadrer et arrondir ?", "Encadrer donne deux nombres ; arrondir donne le plus proche des deux.")]
    unit(lv, R, "comparer-encadrer-et-ranger-les-nombres", "N",
         "Utiliser le vocabulaire égal à, supérieur à, inférieur à, compris entre ; comparer, encadrer, intercaler, ordonner des nombres entiers jusqu’à %s ; les placer sur une demi-droite graduée" % ("999 999" if lv == 1 else "999 999 999"),
         "Comparer, encadrer et ranger les nombres", "Comparer et ranger les nombres",
         "Fiches de maths %s pour comparer, ranger, encadrer et arrondir les grands nombres et les placer sur une demi-droite graduée. 100 exercices corrigés." % GN(lv),
         "Plus de chiffres, plus grand nombre.", "Sinon, on compare les chiffres de gauche à droite.",
         body, faq, sets, 2)


if __name__ == "__main__":
    build(1)
