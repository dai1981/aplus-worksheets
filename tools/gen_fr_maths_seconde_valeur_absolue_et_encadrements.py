# -*- coding: utf-8 -*-
"""
France Maths Seconde : Valeur absolue, distance, encadrements et arrondis
  python3 tools/gen_fr_maths_seconde_valeur_absolue_et_encadrements.py
Erreurs : |−5| = −5, distance = a + b, |x − 3| ⩽ 2 ↔ [−1 ; 5] au lieu de [1 ; 5], confondre arrondi et troncature, chiffres significatifs mal comptés.
"""
import random
import math
from fr_c4 import *

R = random.Random(60503)
K = Kids(R)


def iv(a, b, closed=True):
    return "%s%s ; %s%s" % ("[" if closed else "]", d(a), d(b), "]" if closed else "[")


def s1():
    k = R.choice(["abs", "abs", "calc", "eq"])
    if k == "abs":
        x = R.choice([R.randint(-30, 30), Fr(R.randint(-99, 99), 10)])
        if x == 0:
            return None
        return M("Que vaut |%s| ?" % d(x), d(abs(x)), [d(-abs(x)), d(x * x) if abs(x) > 1 and (x * x).denominator in (1, 100) else d(abs(x) + 1), "0"],
                 "La valeur absolue est la distance à 0 : <b>%s</b>." % d(abs(x)))
    if k == "calc":
        a, b = R.randint(-9, 9), R.randint(-9, 9)
        if a == b:
            return None
        r = abs(a - b)
        return M("Calcule |%s − %s|." % (d(a), par(b)), d(r), [d(abs(a) - abs(b)) if abs(a) - abs(b) != r else d(r + 1), d(a - b) if a - b != r else d(-r) if r else "1", d(abs(a) + abs(b)) if abs(a) + abs(b) != r else d(r + 2)],
                 "%s − %s = %s, donc |%s| = <b>%s</b>." % (d(a), par(b), d(a - b), d(a - b), d(r)))
    a = R.randint(1, 12)
    return M("Quelles sont les solutions de |x| = %d ?" % a, "x = −%d ou x = %d" % (a, a), ["x = %d" % a, "x = −%d" % a, "pas de solution"],
             "Les deux nombres à distance %d de 0 : <b>x = −%d ou x = %d</b>." % (a, a, a))


def s2():
    a, b = R.randint(-12, 12), R.randint(-12, 12)
    if a == b:
        return None
    k = R.choice(["dist", "dist", "milieu"])
    if k == "dist":
        return M("Quelle est la distance entre les réels %s et %s ?" % (d(a), d(b)), d(abs(a - b)), [d(abs(a + b)) if abs(a + b) != abs(a - b) else d(abs(a - b) + 1), d(a - b) if a - b < 0 else d(b - a), d(abs(a) + abs(b)) if abs(a) + abs(b) != abs(a - b) else d(abs(a - b) + 2)],
                 "d(a ; b) = |a − b| = |%s − %s| = <b>%s</b>." % (d(a), par(b), d(abs(a - b))))
    c = Fr(a + b, 2)
    return M("Quel réel est à égale distance de %s et %s ?" % (d(a), d(b)), d(c), [d(Fr(b - a, 2)) if Fr(b - a, 2) != c else d(c + 1), d(a + b) if a + b != c else d(c - 1), d(Fr(abs(a) + abs(b), 2)) if Fr(abs(a) + abs(b), 2) != c else d(c + 2)],
             "C’est le milieu : (%s + %s) ÷ 2 = <b>%s</b>." % (d(a), par(b), d(c)))


def s3():
    a = R.randint(-8, 8)
    r = R.randint(1, 6)
    k = R.choice(["le", "le", "lt", "rev"])
    sign = "−" if a >= 0 else "+"
    form = "|x %s %s|" % (sign, d(abs(a))) if a else "|x|"
    if k in ("le", "lt"):
        cl = k == "le"
        ans = iv(a - r, a + r, cl)
        return M("Quel intervalle correspond à %s %s %d ?" % (form, "⩽" if cl else "&lt;", r), ans, [iv(-a - r, -a + r, cl) if a else iv(0, r, cl), iv(a - r, a + r, not cl), iv(-r, r, cl) if a else iv(-2 * r, 2 * r, cl)],
                 "Les x à une distance de %s %s %d : <b>%s</b>." % (d(a), "au plus" if cl else "strictement moins de", r, ans))
    lo, hi = a - r, a + r
    return M("L’intervalle [%s ; %s] correspond à…" % (d(lo), d(hi)), "%s ⩽ %d" % (form, r), ["%s ⩽ %d" % ("|x %s %s|" % ("+" if a >= 0 else "−", d(abs(a))) if a else "|x|", r) if a else "|x| ⩽ %d" % (2 * r), "%s ⩽ %d" % (form, 2 * r), "%s ⩾ %d" % (form, r)],
             "Centre (%s + %s) ÷ 2 = %s, rayon %d : <b>%s ⩽ %d</b>." % (d(lo), par(hi), d(a), r, form, r))


def s4():
    k = R.choice(["enc", "enc", "arr", "cs"])
    if k == "enc":
        n = R.choice([2, 3, 5, 7, 10, 11, 13])
        p = R.randint(1, 3)
        v = math.sqrt(n)
        lo = Fr(math.floor(v * 10 ** p), 10 ** p)
        return M("Donne l’encadrement de √%d à 10<sup>−%d</sup> près (bornes décimales)." % (n, p), "%s &lt; √%d &lt; %s" % (dk(lo, p), n, dk(lo + Fr(1, 10 ** p), p)),
                 ["%s &lt; √%d &lt; %s" % (dk(lo - Fr(1, 10 ** p), p), n, dk(lo, p)), "%s &lt; √%d &lt; %s" % (dk(Fr(n, 2) - Fr(1, 10 ** p), p), n, dk(Fr(n, 2), p)), "%s &lt; √%d &lt; %s" % (dk(lo + Fr(1, 10 ** p), p), n, dk(lo + Fr(2, 10 ** p), p))],
                 "√%d ≈ %s… : <b>%s &lt; √%d &lt; %s</b> (amplitude 10<sup>−%d</sup>)." % (n, dk(Fr(math.floor(v * 10 ** (p + 2)), 10 ** (p + 2)), p + 2), dk(lo, p), n, dk(lo + Fr(1, 10 ** p), p), p))
    if k == "arr":
        x = Fr(R.randint(10000, 99999), 10000) * R.choice([1, 10])
        p = R.randint(1, 2)
        ar = Fr(round(x * 10 ** p + Fr(1, 10 ** 9)), 10 ** p)
        tr = Fr(math.floor(x * 10 ** p), 10 ** p)
        if ar == tr:
            return None
        return M("Donne l’arrondi de %s au %s." % (d(x), "dixième" if p == 1 else "centième"), dk(ar, p), [dk(tr, p), dk(ar, p + 1) if dk(ar, p + 1) != dk(ar, p) else dk(ar + Fr(1, 10 ** p), p), dk(ar - Fr(2, 10 ** p), p)],
                     "Le chiffre suivant est ⩾ 5, on arrondit au-dessus : <b>%s</b> (la troncature serait %s)." % (dk(ar, p), dk(tr, p)))
    x = R.choice([123456, 0.004567, 98765, 3.14159, 0.0802, 45.678])
    n = R.choice([2, 3])
    from decimal import Decimal, ROUND_HALF_UP
    D = Decimal(str(x))
    e = D.adjusted()
    q = Decimal(1).scaleb(e - n + 1)
    rd = D.quantize(q, rounding=ROUND_HALF_UP) if q < 1 else (D / q).quantize(Decimal(1), rounding=ROUND_HALF_UP) * q
    rf = Fr(str(rd))
    wrong_dec = Fr(str(D.quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))) if D < 1 else Fr(str(D)).limit_denominator(1) + 1
    return M("Arrondis %s à %d chiffres significatifs." % (d(Fr(str(D))), n), d(rf), [d(wrong_dec) if wrong_dec != rf else d(rf * 10), d(rf * 10), d(rf / 10)],
             "On compte à partir du premier chiffre non nul : <b>%s</b>." % d(rf))


def s5():
    k = R.choice(["piece", "temp", "mesure", "pi"])
    if k == "piece":
        a = R.choice([50, 80, 120, 200])
        t = R.choice([Fr(1, 10), Fr(2, 10), Fr(5, 10), 1])
        return M("Une pièce doit mesurer %d mm à %s mm près. Quel intervalle décrit les longueurs acceptées ?" % (a, d(t)), iv(a - t, a + t), [iv(a, a + t), iv(a - 2 * t, a + 2 * t), iv(a - t, a)],
                 "|L − %d| ⩽ %s : <b>%s</b>." % (a, d(t), iv(a - t, a + t)))
    if k == "temp":
        a, b = R.randint(-10, 0), R.randint(1, 15)
        return M("Le matin, il fait %s °C ; l’après-midi, %s °C. De combien de degrés la température a-t-elle varié ?" % (d(a), d(b)), "%s °C" % d(b - a), ["%s °C" % d(b + a) if b + a != b - a else "%s °C" % d(b - a + 1), "%s °C" % d(abs(a)), "%s °C" % d(b)],
                 "|%s − %s| = <b>%s °C</b>." % (d(b), par(a), d(b - a)))
    if k == "mesure":
        v = Fr(R.randint(150, 190), 100)
        return M("Une taille mesurée vaut %s m à 0,01 m près. Dans quel intervalle se trouve la vraie taille ?" % dk(v, 2), iv(v - Fr(1, 100), v + Fr(1, 100)), [iv(v - Fr(1, 10), v + Fr(1, 10)), iv(v, v + Fr(1, 100)), iv(v - Fr(1, 1000), v + Fr(1, 1000))],
                 "|t − %s| ⩽ 0,01 : <b>%s</b>." % (dk(v, 2), iv(v - Fr(1, 100), v + Fr(1, 100))))
    V = [("Quel encadrement de π a une amplitude de 0,01 ?", "3,14 &lt; π &lt; 3,15", ["3 &lt; π &lt; 4", "3,1 &lt; π &lt; 3,2", "3,141 &lt; π &lt; 3,142"]),
         ("Quel est l’arrondi de π au millième ?", "3,142", ["3,141", "3,14", "3,1416"]),
         ("Quelle est la troncature de π au centième ?", "3,14", ["3,15", "3,141", "3,1"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "π ≈ 3,14159… : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Valeur absolue", mix(R, seen, [(s1, 20)])), ("Distance entre deux réels", mix(R, seen, [(s2, 20)])),
            ("Valeur absolue et intervalles", mix(R, seen, [(s3, 20)])), ("Encadrements et arrondis", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["La <b>valeur absolue</b> |x| est la distance de x à 0 : |−5| = |5| = 5. La distance entre a et b est |a − b|.",
              "|x − a| ⩽ r signifie que x est à une distance au plus r de a : x ∈ [a − r ; a + r].",
              "Encadrer à 10<sup>−n</sup> près : deux décimaux d’écart 10<sup>−n</sup>. Arrondir : on regarde le chiffre suivant (⩾ 5 → au-dessus)."],
             [("|x − 3| ⩽ 2", ["centre 3, rayon 2", "3 − 2 = 1 et 3 + 2 = 5"], "x ∈ [1 ; 5]")],
             [["|−5| = −5", "Une distance est positive : |−5| = 5."], ["|x − 3| ⩽ 2 ↔ [−1 ; 5]", "Le centre est 3 : [1 ; 5]."], ["Confondre arrondi et troncature", "2,47 arrondi au dixième donne 2,5 ; tronqué, 2,4."]])
    faq = [("Que signifie « à 0,01 près » ?", "L’écart entre la valeur exacte et la valeur donnée est au plus 0,01."),
           ("Qu’est-ce qu’un chiffre significatif ?", "Tout chiffre à partir du premier chiffre non nul : 0,0802 a trois chiffres significatifs (8, 0, 2).")]
    unit("seconde", R, "valeur-absolue-et-encadrements", "N",
         "Utiliser la valeur absolue comme distance à 0 et la distance entre deux réels ; caractériser un intervalle centré par |x − a| ⩽ r ; encadrer un réel par des décimaux à 10⁻ⁿ près ; arrondir avec un nombre de chiffres significatifs adapté",
         "Valeur absolue, encadrements et arrondis", "Valeur absolue et encadrements",
         "Fiches de maths seconde sur la valeur absolue : distance entre deux réels, |x − a| ⩽ r et intervalles, encadrements, arrondis et chiffres significatifs. 100 exercices corrigés.",
         "|a − b| est la distance entre a et b", "|x − a| ⩽ r ⇔ x ∈ [a − r ; a + r]", body, faq, sets, 3)


if __name__ == "__main__":
    main()
