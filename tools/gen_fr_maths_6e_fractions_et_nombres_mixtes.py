# -*- coding: utf-8 -*-
"""
France Maths 6e : Fractions et nombres mixtes
  python3 tools/gen_fr_maths_6e_fractions_et_nombres_mixtes.py
Fraction d’une figure, fraction et quotient (7/4 = 7 ÷ 4), nombres mixtes, droite graduée, fraction d’une quantité.
Erreurs : inverser numérateur et dénominateur, 7/4 = 7,4, 2 et 1/3 = 2/3, 3/4 de 20 = 20 ÷ 3 × 4.
"""
import random
from fr_c4 import *
from fr_common import bande, disque, droite_frac

R = random.Random(60108)
K = Kids(R)


def s1():
    den = R.choice([3, 4, 5, 6, 8, 10, 12])
    k = R.randint(1, den - 1)
    pic = bande(den, k) if R.random() < 0.5 or den == 12 else disque(den, k)
    if R.random() < 0.5:
        return M("<div class='qfig'>%s</div>Quelle fraction de la figure est coloriée ?" % pic, fq(Fr(k, den)) if Fr(k, den).denominator == den else fr(k, den),
                 [fr(den, k), fr(den - k, den) if den - k != k else fr(k, den + 1), fr(k, den - k) if den - k not in (k, 0) else fr(k + 1, den)],
                 "%d parts égales (dénominateur), %s (numérateur) : <b>%s</b>." % (den, pl(k, "coloriée"), fr(k, den)))
    return M("<div class='qfig'>%s</div>Quelle fraction de la figure n’est <b>pas</b> coloriée ?" % pic, fr(den - k, den), [fr(k, den) if k != den - k else fr(k + 1, den), fr(den, den - k), fr(den - k, k) if k != den - k else fr(1, den)],
             "%s sur %d %s pas coloriée%s : <b>%s</b>." % (pl(den - k, "part"), den, "n’est" if den - k == 1 else "ne sont", "" if den - k == 1 else "s", fr(den - k, den)))


def s2():
    den = R.choice([2, 4, 5, 8, 10, 20, 25])
    n = R.randint(1, 4 * den)
    if n % den == 0:
        return None
    v = Fr(n, den)
    if R.random() < 0.5:
        return M("Quelle est l’écriture décimale de %s ?" % fr(n, den), d(v), ["%d,%d" % (n, den), d(Fr(den, n)) if Fr(den, n).denominator in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100) else d(v + 1), d(v + Fr(1, 10))],
                 "%s = %d %s %d = <b>%s</b>." % (fr(n, den), n, DIV, den, d(v)))
    return M("%d %s %d = …" % (n, DIV, den), fr(n, den), [fr(den, n), "%d,%d" % (n, den), fr(n, den * 10)],
             "Le quotient de %d par %d s’écrit <b>%s</b> (= %s)." % (n, den, fr(n, den), d(v)))


def mx(e, n, den):
    return "%d + %s" % (e, fr(n, den))


def s3():
    den = R.choice([2, 3, 4, 5, 6, 8, 10])
    e = R.randint(1, 5)
    n = R.randint(1, den - 1)
    N = e * den + n
    if R.random() < 0.5:
        return M("Écris %s sous la forme d’un nombre mixte (entier + fraction plus petite que 1)." % fr(N, den), mx(e, n, den),
                 [mx(e + 1, n, den), mx(n, e, den) if e < den and (n, e) != (e, n) else mx(e - 1 if e > 1 else e + 2, n, den), mx(N // 10, N % 10, den) if 0 < N % 10 < den and N // 10 != e else mx(e, n + 1 if n + 1 < den else n - 1, den)],
                 "%d = %d %s %d + %d, donc %s = %s = <b>%s</b>." % (N, den, FOIS, e, n, fr(N, den), "%s + %s" % (fr(e * den, den), fr(n, den)), mx(e, n, den)))
    return M("%s = …" % mx(e, n, den), fr(N, den), [fr(e + n, den), fr(e * n, den), fr(N + den, den)],
             "%d = %s ; %s + %s = <b>%s</b>." % (e, fr(e * den, den), fr(e * den, den), fr(n, den), fr(N, den)))


def s4():
    den = R.choice([2, 3, 4, 5, 6, 8, 10])
    k = R.randint(1, 3 * den - 1)
    if k % den == 0:
        return None
    pic = droite_frac(den, 3, [(k, "A")])
    return M("<div class='qfig'>%s</div>Quelle fraction repère le point A ?" % pic, fr(k, den), [fr(k, 3 * den), fr(k + 1, den), fr(k - 1, den) if k > 1 else fr(k + 2, den)],
             "Chaque unité est partagée en %d. A est à %s de 0 : <b>%s</b>%s." % (den, pl(k, "graduation"), fr(k, den), "" if k < den else " (= %s)" % mx(k // den, k % den, den)))


def s5():
    p = K.next()
    den = R.choice([2, 3, 4, 5, 10])
    n = R.randint(1, den - 1)
    q = R.randint(2, 12)
    tot = den * q
    th = R.choice([("billes", "ses"), ("euros", "ses"), ("pages", "les"), ("élèves", "les")])
    if th[0] == "pages":
        txt = "Un livre a %d pages. %s en a lu les %s. Combien de pages a-t-%s lues ?" % (tot, p[0], fr(n, den), p[1])
    elif th[0] == "élèves":
        txt = "Une classe a %d élèves. Les %s sont des filles. Combien y a-t-il de filles ?" % (tot, fr(n, den))
    else:
        part = "la moitié" if (n, den) == (1, 2) else "les " + fr(n, den) if n > 1 else "le " + fr(n, den)
        txt = ("%s a %d billes. %s en donne %s à son frère. Combien de billes donne-t-%s ?" % (p[0], tot, p[1].capitalize(), part, p[1]) if th[0] == "billes" else
               "%s a %d euros. %s en dépense %s. Combien d’euros dépense-t-%s ?" % (p[0], tot, p[1].capitalize(), part, p[1]))
    return M(txt, str(n * q), [str(tot // n * den) if n > 1 and tot % n == 0 and tot // n * den != n * q else str(tot - n * q) if tot - n * q != n * q else str(n * q + 1), str(q), str(tot * n)],
             "%s de %d : %d %s %d = %d, puis %d %s %d = <b>%d</b>." % (fr(n, den), tot, tot, DIV, den, q, q, FOIS, n, n * q))


def main():
    seen = set()
    sets = [("Fraction d’une figure", mix(R, seen, [(s1, 20)])), ("Fraction et quotient", mix(R, seen, [(s2, 20)])),
            ("Nombres mixtes", mix(R, seen, [(s3, 20)])), ("Droite graduée", mix(R, seen, [(s4, 20)])), ("Fraction d’une quantité", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans %s, 4 est le <b>dénominateur</b> (en combien de parts égales on partage) et 3 le <b>numérateur</b> (combien on en prend)." % fr(3, 4),
              "%s est aussi le quotient de 7 par 4 : 7 ÷ 4 = 1,75." % fr(7, 4),
              "%s = 1 + %s : c’est un <b>nombre mixte</b> (un entier et une fraction plus petite que 1)." % (fr(7, 4), fr(3, 4))],
             [("%s de 20" % fr(3, 4), ["20 ÷ 4 = 5", "5 × 3 = 15"], "15")],
             [["Inverser numérateur et dénominateur", "Le dénominateur (en bas) dit en combien de parts on partage."],
              ["Écrire %s = 7,4" % fr(7, 4), "%s = 7 ÷ 4 = 1,75." % fr(7, 4)],
              ["Croire que 2 + %s = %s" % (fr(1, 3), fr(2, 3)), "2 + %s = %s + %s = %s." % (fr(1, 3), fr(6, 3), fr(1, 3), fr(7, 3))]])
    faq = [("Qu’est-ce qu’un nombre mixte ?", "Un nombre écrit comme un entier plus une fraction plus petite que 1, par exemple 2 + %s." % fr(1, 4)),
           ("Comment calculer %s d’un nombre ?" % fr(3, 4), "On divise le nombre par 4, puis on multiplie par 3.")]
    unit("6e", R, "fractions-et-nombres-mixtes", "N",
         "Utiliser les fractions pour exprimer un partage, une mesure, un quotient ; passer d’une fraction à un nombre mixte ; repérer des fractions sur une droite graduée ; calculer la fraction d’une quantité",
         "Fractions et nombres mixtes", "Fractions et nombres mixtes",
         "Fiches de maths 6e sur les fractions : fraction d’une figure, fraction et quotient, nombres mixtes, droite graduée et fraction d’une quantité. 100 exercices corrigés.",
         "%s = 7 ÷ 4 = 1 + %s" % (fr(7, 4), fr(3, 4)), "Le dénominateur dit en combien de parts on partage.", body, faq, sets, 8)


if __name__ == "__main__":
    main()
