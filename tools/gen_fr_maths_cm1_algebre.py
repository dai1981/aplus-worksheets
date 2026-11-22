# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Égalités à trous, programmes de calcul et suites (algèbre)
  python3 tools/gen_fr_maths_cm1_algebre.py
Calculs avec parenthèses (CM2 : deux paires), nombre manquant dans une égalité à trous ou représenté par un symbole,
programmes de calcul (exécuter ; CM2 : retrouver le nombre de départ), suites de nombres et de motifs, problèmes algébriques
(schéma en barres, balance).
Erreurs : ignorer les parenthèses, 345 + … = 1 000 → 1 345, appliquer les étapes du programme dans le désordre.
"""
import random
from fr_c2 import que
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, wrap, FILL, GREEN, INK, text

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52113 + 100 * lv)
    K = Kids(R)


def s1():
    a, b, c = R.randint(2, 30), R.randint(2, 20), R.randint(2, 9)
    k = R.choice(["p1", "p2", "p3"] + (["p4", "p5"] if L == 2 else []))
    if k == "p1":
        r, w = (a + b) * c, a + b * c
        q = "(%d + %d) %s %d" % (a, b, FOIS, c)
    elif k == "p2":
        if a <= b:
            a, b = b + 5, a
        r, w = (a - b) * c, a - b * c
        q = "(%d − %d) %s %d" % (a, b, FOIS, c)
    elif k == "p3":
        r, w = a + b * c, (a + b) * c
        q = "%d + (%d %s %d)" % (a, b, FOIS, c)
    elif k == "p4":
        d = R.randint(2, 9)
        r, w = (a + b) * (c + d), a + b * c + d
        q = "(%d + %d) %s (%d + %d)" % (a, b, FOIS, c, d)
    else:
        d = R.randint(2, 9)
        if a * c <= b * d:
            return None
        r, w = a * c - b * d, a * (c - b) * d if c > b else (a * c - b) * d
        q = "(%d %s %d) − (%d %s %d)" % (a, FOIS, c, b, FOIS, d)
    if w == r or w <= 0:
        return None
    return mcq("Calcule : %s" % q, num(r), [num(w), num(r + c), num(r - 1)], "On calcule d’abord ce qui est entre parenthèses : %s = <b>%s</b>." % (q, num(r)))


def s2():
    k = R.choice(["add", "sub", "mul", "div", "sub2"])
    sym = R.choice(["…", "■", "?"] if L == 1 else ["…", "■", "<i>n</i>"])
    if k == "add":
        t = R.choice([100, 1000, 500, 250]) if L == 1 else R.choice([1000, 10000, 2500, 100000])
        a = R.randint(t // 10, t - 1)
        return mcq("Trouve le nombre manquant : %s + %s = %s" % (num(a), sym, num(t)), num(t - a), [num(t + a), num(t - a + 10), num(t - a - 1)],
                   "On cherche ce qui manque à %s pour aller à %s : %s − %s = <b>%s</b>." % (num(a), num(t), num(t), num(a), num(t - a)))
    if k == "sub":
        a, r = R.randint(100, 999), R.randint(10, 99)
        return mcq("Trouve le nombre manquant : %s − %s = %d" % (num(a), sym, r), num(a - r), [num(a + r), num(a - r + 10), num(r)],
                   "%s − %s = %d, donc %s = %s − %d = <b>%s</b>." % (num(a), sym, r, sym, num(a), r, num(a - r)))
    if k == "sub2":
        b, r = R.randint(10, 300), R.randint(10, 500)
        return mcq("Trouve le nombre manquant : %s − %d = %d" % (sym, b, r), num(b + r), [num(r - b) if r > b else num(b - r), num(b + r + 10), num(r)],
                   "Le nombre de départ moins %d donne %d : %s = %d + %d = <b>%s</b>." % (b, r, sym, r, b, num(b + r)))
    if k == "mul":
        a, b = R.randint(3, 12), R.randint(3, 25)
        return mcq("Trouve le nombre manquant : %d %s %s = %d" % (a, FOIS, sym, a * b), num(b), [num(a * b - a), num(a * b * a) if a * a * b < 2000 else num(b + 1), num(b + 2)],
                   "%d %s %s = %d, donc %s = %d %s %d = <b>%d</b>." % (a, FOIS, sym, a * b, sym, a * b, DIV, a, b))
    a, b = R.randint(3, 9), R.randint(3, 20)
    return mcq("Trouve le nombre manquant : %s %s %d = %d" % (sym, DIV, a, b), num(a * b), [num(b // a) if b % a == 0 else num(b + a), num(b), num(a * b + a)],
               "%s = %d %s %d = <b>%d</b>." % (sym, b, FOIS, a, a * b))


OPS = [("ajoute", "+"), ("enlève", "−"), ("multiplie par", FOIS)]


def run(x, steps):
    for o, v in steps:
        x = x + v if o == "+" else x - v if o == "−" else x * v
    return x


def s3():
    n = R.randint(2, 3)
    steps = []
    for _ in range(n):
        w, o = R.choice(OPS)
        v = R.randint(2, 9) if o == FOIS else R.randint(2, 15)
        steps.append((o, v, w))
    st = [(o, v) for o, v, _ in steps]
    txt = " ; ".join("%s %d" % (w, v) for _, v, w in steps)
    x = R.randint(3, 20)
    r = run(x, st)
    if r <= 0 or any(run(x, st[:i]) <= 0 for i in range(1, n + 1)):
        return None
    if L == 2 and R.random() < 0.45:
        inv = x
        back = " ; ".join("%s %d" % ({"+": "enlève", "−": "ajoute", FOIS: "divise par"}[o], v) for o, v in st[::-1])
        return mcq("Programme : « Choisis un nombre ; %s. » On obtient %s. Quel était le nombre de départ ?" % (txt.lower() if False else txt, num(r)), num(inv),
                   [num(run(r, st)), num(inv + 1), num(abs(r - sum(v for _, v in st)))],
                   "On remonte le programme en faisant les opérations inverses, dans l’ordre inverse : %s. On trouve <b>%s</b>." % (back, num(inv)))
    rev = run(x, st[::-1])
    return mcq("Programme : « Choisis un nombre ; %s. » Quel résultat obtient-on en choisissant %d ?" % (txt, x), num(r), [num(rev) if rev != r else num(r + 1), num(r + st[-1][1]), num(r - 1)],
               "On fait les étapes dans l’ordre : %s → <b>%s</b>." % (" → ".join(num(run(x, st[:i])) for i in range(0, n + 1)), num(r)))


def motif_svg(a, b, steps=3):
    """motif évolutif : à l’étape n, a + b × n carrés en ligne (une rangée par étape)"""
    q = 14
    s = []
    y = 6
    for n in range(1, steps + 1):
        c = a + b * n
        for i in range(c):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s'/>" % (70 + i * q, y, q - 2, q - 2, FILL, GREEN))
        s.append(text(34, y + 11, "étape %d" % n, 11, weight=600))
        y += q + 10
    W = 80 + (a + b * steps) * q
    return wrap(W, y, "".join(s), "motif évolutif sur %d étapes" % steps, lg=True)


def s4():
    if R.random() < 0.55:
        a = R.randint(1, 50 if L == 1 else 500)
        b = R.choice([3, 4, 5, 6, 7, 9, 11, 12, 15, 25])
        if R.random() < 0.3:
            seq = [a * 2 ** i for i in range(5)]
            rule = "on multiplie par 2"
        elif R.random() < 0.5 and a > 4 * b + 10:
            seq = [a + 5 * b - b * i for i in range(5)]
            rule = "on enlève %d" % b
        else:
            seq = [a + b * i for i in range(5)]
            rule = "on ajoute %d" % b
        nxt = seq[-1] * 2 if "multiplie" in rule else seq[-1] + (seq[1] - seq[0])
        if nxt <= 0:
            return None
        return mcq("Quel nombre vient ensuite : %s ; … ?" % " ; ".join(num(x) for x in seq), num(nxt), [num(seq[-1] + (seq[1] - seq[0]) * 2), num(seq[-1] + 1), num(seq[-1] * 2) if "multiplie" not in rule else num(seq[-1] + seq[-2])],
                   "La règle : %s. Le nombre suivant est <b>%s</b>." % (rule, num(nxt)))
    a, b = R.randint(0, 3), R.randint(2, 4)
    n = R.choice([5, 6, 8, 10]) if L == 1 else R.choice([10, 12, 15, 20, 25])
    r = a + b * n
    return mcq("<div class='qfig'>%s</div>Combien de carrés y aura-t-il à l’étape %d ?" % (motif_svg(a, b), n), num(r), [num(a + b * (n + 1)), num(b * n), num(a + b + n)],
               "À chaque étape, on ajoute %d carrés. À l’étape %d : %d + %d %s %d = <b>%d</b>." % (b, n, a, b, FOIS, n, r) if a else
               "À chaque étape, il y a %d carrés de plus : à l’étape %d, %d %s %d = <b>%d</b>." % (b, n, b, FOIS, n, r))


def s5():
    p, o = K.two()
    k = R.choice(["plus", "fois", "balance", "deux"])
    if k == "plus":
        d, x = R.randint(4, 30), R.randint(10, 60)
        t = 2 * x + d
        return mcq("%s et %s ont %d billes en tout. %s en a %d de plus %s. Combien %s en a-t-%s ?" % (p[0], o[0], t, o[0], d, que(p[0]), p[0], p[1]), str(x), [str(t // 2), str(x + d), str(t - d)],
                   "Schéma en barres : on enlève les %d billes en plus : %d − %d = %d, puis on partage en 2 : <b>%d</b>." % (d, t, d, t - d, x))
    if k == "fois":
        f, x = R.randint(2, 5), R.randint(5, 40)
        t = x * (f + 1)
        return mcq("%s et %s ont %d € en tout. %s a %d fois plus d’argent %s. Combien %s a-t-%s ?" % (p[0], o[0], t, o[0], f, que(p[0]), p[0], p[1]), "%d €" % x, ["%d €" % (t // f), "%d €" % (t // 2), "%d €" % (x * f)],
                   "%s = 1 part, %s = %d parts : %d parts en tout. %d %s %d = <b>%d €</b>." % (p[0], o[0], f, f + 1, t, DIV, f + 1, x))
    if k == "balance":
        n, m, c = R.randint(2, 5), R.randint(1, 4), R.choice([50, 100, 200])
        x = R.randint(2, 9) * 50
        tot = n * x
        return mcq("Sur une balance en équilibre : %d boîtes identiques d’un côté, %s g de l’autre. Combien pèse une boîte ?" % (n, num(tot)), "%s g" % num(x), ["%s g" % num(tot - n), "%s g" % num(tot * n), "%s g" % num(x + 50)],
                   "%d boîtes = %s g, donc 1 boîte = %s %s %d = <b>%s g</b>." % (n, num(tot), num(tot), DIV, n, num(x)))
    a, b = R.randint(2, 9), R.randint(10, 30)
    t = 2 * a + 3 * b if False else None
    pr = R.randint(2, 9)
    return mcq("3 cahiers et 1 classeur coûtent %d €. Le classeur coûte %d €. Combien coûte un cahier ?" % (3 * pr + b, b), "%d €" % pr, ["%d €" % ((3 * pr + b) // 3), "%d €" % (3 * pr), "%d €" % (pr + 1)],
               "%d − %d = %d € pour 3 cahiers ; %d %s 3 = <b>%d €</b>." % (3 * pr + b, b, 3 * pr, 3 * pr, DIV, pr))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Calculs avec parenthèses", mix(R, seen, [(s1, 20)])),
        ("Égalités à trous", mix(R, seen, [(s2, 20)])),
        ("Programmes de calcul", mix(R, seen, [(s3, 20)])),
        ("Suites de nombres et de motifs", mix(R, seen, [(s4, 20)])),
        ("Problèmes algébriques", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Dans un calcul avec <b>parenthèses</b>, on commence par ce qui est entre parenthèses : (12 + 8) %s 3 = 20 %s 3 = 60." % (FOIS, FOIS),
         "Pour une <b>égalité à trous</b>, on utilise l’opération inverse : 345 + … = 1 000, donc … = 1 000 − 345 = 655.",
         "Un <b>programme de calcul</b> se fait étape par étape, dans l’ordre." + (" Pour retrouver le nombre de départ, on fait les opérations inverses en partant de la fin." if lv == 2 else ""),
         "Pour une suite, on cherche la <b>règle</b> : ce qu’on ajoute, enlève ou multiplie à chaque fois."],
        [example("Choisis 7 ; ajoute 5 ; multiplie par 3", ["7 + 5 = 12", "12 %s 3 = 36" % FOIS], "36"),
         example("Léa et Tom ont 54 billes ; Tom en a 12 de plus", ["54 − 12 = 42", "42 ÷ 2 = 21"], "Léa 21, Tom 33")],
        [["Ignorer les parenthèses : (12 + 8) %s 3 = 12 + 24" % FOIS, "On calcule d’abord 12 + 8 = 20."],
         ["345 + … = 1 000 → 1 345", "On cherche ce qui manque : 1 000 − 345 = 655."],
         ["Changer l’ordre des étapes du programme", "Ajouter 5 puis multiplier par 3 ne donne pas la même chose que l’inverse."]])
    faq = [("Pourquoi utiliser un schéma en barres ?", "Il montre les parts connues et inconnues, et aide à choisir les calculs."),
           ("Utilise-t-on des lettres ?", "Parfois un symbole ou une lettre remplace le nombre inconnu ; le calcul avec les lettres viendra au collège.")]
    unit(lv, R, "egalites-a-trous-et-programmes-de-calcul", "N",
         "Effectuer un calcul avec des parenthèses ; trouver le nombre manquant dans une égalité à trous ; exécuter%s un programme de calcul ; identifier et formuler une règle pour poursuivre une suite de nombres ou de motifs ; résoudre des problèmes algébriques" % ("" if lv == 1 else " ou produire"),
         "Égalités à trous, programmes de calcul et suites", "Égalités à trous et programmes de calcul",
         "Fiches de maths %s : calculs avec parenthèses, égalités à trous, programmes de calcul, suites de nombres et de motifs, problèmes avec schéma en barres. 100 exercices corrigés." % GN(lv),
         "On calcule d’abord entre parenthèses.", "Pour un nombre manquant, on utilise l’opération inverse.",
         body, faq, sets, 13)


if __name__ == "__main__":
    build(1)
