# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Dérivée et variations (signe de f′, tableau de variations, extremums, fonctions paires et impaires, inégalités, optimisation)
  python3 tools/gen_fr_maths_premiere_derivee_et_variations.py
Erreurs : lire les variations de f′ au lieu de son signe, f′(a) = 0 donc extremum (sans changement de signe), donner x au lieu de f(x) pour l’extremum, paire ⇔ f(−x) = −f(x).
"""
import random
from fr_ly1 import *

R = random.Random(60611)
X = {3: "x³", 2: "x²", 1: "x", 0: ""}


def poly(cs):
    return expr([(c, X[e]) for c, e in cs])


def ev(cs, x):
    return sum(Fr(c) * Fr(x) ** e for c, e in cs)


def der(cs):
    return [(c * e, e - 1) for c, e in cs if e > 0]


def iv(a, b):
    return "%s ; %s" % (a, b)


def s1():
    k = R.choice(["aff", "aff", "quad", "sign"])
    if k == "aff":
        m, p = nz(R, -6, 6), R.randint(-12, 12)
        x0 = Fr(-p, m)
        dec, cro = ("]−∞ ; %s]" % fq(x0), "[%s ; +∞[" % fq(x0))
        ans = "décroissante sur %s, croissante sur %s" % (dec, cro) if m > 0 else "croissante sur %s, décroissante sur %s" % (dec, cro)
        return M("On sait que f′(x) = %s pour tout réel x. Quelles sont les variations de f ?" % E((m, "x"), (p, "")), ans,
                 ["croissante sur %s, décroissante sur %s" % (dec, cro) if m > 0 else "décroissante sur %s, croissante sur %s" % (dec, cro), "%s sur ℝ" % ("croissante" if m > 0 else "décroissante"),
                  ans.replace(fq(x0), fq(-x0)) if x0 else ans.replace("0", "1")],
                 "f′(x) s’annule en %s et est du signe de %s à droite : f′ %s puis %s, donc <b>%s</b>." % (fq(x0), d(m), MINUS if m > 0 else "+", "+" if m > 0 else MINUS, ans))
    if k == "quad":
        x1, x2 = sorted(R.sample(range(-5, 6), 2))
        a = R.choice([1, -1, 2, 3])
        fp = P2(a, -a * (x1 + x2), a * x1 * x2)
        if a > 0:
            ans = "croissante, décroissante, croissante (changements en %s et %s)" % (d(x1), d(x2))
            w = ["décroissante, croissante, décroissante (changements en %s et %s)" % (d(x1), d(x2)), "décroissante puis croissante (changement en %s)" % fq(Fr(x1 + x2, 2)), "croissante sur ℝ"]
        else:
            ans = "décroissante, croissante, décroissante (changements en %s et %s)" % (d(x1), d(x2))
            w = ["croissante, décroissante, croissante (changements en %s et %s)" % (d(x1), d(x2)), "croissante puis décroissante (changement en %s)" % fq(Fr(x1 + x2, 2)), "décroissante sur ℝ"]
        return M("f′(x) = %s (racines %s et %s). Quelles sont les variations de f ?" % (fp, d(x1), d(x2)), ans, w,
                 "f′(x) est du signe de a = %s à l’extérieur des racines : f′ est %s, donc f est <b>%s</b>." % (d(a), "+, −, +" if a > 0 else "−, +, −", ans))
    xs = sorted(R.sample(range(-6, 7), 2))
    sg = R.choice([["+", MINUS, "+"], [MINUS, "+", MINUS]])
    q = R.choice([0, 1, 2])
    labels = ["]−∞ ; %s]" % d(xs[0]), "[%s ; %s]" % (d(xs[0]), d(xs[1])), "[%s ; +∞[" % d(xs[1])]
    ans = "croissante" if sg[q] == "+" else "décroissante"
    return M("Le signe de f′(x) est %s sur ]−∞ ; %s[, %s sur ]%s ; %s[ et %s sur ]%s ; +∞[. Quel est le sens de variation de f sur %s ?" % (sg[0], d(xs[0]), sg[1], d(xs[0]), d(xs[1]), sg[2], d(xs[1]), labels[q]),
             ans, ["décroissante" if ans == "croissante" else "croissante", "constante", "on ne peut pas savoir sans f"], "f′(x) %s 0 sur cet intervalle : f est <b>%s</b>." % ("⩾" if sg[q] == "+" else "⩽", ans))


def cubic():
    """f(x) = a x³ + b x² + c x + e avec f′ de racines entières"""
    x1, x2 = sorted(R.sample(range(-4, 5), 2))
    a = R.choice([1, -1, 2, -2])
    # f′(x) = 3a (x − x1)(x − x2) = 3a x² − 3a(x1 + x2) x + 3a x1 x2
    b = Fr(-3 * a * (x1 + x2), 2)
    if b.denominator != 1:
        return None
    c = 3 * a * x1 * x2
    e = R.randint(-6, 6)
    cs = [(a, 3), (int(b), 2), (c, 1), (e, 0)]
    cs = [t for t in cs if t[0]]
    return cs, x1, x2, a


def s2():
    r = cubic()
    if not r:
        return None
    cs, x1, x2, a = r
    k = R.choice(["fp", "max", "min", "max", "min"])
    if k == "fp":
        ans = "f′(x) = " + poly(der(cs))
        return M("f(x) = %s. Calcule f′(x)." % poly(cs), ans, ["f′(x) = " + poly([(c * e, e) for c, e in cs if e > 0]), "f′(x) = " + poly([(c, e - 1) for c, e in cs if e > 0]), "f′(x) = " + poly(der(cs) + [(1, 0)]) if all(e > 0 for c, e in der(cs)) else "f′(x) = " + poly([(c * e, e - 1) for c, e in cs if e > 1])],
                 "On dérive terme à terme : <b>%s</b>." % ans)
    y1, y2 = ev(cs, x1), ev(cs, x2)
    if (k == "max") == (a > 0):
        xm, ym = x1, y1
    else:
        xm, ym = x2, y2
    other = y2 if xm == x1 else y1
    word = "maximum" if k == "max" else "minimum"
    return M("f(x) = %s, f′(x) = %s. Quel est le %s local de f ?" % (poly(cs), poly(der(cs)), word), "%s, atteint en x = %s" % (d(ym), d(xm)),
             ["%s, atteint en x = %s" % (d(xm), d(ym)), "%s, atteint en x = %s" % (d(other), d(x2 if xm == x1 else x1)), "0, atteint en x = %s" % d(xm), "%s, atteint en x = %s" % (d(ym), d(-xm)) if xm else "%s, atteint en x = 1" % d(ym)],
             "f′ s’annule en %s et %s ; f′ change de signe %s en %s : %s local <b>f(%s) = %s</b>." % (d(x1), d(x2), "de + à −" if word == "maximum" else "de − à +", d(xm), word, d(xm), d(ym)))


def s3():
    k = R.choice(["read", "read", "nochange", "tangent"])
    if k == "read":
        n = R.choice([3, 4])
        xs = sorted(R.sample(range(-5, 8), n))
        ys = []
        up = R.choice([True, False])
        y = R.randint(-5, 5)
        for i in range(n):
            ys.append(y)
            y += R.randint(2, 7) if up else -R.randint(2, 7)
            up = not up
        sig = ["+" if ys[i + 1] > ys[i] else MINUS for i in range(n - 1)]
        svg = vtab([d(x) for x in xs], ys, dsig=sig)
        sub = R.choice(["max", "min", "fp"])
        if sub == "fp":
            i = R.randint(0, n - 2)
            t = Fr(xs[i] + xs[i + 1], 2)
            ans = "positif" if sig[i] == "+" else "négatif"
            return M("<div class='qfig'>%s</div>Quel est le signe de f′(%s) ?" % (svg, fq(t)), ans, ["négatif" if ans == "positif" else "positif", "nul", "on ne peut pas savoir"],
                     "%s est entre %s et %s, où f est %s : f′(%s) est <b>%s</b>." % (fq(t), d(xs[i]), d(xs[i + 1]), "croissante" if sig[i] == "+" else "décroissante", fq(t), ans))
        m = max(ys) if sub == "max" else min(ys)
        return M("<div class='qfig'>%s</div>Quel est le %s de f sur [%s ; %s] ?" % (svg, "maximum" if sub == "max" else "minimum", d(xs[0]), d(xs[-1])), d(m),
                 [d(xs[ys.index(m)]) if xs[ys.index(m)] != m else d(m + 1), d(min(ys) if sub == "max" else max(ys)), "0" if m else "1", d(-m) if m else "2", d(xs[0])],
                 "On lit la plus %s valeur de la ligne f(x) : <b>%s</b>, atteinte en x = %s." % ("grande" if sub == "max" else "petite", d(m), d(xs[ys.index(m)])))
    if k == "nochange":
        c = R.randint(-5, 5)
        return M("f(x) = x³ %s. f′(0) = 0. f admet-elle un extremum local en 0 ?" % (("+ %d" % c) if c > 0 else ("− %d" % -c) if c else ""), "non, car f′(x) = 3x² ne change pas de signe",
                 ["oui, car f′(0) = 0", "oui, un minimum", "oui, un maximum"], "f′(x) = 3x² ⩾ 0 : f est croissante sur ℝ. f′(0) = 0 mais f′ ne change pas de signe : <b>pas d’extremum</b>.")
    r = cubic()
    if not r:
        return None
    cs, x1, x2, a = r
    xm = R.choice([x1, x2])
    return M("f(x) = %s. En quel point la tangente à la courbe est-elle horizontale, avec x %s 0 ?" % (poly(cs), "&lt;" if xm == x1 and x1 < 0 else "&gt;" if xm == x2 and x2 > 0 else "="),
             "(%s ; %s)" % (d(xm), d(ev(cs, xm))), ["(%s ; 0)" % d(xm), "(0 ; %s)" % d(ev(cs, 0)), "(%s ; %s)" % (d(ev(cs, xm)), d(xm))],
             "Tangente horizontale ⇔ f′(x) = 0 ⇔ x = %s ou x = %s. Le point cherché est <b>(%s ; %s)</b>." % (d(x1), d(x2), d(xm), d(ev(cs, xm)))) if (xm == x1 and x1 < 0) or (xm == x2 and x2 > 0) else None


def s4():
    k = R.choice(["parite", "parite", "parite", "graph", "ineg"])
    if k == "parite":
        a, b = nz(R, -5, 5), nz(R, -9, 9)
        F = [(P2(a, 0, b), "paire"), (expr([(a, "x³"), (b, "x")]), "impaire"), ("%s/x" % d(a), "impaire"), ("%sx⁴ %s x²" % (d(a) if a != 1 else "", "+" if b > 0 else MINUS) if abs(b) == 1 else "%sx⁴ %s %dx²" % (d(a) if a != 1 else "", "+" if b > 0 else MINUS, abs(b)), "paire"),
             (P2(a, b, 0), "ni paire ni impaire"), ("|x| %s %d" % ("+" if b > 0 else MINUS, abs(b)), "paire"), (expr([(a, "x³"), (b, "")]), "ni paire ni impaire")]
        f, ans = R.choice(F)
        expl = {"paire": "f(−x) = f(x) pour tout x : f est <b>paire</b> (courbe symétrique par rapport à l’axe des ordonnées).",
                "impaire": "f(−x) = −f(x) pour tout x : f est <b>impaire</b> (courbe symétrique par rapport à l’origine).",
                "ni paire ni impaire": "Par exemple f(1) ≠ f(−1) et f(−1) ≠ −f(1) : f n’est <b>ni paire ni impaire</b>."}[ans]
        return M("La fonction f(x) = %s est-elle paire, impaire ou ni l’une ni l’autre ?" % f, ans, [v for v in ["paire", "impaire", "ni paire ni impaire", "paire et impaire"] if v != ans], expl)
    if k == "graph":
        t = R.choice(["paire", "impaire"])
        a = R.randint(1, 6)
        b = R.randint(-9, 9)
        return M("f est %s et f(%d) = %s. Que vaut f(%s) ?" % (t, a, d(b), d(-a)), d(b if t == "paire" else -b), [d(-b if t == "paire" else b) if b else "1", d(a), d(-a)],
                 "%s : f(−%d) = %s<b>%s</b>." % ("Paire" if t == "paire" else "Impaire", a, "" if t == "paire" else "−f(%d) = " % a, d(b if t == "paire" else -b)))
    m = R.choice([1, 2, 3])
    return M("On étudie g(x) = x³ − %dx sur [0 ; +∞[ : g′(x) = 3x² − %d, g est décroissante puis croissante, de minimum g(%d) = %s. Que peut-on conclure ?" % (3 * m * m, 3 * m * m, m, d(-2 * m ** 3)),
             "x³ − %dx ⩾ %s pour tout x ⩾ 0" % (3 * m * m, d(-2 * m ** 3)), ["x³ − %dx ⩽ %s pour tout x ⩾ 0" % (3 * m * m, d(-2 * m ** 3)), "x³ − %dx ⩾ 0 pour tout x ⩾ 0" % (3 * m * m), "x³ − %dx &gt; %d pour tout x ⩾ 0" % (3 * m * m, m)],
             "Le minimum de g sur [0 ; +∞[ est %s : <b>g(x) ⩾ %s</b> pour tout x ⩾ 0 (inégalité obtenue par l’étude de fonction)." % (d(-2 * m ** 3), d(-2 * m ** 3)))


def s5():
    k = R.choice(["boite", "boite", "benef", "enclos", "cout"])
    if k == "boite":
        L_ = R.choice([12, 18, 24, 30, 36])
        x = L_ // 6
        V = x * (L_ - 2 * x) ** 2
        return M("Dans un carré de carton de %d cm de côté, on découpe un carré de côté x aux quatre coins pour fabriquer une boîte sans couvercle. V(x) = x(%d − 2x)². Pour quelle valeur de x le volume est-il maximal ?" % (L_, L_),
                 "x = %d cm" % x, ["x = %d cm" % (L_ // 2), "x = %d cm" % (L_ // 4), "x = %d cm" % (L_ // 3)],
                 "V′(x) = (%d − 2x)(%d − 6x) s’annule en x = %d (l’autre racine %d donne V = 0). <b>x = %d cm</b>, V = %s cm³." % (L_, L_, x, L_ // 2, x, num(V)))
    if k == "benef":
        x1, x2 = sorted(R.sample(range(1, 9), 2))
        a = -1
        # B′(x) = −3(x − x1)(x − x2) → B(x) = −x³ + 1,5(x1 + x2)x² − 3x1x2 x + c
        b = Fr(3 * (x1 + x2), 2)
        if b.denominator != 1:
            return None
        cs = [(-1, 3), (int(b), 2), (-3 * x1 * x2, 1), (R.randint(10, 60), 0)]
        return M("Le bénéfice (en milliers d’€) pour x centaines d’objets (0 ⩽ x ⩽ 10) est B(x) = %s. B′(x) = %s. Pour combien de centaines d’objets le bénéfice est-il maximal sur [%d ; 10] ?" % (poly(cs), poly(der(cs)), x1),
                 str(x2), [str(x1), "10", str(x1 + x2), str(x2 + 1), str(x2 - 1)], "B′(x) = −3(x − %d)(x − %d) : B croît sur [%d ; %d] puis décroît. Maximum en <b>x = %d</b>." % (x1, x2, x1, x2, x2))
    if k == "enclos":
        A = R.choice([50, 72, 98, 128, 200, 242])
        import math
        x = int(math.isqrt(A // 2))
        if 2 * x * x != A:
            return None
        return M("Un enclos rectangulaire de %d m² est adossé à un mur : on clôture trois côtés, de longueur totale L(x) = 2x + %d/x. Pour quelle valeur de x la clôture est-elle la plus courte ?" % (A, A),
                 "x = %d m" % x, ["x = %d m" % (2 * x), "x = %s m" % d(Fr(A, 4)) if A % 4 == 0 else "x = %d m" % (x + 2), "x = %d m" % (A // 10), "x = %d m" % (A // x), "x = %d m" % (x - 1)],
                 "L′(x) = 2 − %d/x² s’annule pour x² = %d, soit <b>x = %d m</b> (L′ change de signe de − à +)." % (A, A // 2, x))
    a = R.choice([1, 2])
    q0 = R.choice([10, 20, 30])
    # coût moyen CM(q) = a q + a q0² / q + 5 → min en q0
    return M("Le coût moyen de fabrication est CM(q) = %sq + %s/q + 5 (q &gt; 0). Pour quelle quantité q est-il minimal ?" % (d(a) if a > 1 else "", num(a * q0 * q0)), "q = %d" % q0,
             ["q = %d" % (2 * q0), "q = %d" % (q0 * q0), "q = %d" % (q0 // 2)], "CM′(q) = %s − %s/q² s’annule pour q² = %d : <b>q = %d</b>." % (d(a), num(a * q0 * q0), q0 * q0, q0))


def main():
    seen = set()
    sets = [("Signe de f′ et variations", mix(R, seen, [(s1, 20)])), ("Étudier une fonction polynôme", mix(R, seen, [(s2, 20)])),
            ("Extremums et tableaux de variations", mix(R, seen, [(s3, 20)])), ("Parité et inégalités", mix(R, seen, [(s4, 20)])), ("Optimisation", mix(R, seen, [(s5, 20)]))]
    body = L(["Sur un intervalle : si f′(x) ⩾ 0, f est <b>croissante</b> ; si f′(x) ⩽ 0, f est <b>décroissante</b> ; si f′ = 0, f est constante.",
              "Si f′ s’annule en a <b>en changeant de signe</b>, f admet un extremum local en a (maximum si f′ passe de + à −, minimum de − à +). La tangente y est horizontale.",
              "Méthode : calculer f′(x), étudier son signe (tableau de signes), en déduire le tableau de variations, calculer les extremums.",
              "f est <b>paire</b> si f(−x) = f(x), <b>impaire</b> si f(−x) = −f(x)."],
             [("f(x) = x³ − 3x", ["f′(x) = 3x² − 3 = 3(x − 1)(x + 1)", "f′ : + avant −1, − entre −1 et 1, + après 1"], "maximum local f(−1) = 2, minimum local f(1) = −2")],
             [["f′ décroît, donc f décroît", "C’est le signe de f′ qui compte, pas ses variations."], ["f′(0) = 0 donc 0 est un extremum", "Il faut que f′ change de signe (contre-exemple : x³)."],
              ["Le maximum est x = 2", "Le maximum est une valeur de f : f(2)."], ["x³ est paire", "(−x)³ = −x³ : x³ est impaire."]])
    faq = [("Pourquoi étudier le signe de la dérivée ?", "Parce que f′(x) est la pente de la tangente : pente positive, la courbe monte ; pente négative, elle descend."),
           ("Comment prouver une inégalité f(x) ⩾ g(x) ?", "On étudie h(x) = f(x) − g(x) : si son minimum est positif ou nul, alors h(x) ⩾ 0, donc f(x) ⩾ g(x).")]
    unit("premiere", R, "derivee-et-variations", "F",
         "Lien entre le signe de la dérivée et le sens de variation ; extremum local et tangente horizontale ; fonctions paires et impaires ; étudier les variations d’une fonction, résoudre un problème d’optimisation, établir une inégalité",
         "Dérivée et variations : extremums et optimisation", "Dérivée et variations",
         "Fiches de maths première sur la dérivée et les variations : signe de f′, tableau de variations, extremums, parité, inégalités et optimisation. 100 exercices corrigés.",
         "f′ ⩾ 0 : croissante ; f′ ⩽ 0 : décroissante", "Extremum local là où f′ s’annule en changeant de signe", body, faq, sets, 11)


if __name__ == "__main__":
    main()
