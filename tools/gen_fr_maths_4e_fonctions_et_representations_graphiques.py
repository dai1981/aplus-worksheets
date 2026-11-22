# -*- coding: utf-8 -*-
"""
France Maths 4e : Grandeurs en fonction d’une autre — formules, tableaux, graphiques
  python3 tools/gen_fr_maths_4e_fonctions_et_representations_graphiques.py
Erreurs : lire l’axe horizontal à la place du vertical, (−3)² = −9 dans une formule, confondre augmentation et proportionnalité.
"""
import random
from fr_c4 import *
import de_k10

R = random.Random(60310)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1():
    k = R.choice(["lin", "carre", "carre", "frac"])
    x = nz(-6, 8)
    if k == "lin":
        a, b = nz(-6, 6), R.randint(-9, 9)
        f, form = a * x + b, expr([(a, "x"), (b, "")])
        w = [a + x + b, a * (x + b), -(a * x) + b]
    elif k == "carre":
        a, b = R.choice([1, 2, -1, 3]), R.randint(-9, 9)
        f, form = a * x * x + b, expr([(a, "x²"), (b, "")])
        w = [a * 2 * x + b, -a * x * x + b if x < 0 else a * x + b, (a * x) ** 2 + b if a != 1 else a * x * x - b]
    else:
        a = R.choice([2, 3, 4])
        b = R.randint(1, 9)
        if (x + b) % a:
            return None
        f, form = Fr(x + b, a), "(x + %d) ÷ %d" % (b, a)
        w = [Fr(x, a) + b, x + Fr(b, a), (x + b) * a]
    ws = [d(v) if Fr(v).denominator in (1, 2, 4, 5) else fq(v) for v in w if v != f]
    return M("On calcule y avec la formule y%s=%s%s. Que vaut y pour x = %s ?" % (NB, NB, form.replace(" ", NB), d(x)), d(f), ws, "On remplace x par %s : <b>%s</b>." % (par(x), d(f)))


def courbe():
    k = R.choice(["lin", "dec", "par", "pal"])
    if k == "lin":
        a, b = R.choice([1, 2, 3]), R.randint(0, 6)
        f = lambda x: a * x + b
    elif k == "dec":
        b = R.choice([20, 24, 28])
        f = lambda x: b - 2 * x
    elif k == "par":
        c = R.randint(3, 7)
        f = lambda x: (x - c) ** 2 / Fr(2) + 2 if isinstance(x, int) else (x - c) ** 2 / 2 + 2
    else:
        f = lambda x: 2 * x if x <= 5 else 10 + (0 if x <= 7 else 3 * (x - 7))
    return f


def s2():
    f = courbe()
    pts = [(x, f(x)) for x in range(0, 11) if 0 <= f(x) <= 30 and Fr(f(x)).denominator == 1]
    if len(pts) < 5:
        return None
    top = 30 if max(y for _, y in pts) > 20 else 20
    svg = relabel(de_k10.kurve([(lambda x: float(f(x)), BLUE, "")], (0, 10, 1), (0, top, 2 if top == 20 else 5), W=380, H=270), "courbe dans un repère")
    x, y = R.choice(pts)
    k = R.choice(["img", "img", "ant", "max"])
    if k == "img":
        return M("<div class='qfig'>%s</div>Lis sur le graphique la valeur de y quand x = %d." % (svg, x), d(y), [d(y + 1), d(x) if x != y else d(y + 2), d(y - 2) if y >= 2 else d(y + 3)],
                 "On part de %d sur l’axe horizontal, on monte jusqu’à la courbe et on lit sur l’axe vertical : <b>%s</b>." % (x, d(y)))
    if k == "ant":
        xs = [xx for xx, yy in pts if yy == y]
        ans = " et ".join("x = %d" % xx for xx in xs)
        w = ["x = %s" % d(y) if y not in xs else "x = %d" % (xs[0] + 1), "x = %d" % (xs[-1] + 1), "x = %d" % (xs[0] - 1 if xs[0] > 0 else xs[0] + 2)]
        return M("<div class='qfig'>%s</div>Pour quelle(s) valeur(s) de x a-t-on y = %s ?" % (svg, d(y)), ans, w,
                 "On part de %s sur l’axe vertical, on va jusqu’à la courbe, puis on lit sur l’axe horizontal : <b>%s</b>." % (d(y), ans))
    ys = [yy for _, yy in pts]
    if len(pts) < 11:
        return None
    mx = max(ys)
    xm = [xx for xx, yy in pts if yy == mx]
    return M("<div class='qfig'>%s</div>Pour x entre 0 et 10, quelle est la plus grande valeur de y ?" % svg, d(mx), [d(min(ys)), d(xm[0]) if xm[0] != mx else d(mx + 1), "10"] if mx != 10 else [d(min(ys)), d(mx + 1), d(mx - 2)],
             "Le point le plus haut de la courbe a pour ordonnée <b>%s</b>." % d(mx))


def s3():
    k = R.choice(["tab", "tab", "form"])
    a, b = R.randint(2, 6), R.randint(1, 15)
    if k == "tab":
        xs = sorted(R.sample(range(0, 11), 4))
        ys = [a * x + b for x in xs]
        tb = table(["x"] + [str(x) for x in xs], [["y"] + [str(y) for y in ys]])
        ans = "y = %dx + %d" % (a, b)
        return M("%s<br>Quelle formule correspond à ce tableau ?" % tb, ans, ["y = %s" % expr([(a + b, "x")]), "y = %s" % expr([(b, "x"), (a, "")]), "y = %s" % expr([(1, "x"), (a + b, "")])],
                 "Quand x augmente de 1, y augmente de %d ; pour x = 0, y = %d : <b>%s</b>." % (a, b, ans))
    V = [("Le prix P d’un trajet en taxi : %d € de prise en charge et %d € par km. Quelle formule donne P en fonction du nombre de km x ?" % (b, a), "P = %dx + %d" % (a, b), ["P = %d(x + %d)" % (a, b), "P = %dx + %d" % (b, a), "P = %dx" % (a + b)]),
         ("L’aire A d’un disque de rayon r est…", "A = πr²", ["A = 2πr", "A = πr", "A = (πr)²"]),
         ("Le périmètre P d’un carré de côté c est…", "P = 4c", ["P = c²", "P = c + 4", "P = 2c"]),
         ("Le volume V d’un cube d’arête a est…", "V = a³", ["V = 3a", "V = a²", "V = 6a²"]),
         ("Une bougie de %d cm diminue de %d cm par heure. Quelle formule donne sa hauteur h après t heures ?" % (b + 20, a % 3 + 1), "h = %d − %dt" % (b + 20, a % 3 + 1), ["h = %dt − %d" % (a % 3 + 1, b + 20), "h = %d + %dt" % (b + 20, a % 3 + 1), "h = %dt" % (b + 20)])]
    q, ans, w = R.choice(V)
    return M(q, ans, w, "<b>%s</b>." % ans)


def s4():
    k = R.choice(["lecture", "lecture", "sens"])
    hs = list(range(0, 13, 2))
    temps = [R.randint(-4, 2)]
    for _ in hs[1:]:
        temps.append(temps[-1] + R.choice([1, 2, 3, -1, -2]))
    pts = list(zip(hs, temps))
    lo, hi = min(-6, min(temps) - 2), max(temps) + 2
    lo -= lo % 2
    hi += hi % 2

    def g(x):
        j = min(int(x // 2), len(hs) - 2)
        return temps[j] + (temps[j + 1] - temps[j]) * (x - hs[j]) / 2.0
    svg = relabel(de_k10.kurve([(g, BLUE, "")], (0, 12, 2), (lo, hi, 2), pts=[(x, y, "") for x, y in pts], W=380, H=270), "températures relevées")
    i = R.randrange(len(hs))
    if k == "lecture":
        return M("<div class='qfig'>%s</div>Températures (en °C) relevées de 0 h à 12 h. Quelle température faisait-il à %d h ?" % (svg, hs[i]), "%s °C" % d(temps[i]), ["%s °C" % d(temps[i] + 1), "%s °C" % d(-temps[i]) if temps[i] else "1 °C", "%d °C" % hs[i] if hs[i] != temps[i] else "%s °C" % d(temps[i] - 2)],
                 "On lit l’ordonnée du point d’abscisse %d : <b>%s °C</b>." % (hs[i], d(temps[i])))
    j = R.randrange(len(hs) - 1)
    dv = temps[j + 1] - temps[j]
    ans = "elle augmente" if dv > 0 else "elle baisse" if dv < 0 else "elle reste la même"
    return M("<div class='qfig'>%s</div>Températures (en °C) relevées de 0 h à 12 h. Entre %d h et %d h, comment évolue la température ?" % (svg, hs[j], hs[j + 1]), ans,
             [x for x in ["elle augmente", "elle baisse", "elle reste la même", "on ne peut pas savoir"] if x != ans], "Elle passe de %s °C à %s °C : <b>%s</b>." % (d(temps[j]), d(temps[j + 1]), ans))


def s5():
    p = K.next()
    k = R.choice(["tarifs", "tarifs", "tableur", "dependance"])
    if k == "tarifs":
        a1, b1, a2 = R.randint(3, 6), R.randint(10, 30), 0
        a2 = a1 + R.randint(2, 4)
        n = Fr(b1, a2 - a1)
        if n.denominator != 1:
            return None
        x = R.randint(1, 20)
        c1, c2 = a1 * x + b1, a2 * x
        if c1 == c2:
            ans = "les deux tarifs coûtent pareil"
        else:
            ans = "le tarif A" if c1 < c2 else "le tarif B"
        return M("Cinéma : tarif A = %d € par séance + carte de %d € ; tarif B = %d € par séance. Pour %d séances, quel tarif est le moins cher ?" % (a1, b1, a2, x), ans,
                 [o for o in ["le tarif A", "le tarif B", "les deux tarifs coûtent pareil", "on ne peut pas savoir"] if o != ans][:3],
                 "A : %d × %d + %d = %d € ; B : %d × %d = %d € : <b>%s</b>. (Les tarifs sont égaux pour %d séances.)" % (a1, x, b1, c1, a2, x, c2, ans, n))
    if k == "tableur":
        a, b = R.randint(2, 9), R.randint(1, 9)
        return M("Dans un tableur, A2 contient x. Quelle formule écrire en B2 pour calculer 3x² − %dx + %d ?" % (a, b), "=3*A2^2-%d*A2+%d" % (a, b), ["=3A2^2-%dA2+%d" % (a, b), "=(3*A2)^2-%d*A2+%d" % (a, b), "3*A2*2-%d*A2+%d" % (a, b)],
                 "On écrit * pour multiplier et ^2 pour le carré, en commençant par = : <b>=3*A2^2-%d*A2+%d</b>." % (a, b))
    V = [("Le prix payé dépend du nombre de croissants achetés. Quelle est la grandeur qui « dépend » de l’autre ?", "le prix payé", ["le nombre de croissants", "aucune", "les deux en même temps"]),
         ("Sur un graphique « distance en fonction du temps », où lit-on le temps ?", "sur l’axe horizontal", ["sur l’axe vertical", "sur la courbe seulement", "dans la légende"]),
         ("Une courbe « hauteur d’eau en fonction du temps » est horizontale entre 2 min et 5 min. Que se passe-t-il ?", "la hauteur ne change pas", ["la hauteur augmente", "la hauteur baisse", "le temps s’arrête"]),
         ("Le périmètre d’un carré est-il proportionnel à son côté ?", "oui (P = 4c)", ["non", "seulement pour les grands carrés", "oui, comme son aire"]),
         ("L’aire d’un carré est-elle proportionnelle à son côté ?", "non (A = c²)", ["oui (A = 4c)", "oui, toujours", "seulement si c &gt; 1"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def main():
    seen = set()
    sets = [("Calculer avec une formule", mix(R, seen, [(s1, 20)])), ("Lire un graphique", mix(R, seen, [(s2, 20)])),
            ("Trouver une formule", mix(R, seen, [(s3, 20)])), ("Interpréter une courbe", mix(R, seen, [(s4, 20)])), ("Problèmes et tableur", mix(R, seen, [(s5, 20)]))]
    body = L(["Quand une grandeur y dépend d’une grandeur x, on peut décrire le lien par une <b>formule</b>, un <b>tableau</b> ou un <b>graphique</b>.",
              "Sur un graphique, x se lit sur l’axe horizontal (abscisses) et y sur l’axe vertical (ordonnées).",
              "Pour calculer y, on remplace x par sa valeur dans la formule, en respectant les priorités (attention aux carrés de nombres négatifs)."],
             [("y = 2x² − 3 pour x = −4", ["2 × (−4)² − 3", "2 × 16 − 3"], "29")],
             [["Lire x à la place de y sur le graphique", "On part de l’axe horizontal et on lit sur l’axe vertical."], ["(−4)² = −16", "(−4)² = (−4) × (−4) = 16."],
              ["Croire que tout ce qui augmente est proportionnel", "Il faut un coefficient constant (y = kx)."]])
    faq = [("Qu’est-ce qu’une grandeur « en fonction » d’une autre ?", "C’est une grandeur dont la valeur est déterminée par l’autre, comme le prix en fonction de la quantité achetée."),
           ("Pourquoi relier les points d’un graphique ?", "Seulement quand la grandeur varie de façon continue (température, distance) ; pour des quantités entières, on laisse des points.")]
    unit("4e", R, "fonctions-et-representations-graphiques", "F",
         "Exprimer une grandeur en fonction d’une autre par une formule ; calculer une valeur à l’aide d’une formule ; lire et interpréter un tableau de valeurs et un graphique ; utiliser un tableur",
         "Grandeurs en fonction d’une autre : formules et graphiques", "Formules et représentations graphiques",
         "Fiches de maths 4e sur les grandeurs en fonction d’une autre : formules, tableaux de valeurs, lecture de graphiques, tableur et problèmes. 100 exercices corrigés.",
         "Formule, tableau ou graphique décrivent le même lien", "x en abscisses, y en ordonnées", body, faq, sets, 10)


if __name__ == "__main__":
    main()
