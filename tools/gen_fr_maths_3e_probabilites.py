# -*- coding: utf-8 -*-
"""
France Maths 3e : Probabilités (tirages avec et sans remise, arbres pondérés, fréquences et loi des grands nombres)
  python3 tools/gen_fr_maths_3e_probabilites.py
Erreurs : garder le même dénominateur sans remise, additionner sur un chemin, croire qu’une fréquence observée est la probabilité exacte.
"""
import random
from fr_c4 import *

R = random.Random(60416)
K = Kids(R)
COUL = [("rouge", "rouges"), ("bleue", "bleues"), ("verte", "vertes"), ("jaune", "jaunes"), ("noire", "noires"), ("blanche", "blanches")]


def bo(cs, ns):
    p = ["%d boule%s %s" % (n, "s" if n > 1 else "", c[1] if n > 1 else c[0]) for c, n in zip(cs, ns)]
    return ", ".join(p[:-1]) + " et " + p[-1]


def s1():
    cs = R.sample(COUL, 2)
    a, b = R.randint(2, 6), R.randint(2, 6)
    t = a + b
    k = R.choice(["deuxA", "deuxA", "diff", "deuxB"])
    if k == "deuxA":
        p = Fr(a * (a - 1), t * (t - 1))
        return M("Une urne contient %s. On tire deux boules <b>sans remise</b>. Quelle est la probabilité de tirer deux boules %s ?" % (bo(cs, [a, b]), cs[0][1]), fq(p), [fq(Fr(a * a, t * t)), fq(Fr(a * (a - 1), t * t)), fq(Fr(2 * a, t)) if 2 * a < t else fq(Fr(a, t))],
                 "%s × %s = <b>%s</b> (au 2e tirage, il reste %d boules dont %d %s)." % (fr(a, t), fr(a - 1, t - 1), fq(p), t - 1, a - 1, cs[0][1] if a - 1 > 1 else cs[0][0]))
    if k == "deuxB":
        p = Fr(b * (b - 1), t * (t - 1))
        return M("Une urne contient %s. On tire deux boules sans remise. Quelle est la probabilité de tirer deux boules %s ?" % (bo(cs, [a, b]), cs[1][1]), fq(p), [fq(Fr(b * b, t * t)), fq(Fr(b * (b - 1), t * t)), fq(Fr(b, t))],
                 "%s × %s = <b>%s</b>." % (fr(b, t), fr(b - 1, t - 1), fq(p)))
    p = Fr(2 * a * b, t * (t - 1))
    return M("Une urne contient %s. On tire deux boules sans remise. Quelle est la probabilité d’obtenir deux couleurs différentes ?" % bo(cs, [a, b]), fq(p), [fq(Fr(a * b, t * (t - 1))), fq(Fr(2 * a * b, t * t)), fq(1 - p) if 1 - p != p else fq(p / 2)],
             "%s × %s + %s × %s = <b>%s</b>." % (fr(a, t), fr(b, t - 1), fr(b, t), fr(a, t - 1), fq(p)))


def s2():
    p1 = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(2, 5), Fr(3, 5), Fr(3, 10), Fr(7, 10)])
    p2 = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(1, 5), Fr(4, 5)])
    k = R.choice(["deux", "aumoins", "un"])
    if k == "deux":
        return M("Un joueur réussit son premier tir avec la probabilité %s et son second avec la probabilité %s (indépendamment). Quelle est la probabilité qu’il réussisse les deux ?" % (fq(p1), fq(p2)), fq(p1 * p2), [fq(p1 + p2) if p1 + p2 <= 1 else fq(Fr(1, 2) * p1), fq((1 - p1) * (1 - p2)), fq(p1 * p2 * 2) if p1 * p2 * 2 <= 1 else fq(p2)],
                 "Sur l’arbre, on multiplie le long du chemin : %s × %s = <b>%s</b>." % (fq(p1), fq(p2), fq(p1 * p2)))
    if k == "aumoins":
        p = 1 - (1 - p1) * (1 - p2)
        return M("Deux tirs indépendants réussissent avec les probabilités %s et %s. Quelle est la probabilité d’en réussir au moins un ?" % (fq(p1), fq(p2)), fq(p), [fq(p1 * p2), fq((1 - p1) * (1 - p2)), fq(p1 + p2) if p1 + p2 <= 1 and p1 + p2 != p else fq(1 - p1 * p2) if 1 - p1 * p2 != p else fq(p / 2)],
                 "Événement contraire : « aucun » a pour probabilité %s × %s = %s ; donc 1 − %s = <b>%s</b>." % (fq(1 - p1), fq(1 - p2), fq((1 - p1) * (1 - p2)), fq((1 - p1) * (1 - p2)), fq(p)))
    p = p1 * (1 - p2) + (1 - p1) * p2
    return M("Deux tirs indépendants réussissent avec les probabilités %s et %s. Quelle est la probabilité d’en réussir exactement un ?" % (fq(p1), fq(p2)), fq(p), [fq(p1 * (1 - p2)), fq(p1 * p2), fq(1 - p1 * p2) if 1 - p1 * p2 != p else fq(p / 2)],
             "Deux chemins : %s × %s + %s × %s = <b>%s</b>." % (fq(p1), fq(1 - p2), fq(1 - p1), fq(p2), fq(p)))


def s3():
    k = R.choice(["avec", "avec", "comp", "cartes"])
    if k == "avec":
        cs = R.sample(COUL, 2)
        a, b = R.randint(1, 6), R.randint(1, 6)
        t = a + b
        return M("Une urne contient %s. On tire une boule, on la <b>remet</b>, puis on en tire une seconde. Quelle est la probabilité de tirer deux boules %s ?" % (bo(cs, [a, b]), cs[0][1]), fq(Fr(a * a, t * t)),
                 [fq(Fr(a * (a - 1), t * (t - 1))) if a > 1 and Fr(a * (a - 1), t * (t - 1)) != Fr(a * a, t * t) else fq(Fr(a, t)), fq(Fr(2 * a, t)) if 2 * a < t else fq(Fr(a, 2 * t)), fq(Fr(a, t * t))],
                 "Avec remise, la composition ne change pas : %s × %s = <b>%s</b>." % (fr(a, t), fr(a, t), fq(Fr(a * a, t * t))))
    if k == "comp":
        V = [("On tire deux cartes d’un jeu de 32 cartes. La probabilité d’avoir deux as est-elle la même avec et sans remise ?", "non : sans remise, elle est plus petite", ["oui, toujours", "non : sans remise, elle est plus grande", "on ne peut pas savoir"]),
             ("Dans un arbre de probabilités, la somme des probabilités des branches issues d’un même nœud vaut…", "1", ["0", "la probabilité du chemin", "2"]),
             ("Pour obtenir la probabilité d’un chemin dans un arbre, on…", "multiplie les probabilités des branches", ["additionne les probabilités des branches", "prend la plus grande branche", "divise par le nombre de branches"]),
             ("Pour obtenir la probabilité d’un événement formé de plusieurs chemins, on…", "additionne les probabilités des chemins", ["multiplie les probabilités des chemins", "prend le chemin le plus probable", "compte les chemins"])]
        q, a, w = R.choice(V)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    ev, n, m = R.choice([("deux cœurs", 8, 32), ("deux rois", 4, 32), ("deux cartes rouges", 16, 32), ("deux figures", 12, 32)])
    p = Fr(n * (n - 1), m * (m - 1))
    return M("On tire successivement deux cartes sans remise dans un jeu de 32 cartes. Quelle est la probabilité d’obtenir %s ?" % ev, fq(p), [fq(Fr(n * n, m * m)), fq(Fr(n, m)), fq(Fr(2 * n, m)) if 2 * n < m else fq(Fr(n - 1, m - 1))],
             "%s × %s = <b>%s</b>." % (fr(n, m), fr(n - 1, m - 1), fq(p)))


def s4():
    k = R.choice(["freq", "freq", "lgn", "estim"])
    if k == "freq":
        n = R.choice([50, 100, 200, 500, 1000])
        m = R.randint(n // 5, n // 2)
        return M("On lance une punaise %s fois ; elle tombe %s fois sur la pointe. Quelle est la fréquence de « pointe » ?" % (num(n), num(m)), d(Fr(m, n)), [d(Fr(n - m, n)), fr(1, 2), num(m)],
                 "%s ÷ %s = <b>%s</b>." % (num(m), num(n), d(Fr(m, n))))
    if k == "lgn":
        V = [("Quand on répète une expérience un très grand nombre de fois, la fréquence d’un événement…", "se rapproche de sa probabilité", ["devient égale à 1", "s’éloigne de sa probabilité", "reste toujours la même"]),
             ("Sur 20 lancers d’un dé équilibré, le 6 sort 7 fois. Le dé est-il forcément truqué ?", "non : sur peu de lancers, la fréquence peut s’éloigner de 1/6", ["oui, car 7/20 ≠ 1/6", "oui, le 6 sort trop souvent", "non, car 7 est impair"]),
             ("Pour estimer une probabilité inconnue (punaise, pièce truquée), on…", "répète l’expérience un grand nombre de fois et on calcule la fréquence", ["fait un seul essai", "prend toujours 1/2", "compte les faces"])]
        q, a, w = R.choice(V)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    p = R.choice([Fr(1, 5), Fr(1, 4), Fr(3, 10), Fr(2, 5)])
    n = R.choice([200, 500, 1000, 2000])
    return M("Un jeu est gagnant avec la probabilité %s. Sur %s parties, combien de parties gagnantes peut-on espérer environ ?" % (d(p), num(n)), num(p * n), [num(p * 100), num(n - p * n), num(p * n * 2)],
             "%s × %s = <b>%s</b> (environ)." % (d(p), num(n), num(p * n)))


def s5():
    k = R.choice(["test", "code", "equite", "chaussettes"])
    p = K.next()
    if k == "test":
        a = R.choice([Fr(1, 10), Fr(1, 5)])
        s_ = R.choice([Fr(9, 10), Fr(4, 5)])
        pp = a * s_
        return M("Dans une classe, %s des élèves font du théâtre. Parmi eux, %s font aussi de la musique. On choisit un élève au hasard. Quelle est la probabilité qu’il fasse théâtre et musique ?" % (fq(a), fq(s_)), fq(pp), [fq(a + s_) if a + s_ < 1 else fq(s_), fq(s_), fq(a * (1 - s_))],
                 "%s × %s = <b>%s</b>." % (fq(a), fq(s_), fq(pp)))
    if k == "code":
        n = R.choice([3, 4])
        return M("Un code de %d chiffres (0 à 9) est choisi au hasard. Quelle est la probabilité de le trouver du premier coup ?" % n, fr(1, num(10 ** n)), [fr(1, 10 * n), fr(n, 10), fr(1, 9 ** n)],
                 "Il y a 10<sup>%d</sup> = %s codes : <b>%s</b>." % (n, num(10 ** n), fr(1, num(10 ** n))))
    if k == "equite":
        return M("%s propose : « On tire deux boules sans remise dans une urne de 2 rouges et 2 bleues. Si elles sont de même couleur, je gagne. » Le jeu est-il équitable ?" % p[0], "non : P(même couleur) = 1/3", ["oui : P(même couleur) = 1/2", "non : P(même couleur) = 2/3", "oui, car il y a autant de rouges que de bleues"],
                 "P(RR) + P(BB) = 2/4 × 1/3 + 2/4 × 1/3 = <b>1/3</b> : le jeu n’est pas équitable.")
    n = R.randint(2, 5)
    m = R.randint(2, 5)
    t = n + m
    pp = Fr(n * (n - 1) + m * (m - 1), t * (t - 1))
    return M("Un tiroir contient %d chaussettes noires et %d blanches. %s en prend deux au hasard dans le noir. Quelle est la probabilité d’avoir une paire de même couleur ?" % (n, m, p[0]), fq(pp), [fq(Fr(n * n + m * m, t * t)), fq(Fr(n * (n - 1), t * (t - 1))), fq(1 - pp) if 1 - pp != pp else fq(pp / 2)],
             "P(NN) + P(BB) = %s × %s + %s × %s = <b>%s</b>." % (fr(n, t), fr(n - 1, t - 1), fr(m, t), fr(m - 1, t - 1), fq(pp)))


def main():
    seen = set()
    sets = [("Tirages sans remise", mix(R, seen, [(s1, 20)])), ("Arbres pondérés", mix(R, seen, [(s2, 20)])),
            ("Avec ou sans remise ?", mix(R, seen, [(s3, 20)])), ("Fréquences et probabilités", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans un <b>arbre pondéré</b>, on multiplie les probabilités le long d’un chemin et on additionne les probabilités des chemins qui réalisent l’événement.",
              "<b>Sans remise</b>, la composition change au deuxième tirage : il y a une boule de moins. <b>Avec remise</b>, elle ne change pas.",
              "Quand on répète une expérience un grand nombre de fois, la fréquence observée se rapproche de la probabilité (on peut l’utiliser pour estimer une probabilité inconnue)."],
             [("3 rouges, 2 bleues, deux tirages sans remise : P(RR)", ["3/5 × 2/4"], "6/20 = 3/10")],
             [["Garder 3/5 au 2e tirage sans remise", "Il ne reste que 4 boules dont 2 rouges : 2/4."], ["Additionner sur un chemin", "On multiplie le long d’un chemin."],
              ["Prendre une fréquence sur 20 essais pour la probabilité exacte", "Il faut un grand nombre d’essais, et cela reste une estimation."]])
    faq = [("Comment vérifier un arbre ?", "Les probabilités issues d’un même nœud ont pour somme 1, et la somme des probabilités de tous les chemins vaut 1."),
           ("Quelle différence entre fréquence et probabilité ?", "La fréquence est observée et varie d’une série d’essais à l’autre ; la probabilité est une valeur théorique.")]
    unit("3e", R, "probabilites", "D",
         "Calculer des probabilités dans des expériences à deux épreuves, avec ou sans remise, à l’aide d’arbres pondérés ou de tableaux ; utiliser l’événement contraire ; relier fréquence et probabilité pour estimer une probabilité",
         "Probabilités : arbres et tirages sans remise", "Probabilités",
         "Fiches de maths 3e sur les probabilités : tirages avec et sans remise, arbres pondérés, événement contraire, fréquences et loi des grands nombres, problèmes. 100 exercices corrigés.",
         "Sur un arbre : × le long d’un chemin, + entre chemins", "Sans remise : une boule de moins au 2e tirage", body, faq, sets, 16)


if __name__ == "__main__":
    main()
