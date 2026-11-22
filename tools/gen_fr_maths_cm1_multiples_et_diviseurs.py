# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Multiples et diviseurs (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_multiples_et_diviseurs.py
CM1 : multiples de 2, 5 et 10 ; multiples et diviseurs parmi les nombres jusqu’à 10.
CM2 : en plus, diviseurs d’un nombre jusqu’à 100, tous les diviseurs jusqu’à 30, diviseurs communs (≤ 30), multiples communs (&lt; 15).
Erreurs : croire qu’un nombre qui finit par 2 est multiple de 2 seulement s’il est petit, confondre multiple et diviseur,
oublier 1 et le nombre lui-même dans la liste des diviseurs.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52103 + 100 * lv)
    K = Kids(R)


def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def s1():
    d = R.choice([2, 5, 10])
    good = R.randint(30, 9999 if L == 1 else 99999) // d * d
    bad = set()
    while len(bad) < 3:
        x = good + R.choice([1, 2, 3, 4, 6, 7, 11, 13])
        if x % d:
            bad.add(x)
    allv = sorted(bad | {good})
    rule = {2: "son chiffre des unités est 0, 2, 4, 6 ou 8", 5: "son chiffre des unités est 0 ou 5", 10: "son chiffre des unités est 0"}[d]
    return mcq("Parmi %s, quel nombre est un multiple de %d ?" % (", ".join(num(v) for v in allv[:-1]) + " et " + num(allv[-1]), d), num(good), [num(v) for v in sorted(bad)],
               "Un nombre est multiple de %d quand %s : <b>%s</b>." % (d, rule, num(good)))


def s1b():
    n = R.randint(100, 9999) * 10 + R.choice([0, 0, 5, 2, 4, 6, 8, 1, 3])
    m2, m5, m10 = n % 2 == 0, n % 5 == 0, n % 10 == 0
    lab = lambda a, b, c: ", ".join(x for x, y in (("2", a), ("5", b), ("10", c)) if y) or "aucun des trois"
    right = lab(m2, m5, m10)
    opts = ["2, 5, 10", "2", "5", "aucun des trois", "2, 5", "10"]
    return mcq("%s est multiple de quels nombres parmi 2, 5 et 10 ?" % num(n), right, [o for o in opts if o != right],
               "Chiffre des unités : %d. Réponse : <b>%s</b>." % (n % 10, right))


def s2():
    d = R.randint(3, 9)
    q = R.randint(3, 12)
    yes = R.random() < 0.5
    n = d * q if yes else d * q + R.randint(1, d - 1)
    r = ("oui, car %d %s %d = %d" % (d, FOIS, q, n)) if yes else ("non, car %d %s %d = %d et il reste %d" % (d, FOIS, q, d * q, n - d * q))
    w = [("non, car %d est impair" % n) if n % 2 else ("non, car %d est pair" % n), ("oui, car %d %s %d = %d" % (d, FOIS, q + 1, d * (q + 1))) if not yes else ("non, car %d %s %d = %d" % (d, FOIS, q + 1, d * q + d)),
         "oui, car %d finit par %d" % (n, n % 10) if not yes else "non, car %d n’est pas dans la table de 2" % d]
    return mcq("%d est-il un multiple de %d ?" % (n, d), r, w, ("%d est dans la table de %d." % (n, d)) if yes else ("%d n’est pas dans la table de %d : la division ne tombe pas juste." % (n, d)) + " Réponse : <b>%s</b>." % r.split(",")[0])


def s3_cm1():
    n = R.choice([12, 18, 20, 24, 30, 36, 40, 42, 45, 48, 54, 56, 60, 63, 64, 72, 80, 81, 84, 90])
    ds = [d for d in range(2, 11) if n % d == 0]
    nd = [d for d in range(2, 11) if n % d]
    if not ds or len(nd) < 1:
        return None
    if R.random() < 0.5 and len(nd) >= 1 and len(ds) >= 3:
        x = R.choice(nd)
        opts = R.sample(ds, 3)
        return mcq("Lequel de ces nombres n’est pas un diviseur de %d : %s ?" % (n, ", ".join(map(str, sorted(opts + [x])))), str(x), [str(o) for o in opts],
                   "%d ÷ %d ne tombe pas juste ; les autres divisent %d. Réponse : <b>%d</b>." % (n, x, n, x))
    x = R.choice(ds)
    opts = R.sample(nd, min(3, len(nd)))
    return mcq("Lequel de ces nombres est un diviseur de %d : %s ?" % (n, ", ".join(map(str, sorted(opts + [x])))), str(x), [str(o) for o in opts],
               "%d = %d %s %d : <b>%d</b> est un diviseur de %d." % (n, x, FOIS, n // x, x, n))


def s3_cm2():
    n = R.choice([12, 16, 18, 20, 24, 28, 30, 15, 21, 27, 10, 14, 22, 26])
    k = R.choice(["liste", "nombre"])
    ds = divs(n)
    if k == "liste":
        f = lambda l: ", ".join(map(str, l))
        return mcq("Quels sont tous les diviseurs de %d ?" % n, f(ds), [f(ds[1:-1]), f(ds[:-1]), f([d for d in ds if d % 2 == 0] or ds[1:]) if [d for d in ds if d % 2 == 0] != ds else f(ds + [n * 2])],
                   "On cherche les paires : %s. Diviseurs : <b>%s</b>." % (", ".join("%d %s %d" % (d, FOIS, n // d) for d in ds if d * d <= n), f(ds)))
    return mcq("Combien de diviseurs a le nombre %d ?" % n, str(len(ds)), [str(len(ds) - 2), str(len(ds) - 1), str(len(ds) + 1)],
               "Les diviseurs de %d sont %s : il y en a <b>%d</b> (sans oublier 1 et %d)." % (n, ", ".join(map(str, ds)), len(ds), n))


def s3():
    return s3_cm1() if L == 1 or R.random() < 0.3 else s3_cm2()


def s4_cm1():
    t = R.randint(3, 9)
    lo = R.randint(2, 7) * 10
    hi = lo + 20
    ms = [m for m in range(lo, hi + 1) if m % t == 0]
    f = lambda l: ", ".join(map(str, l)) if l else "aucun"
    return mcq("Quels sont les multiples de %d compris entre %d et %d ?" % (t, lo, hi), f(ms), [f([m + 1 for m in ms]), f(ms[:-1]) if len(ms) > 1 else f([lo]), f([m for m in range(lo, hi + 1) if m % (t + 1) == 0])],
               "On cherche dans la table de %d : <b>%s</b>." % (t, f(ms)))


def s4_cm2():
    if R.random() < 0.5:
        a, b = R.sample([12, 18, 24, 30, 16, 20, 15, 27, 28, 21, 9, 6, 8, 10], 2)
        c = [d for d in divs(a) if b % d == 0]
        f = lambda l: ", ".join(map(str, l))
        return mcq("Quels sont les diviseurs communs de %d et %d ?" % (a, b), f(c), [f(c[1:]) if len(c) > 1 else f(c + [a]), f(sorted(set(divs(a)) | set(divs(b)))), f(c[:-1] + [c[-1] * 2]) if len(c) > 1 else f([1, 2])],
                   "Diviseurs de %d : %s. Diviseurs de %d : %s. Communs : <b>%s</b>." % (a, f(divs(a)), b, f(divs(b)), f(c)))
    a, b = R.sample(range(2, 15), 2)
    m = a * b // __import__("math").gcd(a, b)
    if m > 100:
        return None
    return mcq("Quel est le plus petit multiple commun de %d et %d (autre que 0) ?" % (a, b), str(m), [str(a * b) if a * b != m else str(m * 2), str(a + b), str(max(a, b) * 2) if max(a, b) * 2 != m else str(m + max(a, b))],
               "Multiples de %d : %s… ; de %d : %s… Le premier commun est <b>%d</b>." % (a, ", ".join(str(a * i) for i in range(1, m // a + 1)), b, ", ".join(str(b * i) for i in range(1, m // b + 1)), m))


def s4():
    return s4_cm1() if L == 1 else s4_cm2()


def s5():
    p = K.next()
    k = R.choice(["partage", "rangees", "bus"] + (["pgcd", "ppcm"] if L == 2 else ["paires"]))
    if k == "partage":
        d = R.randint(3, 9)
        n = d * R.randint(6, 15) + R.choice([0, 0, R.randint(1, d - 1)])
        ok = n % d == 0
        right = "oui, %d chacun" % (n // d) if ok else "non, il en reste %d" % (n % d)
        return mcq("%s veut partager %d cartes entre %d amis, sans reste. Est-ce possible ?" % (p[0], n, d), right,
                   ["oui, %d chacun" % (n // d + 1), "non, il en reste %d" % (d - n % d if not ok else 1), "oui, %d chacun" % (n // d) if not ok else "non, il en reste %d" % (d - 1)],
                   ("%d est un multiple de %d : %d ÷ %d = %d." % (n, d, n, d, n // d)) if ok else ("%d n’est pas un multiple de %d : %d %s %d = %d, il reste %d." % (n, d, d, FOIS, n // d, d * (n // d), n % d)))
    if k == "rangees":
        n = R.choice([24, 36, 30, 40, 48, 18, 20, 28])
        ds = [d for d in divs(n) if 1 < d < n]
        x = R.choice(ds)
        bad = [y for y in range(2, 11) if n % y]
        return mcq("Le maître range %d chaises en rangées égales, sans chaise en trop. Quel nombre de chaises par rangée est possible ?" % n, str(x), [str(b) for b in R.sample(bad, min(3, len(bad)))],
                   "%d = %d %s %d : %d est un diviseur de %d." % (n, x, FOIS, n // x, x, n))
    if k == "bus":
        a, b = R.choice([(2, 3), (3, 4), (2, 5), (4, 6), (3, 5), (6, 8)])
        m = a * b // __import__("math").gcd(a, b)
        return mcq("Un bus passe toutes les %d minutes, un tramway toutes les %d minutes. Ils partent ensemble à 8 h. Dans combien de minutes repartiront-ils ensemble ?" % (a * 5, b * 5),
                   "%d min" % (m * 5), ["%d min" % (a * b * 25) if a * b != m else "%d min" % (m * 10), "%d min" % ((a + b) * 5), "%d min" % (b * 5)],
                   "On cherche le premier multiple commun de %d et %d : <b>%d min</b>." % (a * 5, b * 5, m * 5))
    if k == "pgcd":
        a, b = R.choice([(12, 18), (16, 24), (20, 30), (18, 24), (15, 25), (24, 30), (12, 30), (14, 21), (18, 27)])
        g = __import__("math").gcd(a, b)
        return mcq("On fait des sachets identiques avec %d billes rouges et %d billes bleues, sans reste. Combien de sachets au plus ?" % (a, b), str(g), [str(a + b), str(min(a, b)), str(g // 2) if g > 2 else str(g + 1)],
                   "On cherche le plus grand diviseur commun de %d et %d : <b>%d</b>." % (a, b, g))
    if k == "ppcm":
        a, b = R.choice([(4, 6), (6, 8), (6, 9), (4, 10), (8, 12), (10, 12), (9, 12)])
        m = a * b // __import__("math").gcd(a, b)
        return mcq("Des boîtes de %d et des boîtes de %d crayons : quel est le plus petit nombre de crayons qu’on peut ranger exactement avec chaque sorte de boîte ?" % (a, b),
                   str(m), [str(a * b), str(a + b), str(max(a, b) + min(a, b) * 2) if max(a, b) + min(a, b) * 2 != m else str(m * 2)],
                   "C’est le plus petit multiple commun de %d et %d : <b>%d</b>." % (a, b, m))
    n = R.randint(21, 99)
    right = "oui" if n % 2 == 0 else "non, il reste un enfant seul"
    return mcq("%d enfants se mettent par deux. Tout le monde a-t-il un partenaire ?" % n, right, ["non, il reste un enfant seul" if n % 2 == 0 else "oui", "non, il manque deux enfants", "on ne peut pas savoir"],
               "%d est %s : %s." % (n, "pair (multiple de 2)" if n % 2 == 0 else "impair", "<b>oui</b>" if n % 2 == 0 else "<b>non</b>, il reste un enfant"))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Multiples de 2, 5 et 10", mix(R, seen, [(s1, 12), (s1b, 8)])),
        ("Est-ce un multiple ?", mix(R, seen, [(s2, 20)])),
        ("Les diviseurs", mix(R, seen, [(s3, 20)])),
        ("Multiples entre deux nombres" if lv == 1 else "Diviseurs et multiples communs", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["24 est un <b>multiple</b> de 6 car 24 = 6 %s 4. On dit aussi que 6 est un <b>diviseur</b> de 24 : 24 ÷ 6 tombe juste." % FOIS,
         "Multiple de 2 : chiffre des unités 0, 2, 4, 6 ou 8. Multiple de 5 : 0 ou 5. Multiple de 10 : 0.",
         "Pour trouver tous les diviseurs, on cherche les paires : 24 = 1 %s 24 = 2 %s 12 = 3 %s 8 = 4 %s 6." % (FOIS, FOIS, FOIS, FOIS)],
        [example("Les diviseurs de 18", ["1 %s 18, 2 %s 9, 3 %s 6" % (FOIS, FOIS, FOIS)], "1, 2, 3, 6, 9, 18")],
        [["Confondre multiple et diviseur", "Le multiple est le plus grand nombre (24), le diviseur est le plus petit (6)."],
         ["Oublier 1 et le nombre lui-même", "1 et 18 sont toujours des diviseurs de 18."],
         ["Regarder tout le nombre pour les multiples de 2", "Seul le chiffre des unités compte : 4 738 est pair."]])
    faq = [("Quel est le lien avec les tables ?", "Les multiples de 7 sont les nombres de la table de 7 : 7, 14, 21, 28…"),
           ("0 est-il un multiple de tous les nombres ?", "Oui : 0 = 7 %s 0. Mais on cherche en général les multiples non nuls." % FOIS)]
    unit(lv, R, "multiples-et-diviseurs", "N",
         ("Reconnaître les multiples de 2, de 5 et de 10 ; déterminer si un nombre est multiple ou diviseur d’un autre parmi les nombres inférieurs ou égaux à 10" if lv == 1 else
          "Déterminer si un nombre inférieur ou égal à 10 est diviseur d’un entier ; déterminer les diviseurs d’un nombre inférieur ou égal à 100 et tous les diviseurs d’un nombre jusqu’à 30 ; diviseurs communs et multiples communs"),
         "Multiples et diviseurs", "Multiples et diviseurs",
         "Fiches de maths %s sur les multiples et les diviseurs : multiples de 2, 5 et 10, tables, liste des diviseurs%s et problèmes. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", diviseurs et multiples communs"),
         "24 = 6 × 4 : 24 est un multiple de 6, et 6 un diviseur de 24.", "Multiple de 2 : 0, 2, 4, 6, 8 ; de 5 : 0, 5 ; de 10 : 0.",
         body, faq, sets, 3)


if __name__ == "__main__":
    build(1)
