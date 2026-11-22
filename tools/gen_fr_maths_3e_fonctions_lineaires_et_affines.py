# -*- coding: utf-8 -*-
"""
France Maths 3e : Fonctions linéaires et affines
  python3 tools/gen_fr_maths_3e_fonctions_lineaires_et_affines.py
Erreurs : a = (y2 − y1) ÷ (x2 + x1), confondre coefficient directeur et ordonnée à l’origine, croire qu’une fonction affine est proportionnelle.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60409)
K = Kids(R)
FN = ["f", "g", "h"]


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def s1():
    k = R.choice(["nature", "nature", "coef"])
    if k == "nature":
        V = [(E((nz(-9, 9), "x")), "linéaire (donc aussi affine)"), (E((nz(-9, 9), "x"), (nz(-9, 9), "")), "affine, mais pas linéaire"),
             (E((1, "x²"), (nz(-9, 9), "")), "ni linéaire ni affine"), (d(nz(-9, 9)), "affine (constante), mais pas linéaire"), ("%s" % fr(1, "x"), "ni linéaire ni affine")]
        form, ans = R.choice(V)
        opts = ["linéaire (donc aussi affine)", "affine, mais pas linéaire", "ni linéaire ni affine", "affine (constante), mais pas linéaire"]
        return M("La fonction f : x ↦ %s est…" % form, ans, [o for o in opts if o != ans], "f(x) = ax est linéaire ; f(x) = ax + b est affine ; <b>%s</b>." % ans)
    a, b = nz(-9, 9), nz(-9, 9)
    q = R.choice(["a", "b"])
    return M("Pour f(x) = %s, quel est %s ?" % (E((a, "x"), (b, "")), "le coefficient directeur" if q == "a" else "l’ordonnée à l’origine"), d(a if q == "a" else b), [d(b if q == "a" else a), d(-a if q == "a" else -b), d(a + b)],
             "f(x) = ax + b avec a = %s (coefficient directeur) et b = %s (ordonnée à l’origine) : <b>%s</b>." % (d(a), d(b), d(a if q == "a" else b)))


def s2():
    k = R.choice(["lin", "lin", "aff", "aff"])
    f = R.choice(FN)
    if k == "lin":
        a = nz(-6, 6)
        x1 = nz(-5, 6)
        x2 = nz(-6, 8)
        if x1 == x2:
            return None
        return M("%s est une fonction linéaire telle que %s(%s) = %s. Que vaut %s(%s) ?" % (f, f, d(x1), d(a * x1), f, d(x2)), d(a * x2), [d(a * x1 + x2 - x1), d(Fr(x2, a)) if (Fr(x2, a) * 10).denominator == 1 else d(a * x2 + 1), d(a * x1 * x2)],
                 "a = %s ÷ %s = %s, donc %s(%s) = %s × %s = <b>%s</b>." % (d(a * x1), par(x1), d(a), f, d(x2), d(a), par(x2), d(a * x2)))
    a, b = nz(-5, 5), R.randint(-9, 9)
    x1, x2 = R.sample(range(-5, 7), 2)
    y1, y2 = a * x1 + b, a * x2 + b
    q = R.choice(["a", "b"])
    w_a = [d(Fr(y2 - y1, x2 + x1)) if x2 + x1 and (Fr(y2 - y1, x2 + x1) * 10).denominator == 1 and Fr(y2 - y1, x2 + x1) != a else d(a + 1), d(Fr(x2 - x1, y2 - y1)) if y2 != y1 and (Fr(x2 - x1, y2 - y1) * 10).denominator == 1 and Fr(x2 - x1, y2 - y1) != a else d(-a), d(y2 - y1) if y2 - y1 != a else d(a - 1)]
    if q == "a":
        return M("%s est affine avec %s(%s) = %s et %s(%s) = %s. Quel est son coefficient directeur ?" % (f, f, d(x1), d(y1), f, d(x2), d(y2)), d(a), w_a,
                 "a = (%s − %s) ÷ (%s − %s) = %s ÷ %s = <b>%s</b>." % (d(y2), par(y1), d(x2), par(x1), d(y2 - y1), par(x2 - x1), d(a)))
    return M("%s est affine avec %s(%s) = %s et %s(%s) = %s. Quelle est son expression ?" % (f, f, d(x1), d(y1), f, d(x2), d(y2)), "%s(x) = %s" % (f, E((a, "x"), (b, ""))),
             ["%s(x) = %s" % (f, E((a, "x"), (-b, ""))) if b else "%s(x) = %s" % (f, E((a, "x"), (1, ""))), "%s(x) = %s" % (f, E((b, "x"), (a, ""))) if b != a and b else "%s(x) = %s" % (f, E((-a, "x"), (b, ""))), "%s(x) = %s" % (f, E((-a, "x"), (b, ""))) if a else "%s(x) = x" % f],
             "a = %s ÷ %s = %s ; b = %s − %s × %s = %s : <b>%s(x) = %s</b>." % (d(y2 - y1), par(x2 - x1), d(a), d(y1), d(a), par(x1), d(b), f, E((a, "x"), (b, ""))))


def s3():
    a = R.choice([-2, -1, Fr(-1, 2), Fr(1, 2), 1, 2, 3, Fr(3, 2)])
    b = R.randint(-3, 3)
    if Fr(a).denominator == 2 and b % 1:
        return None
    svg = relabel(de_k8.kosy(lines=[(a, b, BLUE, "")], lo=-5, hi=5, u=22), "droite dans un repère")
    k = R.choice(["b", "a", "expr"])
    if k == "b":
        return M("<div class='qfig'>%s</div>Quelle est l’ordonnée à l’origine de cette droite ?" % svg, d(b), [d(-b) if b else "1", fq(a) if Fr(a) != b else d(b + 2), d(b + 1)],
                 "La droite coupe l’axe des ordonnées en %s : <b>b = %s</b>." % (d(b), d(b)))
    if k == "a":
        return M("<div class='qfig'>%s</div>Quel est le coefficient directeur de cette droite ?" % svg, fq(a), [fq(-a), fq(1 / Fr(a)) if 1 / Fr(a) != a else fq(a * 2), d(b) if Fr(b) not in (Fr(a), -Fr(a)) else fq(a + 1)],
                 "Quand x augmente de %s, y %s de %s : <b>a = %s</b>." % ("1" if Fr(a).denominator == 1 else "2", "augmente" if a > 0 else "diminue", d(abs(a)) if Fr(a).denominator == 1 else d(abs(2 * a)), fq(a)))
    ans = "y = %s" % E((a, "x"), (b, ""))
    return M("<div class='qfig'>%s</div>Quelle fonction affine est représentée ?" % svg, ans.replace("y =", "f(x) ="), ["f(x) = %s" % E((-a, "x"), (b, "")), "f(x) = %s" % E((b, "x"), (a, "")) if b and Fr(b) != Fr(a) else "f(x) = %s" % E((a, "x"), (b + 1, "")), "f(x) = %s" % E((a, "x"), (-b, "")) if b else "f(x) = %s" % E((a * 2, "x"))],
             "Ordonnée à l’origine %s, coefficient directeur %s : <b>f(x) = %s</b>." % (d(b), fq(a), E((a, "x"), (b, ""))))


def s4():
    k = R.choice(["pc", "pc", "prop", "inter"])
    if k == "pc":
        t = R.choice([5, 10, 15, 20, 25, 30, 40])
        up = R.random() < 0.5
        c = 1 + Fr(t if up else -t, 100)
        return M("Quelle fonction linéaire modélise une %s de %d %% ?" % ("augmentation" if up else "diminution", t), "x ↦ %sx" % d(c), ["x ↦ %sx" % d(Fr(t, 100)), "x ↦ x %s %d" % ("+" if up else MINUS, t), "x ↦ %sx" % d(1 - Fr(t if up else -t, 100))],
                 "%s de %d %% = multiplier par %s : <b>x ↦ %sx</b>." % ("Augmenter" if up else "Diminuer", t, d(c), d(c)))
    if k == "prop":
        V = [("Une fonction linéaire modélise…", "une situation de proportionnalité", ["une situation qui n’est jamais proportionnelle", "une courbe en forme de U", "un prix avec abonnement"]),
             ("La représentation graphique d’une fonction linéaire est…", "une droite passant par l’origine", ["une droite qui ne passe pas par l’origine", "une parabole", "un ensemble de points non alignés"]),
             ("La représentation graphique d’une fonction affine est…", "une droite", ["une parabole", "toujours une droite passant par l’origine", "une courbe quelconque"]),
             ("Si le coefficient directeur est négatif, la fonction affine est…", "décroissante", ["croissante", "constante", "linéaire"])]
        q, a_, w = R.choice(V)
        return M(q, a_, w, "Réponse : <b>%s</b>." % a_)
    a, b = nz(1, 5), R.randint(-6, 6)
    c, e = nz(-5, -1), R.randint(-6, 6)
    x = Fr(e - b, a - c)
    if x.denominator != 1:
        return None
    return M("Pour quelle valeur de x a-t-on %s = %s ?" % (E((a, "x"), (b, "")), E((c, "x"), (e, ""))), d(x), [d(Fr(e - b, a + c)) if a + c and Fr(e - b, a + c).denominator == 1 and Fr(e - b, a + c) != x else d(x + 1), d(-x) if x else "1", d(Fr(e + b, a - c)) if Fr(e + b, a - c).denominator == 1 and Fr(e + b, a - c) != x else d(x - 1)],
             "%s = %s, donc x = <b>%s</b> (abscisse du point d’intersection des deux droites)." % (E((a - c, "x")), d(e - b), d(x)))


def s5():
    k = R.choice(["taxi", "forfait", "bougie", "temp"])
    if k == "taxi":
        a, b = R.choice([Fr(3, 2), 2, Fr(5, 2), 3]), R.randint(3, 8)
        x = R.choice([4, 6, 8, 10, 12])
        return M("Un taxi facture %s € de prise en charge et %s € par km. Le prix est donné par P(x) = %sx + %d. Combien coûte une course de %d km ?" % (b, d(a), d(a), b, x), euro(a * x + b), [euro((a + b) * x), euro(a * x), euro(a + b + x)],
                 "P(%d) = %s × %d + %d = <b>%s</b>." % (x, d(a), x, b, euro(a * x + b)))
    if k == "forfait":
        a1, b1, a2 = R.randint(2, 5), R.randint(10, 30), 0
        a2 = a1 + R.randint(2, 5)
        n = Fr(b1, a2 - a1)
        if n.denominator != 1:
            return None
        return M("Tarif A : f(x) = %dx + %d. Tarif B : g(x) = %dx (x = nombre d’entrées). Pour combien d’entrées les deux tarifs sont-ils égaux ?" % (a1, b1, a2), str(n), [str(Fr(b1, a2 + a1)) if Fr(b1, a2 + a1).denominator == 1 else str(n + 1), str(b1), str(n * 2)],
                 "%dx + %d = %dx ⇔ %dx = %d ⇔ x = <b>%s</b>." % (a1, b1, a2, a2 - a1, b1, n))
    if k == "bougie":
        h0, v = R.choice([(20, 2), (24, 3), (18, 2), (30, 5), (15, 3)])
        t = R.randint(1, h0 // v - 1)
        return M("Une bougie de %d cm diminue de %d cm par heure. Sa hauteur est h(t) = %d − %dt. Au bout de combien de temps mesure-t-elle %d cm ?" % (h0, v, h0, v, h0 - v * t), "%d h" % t, ["%d h" % (h0 - v * t), "%s h" % d(Fr(h0 - v * t, v)) if (Fr(h0 - v * t, v) * 10).denominator == 1 and Fr(h0 - v * t, v) != t else "%d h" % (t + 1), "%d h" % (h0 // v)],
                 "%d − %dt = %d ⇔ %dt = %d ⇔ t = <b>%d h</b>." % (h0, v, h0 - v * t, v, v * t, t))
    c = R.choice([0, 10, 20, 25, 30, 35, 100])
    f = Fr(9, 5) * c + 32
    return M("La température en °F s’obtient par F(c) = 1,8c + 32 (c en °C). Combien font %d °C en °F ?" % c, "%s °F" % d(f), ["%s °F" % d(Fr(9, 5) * (c + 32)), "%s °F" % d(c + 32), "%s °F" % d(Fr(9, 5) * c)],
             "1,8 × %d + 32 = <b>%s °F</b>." % (c, d(f)))


def main():
    seen = set()
    sets = [("Reconnaître une fonction affine", mix(R, seen, [(s1, 20)])), ("Déterminer une fonction", mix(R, seen, [(s2, 20)])),
            ("Lire une droite", mix(R, seen, [(s3, 20)])), ("Propriétés et intersections", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une fonction <b>affine</b> s’écrit f(x) = ax + b : a est le <b>coefficient directeur</b>, b l’<b>ordonnée à l’origine</b>. Si b = 0, elle est <b>linéaire</b> (proportionnalité).",
              "Sa représentation graphique est une droite ; celle d’une fonction linéaire passe par l’origine.",
              "Avec deux valeurs : a = (f(x₂) − f(x₁)) ÷ (x₂ − x₁), puis b = f(x₁) − a × x₁."],
             [("f(2) = 7 et f(5) = 16", ["a = (16 − 7) ÷ (5 − 2) = 3", "b = 7 − 3 × 2 = 1"], "f(x) = 3x + 1")],
             [["a = (16 − 7) ÷ (5 + 2)", "On divise par la différence des x : 5 − 2."], ["Confondre a et b", "b se lit sur l’axe des ordonnées (x = 0) ; a est la pente."],
              ["Croire qu’une fonction affine traduit la proportionnalité", "Seulement si b = 0 (fonction linéaire)."]])
    faq = [("Comment lire le coefficient directeur sur un graphique ?", "On avance de 1 vers la droite et on regarde de combien on monte (a &gt; 0) ou on descend (a &lt; 0)."),
           ("Une fonction constante est-elle affine ?", "Oui : f(x) = b, avec a = 0. Sa droite est horizontale.")]
    unit("3e", R, "fonctions-lineaires-et-affines", "F",
         "Reconnaître une fonction linéaire et une fonction affine ; déterminer son expression à partir de deux valeurs ou de sa représentation graphique ; interpréter le coefficient directeur et l’ordonnée à l’origine ; modéliser des situations",
         "Fonctions linéaires et affines", "Fonctions linéaires et affines",
         "Fiches de maths 3e sur les fonctions linéaires et affines : coefficient directeur, ordonnée à l’origine, lecture graphique, expression et problèmes. 100 exercices corrigés.",
         "f(x) = ax + b : a coefficient directeur, b ordonnée à l’origine", "Linéaire (b = 0) ⇔ proportionnalité", body, faq, sets, 9)


if __name__ == "__main__":
    main()
