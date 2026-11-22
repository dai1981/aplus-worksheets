# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Cercle trigonométrique et radian (conversions, longueur d’arc, enroulement, mesure principale, cosinus et sinus des angles remarquables, cos² + sin² = 1)
  python3 tools/gen_fr_maths_premiere_cercle_trigonometrique_et_radian.py
Erreurs : 60° = π/6, confondre cos(π/3) et sin(π/3), oublier le signe selon le quadrant, mesure principale hors de ]−π ; π].
"""
import math
import random
from fr_ly1 import *

R = random.Random(60614)
ANG = [Fr(k, 6) for k in range(-11, 13)] + [Fr(k, 4) for k in range(-7, 9) if k % 2]


def circle(t, label="M"):
    W, H = 260, 260
    c, r = 130, 95
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2'/>" % (c, c, r, INK), line(20, c, 240, c, INK, 1.2), line(c, 240, c, 20, INK, 1.2)]
    for k in range(24):
        a = k * math.pi / 12
        x, y = c + r * math.cos(a), c - r * math.sin(a)
        s.append(line(c + (r - 5) * math.cos(a), c - (r - 5) * math.sin(a), c + (r + 5) * math.cos(a), c - (r + 5) * math.sin(a), INK, 1))
    a = float(t) * math.pi
    x, y = c + r * math.cos(a), c - r * math.sin(a)
    s.append(line(c, c, x, y, BLUE, 1.8))
    s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x, y, RED))
    s.append(text(x + 16 * math.cos(a), y - 16 * math.sin(a) + 5, label, 16, col=RED, weight=700))
    s.append(text(c + r + 12, c - 6, "I", 14) + text(c + 8, c - r - 6, "J", 14) + text(c - 10, c + 18, "O", 14))
    return wrap(W, H, "".join(s), "cercle trigonométrique", lg=True)


def s1():
    k = R.choice(["d2r", "d2r", "r2d"])
    t = R.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(5, 6), Fr(1), Fr(7, 6), Fr(5, 4), Fr(4, 3), Fr(3, 2), Fr(5, 3), Fr(7, 4), Fr(11, 6), Fr(2), Fr(1, 12), Fr(5, 12), Fr(1, 9), Fr(1, 5)])
    deg = t * 180
    if k == "d2r":
        return M("Convertis %s° en radians." % d(deg), pif(t), [pif(1 / t) if 1 / t != t else pif(t / 2), pif(t * 2), pif(t / 2), pif(t + Fr(1, 6)), pif(t + Fr(1, 4))],
                 "180° = π rad, donc %s° = %s × π ÷ 180 = <b>%s</b> rad." % (d(deg), d(deg), pif(t)))
    return M("Convertis %s rad en degrés." % pif(t), "%s°" % d(deg), ["%s°" % d(t * 360), "%s°" % d(t * 90), "%s°" % d(deg + 30)],
             "π rad = 180°, donc %s = %s × 180° = <b>%s°</b>." % (pif(t), fq(t), d(deg)))


def s2():
    k = R.choice(["arc", "arc", "angle", "tour"])
    r = R.randint(2, 12)
    if k == "arc":
        t = R.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(1), Fr(3, 2)])
        return M("Sur un cercle de rayon %d cm, quelle est la longueur d’un arc intercepté par un angle de %s rad ?" % (r, pif(t)), pif(r * t) + " cm",
                 [pif(t) + " cm", pif(2 * r * t) + " cm", pif(t / r) + " cm", d(r * t * 180) + " cm"], "Longueur = r × θ = %d × %s = <b>%s cm</b>." % (r, pif(t), pif(r * t)))
    if k == "angle":
        L_ = R.randint(1, 3 * r)
        return M("Sur un cercle de rayon %d cm, un arc mesure %d cm. Quelle est la mesure de l’angle au centre en radians ?" % (r, L_), fq(Fr(L_, r)) + " rad",
                 [fq(Fr(r, L_)) + " rad", fq(Fr(L_ * r)) + " rad", fq(Fr(L_, 2 * r)) + " rad", pif(Fr(L_, r)) + " rad", fq(Fr(2 * L_, r)) + " rad"], "θ = longueur ÷ rayon = %d ÷ %d = <b>%s rad</b>." % (L_, r, fq(Fr(L_, r))))
    n = R.choice([2, 3, 4, 6, 8])
    return M("Sur le cercle trigonométrique (rayon 1), quelle longueur parcourt-on en faisant 1/%d de tour ?" % n, pif(Fr(2, n)), [pif(Fr(1, n)), "%s" % fq(Fr(1, n)), pif(Fr(4, n))],
             "Un tour mesure 2π ; 1/%d de tour : 2π ÷ %d = <b>%s</b>." % (n, n, pif(Fr(2, n))))


def s3():
    k = R.choice(["meme", "princ", "princ", "fig"])
    base = R.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(2, 3), Fr(3, 4), Fr(5, 6), Fr(-1, 6), Fr(-1, 3), Fr(-3, 4), Fr(-2, 3), Fr(1, 2), Fr(-1, 2)])
    n = R.choice([1, 2, -1, -2, 3])
    t = base + 2 * n
    if k == "meme":
        return M("Quel réel est associé au même point du cercle trigonométrique que %s ?" % pif(t), pif(base), [pif(-base), pif(base + 1), pif(t - 1), pif(base + Fr(1, 2)), pif(base - Fr(1, 2))],
                 "On enlève ou on ajoute des tours de 2π : %s %s %s = <b>%s</b>." % (pif(t), MINUS if n > 0 else "+", pif(abs(2 * n)), pif(base)))
    if k == "princ":
        return M("Quelle est la mesure principale (dans ]−π ; π]) de l’angle %s ?" % pif(t), pif(base), [pif(base + 2) if base + 2 <= 2 else pif(base - 2), pif(-base), pif(t - 1) if abs(t - 1) <= 3 else pif(base + 1), pif(base + 1), pif(base - 1)],
                 "%s = %s %s %s, et %s est dans ]−π ; π] : <b>%s</b>." % (pif(t), pif(base), "+" if n > 0 else MINUS, pif(abs(2 * n)), pif(base), pif(base)))
    svg = circle(base)
    return M("<div class='qfig'>%s</div>Les graduations sont tous les π/12. Quel réel de ]−π ; π] est associé au point M ?" % svg, pif(base), [pif(-base), pif(1 - base) if 1 - base <= 1 else pif(base / 2), pif(base + Fr(1, 2)) if base + Fr(1, 2) <= 1 else pif(base - Fr(1, 2)), pif(base + Fr(1, 6)) if base + Fr(1, 6) <= 1 else pif(base - Fr(1, 6)), pif(base - Fr(1, 4)) if base - Fr(1, 4) > -1 else pif(base + Fr(1, 4))],
             "On compte les graduations depuis I dans le sens %s : <b>%s</b>." % ("direct (inverse des aiguilles d’une montre)" if base > 0 else "indirect", pif(base)))


def s4():
    t = R.choice(ANG)
    fn = R.choice(["cos", "sin"])
    v = trig_val(t, fn)
    other = trig_val(t, "sin" if fn == "cos" else "cos")
    w = [other, trig_val(-t if fn == "sin" else t + 1, fn), MINUS + v if not v.startswith(MINUS) and v != "0" else v.lstrip(MINUS) if v != "0" else "1", FR("√3", 2) if "√3" not in v else FR(1, 2), FR("√2", 2) if "√2" not in v else FR("√3", 2), FR(1, 2), MINUS + FR(1, 2), "1", "0", MINUS + "1", MINUS + FR("√3", 2), MINUS + FR("√2", 2)]
    return M("Que vaut %s(%s) ?" % (fn, pif(t)), v, w, "On place %s sur le cercle trigonométrique : %s est %s du point. <b>%s(%s) = %s</b>." % (pif(t), fn, "l’abscisse" if fn == "cos" else "l’ordonnée", fn, pif(t), v))


def s5():
    k = R.choice(["pyth", "pyth", "coord", "signe"])
    if k == "pyth":
        a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
        fn = R.choice(["cos", "sin"])
        q = R.choice([1, 2, 3, 4])
        sign = {"cos": {1: 1, 2: -1, 3: -1, 4: 1}, "sin": {1: 1, 2: 1, 3: -1, 4: -1}}
        o = "sin" if fn == "cos" else "cos"
        given = sign[fn][q] * a
        ans = sign[o][q] * b
        iv = {1: "]0 ; π/2[", 2: "]π/2 ; π[", 3: "]−π ; −π/2[", 4: "]−π/2 ; 0["}[q]
        return M("%s x = %s et x ∈ %s. Que vaut %s x ?" % (fn, fq(Fr(given, c)), iv, o), fq(Fr(ans, c)),
                 [fq(Fr(-ans, c)), fq(Fr(c - abs(given), c)) if c - abs(given) != b else fq(Fr(b, a)), fq(Fr(abs(given), c)) if Fr(abs(given), c) != Fr(ans, c) else fq(Fr(a, b))],
                 "cos² x + sin² x = 1 : %s² x = 1 − %s = %s, et sur %s, %s x est %s : <b>%s</b>." % (o, fq(Fr(a * a, c * c)), fq(Fr(b * b, c * c)), iv, o, "positif" if ans > 0 else "négatif", fq(Fr(ans, c))))
    t = R.choice(ANG)
    if k == "coord":
        ans = "(%s ; %s)" % (trig_val(t, "cos"), trig_val(t, "sin"))
        w = ["(%s ; %s)" % (trig_val(t, "sin"), trig_val(t, "cos")), "(%s ; %s)" % (trig_val(-t, "cos"), trig_val(-t, "sin")), "(%s ; %s)" % (trig_val(t + 1, "cos"), trig_val(t + 1, "sin")), "(%s ; %s)" % (trig_val(t + Fr(1, 2), "cos"), trig_val(t + Fr(1, 2), "sin")), "(%s ; %s)" % (trig_val(t, "cos"), trig_val(t, "cos")), "(%s ; %s)" % (trig_val(t, "sin"), trig_val(t, "sin"))]
        return M("Quelles sont les coordonnées du point M du cercle trigonométrique associé à %s ?" % pif(t), ans, w, "M(cos(%s) ; sin(%s)) = <b>%s</b>." % (pif(t), pif(t), ans))
    if t in (0, 1, -1, Fr(1, 2), Fr(-1, 2)) or t.denominator == 1:
        return None
    q = "cos" if R.random() < 0.5 else "sin"
    v = (math.cos if q == "cos" else math.sin)(float(t) * math.pi)
    ans = "positif" if v > 0 else "négatif"
    return M("Quel est le signe de %s(%s) ?" % (q, pif(t)), ans, ["négatif" if ans == "positif" else "positif", "nul", "on ne peut pas savoir sans calculatrice"],
             "Le point associé à %s est %s : son %s est <b>%s</b>." % (pif(t), "à droite de l’axe des ordonnées" if math.cos(float(t) * math.pi) > 0 else "à gauche de l’axe des ordonnées", "abscisse (cos)" if q == "cos" else "ordonnée (sin)", ans) if q == "cos" else
             "Le point associé à %s est %s : son ordonnée (sin) est <b>%s</b>." % (pif(t), "au-dessus de l’axe des abscisses" if v > 0 else "au-dessous de l’axe des abscisses", ans))


def main():
    seen = set()
    sets = [("Degrés et radians", mix(R, seen, [(s1, 20)])), ("Longueur d’arc", mix(R, seen, [(s2, 20)])),
            ("Enroulement et mesure principale", mix(R, seen, [(s3, 20)])), ("Valeurs remarquables", mix(R, seen, [(s4, 20)])), ("cos² + sin² = 1 et signes", mix(R, seen, [(s5, 20)]))]
    body = L(["Le <b>radian</b> : sur un cercle de rayon 1, un angle de θ rad intercepte un arc de longueur θ. 180° = π rad ; sur un cercle de rayon r, l’arc mesure r × θ.",
              "On enroule la droite des réels sur le cercle trigonométrique : x et x + 2kπ (k entier) donnent le même point M. La mesure principale est dans ]−π ; π].",
              "M(cos x ; sin x) : cos x est l’abscisse de M, sin x son ordonnée. Pour tout x, cos² x + sin² x = 1.",
              "Valeurs remarquables : cos(π/6) = √3/2, cos(π/4) = √2/2, cos(π/3) = 1/2 ; sin(π/6) = 1/2, sin(π/4) = √2/2, sin(π/3) = √3/2."],
             [("x = 2π/3", ["Le point est dans le quart en haut à gauche, symétrique de π/3 par rapport à l’axe des ordonnées"], "cos(2π/3) = −1/2 et sin(2π/3) = √3/2")],
             [["60° = π/6", "60° = π/3 (180 ÷ 60 = 3)."], ["cos(π/3) = √3/2", "cos(π/3) = 1/2 ; c’est sin(π/3) qui vaut √3/2."], ["Mesure principale de 5π/3 : 5π/3", "5π/3 − 2π = −π/3, dans ]−π ; π]."]])
    faq = [("Pourquoi utiliser les radians ?", "Avec les radians, la longueur d’un arc vaut simplement rayon × angle, et les fonctions cosinus et sinus se dérivent simplement (programme de terminale)."),
           ("Comment retrouver les valeurs remarquables ?", "Avec un triangle équilatéral coupé en deux (π/6 et π/3) et un carré coupé par sa diagonale (π/4). On les retrouve aussi sur le cercle.")]
    unit("premiere", R, "cercle-trigonometrique-et-radian", "F",
         "Cercle trigonométrique, enroulement de la droite des réels ; le radian ; cosinus et sinus d’un nombre réel ; valeurs remarquables ; relation cos² x + sin² x = 1",
         "Cercle trigonométrique et radian", "Cercle trigonométrique",
         "Fiches de maths première sur le cercle trigonométrique : radians, longueur d’arc, enroulement, mesure principale, valeurs remarquables de cos et sin, cos² + sin² = 1. 100 exercices corrigés.",
         "180° = π rad ; M(cos x ; sin x)", "cos² x + sin² x = 1", body, faq, sets, 14)


if __name__ == "__main__":
    main()
