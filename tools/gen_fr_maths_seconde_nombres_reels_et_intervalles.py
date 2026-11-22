# -*- coding: utf-8 -*-
"""
France Maths Seconde : Ensembles de nombres (ℕ, ℤ, 𝔻, ℚ, ℝ) et intervalles
  python3 tools/gen_fr_maths_seconde_nombres_reels_et_intervalles.py
Erreurs : 1/3 décimal, crochet du mauvais sens, −∞ avec un crochet fermé, confondre réunion et intersection.
"""
import random
from fr_c4 import *

R = random.Random(60502)
K = Kids(R)
SETS = ["ℕ", "ℤ", "𝔻", "ℚ", "ℝ"]


def smallest(kind):
    """texte d’un nombre dont le plus petit ensemble est kind"""
    if kind == "ℕ":
        return R.choice([str(R.randint(0, 99)), "√%d" % R.choice([4, 9, 16, 25, 49])])
    if kind == "ℤ":
        return R.choice(["−%d" % R.randint(1, 99), "−√%d" % R.choice([4, 9, 16, 25])])
    if kind == "𝔻":
        x = Fr(R.randint(1, 999), R.choice([10, 100, 1000]))
        if x.denominator == 1:
            x += Fr(1, 10)
        return R.choice([d(x), fr(R.randint(1, 9) * 2 + 1, R.choice([4, 8, 20]))])
    if kind == "ℚ":
        return R.choice([fr(R.choice([1, 2, 4, 5, 7]), R.choice([3, 9, 11])), "−" + fr(R.choice([1, 2, 5]), R.choice([3, 7]))])
    return R.choice(["π", "√%d" % R.choice([2, 3, 5, 7, 10]), "π ÷ 2"])


def s1():
    kind = R.choice(SETS)
    t = smallest(kind)
    return M("Quel est le plus petit ensemble de nombres qui contient %s ?" % t, kind, [s_ for s_ in SETS if s_ != kind][:3] if kind != "ℝ" else ["ℚ", "𝔻", "ℤ"],
             "ℕ ⊂ ℤ ⊂ 𝔻 ⊂ ℚ ⊂ ℝ. %s appartient à <b>%s</b> mais pas à l’ensemble précédent." % (t, kind))


def s1b():
    V = [("Le nombre %s est-il décimal ?" % fr(1, 3), "non : 1 ÷ 3 = 0,333… ne s’arrête pas", ["oui, il vaut 0,33", "oui, c’est une fraction", "on ne peut pas savoir"]),
         ("Le nombre √2 est…", "irrationnel", ["rationnel", "décimal", "entier"]),
         ("Le nombre π est…", "irrationnel", ["égal à 3,14", "rationnel, égal à 22/7", "décimal"]),
         ("Quelle affirmation est vraie ?", "tout nombre décimal est rationnel", ["tout rationnel est décimal", "tout réel est rationnel", "tout entier relatif est naturel"]),
         ("Le nombre −7 appartient à…", "ℤ, 𝔻, ℚ et ℝ", ["ℕ seulement", "ℤ seulement", "ℝ seulement"]),
         ("Le nombre %s est-il décimal ?" % fr(7, 4), "oui : 7 ÷ 4 = 1,75", ["non, c’est une fraction", "non, il n’est pas entier", "on ne peut pas savoir"]),
         ("√9 appartient à…", "ℕ", ["ℝ seulement", "ℚ mais pas ℕ", "aucun ensemble"]),
         ("Que signifie l’écriture ℤ ⊂ ℚ ?", "tout entier relatif est un nombre rationnel", ["tout rationnel est un entier", "ℤ et ℚ sont égaux", "ℤ et ℚ n’ont rien en commun"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def iv(a, b, ca, cb):
    """intervalle : ca, cb = True si fermé"""
    A = "−∞" if a is None else d(a)
    B = "+∞" if b is None else d(b)
    return "%s%s ; %s%s" % ("[" if ca and a is not None else "]", A, B, "]" if cb and b is not None else "[")


def s2():
    a = R.randint(-9, 6)
    b = a + R.randint(1, 10)
    k = R.choice(["ab", "ab", "inf", "sup"])
    if k == "ab":
        ca, cb = R.choice([(True, True), (True, False), (False, True), (False, False)])
        ineq = "%s %s x %s %s" % (d(a), "⩽" if ca else "&lt;", "⩽" if cb else "&lt;", d(b))
        ans = iv(a, b, ca, cb)
        w = [iv(a, b, not ca, not cb), iv(a, b, not ca, cb) if (ca, cb) != (False, True) else iv(a, b, True, True), iv(a, b, ca, not cb) if (ca, cb) != (True, False) else iv(a, b, False, False)]
        return M("Quel intervalle correspond à %s ?" % ineq, ans, w, "Crochet tourné vers le nombre s’il est inclus (⩽), vers l’extérieur s’il est exclu (&lt;) : <b>%s</b>." % ans)
    if k == "inf":
        c = R.choice([True, False])
        ans = iv(None, b, False, c)
        return M("Quel intervalle correspond à x %s %s ?" % ("⩽" if c else "&lt;", d(b)), ans, [iv(None, b, False, not c), iv(b, None, c, False), "[−∞ ; %s]" % d(b) if c else "[−∞ ; %s[" % d(b)],
                 "Les nombres %s %s : <b>%s</b> (toujours un crochet ouvert du côté de −∞)." % ("inférieurs ou égaux à" if c else "strictement inférieurs à", d(b), ans))
    c = R.choice([True, False])
    ans = iv(a, None, c, False)
    return M("Quel intervalle correspond à x %s %s ?" % ("⩾" if c else "&gt;", d(a)), ans, [iv(a, None, not c, False), iv(None, a, False, c), "[%s ; +∞]" % d(a) if c else "]%s ; +∞]" % d(a)],
             "Les nombres %s %s : <b>%s</b>." % ("supérieurs ou égaux à" if c else "strictement supérieurs à", d(a), ans))


def s3():
    a = R.randint(-6, 4)
    b = a + R.randint(2, 8)
    ca, cb = R.choice([True, False]), R.choice([True, False])
    k = R.choice(["app", "app", "ent"])
    if k == "app":
        x = R.choice([a, b, Fr(a + b, 2), a - 1, b + 1, Fr(2 * a + 1, 2)])
        ok = (a < x < b) or (x == a and ca) or (x == b and cb)
        return M("Le nombre %s appartient-il à l’intervalle %s ?" % (d(x), iv(a, b, ca, cb)), "oui" if ok else "non", ["non" if ok else "oui", "seulement s’il est entier", "on ne peut pas savoir"],
                 "%s" % ("<b>oui</b>" if ok else "<b>non</b>") + (" (borne %s)." % ("incluse" if ok else "exclue") if x in (a, b) else "."))
    ents = [n for n in range(a, b + 1) if (a < n < b) or (n == a and ca) or (n == b and cb)]
    return M("Combien d’entiers appartiennent à l’intervalle %s ?" % iv(a, b, ca, cb), str(len(ents)), [str(b - a + 1) if b - a + 1 != len(ents) else str(len(ents) + 1), str(b - a) if b - a != len(ents) else str(len(ents) - 1), str(len(ents) + 2)],
             "Ce sont %s : <b>%d</b>." % (", ".join(d(n) for n in ents), len(ents)))


def s4():
    a, b, c, e = sorted(R.sample(range(-9, 10), 4))
    k = R.choice(["inter", "union", "inter2"])
    if k == "inter":
        return M("Quelle est l’intersection [%s ; %s] ∩ [%s ; %s] ?" % (d(a), d(c), d(b), d(e)), "[%s ; %s]" % (d(b), d(c)), ["[%s ; %s]" % (d(a), d(e)), "[%s ; %s]" % (d(a), d(b)), "∅"],
                 "Les nombres communs aux deux intervalles : <b>[%s ; %s]</b>." % (d(b), d(c)))
    if k == "union":
        return M("Quelle est la réunion [%s ; %s] ∪ [%s ; %s] ?" % (d(a), d(c), d(b), d(e)), "[%s ; %s]" % (d(a), d(e)), ["[%s ; %s]" % (d(b), d(c)), "[%s ; %s] ∪ [%s ; %s]" % (d(a), d(b), d(c), d(e)), "∅"],
                 "Les nombres qui sont dans l’un ou l’autre : <b>[%s ; %s]</b>." % (d(a), d(e)))
    return M("Quelle est l’intersection [%s ; %s] ∩ [%s ; %s] ?" % (d(a), d(b), d(c), d(e)), "∅", ["[%s ; %s]" % (d(b), d(c)), "[%s ; %s]" % (d(a), d(e)), "{%s ; %s}" % (d(b), d(c))],
             "Les intervalles n’ont aucun nombre en commun : <b>∅</b> (ensemble vide).")


def s5():
    k = R.choice(["temp", "age", "taille", "prix"])
    a = R.randint(-10, 2)
    b = a + R.randint(5, 12)
    if k == "temp":
        return M("Dans une ville, la température d’hiver reste entre %s °C (inclus) et %s °C (inclus). Quel intervalle la décrit ?" % (d(a), d(b)), "[%s ; %s]" % (d(a), d(b)), ["]%s ; %s[" % (d(a), d(b)), "[%s ; %s]" % (d(b), d(a)), "]−∞ ; %s]" % d(b)],
                 "Les deux bornes sont incluses : <b>[%s ; %s]</b>." % (d(a), d(b)))
    if k == "age":
        n = R.choice([12, 16, 18])
        return M("Un film est interdit aux moins de %d ans. Quel intervalle décrit les âges autorisés ?" % n, "[%d ; +∞[" % n, ["]%d ; +∞[" % n, "[0 ; %d[" % n, "[%d ; +∞]" % n],
                 "À partir de %d ans inclus : <b>[%d ; +∞[</b>." % (n, n))
    if k == "taille":
        h = R.choice([120, 130, 140])
        return M("Une attraction est réservée aux personnes de plus de %d cm (exclu) et de moins de 2 m (exclu). Quel intervalle (en cm) ?" % h, "]%d ; 200[" % h, ["[%d ; 200]" % h, "]%d ; 2[" % h, "[%d ; 200[" % h],
                 "Les deux bornes sont exclues : <b>]%d ; 200[</b>." % h)
    p = R.choice([20, 30, 50])
    return M("Un article coûte au plus %d €. Quel intervalle décrit son prix x (en €) ?" % p, "]0 ; %d]" % p, ["]0 ; %d[" % p, "[%d ; +∞[" % p, "]−∞ ; %d]" % p],
             "Un prix est positif et « au plus » inclut %d : <b>]0 ; %d]</b>." % (p, p))


def main():
    seen = set()
    sets = [("Ensembles de nombres", mix(R, seen, [(s1, 12), (s1b, 8)])), ("Écrire un intervalle", mix(R, seen, [(s2, 20)])),
            ("Appartenance à un intervalle", mix(R, seen, [(s3, 20)])), ("Intersection et réunion", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["ℕ (entiers naturels) ⊂ ℤ (entiers relatifs) ⊂ 𝔻 (décimaux) ⊂ ℚ (rationnels) ⊂ ℝ (réels). √2 et π sont <b>irrationnels</b>.",
              "Un <b>intervalle</b> s’écrit avec des crochets : [a ; b] contient a et b, ]a ; b[ les exclut. Du côté de −∞ ou +∞, le crochet est toujours ouvert.",
              "∩ (intersection) : les nombres communs aux deux ensembles ; ∪ (réunion) : les nombres de l’un ou de l’autre."],
             [("−2 &lt; x ⩽ 5", ["−2 exclu : ]−2", "5 inclus : 5]"], "]−2 ; 5]")],
             [["1/3 = 0,33, donc 1/3 est décimal", "1/3 = 0,333… : il n’est pas décimal."], ["Écrire [−∞ ; 3]", "On écrit ]−∞ ; 3]."],
              ["Confondre ∩ et ∪", "∩ = « et » (en commun) ; ∪ = « ou » (l’un ou l’autre)."]])
    faq = [("Quelle différence entre décimal et rationnel ?", "Un décimal s’écrit avec un nombre fini de chiffres après la virgule ; un rationnel est un quotient d’entiers (il peut avoir une écriture décimale illimitée périodique)."),
           ("Comment représenter un intervalle ?", "Sur une droite graduée, on colorie la partie concernée et on met des crochets aux bornes.")]
    unit("seconde", R, "nombres-reels-et-intervalles", "N",
         "Connaître les ensembles ℕ, ℤ, 𝔻, ℚ et ℝ ; savoir que √2 et π sont irrationnels ; représenter et écrire des intervalles ; tester l’appartenance d’un nombre à un intervalle ; déterminer une intersection ou une réunion d’intervalles",
         "Nombres réels et intervalles", "Nombres réels et intervalles",
         "Fiches de maths seconde sur les ensembles de nombres et les intervalles : ℕ, ℤ, 𝔻, ℚ, ℝ, notation des intervalles, appartenance, intersection et réunion. 100 exercices corrigés.",
         "ℕ ⊂ ℤ ⊂ 𝔻 ⊂ ℚ ⊂ ℝ", "[a ; b] : bornes incluses ; ]a ; b[ : bornes exclues", body, faq, sets, 2)


if __name__ == "__main__":
    main()
