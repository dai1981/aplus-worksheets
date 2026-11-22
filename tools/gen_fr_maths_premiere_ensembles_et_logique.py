# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Vocabulaire ensembliste et logique (ensembles, implication, réciproque, contraposée, conditions nécessaires et suffisantes, négation, contre-exemples, raisonnements)
  python3 tools/gen_fr_maths_premiere_ensembles_et_logique.py
Erreurs : confondre réciproque et contraposée, croire qu’une implication vraie a une réciproque vraie, nier « et » par « et », nier « tous » par « aucun ».
"""
import random
from fr_ly1 import *

R = random.Random(60601)


def ens(v):
    v = sorted(v)
    return "∅" if not v else "{%s}" % " ; ".join(str(x) for x in v)


def s1():
    k = R.choice(["inter", "union", "comp", "card", "iv", "diff"])
    if k == "card":
        a, b = R.randint(12, 40), R.randint(10, 35)
        c = R.randint(2, min(a, b) - 2)
        ctx = R.choice([("élèves", "font du sport", "font de la musique"), ("clients", "ont acheté un livre", "ont acheté un jeu"), ("adhérents", "nagent", "courent")])
        return M("Dans un groupe, A est l’ensemble des %s qui %s (Card(A) = %d) et B ceux qui %s (Card(B) = %d). Card(A ∩ B) = %d. Combien d’éléments a A ∪ B ?" % (ctx[0], ctx[1], a, ctx[2], b, c),
                 str(a + b - c), [str(a + b), str(a + b + c), str(a + b - 2 * c)], "Card(A ∪ B) = Card(A) + Card(B) − Card(A ∩ B) = %d + %d − %d = <b>%d</b> (sinon on compte deux fois A ∩ B)." % (a, b, c, a + b - c))
    if k == "iv":
        a, b, c, e = sorted(R.sample(range(-9, 10), 4))
        op = R.choice(["∩", "∪"])
        I, J = "[%s ; %s]" % (d(a), d(c)), "[%s ; %s]" % (d(b), d(e))
        if op == "∩":
            ans, w = "[%s ; %s]" % (d(b), d(c)), ["[%s ; %s]" % (d(a), d(e)), "[%s ; %s]" % (d(a), d(b)), "∅"]
        else:
            ans, w = "[%s ; %s]" % (d(a), d(e)), ["[%s ; %s]" % (d(b), d(c)), "[%s ; %s]" % (d(c), d(e)), "[%s ; %s] ∪ [%s ; %s]" % (d(a), d(b), d(c), d(e))]
        return M("Détermine %s %s %s." % (I, op, J), ans, w, "Sur une droite graduée, %s : <b>%s</b>." % ("on garde la partie commune" if op == "∩" else "on réunit les deux intervalles, qui se chevauchent", ans))
    E = list(range(1, 11))
    A = set(R.sample(E, R.randint(3, 5)))
    B = set(R.sample(E, R.randint(3, 5)))
    if A == B:
        return None
    pre = "E = {1 ; 2 ; … ; 10}, A = %s et B = %s." % (ens(A), ens(B))
    if k == "inter":
        return M(pre + " Détermine A ∩ B.", ens(A & B), [ens(A | B), ens(A - B), ens(B - A), ens(set(E) - A - B), ens(A), ens(B)], "A ∩ B contient les éléments communs à A et à B : <b>%s</b>." % ens(A & B))
    if k == "union":
        return M(pre + " Détermine A ∪ B.", ens(A | B), [ens(A & B), ens(A ^ B), ens(set(E) - (A & B)), ens(A), ens(B), ens(set(E) - A)], "A ∪ B contient les éléments de A ou de B (ou des deux) : <b>%s</b>." % ens(A | B))
    if k == "diff":
        return M(pre + " Détermine A ∖ B (éléments de A qui ne sont pas dans B).", ens(A - B), [ens(B - A), ens(A & B), ens(A ^ B), ens(A), ens(B), ens(A | B)], "On retire de A les éléments de B : <b>%s</b>." % ens(A - B))
    return M(pre + " Détermine le complémentaire Ā de A dans E.", ens(set(E) - A), [ens(A), ens(set(E) - B), ens(set(E) - (A | B)), ens(B), ens(A | B)], "Ā contient les éléments de E qui ne sont pas dans A : <b>%s</b>." % ens(set(E) - A))


def tpl():
    a = R.randint(2, 9)
    b = a - R.randint(1, 5)
    k = R.randint(2, 5)
    m = R.choice([2, 3])
    T = [("x = %d" % a, "x² = %d" % (a * a), "x ≠ %d" % a, "x² ≠ %d" % (a * a), True, False),
         ("x &gt; %s" % d(a), "x &gt; %s" % d(b), "x ⩽ %s" % d(a), "x ⩽ %s" % d(b), True, False),
         ("n est divisible par %d" % (k * m), "n est divisible par %d" % k, "n n’est pas divisible par %d" % (k * m), "n n’est pas divisible par %d" % k, True, False),
         ("ABCD est un carré", "ABCD est un rectangle", "ABCD n’est pas un carré", "ABCD n’est pas un rectangle", True, False),
         ("ABCD est un losange", "les diagonales de ABCD sont perpendiculaires", "ABCD n’est pas un losange", "les diagonales de ABCD ne sont pas perpendiculaires", True, False),
         ("x = %d" % a, "%dx = %d" % (k, k * a), "x ≠ %d" % a, "%dx ≠ %d" % (k, k * a), True, True),
         ("le triangle ABC est rectangle en A", "BC² = AB² + AC²", "le triangle ABC n’est pas rectangle en A", "BC² ≠ AB² + AC²", True, True),
         ("n est pair", "n² est pair", "n est impair", "n² est impair", True, True),
         ("x ∈ [%d ; %d]" % (b, a), "x ∈ [%d ; %d]" % (b - k, a + k), "x ∉ [%d ; %d]" % (b, a), "x ∉ [%d ; %d]" % (b - k, a + k), True, False)]
    return R.choice(T)


def s2():
    P, Q, nP, nQ, pq, qp = tpl()
    k = R.choice(["rec", "contra", "vrai", "vrai_rec"])
    imp = "« Si %s, alors %s »" % (P, Q)
    if k == "rec":
        return M("Quelle est la réciproque de l’implication %s ?" % imp, "Si %s, alors %s." % (Q, P), ["Si %s, alors %s." % (nQ, nP), "Si %s, alors %s." % (nP, nQ), "Si %s, alors %s." % (P, nQ)],
                 "La réciproque échange l’hypothèse et la conclusion : <b>Si %s, alors %s</b>." % (Q, P))
    if k == "contra":
        return M("Quelle est la contraposée de l’implication %s ?" % imp, "Si %s, alors %s." % (nQ, nP), ["Si %s, alors %s." % (Q, P), "Si %s, alors %s." % (nP, nQ), "Si %s, alors %s." % (nQ, P)],
                 "La contraposée de « P ⇒ Q » est « non Q ⇒ non P » : <b>Si %s, alors %s</b>. Elle a la même valeur de vérité que l’implication." % (nQ, nP))
    if k == "vrai":
        ans = "vraie" if pq else "fausse"
        return M("L’implication %s est-elle vraie ?" % imp, ans, ["fausse" if pq else "vraie", "vraie seulement si sa réciproque est vraie", "on ne peut pas savoir"],
                 "Dès que « %s » est vrai, « %s » l’est aussi : l’implication est <b>vraie</b>." % (P, Q) if pq else "Elle est <b>fausse</b>.")
    ans = "vraie" if qp else "fausse"
    return M("L’implication %s est vraie. Sa réciproque est-elle vraie ?" % imp, ans, ["fausse" if qp else "vraie", "toujours vraie, comme l’implication", "elle n’existe pas"],
             ("La réciproque « Si %s, alors %s » est <b>vraie</b> ici : les deux propositions sont équivalentes." % (Q, P)) if qp else
             ("La réciproque « Si %s, alors %s » est <b>fausse</b> : une implication vraie peut avoir une réciproque fausse." % (Q, P)))


def s3():
    a = R.randint(2, 9)
    P, Q, nP, nQ, pq, qp = tpl()
    if R.random() < 0.25:
        b = a + R.randint(2, 6)
        P, Q, pq, qp = R.choice([("x &gt; %d" % a, "x &lt; %d" % b, False, False), ("n est pair", "n est un multiple de %d" % R.choice([3, 5, 7]), False, False),
                                 ("x² = %d" % (a * a), "x = %d" % a, False, True)])
    swap = R.random() < 0.5
    if swap:
        P, Q, pq, qp = Q, P, qp, pq
    lab = {(True, True): "nécessaire et suffisante", (True, False): "suffisante mais pas nécessaire", (False, True): "nécessaire mais pas suffisante", (False, False): "ni nécessaire ni suffisante"}
    ans = lab[(pq, qp)]
    w = [v for v in lab.values() if v != ans]
    expl = "« %s » ⇒ « %s » est %s ; « %s » ⇒ « %s » est %s. La condition %s <b>%s</b>." % (P, Q, "vraie" if pq else "fausse", Q, P, "vraie" if qp else "fausse", "n’est" if ans.startswith("ni") else "est", ans)
    return M("Pour avoir « %s », la condition « %s » est :" % (Q, P), ans, w, expl)


def s4():
    a, b = R.randint(-5, 9), R.randint(-5, 9)
    k = R.choice(["simple", "et", "ou", "tous", "existe", "tous2"])
    if k == "simple":
        op, neg, w = R.choice([("&gt;", "⩽", ["&lt;", "⩾", "≠"]), ("⩾", "&lt;", ["⩽", "&gt;", "="]), ("&lt;", "⩾", ["&gt;", "⩽", "≠"])])
        return M("Quelle est la négation de « x %s %s » ?" % (op, d(a)), "x %s %s" % (neg, d(a)), ["x %s %s" % (o, d(a)) for o in w], "Le contraire de « %s » est « %s » : <b>x %s %s</b>." % (op, neg, neg, d(a)))
    if k == "et":
        return M("Quelle est la négation de « x &gt; %s et y ⩽ %s » ?" % (d(a), d(b)), "x ⩽ %s ou y &gt; %s" % (d(a), d(b)),
                 ["x ⩽ %s et y &gt; %s" % (d(a), d(b)), "x &lt; %s ou y ⩾ %s" % (d(a), d(b)), "x &gt; %s ou y ⩽ %s" % (d(a), d(b))],
                 "La négation de « P et Q » est « non P <b>ou</b> non Q » : <b>x ⩽ %s ou y &gt; %s</b>." % (d(a), d(b)))
    if k == "ou":
        lo, hi = sorted(R.sample(range(-8, 10), 2))
        return M("Quelle est la négation de « x &lt; %s ou x &gt; %s » ?" % (d(lo), d(hi)), "x ⩾ %s et x ⩽ %s" % (d(lo), d(hi)),
                 ["x ⩾ %s ou x ⩽ %s" % (d(lo), d(hi)), "x &gt; %s et x &lt; %s" % (d(lo), d(hi)), "x &lt; %s et x &gt; %s" % (d(lo), d(hi))],
                 "La négation de « P ou Q » est « non P <b>et</b> non Q » : <b>%s ⩽ x ⩽ %s</b>." % (d(lo), d(hi)))
    if k in ("tous", "tous2"):
        a = abs(a) + 2
        g, gs, sing, att, atts = R.choice([("les nombres de la liste", "sont supérieurs", "nombre de la liste", "est", "sont"), ("les termes de la suite", "sont supérieurs", "terme de la suite", "est", "sont"),
                                           ("les élèves de la classe", "ont une note supérieure", "élève de la classe", "a une note", "ont une note")])
        fem = "note" in att
        inf, infeg = ("inférieure", "inférieure ou égale") if fem else ("inférieur", "inférieur ou égal")
        infs = "inférieure" if fem else "inférieurs"
        sup = "supérieure" if fem else "supérieur"
        neg_att = "n’a une note" if fem else "n’est"
        return M("Quelle est la négation de « Tous %s %s à %d » ?" % (g, gs, a), "Au moins un %s %s %s à %d" % (sing, att, infeg, a),
                 ["Tous %s %s %s à %d" % (g, atts, infs, a), "Aucun %s %s %s à %d" % (sing, neg_att, sup, a), "Au moins un %s %s %s à %d" % (sing, att, inf, a)],
                 "La négation de « tous … vérifient P » est « <b>au moins un</b> … ne vérifie pas P ». Le contraire de « %s à %d » est « %s à %d »." % (sup, a, infeg, a))
    a = abs(a) + 1
    return M("Quelle est la négation de « Il existe un réel x tel que x² = %d » ?" % a, "Pour tout réel x, x² ≠ %d" % a,
             ["Il existe un réel x tel que x² ≠ %d" % a, "Pour tout réel x, x² = %d" % a, "Il n’existe aucun réel x tel que x² ≠ %d" % a],
             "La négation de « il existe … tel que P » est « pour tout …, non P » : <b>pour tout réel x, x² ≠ %d</b>." % a)


def s5():
    k = R.choice(["x2", "carre", "sup", "racine", "type", "type"])
    if k == "x2":
        c = R.choice(["0,5", "0,2", "0,3", "0,8", "0,25", "0,4"])
        others = R.sample(["0", "1", "2", "3", MINUS + "1", MINUS + "2", "10", "5"], 3)
        return M("On veut montrer que « pour tout réel x, x² ⩾ x » est fausse. Quelle valeur de x est un contre-exemple (parmi %s ; %s ; %s ; %s) ?" % tuple(sorted([c] + others)), c, others,
                 "Pour x = %s, x² = %s &lt; x : <b>%s</b> est un contre-exemple. Les autres valeurs vérifient x² ⩾ x." % (c, d(Fr(c.replace(",", ".")) ** 2), c))
    if k == "carre":
        a, b = R.randint(1, 6), R.randint(1, 6)
        return M("« Pour tous réels a et b, (a + b)² = a² + b². » Quel couple est un contre-exemple ?", "a = %d et b = %d" % (a, b), ["a = %d et b = 0" % a, "a = 0 et b = %d" % b, "a = 0 et b = 0"],
                 "(%d + %d)² = %d mais %d² + %d² = %d : <b>a = %d et b = %d</b> est un contre-exemple (avec a = 0 ou b = 0 l’égalité est vraie)." % (a, b, (a + b) ** 2, a, b, a * a + b * b, a, b))
    if k == "sup":
        a = R.randint(1, 9)
        c = a + R.randint(1, 4)
        return M("« Pour tout réel x, si x² &gt; %d alors x &gt; %d. » Quelle valeur de x est un contre-exemple ?" % (a * a, a), "x = %s" % d(-c), ["x = %d" % c, "x = %d" % a, "x = 0"],
                 "Pour x = %s : x² = %d &gt; %d mais x &lt; %d. <b>x = %s</b> est un contre-exemple." % (d(-c), c * c, a * a, a, d(-c)))
    if k == "racine":
        c = R.choice(["0,25", "0,04", "0,09", "0,16", "0,36", "0,49", "0,64", "0,81"])
        others = R.sample(["4", "9", "16", "25", "100", "2", "3"], 3)
        return M("« Pour tout réel x &gt; 0, √x ⩽ x. » Quelle valeur est un contre-exemple (parmi %s ; %s ; %s ; %s) ?" % tuple(sorted([c] + others, key=lambda t: float(t.replace(",", ".")))), c, others,
                 "√%s = 0,%d &gt; %s : <b>%s</b> est un contre-exemple (entre 0 et 1, √x &gt; x)." % (c, int(round(float(c.replace(",", ".")) ** 0.5 * 10)), c, c))
    T = [("Pour montrer que √2 est irrationnel, on suppose que √2 = p/q (fraction irréductible) et on arrive à une contradiction. Quel raisonnement est utilisé ?", "par l’absurde", ["par contraposition", "par disjonction des cas", "par contre-exemple"]),
         ("Pour montrer « si n² est pair, alors n est pair », on montre « si n est impair, alors n² est impair ». Quel raisonnement est utilisé ?", "par contraposition", ["par l’absurde", "par disjonction des cas", "par la réciproque"]),
         ("Pour montrer que n(n + 1) est pair, on étudie le cas n pair puis le cas n impair. Quel raisonnement est utilisé ?", "par disjonction des cas", ["par l’absurde", "par contraposition", "par contre-exemple"]),
         ("Pour montrer que « tout nombre premier est impair » est fausse, on cite le nombre 2. Quel raisonnement est utilisé ?", "un contre-exemple", ["par l’absurde", "par contraposition", "par disjonction des cas"]),
         ("Pour montrer que |x| ⩾ x pour tout réel x, on traite x ⩾ 0 puis x &lt; 0. Quel raisonnement est utilisé ?", "par disjonction des cas", ["par contraposition", "par l’absurde", "un contre-exemple"]),
         ("Pour montrer « si n n’est pas divisible par 3, alors n² non plus », on montre « si n² est divisible par 3, alors n l’est ». Quel raisonnement est utilisé ?", "par contraposition", ["par l’absurde", "par la réciproque", "par disjonction des cas"])]
    q, a_, w = R.choice(T)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Ensembles et intervalles", mix(R, seen, [(s1, 20)])), ("Implication, réciproque et contraposée", mix(R, seen, [(s2, 20)])),
            ("Conditions nécessaires et suffisantes", mix(R, seen, [(s3, 20)])), ("Négation d’une proposition", mix(R, seen, [(s4, 20)])),
            ("Contre-exemples et raisonnements", mix(R, seen, [(s5, 20)]))]
    body = L(["A ∩ B : éléments communs ; A ∪ B : éléments de A ou de B ; Ā : éléments qui ne sont pas dans A. Card(A ∪ B) = Card(A) + Card(B) − Card(A ∩ B).",
              "« P ⇒ Q » : si P est vraie, Q est vraie. Sa <b>réciproque</b> est « Q ⇒ P » (pas forcément vraie). Sa <b>contraposée</b> « non Q ⇒ non P » a toujours la même valeur de vérité.",
              "Si P ⇒ Q est vraie, P est une condition <b>suffisante</b> pour Q, et Q une condition <b>nécessaire</b> pour P.",
              "Négations : non (P et Q) = non P ou non Q ; non (P ou Q) = non P et non Q ; « tous » devient « au moins un … ne … pas »."],
             [("« Si x = 3, alors x² = 9 »", ["Vraie.", "Réciproque : si x² = 9, alors x = 3 : fausse (x = −3).", "Contraposée : si x² ≠ 9, alors x ≠ 3 : vraie."], "x = 3 est une condition suffisante, pas nécessaire, pour x² = 9")],
             [["Confondre réciproque et contraposée", "Réciproque : Q ⇒ P. Contraposée : non Q ⇒ non P."], ["Négation de « x &gt; 2 » : « x &lt; 2 »", "C’est « x ⩽ 2 »."],
              ["Négation de « tous sont reçus » : « aucun n’est reçu »", "C’est « au moins un n’est pas reçu »."], ["Un exemple prouve une affirmation générale", "Un exemple ne prouve rien ; un contre-exemple suffit pour montrer qu’elle est fausse."]])
    faq = [("Une implication vraie a-t-elle toujours une réciproque vraie ?", "Non. « Si x = 3, alors x² = 9 » est vraie, mais sa réciproque est fausse (x = −3)."),
           ("Quand utiliser la contraposée ?", "Quand la conclusion « non P » est plus facile à obtenir à partir de « non Q » : on montre « non Q ⇒ non P », ce qui prouve « P ⇒ Q »."),
           ("Que signifie « condition nécessaire et suffisante » ?", "P ⇔ Q : P ⇒ Q et Q ⇒ P sont vraies toutes les deux. On dit aussi « si et seulement si ».")]
    unit("premiere", R, "ensembles-et-logique", "L",
         "Utiliser le vocabulaire ensembliste (appartenance, inclusion, réunion, intersection, complémentaire, cardinal) ; distinguer implication, réciproque et contraposée, conditions nécessaires et suffisantes ; formuler la négation d’une proposition avec « et », « ou », « tous », « il existe » ; utiliser un contre-exemple, le raisonnement par l’absurde, par contraposition et par disjonction des cas",
         "Ensembles et logique : implication, réciproque, contraposée", "Ensembles et logique",
         "Fiches de maths première sur le vocabulaire ensembliste et la logique : réunion, intersection, implication, réciproque, contraposée, conditions nécessaires et suffisantes, négation et contre-exemples. 100 exercices corrigés.",
         "P ⇒ Q a la même valeur que non Q ⇒ non P", "La réciproque Q ⇒ P peut être fausse", body, faq, sets, 1)


if __name__ == "__main__":
    main()
