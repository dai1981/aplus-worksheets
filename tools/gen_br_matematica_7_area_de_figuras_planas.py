# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Área de figuras planas (Grandezas e medidas, EF07MA31, EF07MA32)
  python3 tools/gen_br_matematica_7_area_de_figuras_planas.py
Área do retângulo, paralelogramo (base × altura), triângulo (base × altura ÷ 2), trapézio ((B + b) × h ÷ 2) e losango (D × d ÷ 2),
obtidas por decomposição; figuras compostas; equivalência de áreas; problemas (terrenos, telhados, pisos).
Erros: usar o lado inclinado como altura, esquecer de dividir por 2 no triângulo, somar as bases do trapézio sem dividir.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, bank, formas, unit, _ln, RED

R = random.Random(87016)


def fig(kind, b, h, extra=None):
    sc = min(200.0 / max(b + (extra or 0), 1), 120.0 / h)
    x0, y0 = 50, 160
    H = h * sc
    if kind == "par":
        off = R.choice([2, 3]) * sc
        P = {"A": (x0, y0), "B": (x0 + b * sc, y0), "C": (x0 + b * sc + off, y0 - H), "D": (x0 + off, y0 - H)}
        sh = {"pts": P, "poly": "ABCD", "sides": [("A", "B", "%d cm" % b)]}
        hx = x0 + off
    elif kind == "tri":
        t = R.uniform(0.25, 0.75) * b * sc
        P = {"A": (x0, y0), "B": (x0 + b * sc, y0), "C": (x0 + t, y0 - H)}
        sh = {"pts": P, "poly": "ABC", "sides": [("A", "B", "%d cm" % b)]}
        hx = x0 + t
    else:
        bb = extra
        off = (b - bb) / 2.0 * sc
        P = {"A": (x0, y0), "B": (x0 + b * sc, y0), "C": (x0 + off + bb * sc, y0 - H), "D": (x0 + off, y0 - H)}
        sh = {"pts": P, "poly": "ABCD", "sides": [("A", "B", "%d cm" % b), ("D", "C", "%d cm" % bb)]}
        hx = x0 + off + bb * sc / 2
    ex = "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8' stroke-dasharray='5 4'/>" % (hx, y0, hx, y0 - H, RED)
    ex += "<text x='%.1f' y='%.1f' font-size='14' fill='%s' font-weight='700' font-family='sans-serif'>%d cm</text>" % (hx + 5, y0 - H / 2 + 5, RED, h)
    svg = formas([sh], W=int(x0 + (b + (2 if kind == "par" else 0)) * sc + 70), H=190, label="figura com base e altura", extra=ex)
    for k in "ABCD":
        svg = svg.replace(">%s<" % k, "><")
    return svg


def s1_formulas():
    k = R.choice(["par", "tri", "tra"])
    b, h = R.randint(4, 16), R.randint(3, 10)
    if k == "par":
        return M(fig("par", b, h) + "Qual é a área deste paralelogramo? (A linha tracejada é a altura.)", "%d cm²" % (b * h), ["%s cm²" % d(F(b * h, 2)), "%d cm²" % (2 * (b + h)), "%d cm²" % (b * h + b)],
                 "Paralelogramo: base × altura = %d × %d = <b>%d cm²</b>." % (b, h, b * h))
    if k == "tri":
        return M(fig("tri", b, h) + "Qual é a área deste triângulo? (A linha tracejada é a altura.)", "%s cm²" % d(F(b * h, 2)), ["%d cm²" % (b * h), "%d cm²" % (b + h), "%s cm²" % d(F(b * h, 4))],
                 "Triângulo: base × altura ÷ 2 = %d × %d ÷ 2 = <b>%s cm²</b>." % (b, h, d(F(b * h, 2))))
    bb = R.randint(2, b - 1) if b > 3 else 2
    A = F((b + bb) * h, 2)
    return M(fig("tra", b, h, bb) + "Qual é a área deste trapézio? (A linha tracejada é a altura.)", "%s cm²" % d(A), ["%d cm²" % ((b + bb) * h), "%d cm²" % (b * h), "%d cm²" % (b * bb)],
             "Trapézio: (B + b) × h ÷ 2 = (%d + %d) × %d ÷ 2 = <b>%s cm²</b>." % (b, bb, h, d(A)))


def s2_texto():
    k = R.choice(["los", "tri", "par", "tra", "inv"])
    if k == "los":
        D, dd = R.randint(4, 20), R.randint(2, 14)
        if D == dd:
            return None
        return M("As diagonais de um losango medem %d cm e %d cm. Qual é a área?" % (D, dd), "%s cm²" % d(F(D * dd, 2)), ["%d cm²" % (D * dd), "%d cm²" % (2 * (D + dd)), "%s cm²" % d(F(D * dd, 4))], "D × d ÷ 2 = <b>%s cm²</b>." % d(F(D * dd, 2)))
    if k == "inv":
        b, h = R.randint(4, 20), R.randint(3, 12)
        A = b * h
        if A % 2:
            return None
        return M("Um triângulo tem área de %d cm² e base de %d cm. Qual é a altura?" % (A // 2, b), "%d cm" % h, ["%s cm" % d(F(A // 2, b), 1) if (F(A // 2, b) * 10).denominator == 1 else "%d cm" % (h + 1), "%d cm" % (A // 2 - b), "%d cm" % (2 * h)],
                 "b × h ÷ 2 = %d → %d × h = %d → <b>h = %d cm</b>." % (A // 2, b, A, h))
    b, h = R.randint(3, 25), R.randint(2, 15)
    if k == "tri":
        return M("Um triângulo tem base de %d m e altura de %d m. Qual é a área?" % (b, h), "%s m²" % d(F(b * h, 2)), ["%d m²" % (b * h), "%d m²" % (b + h), "%s m²" % d(F(b + h, 2))], "%d × %d ÷ 2 = <b>%s m²</b>." % (b, h, d(F(b * h, 2))))
    if k == "par":
        return M("Um paralelogramo tem base de %d m e altura de %d m. Qual é a área?" % (b, h), "%d m²" % (b * h), ["%s m²" % d(F(b * h, 2)), "%d m²" % (2 * (b + h)), "%d m²" % (b * h + h)], "%d × %d = <b>%d m²</b>." % (b, h, b * h))
    bb = R.randint(1, b - 1) if b > 2 else 1
    return M("Um trapézio tem bases de %d m e %d m e altura de %d m. Qual é a área?" % (b, bb, h), "%s m²" % d(F((b + bb) * h, 2)), ["%d m²" % ((b + bb) * h), "%d m²" % (b * bb * h), "%s m²" % d(F((b - bb) * h, 2))],
             "(%d + %d) × %d ÷ 2 = <b>%s m²</b>." % (b, bb, h, d(F((b + bb) * h, 2))))


def s3_problemas():
    k = R.choice(["terreno", "jardim", "telhado", "bandeira"])
    if k == "terreno":
        b, bb, h = R.randint(20, 40), R.randint(10, 19), R.randint(10, 30)
        A = F((b + bb) * h, 2)
        p = R.choice([200, 300, 500])
        return M("Um terreno tem forma de trapézio com bases %d m e %d m e altura %d m. Custa %s o m². Qual é o preço?" % (b, bb, h, reais(p * 100)), reais(int(A * p) * 100), [reais(int((b + bb) * h * p) * 100), reais(int(A) * 100), reais(int(b * h * p) * 100)],
                 "Área = (%d + %d) × %d ÷ 2 = %s m²; × %s = <b>%s</b>." % (b, bb, h, d(A), reais(p * 100), reais(int(A * p) * 100)))
    if k == "jardim":
        L, b, h = R.randint(8, 15), R.randint(2, 6), R.randint(2, 6)
        A = L * L - F(b * h, 2)
        return M("Um quintal quadrado de lado %d m tem, num canto, um canteiro triangular de base %d m e altura %d m. Qual é a área do quintal fora do canteiro?" % (L, b, h), "%s m²" % d(A), ["%s m²" % d(L * L - b * h), "%d m²" % (L * L), "%s m²" % d(4 * L - F(b * h, 2))],
                 "%d² − %d × %d ÷ 2 = %d − %s = <b>%s m²</b>." % (L, b, h, L * L, d(F(b * h, 2)), d(A)))
    if k == "telhado":
        b, h, n = R.randint(6, 12), R.randint(3, 6), R.choice([2, 4])
        A = F(b * h, 2) * n
        return M("Um telhado tem %d partes iguais em forma de triângulo, cada uma com base %d m e altura %d m. Qual é a área total do telhado?" % (n, b, h), "%s m²" % d(A), ["%d m²" % (b * h * n), "%s m²" % d(F(b * h, 2)), "%d m²" % ((b + h) * n)],
                 "%d × (%d × %d ÷ 2) = <b>%s m²</b>." % (n, b, h, d(A)))
    c, l = R.randint(8, 20), R.randint(6, 14)
    return M("Uma bandeira retangular de %d dm por %d dm tem um losango no meio, com diagonais iguais aos lados da bandeira. Qual é a área do losango?" % (c, l), "%s dm²" % d(F(c * l, 2)), ["%d dm²" % (c * l), "%s dm²" % d(F(c * l, 4)), "%d dm²" % (2 * (c + l))],
             "Losango: D × d ÷ 2 = %d × %d ÷ 2 = <b>%s dm²</b> (metade do retângulo)." % (c, l, d(F(c * l, 2))))


s4_conceitos = bank(R, [
    ("A área do triângulo é a metade da área de…", "um paralelogramo de mesma base e altura", ["um quadrado de lado igual à base", "um círculo", "um trapézio qualquer"]),
    ("Na área do paralelogramo, a altura é…", "a distância perpendicular entre as bases", ["o lado inclinado", "a diagonal maior", "a soma dos lados"]),
    ("Dois triângulos com a mesma base e a mesma altura têm…", "a mesma área", ["o mesmo perímetro sempre", "a mesma forma", "áreas diferentes"]),
    ("Cortando um trapézio por uma diagonal, obtemos…", "dois triângulos", ["dois retângulos", "um quadrado e um triângulo", "dois trapézios"]),
    ("A área de um losango é a metade de…", "o produto das diagonais", ["a soma das diagonais", "o quadrado do lado", "o perímetro"]),
    ("Se dobrarmos só a altura de um triângulo, a área…", "dobra", ["quadruplica", "não muda", "cai pela metade"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Paralelogramo, triângulo e trapézio", mix(R, seen, [(s1_formulas, 20)])),
        ("Usar as fórmulas", mix(R, seen, [(s2_texto, 20)])),
        ("Figuras com altura marcada", mix(R, seen, [(s1_formulas, 14), (s4_conceitos, 6)])),
        ("Problemas", mix(R, seen, [(s3_problemas, 20)])),
        ("Revisão", mix(R, seen, [(s2_texto, 10), (s3_problemas, 10)])),
    ]
    body = lesson(
        ["<b>Paralelogramo</b>: corte um triângulo de um lado e encaixe do outro: vira um retângulo. Área = base × altura.",
         "<b>Triângulo</b>: é metade de um paralelogramo. Área = base × altura ÷ 2.",
         "<b>Trapézio</b>: dois trapézios iguais formam um paralelogramo de base B + b. Área = (B + b) × h ÷ 2. <b>Losango</b>: D × d ÷ 2.",
         "A altura é sempre perpendicular à base, não o lado inclinado."],
        [("Triângulo de base 10 e altura 6", ["10 × 6 ÷ 2"], "30"),
         ("Trapézio com bases 8 e 4, altura 5", ["(8 + 4) × 5 ÷ 2"], "30")],
        [["Usar o lado inclinado como altura", "A altura forma ângulo reto com a base."],
         ["Esquecer o ÷ 2 no triângulo", "O triângulo é metade do paralelogramo."],
         ["Não dividir por 2 no trapézio", "(B + b) × h ÷ 2."]],
        fig("tri", 10, 6))
    faq = [("Como calcular a área de um trapézio?", "Some a base maior com a base menor, multiplique pela altura e divida por 2: A = (B + b) × h ÷ 2."),
           ("O que a BNCC pede no 7º ano?", "Estabelecer expressões de cálculo de área de triângulos e de quadriláteros (EF07MA31) e resolver e elaborar problemas de cálculo de medida de área de figuras planas que podem ser decompostas por quadrados, retângulos e/ou triângulos (EF07MA32).")]
    unit(R, "area-de-figuras-planas", "M", ["EF07MA31", "EF07MA32"],
         "Estabelecer expressões de cálculo de área de triângulos e de quadriláteros; resolver e elaborar problemas de cálculo de medida de área de figuras planas que podem ser decompostas por quadrados, retângulos e/ou triângulos, utilizando a equivalência entre áreas",
         "Área de triângulos e quadriláteros", "Área de figuras planas",
         "Atividades de matemática para o 7º ano sobre área de figuras planas: paralelogramo, triângulo, trapézio e losango, altura, figuras compostas e problemas com terrenos e telhados. 100 exercícios com gabarito.",
         "Triângulo: base × altura ÷ 2.", "Trapézio: (B + b) × h ÷ 2.",
         body, faq, sets, 16, grade="7-ano")


if __name__ == "__main__":
    main()
