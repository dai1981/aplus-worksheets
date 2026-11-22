# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les probabilités (Organisation et gestion de données et probabilités)
  python3 tools/gen_fr_maths_cm1_probabilites.py
CM1 : expériences aléatoires, issues possibles, vocabulaire (certain, possible, impossible, probable, peu probable), comparer,
équiprobabilité, « deux issues ne veut pas dire une chance sur deux ». CM2 : issues réalisant un événement, « a chances sur b »,
comparer, indépendance, expériences en deux étapes (tableau, arbre).
Erreurs : croire qu’après 3 « pile » le « face » est plus probable, confondre nombre de boules et chances, deux issues = 1 chance sur 2.
"""
import random, math
from fr_c3 import mcq, lesson, example, unit, mix, Kids, GN, FOIS, wrap, text, INK, fr

R = K = None
L = 1
COL = {"rouge": "#e57373", "bleue": "#64b5f6", "verte": "#81c784", "jaune": "#ffd54f"}
COLM = {"rouge": "rouge", "bleue": "bleu", "verte": "vert", "jaune": "jaune"}


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52125 + 100 * lv)
    K = Kids(R)


def sac(counts):
    balls = []
    for c, n in counts.items():
        balls += [c] * n
    R.shuffle(balls)
    s = ["<path d='M10 30 Q10 150 80 150 Q150 150 150 30 Z' fill='#f4efe2' stroke='%s' stroke-width='2'/>" % INK]
    per = 5
    for i, c in enumerate(balls):
        x, y = 30 + (i % per) * 25, 125 - (i // per) * 24
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s' stroke='%s'/>" % (x, y, COL[c], INK))
    return wrap(162, 160, "".join(s), "un sac de boules : " + ", ".join("%d %s%s" % (n, c, "s" if n > 1 else "") for c, n in counts.items()))


def roue(secs):
    cx = cy = 80
    r = 70
    s, a0 = [], -math.pi / 2
    tot = float(sum(n for _, n in secs))
    for c, n in secs:
        a1 = a0 + 2 * math.pi * n / tot
        big = 1 if a1 - a0 > math.pi else 0
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, big, cx + r * math.cos(a1), cy + r * math.sin(a1), COL[c], INK))
        a0 = a1
    s.append("<path d='M%d %d l-7 -14 h14 Z' fill='%s'/>" % (cx, cy - r - 2, INK))
    return wrap(160, 160, "".join(s), "une roue de loterie")


def pl(n, c):
    return "%d boule%s %s%s" % (n, "s" if n > 1 else "", c, "s" if n > 1 else "")


def s1():
    k = R.choice(["de", "piece", "sac", "alea", "alea"])
    if k == "de":
        f = R.choice([6, 4, 8, 12])
        return mcq("On lance un dé à %d faces numérotées de 1 à %d. Combien d’issues possibles y a-t-il ?" % (f, f), str(f), [str(f // 2), str(f + 1), "1"], "Chaque face peut sortir : <b>%d</b> issues." % f)
    if k == "piece":
        n = R.choice([2, 3])
        return mcq("On lance %s pièce%s. Combien d’issues possibles (dans l’ordre) ?" % ("deux" if n == 2 else "trois", "s"), str(2 ** n), [str(n), str(2 * n), str(n + 1)],
                   "Pour chaque pièce, 2 possibilités : %s = <b>%d</b>." % (" %s ".join(["2"] * n) % tuple([FOIS] * (n - 1)), 2 ** n))
    if k == "sac":
        cs = R.sample(list(COL), R.randint(2, 4))
        counts = {c: R.randint(1, 4) for c in cs}
        return mcq("<div class='qfig'>%s</div>On tire une boule au hasard. Combien de couleurs différentes peut-on obtenir ?" % sac(counts), str(len(cs)), [str(sum(counts.values())), str(len(cs) + 1), "1" if len(cs) > 1 else "2"],
                   "Les issues possibles sont les couleurs : %s. Il y en a <b>%d</b>." % (", ".join(COLM[c] for c in cs), len(cs)))
    q, a, w = R.choice([("Lancer un dé est-il une expérience aléatoire ?", "oui, on ne peut pas prévoir le résultat", ["non, on sait toujours le résultat", "seulement si le dé est rouge", "non, il n’y a qu’une issue"]),
                        ("Lâcher une balle : va-t-elle tomber ? Est-ce une expérience aléatoire ?", "non, on connaît le résultat à l’avance", ["oui, c’est le hasard", "oui, il y a deux issues", "on ne peut pas savoir"]),
                        ("Tirer une carte au hasard dans un jeu mélangé est-il une expérience aléatoire ?", "oui", ["non", "seulement avec 52 cartes", "seulement si on gagne"]),
                        ("Faire 2 + 3 sur une calculatrice est-il une expérience aléatoire ?", "non, le résultat est toujours 5", ["oui", "seulement la première fois", "on ne peut pas savoir"]),
                        ("Tourner une roue de loterie est-il une expérience aléatoire ?", "oui", ["non", "seulement si elle a 2 couleurs", "non, on peut tout prévoir"])])
    return mcq(q, a, w, "Une expérience est aléatoire quand on ne peut pas prévoir le résultat, même si on connaît les issues possibles. Réponse : <b>%s</b>." % a)


def s2():
    cs = R.sample(list(COL), 3)
    counts = {cs[0]: R.randint(3, 6), cs[1]: R.randint(0, 2)}
    counts = {c: n for c, n in counts.items() if n}
    ask = R.choice(cs)
    n = counts.get(ask, 0)
    tot = sum(counts.values())
    if n == 0:
        right = "impossible"
    elif n == tot:
        right = "certain"
    else:
        right = "possible" if L == 1 or R.random() < 0.4 else ("probable" if n * 2 > tot else "peu probable")
    opts = ["certain", "possible", "impossible", "on ne peut pas savoir"] if right in ("certain", "possible", "impossible") else ["probable", "peu probable", "certain", "impossible"]
    return mcq("<div class='qfig'>%s</div>On tire une boule au hasard. Tirer une boule %s est…" % (sac(counts), COLM[ask] if False else ask.replace("bleue", "bleue")), right, [o for o in opts if o != right],
               "Il y a %d boule%s %s sur %d : c’est <b>%s</b>." % (n, "s" if n > 1 else "", ask, tot, right))


def s3():
    c = R.choice(list(COL))
    o = R.choice([x for x in COL if x != c])
    a1, b1 = R.randint(1, 5), R.randint(1, 5)
    a2, b2 = R.randint(1, 5), R.randint(1, 5)
    p1, p2 = a1 / float(a1 + b1), a2 / float(a2 + b2)
    if p1 == p2:
        return None
    right = "le sac A" if p1 > p2 else "le sac B"
    return mcq("Sac A : %s et %s. Sac B : %s et %s. Dans quel sac a-t-on le plus de chances de tirer une boule %s ?" % (pl(a1, c), pl(b1, o), pl(a2, c), pl(a2 and b2, o), c),
               right, ["le sac B" if right == "le sac A" else "le sac A", "autant de chances", "on ne peut pas savoir"],
               "On compare la part des boules %ss : %d sur %d dans A, %d sur %d dans B. C’est <b>%s</b>." % (c, a1, a1 + b1, a2, a2 + b2, right))


def s4_cm1():
    if R.random() < 0.5:
        k = R.choice(["eq", "ineq"])
        cs = R.sample(list(COL), R.choice([2, 3]))
        if k == "eq":
            secs = [(c, 1) for c in cs]
        else:
            secs = [(cs[0], 2)] + [(c, 1) for c in cs[1:]]
        right = "oui" if k == "eq" else "non"
        return mcq("<div class='qfig'>%s</div>Chaque couleur a-t-elle la même chance de sortir ?" % roue(secs), right, ["non" if right == "oui" else "oui", "on ne peut pas savoir", "seulement la première fois"],
                   ("Les parts sont identiques : les couleurs sont <b>équiprobables</b>." if k == "eq" else "La part %s est plus grande : elle a plus de chances de sortir. Réponse : <b>non</b>." % COLM[cs[0]]))
    q, a, w = R.choice([("Une pièce est tombée 3 fois sur « pile ». Au 4e lancer, que se passe-t-il ?", "« pile » et « face » ont toujours autant de chances", ["« face » a plus de chances", "« pile » a plus de chances", "« face » est certain"]),
                        ("Un sac contient 1 boule rouge et 9 bleues. Il y a deux couleurs. A-t-on une chance sur deux de tirer la rouge ?", "non, la rouge a moins de chances", ["oui, deux couleurs donc une chance sur deux", "non, la rouge est certaine", "oui, si on mélange bien"]),
                        ("Avec un dé normal, a-t-on plus de chances d’obtenir 6 que 1 ?", "non, autant de chances", ["oui", "non, 1 est plus probable", "cela dépend du lanceur"]),
                        ("Demain, il fera soit beau soit mauvais. Est-ce forcément une chance sur deux ?", "non, deux issues n’ont pas forcément la même chance", ["oui", "oui, comme une pièce", "non, c’est impossible"])])
    return mcq(q, a, w, "Réponse : <b>%s</b>." % a)


def s4_cm2():
    k = R.choice(["sac", "de", "roue"])
    if k == "sac":
        cs = R.sample(list(COL), 3)
        counts = {c: R.randint(1, 5) for c in cs}
        c = R.choice(cs)
        tot = sum(counts.values())
        return mcq("<div class='qfig'>%s</div>Quelle est la probabilité de tirer une boule %s ?" % (sac(counts), c), "%d chance%s sur %d" % (counts[c], "s" if counts[c] > 1 else "", tot),
                   ["%d chance%s sur %d" % (counts[c], "s" if counts[c] > 1 else "", len(cs)), "1 chance sur %d" % len(cs) if counts[c] != 1 else "1 chance sur 2", "%d chances sur %d" % (tot - counts[c], tot)],
                   "%d boules %ss sur %d boules : <b>%d chance%s sur %d</b>." % (counts[c], c, tot, counts[c], "s" if counts[c] > 1 else "", tot))
    if k == "de":
        f = R.choice([6, 8, 10, 12])
        ev = R.choice(["pair", "multiple de 3", "plus grand que 4", "plus petit que 3"])
        good = [x for x in range(1, f + 1) if (ev == "pair" and x % 2 == 0) or (ev == "multiple de 3" and x % 3 == 0) or (ev == "plus grand que 4" and x > 4) or (ev == "plus petit que 3" and x < 3)]
        n = len(good)
        return mcq("On lance un dé à %d faces (1 à %d). Quelle est la probabilité d’obtenir un nombre %s ?" % (f, f, ev), "%d chance%s sur %d" % (n, "s" if n > 1 else "", f),
                   ["%d chances sur %d" % (f - n, f) if f - n != n else "%d chances sur %d" % (n + 1, f), "1 chance sur 2" if n * 2 != f else "1 chance sur %d" % f, "%d chance%s sur 6" % (n, "s" if n > 1 else "") if f != 6 else "%d chances sur 12" % n],
                   "Les issues favorables sont %s : <b>%d chance%s sur %d</b>." % (", ".join(map(str, good)), n, "s" if n > 1 else "", f))
    secs = [(c, R.randint(1, 3)) for c in R.sample(list(COL), 3)]
    tot = sum(n for _, n in secs)
    c, n = R.choice(secs)
    return mcq("<div class='qfig'>%s</div>La roue a %d parts égales. Quelle est la probabilité d’obtenir %s ?" % (roue(secs), tot, "le " + COLM[c]), "%d chance%s sur %d" % (n, "s" if n > 1 else "", tot),
               ["1 chance sur 3" if n != 1 or tot != 3 else "1 chance sur 2", "%d chances sur %d" % (tot - n, tot) if tot - n != n else "%d chances sur %d" % (n + 1, tot), "%d chance%s sur 3" % (n, "s" if n > 1 else "") if tot != 3 else "%d chances sur 4" % n],
               "%d part%s %s sur %d parts égales : <b>%d chance%s sur %d</b>." % (n, "s" if n > 1 else "", COLM[c], tot, n, "s" if n > 1 else "", tot))


def s4():
    return s4_cm1() if L == 1 else s4_cm2()


def somme():
    t = R.randint(3, 11)
    pairs = [(a, t - a) for a in range(1, 7) if 1 <= t - a <= 6]
    n = len(pairs)
    return mcq("On lance deux dés à 6 faces (un rouge, un bleu). Combien d’issues donnent une somme égale à %d ?" % t, str(n), [str(n + 1), str(n - 1) if n > 1 else "2", str(t)] if t != n + 1 else [str(n + 2), str(n - 1), "36"],
               "Dans le tableau 6 %s 6, on cherche les cases de somme %d : %s. Il y en a <b>%d</b>." % (FOIS, t, ", ".join("(%d ; %d)" % pq for pq in pairs), n))


def s5():
    if L == 1:
        cs = R.sample(list(COL), 2)
        a, b = R.randint(1, 6), R.randint(1, 6)
        k = R.choice(["plus", "ajout"])
        if k == "plus":
            if a == b:
                return None
            right = "plutôt %s" % cs[0] if a > b else "plutôt %s" % cs[1]
            return mcq("Un sac contient %s et %s. Si on tire une boule, quelle couleur obtiendra-t-on plus probablement ?" % (pl(a, cs[0]), pl(b, cs[1])), right,
                       ["plutôt %s" % (cs[1] if right.endswith(cs[0]) else cs[0]), "les deux autant", "aucune des deux"], "Il y a plus de boules %ss : <b>%s</b>." % (cs[0] if a > b else cs[1], right))
        need = b - a + 1
        if need <= 0:
            return None
        return mcq("Un sac contient %s et %s. Combien de boules %ss faut-il ajouter, au minimum, pour que le %s soit plus probable que le %s ?" % (pl(a, cs[0]), pl(b, cs[1]), cs[0], COLM[cs[0]], COLM[cs[1]]),
                   str(need), [str(b - a), str(b), str(need + 1)], "Il faut plus de boules %ss que de %ss : %d + %d = %d &gt; %d. Réponse : <b>%d</b>." % (cs[0], cs[1], a, need, a + need, b, need))
    k = R.choice(["tab", "arbre", "indep", "event"])
    if k == "tab":
        a, b = R.choice([(2, 3), (3, 3), (2, 4), (3, 4), (2, 6)])
        return mcq("On lance une pièce (pile ou face) puis on tourne une roue à %d couleurs. Combien d’issues possibles ?" % b if a == 2 else
                   "On tire une boule dans un sac de %d couleurs, puis une dans un sac de %d couleurs. Combien d’issues possibles ?" % (a, b), str(a * b), [str(a + b), str(a * b - 1), str(a * b * 2)],
                   "Dans un tableau, %d lignes et %d colonnes : %d %s %d = <b>%d</b> issues." % (a, b, a, FOIS, b, a * b))
    if k == "arbre":
        return mcq("On lance deux fois une pièce. Combien d’issues donnent exactement un « pile » ?", "2 (PF et FP)", ["1", "3", "4"], "Les issues sont PP, PF, FP, FF. Exactement un pile : <b>PF et FP</b>.") if R.random() < 0.5 else \
            somme()
    if k == "indep":
        n = R.randint(3, 6)
        return mcq("Un dé est tombé %d fois de suite sur 6. Quelle est la probabilité d’obtenir 6 au lancer suivant ?" % n, "1 chance sur 6", ["presque 0", "1 chance sur %d" % (6 + n), "plus d’1 chance sur 6"],
                   "Le dé n’a pas de mémoire : chaque lancer est indépendant. Probabilité : <b>1 chance sur 6</b>.")
    f = 6
    ev = R.choice([("un nombre premier (2, 3, 5)", 3), ("un multiple de 2", 3), ("un nombre plus grand que 2", 4), ("un diviseur de 6", 4), ("7", 0)])
    return mcq("On lance un dé à 6 faces. Combien d’issues réalisent l’événement « obtenir %s » ?" % ev[0], str(ev[1]), [str(x) for x in (6 - ev[1], ev[1] + 1, 1) if x != ev[1]] + ["2"],
               "On liste les issues favorables : <b>%d</b>%s." % (ev[1], " (événement impossible)" if ev[1] == 0 else ""))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Expériences aléatoires et issues", mix(R, seen, [(s1, 20)])),
        ("Certain, possible, impossible", mix(R, seen, [(s2, 20)])),
        ("Comparer des chances", mix(R, seen, [(s3, 20)])),
        ("Équiprobabilité" if lv == 1 else "« a chances sur b »", mix(R, seen, [(s4, 20)])),
        ("Problèmes" if lv == 1 else "Deux étapes et indépendance", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Une expérience est <b>aléatoire</b> quand on connaît les issues possibles mais qu’on ne peut pas prévoir le résultat (lancer un dé, tirer une boule).",
         "Un événement peut être <b>certain</b>, <b>impossible</b> ou <b>possible</b> ; s’il est possible, il peut être <b>probable</b> ou <b>peu probable</b>.",
         "Deux issues n’ont pas forcément la même chance : 1 boule rouge et 9 bleues, ce n’est pas une chance sur deux."] +
        (["Si les issues ont toutes la même chance, la probabilité d’un événement se dit « a chances sur b » : 3 boules rouges sur 10 boules = 3 chances sur 10.",
          "Le hasard n’a pas de mémoire : après plusieurs « pile », « face » n’est pas plus probable."] if lv == 2 else []),
        [example("Sac de 3 rouges et 1 bleue", ["rouge : 3 sur 4", "bleue : 1 sur 4"], "rouge plus probable")],
        [["Croire qu’après 3 « pile », « face » est plus probable", "Chaque lancer est indépendant : toujours une chance sur deux."],
         ["Comparer le nombre de boules au lieu de la part", "3 rouges sur 4 est plus probable que 4 rouges sur 10."],
         ["Deux issues = une chance sur deux", "Seulement si les deux issues ont la même chance."]])
    faq = [("Que veut dire équiprobable ?", "Que toutes les issues ont la même chance : les faces d’un dé normal, les deux côtés d’une pièce."),
           ("Comment écrire une probabilité au CM2 ?", "Sous la forme « a chances sur b », par exemple 2 chances sur 6.")]
    unit(lv, R, "probabilites", "D",
         ("Identifier des expériences aléatoires et toutes les issues possibles ; utiliser le vocabulaire approprié ; comparer des issues ou des évènements selon leur probabilité ; comprendre que deux issues n’ont pas forcément une chance sur deux ; reconnaître l’équiprobabilité" if lv == 1 else
          "Identifier toutes les issues possibles et celles qui réalisent un évènement ; exprimer une probabilité sous la forme « a chances sur b » ; comparer des probabilités ; comprendre l’indépendance ; recenser les issues d’une expérience en deux étapes (tableau, arbre)"),
         "Les probabilités", "Probabilités",
         "Fiches de maths %s sur les probabilités : expériences aléatoires, issues, certain, possible, impossible, comparer des chances%s. 100 exercices corrigés." % (GN(lv), ", équiprobabilité" if lv == 1 else ", « a chances sur b », expériences en deux étapes"),
         "Aléatoire : on ne peut pas prévoir le résultat.", "Deux issues ne veulent pas dire une chance sur deux.",
         body, faq, sets, 25)


if __name__ == "__main__":
    build(1)
