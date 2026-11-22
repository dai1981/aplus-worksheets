# -*- coding: utf-8 -*-
"""
France Maths Seconde : Vecteurs (translation, égalité, somme et relation de Chasles, produit par un réel, colinéarité)
  python3 tools/gen_fr_maths_seconde_vecteurs.py
Erreurs : AB→ + BC→ = CA→, ABCD parallélogramme ⇔ AB→ = CD→, 2u→ − u→ = 2, kAB→ de sens toujours identique.
"""
import random
from fr_c4 import *

R = random.Random(60512)
K = Kids(R)


def V(s):
    return "<span class='vec'>%s</span>" % s


def s1():
    P = R.sample("ABCDEFMN", 4)
    A, B, C, D = P
    k = R.choice(["chasles", "chasles", "chasles3", "opp"])
    if k == "chasles":
        return M("Simplifie : %s + %s" % (V(A + B), V(B + C)), V(A + C), [V(C + A), V(A + B), V(B + C)],
                 "Relation de Chasles : on va de %s à %s puis de %s à %s, on arrive en %s : <b>%s</b>." % (A, B, B, C, C, V(A + C)))
    if k == "chasles3":
        return M("Simplifie : %s + %s + %s" % (V(A + B), V(B + C), V(C + D)), V(A + D), [V(D + A), V(A + C), V(B + D)], "On enchaîne : %s → %s → %s → %s : <b>%s</b>." % (A, B, C, D, V(A + D)))
    return M("Simplifie : %s − %s" % (V(A + B), V(C + B)), V(A + C), [V(C + A), V(A + B), V(B + C)], "− %s = %s, donc %s + %s = <b>%s</b>." % (V(C + B), V(B + C), V(A + B), V(B + C), V(A + C)))


def s2():
    V_ = [("ABCD est un parallélogramme. Quel vecteur est égal à %s ?" % V("AB"), V("DC"), [V("CD"), V("BC"), V("AD")]),
          ("%s = %s (A, B, C non alignés). Quelle est la nature de ABDC ?" % (V("AB"), V("CD")), "un parallélogramme", ["un rectangle", "un trapèze quelconque", "un losange"]),
          ("I est le milieu de [AB]. Quelle égalité est vraie ?", "%s = %s" % (V("AI"), V("IB")), ["%s = %s" % (V("AI"), V("BI")), "%s = %s" % (V("IA"), V("IB")), "%s = 2%s" % (V("AI"), V("AB"))]),
          ("Deux vecteurs égaux ont…", "même direction, même sens et même norme", ["seulement la même norme", "la même origine", "des directions perpendiculaires"]),
          ("Le vecteur %s est l’opposé de…" % V("AB"), V("BA"), [V("AB"), "2" + V("AB"), V("BB")]),
          ("%s + %s = …" % (V("AB"), V("BA")), "le vecteur nul", [V("AB"), "2" + V("AB"), V("AA") + " + 1"]),
          ("ABCD est un parallélogramme. Que vaut %s + %s ?" % (V("AB"), V("AD")), V("AC"), [V("BD"), V("DB"), V("CA")]),
          ("La translation de vecteur %s transforme M en M’. Que peut-on dire de %s ?" % (V("AB"), V("MM’")), "%s = %s" % (V("MM’"), V("AB")), ["%s = %s" % (V("MM’"), V("BA")), "%s = 2%s" % (V("MM’"), V("AB")), "rien en général"])]
    q, a, w = R.choice(V_)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s2b():
    P, Q, Rr, S = R.sample("ABCDEFGHKLMNPRST", 4)
    k = R.choice(["eq", "eq", "sum", "mil"])
    if k == "eq":
        pairs = [(P + Q, S + Rr), (Q + Rr, P + S), (Q + P, Rr + S), (Rr + Q, S + P)]
        a, b = R.choice(pairs)
        wr = [b[::-1], a[::-1], (P + Rr) if a not in (P + Rr,) else (Q + S)]
        return M("%s%s%s%s est un parallélogramme. Quel vecteur est égal à %s ?" % (P, Q, Rr, S, V(a)), V(b), [V(x) for x in wr],
                 "Dans le parallélogramme %s%s%s%s, les côtés opposés donnent des vecteurs égaux (même sens) : <b>%s = %s</b>." % (P, Q, Rr, S, V(a), V(b)))
    if k == "sum":
        return M("%s%s%s%s est un parallélogramme. Que vaut %s + %s ?" % (P, Q, Rr, S, V(P + Q), V(P + S)), V(P + Rr), [V(Q + S), V(S + Q), V(Rr + P)],
                 "Règle du parallélogramme : %s + %s = %s + %s = <b>%s</b>." % (V(P + Q), V(P + S), V(P + Q), V(Q + Rr), V(P + Rr)))
    return M("%s est le milieu de [%s%s]. Quelle égalité est vraie ?" % (S, P, Q), "%s = %s" % (V(P + S), V(S + Q)), ["%s = %s" % (V(P + S), V(Q + S)), "%s = %s" % (V(S + P), V(S + Q)), "%s = 2%s" % (V(P + S), V(P + Q))],
             "%s est au milieu : <b>%s = %s</b>." % (S, V(P + S), V(S + Q)))


def s3():
    k = R.choice(["somme", "somme", "lin", "norme"])
    a, b = nz(-5, 5), nz(-5, 5)
    if k == "somme":
        c, e = nz(-5, 5), nz(-5, 5)
        r = a + c, b + e
        return M("Simplifie : (%s) + (%s)" % (comb(a, b), comb(c, e)),
                 comb(r[0], r[1]), [comb(a * c, b * e), comb(a + c, b - e) if b - e != b + e else comb(a + c + 1, b + e), comb(a + b, c + e) if (a + b, c + e) != r else comb(r[0], r[1] + 1)],
                 "On regroupe les %s et les %s : <b>%s</b>." % (V("u"), V("v"), comb(r[0], r[1])))
    if k == "lin":
        k1 = nz(-4, 4)
        return M("Développe : %s(%s)" % (d(k1) if k1 != -1 else MINUS, comb(a, b)), comb(k1 * a, k1 * b), [comb(k1 * a, b), comb(k1 + a, k1 + b), comb(a, k1 * b)],
                 "k(%s + %s) = k%s + k%s : <b>%s</b>." % (V("u"), V("v"), V("u"), V("v"), comb(k1 * a, k1 * b)))
    kk = R.choice([2, 3, Fr(1, 2), -2, -3, Fr(-1, 2)])
    n = R.randint(2, 10)
    return M("‖%s‖ = %d. Que vaut ‖%s%s‖, et quel est son sens par rapport à %s ?" % (V("u"), n, fq(kk) if Fr(kk).denominator > 1 else d(kk), V("u"), V("u")),
             "%s, %s" % (d(abs(kk) * n), "même sens" if kk > 0 else "sens contraire"), ["%s, %s" % (d(kk * n), "même sens"), "%s, %s" % (d(abs(kk) * n), "sens contraire" if kk > 0 else "même sens"), "%s, %s" % (d(n), "même sens" if kk > 0 else "sens contraire")],
             "La norme est multipliée par |k| = %s ; k est %s : <b>%s, %s</b>." % (fq(abs(Fr(kk))), "positif" if kk > 0 else "négatif", d(abs(kk) * n), "même sens" if kk > 0 else "sens contraire"))


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def cf(k):
    return "" if k == 1 else MINUS if k == -1 else d(k)


def comb(a, b):
    a, b = Fr(a), Fr(b)
    if a == 0 and b == 0:
        return "vecteur nul"
    s = ""
    if a:
        s = "%s%s" % (cf(a), V("u"))
    if b:
        s += (" + " if b > 0 else " − ") + ("" if abs(b) == 1 else d(abs(b))) + V("v") if s else "%s%s" % (cf(b), V("v"))
    return s


def s4():
    k = R.choice(["col", "col", "milieu", "align"])
    if k == "col":
        a = nz(-5, 5)
        b = R.choice([2, 3, -2, Fr(1, 2), -1])
        ok = R.random() < 0.5
        c = a * b if ok else a * b + R.choice([1, -1])
        return M("%s = %s et %s = %s. Ces vecteurs sont-ils colinéaires ?" % (V("w"), comb(a, 2), V("z"), comb(c, 2 * b)), "oui" if ok else "non", ["non" if ok else "oui", "seulement si %s et %s sont colinéaires" % (V("u"), V("v")), "on ne peut pas savoir"],
                 "%s" % ("%s = %s%s : <b>oui</b>." % (V("z"), fq(b), V("w")) if ok else "Les coefficients ne sont pas proportionnels : <b>non</b>."))
    if k == "milieu":
        V_ = [("I est le milieu de [AB]. Exprime %s en fonction de %s." % (V("AI"), V("AB")), "%s = %s%s" % (V("AI"), fr(1, 2), V("AB")), ["%s = 2%s" % (V("AI"), V("AB")), "%s = −%s%s" % (V("AI"), fr(1, 2), V("AB")), "%s = %s" % (V("AI"), V("AB"))]),
              ("I est le milieu de [AB] et M un point quelconque. Que vaut %s + %s ?" % (V("MA"), V("MB")), "2" + V("MI"), [V("MI"), V("AB"), "vecteur nul"]),
              ("I est le milieu de [AB]. Que vaut %s + %s ?" % (V("IA"), V("IB")), "le vecteur nul", [V("AB"), "2" + V("IA"), V("BA")]),
              ("%s = 3%s. Que peut-on dire de A, B et C ?" % (V("AC"), V("AB")), "ils sont alignés", ["ABC est un triangle rectangle", "C est le milieu de [AB]", "on ne peut rien dire"])]
        q, a_, w = R.choice(V_)
        return M(q, a_, w, "Réponse : <b>%s</b>." % a_)
    kk = R.choice([2, 3, -2, Fr(1, 2), Fr(3, 2), -1])
    return M("On sait que %s = %s%s. Que peut-on en déduire ?" % (V("AC"), fq(kk) if kk != -1 else MINUS, V("AB")), "A, B et C sont alignés", ["(AB) et (AC) sont perpendiculaires", "ABC est isocèle", "C est le milieu de [AB]" if kk != Fr(1, 2) else "B est le milieu de [AC]"],
             "%s et %s sont colinéaires et ont le point A en commun : <b>A, B et C sont alignés</b>." % (V("AC"), V("AB")))


def s5():
    k = R.choice(["force", "force", "deplacement", "para"])
    if k == "force":
        a, b = R.randint(2, 9), R.randint(2, 9)
        V_ = [("Deux forces de même direction et même sens, d’intensités %d N et %d N, s’exercent sur un objet. Quelle est l’intensité de la force totale ?" % (a, b), "%d N" % (a + b), ["%d N" % abs(a - b), "%d N" % (a * b), "%s N" % d(Fr(a + b, 2))]),
              ("Deux forces de même direction mais de sens contraires, d’intensités %d N et %d N. Quelle est l’intensité de la force totale ?" % (max(a, b), min(a, b) if a != b else a - 1), "%d N" % (max(a, b) - (min(a, b) if a != b else a - 1)), ["%d N" % (max(a, b) + (min(a, b) if a != b else a - 1)), "0 N", "%d N" % max(a, b)])]
        q, a_, w = R.choice(V_)
        return M(q, a_, w, "On additionne les vecteurs forces : <b>%s</b>." % a_)
    if k == "deplacement":
        n = R.randint(2, 6)
        return M("Un robot fait %d fois le même déplacement %s. Quel vecteur décrit le déplacement total ?" % (n, V("u")), "%d%s" % (n, V("u")), ["%s + %d" % (V("u"), n), V("u"), "%d%s" % (n * n, V("u"))],
                 "%s + %s + … (%d fois) = <b>%d%s</b>." % (V("u"), V("u"), n, n, V("u")))
    V_ = [("Pour démontrer que (AB) et (CD) sont parallèles, il suffit de montrer que…", "%s et %s sont colinéaires" % (V("AB"), V("CD")), ["%s = %s" % (V("AB"), V("DC")) + " est impossible", "AB = CD", "les points A, B, C, D sont alignés"]),
          ("Pour démontrer que A, B, C sont alignés, il suffit de montrer que…", "%s et %s sont colinéaires" % (V("AB"), V("AC")), ["AB = AC", "%s = %s" % (V("AB"), V("BC")) + " seulement", "ABC est isocèle"]),
          ("ABCD est un parallélogramme de centre O. Que vaut %s + %s ?" % (V("OA"), V("OC")), "le vecteur nul", ["2" + V("OA"), V("AC"), V("BD")])]
    q, a_, w = R.choice(V_)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Relation de Chasles", mix(R, seen, [(s1, 20)])), ("Égalité de vecteurs", mix(R, seen, [(s2, 6), (s2b, 14)])),
            ("Calculer avec des vecteurs", mix(R, seen, [(s3, 20)])), ("Colinéarité", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Le vecteur %s est associé à la translation qui transforme A en B : une direction, un sens et une norme (longueur AB)." % V("AB"),
              "<b>Relation de Chasles</b> : %s + %s = %s. ABDC est un parallélogramme ⇔ %s = %s." % (V("AB"), V("BC"), V("AC"), V("AB"), V("CD")),
              "k%s a la même direction que %s, une norme multipliée par |k|, le même sens si k &gt; 0 et le sens contraire si k &lt; 0. Deux vecteurs sont <b>colinéaires</b> si l’un est un multiple de l’autre." % (V("u"), V("u"))],
             [("%s + %s + %s" % (V("AB"), V("CA"), V("BC")), ["on réordonne : %s + %s + %s" % (V("CA"), V("AB"), V("BC")), "= %s" % V("CC")], "le vecteur nul")],
             [["%s + %s = %s" % (V("AB"), V("BC"), V("CA")), "On arrive en C : %s." % V("AC")], ["%s = %s ⇒ ABCD parallélogramme" % (V("AB"), V("CD")), "C’est ABDC (attention à l’ordre)."],
              ["Penser que −2%s a le même sens que %s" % (V("u"), V("u")), "k négatif : sens contraire."]])
    faq = [("À quoi sert la colinéarité ?", "À démontrer que des points sont alignés ou que des droites sont parallèles."),
           ("Quelle différence entre vecteur et segment ?", "Un segment a une longueur ; un vecteur a en plus une direction et un sens.")]
    unit("seconde", R, "vecteurs", "G",
         "Associer un vecteur à une translation ; utiliser l’égalité de vecteurs, la somme et la relation de Chasles ; multiplier un vecteur par un réel ; reconnaître des vecteurs colinéaires pour démontrer un alignement ou un parallélisme",
         "Vecteurs", "Vecteurs",
         "Fiches de maths seconde sur les vecteurs : translation, égalité, relation de Chasles, produit par un réel, colinéarité et problèmes. 100 exercices corrigés.",
         "AB→ + BC→ = AC→ (Chasles)", "Colinéaires : v→ = ku→", body, faq, sets, 12)


if __name__ == "__main__":
    main()
