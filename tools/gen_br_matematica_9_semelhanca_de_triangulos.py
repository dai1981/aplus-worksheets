# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Semelhança de triângulos e teorema de Tales (Geometria, EF09MA12, EF09MA14)
  python3 tools/gen_br_matematica_9_semelhanca_de_triangulos.py
Razão de semelhança; lados correspondentes; perímetros (k) e áreas (k²); casos AA, LAL, LLL; teorema de Tales (feixe de paralelas);
triângulo com paralela a um lado; sombras (altura de prédios e árvores).
Erros: comparar lados que não se correspondem, usar k para áreas (é k²), montar a proporção invertida.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, formas, tri_pts, unit

R = random.Random(89012)
BASE = [(4, 5, 6), (5, 6, 7), (3, 5, 6), (6, 7, 8), (4, 6, 7), (5, 7, 8), (4, 7, 8), (6, 8, 9)]
KS = [F(2), F(3), F(3, 2), F(5, 2), F(4, 3)]


def ren(P, m):
    return {m[k]: v for k, v in P.items()}


def par_tri(a, b, c, k, lab1, lab2):
    big = max(a, b, c) * k
    sc = 170.0 / float(big)
    P1 = tri_pts(a, b, c, 30, 200, sc)
    P2 = ren(tri_pts(float(a * k), float(b * k), float(c * k), 110 + a * sc, 200, sc), {"A": "D", "B": "E", "C": "F"})
    W = int(140 + a * sc + float(a * k) * sc + 20)
    s1 = {"pts": P1, "poly": "ABC", "sides": lab1}
    s2 = {"pts": P2, "poly": "DEF", "sides": lab2}
    return formas([s1, s2], W=max(W, 300), H=235, label="triângulos ABC e DEF semelhantes")


def s1_lado():
    a, b, c = R.choice(BASE)
    k = R.choice(KS)
    if (a * k).denominator != 1 or (b * k).denominator != 1 or (c * k).denominator != 1:
        return None
    L1 = {"BC": a, "CA": b, "AB": c}
    L2 = {"EF": a * k, "FD": b * k, "DE": c * k}
    side2 = R.choice(["EF", "FD", "DE"])
    known = [x for x in ["EF", "FD", "DE"] if x != side2][0]
    corr = {"EF": "BC", "FD": "CA", "DE": "AB"}
    lab1 = [(s[0], s[1], d(L1[s])) for s in ["BC", "CA", "AB"]]
    lab2 = [(known[0], known[1], d(L2[known])), (side2[0], side2[1], "x")]
    pic = par_tri(a, b, c, k, lab1, lab2)
    ans = L2[side2]
    return M(pic + "Os triângulos ABC e DEF são semelhantes (A ↔ D, B ↔ E, C ↔ F), com as medidas em cm. Quanto mede x?", "%s cm" % d(ans),
             ["%s cm" % d(L1[corr[side2]] + L2[known] - L1[corr[known]]), "%s cm" % d(L1[corr[side2]] * F(L1[corr[known]], 1) / L2[known], 1), "%s cm" % d(L2[known]), "%s cm" % d(ans + 1)],
             "Razão de semelhança: %s ÷ %s = %s. Então x = %s · %s = <b>%s cm</b>." % (d(L2[known]), d(L1[corr[known]]), d(k), d(L1[corr[side2]]), d(k), d(ans)))


def s2_razao():
    k = R.choice([2, 3, 4, 5])
    kind = R.choice(["per", "area", "area_inv", "k"])
    if kind == "per":
        p = R.choice([12, 15, 18, 20, 24, 30])
        return M("Dois triângulos são semelhantes com razão %d (o maior é %d vezes o menor). O perímetro do menor é %d cm. Qual é o perímetro do maior?" % (k, k, p), "%d cm" % (p * k), ["%d cm" % (p * k * k), "%d cm" % (p + k), "%s cm" % d(F(p, k), 1)],
                     "Os perímetros têm a mesma razão k: %d · %d = <b>%d cm</b>." % (p, k, p * k))
    if kind == "area":
        A = R.choice([6, 8, 10, 12, 15, 20])
        return M("Dois triângulos são semelhantes com razão %d (o maior é %d vezes o menor). A área do menor é %d cm². Qual é a área do maior?" % (k, k, A), "%d cm²" % (A * k * k), ["%d cm²" % (A * k), "%d cm²" % (A * 2 * k), "%d cm²" % (A + k * k)],
                     "As áreas têm razão k² = %d: %d · %d = <b>%d cm²</b>." % (k * k, A, k * k, A * k * k))
    if kind == "area_inv":
        A = R.choice([5, 6, 7, 8, 9, 10])
        return M("A área de um triângulo é %d vezes a área de outro, semelhante a ele. Qual é a razão de semelhança entre os lados?" % (k * k), d(k), [d(k * k), d(F(k * k, 2), 1), d(k * k * k)],
                 "Se as áreas estão na razão k² = %d, então k = √%d = <b>%d</b>." % (k * k, k * k, k))
    a, ka = R.choice([(4, 12), (5, 15), (6, 9), (8, 20), (10, 25), (6, 15)])
    return M("Um lado de um triângulo mede %d cm, e o lado correspondente de um triângulo semelhante mede %d cm. Qual é a razão de semelhança (maior ÷ menor)?" % (a, ka), d(F(ka, a)), [d(F(a, ka), 2) if (F(a, ka) * 100).denominator == 1 else "%d/%d" % (a, ka), d(ka - a), d(ka + a)],
             "%d ÷ %d = <b>%s</b>." % (ka, a, d(F(ka, a))))


def tales_svg(segs):
    """três paralelas horizontais cortadas por duas transversais; segs: [(texto AB), (BC), (DE), (EF)]"""
    ys = [40, 105, 185]
    x1 = [70, 100, 137]
    x2 = [250, 300, 362]
    P = {"A": (x1[0], ys[0]), "B": (x1[1], ys[1]), "C": (x1[2], ys[2]), "D": (x2[0], ys[0]), "E": (x2[1], ys[1]), "F": (x2[2], ys[2])}
    ex = "".join("<line x1='20' y1='%d' x2='410' y2='%d' stroke='#888' stroke-width='1.6'/>" % (y, y) for y in ys)
    sh = {"pts": P, "segs": [("A", "C"), ("D", "F")], "sides": [("A", "B", segs[0]), ("B", "C", segs[1]), ("D", "E", segs[2]), ("E", "F", segs[3])], "ref": (200, 112)}
    return formas([sh], W=430, H=215, label="feixe de três retas paralelas cortadas por duas transversais", extra=ex)


def s3_tales():
    a, b = R.choice([(2, 3), (3, 4), (4, 6), (3, 5), (5, 8), (6, 9), (4, 5)])
    k = R.choice([F(3, 2), F(2), F(5, 2), F(3), F(4, 3)])
    c, e = a * k, b * k
    if c.denominator != 1 or e.denominator != 1:
        return None
    which = R.choice([1, 2, 3])
    vals = [d(a), d(b), d(c), d(e)]
    ans = [a, b, c, e][which]
    vals[which] = "x"
    pic = tales_svg(vals)
    return M(pic + "As três retas horizontais são paralelas (medidas em cm). Pelo teorema de Tales, quanto mede x?", "%s cm" % d(ans),
             ["%s cm" % d([a, b, c, e][[2, 3, 0, 1][which]]), "%s cm" % d(ans + 1), "%s cm" % d(ans * 2), "%s cm" % d([a, b, c, e][3 - which])],
             "Segmentos correspondentes são proporcionais: AB/BC = DE/EF, isto é, %s/%s = %s/%s. Então <b>x = %s cm</b>." % (d(a), d(b), d(c), d(e), d(ans)))


def s4_paralela():
    ad, db = R.choice([(2, 3), (3, 2), (4, 2), (2, 4), (3, 3), (5, 3), (4, 6)])
    de = R.choice([4, 5, 6, 8, 10])
    bc = F(de * (ad + db), ad)
    if bc.denominator != 1:
        return None
    B, C, A = (40, 190), (330, 190), (150, 25)
    t = F(ad, ad + db)
    D = (A[0] + float(t) * (B[0] - A[0]), A[1] + float(t) * (B[1] - A[1]))
    E = (A[0] + float(t) * (C[0] - A[0]), A[1] + float(t) * (C[1] - A[1]))
    sh = {"pts": {"A": A, "B": B, "C": C, "D": D, "E": E}, "poly": "ABC", "segs": [("D", "E")], "sides": [("A", "D", d(ad)), ("D", "B", d(db)), ("D", "E", d(de)), ("B", "C", "x")], "ref": (190, 120)}
    pic = formas([sh], W=380, H=215, label="triângulo ABC com DE paralelo a BC")
    return M(pic + "No triângulo ABC, DE é paralelo a BC (medidas em cm). Quanto mede x = BC?", "%s cm" % d(bc), ["%s cm" % d(F(de * db, ad), 1), "%s cm" % d(de + db), "%s cm" % d(F(de * ad, ad + db), 1), "%s cm" % d(bc + 2)],
             "Os triângulos ADE e ABC são semelhantes: AD/AB = DE/BC → %d/%d = %d/x → <b>x = %s cm</b>." % (ad, ad + db, de, d(bc)))


def s5_sombra():
    k = R.choice(["pred", "arv", "poste"])
    p, sp = R.choice([(F(2), F(3, 2)), (F(18, 10), F(12, 10)), (F(1), F(1, 2)), (F(15, 10), F(2)), (F(16, 10), F(8, 10))])
    S = R.choice([6, 8, 9, 10, 12, 15, 18, 24])
    h = p * S / sp
    if (h * 10).denominator != 1:
        return None
    obj = {"pred": "um prédio", "arv": "uma árvore", "poste": "um poste"}[k]
    who = R.choice(["uma vara de %s m" % d(p), "uma pessoa de %s m de altura" % d(p)]) if p >= F(3, 2) else "uma vara de %s m" % d(p)
    return M("No mesmo momento, %s faz uma sombra de %s m e %s faz uma sombra de %d m. Qual é a altura %s?" % (who, d(sp), obj, S, {"pred": "do prédio", "arv": "da árvore", "poste": "do poste"}[k]),
             "%s m" % d(h), ["%s m" % d(sp * S / p, 1), "%s m" % d(S + p - sp), "%s m" % d(S * p), "%s m" % d(h + 2)],
             "Os raios de sol formam triângulos semelhantes: altura/sombra é igual. %s/%s = h/%d → <b>h = %s m</b>." % (d(p), d(sp), S, d(h)))


def s6_casos():
    q, a, w = R.choice([
        ("Dois triângulos têm dois ângulos iguais (40° e 75°). Eles são…", "semelhantes (caso AA)", ["congruentes sempre", "não semelhantes", "semelhantes só se os lados forem iguais"]),
        ("Os lados de um triângulo medem 3, 4 e 5 cm; os de outro, 6, 8 e 10 cm. Eles são…", "semelhantes (caso LLL), com razão 2", ["congruentes", "não semelhantes", "semelhantes com razão 3"]),
        ("Os lados de um triângulo medem 4, 6 e 7 cm; os de outro, 8, 12 e 15 cm. Eles são…", "não semelhantes", ["semelhantes com razão 2", "congruentes", "semelhantes com razão 3"]),
        ("Dois triângulos têm um ângulo igual e os lados que o formam proporcionais. Pelo caso LAL, eles são…", "semelhantes", ["congruentes sempre", "retângulos", "não semelhantes"]),
        ("Dois triângulos semelhantes têm…", "ângulos iguais e lados proporcionais", ["lados iguais e ângulos proporcionais", "a mesma área", "o mesmo perímetro"]),
        ("Todo triângulo equilátero é semelhante a…", "qualquer outro triângulo equilátero", ["qualquer triângulo isósceles", "qualquer triângulo retângulo", "nenhum outro triângulo"]),
        ("Dois triângulos semelhantes têm razão de semelhança 1. Eles são…", "congruentes", ["diferentes", "retângulos", "equiláteros"]),
        ("Um triângulo tem ângulos de 50° e 60°; outro, de 60° e 70°. Eles são…", "semelhantes, pois o terceiro ângulo do primeiro é 70°", ["não semelhantes", "congruentes", "semelhantes só se forem retângulos"]),
        ("Um triângulo tem ângulos de 30° e 80°; outro, de 30° e 60°. Eles são…", "não semelhantes", ["semelhantes (caso AA)", "congruentes", "semelhantes com razão 2"]),
        ("Uma reta paralela a um lado de um triângulo corta os outros dois lados. O triângulo menor formado é…", "semelhante ao triângulo original", ["congruente ao original", "sempre retângulo", "sem relação com o original"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Lados correspondentes", mix(R, seen, [(s1_lado, 20)])),
        ("Razão de semelhança, perímetro e área", mix(R, seen, [(s2_razao, 14), (s6_casos, 6)])),
        ("Teorema de Tales", mix(R, seen, [(s3_tales, 20)])),
        ("Paralela a um lado do triângulo", mix(R, seen, [(s4_paralela, 16), (s6_casos, 4)])),
        ("Sombras e alturas", mix(R, seen, [(s5_sombra, 20)])),
    ]
    body = lesson(
        ["Dois triângulos são <b>semelhantes</b> quando têm os ângulos iguais e os lados correspondentes proporcionais.",
         "A <b>razão de semelhança</b> k é a divisão de um lado do maior pelo lado correspondente do menor. Os perímetros também estão na razão k; as áreas, na razão <b>k²</b>.",
         "Basta verificar dois ângulos iguais (caso AA), os três lados proporcionais (LLL) ou dois lados proporcionais com o ângulo entre eles igual (LAL).",
         "<b>Teorema de Tales:</b> retas paralelas cortadas por duas transversais formam segmentos proporcionais."],
        [("Triângulo de lados 4, 5, 6 e outro semelhante com lado 8 no lugar de 4", ["k = 8 ÷ 4 = 2"], "os outros lados medem 10 e 12"),
         ("Vara de 2 m com sombra de 1,5 m; prédio com sombra de 12 m", ["2/1,5 = h/12"], "h = 16 m")],
        [["Comparar lados que não se correspondem", "Siga a correspondência dos vértices: A ↔ D, B ↔ E."],
         ["Usar k para as áreas", "As áreas estão na razão k²."],
         ["Montar a proporção invertida", "Escreva maior/menor dos dois lados ou menor/maior dos dois."]])
    faq = [("Como saber se dois triângulos são semelhantes?", "Verifique se dois ângulos são iguais (AA), se os três lados são proporcionais (LLL) ou se dois lados são proporcionais e o ângulo entre eles é igual (LAL)."),
           ("O que diz o teorema de Tales?", "Se um feixe de retas paralelas é cortado por duas transversais, os segmentos formados numa transversal são proporcionais aos segmentos correspondentes na outra.")]
    unit(R, "semelhanca-de-triangulos", "G", ["EF09MA12", "EF09MA14"],
         "Reconhecer as condições necessárias e suficientes para que dois triângulos sejam semelhantes; resolver e elaborar problemas de aplicação do teorema de Tales e de semelhança de triângulos",
         "Semelhança de triângulos e teorema de Tales", "Semelhança de triângulos",
         "Atividades de matemática para o 9º ano sobre semelhança de triângulos: razão de semelhança, lados correspondentes, perímetro e área, casos AA, LLL e LAL, teorema de Tales e sombras. 100 exercícios com gabarito.",
         "Ângulos iguais, lados proporcionais.", "Perímetros na razão k; áreas na razão k².",
         body, faq, sets, 12)


if __name__ == "__main__":
    main()
