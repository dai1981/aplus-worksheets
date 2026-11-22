# -*- coding: utf-8 -*-
"""
France Maths 5e : Probabilités (vocabulaire, équiprobabilité, échelle, fréquences)
  python3 tools/gen_fr_maths_5e_probabilites.py
Erreurs : probabilité > 1, compter les issues favorables mais oublier le total, confondre fréquence observée et probabilité.
"""
import random
from fr_c4 import *

R = random.Random(60219)
K = Kids(R)
COUL = [("rouge", "rouges"), ("bleue", "bleues"), ("verte", "vertes"), ("jaune", "jaunes"), ("noire", "noires"), ("blanche", "blanches")]


def urne():
    cs = R.sample(COUL, R.choice([2, 3]))
    ns = [R.randint(1, 9) for _ in cs]
    return cs, ns


def desc(cs, ns):
    parts = ["%d boule%s %s" % (n, "s" if n > 1 else "", c[1] if n > 1 else c[0]) for c, n in zip(cs, ns)]
    return ", ".join(parts[:-1]) + " et " + parts[-1]


def s1():
    k = R.choice(["issues", "issues", "voc", "nb"])
    if k == "voc":
        V = [("On lance un dé à 6 faces. « Obtenir 7 » est un événement…", "impossible", ["certain", "probable", "équiprobable"]),
             ("On lance un dé à 6 faces. « Obtenir un nombre inférieur à 7 » est un événement…", "certain", ["impossible", "peu probable", "équiprobable"]),
             ("On lance une pièce équilibrée. Les issues « pile » et « face » sont…", "équiprobables", ["impossibles", "certaines", "de probabilités 1 et 0"]),
             ("Quelle probabilité a un événement impossible ?", "0", ["1", "0,5", "−1"]),
             ("Quelle probabilité a un événement certain ?", "1", ["0", "100", "0,5"]),
             ("Quel nombre ne peut pas être une probabilité ?", "1,2", ["0", "0,7", "1"]),
             ("Quel nombre ne peut pas être une probabilité ?", "−0,3", ["0,3", fr(1, 3), "1"]),
             ("On tire une carte dans un jeu de 32 cartes. Combien y a-t-il d’issues possibles ?", "32", ["4", "8", "1"]),
             ("On fait tourner une roue partagée en 8 secteurs égaux numérotés de 1 à 8. Les issues sont-elles équiprobables ?", "oui", ["non", "seulement pour le 1", "on ne peut pas savoir"])]
        q, a, w = R.choice(V)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    if k == "nb":
        n = R.choice([4, 6, 8, 10, 12, 20])
        return M("On lance un dé équilibré à %d faces numérotées de 1 à %d. Combien y a-t-il d’issues possibles ?" % (n, n), str(n), [str(n - 1), "1", str(2 * n)],
                 "Chaque face est une issue : <b>%d</b>." % n)
    n = R.choice([6, 8, 10, 12])
    ev, f = R.choice([("obtenir un nombre pair", lambda x: x % 2 == 0), ("obtenir un nombre impair", lambda x: x % 2 == 1),
                      ("obtenir un multiple de 3", lambda x: x % 3 == 0), ("obtenir un nombre supérieur à 4", lambda x: x > 4),
                      ("obtenir un nombre inférieur ou égal à 3", lambda x: x <= 3), ("obtenir un diviseur de %d" % n, lambda x: n % x == 0)])
    iss = [x for x in range(1, n + 1) if f(x)]
    return M("Dé à %d faces (1 à %d). Combien d’issues réalisent l’événement « %s » ?" % (n, n, ev), str(len(iss)), [str(len(iss) + 1), str(n - len(iss)) if n - len(iss) != len(iss) else str(len(iss) - 1), str(n)],
             "Les issues favorables sont %s : <b>%d</b>." % (", ".join(map(str, iss)), len(iss)))


def s2():
    cs, ns = urne()
    tot = sum(ns)
    i = R.randrange(len(cs))
    p = Fr(ns[i], tot)
    if len(set(ns)) < len(ns) and R.random() < 0.5:
        return None
    return M("Une urne contient %s. On tire une boule au hasard. Quelle est la probabilité d’obtenir une boule %s ?" % (desc(cs, ns), cs[i][0]), fq(p),
             [fr(ns[i], tot - ns[i]) if tot - ns[i] != ns[i] else fr(1, len(cs) + 1), fr(1, len(cs)) if Fr(1, len(cs)) != p else fr(ns[i], 10), fq(1 - p) if 1 - p != p else fr(ns[i] + 1, tot)],
             "Issues favorables ÷ issues possibles = %s%s." % (fr(ns[i], tot), "" if Fr(ns[i], tot).numerator == ns[i] else " = <b>%s</b>" % fq(p)) if Fr(ns[i], tot).numerator != ns[i] else "Issues favorables ÷ issues possibles = <b>%s</b>." % fq(p))


def s3():
    k = R.choice(["dec", "pc", "contr", "ech"])
    if k == "ech":
        V = [(fr(1, 2), "une chance sur deux"), ("0,9", "très probable"), ("0,1", "peu probable"), ("0", "impossible"), ("1", "certain")]
        a, b = R.choice(V)
        opts = [x[1] for x in V if x[1] != b]
        R.shuffle(opts)
        return M("Un événement a une probabilité de %s. Comment le décrire ?" % a, b, opts[:3], "Sur l’échelle de 0 à 1 : <b>%s</b>." % b)
    n = R.choice([4, 5, 8, 10, 20, 25])
    m = R.randint(1, n - 1)
    p = Fr(m, n)
    if k == "dec":
        return M("La probabilité d’un événement est %s. Écris-la en écriture décimale." % fr(m, n), d(p), [d(Fr(m, 10)) if Fr(m, 10) != p else d(p + Fr(1, 10)), d(1 - p) if 1 - p != p else "0,05", "%d,%d" % (m, n)],
                 "%d ÷ %d = <b>%s</b>." % (m, n, d(p)))
    if k == "pc":
        return M("La probabilité d’un événement est %s. Écris-la en pourcentage." % d(p), "%s %%" % d(p * 100), ["%s %%" % d(p), "%s %%" % d((1 - p) * 100) if p != Fr(1, 2) else "5 %", "%s %%" % d(p * 10)],
                 "%s = %s/100 = <b>%s %%</b>." % (d(p), d(p * 100), d(p * 100)))
    return M("La probabilité qu’il pleuve demain est %s. Quelle est la probabilité qu’il ne pleuve pas ?" % d(p), d(1 - p), [d(p), d(1 - p + Fr(1, 10)) if 1 - p + Fr(1, 10) <= 1 else "0", d(1 + p)],
             "Les deux probabilités ont pour somme 1 : 1 − %s = <b>%s</b>." % (d(p), d(1 - p)))


def s4():
    n = R.choice([50, 100, 200, 500, 1000])
    face = R.randint(1, 6)
    m = R.randint(n // 8, n // 4)
    k = R.choice(["freq", "freq", "compare", "grand"])
    if k == "freq":
        return M("On lance un dé %s fois ; le %d sort %s fois. Quelle est la fréquence d’apparition du %d ?" % (num(n), face, num(m), face), d(Fr(m, n)),
                 [fr(1, 6), d(Fr(m, 100)) if n != 100 else d(Fr(m, 1000)), num(m)], "Fréquence = %s ÷ %s = <b>%s</b>." % (num(m), num(n), d(Fr(m, n))))
    if k == "compare":
        return M("On lance un dé équilibré %s fois ; le %d sort %s fois. La probabilité d’obtenir %d est-elle égale à cette fréquence ?" % (num(n), face, num(m), face),
                 "non, elle vaut %s ; la fréquence s’en approche quand on fait beaucoup de lancers" % fr(1, 6),
                 ["oui, c’est exactement la probabilité", "non, la probabilité vaut %s" % d(Fr(m, n) * 2), "on ne peut pas connaître la probabilité"],
                 "Probabilité théorique : %s. La fréquence observée varie d’une série à l’autre." % fr(1, 6))
    V = [("Avec une pièce équilibrée, sur 10 lancers, on obtient 7 piles. Que peut-on dire ?", "c’est possible : sur peu de lancers, la fréquence peut s’éloigner de 0,5", ["la pièce est forcément truquée", "la probabilité de pile est 0,7", "le prochain lancer sera face"]),
         ("Sur un très grand nombre de lancers d’une pièce équilibrée, vers quelle valeur la fréquence de « pile » se rapproche-t-elle ?", "0,5", ["0", "1", "0,7"]),
         ("Une pièce a donné 5 fois « face » de suite. Quelle est la probabilité d’obtenir « face » au lancer suivant ?", "0,5", ["0", "1", "moins de 0,5"]),
         ("Sur 1 000 lancers d’une punaise, elle tombe 620 fois sur le dos. Quelle valeur peut-on prendre comme estimation de la probabilité qu’elle tombe sur le dos ?", "0,62", ["0,5", "620", "0,38"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s5():
    k = R.choice(["roue", "sac", "cartes", "choix"])
    p = K.next()
    if k == "roue":
        n = R.choice([8, 10, 12])
        a = R.randint(1, n // 2)
        b = R.randint(1, n - a - 1)
        c = n - a - b
        pa = Fr(c, n)
        return M("Une roue a %d secteurs égaux : %s, %s et les autres verts. Quelle est la probabilité de tomber sur un secteur vert ?" % (n, pl(a, "rouge"), pl(b, "bleu")), fq(pa),
                 [fq(Fr(c, a + b)) if a + b != c else fr(1, 3), fr(1, 3) if Fr(1, 3) not in (pa, Fr(c, a + b)) else fr(1, 2), fq(Fr(a + b, n)) if Fr(a + b, n) != pa else fr(c + 1, n)],
                 "Il y a %d − %d − %d = %s : %s = <b>%s</b>." % (n, a, b, pl(c, "secteur vert", "secteurs verts"), fr(c, n), fq(pa)))
    if k == "sac":
        cs, ns = urne()
        if len(cs) != 2:
            return None
        tot = sum(ns)
        add = R.randint(1, 5)
        p0 = Fr(ns[0] + add, tot + add)
        return M("Un sac contient %s. %s ajoute %d boule%s %s. Quelle est maintenant la probabilité de tirer une boule %s ?" % (desc(cs, ns), p[0], add, "s" if add > 1 else "", cs[0][1] if add > 1 else cs[0][0], cs[0][0]),
                 fq(p0), [fr(ns[0] + add, tot) , fq(Fr(ns[0], tot)) if Fr(ns[0], tot) != p0 else fr(1, 2), fr(ns[0], tot + add)],
                 "Boules %s : %d ; total : %d. Probabilité : <b>%s</b>." % (cs[0][1], ns[0] + add, tot + add, fq(p0)))
    if k == "cartes":
        ev, m = R.choice([("un cœur", 8), ("un as", 4), ("une figure (valet, dame ou roi)", 12), ("une carte rouge", 16), ("le roi de pique", 1)])
        pp = Fr(m, 32)
        return M("On tire une carte au hasard dans un jeu de 32 cartes. Quelle est la probabilité de tirer %s ?" % ev, fq(pp), [fr(1, m) if m > 1 else fr(1, 4), fr(m, 52), fq(1 - pp)],
                 "%s sur 32 : <b>%s</b>." % (pl(m, "carte favorable", "cartes favorables"), fq(pp)))
    a1, t1 = R.randint(2, 6), R.randint(8, 15)
    a2, t2 = R.randint(2, 6), R.randint(8, 15)
    if Fr(a1, t1) == Fr(a2, t2) or (a1 > a2) == (Fr(a1, t1) > Fr(a2, t2)):
        return None
    best = "le sac A" if Fr(a1, t1) > Fr(a2, t2) else "le sac B"
    return M("Sac A : %d boules gagnantes sur %d. Sac B : %d boules gagnantes sur %d. %s veut gagner. Quel sac doit-%s choisir ?" % (a1, t1, a2, t2, p[0], p[1]), best,
             ["le sac B" if best == "le sac A" else "le sac A", "les deux sont pareils", "celui qui a le plus de boules"],
             "On compare %s et %s : <b>%s</b>. (Il ne suffit pas de compter les boules gagnantes.)" % (fr(a1, t1), fr(a2, t2), best))


def main():
    seen = set()
    sets = [("Issues et vocabulaire", mix(R, seen, [(s1, 20)])), ("Calculer une probabilité", mix(R, seen, [(s2, 20)])),
            ("Échelle, écritures et événement contraire", mix(R, seen, [(s3, 20)])), ("Fréquences et probabilités", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une <b>issue</b> est un résultat possible ; un <b>événement</b> est un ensemble d’issues.",
              "Quand les issues sont <b>équiprobables</b> : probabilité = nombre d’issues favorables ÷ nombre d’issues possibles.",
              "Une probabilité est toujours entre 0 (impossible) et 1 (certain). La probabilité de l’événement contraire est 1 − p."],
             [("Urne : 3 boules rouges et 5 bleues. P(rouge) ?", ["3 favorables", "3 + 5 = 8 possibles"], "3/8")],
             [["Diviser par le nombre de boules d’une autre couleur (3/5)", "On divise par le nombre total : 3/8."], ["Trouver une probabilité plus grande que 1", "Elle est toujours entre 0 et 1."],
              ["Croire qu’après 5 « face », « pile » est plus probable", "Chaque lancer est indépendant : la probabilité reste 0,5."]])
    faq = [("Fréquence et probabilité, c’est pareil ?", "Non : la fréquence est observée lors d’une expérience ; elle se rapproche de la probabilité quand le nombre d’essais est grand."),
           ("Comment écrire une probabilité ?", "En fraction, en décimal ou en pourcentage : 1/4 = 0,25 = 25 %.")]
    unit("5e", R, "probabilites", "D",
         "Utiliser le vocabulaire des probabilités (issue, événement, certain, impossible, équiprobable) ; calculer des probabilités dans des situations d’équiprobabilité ; placer une probabilité sur une échelle de 0 à 1 ; faire le lien entre fréquence observée et probabilité",
         "Probabilités", "Probabilités",
         "Fiches de maths 5e sur les probabilités : issues, événements, équiprobabilité, échelle de 0 à 1, événement contraire, fréquences. 100 exercices corrigés.",
         "Probabilité = issues favorables ÷ issues possibles", "Toujours entre 0 et 1", body, faq, sets, 19)


if __name__ == "__main__":
    main()
