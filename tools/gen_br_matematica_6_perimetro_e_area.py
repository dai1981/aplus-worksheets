# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Perímetro, área e plantas baixas (Grandezas e medidas, EF06MA28, EF06MA29)
  python3 tools/gen_br_matematica_6_perimetro_e_area.py
Perímetro e área de retângulos, quadrados e triângulos retângulos; figuras compostas (plantas baixas de casas e salas);
o que acontece com o perímetro e a área quando o lado do quadrado dobra ou triplica (o perímetro é proporcional ao lado, a área não);
unidades cm², m² e conversão; quantidade de piso, tinta e rodapé.
Usa geradores do 5º ano (malha, mesma área, figura composta) com outro sorteio.
Erros: somar só dois lados no perímetro, achar que a área dobra quando o lado dobra, confundir perímetro (rodapé) com área (piso).
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use, reais
from br_9 import M, d, bank, formas, unit

R = random.Random(86019)
a_malha, a_mesma, a_comp = use("gen_br_matematica_5_perimetro_e_area", 86919, "s1_malha", "s3_mesma_area", "s4_composta")


def s1_formula():
    k = R.choice(["ret", "quad", "tri"])
    if k == "ret":
        a, b = R.randint(3, 25), R.randint(2, 15)
        if a == b:
            return None
        q = R.choice(["perímetro", "área"])
        ans = 2 * (a + b) if q == "perímetro" else a * b
        u = "cm" if q == "perímetro" else "cm²"
        return M("Um retângulo tem %d cm de comprimento e %d cm de largura. Qual é a %s?" % (a, b, q), "%d %s" % (ans, u), ["%d %s" % (a * b if q == "perímetro" else 2 * (a + b), "cm" if q == "perímetro" else "cm²"), "%d %s" % (a + b, u), "%d %s" % (ans + a, u)],
                 "%s = <b>%d %s</b>." % ("2 × (%d + %d)" % (a, b) if q == "perímetro" else "%d × %d" % (a, b), ans, u))
    if k == "quad":
        L = R.randint(3, 20)
        return M("Um quadrado tem lado %d m. Qual é a área?" % L, "%d m²" % (L * L), ["%d m²" % (4 * L), "%d m²" % (2 * L), "%d m²" % (L * L + L)], "%d × %d = <b>%d m²</b>." % (L, L, L * L))
    a, b = R.randint(3, 20), R.randint(2, 16)
    A = F(a * b, 2)
    return M("Um triângulo retângulo tem catetos (os lados do ângulo reto) de %d cm e %d cm. Qual é a área?" % (a, b), "%s cm²" % d(A), ["%d cm²" % (a * b), "%d cm²" % (a + b), "%s cm²" % d(A + a)], "A área é metade do retângulo %d × %d: %d ÷ 2 = <b>%s cm²</b>." % (a, b, a * b, d(A)))


def s2_variacao():
    L = R.randint(2, 12)
    k = R.choice([2, 3, 4])
    q = R.choice(["perímetro", "área"])
    nome = {2: "dobra", 3: "triplica", 4: "quadruplica"}[k]
    if q == "perímetro":
        return M("O lado de um quadrado de %d cm %s. O que acontece com o perímetro?" % (L, nome), "fica %d vezes maior" % k, ["fica %d vezes maior" % (k * k), "não muda", "aumenta %d cm" % k],
                 "Perímetro: %d → %d. Ele é proporcional ao lado: <b>fica %d vezes maior</b>." % (4 * L, 4 * L * k, k))
    return M("O lado de um quadrado de %d cm %s. O que acontece com a área?" % (L, nome), "fica %d vezes maior" % (k * k), ["fica %d vezes maior" % k, "não muda", "aumenta %d cm²" % k],
             "Área: %d → %d cm². Ela <b>fica %d vezes maior</b> (%d × %d): não é proporcional ao lado." % (L * L, L * L * k * k, k * k, k, k))


def planta():
    a, b = R.randint(6, 12), R.randint(5, 10)
    c, e = R.randint(2, a - 3), R.randint(2, b - 2)
    sc = 16
    x0, y0 = 60, 30
    P = {"A": (x0, y0), "B": (x0 + a * sc, y0), "C": (x0 + a * sc, y0 + e * sc), "D": (x0 + c * sc, y0 + e * sc), "E": (x0 + c * sc, y0 + b * sc), "F": (x0, y0 + b * sc)}
    sh = {"pts": {k: v for k, v in P.items()}, "poly": "ABCDEF", "sides": [("A", "B", "%d m" % a), ("B", "C", "%d m" % e), ("E", "F", "%d m" % c), ("F", "A", "%d m" % b)], "fill": "#f3eee2"}
    svg = formas([sh], W=a * sc + 130, H=b * sc + 64, label="planta baixa de uma sala em forma de L")
    svg = svg.replace(">A<", "><").replace(">B<", "><").replace(">C<", "><").replace(">D<", "><").replace(">E<", "><").replace(">F<", "><")
    area = a * e + c * (b - e)
    per = 2 * (a + b)
    return svg, area, per, (a, b, c, e)


def s3_planta():
    svg, area, per, (a, b, c, e) = planta()
    k = R.choice(["area", "per", "piso"])
    if k == "area":
        return M(svg + "A planta mostra uma sala em forma de L. Qual é a área da sala?", "%d m²" % area, ["%d m²" % (a * b), "%d m²" % per, "%d m²" % (area + c)],
                 "Divida em dois retângulos: %d × %d + %d × %d = <b>%d m²</b>." % (a, e, c, b - e, area))
    if k == "per":
        return M(svg + "Quantos metros de rodapé são necessários para contornar toda a sala (sem descontar portas)?", "%d m" % per, ["%d m" % area, "%d m" % (a + b + c + e), "%d m" % (per - 2)],
                 "Os lados que faltam medem %d − %d = %d m e %d − %d = %d m; somando todos: <b>%d m</b>." % (a, c, a - c, b, e, b - e, per))
    p = R.choice([35, 40, 45, 50, 60])
    return M(svg + "O piso custa %s por m². Quanto custa o piso para toda a sala?" % reais(p * 100), reais(area * p * 100), [reais(per * p * 100), reais(a * b * p * 100), reais((area + p) * 100)],
             "Área %d m² × %s = <b>%s</b>." % (area, reais(p * 100), reais(area * p * 100)))


s4_conceitos = bank(R, [
    ("Para saber quanto de rodapé comprar, calculamos o…", "perímetro", ["área", "volume", "ângulo"]),
    ("Para saber quanto de piso comprar, calculamos a…", "área", ["perímetro", "altura", "diagonal"]),
    ("1 m² equivale a quantos cm²?", "10.000", ["100", "1.000", "10"]),
    ("Dois retângulos de mesma área sempre têm o mesmo perímetro?", "não", ["sim", "só se forem quadrados", "só se forem grandes"]),
    ("Entre os retângulos de perímetro 20 cm, o de maior área é…", "o quadrado de lado 5 cm", ["o de lados 9 cm e 1 cm", "o de lados 8 cm e 2 cm", "todos têm a mesma área"]),
    ("O perímetro de um quadrado é proporcional ao lado. A área também é?", "não, a área cresce com o quadrado do lado", ["sim, sempre", "sim, se o lado for inteiro", "não, a área não muda"]),
    ("Um terreno de 12 m por 30 m tem área de…", "360 m²", ["84 m²", "42 m²", "3.600 m²"]),
    ("Numa planta na escala 1 : 100, um quarto mede 4 cm por 3 cm. A área real é…", "12 m²", ["12 cm²", "7 m²", "1.200 m²"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Perímetro e área na malha", mix(R, seen, [(a_malha, 12), (a_mesma, 8)])),
        ("Fórmulas de perímetro e área", mix(R, seen, [(s1_formula, 20)])),
        ("Plantas baixas", mix(R, seen, [(s3_planta, 16), (a_comp, 4)])),
        ("Quando o lado aumenta", mix(R, seen, [(s2_variacao, 12), (s4_conceitos, 8)])),
        ("Problemas", mix(R, seen, [(s3_planta, 10), (s1_formula, 10)])),
    ]
    body = lesson(
        ["<b>Perímetro</b> é o contorno: some todos os lados. <b>Área</b> é a superfície: retângulo = comprimento × largura; triângulo retângulo = metade do retângulo.",
         "Numa <b>planta baixa</b>, divida a figura em retângulos para calcular a área e descubra as medidas que faltam antes de somar o perímetro.",
         "Se o lado do quadrado dobra, o perímetro dobra (é proporcional), mas a área fica 4 vezes maior."],
        [("Sala em L: 8 m × 3 m e 4 m × 2 m", ["24 + 8"], "32 m²"),
         ("Quadrado de lado 3 → lado 6", ["perímetro 12 → 24", "área 9 → 36"], "perímetro × 2; área × 4")],
        [["Somar só dois lados", "O perímetro passa pelos quatro lados."],
         ["Achar que a área dobra", "Com lado × 2, área × 4."],
         ["Trocar rodapé por piso", "Rodapé: perímetro. Piso: área."]],
        planta()[0])
    faq = [("Qual é a diferença entre perímetro e área?", "O perímetro é a medida do contorno (em cm, m). A área é a medida da superfície (em cm², m²). Rodapé e cerca usam perímetro; piso e pintura usam área."),
           ("O que a BNCC pede no 6º ano?", "Interpretar, descrever e desenhar plantas baixas simples de residências e vistas aéreas (EF06MA28) e analisar e descrever mudanças que ocorrem no perímetro e na área de um quadrado ao se ampliarem ou reduzirem as medidas de seus lados (EF06MA29).")]
    unit(R, "perimetro-e-area", "M", ["EF06MA28", "EF06MA29"],
         "Interpretar, descrever e desenhar plantas baixas simples de residências e vistas aéreas; analisar e descrever mudanças que ocorrem no perímetro e na área de um quadrado ao se ampliarem ou reduzirem, igualmente, as medidas de seus lados, para compreender que o perímetro é proporcional à medida do lado, o que não ocorre com a área",
         "Perímetro, área e plantas baixas", "Perímetro e área",
         "Atividades de matemática para o 6º ano sobre perímetro e área: retângulos, quadrados e triângulos retângulos, plantas baixas, piso e rodapé e o que muda quando o lado do quadrado aumenta. 100 exercícios com gabarito.",
         "Perímetro: contorno. Área: superfície.", "Lado × 2 → perímetro × 2, área × 4.",
         body, faq, sets, 19, grade="6-ano")


if __name__ == "__main__":
    main()
