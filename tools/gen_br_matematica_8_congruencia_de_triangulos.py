# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Congruência de triângulos (Geometria, EF08MA14)
  python3 tools/gen_br_matematica_8_congruencia_de_triangulos.py
Triângulos congruentes (lados e ângulos correspondentes iguais); casos LLL, LAL, ALA e LAAₒ; por que LLA e AAA não garantem
congruência; usar a congruência para demonstrar propriedades (triângulo isósceles: ângulos da base iguais; diagonais do paralelogramo
se cortam ao meio); achar medidas desconhecidas.
Erros: aceitar LLA ou AAA como caso de congruência, comparar lados que não se correspondem, achar que congruente é só «parecido».
"""
import random
from br_common import lesson, mix
from br_9 import M, bank, formas, tri_pts, unit

R = random.Random(88012)
CASOS = {"LLL": "três lados iguais", "LAL": "dois lados e o ângulo entre eles iguais", "ALA": "dois ângulos e o lado entre eles iguais", "LAAₒ": "um lado, um ângulo adjacente e o ângulo oposto a esse lado iguais"}


def par_tri(marks1, marks2):
    a, b, c = R.choice([(6, 5, 4), (7, 5, 6), (6, 4, 5), (7, 6, 5)])
    sc = 22
    P1 = tri_pts(a, b, c, 20, 150, sc)
    P2 = {k2: (x + a * sc + 50, y) for (k, (x, y)), k2 in zip(sorted(P1.items()), "DEF")}
    s1 = {"pts": P1, "poly": "ABC"}
    s2 = {"pts": P2, "poly": "EFD"}
    s1.update(marks1)
    s2.update(marks2)
    return formas([s1, s2], W=int(2 * a * sc + 110), H=175, label="dois triângulos com marcas de lados e ângulos iguais")


def s1_caso():
    caso = R.choice(["LLL", "LAL", "ALA", "LAAₒ"])
    sides = {"LLL": [("A", "B", "|"), ("B", "C", "||"), ("C", "A", "|||")], "LAL": [("A", "B", "|"), ("B", "C", "||")], "ALA": [("B", "C", "|")], "LAAₒ": [("B", "C", "|")]}[caso]
    angs = {"LLL": [], "LAL": [("B", "A", "C", "•")], "ALA": [("B", "A", "C", "•"), ("C", "B", "A", "••")], "LAAₒ": [("B", "A", "C", "•"), ("A", "B", "C", "••")]}[caso]
    m = {"A": "D", "B": "E", "C": "F"}
    pic = par_tri({"sides": sides, "angles": angs}, {"sides": [(m[p], m[q], t) for p, q, t in sides], "angles": [(m[v], m[x], m[y], t) for v, x, y, t in angs]})
    return M(pic + "As marcas iguais indicam medidas iguais. Por qual caso os triângulos ABC e DEF são congruentes?", caso, [c for c in ["LLL", "LAL", "ALA", "LAAₒ", "AAA"] if c != caso][:3],
             "Os triângulos têm %s: caso <b>%s</b>." % (CASOS[caso], caso))


def s2_texto():
    caso = R.choice(["LLL", "LAL", "ALA", "LAAₒ", "LLA", "AAA"])
    a, b, c = R.randint(3, 9), R.randint(3, 9), R.randint(3, 9)
    x, y = R.choice([(40, 60), (50, 70), (35, 85), (45, 75)])
    txt = {"LLL": "AB = DE = %d cm, BC = EF = %d cm e AC = DF = %d cm" % (a, b, c),
           "LAL": "AB = DE = %d cm, BC = EF = %d cm e o ângulo B = ângulo E = %d°" % (a, b, x),
           "ALA": "ângulo A = ângulo D = %d°, ângulo B = ângulo E = %d° e AB = DE = %d cm" % (x, y, a),
           "LAAₒ": "AB = DE = %d cm, ângulo A = ângulo D = %d° e ângulo C = ângulo F = %d°" % (a, x, y),
           "LLA": "AB = DE = %d cm, BC = EF = %d cm e ângulo A = ângulo D = %d°" % (a, b, x),
           "AAA": "ângulo A = ângulo D = %d°, ângulo B = ângulo E = %d° e ângulo C = ângulo F = %d°" % (x, y, 180 - x - y)}[caso]
    ans = caso if caso in CASOS else "não dá para garantir a congruência"
    return M("Nos triângulos ABC e DEF, %s. O que se pode concluir?" % txt, "são congruentes pelo caso %s" % ans if caso in CASOS else ans,
             ["são congruentes pelo caso %s" % c for c in ["LLL", "LAL", "ALA", "LAAₒ"] if c != caso][:2] + (["não dá para garantir a congruência"] if caso in CASOS else ["são congruentes pelo caso %s" % ("LAL" if caso == "LLA" else "ALA")]),
             ("Caso %s: %s." % (caso, CASOS[caso]) if caso in CASOS else ("Com %s, os triângulos podem ser diferentes" % ("dois lados e um ângulo que não está entre eles" if caso == "LLA" else "só os ângulos iguais, eles podem ter tamanhos diferentes (são semelhantes)"))) + " Resposta: <b>%s</b>." % ("são congruentes pelo caso %s" % ans if caso in CASOS else ans))


def s3_medidas():
    a, b, c = R.randint(3, 12), R.randint(3, 12), R.randint(3, 12)
    if max(a, b, c) * 2 >= a + b + c:
        return None
    x, y = R.choice([(40, 60), (50, 70), (35, 85), (45, 75), (30, 100)])
    k = R.choice(["lado", "ang"])
    if k == "lado":
        return M("Os triângulos ABC e DEF são congruentes, com A ↔ D, B ↔ E, C ↔ F. Se AB = %d cm, BC = %d cm e AC = %d cm, quanto mede EF?" % (a, b, c), "%d cm" % b, ["%d cm" % a, "%d cm" % c, "%d cm" % (a + b + c - b)],
                     "EF corresponde a BC: <b>%d cm</b>." % b)
    return M("Os triângulos ABC e DEF são congruentes, com A ↔ D, B ↔ E, C ↔ F. Se o ângulo A mede %d° e o ângulo B mede %d°, quanto mede o ângulo F?" % (x, y), "%d°" % (180 - x - y), ["%d°" % x, "%d°" % y, "%d°" % (180 - x)],
             "F corresponde a C = 180° − %d° − %d° = <b>%d°</b>." % (x, y, 180 - x - y))


s4_provas = bank(R, [
    ("Num triângulo isósceles ABC (AB = AC), a mediana AM divide-o em dois triângulos congruentes pelo caso…", "LLL", ["AAA", "LLA", "nenhum"]),
    ("Dessa congruência (ABM e ACM), conclui-se que os ângulos da base B e C são…", "iguais", ["suplementares", "retos", "diferentes"]),
    ("Num paralelogramo ABCD, a diagonal AC divide-o em dois triângulos congruentes. Por isso, os lados opostos são…", "iguais", ["perpendiculares", "diferentes", "metade um do outro"]),
    ("A bissetriz do ângulo do vértice de um triângulo isósceles também é…", "mediana e altura", ["lado", "diagonal", "um ângulo raso"]),
    ("Dois triângulos com os três ângulos iguais são sempre…", "semelhantes, mas não necessariamente congruentes", ["congruentes", "retângulos", "isósceles"]),
    ("Triângulos congruentes têm…", "mesma forma e mesmo tamanho", ["só a mesma forma", "só o mesmo perímetro", "só a mesma área"]),
    ("Se dois triângulos são congruentes, seus perímetros são…", "iguais", ["diferentes", "proporcionais com razão 2", "não dá para saber"]),
    ("Qual destes NÃO é caso de congruência?", "LLA", ["LLL", "LAL", "ALA"]),
], "s4_provas")


def main():
    seen = set()
    sets = [
        ("Qual é o caso?", mix(R, seen, [(s1_caso, 16), (s4_provas, 4)])),
        ("Casos de congruência em texto", mix(R, seen, [(s2_texto, 20)])),
        ("Medidas correspondentes", mix(R, seen, [(s3_medidas, 20)])),
        ("Demonstrações", mix(R, seen, [(s4_provas, 4), (s2_texto, 8), (s3_medidas, 8)])),
        ("Revisão", mix(R, seen, [(s2_texto, 10), (s3_medidas, 10)])),
    ]
    body = lesson(
        ["Dois triângulos são <b>congruentes</b> quando têm os lados e os ângulos correspondentes iguais: mesma forma e mesmo tamanho.",
         "Não é preciso conferir tudo. Bastam os casos: <b>LLL</b> (3 lados), <b>LAL</b> (2 lados e o ângulo entre eles), <b>ALA</b> (2 ângulos e o lado entre eles), <b>LAAₒ</b> (lado, ângulo adjacente e ângulo oposto).",
         "LLA e AAA não garantem congruência.",
         "A congruência ajuda a demonstrar propriedades: no isósceles, os ângulos da base são iguais."],
        [("AB = DE, BC = EF, ângulo B = ângulo E", ["o ângulo está entre os lados"], "caso LAL")],
        [["Aceitar LLA ou AAA", "Esses dados não fixam o triângulo."],
         ["Comparar lados que não se correspondem", "Siga a correspondência dos vértices."],
         ["Achar que congruente é «parecido»", "Congruente é igual em tudo; parecido é semelhante."]])
    faq = [("Quais são os casos de congruência de triângulos?", "LLL, LAL, ALA e LAAₒ. Cada um indica dados mínimos que garantem que dois triângulos são iguais em forma e tamanho."),
           ("O que a BNCC pede no 8º ano?", "Demonstrar propriedades de quadriláteros por meio da identificação da congruência de triângulos (EF08MA14).")]
    unit(R, "congruencia-de-triangulos", "G", ["EF08MA14"],
         "Demonstrar propriedades de quadriláteros por meio da identificação da congruência de triângulos",
         "Congruência de triângulos: casos LLL, LAL, ALA e LAAo", "Congruência de triângulos",
         "Atividades de matemática para o 8º ano sobre congruência de triângulos: casos LLL, LAL, ALA e LAAo, por que LLA e AAA não servem, medidas correspondentes e demonstrações. 100 exercícios com gabarito.",
         "LLL, LAL, ALA, LAAo.", "LLA e AAA não garantem congruência.",
         body, faq, sets, 12, grade="8-ano")


if __name__ == "__main__":
    main()
