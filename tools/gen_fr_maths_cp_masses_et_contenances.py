# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Masses et contenances
  python3 tools/gen_fr_maths_cp_masses_et_contenances.py
CP : comparer des masses (balance) et des contenances (récipients, nombre de verres). CE1 : g, kg ; L, dL, cL ; lire une balance
et un verre doseur ; problèmes.
Erreurs : croire que le plus gros est le plus lourd, croire que le plateau qui monte est le plus lourd, 1 kg = 100 g.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, ch, KINDS, nom, le, NB, FOIS, CHOSE
import k_pics as KP
import f_common as FC
import gen_fr_maths_ce2_masses_et_contenances as MC

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53011 + 100 * lv)
    K = Kids(R)
    MC.R = R
    MC.K = K


LOURD = [("une plume", 1), ("une feuille de papier", 2), ("une gomme", 3), ("une pomme", 5), ("un livre", 7), ("une bouteille d’eau", 8),
         ("un chat", 10), ("un sac de pommes de terre", 12), ("un enfant", 14), ("un vélo", 15), ("une vache", 20), ("une voiture", 22), ("un éléphant", 25)]


def s1():
    a, b = R.sample(KINDS, 2)
    k = R.choice(["left", "right", "equal"]) if R.random() < 0.9 else "equal"
    n, m = R.randint(1, 4), R.randint(1, 4)
    svg = pic(KP.balance_svg((a, n), (b, m), k), "balance : à gauche %s, à droite %s" % (ch(a, n), ch(b, m)), lg=True)
    A, B = "les %s" % nom(a, n) if n > 1 else le(a), "les %s" % nom(b, m) if m > 1 else le(b)
    if k == "equal":
        return mcq("<div class='qfig'>%s</div>Que montre la balance ?" % svg, "les deux côtés ont la même masse", ["le côté gauche est plus lourd", "le côté droit est plus lourd", "on ne peut pas savoir"],
                   "Les plateaux sont au même niveau : <b>les deux côtés ont la même masse</b>.")
    heavy = A if k == "left" else B
    light = B if k == "left" else A
    return mcq("<div class='qfig'>%s</div>Qu’est-ce qui est le plus lourd ?" % svg, heavy, [light, "les deux ont la même masse", "on ne peut pas savoir"],
               "Le plateau le plus lourd descend : <b>%s</b>." % heavy)


def s2():
    xs = sorted(R.sample(LOURD, 4), key=lambda t: t[1])
    heavy = R.random() < 0.55
    ans = xs[-1][0] if heavy else xs[0][0]
    return mcq("Qu’est-ce qui est le plus %s : %s ?" % ("lourd" if heavy else "léger", ", ".join(t[0] for t in R.sample(xs, 4))), ans, [t[0] for t in xs if t[0] != ans],
               "<b>%s</b> est le plus %s." % (ans[0].upper() + ans[1:], "lourd" if heavy else "léger"))


def s3():
    n = R.choice([3, 4])
    ws = R.sample([40, 50, 60, 70], n)
    hs = [R.randint(70, 120) for _ in range(n)]
    k = R.choice(["same", "level"])
    if k == "same":
        lev = [R.uniform(0.2, 0.95) for _ in range(n)]
        ws = [50] * n
        hs = [110] * n
        vol = lev
    else:
        lev = [0.999] * n
        ws = [R.choice([40, 50, 60, 70]) for _ in range(n)]
        hs = [R.randint(60, 120) for _ in range(n)]
        vol = [w * h for w, h in zip(ws, hs)]
    if len(set(round(v, 2) for v in vol)) < n:
        return None
    i = max(range(n), key=lambda j: vol[j])
    svg = pic(FC.glasses_svg(list(zip(ws, hs, lev))), "%d récipients A à %s" % (n, "ABCD"[n - 1]), lg=True)
    if k == "same":
        return mcq("<div class='qfig'>%s</div>Les verres sont pareils. Dans quel verre y a-t-il le plus d’eau ?" % svg, "le verre %s" % "ABCD"[i], ["le verre %s" % "ABCD"[j] for j in range(n) if j != i] + ["ils ont tous autant d’eau"],
                       "Les verres ont la même forme : le plus d’eau, c’est le niveau le plus haut, <b>le verre %s</b>." % "ABCD"[i])
    srt = sorted(range(n), key=lambda j: vol[j])
    if vol[srt[-1]] < vol[srt[-2]] * 1.25:
        return None
    return mcq("<div class='qfig'>%s</div>Les récipients sont pleins. Lequel contient le plus ?" % svg, "le récipient %s" % "ABCD"[i], ["le récipient %s" % "ABCD"[j] for j in range(n) if j != i] + ["ils contiennent tous autant"],
               "Le récipient %s est à la fois large et haut : c’est <b>le récipient %s</b>." % ("ABCD"[i], "ABCD"[i]))


def s4():
    a, b = R.sample(range(2, 9), 2)
    names = R.sample(["la carafe", "la bouteille", "le seau", "l’arrosoir", "la casserole", "le pichet"], 2)
    more = R.random() < 0.6
    v = names[0] if (a > b) == more else names[1]
    if R.random() < 0.4:
        svg = pic(KP.row_svg(a, "cup"), "%d verres" % a)
        return mcq("<div class='qfig'>%s</div>Il faut %d verres pour remplir %s et %d verres pour remplir %s. Qui contient le %s ?" % (svg, a, names[0], b, names[1], "plus" if more else "moins"),
                   v, [names[1] if v == names[0] else names[0], "ils contiennent autant", "on ne peut pas savoir"],
                   "Plus il faut de verres, plus le récipient contient : <b>%s</b>." % v)
    return mcq("Il faut %d verres pour remplir %s et %d verres pour remplir %s. Qui contient le %s ?" % (a, names[0], b, names[1], "plus" if more else "moins"),
               v, [names[1] if v == names[0] else names[0], "ils contiennent autant", "on ne peut pas savoir"],
               "Plus il faut de verres, plus le récipient contient : <b>%s</b>." % v)


def s5():
    p = K.next()
    k = R.choice(["eq", "verres", "verres2", "bal3"])
    if k == "eq":
        n = R.randint(2, 5)
        m = R.randint(2, 4)
        return mcq("Un melon pèse autant que %d pommes. Combien de pommes faut-il pour équilibrer %d melons ?" % (n, m), str(n * m), [str(n + m), str(n), str(m)],
                   "%s = <b>%d</b> pommes." % (" + ".join([str(n)] * m), n * m))
    if k == "verres":
        n, m = R.randint(2, 5), R.randint(2, 3)
        return mcq("%s remplit une carafe avec %d verres. Combien de verres faut-il pour remplir %d carafes pareilles ?" % (p[0], n, m), str(n * m), [str(n + m), str(n), str(n * m + 1)],
                   "%s = <b>%d</b> verres." % (" + ".join([str(n)] * m), n * m))
    if k == "verres2":
        a, b = R.randint(5, 9), R.randint(1, 4)
        return mcq("Une bouteille remplit %d verres. %s a déjà rempli %s. Combien de verres peut-%s encore remplir ?" % (a, p[0], pl(b, "verre"), p[1]), str(a - b), [str(a + b), str(a), str(b)],
                   "%d − %d = <b>%d</b> verres." % (a, b, a - b))
    x = R.sample(["le livre", "la trousse", "la boîte", "le sac", "la valise", "le cartable"], 3)
    cap = lambda t: t[0].upper() + t[1:]
    lourd = lambda t: "lourde" if t.startswith("la ") else "lourd"
    return mcq("%s est plus %s que %s. %s est plus %s que %s. Qu’est-ce qui est le plus léger ?" % (cap(x[0]), lourd(x[0]), x[1], cap(x[1]), lourd(x[1]), x[2]),
               x[2], [x[0], x[1], "on ne peut pas savoir"], "%s, puis %s, puis %s : le plus léger est <b>%s</b>." % (x[0], x[1], x[2], x[2]))


# --------------------------------------------------- CE1
MASS1 = [m for m in MC.MASS if m[2] in ("g", "kg")]
CAP1 = [c for c in MC.CAP if c[2] in ("L", "cL", "dL")]


def e1():
    if R.random() < 0.5:
        o, v, u = R.choice(MASS1)
        return mcq("Quelle unité convient ? %s %s …" % (o, num(v)), u, [x for x in ["g", "kg", "L", "cL"] if x != u], "%s %s <b>%s</b>." % (o, num(v), u))
    o, v, u = R.choice(CAP1)
    return mcq("Quelle unité convient ? %s %s …" % (o, num(v)), u, [x for x in ["L", "dL", "cL", "kg"] if x != u], "%s %s <b>%s</b>." % (o, num(v), u))


def e2():
    k = R.choice(["kg_g", "kgg", "L_cL", "L_dL", "cmp_kg", "cmp_L"])
    a = R.randint(1, 9)
    U = MC.U
    if k == "kg_g":
        return mcq("Complète : %s = … g" % U(a, "kg"), num(a * 1000), [num(a * 100), num(a * 10), num(a + 1000)], "1 kg = 1 000 g, donc %d kg = <b>%s g</b>." % (a, num(a * 1000)))
    if k == "kgg":
        b = R.choice([100, 200, 250, 300, 400, 500, 600, 750, 800])
        if a > 4:
            return None
        return mcq("Complète : %s %s = … g" % (U(a, "kg"), U(b, "g")), num(a * 1000 + b), [num(a * 100 + b), num(a + b), num(a * 1000 + b * 10)],
                   "%d kg = %s g ; %s + %d = <b>%s g</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "L_cL":
        return mcq("Complète : %s = … cL" % U(a, "L"), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 L = 100 cL, donc %d L = <b>%s cL</b>." % (a, num(a * 100)))
    if k == "L_dL":
        return mcq("Complète : %s = … dL" % U(a, "L"), num(a * 10), [num(a * 100), num(a), num(a * 1000)], "1 L = 10 dL, donc %d L = <b>%s dL</b>." % (a, num(a * 10)))
    if k == "cmp_kg":
        y = R.choice([500, 800, 900, 1200, 1500, 2000, 750, 950])
        ans = "1 kg" if y < 1000 else U(y, "g")
        return mcq("Lequel est le plus lourd : 1 kg ou %s ?" % U(y, "g"), ans, [U(y, "g") if y < 1000 else "1 kg", "ils ont la même masse", "on ne peut pas comparer"],
                   "1 kg = 1 000 g : le plus lourd est <b>%s</b>." % ans)
    y = R.choice([50, 75, 90, 120, 150, 200, 80])
    ans = "1 L" if y < 100 else U(y, "cL")
    return mcq("Lequel contient le plus : 1 L ou %s ?" % U(y, "cL"), ans, [U(y, "cL") if y < 100 else "1 L", "ils contiennent autant", "on ne peut pas comparer"],
               "1 L = 100 cL : c’est <b>%s</b>." % ans)


def e5():
    p = K.next()
    k = R.choice(["sac", "bouteilles", "panier", "verres", "reste", "farine"])
    if k == "sac":
        a, b = R.randint(1, 4), R.choice([200, 250, 300, 500])
        return mcq("%s porte un sac de %d kg et un paquet de %d g. Quelle masse porte-t-%s en tout ?" % (p[0], a, b, p[1]), "%s g" % num(a * 1000 + b), ["%s g" % num(a + b), "%s g" % num(a * 100 + b), "%s kg" % num(a + b)],
                   "%d kg = %s g ; %s + %d = <b>%s g</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "bouteilles":
        n, c = R.randint(2, 4), R.choice([25, 50])
        return mcq("On remplit %d bouteilles de %d cL. Combien de centilitres faut-il ?" % (n, c), "%d cL" % (n * c), ["%d cL" % (n + c), "%d L" % (n * c), "%d cL" % (n * c + c)],
                   "%s = <b>%d cL</b>." % (" + ".join([str(c)] * n), n * c))
    if k == "panier":
        a, b, c = R.choice([150, 200, 250]), R.choice([300, 400, 500]), R.choice([100, 120, 180])
        return mcq("Dans un panier, il y a une pomme de %d g, un melon de %d g et une poire de %d g. Quelle est la masse des fruits ?" % (a, b, c), "%d g" % (a + b + c), ["%d g" % (a + b), "%d kg" % (a + b + c), "%d g" % (a + b + c + 100)],
                   "%d + %d + %d = <b>%d g</b>." % (a, b, c, a + b + c))
    if k == "verres":
        v = R.choice([20, 25, 50])
        return mcq("Avec une bouteille de 1 L, combien de verres de %d cL peut-on remplir ?" % v, str(100 // v), [str(100 - v), str(10 // (v // 10) if v != 25 else 3), str(v)],
                   "1 L = 100 cL ; %s = 100 : <b>%d</b> verres." % (" + ".join([str(v)] * (100 // v)), 100 // v))
    if k == "reste":
        b = R.choice([20, 30, 40, 25, 60, 75])
        return mcq("Une bouteille contient 1 L de jus. %s en boit %d cL. Combien de jus reste-t-il ?" % (p[0], b), "%d cL" % (100 - b), ["%d cL" % (b + 100), "%d cL" % (10 - b // 10), "%d L" % (100 - b)],
                   "1 L = 100 cL ; 100 − %d = <b>%d cL</b>." % (b, 100 - b))
    b = R.choice([200, 250, 300, 400, 600, 750])
    return mcq("Un paquet contient 1 kg de farine. Pour un gâteau, on utilise %d g. Combien de farine reste-t-il ?" % b, "%d g" % (1000 - b), ["%d g" % (100 - b // 10), "%s g" % num(1000 + b), "%d kg" % (1000 - b)],
               "1 kg = 1 000 g ; 1 000 − %d = <b>%d g</b>." % (b, 1000 - b))


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("La balance", mix(R, seen, [(s1, 20)])), ("Lourd ou léger", mix(R, seen, [(s2, 20)])),
                ("Comparer des contenances", mix(R, seen, [(s3, 20)])), ("Mesurer avec des verres", mix(R, seen, [(s4, 20)])),
                ("Problèmes", mix(R, seen, [(s5, 20)]))]
        th = ["Pour comparer des masses, on utilise une <b>balance</b> : le plateau le plus lourd descend.",
              "Un gros objet n’est pas toujours le plus lourd : un ballon est gros mais léger.",
              "Pour comparer des contenances, on peut compter combien de verres il faut pour remplir chaque récipient."]
        ex = example("Il faut 5 verres pour la carafe et 3 pour la bouteille", ["5 &gt; 3"], "la carafe contient le plus")
    else:
        sets = [("Choisir la bonne unité", mix(R, seen, [(e1, 20)])), ("Convertir et comparer", mix(R, seen, [(e2, 20)])),
                ("Lire une balance", mix(R, seen, [(MC.s4_balance, 20)])), ("Lire un verre doseur", mix(R, seen, [(MC.s4_verre, 20)])),
                ("Problèmes", mix(R, seen, [(e5, 20)]))]
        th = ["La masse se mesure en <b>grammes</b> (g) et en <b>kilogrammes</b> (kg) : 1 kg = 1 000 g.",
              "La contenance se mesure en <b>litres</b> (L), décilitres (dL) et centilitres (cL) : 1 L = 10 dL = 100 cL.",
              "Pour comparer, on met les deux mesures dans la même unité."]
        ex = example("2 kg 300 g = … g", ["2 kg = 2 000 g", "2 000 + 300"], "2 300 g")
    body = lesson(th, [ex], [["Croire que le plus gros est le plus lourd", "On vérifie avec la balance."],
                             ["Croire que le plateau qui monte est le plus lourd", "C’est le plateau qui descend."],
                             ["1 kg = 100 g" if lv else "Comparer des verres de tailles différentes", "1 kg = 1 000 g." if lv else "On utilise toujours le même verre pour mesurer."]])
    faq = [("Comment lire une balance à plateaux ?", "Le côté le plus lourd descend ; si les plateaux sont au même niveau, les masses sont égales."),
           ("Quelle est la différence entre masse et contenance ?", "La masse dit si c’est lourd ; la contenance dit combien de liquide un récipient peut contenir.")]
    unit(lv, R, "masses-et-contenances", "G",
         ("Comparer des masses avec une balance ; comparer des contenances par transvasement ou en comptant des verres ; résoudre des problèmes simples" if lv == 0 else
          "Connaître le gramme et le kilogramme (1 kg = 1 000 g), le litre, le décilitre et le centilitre ; lire une balance et un récipient gradué ; résoudre des problèmes de masses et de contenances"),
         "Masses et contenances", "Masses et contenances",
         ("Fiches de maths CP sur les masses et les contenances : lire une balance, lourd ou léger, comparer des récipients, mesurer avec des verres et problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 sur les masses et les contenances : g, kg, L, dL, cL, convertir, lire une balance et un verre doseur, problèmes. 100 exercices corrigés."),
         "Le plateau le plus lourd descend." if lv == 0 else "1 kg = 1 000 g ; 1 L = 100 cL", "On compare avec une balance ou des verres." if lv == 0 else "On convertit avant de comparer.",
         body, faq, sets, 11)


if __name__ == "__main__":
    build(0)
