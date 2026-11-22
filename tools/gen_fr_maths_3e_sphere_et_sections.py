# -*- coding: utf-8 -*-
"""
France Maths 3e : Sphère et boule, sections de solides, repérage sur la sphère terrestre
  python3 tools/gen_fr_maths_3e_sphere_et_sections.py
Erreurs : utiliser le diamètre au lieu du rayon, confondre aire (4πr²) et volume (4/3 πr³), croire que toutes les sections d’un cube sont des carrés.
"""
import random
import math
from fr_c4 import *

R = random.Random(60413)
K = Kids(R)


def s1():
    r = R.randint(1, 12)
    k = R.choice(["aire", "vol", "aire_arr", "vol_arr", "diam"])
    if k == "aire":
        return M("Quelle est l’aire exacte d’une sphère de rayon %d cm ?" % r, "%sπ cm²" % num(4 * r * r), ["%sπ cm²" % num(r * r), "%sπ cm²" % num(Fr(4 * r ** 3, 3)) if Fr(4 * r ** 3, 3).denominator == 1 else "%sπ cm²" % num(2 * r * r), "%sπ cm²" % num(8 * r)],
                 "A = 4πr² = 4π × %d² = <b>%sπ cm²</b>." % (r, num(4 * r * r)))
    if k == "vol":
        if (4 * r ** 3) % 3:
            return None
        return M("Quel est le volume exact d’une boule de rayon %d cm ?" % r, "%sπ cm³" % num(4 * r ** 3 // 3), ["%sπ cm³" % num(4 * r * r), "%sπ cm³" % num(r ** 3), "%sπ cm³" % num(4 * r ** 3)],
                 "V = 4/3 × π × r³ = 4/3 × π × %s = <b>%sπ cm³</b>." % (num(r ** 3), num(4 * r ** 3 // 3)))
    if k == "aire_arr":
        v = Fr(round(4 * math.pi * r * r * 10), 10)
        return M("Donne l’aire d’une sphère de rayon %d cm, arrondie au dixième." % r, "%s cm²" % d(v), ["%s cm²" % d(Fr(round(math.pi * r * r * 10), 10)), "%s cm²" % d(Fr(round(4 / 3 * math.pi * r ** 3 * 10), 10)), "%s cm²" % d(Fr(round(4 * math.pi * r * 10), 10))],
                 "4 × π × %d² ≈ <b>%s cm²</b>." % (r, d(v)))
    if k == "vol_arr":
        v = Fr(round(4 / 3 * math.pi * r ** 3 * 10), 10)
        return M("Donne le volume d’une boule de rayon %d cm, arrondi au dixième." % r, "%s cm³" % d(v), ["%s cm³" % d(Fr(round(4 * math.pi * r * r * 10), 10)), "%s cm³" % d(Fr(round(math.pi * r ** 3 * 10), 10)), "%s cm³" % d(Fr(round(4 / 3 * math.pi * (2 * r) ** 3 * 10), 10))],
                 "4/3 × π × %d³ ≈ <b>%s cm³</b>." % (r, d(v)))
    D = 2 * r
    v = Fr(round(4 / 3 * math.pi * r ** 3 * 10), 10)
    return M("Un ballon a un diamètre de %d cm. Quel est son volume, arrondi au dixième ?" % D, "%s cm³" % d(v), ["%s cm³" % d(Fr(round(4 / 3 * math.pi * D ** 3 * 10), 10)), "%s cm³" % d(Fr(round(4 * math.pi * r * r * 10), 10)), "%s cm³" % d(Fr(round(4 / 3 * math.pi * r * r * 10), 10))],
             "Rayon = %d ÷ 2 = %d cm ; V = 4/3 × π × %d³ ≈ <b>%s cm³</b>." % (D, r, r, d(v)))


def s2():
    a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25)])
    f = R.choice([1, 1, 2, Fr(1, 2)])
    a, b, c = a * f, b * f, c * f
    if R.random() < 0.5:
        a, b = b, a
    k = R.choice(["rayon", "rayon", "dist", "nature"])
    if k == "rayon":
        return M("On coupe une boule de rayon %s cm par un plan situé à %s cm du centre. Quel est le rayon du cercle de section ?" % (d(c), d(a)), "%s cm" % d(b), ["%s cm" % d(c - a), "%s cm" % d(c), "%s cm" % d(Fr(round(math.sqrt(c * c + a * a) * 10), 10))],
                 "Avec Pythagore : r² = %s² − %s² = %s, donc <b>r = %s cm</b>." % (d(c), d(a), d(b * b), d(b)))
    if k == "dist":
        return M("Une sphère de rayon %s cm est coupée par un plan ; la section est un cercle de rayon %s cm. À quelle distance du centre est le plan ?" % (d(c), d(b)), "%s cm" % d(a), ["%s cm" % d(c - b), "%s cm" % d(b), "%s cm" % d(c + b)],
                 "d² = %s² − %s² = %s, donc <b>d = %s cm</b>." % (d(c), d(b), d(a * a), d(a)))
    V_ = [("La section d’une sphère par un plan est…", "un cercle (ou un point)", ["un carré", "une ellipse", "toujours un grand cercle"]),
          ("Quand le plan passe par le centre de la sphère, la section est…", "un grand cercle de même rayon que la sphère", ["un point", "un cercle plus petit", "une droite"]),
          ("Plus le plan est loin du centre, plus le cercle de section est…", "petit", ["grand", "le même", "elliptique"])]
    q, a_, w = R.choice(V_)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s3():
    V_ = [("La section d’un pavé droit par un plan parallèle à une face est…", "un rectangle de mêmes dimensions que cette face", ["un triangle", "un cercle", "un rectangle plus petit"]),
          ("La section d’un pavé droit par un plan parallèle à une arête est…", "un rectangle", ["un cercle", "un triangle", "un trapèze quelconque"]),
          ("La section d’un cylindre par un plan perpendiculaire à son axe est…", "un disque de même rayon que la base", ["un rectangle", "une ellipse", "un disque plus petit"]),
          ("La section d’un cylindre par un plan parallèle à son axe est…", "un rectangle", ["un disque", "un triangle", "un carré toujours"]),
          ("La section d’une pyramide par un plan parallèle à sa base est…", "une réduction de la base", ["un agrandissement de la base", "toujours un carré", "un triangle quelconque"]),
          ("La section d’un cône de révolution par un plan parallèle à sa base est…", "un disque", ["un triangle", "un rectangle", "un carré"]),
          ("La section d’un cône de révolution par un plan contenant son axe est…", "un triangle isocèle", ["un disque", "un rectangle", "un triangle rectangle quelconque"]),
          ("La section d’un cube par un plan parallèle à une face est…", "un carré", ["un rectangle non carré", "un triangle", "un hexagone"])]
    q, a_, w = R.choice(V_)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s3b():
    k = R.choice(["pyr", "cone", "pave"])
    if k == "pyr":
        c = R.choice([6, 8, 9, 12])
        h = R.choice([9, 12, 15])
        t = R.choice([Fr(1, 3), Fr(2, 3), Fr(1, 2)])
        return M("Une pyramide a une base carrée de côté %d cm et une hauteur de %d cm. On la coupe parallèlement à la base, à %s cm du sommet. Quel est le côté de la section ?" % (c, h, d(h * t)), "%s cm" % d(c * t), ["%s cm" % d(c * (1 - t)), "%s cm" % d(c * t * t), "%d cm" % c],
                 "La section est une réduction de rapport %s ÷ %d = %s : %d × %s = <b>%s cm</b>." % (d(h * t), h, fq(t), c, fq(t), d(c * t)))
    if k == "cone":
        r = R.choice([6, 9, 12])
        h = R.choice([8, 12, 15])
        t = R.choice([Fr(1, 3), Fr(2, 3)])
        return M("Un cône a un rayon de base de %d cm et une hauteur de %d cm. On le coupe parallèlement à la base, à %s cm du sommet. Quel est le rayon de la section ?" % (r, h, d(h * t)), "%s cm" % d(r * t), ["%s cm" % d(r * (1 - t)), "%s cm" % d(r * t * t), "%d cm" % r],
                 "Rapport de réduction %s : %d × %s = <b>%s cm</b>." % (fq(t), r, fq(t), d(r * t)))
    a, b, c = R.randint(3, 10), R.randint(3, 10), R.randint(3, 10)
    return M("Un pavé droit mesure %d cm × %d cm × %d cm. On le coupe par un plan parallèle à la face de %d cm × %d cm. Quelle est l’aire de la section ?" % (a, b, c, a, b), "%d cm²" % (a * b), ["%d cm²" % (a * c), "%d cm²" % (b * c), "%d cm²" % (a * b * c)],
             "La section est un rectangle identique à cette face : %d × %d = <b>%d cm²</b>." % (a, b, a * b))


def s4():
    k = R.choice(["lat", "lat", "lon", "voc"])
    if k == "lat":
        v = R.randint(1, 80)
        ns = R.choice(["N", "S"])
        return M("Un point a pour latitude %d° %s. Où se trouve-t-il ?" % (v, ns), "dans l’hémisphère %s" % ("Nord" if ns == "N" else "Sud"), ["dans l’hémisphère %s" % ("Sud" if ns == "N" else "Nord"), "sur l’équateur", "sur le méridien de Greenwich"],
                 "La latitude se mesure à partir de l’<b>équateur</b> ; %s indique l’hémisphère <b>%s</b>." % (ns, "Nord" if ns == "N" else "Sud"))
    if k == "lon":
        v = R.randint(1, 170)
        eo = R.choice(["E", "O"])
        return M("Un point a pour longitude %d° %s. Par rapport au méridien de Greenwich, il est…" % (v, eo), "à l’%s" % ("est" if eo == "E" else "ouest"), ["à l’%s" % ("ouest" if eo == "E" else "est"), "au nord", "au sud"],
                 "La longitude se mesure à partir du méridien de Greenwich : <b>%s</b>." % ("est" if eo == "E" else "ouest"))
    V_ = [("L’équateur est…", "le grand cercle de latitude 0°", ["le méridien de longitude 0°", "un cercle passant par les pôles", "le cercle de latitude 90°"]),
          ("Le pôle Nord a pour latitude…", "90° N", ["0°", "180°", "90° E"]),
          ("Paris a pour coordonnées environ 49° N, 2° E. Quelle ville est dans l’hémisphère Sud ?", "Le Cap (34° S, 18° E)", ["Londres (51° N, 0°)", "New York (41° N, 74° O)", "Tokyo (36° N, 140° E)"]),
          ("Un méridien est…", "un demi-cercle qui va d’un pôle à l’autre", ["un cercle parallèle à l’équateur", "l’équateur", "un cercle de latitude 45°"]),
          ("Les parallèles sont…", "des cercles parallèles à l’équateur", ["des demi-cercles passant par les pôles", "des droites", "des méridiens"])]
    q, a_, w = R.choice(V_)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s5():
    k = R.choice(["terre", "ballon", "boules", "demi", "peinture", "cube", "cube"])
    if k == "cube":
        r = R.randint(2, 9)
        v = round((2 * r) ** 3 - 4 / 3 * math.pi * r ** 3)
        return M("Une boule de rayon %d cm est placée dans une boîte cubique de %d cm de côté. Quel volume reste vide, arrondi au cm³ ?" % (r, 2 * r), "%s cm³" % num(v), ["%s cm³" % num(round(4 / 3 * math.pi * r ** 3)), "%s cm³" % num((2 * r) ** 3), "%s cm³" % num(round((2 * r) ** 3 - 4 * math.pi * r * r))],
                 "Cube : %s cm³ ; boule : 4/3 × π × %d³ ≈ %s cm³ ; différence ≈ <b>%s cm³</b>." % (num((2 * r) ** 3), r, num(round(4 / 3 * math.pi * r ** 3)), num(v)))
    if k == "terre":
        r = 6371
        v = round(4 * math.pi * r * r / 1e6)
        return M("La Terre est assimilée à une sphère de rayon 6 371 km. Quelle est son aire, en millions de km², arrondie à l’unité ?", "%d millions de km²" % v, ["%d millions de km²" % round(math.pi * r * r / 1e6), "%d millions de km²" % round(4 / 3 * math.pi * r ** 3 / 1e9), "%d millions de km²" % round(4 * math.pi * r / 1e3)],
                 "4 × π × 6 371² ≈ 510 000 000 km² : <b>%d millions de km²</b>." % v)
    if k == "ballon":
        r = R.choice([11, 12, 15, 20])
        v = Fr(round(4 / 3 * math.pi * r ** 3 / 1000 * 10), 10)
        return M("Un ballon a un rayon de %d cm. Quel volume d’air contient-il, en litres, arrondi au dixième ?" % r, "%s L" % d(v), ["%s L" % d(v * 10), "%s L" % d(Fr(round(4 * math.pi * r * r / 1000 * 10), 10)), "%s L" % d(Fr(round(4 / 3 * math.pi * (2 * r) ** 3 / 1000 * 10), 10))],
                 "V = 4/3 × π × %d³ ≈ %s cm³ = <b>%s L</b>." % (r, num(round(4 / 3 * math.pi * r ** 3)), d(v)))
    if k == "boules":
        r = R.choice([2, 3, 4])
        n = R.choice([2, 3])
        return M("Une boîte cylindrique contient exactement %d balles de rayon %d cm empilées. Quelle est la hauteur de la boîte ?" % (n, r), "%d cm" % (2 * r * n), ["%d cm" % (r * n), "%d cm" % (2 * r), "%d cm" % (4 * r * n)],
                 "Chaque balle a un diamètre de %d cm : %d × %d = <b>%d cm</b>." % (2 * r, n, 2 * r, 2 * r * n))
    if k == "demi":
        r = R.choice([3, 6, 9])
        return M("Un bol a la forme d’une demi-boule de rayon %d cm. Quelle est sa contenance exacte ?" % r, "%sπ cm³" % num(Fr(2 * r ** 3, 3)), ["%sπ cm³" % num(Fr(4 * r ** 3, 3)), "%sπ cm³" % num(2 * r * r), "%sπ cm³" % num(r ** 3)],
                 "Demi-boule : 1/2 × 4/3 × π × %d³ = <b>%sπ cm³</b>." % (r, num(Fr(2 * r ** 3, 3))))
    r = R.choice([1, 2, 3])
    return M("On peint une boule décorative de %d m de rayon. 1 L de peinture couvre 10 m². Combien de litres faut-il, arrondi au dixième ?" % r, "%s L" % d(Fr(round(4 * math.pi * r * r), 10)), ["%s L" % d(Fr(round(4 / 3 * math.pi * r ** 3), 10)), "%s L" % d(Fr(round(math.pi * r * r), 10)), "%s L" % d(Fr(round(4 * math.pi * r * r * 10), 10))],
             "Aire = 4π × %d² ≈ %s m² ; ÷ 10 = <b>%s L</b>." % (r, d(Fr(round(4 * math.pi * r * r * 10), 10)), d(Fr(round(4 * math.pi * r * r), 10))))


def main():
    seen = set()
    sets = [("Aire et volume de la boule", mix(R, seen, [(s1, 20)])), ("Sections d’une sphère", mix(R, seen, [(s2, 20)])),
            ("Sections d’autres solides", mix(R, seen, [(s3, 8), (s3b, 12)])), ("Se repérer sur la Terre", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Aire d’une sphère de rayon r : <b>A = 4πr²</b>. Volume d’une boule : <b>V = 4/3 × π × r³</b>.",
              "La section d’une sphère par un plan est un cercle. Si le plan est à la distance d du centre, son rayon vérifie r’² = r² − d² (Pythagore).",
              "Sur la Terre, un point est repéré par sa latitude (nord ou sud de l’équateur) et sa longitude (est ou ouest du méridien de Greenwich)."],
             [("Boule de rayon 3 cm", ["A = 4π × 9 = 36π", "V = 4/3 × π × 27 = 36π"], "36π cm² et 36π cm³")],
             [["Prendre le diamètre comme rayon", "r = diamètre ÷ 2."], ["Confondre 4πr² et 4/3 πr³", "L’aire est en cm², le volume en cm³."], ["Croire que les sections d’un cube sont toujours des carrés", "On peut obtenir des rectangles, des triangles…"]])
    faq = [("Quelle différence entre sphère et boule ?", "La sphère est la surface (la peau du ballon) ; la boule est le solide plein."),
           ("Pourquoi les sections parallèles à la base d’une pyramide sont-elles des réductions ?", "D’après le théorème de Thalès, toutes les longueurs sont multipliées par le même rapport.")]
    unit("3e", R, "sphere-et-sections", "E",
         "Calculer l’aire d’une sphère et le volume d’une boule ; connaître la nature des sections planes d’une sphère, d’un pavé, d’un cylindre, d’une pyramide et d’un cône ; se repérer sur la sphère terrestre",
         "Sphère, boule et sections de solides", "Sphère et sections",
         "Fiches de maths 3e sur la sphère et la boule : aire, volume, sections planes de solides, latitude et longitude, problèmes. 100 exercices corrigés.",
         "Sphère : A = 4πr² ; boule : V = 4/3 πr³", "Section d’une sphère : un cercle", body, faq, sets, 13)


if __name__ == "__main__":
    main()
