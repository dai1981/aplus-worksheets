# -*- coding: utf-8 -*-
"""
France Maths 3e : Trigonométrie dans le triangle rectangle (cosinus, sinus, tangente)
  python3 tools/gen_fr_maths_3e_trigonometrie.py
Erreurs : confondre côté adjacent et côté opposé, prendre l’hypoténuse pour la tangente, calculatrice en radians, diviser au lieu de multiplier.
"""
import random
import math
from fr_c4 import *

R = random.Random(60411)
K = Kids(R)
LET = ["ABC", "EFG", "RST", "KLM", "DEF", "PQR", "IJK", "UVW"]


def tfig(L, a, b, labs, ang=None):
    V, P, Q = L
    pts = {V: (0, 0), P: (a, 0), Q: (0, b)}
    return figure(pts, [(V, P), (P, Q), (Q, V)], labs, right=[(V, P, Q)], label="triangle rectangle")


def s1():
    L = R.choice(LET)
    V, P, Q = L
    k = R.choice(["cos", "sin", "tan"])
    ang = R.choice([P, Q])
    other = Q if ang == P else P
    adj = "%s%s" % ((V, ang) if V < ang else (ang, V))
    opp = "%s%s" % ((V, other) if V < other else (other, V))
    hyp = "%s%s" % ((P, Q) if P < Q else (Q, P))
    ans = {"cos": fr(adj, hyp), "sin": fr(opp, hyp), "tan": fr(opp, adj)}[k]
    w = [x for x in [fr(adj, hyp), fr(opp, hyp), fr(opp, adj), fr(adj, opp)] if x != ans]
    return M("Le triangle %s est rectangle en %s. Que vaut %s de l’angle en %s ?" % (L, V, {"cos": "le cosinus", "sin": "le sinus", "tan": "la tangente"}[k], ang), ans, w,
             "Pour l’angle en %s : côté adjacent [%s], côté opposé [%s], hypoténuse [%s]. %s = <b>%s</b>." % (ang, adj, opp, hyp, {"cos": "cos = adjacent/hypoténuse", "sin": "sin = opposé/hypoténuse", "tan": "tan = opposé/adjacent"}[k], ans))


def s2():
    L = R.choice(LET)
    V, P, Q = L
    a = R.choice([25, 30, 35, 40, 50, 55, 60, 65])
    k = R.choice(["adj", "opp", "opp_t"])
    h = R.randint(4, 15)
    ra = math.radians(a)
    if k == "adj":
        v = Fr(round(h * math.cos(ra) * 10), 10)
        svg = tfig(L, 5, 5 * math.tan(ra), [(P, Q, "%d cm" % h)])
        return M("<div class='qfig'>%s</div>%s est rectangle en %s, l’angle en %s mesure %d° et %s%s = %d cm. Calcule %s%s, arrondi au dixième." % (svg, L, V, P, a, P, Q, h, V, P), "%s cm" % d(v),
                 ["%s cm" % d(Fr(round(h * math.sin(ra) * 10), 10)), "%s cm" % d(Fr(round(h / math.cos(ra) * 10), 10)), "%s cm" % d(Fr(round(h * math.tan(ra) * 10), 10))],
                 "cos %d° = %s%s/%s%s, donc %s%s = %d × cos %d° ≈ <b>%s cm</b>." % (a, V, P, P, Q, V, P, h, a, d(v)))
    if k == "opp":
        v = Fr(round(h * math.sin(ra) * 10), 10)
        svg = tfig(L, 5, 5 * math.tan(ra), [(P, Q, "%d cm" % h)])
        return M("<div class='qfig'>%s</div>%s est rectangle en %s, l’angle en %s mesure %d° et %s%s = %d cm. Calcule %s%s, arrondi au dixième." % (svg, L, V, P, a, P, Q, h, V, Q), "%s cm" % d(v),
                 ["%s cm" % d(Fr(round(h * math.cos(ra) * 10), 10)), "%s cm" % d(Fr(round(h / math.sin(ra) * 10), 10)), "%s cm" % d(Fr(round(h * math.tan(ra) * 10), 10))],
                 "sin %d° = %s%s/%s%s, donc %s%s = %d × sin %d° ≈ <b>%s cm</b>." % (a, V, Q, P, Q, V, Q, h, a, d(v)))
    v = Fr(round(h * math.tan(ra) * 10), 10)
    svg = tfig(L, 5, 5 * math.tan(ra), [(V, P, "%d cm" % h)])
    return M("<div class='qfig'>%s</div>%s est rectangle en %s, l’angle en %s mesure %d° et %s%s = %d cm. Calcule %s%s, arrondi au dixième." % (svg, L, V, P, a, V, P, h, V, Q), "%s cm" % d(v),
             ["%s cm" % d(Fr(round(h * math.sin(ra) * 10), 10)), "%s cm" % d(Fr(round(h / math.tan(ra) * 10), 10)), "%s cm" % d(Fr(round(h * math.cos(ra) * 10), 10))],
             "tan %d° = %s%s/%s%s, donc %s%s = %d × tan %d° ≈ <b>%s cm</b>." % (a, V, Q, V, P, V, Q, h, a, d(v)))


def s3():
    L = R.choice(LET)
    V, P, Q = L
    a, b = R.randint(3, 12), R.randint(3, 12)
    k = R.choice(["tan", "cos", "sin"])
    if k == "tan":
        ang = round(math.degrees(math.atan(b / a)))
        return M("%s est rectangle en %s avec %s%s = %d cm et %s%s = %d cm. Donne la mesure de l’angle en %s, arrondie au degré." % (L, V, V, P, a, V, Q, b, P), "%d°" % ang, ["%d°" % (90 - ang) if 90 - ang != ang else "%d°" % (ang + 5), "%d°" % round(math.degrees(math.atan(a / b)) + 1) if round(math.degrees(math.atan(a / b)) + 1) not in (ang, 90 - ang) else "%d°" % (ang + 3), "%d°" % (ang + 1)],
                 "tan = opposé/adjacent = %d/%d, donc angle = arctan(%d/%d) ≈ <b>%d°</b>." % (b, a, b, a, ang))
    c = max(a, b) + R.randint(1, 6)
    if k == "cos":
        ang = round(math.degrees(math.acos(a / c)))
        return M("%s est rectangle en %s avec %s%s = %d cm et %s%s = %d cm. Donne la mesure de l’angle en %s, arrondie au degré." % (L, V, V, P, a, P, Q, c, P), "%d°" % ang, ["%d°" % (90 - ang) if 90 - ang != ang else "%d°" % (ang + 5), "%d°" % round(math.degrees(math.atan(a / c))), "%d°" % (ang + 1)],
                     "cos = adjacent/hypoténuse = %d/%d, donc angle = arccos(%d/%d) ≈ <b>%d°</b>." % (a, c, a, c, ang))
    ang = round(math.degrees(math.asin(b / c)))
    return M("%s est rectangle en %s avec %s%s = %d cm et %s%s = %d cm. Donne la mesure de l’angle en %s, arrondie au degré." % (L, V, V, Q, b, P, Q, c, P), "%d°" % ang, ["%d°" % (90 - ang) if 90 - ang != ang else "%d°" % (ang + 5), "%d°" % round(math.degrees(math.atan(b / c))), "%d°" % (ang - 1)],
             "sin = opposé/hypoténuse = %d/%d, donc angle = arcsin(%d/%d) ≈ <b>%d°</b>." % (b, c, b, c, ang))


def s4():
    k = R.choice(["hyp", "hyp", "prop", "valeur"])
    L = R.choice(LET)
    V, P, Q = L
    if k == "hyp":
        a = R.choice([30, 35, 40, 50, 60])
        o = R.randint(3, 12)
        v = Fr(round(o / math.sin(math.radians(a)) * 10), 10)
        return M("%s est rectangle en %s, l’angle en %s mesure %d° et %s%s = %d cm. Calcule l’hypoténuse %s%s, arrondie au dixième." % (L, V, P, a, V, Q, o, P, Q), "%s cm" % d(v),
                 ["%s cm" % d(Fr(round(o * math.sin(math.radians(a)) * 10), 10)), "%s cm" % d(Fr(round(o / math.cos(math.radians(a)) * 10), 10)), "%s cm" % d(Fr(round(o * math.tan(math.radians(a)) * 10), 10))],
                 "sin %d° = %d/%s%s, donc %s%s = %d ÷ sin %d° ≈ <b>%s cm</b>." % (a, o, P, Q, P, Q, o, a, d(v)))
    if k == "prop":
        V_ = [("Pour tout angle aigu x, cos²x + sin²x vaut…", "1", ["0", "2", "cela dépend de x"]),
              ("Le cosinus d’un angle aigu est toujours…", "compris entre 0 et 1", ["supérieur à 1", "négatif", "égal à la tangente"]),
              ("Dans un triangle rectangle, si un angle aigu mesure 30°, l’autre mesure…", "60°", ["30°", "90°", "150°"]),
              ("tan x est égal à…", "sin x ÷ cos x", ["cos x ÷ sin x", "sin x × cos x", "1 − cos x"]),
              ("Pour un angle aigu, quand l’angle augmente, son cosinus…", "diminue", ["augmente", "reste le même", "dépasse 1"]),
              ("Le cosinus de 60° vaut…", "0,5", ["√3/2", "1", "60"])]
        q, a_, w = R.choice(V_)
        return M(q, a_, w, "Réponse : <b>%s</b>." % a_)
    a = R.choice([20, 25, 35, 40, 50, 55, 70, 75])
    f = R.choice(["cos", "sin", "tan"])
    v = {"cos": math.cos, "sin": math.sin, "tan": math.tan}[f](math.radians(a))
    vv = Fr(round(v * 100), 100)
    other = {"cos": math.sin, "sin": math.cos, "tan": lambda t: 1 / math.tan(t)}[f](math.radians(a))
    return M("À la calculatrice (en degrés), donne %s %d° arrondi au centième." % (f, a), dk(vv, 2), [dk(Fr(round(other * 100), 100), 2) if round(other * 100) != round(v * 100) else dk(vv + Fr(1, 100), 2), dk(vv + Fr(1, 100), 2) if round(other * 100) != round(v * 100) else dk(vv - Fr(1, 100), 2), dk(Fr(round({"cos": math.cos, "sin": math.sin, "tan": math.tan}[f](a) * 100), 100), 2)],
             "%s %d° ≈ <b>%s</b> (vérifie que la calculatrice est en mode degrés)." % (f, a, dk(vv, 2)))


def s5():
    k = R.choice(["echelle", "rampe", "arbre", "avion", "pente"])
    if k == "echelle":
        L_ = R.choice([4, 5, 6, 8])
        a = R.choice([60, 65, 70, 75])
        h = Fr(round(L_ * math.sin(math.radians(a)) * 100), 100)
        return M("Une échelle de %d m fait un angle de %d° avec le sol. À quelle hauteur touche-t-elle le mur, arrondie au centimètre ?" % (L_, a), "%s m" % dk(h, 2), ["%s m" % dk(Fr(round(L_ * math.cos(math.radians(a)) * 100), 100), 2), "%s m" % dk(Fr(round(L_ * math.tan(math.radians(a)) * 100), 100), 2), "%s m" % dk(Fr(round(L_ / math.sin(math.radians(a)) * 100), 100), 2)],
                 "sin %d° = h/%d, donc h = %d × sin %d° ≈ <b>%s m</b>." % (a, L_, L_, a, dk(h, 2)))
    if k == "rampe":
        h, l = R.choice([(Fr(1, 2), 6), (Fr(3, 10), 4), (1, 12), (Fr(4, 10), 5)])
        ang = Fr(round(math.degrees(math.atan(float(h) / l)) * 10), 10)
        return M("Une rampe monte de %s m sur une distance horizontale de %d m. Quel angle fait-elle avec le sol, arrondi au dixième de degré ?" % (d(h), l), "%s°" % d(ang), ["%s°" % d(Fr(round(math.degrees(math.atan(l / float(h))) * 10), 10)), "%s°" % d(Fr(round(math.degrees(math.asin(float(h) / l)) * 10), 10) + Fr(3, 10)), "%s°" % d(h * 10)],
                 "tan(angle) = %s/%d, donc angle ≈ <b>%s°</b>." % (d(h), l, d(ang)))
    if k == "arbre":
        dd = R.choice([10, 15, 20, 25])
        a = R.choice([30, 35, 40, 45, 50])
        h = Fr(round(dd * math.tan(math.radians(a)) * 10), 10)
        return M("Depuis un point au sol à %d m du pied d’un arbre, on voit son sommet sous un angle de %d°. Quelle est la hauteur de l’arbre, arrondie au dixième ?" % (dd, a), "%s m" % d(h), ["%s m" % d(Fr(round(dd * math.sin(math.radians(a)) * 10), 10)), "%s m" % d(Fr(round(dd / math.tan(math.radians(a)) * 10), 10)) if a != 45 else "%s m" % d(h + 2), "%s m" % d(Fr(round(dd * math.cos(math.radians(a)) * 10), 10))],
                 "tan %d° = h/%d, donc h = %d × tan %d° ≈ <b>%s m</b>." % (a, dd, dd, a, d(h)))
    if k == "avion":
        a = R.choice([5, 8, 10, 12, 15])
        dd = R.choice([2, 3, 5])
        h = round(dd * 1000 * math.sin(math.radians(a)))
        return M("Un avion décolle avec un angle de %d° et parcourt %d km en ligne droite. À quelle altitude est-il, arrondie au mètre ?" % (a, dd), "%s m" % num(h), ["%s m" % num(round(dd * 1000 * math.cos(math.radians(a)))), "%s m" % num(round(dd * 1000 * math.tan(math.radians(a)))), "%s m" % num(round(dd * 1000 / math.sin(math.radians(a))))],
                 "altitude = %s × sin %d° ≈ <b>%s m</b>." % (num(dd * 1000), a, num(h)))
    p = R.choice([5, 8, 10, 12, 15])
    ang = Fr(round(math.degrees(math.atan(p / 100)) * 10), 10)
    return M("Un panneau indique une pente de %d %% (on monte de %d m pour 100 m à l’horizontale). Quel angle fait la route avec l’horizontale, arrondi au dixième de degré ?" % (p, p), "%s°" % d(ang), ["%d°" % p, "%s°" % d(Fr(round(math.degrees(math.asin(p / 100)) * 10), 10) + Fr(1, 10)), "%s°" % d(Fr(p * 90, 100))],
             "tan(angle) = %d/100, donc angle ≈ <b>%s°</b>." % (p, d(ang)))


def main():
    seen = set()
    sets = [("Écrire cos, sin, tan", mix(R, seen, [(s1, 20)])), ("Calculer une longueur", mix(R, seen, [(s2, 20)])),
            ("Calculer un angle", mix(R, seen, [(s3, 20)])), ("Hypoténuse, calculatrice et propriétés", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans un triangle rectangle, pour un angle aigu : <b>cos = adjacent / hypoténuse</b>, <b>sin = opposé / hypoténuse</b>, <b>tan = opposé / adjacent</b> (moyen mnémotechnique : SOH CAH TOA).",
              "Pour calculer une longueur, on écrit la formule avec la longueur inconnue, puis on fait un produit en croix.",
              "Pour calculer un angle, on utilise les touches arccos, arcsin ou arctan (cos⁻¹, sin⁻¹, tan⁻¹) de la calculatrice, réglée en degrés."],
             [("ABC rectangle en A, B̂ = 35°, BC = 8 cm, calculer AB", ["cos 35° = AB/BC", "AB = 8 × cos 35°"], "AB ≈ 6,6 cm")],
             [["Confondre adjacent et opposé", "Le côté adjacent touche l’angle ; l’opposé est en face."], ["Calculatrice en radians", "Vérifie le mode « deg »."],
              ["Écrire AB = 8 ÷ cos 35°", "cos 35° = AB/8, donc AB = 8 × cos 35°."]])
    faq = [("Quelle formule choisir ?", "Celle qui utilise la longueur connue et la longueur cherchée (par rapport à l’angle connu)."),
           ("La trigonométrie marche-t-elle dans tous les triangles ?", "Les formules cos, sin, tan du collège ne s’utilisent que dans un triangle rectangle.")]
    unit("3e", R, "trigonometrie", "E",
         "Connaître et utiliser le cosinus, le sinus et la tangente d’un angle aigu dans un triangle rectangle pour calculer une longueur ou un angle ; utiliser la calculatrice ; résoudre des problèmes",
         "Trigonométrie dans le triangle rectangle", "Trigonométrie",
         "Fiches de maths 3e sur la trigonométrie : cosinus, sinus, tangente, calculer une longueur ou un angle, calculatrice et problèmes, avec figures. 100 exercices corrigés.",
         "cos = adj/hyp ; sin = opp/hyp ; tan = opp/adj", "SOH CAH TOA", body, faq, sets, 11)


if __name__ == "__main__":
    main()
