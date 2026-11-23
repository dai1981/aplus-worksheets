# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Polígonos e seus ângulos (Geometria, EF07MA27, EF07MA28)
  python3 tools/gen_br_matematica_7_poligonos_e_angulos_internos.py
Soma dos ângulos internos (n − 2) · 180° pela decomposição em triângulos; ângulo que falta num polígono; ângulo interno e externo
de polígonos regulares; quantos lados tem o polígono; algoritmo (fluxograma) para construir polígonos regulares; ladrilhamento.
Usa geradores do 9º ano (polígonos regulares) com outro sorteio.
Erros: usar n · 180°, esquecer de dividir por n no polígono regular, confundir ângulo interno e externo.
"""
import random
from br_common import lesson, mix, use
from br_9 import M, d, unit

R = random.Random(87014)
r_ang, r_inv, r_cons = use("gen_br_matematica_9_poligonos_regulares", 87914, "s1_angulos", "s2_inverso", "s3_construcao")
NOMES = {4: "quadrilátero", 5: "pentágono", 6: "hexágono", 7: "heptágono", 8: "octógono", 9: "eneágono", 10: "decágono", 12: "dodecágono"}


def s1_soma():
    n = R.choice(sorted(NOMES))
    k = R.choice(["soma", "tri"])
    if k == "tri":
        return M("Traçando todas as diagonais a partir de um só vértice, em quantos triângulos fica dividido um %s?" % NOMES[n], str(n - 2), [str(n), str(n - 1), str(n - 3)],
                 "Um polígono de n lados fica dividido em n − 2 triângulos: <b>%d</b>." % (n - 2))
    S = (n - 2) * 180
    return M("Qual é a soma dos ângulos internos de um %s?" % NOMES[n], "%s°" % d(S), ["%s°" % d(n * 180), "%d°" % 360, "%s°" % d((n - 1) * 180)],
             "(%d − 2) × 180° = <b>%s°</b>." % (n, d(S)))


def s2_falta():
    n = R.choice([4, 5, 6])
    S = (n - 2) * 180
    angs = [R.randint(70, 150) for _ in range(n - 1)]
    x = S - sum(angs)
    if not 30 <= x <= 170:
        return None
    return M("Um %s tem %s ângulos medindo %s. Quanto mede o ângulo que falta?" % (NOMES[n], {3: "três", 4: "quatro", 5: "cinco"}[n - 1], ", ".join("%d°" % a for a in angs)), "%d°" % x, ["%d°" % (360 - sum(angs)) if 0 < 360 - sum(angs) else "%d°" % (x + 30), "%d°" % (x + 180), "%d°" % (x - 20)],
             "Soma total: %s°; %s − %d = <b>%d°</b>." % (d(S), d(S), sum(angs), x))


def main():
    seen = set()
    sets = [
        ("Soma dos ângulos internos", mix(R, seen, [(s1_soma, 16)] + [(r_ang, 4)])),
        ("O ângulo que falta", mix(R, seen, [(s2_falta, 20)])),
        ("Polígonos regulares", mix(R, seen, [(r_ang, 20)])),
        ("Quantos lados?", mix(R, seen, [(r_inv, 14), (s2_falta, 6)])),
        ("Construções e algoritmos", mix(R, seen, [(r_cons, 20)])),
    ]
    body = lesson(
        ["Traçando as diagonais a partir de um vértice, um polígono de n lados fica dividido em n − 2 triângulos. Por isso a <b>soma dos ângulos internos</b> é (n − 2) · 180°.",
         "Num <b>polígono regular</b>, todos os ângulos são iguais: ângulo interno = (n − 2) · 180° ÷ n. O ângulo externo é 360° ÷ n.",
         "Para construir um polígono regular, divida a circunferência em n arcos iguais (360° ÷ n) e ligue os pontos."],
        [("Hexágono", ["(6 − 2) · 180 = 720"], "soma 720°; regular: 120° cada"),
         ("Pentágono com ângulos 100°, 110°, 90°, 120°", ["540 − 420"], "o quinto mede 120°")],
        [["Usar n · 180°", "São n − 2 triângulos."],
         ["Não dividir por n", "A soma é de todos os ângulos; cada um é a soma ÷ n."],
         ["Confundir interno e externo", "Interno + externo = 180°."]])
    faq = [("Por que a soma dos ângulos internos é (n − 2) · 180°?", "Porque, traçando as diagonais de um único vértice, o polígono fica dividido em n − 2 triângulos, e cada triângulo tem 180°."),
           ("O que a BNCC pede no 7º ano?", "Calcular medidas de ângulos internos de polígonos regulares, sem o uso de fórmulas, e estabelecer relações entre ângulos internos e externos de polígonos (EF07MA27) e descrever um algoritmo para a construção de um polígono regular (EF07MA28).")]
    unit(R, "poligonos-e-angulos-internos", "G", ["EF07MA27", "EF07MA28"],
         "Calcular medidas de ângulos internos de polígonos regulares, sem o uso de fórmulas, e estabelecer relações entre ângulos internos e externos de polígonos, preferencialmente vinculadas à construção de mosaicos e de ladrilhamentos; descrever, por escrito e por meio de um fluxograma, um algoritmo para a construção de um polígono regular (como quadrado e triângulo equilátero), conhecida a medida de seu lado",
         "Polígonos: soma dos ângulos internos e polígonos regulares", "Ângulos dos polígonos",
         "Atividades de matemática para o 7º ano sobre polígonos: soma dos ângulos internos, ângulo que falta, ângulo interno e externo de polígonos regulares, número de lados e construções. 100 exercícios com gabarito.",
         "Soma dos ângulos internos = (n − 2) · 180°", "Ângulo externo do regular = 360° ÷ n",
         body, faq, sets, 14, grade="7-ano")


if __name__ == "__main__":
    main()
