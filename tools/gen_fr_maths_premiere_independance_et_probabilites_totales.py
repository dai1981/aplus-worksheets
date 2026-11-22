# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Indépendance et probabilités totales (partition, formule des probabilités totales, indépendance de deux événements, succession d’épreuves indépendantes, répétitions de Bernoulli jusqu’à 4 épreuves)
  python3 tools/gen_fr_maths_premiere_independance_et_probabilites_totales.py
Erreurs : P(B) = P_A(B) + P_Ā(B), confondre indépendants et incompatibles, oublier les différents ordres (chemins) dans les répétitions, p² au lieu de 2p(1 − p).
"""
import random
from math import comb
from fr_ly1 import *
from fr_c4 import val

R = random.Random(60621)


def P_(a, b):
    return "P<sub>%s</sub>(%s)" % (a, b)


def s1():
    pa = Fr(R.randint(1, 9), 10)
    pba, pbna = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
    pb = pa * pba + (1 - pa) * pbna
    k = R.choice(["text", "text", "arbre"])
    q = ("P(A) = %s, %s = %s et %s = %s. Calcule P(B)." % (d(pa), P_("A", "B"), d(pba), P_("Ā", "B"), d(pbna))) if k == "text" else "<div class='qfig'>%s</div>Calcule P(B)." % arbre(pa, pba, pbna)
    return M(q, d(pb), [d(pba + pbna) if pba + pbna <= 1 else d(pba * pbna), d(pa * pba), d(pa * pba + pa * pbna), d(pa * pba + (1 - pa) * (1 - pbna))],
             "Formule des probabilités totales (A, Ā partition) : P(B) = %s × %s + %s × %s = <b>%s</b>." % (d(pa), d(pba), d(1 - pa), d(pbna), d(pb)))


def s2():
    ps = R.choice([(Fr(5, 10), Fr(3, 10), Fr(2, 10)), (Fr(4, 10), Fr(35, 100), Fr(25, 100)), (Fr(6, 10), Fr(25, 100), Fr(15, 100)), (Fr(2, 10), Fr(5, 10), Fr(3, 10))])
    ds = [Fr(R.randint(1, 9), 100) for _ in range(3)]
    k = R.choice(["tot", "tot", "inv"])
    tot = sum(p * q for p, q in zip(ps, ds))
    lab = R.choice([("trois usines U₁, U₂, U₃", "défectueuse"), ("trois fournisseurs F₁, F₂, F₃", "abîmée"), ("trois lignes de bus L₁, L₂, L₃", "en retard")])
    q = "Les pièces viennent de %s dans les proportions %s, %s et %s. Elles sont %s avec les probabilités %s, %s et %s." % (lab[0], d(ps[0]), d(ps[1]), d(ps[2]), lab[1] + "s" if not lab[1].startswith("en") else lab[1], d(ds[0]), d(ds[1]), d(ds[2]))
    if "bus" in lab[0]:
        q = "Les trajets se font avec %s dans les proportions %s, %s et %s. Ils sont en retard avec les probabilités %s, %s et %s." % (lab[0], d(ps[0]), d(ps[1]), d(ps[2]), d(ds[0]), d(ds[1]), d(ds[2]))
    if k == "tot":
        return M(q + " Quelle est la probabilité qu’un%s soit %s ?" % ("e pièce" if "bus" not in lab[0] else " trajet", lab[1]), d(tot), [d(sum(ds)), d(sum(ds) / 3) if (sum(ds) / 3).denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000) else d(ds[0]), d(ps[0] * ds[0])],
                 "On additionne les trois chemins : %s = <b>%s</b>." % (" + ".join("%s × %s" % (d(p), d(q_)) for p, q_ in zip(ps, ds)), d(tot)))
    v = ps[0] * ds[0] / tot
    return M(q + " Sachant qu’%s est %s, quelle est la probabilité qu’%s vienne de %s (arrondie à 0,01) ?" % ("une pièce" if "bus" not in lab[0] else "un trajet", lab[1], "elle" if "bus" not in lab[0] else "il", lab[0].split(" ")[-3].rstrip(",")),
             dk(v, 2), [dk(ds[0], 2), d(ps[0] * ds[0]), dk(ps[0], 2) if dk(ps[0], 2) != dk(v, 2) else dk(v + Fr(1, 10), 2)],
             "P(… ∩ %s) ÷ P(%s) = %s ÷ %s ≈ <b>%s</b>." % (lab[1], lab[1], d(ps[0] * ds[0]), d(tot), dk(v, 2)))


def s3():
    k = R.choice(["test", "test", "inter", "vs"])
    pa, pb = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
    if k == "test":
        ind = R.random() < 0.5
        pab = pa * pb if ind else pa * pb + R.choice([Fr(1, 100), Fr(-1, 100), Fr(2, 100), Fr(5, 100)])
        if pab <= 0 or pab > min(pa, pb):
            return None
        return M("P(A) = %s, P(B) = %s et P(A ∩ B) = %s. Les événements A et B sont-ils indépendants ?" % (d(pa), d(pb), d(pab)), "oui" if ind else "non",
                 ["non" if ind else "oui", "oui, car P(A ∩ B) ≠ 0", "on ne peut pas savoir"],
                 "P(A) × P(B) = %s %s P(A ∩ B) : <b>%s</b>." % (d(pa * pb), "=" if ind else "≠", "indépendants" if ind else "pas indépendants"))
    if k == "inter":
        sub = R.choice(["inter", "union"])
        if sub == "inter":
            return M("A et B sont indépendants, P(A) = %s et P(B) = %s. Calcule P(A ∩ B)." % (d(pa), d(pb)), d(pa * pb), [d(pa + pb) if pa + pb <= 1 else d(pa), "0", d(pa + pb - pa * pb)],
                     "Indépendants : P(A ∩ B) = P(A) × P(B) = <b>%s</b>." % d(pa * pb))
        return M("A et B sont indépendants, P(A) = %s et P(B) = %s. Calcule P(A ∪ B)." % (d(pa), d(pb)), d(pa + pb - pa * pb), [d(pa + pb) if pa + pb <= 1 else "1", d(pa * pb), d(1 - pa * pb)],
                 "P(A ∪ B) = P(A) + P(B) − P(A) × P(B) = <b>%s</b>." % d(pa + pb - pa * pb))
    return M("A et B sont deux événements de probabilités non nulles. S’ils sont incompatibles (A ∩ B = ∅), peuvent-ils être indépendants ?", "non, car P(A ∩ B) = 0 ≠ P(A) × P(B)",
             ["oui, toujours", "oui, si P(A) = P(B)", "on ne peut pas savoir"], "Incompatibles : P(A ∩ B) = 0, alors que P(A) × P(B) &gt; 0 : <b>ils ne sont pas indépendants</b>.") if R.random() < 0.2 else \
        M("A et B sont indépendants avec P(A) = %s. Que vaut %s ?" % (d(pa), P_("B", "A")), d(pa), [d(1 - pa), d(pa * pb), d(pb)], "Indépendants : %s = P(A) = <b>%s</b>." % (P_("B", "A"), d(pa)))


def s4():
    n = R.choice([2, 3, 3, 4, 4])
    p = R.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(1, 5), Fr(2, 5), Fr(1, 6), Fr(3, 10), Fr(2, 3), Fr(3, 4)])
    k = R.randint(0, n)
    v = comb(n, k) * p ** k * (1 - p) ** (n - k)
    ctx = R.choice(["On lance %d fois une pièce truquée qui donne pile avec la probabilité %s.", "Un tireur atteint la cible avec la probabilité %s. Il tire %d fois, les tirs étant indépendants.",
                    "Une ampoule est défectueuse avec la probabilité %s. On en prend %d au hasard (tirages indépendants)."])
    if ctx.startswith("On lance"):
        q = ctx % (n, fq(p)) + " Quelle est la probabilité d’obtenir exactement %d pile%s ?" % (k, "s" if k > 1 else "")
    elif ctx.startswith("Un tireur"):
        q = ctx % (fq(p), n) + " Quelle est la probabilité qu’il atteigne la cible exactement %d fois ?" % k
    else:
        q = ctx % (fq(p), n) + " Quelle est la probabilité d’avoir exactement %d ampoule%s défectueuse%s ?" % (k, "s" if k > 1 else "", "s" if k > 1 else "")
    w = [fq(p ** k * (1 - p) ** (n - k)) if comb(n, k) > 1 else fq(1 - v) if v != Fr(1, 2) else fq(p), fq(comb(n, k) * p ** k), fq(Fr(k, n)) if Fr(k, n) != v else fq(p ** n), fq(p ** k) if p ** k != v else fq(v * 2) if v * 2 < 1 else fq(v / 2)]
    w = [x for x in w if x is not None and val(x) is not None and 0 <= val(x)[0] < 1] + [fq(v / 2), fq(p * (1 - p))]
    return M(q, fq(v), w, "Il y a %d chemin%s avec %d succès sur l’arbre ; chacun a la probabilité %s<sup>%d</sup> × %s<sup>%d</sup> : %d × %s = <b>%s</b>." % (comb(n, k), "s" if comb(n, k) > 1 else "", k, fq(p), k, fq(1 - p), n - k, comb(n, k), fq(p ** k * (1 - p) ** (n - k)), fq(v)))


def s5():
    k = R.choice(["au_moins", "au_moins", "deux_ep", "chemins"])
    if k == "au_moins":
        n = R.choice([2, 3, 4])
        p = R.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(1, 5), Fr(1, 10), Fr(2, 5), Fr(1, 6)])
        v = 1 - (1 - p) ** n
        return M("Une expérience réussit avec la probabilité %s. On la répète %d fois de façon indépendante. Quelle est la probabilité d’au moins un succès ?" % (fq(p), n), fq(v),
                 [fq(n * p) if n * p < 1 else fq(p ** n), fq((1 - p) ** n), fq(1 - p ** n), fq(p ** n)],
                 "Contraire : aucun succès, de probabilité %s<sup>%d</sup>. Donc 1 − %s = <b>%s</b>." % (fq(1 - p), n, fq((1 - p) ** n), fq(v)))
    if k == "deux_ep":
        a = Fr(R.randint(1, 5), 6)
        b = Fr(R.randint(1, 3), 4)
        return M("On lance un dé équilibré puis une pièce truquée (indépendants). P(« le dé donne au plus %d ») = %s et P(« pile ») = %s. Probabilité d’avoir les deux ?" % (a * 6, fq(a), fq(b)), fq(a * b),
                 [fq(a + b) if a + b <= 1 else fq(a), fq(a + b - a * b), fq((1 - a) * (1 - b))], "Épreuves indépendantes : on multiplie, %s × %s = <b>%s</b>." % (fq(a), fq(b), fq(a * b)))
    n = R.choice([3, 4])
    kk = R.randint(1, n - 1)
    return M("On répète %d fois une épreuve de Bernoulli. Combien de chemins de l’arbre comportent exactement %d succès ?" % (n, kk), str(comb(n, kk)), [str(kk), str(n), str(2 ** n), str(n * kk)],
             "On compte les façons de placer %d succès parmi %d épreuves : <b>%d</b> chemins." % (kk, n, comb(n, kk)))


def main():
    seen = set()
    sets = [("Probabilités totales avec un arbre", mix(R, seen, [(s1, 20)])), ("Partition en trois événements", mix(R, seen, [(s2, 20)])),
            ("Indépendance de deux événements", mix(R, seen, [(s3, 20)])), ("Répétitions de Bernoulli", mix(R, seen, [(s4, 20)])), ("Épreuves indépendantes", mix(R, seen, [(s5, 20)]))]
    body = L(["Si A<sub>1</sub>, …, A<sub>n</sub> forment une <b>partition</b> de l’univers : P(B) = P(A<sub>1</sub> ∩ B) + … + P(A<sub>n</sub> ∩ B) (formule des probabilités totales). Sur un arbre : on additionne les chemins qui mènent à B.",
              "A et B sont <b>indépendants</b> si P(A ∩ B) = P(A) × P(B) (si P(A) ≠ 0, cela équivaut à P<sub>A</sub>(B) = P(B)).",
              "Lors d’épreuves indépendantes, la probabilité d’une issue (chemin) est le produit des probabilités. Pour k succès en n répétitions de Bernoulli : nombre de chemins × p<sup>k</sup>(1 − p)<sup>n−k</sup>."],
             [("3 lancers, P(succès) = 1/3, exactement 2 succès", ["chemins SSE, SES, ESS : 3", "chacun : (1/3)² × 2/3 = 2/27"], "3 × 2/27 = 2/9")],
             [["P(B) = P<sub>A</sub>(B) + P<sub>Ā</sub>(B)", "On pondère : P(A)P<sub>A</sub>(B) + P(Ā)P<sub>Ā</sub>(B)."], ["Indépendants = incompatibles", "Incompatibles : P(A ∩ B) = 0. Indépendants : P(A ∩ B) = P(A)P(B)."],
              ["2 succès sur 3 : p²(1 − p)", "Il faut multiplier par le nombre de chemins (3)."]])
    faq = [("Comment savoir si deux événements sont indépendants ?", "On calcule P(A) × P(B) et on compare à P(A ∩ B). L’indépendance se démontre par le calcul, ou elle est donnée par le contexte (tirages avec remise, lancers successifs)."),
           ("Pourquoi utiliser l’événement contraire pour « au moins un » ?", "« Au moins un succès » a de nombreux chemins, alors que son contraire « aucun succès » n’en a qu’un : 1 − (1 − p)<sup>n</sup>.")]
    unit("premiere", R, "independance-et-probabilites-totales", "S",
         "Partition de l’univers et formule des probabilités totales ; indépendance de deux événements ; succession de deux épreuves indépendantes ; répétitions d’épreuves de Bernoulli (n ⩽ 4) représentées par un arbre",
         "Indépendance et probabilités totales", "Probabilités totales",
         "Fiches de maths première sur l’indépendance et les probabilités totales : partition, formule des probabilités totales, événements indépendants, épreuves répétées de Bernoulli. 100 exercices corrigés.",
         "Indépendants : P(A ∩ B) = P(A) × P(B)", "P(B) = somme des chemins de l’arbre qui mènent à B", body, faq, sets, 21)


if __name__ == "__main__":
    main()
