# -*- coding: utf-8 -*-
"""
France Maths 3e : Statistiques (médiane, quartiles, écart interquartile, boîte à moustaches, comparer des séries)
  python3 tools/gen_fr_maths_3e_statistiques.py
Quartiles au sens du collège : Q1 = valeur de rang ⌈n/4⌉, Q3 = valeur de rang ⌈3n/4⌉ dans la série rangée.
Erreurs : ne pas ranger, Q1 = moyenne des valeurs basses, confondre étendue et écart interquartile.
"""
import random
import math
from fr_c4 import *

R = random.Random(60415)
K = Kids(R)


def med(v):
    s = sorted(v)
    n = len(s)
    return Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)


def q1(v):
    s = sorted(v)
    return s[math.ceil(len(s) / 4) - 1]


def q3(v):
    s = sorted(v)
    return s[math.ceil(3 * len(s) / 4) - 1]


def boite(mn, a, m, b, mx, lo, hi, label="boîte à moustaches"):
    W, H = 420, 120
    X = lambda v: 30 + (float(v) - lo) / (hi - lo) * (W - 60)
    s = [line(X(lo), 90, X(hi), 90, INK, 1.6)]
    step = 5 if hi - lo > 30 else 2 if hi - lo > 12 else 1
    v = lo
    while v <= hi:
        s.append(line(X(v), 86, X(v), 94, INK, 1.2) + (text(X(v), 110, str(v), 12, weight=500) if (v - lo) % (step * 2) == 0 else ""))
        v += step
    s.append(line(X(mn), 45, X(a), 45, BLUE, 2) + line(X(b), 45, X(mx), 45, BLUE, 2))
    s.append(line(X(mn), 35, X(mn), 55, BLUE, 2) + line(X(mx), 35, X(mx), 55, BLUE, 2))
    s.append("<rect x='%.1f' y='25' width='%.1f' height='40' fill='%s' stroke='%s' stroke-width='2'/>" % (X(a), X(b) - X(a), FILL, BLUE))
    s.append(line(X(m), 25, X(m), 65, RED, 2.6))
    return wrap(W, H, "".join(s), label, lg=True)


def s1():
    n = R.choice([7, 8, 9, 10, 11, 12])
    v = [R.randint(2, 20) for _ in range(n)]
    k = R.choice(["q1", "q3", "med"])
    s = sorted(v)
    if k == "med":
        m = med(v)
        return M("Série : %s. Quelle est la médiane ?" % " ; ".join(map(str, v)), d(m), [d(Fr(v[n // 2])) if Fr(v[n // 2]) != m else d(m + 1), d(Fr(sum(v), n)) if (Fr(sum(v), n) * 100).denominator == 1 and Fr(sum(v), n) != m else d(m - 1), d(Fr(n + 1, 2)) if Fr(n + 1, 2) != m else d(m + 2)],
                 "Rangée : %s. Médiane : <b>%s</b>." % (" ; ".join(map(str, s)), d(m)))
    r = math.ceil(n / 4) if k == "q1" else math.ceil(3 * n / 4)
    val = s[r - 1]
    wrong = [s[r] if s[r] != val else s[r] + 1 if r < n else val + 1, v[r - 1] if v[r - 1] != val else val - 1, r if r != val else r + 1]
    return M("Série : %s. Quel est le %s quartile ?" % (" ; ".join(map(str, v)), "premier" if k == "q1" else "troisième"), str(val), [str(x) for x in wrong],
             "Rangée : %s. %s = %d, donc on prend la %de valeur : <b>%d</b>." % (" ; ".join(map(str, s)), ("n ÷ 4 = %s" % d(Fr(n, 4))) if k == "q1" else ("3n ÷ 4 = %s" % d(Fr(3 * n, 4))), r, r, val))


def s2():
    n = R.choice([8, 9, 10, 11, 12])
    v = [R.randint(5, 40) for _ in range(n)]
    k = R.choice(["eiq", "eiq", "etendue"])
    a, b = q1(v), q3(v)
    if k == "eiq":
        return M("Série : %s. Quel est l’écart interquartile ?" % " ; ".join(map(str, v)), str(b - a), [str(max(v) - min(v)) if max(v) - min(v) != b - a else str(b - a + 1), str(b + a), str(b - a + 2)],
                 "Q1 = %d et Q3 = %d : Q3 − Q1 = <b>%d</b>." % (a, b, b - a))
    return M("Série : %s. Quelle est l’étendue ?" % " ; ".join(map(str, v)), str(max(v) - min(v)), [str(b - a) if b - a != max(v) - min(v) else str(b - a + 1), str(max(v)), str(abs(v[-1] - v[0])) if abs(v[-1] - v[0]) != max(v) - min(v) else str(max(v) + min(v))],
             "Étendue = max − min = %d − %d = <b>%d</b>." % (max(v), min(v), max(v) - min(v)))


def s3():
    mn = R.randint(0, 10)
    a = mn + R.randint(2, 8)
    m = a + R.randint(1, 6)
    b = m + R.randint(1, 8)
    mx = b + R.randint(2, 10)
    lo = mn - mn % 5
    hi = mx + (5 - mx % 5) % 5
    svg = boite(mn, a, m, b, mx, lo, hi)
    k = R.choice(["med", "q1", "q3", "eiq", "ext", "pc"])
    if k == "med":
        return M("<div class='qfig'>%s</div>Quelle est la médiane de cette série ?" % svg, str(m), [str(a), str(b), str(Fr(mn + mx, 2)) if Fr(mn + mx, 2).denominator == 1 and Fr(mn + mx, 2) != m else str(m + 1)], "La médiane est le trait à l’intérieur de la boîte : <b>%d</b>." % m)
    if k == "q1":
        return M("<div class='qfig'>%s</div>Quel est le premier quartile ?" % svg, str(a), [str(mn), str(m), str(b)], "Q1 est le bord gauche de la boîte : <b>%d</b>." % a)
    if k == "q3":
        return M("<div class='qfig'>%s</div>Quel est le troisième quartile ?" % svg, str(b), [str(mx), str(m), str(a)], "Q3 est le bord droit de la boîte : <b>%d</b>." % b)
    if k == "eiq":
        return M("<div class='qfig'>%s</div>Quel est l’écart interquartile ?" % svg, str(b - a), [str(mx - mn), str(b - m) if b - m != b - a else str(b - a + 1), str(m - a) if m - a != b - a else str(b - a + 2)], "Largeur de la boîte : %d − %d = <b>%d</b>." % (b, a, b - a))
    if k == "ext":
        return M("<div class='qfig'>%s</div>Quelle est l’étendue de la série ?" % svg, str(mx - mn), [str(b - a), str(mx), str(mx + mn)], "Bouts des moustaches : %d − %d = <b>%d</b>." % (mx, mn, mx - mn))
    return M("<div class='qfig'>%s</div>Quel pourcentage environ des valeurs est inférieur ou égal à %d ?" % (svg, b), "au moins 75 %", ["au moins 25 %", "au moins 50 %", "100 %"], "%d est le troisième quartile : <b>au moins 75 %%</b> des valeurs lui sont inférieures ou égales." % b)


def s4():
    V_ = [("Le premier quartile Q1 est la plus petite valeur telle qu’au moins…", "25 % des valeurs lui soient inférieures ou égales", ["50 % des valeurs lui soient inférieures", "75 % des valeurs lui soient inférieures ou égales", "25 % des valeurs lui soient supérieures"]),
          ("Entre Q1 et Q3, on trouve environ…", "la moitié des valeurs", ["un quart des valeurs", "toutes les valeurs", "trois quarts des valeurs"]),
          ("Quel indicateur n’est pas influencé par une valeur extrême ?", "la médiane", ["la moyenne", "l’étendue", "la somme des valeurs"]),
          ("Deux séries ont la même médiane. La série A a un écart interquartile plus petit. Que peut-on dire ?", "les valeurs centrales de A sont plus regroupées", ["A a une moyenne plus grande", "A a plus de valeurs", "les deux séries sont identiques"]),
          ("L’écart interquartile mesure…", "la dispersion des valeurs centrales", ["la valeur moyenne", "la plus grande valeur", "le nombre de valeurs"]),
          ("Dans une boîte à moustaches, le trait à l’intérieur de la boîte représente…", "la médiane", ["la moyenne", "le premier quartile", "l’étendue"])]
    q, a, w = R.choice(V_)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s4b():
    a = [R.randint(8, 15) for _ in range(8)]
    b = [R.randint(3, 20) for _ in range(8)]
    ia, ib = q3(a) - q1(a), q3(b) - q1(b)
    if ia == ib:
        return None
    ans = "la classe A" if ia < ib else "la classe B"
    return M("Notes de la classe A : %s. Notes de la classe B : %s. Quelle classe a les notes les plus homogènes (plus petit écart interquartile) ?" % (" ; ".join(map(str, a)), " ; ".join(map(str, b))), ans,
             ["la classe B" if ans == "la classe A" else "la classe A", "elles sont aussi homogènes", "on ne peut pas savoir"],
             "A : Q3 − Q1 = %d − %d = %d ; B : %d − %d = %d. <b>%s</b>." % (q3(a), q1(a), ia, q3(b), q1(b), ib, ans[0].upper() + ans[1:]))


def s5():
    k = R.choice(["salaire", "pc", "tableau", "moy"])
    if k == "salaire":
        v = sorted(R.choice([1400, 1500, 1600, 1700, 1800, 1900, 2000, 2200]) for _ in range(7)) + [R.choice([7000, 9000])]
        m = med(v)
        mo = Fr(sum(v), 8)
        return M("Salaires (en €) dans une entreprise : %s. Quelle est la médiane ?" % " ; ".join(num(x) for x in v), "%s €" % num(m) if m.denominator == 1 else "%s €" % d(m), ["%s €" % d(mo) if (mo * 100).denominator == 1 else "%s €" % num(round(mo)), "%s €" % num(v[3]) if v[3] != m else "%s €" % num(v[5]), "%s €" % num(v[-1] - v[0])],
                 "Valeurs 4 et 5 : (%s + %s) ÷ 2 = <b>%s €</b>. La moyenne est tirée vers le haut par le salaire de %s €." % (num(v[3]), num(v[4]), num(m) if m.denominator == 1 else d(m), num(v[-1])))
    if k == "pc":
        n = R.choice([20, 24, 28, 32, 40])
        return M("Dans une classe de %d élèves, le troisième quartile des tailles est 168 cm. Combien d’élèves au moins mesurent 168 cm ou moins ?" % n, str(math.ceil(3 * n / 4)), [str(n // 4), str(n // 2), str(n)],
                 "Au moins 75 %% des élèves : 0,75 × %d = <b>%d</b>." % (n, math.ceil(3 * n / 4)))
    if k == "tableau":
        vals = [10, 12, 14, 16, 18]
        eff = [R.randint(1, 5) for _ in vals]
        n = sum(eff)
        full = [x for x, e in zip(vals, eff) for _ in range(e)]
        a = q1(full)
        tb = table(["Note"] + [str(x) for x in vals], [["Effectif"] + [str(e) for e in eff]])
        return M("%s<br>Quel est le premier quartile de ces notes ?" % tb, str(a), [str(vals[1]) if vals[1] != a else str(vals[2]), str(math.ceil(n / 4)) if math.ceil(n / 4) != a else str(a + 2), str(q3(full)) if q3(full) != a else str(a + 4)],
                 "%d notes ; %d ÷ 4 = %s, on prend la %de note : <b>%d</b>." % (n, n, d(Fr(n, 4)), math.ceil(n / 4), a))
    v = [R.randint(8, 16) for _ in range(5)]
    x = R.randint(0, 20)
    nm = Fr(sum(v) + x, 6)
    if (nm * 100).denominator != 1 or (Fr(sum(v), 5) * 100).denominator != 1:
        return None
    return M("Un élève a les notes %s (moyenne %s). Il obtient %d au contrôle suivant. Quelle est sa nouvelle moyenne ?" % (" ; ".join(map(str, v)), d(Fr(sum(v), 5)), x), d(nm), [d(Fr(Fr(sum(v), 5) + x, 2)) if (Fr(Fr(sum(v), 5) + x, 2) * 100).denominator == 1 and Fr(Fr(sum(v), 5) + x, 2) != nm else d(nm + 1), d(Fr(sum(v) + x, 5)) if (Fr(sum(v) + x, 5) * 100).denominator == 1 else d(nm - 1), d(nm + Fr(1, 2))],
             "(%d + %d) ÷ 6 = %d ÷ 6 = <b>%s</b>." % (sum(v), x, sum(v) + x, d(nm)))


def main():
    seen = set()
    sets = [("Médiane et quartiles", mix(R, seen, [(s1, 20)])), ("Étendue et écart interquartile", mix(R, seen, [(s2, 20)])),
            ("Lire une boîte à moustaches", mix(R, seen, [(s3, 20)])), ("Interpréter et comparer", mix(R, seen, [(s4, 6), (s4b, 14)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["On range la série. La <b>médiane</b> partage les valeurs en deux groupes de même effectif.",
              "<b>Q1</b> est la plus petite valeur telle qu’au moins 25 % des valeurs lui soient inférieures ou égales (rang : n ÷ 4 arrondi à l’entier supérieur) ; <b>Q3</b> : au moins 75 % (rang 3n ÷ 4 arrondi à l’entier supérieur).",
              "Étendue = max − min ; <b>écart interquartile</b> = Q3 − Q1. Une boîte à moustaches résume la série : min, Q1, médiane, Q3, max."],
             [("Série rangée : 3 ; 5 ; 6 ; 8 ; 9 ; 11 ; 12 ; 15 ; 18 ; 20", ["n = 10", "Q1 : rang 3 → 6", "Q3 : rang 8 → 15"], "Q3 − Q1 = 9")],
             [["Calculer les quartiles sans ranger", "On range toujours la série d’abord."], ["Q1 = moyenne de la première moitié", "Au collège, Q1 est une valeur de la série (rang ⌈n/4⌉)."],
              ["Confondre étendue et écart interquartile", "Étendue : max − min ; écart interquartile : Q3 − Q1."]])
    faq = [("Pourquoi utiliser les quartiles ?", "Ils décrivent la répartition des valeurs sans être influencés par les valeurs extrêmes."),
           ("Comment lire une boîte à moustaches ?", "Les bouts des moustaches sont le minimum et le maximum, les bords de la boîte Q1 et Q3, le trait intérieur la médiane.")]
    unit("3e", R, "statistiques", "D",
         "Calculer et interpréter la médiane, les quartiles, l’étendue et l’écart interquartile d’une série ; lire et interpréter une boîte à moustaches ; comparer des séries statistiques",
         "Statistiques : quartiles et boîtes à moustaches", "Statistiques",
         "Fiches de maths 3e sur les statistiques : médiane, quartiles, étendue, écart interquartile, boîtes à moustaches et comparaison de séries. 100 exercices corrigés.",
         "Q1 et Q3 encadrent la moitié centrale des valeurs", "Écart interquartile = Q3 − Q1", body, faq, sets, 15)


if __name__ == "__main__":
    main()
