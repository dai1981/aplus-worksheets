# -*- coding: utf-8 -*-
"""
France Maths Seconde : Problèmes de géométrie (projeté orthogonal, distance à une droite, trigonométrie, cos² + sin² = 1, aires et volumes)
  python3 tools/gen_fr_maths_seconde_geometrie_plane.py
Erreurs : distance à une droite mesurée en oblique, cos = opposé/hypoténuse, sin α = 1 − cos α, oublier ÷ 2 dans l’aire d’un triangle.
"""
import random
import math
from fr_c4 import *

R = random.Random(60516)
K = Kids(R)
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20)]


def s1():
    k = R.choice(["def", "dist", "dist", "pyth"])
    if k == "def":
        V = [("H est le projeté orthogonal de M sur la droite (d). Que peut-on dire de (MH) ?", "(MH) est perpendiculaire à (d)", ["(MH) est parallèle à (d)", "MH = 0 toujours", "H est le milieu de [M ; (d)]"]),
             ("H est le projeté orthogonal de M sur (d). Pour tout point P de (d), on a…", "MP ⩾ MH", ["MP ⩽ MH", "MP = MH", "MP = 2MH"]),
             ("La distance d’un point M à une droite (d) est…", "la distance MH, où H est le projeté orthogonal de M sur (d)", ["la plus grande distance entre M et un point de (d)", "la distance de M à l’origine", "n’importe quelle distance MP avec P sur (d)"]),
             ("Si M appartient à la droite (d), son projeté orthogonal sur (d) est…", "M lui-même", ["l’origine du repère", "il n’existe pas", "un point quelconque de (d)"])]
        q, a, w = R.choice(V)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    a, b, c = R.choice(TRIP)
    f = R.choice([1, 1, 2, Fr(1, 2)])
    a, b, c = a * f, b * f, c * f
    if k == "dist":
        return M("H est le projeté orthogonal de M sur (d), P un point de (d) avec MP = %s cm et HP = %s cm. Quelle est la distance de M à (d) ?" % (d(c), d(a)), "%s cm" % d(b), ["%s cm" % d(c), "%s cm" % d(c - a), "%s cm" % d(c + a)],
                 "MHP est rectangle en H : MH² = %s² − %s² = %s, donc <b>MH = %s cm</b>." % (d(c), d(a), d(b * b), d(b)))
    return M("H est le projeté orthogonal de M sur (d) avec MH = %s cm. P est un point de (d) avec HP = %s cm. Combien mesure MP ?" % (d(a), d(b)), "%s cm" % d(c), ["%s cm" % d(a + b), "%s cm" % d(b - a), "%s cm" % d(b)],
             "MP² = MH² + HP² = %s + %s = %s, <b>MP = %s cm</b>." % (d(a * a), d(b * b), d(c * c), d(c)))


def s2():
    a, b, c = R.choice(TRIP)
    k = R.choice(["cos", "sin", "tan", "cos2"])
    if k == "cos2":
        cv = Fr(a, c)
        return M("α est un angle aigu avec cos α = %s. Que vaut sin α ?" % fq(cv), fq(Fr(b, c)), [fq(1 - cv), fq(Fr(c, b)), fq(Fr(b, a))],
                 "cos²α + sin²α = 1 : sin²α = 1 − %s = %s, et sin α &gt; 0, donc <b>sin α = %s</b>." % (fq(cv * cv), fq(1 - cv * cv), fq(Fr(b, c))))
    ans = {"cos": Fr(a, c), "sin": Fr(b, c), "tan": Fr(b, a)}[k]
    return M("Dans le triangle ABC rectangle en A, AB = %d, AC = %d et BC = %d. Que vaut %s de l’angle en B ?" % (a, b, c, {"cos": "le cosinus", "sin": "le sinus", "tan": "la tangente"}[k]), fq(ans),
             [fq(x) for x in [Fr(a, c), Fr(b, c), Fr(b, a), Fr(a, b)] if x != ans][:3],
             "Pour l’angle en B : adjacent AB = %d, opposé AC = %d, hypoténuse BC = %d : <b>%s</b>." % (a, b, c, fq(ans)))


def s3():
    k = R.choice(["long", "long", "angle"])
    if k == "long":
        h = R.randint(4, 15)
        ang = R.choice([25, 30, 35, 40, 50, 55, 60])
        f = R.choice(["cos", "sin"])
        v = Fr(round(h * (math.cos if f == "cos" else math.sin)(math.radians(ang)) * 10), 10)
        o = Fr(round(h * (math.sin if f == "cos" else math.cos)(math.radians(ang)) * 10), 10)
        return M("Un triangle est rectangle ; son hypoténuse mesure %d cm et un angle aigu α = %d°. Quelle est la longueur du côté %s à α, arrondie au dixième ?" % (h, ang, "adjacent" if f == "cos" else "opposé"), "%s cm" % d(v),
                 ["%s cm" % d(o), "%s cm" % d(Fr(round(h / (math.cos if f == "cos" else math.sin)(math.radians(ang)) * 10), 10)), "%s cm" % d(Fr(round(h * math.tan(math.radians(ang)) * 10), 10))],
                 "%s α = côté ÷ hypoténuse, donc côté = %d × %s %d° ≈ <b>%s cm</b>." % (f, h, f, ang, d(v)))
    a, b = R.randint(3, 12), R.randint(3, 12)
    ang = round(math.degrees(math.atan(b / a)))
    return M("Un triangle est rectangle avec des côtés de l’angle droit de %d cm et %d cm. Quel est l’angle opposé au côté de %d cm, arrondi au degré ?" % (a, b, b), "%d°" % ang, ["%d°" % (90 - ang) if 90 - ang != ang else "%d°" % (ang + 5), "%d°" % round(math.degrees(math.atan(a / b)) + 2) if round(math.degrees(math.atan(a / b)) + 2) not in (ang, 90 - ang) else "%d°" % (ang + 3), "%d°" % (ang + 1)],
             "tan α = %d ÷ %d, donc α ≈ <b>%d°</b>." % (b, a, ang))


def s4():
    k = R.choice(["tri", "trap", "disque", "cyl", "sphere"])
    if k == "tri":
        b, h = R.randint(3, 20), R.randint(3, 20)
        return M("Quelle est l’aire d’un triangle de base %d cm et de hauteur %d cm ?" % (b, h), "%s cm²" % d(Fr(b * h, 2)), ["%d cm²" % (b * h), "%d cm²" % (b + h), "%s cm²" % d(Fr(b * h, 3))], "A = base × hauteur ÷ 2 = <b>%s cm²</b>." % d(Fr(b * h, 2)))
    if k == "trap":
        B, b, h = R.randint(6, 15), R.randint(2, 5), R.randint(2, 10)
        return M("Quelle est l’aire d’un trapèze de bases %d cm et %d cm et de hauteur %d cm ?" % (B, b, h), "%s cm²" % d(Fr((B + b) * h, 2)), ["%d cm²" % ((B + b) * h), "%d cm²" % (B * b * h), "%s cm²" % d(Fr(B * h, 2))],
                 "A = (B + b) × h ÷ 2 = <b>%s cm²</b>." % d(Fr((B + b) * h, 2)))
    if k == "disque":
        r = R.randint(2, 12)
        return M("Quelle est l’aire exacte d’un disque de rayon %d cm ?" % r, "%dπ cm²" % (r * r), ["%dπ cm²" % (2 * r), "%dπ cm²" % (4 * r * r), "%dπ cm²" % r], "A = πr² = <b>%dπ cm²</b>." % (r * r))
    if k == "cyl":
        r, h = R.randint(2, 8), R.randint(3, 15)
        return M("Quel est le volume exact d’un cylindre de rayon %d cm et de hauteur %d cm ?" % (r, h), "%sπ cm³" % num(r * r * h), ["%sπ cm³" % num(2 * r * h), "%sπ cm³" % num(Fr(r * r * h, 3)) if (r * r * h) % 3 == 0 else "%sπ cm³" % num(r * h), "%sπ cm³" % num(4 * r * r * h)],
                 "V = πr²h = <b>%sπ cm³</b>." % num(r * r * h))
    r = R.choice([3, 6, 9])
    return M("Quel est le volume exact d’une boule de rayon %d cm ?" % r, "%sπ cm³" % num(4 * r ** 3 // 3), ["%sπ cm³" % num(4 * r * r), "%sπ cm³" % num(r ** 3), "%sπ cm³" % num(4 * r ** 3)], "V = 4/3 πr³ = <b>%sπ cm³</b>." % num(4 * r ** 3 // 3))


def s5():
    k = R.choice(["opt", "opt", "aire_sin", "rampe"])
    if k == "opt":
        L_ = R.choice([8, 10, 12, 16, 20])
        h = L_ // 2
        return M("M est sur un segment [AB] de longueur %d cm, avec AM = x. On construit deux carrés de côtés AM et MB. Pour quelle valeur de x la somme de leurs aires est-elle minimale ?" % L_, "x = %d" % h, ["x = 0", "x = %d" % L_, "x = %d" % (h // 2) if h // 2 else "x = 1"],
                 "S(x) = x² + (%d − x)² = 2(x − %d)² + %d : minimum en <b>x = %d</b>." % (L_, h, h * h * 2, h))
    if k == "aire_sin":
        a, b = R.randint(3, 10), R.randint(3, 10)
        ang = R.choice([30, 90, 150])
        A = Fr(a * b, 2) * Fr({30: 1, 90: 2, 150: 1}[ang], 2)
        return M("Un triangle a deux côtés de %d cm et %d cm formant un angle de %d°. Quelle est son aire ? (A = ½ × a × b × sin C)" % (a, b, ang), "%s cm²" % d(A), ["%d cm²" % (a * b), "%s cm²" % d(Fr(a * b, 2)) if Fr(a * b, 2) != A else "%s cm²" % d(A * 2), "%s cm²" % d(A / 2)],
                 "sin %d° = %s : A = ½ × %d × %d × %s = <b>%s cm²</b>." % (ang, d(Fr({30: 1, 90: 2, 150: 1}[ang], 2)), a, b, d(Fr({30: 1, 90: 2, 150: 1}[ang], 2)), d(A)))
    L_ = R.choice([4, 5, 6, 8])
    ang = R.choice([5, 8, 10, 12])
    h = Fr(round(L_ * math.sin(math.radians(ang)) * 100), 100)
    return M("Une rampe de %d m fait un angle de %d° avec le sol. À quelle hauteur monte-t-elle, arrondie au centimètre ?" % (L_, ang), "%s m" % dk(h, 2), ["%s m" % dk(Fr(round(L_ * math.cos(math.radians(ang)) * 100), 100), 2), "%s m" % dk(Fr(round(L_ * math.tan(math.radians(ang)) * 100), 100), 2) if round(L_ * math.tan(math.radians(ang)) * 100) != round(L_ * math.sin(math.radians(ang)) * 100) else "%s m" % dk(h + Fr(1, 10), 2), "%s m" % dk(Fr(L_ * ang, 100), 2)],
             "h = %d × sin %d° ≈ <b>%s m</b>." % (L_, ang, dk(h, 2)))


def main():
    seen = set()
    sets = [("Projeté orthogonal et distance", mix(R, seen, [(s1, 20)])), ("Trigonométrie et cos² + sin² = 1", mix(R, seen, [(s2, 20)])),
            ("Calculer des longueurs et des angles", mix(R, seen, [(s3, 20)])), ("Aires et volumes", mix(R, seen, [(s4, 20)])), ("Problèmes et optimisation", mix(R, seen, [(s5, 20)]))]
    body = L(["Le <b>projeté orthogonal</b> H de M sur (d) est le pied de la perpendiculaire à (d) passant par M ; c’est le point de (d) le plus proche de M (MH est la distance de M à (d)).",
              "Dans un triangle rectangle, pour un angle aigu α : cos α = adjacent ÷ hypoténuse, sin α = opposé ÷ hypoténuse, tan α = opposé ÷ adjacent, et <b>cos²α + sin²α = 1</b>.",
              "On combine Pythagore, la trigonométrie et les formules d’aires et de volumes pour résoudre des problèmes."],
             [("cos α = 0,6", ["sin²α = 1 − 0,36 = 0,64", "sin α &gt; 0"], "sin α = 0,8")],
             [["Mesurer la distance à une droite « en biais »", "On utilise le projeté orthogonal (perpendiculaire)."], ["sin α = 1 − cos α", "C’est sin²α = 1 − cos²α."], ["Oublier ÷ 2 pour l’aire d’un triangle", "A = base × hauteur ÷ 2."]])
    faq = [("Pourquoi cos²α + sin²α = 1 ?", "Parce que (adjacent² + opposé²) ÷ hypoténuse² = 1 d’après le théorème de Pythagore."),
           ("Pourquoi le projeté orthogonal est-il le point le plus proche ?", "Pour tout autre point P de (d), MP est l’hypoténuse du triangle MHP, donc MP &gt; MH.")]
    unit("seconde", R, "geometrie-plane", "G",
         "Résoudre des problèmes de géométrie plane : projeté orthogonal et distance d’un point à une droite, trigonométrie dans le triangle rectangle et relation cos²α + sin²α = 1 ; calculer des longueurs, des angles, des aires et des volumes ; optimiser",
         "Problèmes de géométrie plane", "Géométrie plane",
         "Fiches de maths seconde sur les problèmes de géométrie : projeté orthogonal, distance à une droite, trigonométrie, cos² + sin² = 1, aires, volumes et optimisation. 100 exercices corrigés.",
         "cos²α + sin²α = 1", "Le projeté orthogonal est le point le plus proche", body, faq, sets, 16)


if __name__ == "__main__":
    main()
