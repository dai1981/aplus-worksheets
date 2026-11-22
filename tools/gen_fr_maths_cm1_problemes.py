# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Résoudre des problèmes (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_problemes.py
Problèmes additifs (parties-tout, comparaison) avec entiers et décimaux, multiplicatifs (parties-tout, comparaison
multiplicative), problèmes mixtes en plusieurs étapes, dénombrement, optimisation ; CM2 : problèmes préparant aux algorithmes.
Erreurs : choisir l’opération d’après un mot, oublier une étape, additionner les choix d’un dénombrement.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, dz

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52114 + 100 * lv)
    K = Kids(R)


def big(lo, hi):
    return R.randint(lo, hi) * (1 if L == 1 else 10)


def s1():
    p, o = K.two()
    k = R.choice(["tout", "partie", "ecart", "decimal", "plus"])
    if k == "tout":
        a, b = big(12000, 48000), big(9000, 39000)
        return mcq("Un stade a vendu %s billets samedi et %s dimanche. Combien de billets en tout ?" % (num(a), num(b)), num(a + b), [num(abs(a - b)), num(a + b + 1000), num(a + b - 100)],
                   "Le tout = la somme des parties : %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "partie":
        t, a = big(30000, 90000), big(8000, 25000)
        return mcq("Une ville a %s habitants, dont %s enfants. Combien d’adultes ?" % (num(t), num(a)), num(t - a), [num(t + a), num(t - a + 1000), num(a)],
                   "On cherche une partie : %s − %s = <b>%s</b>." % (num(t), num(a), num(t - a)))
    if k == "ecart":
        a, b = R.randint(1800, 2900), R.randint(4000, 8848)
        return mcq("Le Mont Blanc mesure 4 806 m. Une montagne mesure %s m. Quel est l’écart de hauteur ?" % num(a), "%s m" % num(4806 - a), ["%s m" % num(4806 + a), "%s m" % num(4806 - a + 100), "%s m" % num(a)],
                   "On cherche l’écart : 4 806 − %s = <b>%s m</b>." % (num(a), num(4806 - a)))
    if k == "decimal":
        a, b = R.randint(105, 899), R.randint(105, 899)
        return mcq("%s achète un livre à %s € et un cahier à %s €. Combien paie-t-%s ?" % (p[0], dz(a + 500, 2, True), dz(b, 2, True), p[1]), dz(a + 500 + b, 2, True) + " €",
                   [dz(abs(a + 500 - b), 2, True) + " €", dz(a + 500 + b + 100, 2, True) + " €", dz(a + 500 + b - 10, 2, True) + " €"], "%s + %s = <b>%s €</b>." % (dz(a + 500, 2, True), dz(b, 2, True), dz(a + 500 + b, 2, True)))
    a, d = R.randint(1200, 9000), R.randint(150, 900)
    return mcq("%s a marché %s pas. C’est %s pas de moins que %s. Combien de pas %s a-t-%s faits ?" % (p[0], num(a), num(d), o[0], o[0], o[1]), num(a + d), [num(a - d), num(d), num(a + d + 100)],
               "%s en a fait plus : %s + %s = <b>%s</b>. « De moins » ne veut pas toujours dire « − »." % (o[0], num(a), num(d), num(a + d)))


def s2():
    p, o = K.two()
    k = R.choice(["groupes", "partage", "fois", "foismoins", "prix"])
    if k == "groupes":
        a, b = R.randint(12, 48), R.randint(24, 64)
        return mcq("Un théâtre a %d rangées de %d places. Combien de places ?" % (a, b), num(a * b), [num(a + b), num(a * b + b), num(a * (b - 1))], "%d %s %d = <b>%s</b>." % (a, FOIS, b, num(a * b)))
    if k == "partage":
        d, q = R.randint(3, 9), R.randint(25, 150)
        return mcq("On partage %s € de façon égale entre %d associations. Combien reçoit chacune ?" % (num(d * q), d), "%s €" % num(q), ["%s €" % num(d * q - d), "%s €" % num(d * q * d), "%s €" % num(q + d)],
                   "%s %s %d = <b>%s €</b>." % (num(d * q), DIV, d, num(q)))
    if k == "fois":
        a, f = R.randint(15, 250), R.randint(3, 12)
        return mcq("Un vélo coûte %d €. Une moto coûte %d fois plus cher. Combien coûte la moto ?" % (a, f), "%s €" % num(a * f), ["%s €" % num(a + f), "%s €" % num(a * f + a), "%s €" % num(a * (f - 1))],
                   "%d fois plus : %d %s %d = <b>%s €</b>." % (f, a, FOIS, f, num(a * f)))
    if k == "foismoins":
        f, q = R.randint(3, 9), R.randint(12, 90)
        return mcq("La tour Eiffel mesure environ 330 m. Un immeuble est %d fois moins haut qu’une tour de %d m. Quelle est sa hauteur ?" % (f, f * q) if False else
                   "Un camion transporte %s kg. Une camionnette transporte %d fois moins. Combien transporte la camionnette ?" % (num(f * q * 10), f), "%s kg" % num(q * 10),
                   ["%s kg" % num(f * q * 10 - f), "%s kg" % num(f * q * 10 * f), "%s kg" % num(q * 10 + f)], "%d fois moins : %s %s %d = <b>%s kg</b>." % (f, num(f * q * 10), DIV, f, num(q * 10)))
    a, b = R.randint(2, 9), R.randint(3, 15)
    return mcq("%s a %d ans. Son grand-père a %d ans de plus que %d fois son âge. Quel âge a le grand-père ?" % (p[0], b, a, R.choice([5, 6, 7])) if False else
               "%s a %d images. %s en a %d fois plus. Combien d’images ont-ils ensemble ?" % (p[0], b, o[0], a), num(b + a * b), [num(a * b), num(a + b), num(b * (a + 2))],
               "%s : %d %s %d = %d. Ensemble : %d + %d = <b>%d</b>." % (o[0], b, FOIS, a, a * b, b, a * b, b + a * b))


def s3():
    p = K.next()
    k = R.choice(["sortie", "achat", "stock", "voyage", "salaire"])
    if k == "sortie":
        n, pb, nb = R.randint(20, 30), R.randint(5, 12), R.randint(2, 4)
        bus = R.randint(150, 400)
        t = n * pb + bus
        return mcq("Une classe de %d élèves va au musée. L’entrée coûte %d € par élève et le car coûte %d €. Quel est le prix total ?" % (n, pb, bus), "%s €" % num(t), ["%s €" % num(n * pb), "%s €" % num(n + pb + bus), "%s €" % num((pb + bus) * n) if (pb + bus) * n < 20000 else "%s €" % num(t + 100)],
                   "%d %s %d = %d € ; %d + %d = <b>%s €</b>." % (n, FOIS, pb, n * pb, n * pb, bus, num(t)))
    if k == "achat":
        a, pa, b, pb, have = R.randint(2, 5), R.randint(105, 899), R.randint(2, 4), R.randint(250, 1299), 5000
        t = a * pa + b * pb
        if t >= have:
            return None
        return mcq("%s achète %d stylos à %s € et %d livres à %s €. %s paie avec 50 €. Combien lui rend-on ?" % (p[0], a, dz(pa, 2, True), b, dz(pb, 2, True), p[1].capitalize()), dz(have - t, 2, True) + " €",
                   [dz(t, 2, True) + " €", dz(have - pa - pb, 2, True) + " €", dz(have - t + 100, 2, True) + " €"],
                   "%d %s %s + %d %s %s = %s € ; 50 − %s = <b>%s €</b>." % (a, FOIS, dz(pa, 2, True), b, FOIS, dz(pb, 2, True), dz(t, 2, True), dz(t, 2, True), dz(have - t, 2, True)))
    if k == "stock":
        c, n, v = R.randint(12, 40), R.choice([6, 12, 24]), R.randint(50, 200)
        t = c * n - v
        if t <= 0:
            return None
        return mcq("Un magasin reçoit %d cartons de %d bouteilles. Il en vend %d. Combien de bouteilles reste-t-il ?" % (c, n, v), num(t), [num(c * n + v), num(c * n), num((c - v // n) * n) if (c - v // n) * n != t else num(t + n)],
                   "%d %s %d = %s ; %s − %d = <b>%s</b>." % (c, FOIS, n, num(c * n), num(c * n), v, num(t)))
    if k == "voyage":
        d, j = R.randint(150, 480), R.randint(3, 6)
        tot = d * j
        return mcq("Une famille roule %d km par jour pendant %d jours, puis %d km pour rentrer. Combien de kilomètres en tout ?" % (d, j, d + 100), "%s km" % num(tot + d + 100),
                   ["%s km" % num(tot), "%s km" % num(d * (j + 1)), "%s km" % num(tot + d + 100 + 1000)], "%d %s %d = %s ; %s + %d = <b>%s km</b>." % (d, FOIS, j, num(tot), num(tot), d + 100, num(tot + d + 100)))
    m, f = R.randint(1200, 2400), R.randint(200, 600)
    return mcq("Une famille gagne %s € par mois. Elle dépense %s € pour le loyer et %d € pour les courses. Combien reste-t-il ?" % (num(m * 2), num(m), f), "%s €" % num(m - f),
               ["%s €" % num(m * 2 - f), "%s €" % num(m + f), "%s €" % num(m)], "%s − %s − %d = <b>%s €</b>." % (num(m * 2), num(m), f, num(m - f)))


def s4():
    k = R.choice(["menu", "nombres", "ranger", "tenues", "drapeaux"])
    if k == "menu":
        a, b, c = R.randint(2, 4), R.randint(2, 5), R.randint(2, 4)
        return mcq("Au restaurant : %d entrées, %d plats et %d desserts. Combien de menus différents (entrée + plat + dessert) ?" % (a, b, c), num(a * b * c), [num(a + b + c), num(a * b + c), num(a * b * c + 1)],
                   "Chaque entrée va avec chaque plat et chaque dessert : %d %s %d %s %d = <b>%d</b>." % (a, FOIS, b, FOIS, c, a * b * c))
    if k == "nombres":
        ds = R.sample(range(1, 10), R.choice([3, 4]))
        n = len(ds)
        r = n * (n - 1)
        return mcq("Avec les chiffres %s, combien de nombres à 2 chiffres différents peut-on écrire (sans utiliser deux fois le même chiffre) ?" % ", ".join(map(str, ds)), str(r), [str(n * n), str(n), str(n + n - 1)],
                   "%d choix pour le premier chiffre, puis %d pour le second : %d %s %d = <b>%d</b>." % (n, n - 1, n, FOIS, n - 1, r))
    if k == "ranger":
        n = R.choice([3, 4])
        f = 6 if n == 3 else 24
        return mcq("De combien de façons %d enfants peuvent-ils se mettre en file l’un derrière l’autre ?" % n, str(f), [str(n * n), str(n), str(f // 2)],
                   "%s = <b>%d</b> façons." % (" %s ".join(str(i) for i in range(n, 0, -1)) % tuple([FOIS] * (n - 1)), f))
    if k == "tenues":
        a, b = R.randint(3, 6), R.randint(2, 5)
        return mcq("%s a %d pulls et %d pantalons. Combien de tenues différentes ?" % (K.next()[0], a, b), str(a * b), [str(a + b), str(a * b - 1), str(a * a)],
                   "%d %s %d = <b>%d</b>." % (a, FOIS, b, a * b))
    n = R.choice([4, 5, 6])
    r = n * (n - 1) // 2
    return mcq("%d amis se serrent la main, chacun une fois avec chacun des autres. Combien de poignées de main ?" % n, str(r), [str(n * (n - 1)), str(n * n), str(n)],
               "Chacun serre %d mains : %d %s %d = %d, mais chaque poignée est comptée deux fois : %d %s 2 = <b>%d</b>." % (n - 1, n, FOIS, n - 1, n * (n - 1), n * (n - 1), DIV, r))


def s5():
    k = R.choice(["boites", "prix", "minibus"] + (["algo", "algo2"] if L == 2 else ["monnaie"]))
    if k == "boites":
        n = R.randint(40, 150)
        b1, b2 = 12, 5
        best = None
        for x in range(n // b1 + 2):
            rest = n - b1 * x
            if rest < 0:
                continue
            y = -(-rest // b2)
            t = x + y
            if best is None or t < best:
                best = t
        return mcq("On doit ranger %d œufs dans des boîtes de 12 ou de 5. Quel est le plus petit nombre de boîtes possible ?" % n, str(best), [str(best + 1), str(-(-n // 5)), str(best - 1) if best > 1 else str(best + 2)],
                   "On utilise le plus possible de boîtes de 12, puis des boîtes de 5 pour le reste : <b>%d</b> boîtes." % best)
    if k == "prix":
        u = R.randint(60, 150)
        lot = 6 * u - R.randint(30, 120)
        n = 6
        a = "le lot de 6" if lot < 6 * u else "6 à l’unité"
        return mcq("Un yaourt coûte %s €. Un lot de 6 yaourts coûte %s €. Pour 6 yaourts, quelle est la solution la moins chère, et combien économise-t-on ?" % (dz(u, 2, True), dz(lot, 2, True)),
                   "le lot, on économise %s €" % dz(6 * u - lot, 2, True), ["à l’unité, on économise %s €" % dz(6 * u - lot, 2, True), "le lot, on économise %s €" % dz(6 * u, 2, True), "c’est le même prix"],
                   "6 %s %s = %s € ; %s − %s = <b>%s €</b> d’économie avec le lot." % (FOIS, dz(u, 2, True), dz(6 * u, 2, True), dz(6 * u, 2, True), dz(lot, 2, True), dz(6 * u - lot, 2, True)))
    if k == "minibus":
        n, c = R.randint(30, 95), R.choice([8, 9, 12])
        q = -(-n // c)
        if n % c == 0:
            return None
        return mcq("%d personnes partent en minibus de %d places. Combien de minibus faut-il au minimum ?" % (n, c), str(q), [str(q - 1), str(n % c), str(q + 1)],
                   "%d %s %d = %d reste %d : il faut un minibus de plus : <b>%d</b>." % (n, DIV, c, n // c, n % c, q))
    if k == "monnaie":
        t = R.choice([380, 270, 460, 590, 740, 830, 960, 1170])
        coins = []
        r = t
        for v in [200, 100, 50, 20, 10]:
            while r >= v:
                coins.append(v)
                r -= v
        return mcq("Avec des pièces de 2 €, 1 €, 50 c, 20 c et 10 c, quel est le plus petit nombre de pièces pour payer %s € ?" % dz(t, 2, True), str(len(coins)), [str(len(coins) + 1), str(t // 100 + 1), str(len(coins) - 1)],
                   "On prend d’abord les plus grosses pièces : %s → <b>%d pièces</b>." % (" + ".join(("%d €" % (c // 100)) if c >= 100 else "%d c" % c for c in coins), len(coins)))
    if k == "algo":
        s, a, lim = R.randint(1, 20), R.randint(4, 9), R.randint(50, 120)
        n, x = 0, s
        while x <= lim:
            x += a
            n += 1
        return mcq("On part de %d. On répète : « ajoute %d », jusqu’à dépasser %d. Combien de fois ajoute-t-on %d ?" % (s, a, lim, a), str(n), [str(n - 1), str(n + 1), str(lim // a)],
                   "On ajoute %d jusqu’à %d, qui dépasse %d : <b>%d</b> fois." % (a, x, lim, n) if lim // a != n else "On ajoute %d jusqu’à %d : <b>%d</b> fois." % (a, x, n))
    x = R.randint(40, 90)
    steps = []
    n = x
    c = 0
    while n != 1 and c < 12:
        n = n // 2 if n % 2 == 0 else n + 1
        c += 1
    if n != 1:
        return None
    return mcq("Règle : si le nombre est pair, on le divise par 2 ; s’il est impair, on ajoute 1. On part de %d. Combien d’étapes pour arriver à 1 ?" % x, str(c), [str(c - 1), str(c + 1), str(c + 2)],
               "On applique la règle jusqu’à 1 : <b>%d</b> étapes." % c)


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Problèmes additifs", mix(R, seen, [(s1, 20)])),
        ("Problèmes multiplicatifs", mix(R, seen, [(s2, 20)])),
        ("Problèmes en plusieurs étapes", mix(R, seen, [(s3, 20)])),
        ("Dénombrer", mix(R, seen, [(s4, 20)])),
        ("Optimiser" if lv == 1 else "Optimiser et suivre un algorithme", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Je lis l’énoncé et je cherche <b>ce que l’on demande</b>. Je fais un schéma (barres) pour voir le tout et les parties.",
         "Tout = somme des parties ; une partie = tout − autre partie ; un écart se calcule avec une soustraction.",
         "« %d fois plus » : %s ; « %d fois moins » : %s." % (3, FOIS, 3, DIV),
         "Pour dénombrer, je cherche une méthode : tableau, arbre, ou produit des choix (3 entrées %s 4 plats = 12 menus)." % FOIS],
        [example("Une classe de 25 élèves : entrée 8 € par élève, car 300 €", ["25 %s 8 = 200" % FOIS, "200 + 300 = 500"], "500 €")],
        [["Choisir l’opération d’après un mot", "« de moins » peut demander une addition : fais un schéma."],
         ["Oublier une étape", "Écris les questions intermédiaires : « combien pour les élèves ? », puis « combien en tout ? »"],
         ["Additionner les choix : 3 entrées et 4 plats = 7 menus", "Chaque entrée va avec chaque plat : 3 %s 4 = 12." % FOIS]])
    faq = [("Comment savoir quelle opération choisir ?", "On imagine la situation ou on fait un schéma en barres : on voit si on cherche un tout, une partie, un écart ou un nombre de fois."),
           ("Qu’est-ce qu’un problème d’optimisation ?", "On cherche la meilleure solution : le moins de boîtes, le prix le plus bas, le chemin le plus court…")]
    unit(lv, R, "problemes", "N",
         "Résoudre des problèmes additifs (parties-tout, comparaison), multiplicatifs (parties-tout, comparaison multiplicative), mixtes en plusieurs étapes, de dénombrement et d’optimisation%s, avec des nombres entiers et décimaux" % ("" if lv == 1 else " ; problèmes préparant à l’utilisation d’algorithmes"),
         "Résoudre des problèmes", "Problèmes",
         "Fiches de maths %s de problèmes : additifs, multiplicatifs, en plusieurs étapes, dénombrement et optimisation%s. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", algorithmes"),
         "Je cherche ce que l’on demande, puis je fais un schéma.", "Tout, partie, écart, fois plus : chaque situation a son opération.",
         body, faq, sets, 14)


if __name__ == "__main__":
    build(1)
