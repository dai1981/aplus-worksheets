# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Fonctions cosinus et sinus (parité, périodicité, angles associés, courbes, équations cos x = a et sin x = a)
  python3 tools/gen_fr_maths_premiere_fonctions_cosinus_et_sinus.py
Erreurs : cos impaire / sin paire, cos(π − x) = cos x, oublier la deuxième solution de cos x = a, période π au lieu de 2π.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60615)
ANG = [Fr(k, 6) for k in range(-11, 13)] + [Fr(k, 4) for k in range(-7, 9) if k % 2]
VALS = [(Fr(1, 2), FR(1, 2)), (Fr(-1, 2), MINUS + FR(1, 2)), (None, FR("√2", 2)), (None, MINUS + FR("√2", 2)), (None, FR("√3", 2)), (None, MINUS + FR("√3", 2))]


def neg(v):
    return v[1:] if v.startswith(MINUS) else (v if v == "0" else MINUS + v)


def s1():
    k = R.choice(["cosneg", "sinneg", "per", "parite", "per2"])
    a = R.choice([Fr(1, 5), Fr(2, 7), Fr(3, 5), Fr(-2, 5), Fr(4, 9), Fr(-1, 3), Fr(5, 8)])
    x = R.choice(["x", "a", "t"])
    if k == "cosneg":
        return M("On sait que cos %s = %s. Que vaut cos(−%s) ?" % (x, fq(a), x), fq(a), [fq(-a), fq(1 - a), fq(1 / a)], "cos est paire : cos(−%s) = cos %s = <b>%s</b>." % (x, x, fq(a)))
    if k == "sinneg":
        return M("On sait que sin %s = %s. Que vaut sin(−%s) ?" % (x, fq(a), x), fq(-a), [fq(a), fq(1 - a), fq(-1 / a)], "sin est impaire : sin(−%s) = −sin %s = <b>%s</b>." % (x, x, fq(-a)))
    if k == "per":
        n = R.choice([1, 2, 3, -1, -2])
        fn = R.choice(["cos", "sin"])
        return M("On sait que %s %s = %s. Que vaut %s(%s %s %s) ?" % (fn, x, fq(a), fn, x, "+" if n > 0 else MINUS, pif(abs(2 * n)), ), fq(a), [fq(-a), fq(a + 2 * n) if abs(a + 2 * n) < 5 else fq(2 * a), fq(1 - a)],
                 "%s est 2π-périodique : on ajoute ou retire des tours complets. <b>%s</b>." % (fn, fq(a)))
    if k == "parite":
        fn = R.choice(["cos", "sin"])
        ans = "paire" if fn == "cos" else "impaire"
        return M("La fonction %s est-elle paire ou impaire ? Que montre sa courbe ?" % ("cosinus" if fn == "cos" else "sinus"),
                 ans + (" : courbe symétrique par rapport à l’axe des ordonnées" if fn == "cos" else " : courbe symétrique par rapport à l’origine"),
                 ["paire : courbe symétrique par rapport à l’axe des ordonnées" if fn == "sin" else "impaire : courbe symétrique par rapport à l’origine", "ni paire ni impaire", ans + " : courbe symétrique par rapport à l’axe des abscisses"],
                 "%s(−x) = %s pour tout x : <b>%s</b>." % (fn, "cos x" if fn == "cos" else "−sin x", ans))
    return M("Quelle est la période des fonctions cosinus et sinus ?", "2π", ["π", "π/2", "360"], "cos(x + 2π) = cos x et sin(x + 2π) = sin x : la période est <b>2π</b>.") if R.random() < 0.3 else None


def s2():
    a = R.choice([Fr(1, 5), Fr(2, 7), Fr(3, 5), Fr(-2, 5), Fr(4, 9), Fr(-1, 3), Fr(5, 8), Fr(3, 4), Fr(-3, 7)])
    fn, form, sgn, expl = R.choice([("cos", "cos(π − x)", -1, "cos(π − x) = −cos x"), ("sin", "sin(π − x)", 1, "sin(π − x) = sin x"),
                                    ("cos", "cos(π + x)", -1, "cos(π + x) = −cos x"), ("sin", "sin(π + x)", -1, "sin(π + x) = −sin x"),
                                    ("cos", "sin(π/2 − x)", 1, "sin(π/2 − x) = cos x"), ("sin", "cos(π/2 − x)", 1, "cos(π/2 − x) = sin x"),
                                    ("cos", "cos(x − π)", -1, "cos(x − π) = −cos x"), ("sin", "sin(x + 2π)", 1, "sin est 2π-périodique")])
    return M("On sait que %s x = %s. Que vaut %s ?" % (fn, fq(a), form), fq(sgn * a), [fq(-sgn * a), fq(1 - a), fq(-(1 - a)), fq(sgn * a + 1), fq(2 * a), fq(1 / a)],
             "%s, donc <b>%s = %s</b>. On le voit en plaçant les points associés sur le cercle." % (expl, form, fq(sgn * a)))


def s3():
    t = R.choice(ANG)
    a, b = R.choice([2, 3, -2, 4]), R.randint(-3, 3)
    fn = R.choice(["cos", "sin"])
    v = (math.cos if fn == "cos" else math.sin)(float(t) * math.pi)
    tv = trig_val(t, fn)
    if abs(v - round(v)) > 1e-9 and abs(2 * v - round(2 * v)) > 1e-9:
        return None
    val_ = Fr(round(2 * v), 2) * a + b
    f = "%s%s x %s" % (d(a), fn, ("+ %d" % b) if b >= 0 else "− %d" % -b) if b else "%s%s x" % (d(a), fn)
    bt = (" + %d" % b) if b > 0 else (" − %d" % -b) if b else ""
    return M("f(x) = %s. Calcule f(%s)." % (f, pif(t)), fq(val_), [fq(-Fr(round(2 * v), 2) * a + b), fq(Fr(round(2 * v), 2) + b), fq(a * (Fr(round(2 * v), 2) + b)) if a * (Fr(round(2 * v), 2) + b) != val_ else fq(val_ + 1), fq(val_ + a)],
             "%s(%s) = %s, donc f(%s) = %s × %s%s = <b>%s</b>." % (fn, pif(t), tv, pif(t), d(a), "(" + tv + ")" if tv.startswith(MINUS) else tv, bt, fq(val_)))


def s4():
    k = R.choice(["which", "which", "max", "signe"])
    if k == "which":
        fn, lab, f = R.choice([("cos", "x ↦ cos x", lambda x: math.cos(x)), ("sin", "x ↦ sin x", lambda x: math.sin(x)), ("−cos", "x ↦ −cos x", lambda x: -math.cos(x)), ("−sin", "x ↦ −sin x", lambda x: -math.sin(x)),
                                ("2cos", "x ↦ 2cos x", lambda x: 2 * math.cos(x)), ("2sin", "x ↦ 2sin x", lambda x: 2 * math.sin(x))])
        svg = kurve([(f, BLUE, "")], (-2 * math.pi, 2 * math.pi, math.pi), (-2, 2, 1), W=430, H=230, label="courbe d’une fonction trigonométrique", xlab=lambda v: pit(Fr(v / math.pi).limit_denominator(4)))
        others = [l for _, l, _ in [("cos", "x ↦ cos x", 0), ("sin", "x ↦ sin x", 0), ("−cos", "x ↦ −cos x", 0), ("−sin", "x ↦ −sin x", 0), ("2cos", "x ↦ 2cos x", 0), ("2sin", "x ↦ 2sin x", 0)] if l != lab]
        R.shuffle(others)
        return M("<div class='qfig'>%s</div>Quelle fonction est représentée ?" % svg, lab, others,
                 "On lit f(0) = %s et le maximum %s : c’est <b>%s</b>." % (d(round(f(0))), "2" if "2" in fn else "1", lab))
    if k == "max":
        a, b = R.randint(2, 5), nz(R, -4, 4)
        fn = R.choice(["cos", "sin"])
        sub = R.choice(["max", "min"])
        v = a + b if sub == "max" else -a + b
        return M("Quel est le %s de f(x) = %d%s x %s sur ℝ ?" % ("maximum" if sub == "max" else "minimum", a, fn, ("+ %d" % b) if b >= 0 else "− %d" % -b), d(v),
                 [d(a), d(b), d(-v) if v else "1", d(a * b) if a * b != v else d(v + 2)], "%s x varie entre −1 et 1 : f(x) varie entre %s et %s : <b>%s</b>." % (fn, d(-a + b), d(a + b), d(v)))
    fn = R.choice(["cos", "sin"])
    ivs = {"sin": [("]0 ; π[", "positif"), ("]π ; 2π[", "négatif"), ("]−π ; 0[", "négatif")], "cos": [("]−π/2 ; π/2[", "positif"), ("]π/2 ; 3π/2[", "négatif")]}
    iv, ans = R.choice(ivs[fn])
    return M("Quel est le signe de %s x pour x ∈ %s ?" % (fn, iv), ans, ["négatif" if ans == "positif" else "positif", "positif puis négatif", "nul"],
             "Sur le cercle, les points associés sont %s : %s x est <b>%s</b>." % ("au-dessus de l’axe des abscisses" if (fn, ans) == ("sin", "positif") else "au-dessous de l’axe des abscisses" if fn == "sin" else "à droite de l’axe des ordonnées" if ans == "positif" else "à gauche de l’axe des ordonnées", fn, ans))


def s5():
    k = R.choice(["cos", "cos", "sin", "sin", "roue"])
    if k in ("cos", "sin"):
        target = R.choice([Fr(1, 2), Fr(-1, 2), "√2", "−√2", "√3", "−√3", 1, 0, -1])
        sval = {Fr(1, 2): FR(1, 2), Fr(-1, 2): MINUS + FR(1, 2), "√2": FR("√2", 2), "−√2": MINUS + FR("√2", 2), "√3": FR("√3", 2), "−√3": MINUS + FR("√3", 2), 1: "1", 0: "0", -1: MINUS + "1"}[target]
        num_ = {"√2": math.sqrt(2) / 2, "−√2": -math.sqrt(2) / 2, "√3": math.sqrt(3) / 2, "−√3": -math.sqrt(3) / 2}.get(target, float(target) if not isinstance(target, str) else 0)
        f = math.cos if k == "cos" else math.sin
        sols = sorted(t for t in [Fr(j, 12) for j in range(-11, 13)] if abs(f(float(t) * math.pi) - num_) < 1e-9)
        if not sols:
            return None
        ans = "S = {%s}" % " ; ".join(pif(t) for t in sols)
        def nrm(t):
            while t > 1:
                t -= 2
            while t <= -1:
                t += 2
            return t
        S_ = lambda ts: "S = {%s}" % " ; ".join(pif(t) for t in sorted(set(ts)))
        w = [S_([sols[0]]), S_([sols[-1]]), S_([nrm(-t) for t in sols]), S_([nrm(1 - t) for t in sols]), S_([nrm(t + Fr(1, 2)) for t in sols]), "S = ∅"]
        return M("Résous %s x = %s dans ]−π ; π]." % (k, sval), ans, w,
                 "Sur le cercle trigonométrique, on cherche les points %s %s : <b>%s</b>." % ("d’abscisse" if k == "cos" else "d’ordonnée", sval, ans))
    h0, a = R.choice([(10, 8), (12, 10), (20, 15), (6, 5)])
    T = R.choice([20, 30, 40, 60])
    t = R.choice([T // 2, T // 4, T, 3 * T // 4])
    ang = Fr(2 * t, T)
    v = h0 - a * math.cos(float(ang) * math.pi)
    return M("Une nacelle de grande roue est à la hauteur h(t) = %d − %d cos(2πt ÷ %d) mètres (t en secondes). Quelle est sa hauteur à t = %d s ?" % (h0, a, T, t), d(Fr(round(v))) + " m",
             [d(h0) + " m", d(h0 + a) + " m" if round(v) != h0 + a else d(h0 - a) + " m", d(a) + " m"], "2π × %d ÷ %d = %s et cos(%s) = %s : h = %d − %d × %s = <b>%s m</b>." % (t, T, pif(ang), pif(ang), trig_val(ang, "cos"), h0, a, "(" + trig_val(ang, "cos") + ")" if trig_val(ang, "cos").startswith(MINUS) else trig_val(ang, "cos"), d(Fr(round(v)))))


def main():
    seen = set()
    sets = [("Parité et périodicité", mix(R, seen, [(s1, 20)])), ("Angles associés", mix(R, seen, [(s2, 20)])),
            ("Calculer avec cos et sin", mix(R, seen, [(s3, 20)])), ("Courbes et signes", mix(R, seen, [(s4, 20)])), ("Équations et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["cos et sin sont définies sur ℝ, à valeurs dans [−1 ; 1], et <b>2π-périodiques</b> : cos(x + 2π) = cos x, sin(x + 2π) = sin x.",
              "cos est <b>paire</b> (cos(−x) = cos x, courbe symétrique par rapport à l’axe des ordonnées) ; sin est <b>impaire</b> (sin(−x) = −sin x, symétrie par rapport à l’origine).",
              "Angles associés : cos(π − x) = −cos x ; sin(π − x) = sin x ; cos(π + x) = −cos x ; sin(π + x) = −sin x ; cos(π/2 − x) = sin x.",
              "Pour résoudre cos x = a, on place a sur l’axe des abscisses du cercle : en général deux points, x et −x."],
             [("cos x = 1/2 dans ]−π ; π]", ["cos(π/3) = 1/2", "et cos(−π/3) = 1/2 (cos est paire)"], "S = {−π/3 ; π/3}")],
             [["cos(π − x) = cos x", "cos(π − x) = −cos x (symétrie par rapport à l’axe des ordonnées)."], ["sin est paire", "sin(−x) = −sin x : sin est impaire."],
              ["cos x = 1/2 : x = π/3 seulement", "Il y a aussi −π/3 dans ]−π ; π]."]])
    faq = [("Comment retrouver les formules des angles associés ?", "On place x, −x, π − x et π + x sur le cercle trigonométrique : les points sont symétriques par rapport aux axes ou à l’origine, ce qui donne les signes."),
           ("Pourquoi les courbes de cos et sin se ressemblent-elles ?", "Parce que sin x = cos(x − π/2) : la courbe de sin est celle de cos décalée de π/2 vers la droite.")]
    unit("premiere", R, "fonctions-cosinus-et-sinus", "F",
         "Fonctions cosinus et sinus : parité, périodicité, courbes représentatives ; lien entre le cercle trigonométrique et les courbes ; angles associés ; résoudre des équations cos x = a et sin x = a sur un intervalle",
         "Fonctions cosinus et sinus", "Fonctions cosinus et sinus",
         "Fiches de maths première sur les fonctions cosinus et sinus : parité, périodicité, angles associés, courbes, signes et équations cos x = a, sin x = a. 100 exercices corrigés.",
         "cos paire, sin impaire, période 2π", "cos(π − x) = −cos x ; sin(π − x) = sin x", body, faq, sets, 15)


if __name__ == "__main__":
    main()
