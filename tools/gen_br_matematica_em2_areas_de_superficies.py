# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Áreas de superfícies planas (EM13MAT307, EM13MAT201)
  python3 tools/gen_br_matematica_em2_areas_de_superficies.py
Áreas por decomposição e composição (triangulação de polígonos no quadriculado), trapézio e losango, setor circular,
coroa, fórmula de Heron; problemas práticos: pisos, tinta, grama, terreno.
Usa geradores do 8º ano (área do círculo, figuras compostas) com outro sorteio.
Erros: esquecer de dividir por 2 no triângulo, usar o diâmetro em πr², arredondar latas de tinta para baixo.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, R2, num, kosy

R = random.Random(92006)
a_circ, a_comp = use("gen_br_matematica_8_area_de_figuras_planas", 92904, "s1_circulo", "s3_compostas")
PI = F(314, 100)


def shoelace(pts):
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return F(abs(s), 2)


def s1_poligono():
    for _ in range(50):
        n = R.choice([3, 4, 4, 5])
        pts = [(R.randint(0, 5), R.randint(0, 5)) for _ in range(n)]
        cx = sum(x for x, _ in pts) / n
        cy = sum(y for _, y in pts) / n
        pts = sorted(set(pts), key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        if len(pts) != n:
            continue
        A = shoelace(pts)
        if A >= 4:
            break
    else:
        return None
    names = "ABCDE"[:n]
    g = kosy(pts=[(x, y, nm) for (x, y), nm in zip(pts, names)], lo=-1, hi=6, label="polígono %s no quadriculado (cada quadradinho tem 1 unidade de lado)" % names)
    u, x0, y0 = 24, 20 + 1 * 24, 20 + 6 * 24
    poly = "<polygon points='%s' fill='#1f5fbf' fill-opacity='0.15' stroke='#1f5fbf' stroke-width='2.2'/>" % " ".join("%d,%d" % (x0 + x * u, y0 - y * u) for x, y in pts)
    i = g.index("<circle")
    g = g[:i] + poly + g[i:]
    w = [d(A * 2), d(A + 1), d(A - 1) if A > 1 else d(A + 2)]
    return M(g + "Os vértices do polígono %s são %s. Qual é a sua área, em unidades de área?" % (names, ", ".join("%s(%d, %d)" % (nm, x, y) for (x, y), nm in zip(pts, names))), d(A), w,
             "Decompondo em triângulos e retângulos (ou pela fórmula dos vértices), a área é <b>%s</b>." % d(A))


def s2_formulas():
    k = R.choice(["trap", "los", "setor", "coroa", "heron"])
    if k == "trap":
        B, b, h = R.randint(8, 20), R.randint(3, 7), R.randint(3, 10)
        return M("Um trapézio tem bases de %d cm e %d cm e altura de %d cm. Qual é a área?" % (B, b, h), "%s cm²" % d(F((B + b) * h, 2)), ["%d cm²" % ((B + b) * h), "%d cm²" % (B * b * h), "%s cm²" % d(F(B * h, 2))], "(B + b) · h ÷ 2 = (%d + %d) · %d ÷ 2 = <b>%s cm²</b>." % (B, b, h, d(F((B + b) * h, 2))))
    if k == "los":
        D, dd = R.randint(6, 20), R.randint(4, 12)
        return M("As diagonais de um losango medem %d m e %d m. Qual é a área?" % (D, dd), "%s m²" % d(F(D * dd, 2)), ["%d m²" % (D * dd), "%d m²" % (2 * (D + dd)), "%s m²" % d(F(D * dd, 4))], "D · d ÷ 2 = <b>%s m²</b>." % d(F(D * dd, 2)))
    if k == "setor":
        r = R.choice([2, 3, 4, 6, 10, 12])
        a = R.choice([30, 45, 60, 90, 120, 180, 270])
        A = F(a, 360) * r * r
        return M("Qual é a área de um setor circular de raio %d cm e ângulo central de %d°? (Deixe com π.)" % (r, a), ("%sπ cm²" % d(A)).replace("1π", "π") if A != 1 else "π cm²", ["%sπ cm²" % d(A * 2), "%sπ cm²" % d(F(a, 360) * 2 * r), "%dπ cm²" % (r * r)],
                 "%d/360 · π · %d² = <b>%sπ cm²</b>." % (a, r, d(A)))
    if k == "coroa":
        r1, r2 = sorted(R.sample(range(2, 11), 2))
        return M("Uma pista circular tem raio interno de %d m e raio externo de %d m. Qual é a área da pista? (π = 3,14)" % (r1, r2), "%s m²" % d(PI * (r2 * r2 - r1 * r1)), ["%s m²" % d(PI * (r2 - r1) ** 2), "%s m²" % d(PI * r2 * r2), "%s m²" % d(2 * PI * (r2 - r1))],
                 "3,14 · (%d² − %d²) = 3,14 · %d = <b>%s m²</b>." % (r2, r1, r2 * r2 - r1 * r1, d(PI * (r2 * r2 - r1 * r1))))
    a, b, c = R.choice([(13, 14, 15), (5, 5, 6), (5, 5, 8), (10, 13, 13), (7, 15, 20), (9, 10, 17), (6, 25, 29), (3, 4, 5)])
    p = F(a + b + c, 2)
    A = math.isqrt(int(p * (p - a) * (p - b) * (p - c)))
    return M("Pela fórmula de Heron, qual é a área de um triângulo de lados %d, %d e %d?" % (a, b, c), num(A), [num(a * b // 2), num(int(p)), num(a * b * c // 4) if a * b * c // 4 != A else num(A + 6)],
             "p = %s; A = √(%s · %s · %s · %s) = <b>%d</b>." % (d(p), d(p), d(p - a), d(p - b), d(p - c), A))


def s3_pratica():
    k = R.choice(["piso", "tinta", "grama", "azulejo"])
    if k == "piso":
        c, l = R.choice([(4, 3), (5, 4), (6, 5), (8, 6), (5, 3)])
        p = R.choice([F(1, 2), F(1, 4)])
        lado = {F(1, 2): "50 cm", F(1, 4): "25 cm"}[p]
        n = int(F(c * l) / (p * p))
        return M("Quantas peças quadradas de %s de lado são necessárias para cobrir um piso de %d m × %d m?" % (lado, c, l), num(n), [num(c * l), num(int(F(c * l) / p)), num(n // 2)],
                 "Área %d m²; cada peça %s m²; %d ÷ %s = <b>%s</b>." % (c * l, d(p * p), c * l, d(p * p), num(n)))
    if k == "tinta":
        c, l, h = R.choice([(4, 3, F(5, 2)), (5, 4, 3), (6, 4, F(5, 2))])
        area = 2 * (c + l) * h
        rend = R.choice([20, 25, 30])
        n = math.ceil(area / rend)
        return M("As 4 paredes de uma sala de %d m × %d m têm %s m de altura. Uma lata de tinta pinta %d m². Quantas latas são necessárias (sem descontar portas e janelas)?" % (c, l, d(h), rend), "%d latas" % n, ["%d latas" % (n - 1) if n > 1 else "2 latas", "%d latas" % math.ceil(c * l / rend) if math.ceil(c * l / rend) != n else "%d latas" % (n + 2), "%d latas" % (n + 1)],
                 "Área das paredes: 2 · (%d + %d) · %s = %s m²; %s ÷ %d ≈ %s ⇒ <b>%d latas</b> (arredonde para cima)." % (c, l, d(h), d(area), d(area), rend, d(area / rend, 2), n))
    if k == "grama":
        r = R.choice([3, 4, 5, 6, 10])
        p = R.choice([8, 10, 12, 15])
        A = PI * r * r
        return M("Um canteiro circular de %d m de raio vai receber grama a %s por m². Quanto custa? (π = 3,14)" % (r, R2(p)), R2(A * p), [R2(2 * PI * r * p), R2(A), R2(PI * 4 * r * r * p)], "Área = 3,14 · %d² = %s m²; × %d = <b>%s</b>." % (r, d(A), p, R2(A * p)))
    c, h = R.choice([(3, 2), (4, F(5, 2)), (2, 2), (5, 3)])
    a = R.choice([F(1, 5), F(1, 10)])
    n = int(F(c) * h / (a * a))
    return M("Uma parede de %s m por %s m será coberta com azulejos quadrados de %d cm de lado. Quantos azulejos serão necessários?" % (d(c), d(h), int(a * 100)), num(n), [num(int(F(c) * h / a)), num(int(F(c) * h * 100)), num(n // 2)],
             "%s m² ÷ %s m² = <b>%s</b>." % (d(F(c) * h), d(a * a), num(n)))


def main():
    seen = set()
    sets = [
        ("Polígonos no quadriculado", mix(R, seen, [(s1_poligono, 20)])),
        ("Trapézio, losango e Heron", mix(R, seen, [(s2_formulas, 20)])),
        ("Círculo, setor e coroa", mix(R, seen, [(a_circ, 12), (s2_formulas, 8)])),
        ("Figuras compostas", mix(R, seen, [(a_comp, 20)])),
        ("Pisos, tintas e terrenos", mix(R, seen, [(s3_pratica, 20)])),
    ]
    body = lesson(
        ["Para achar a área de uma figura complicada, <b>decomponha</b> em retângulos, triângulos e partes de círculo, ou <b>complete</b> um retângulo e subtraia o que sobra.",
         "Triângulo: b · h ÷ 2. Trapézio: (B + b) · h ÷ 2. Losango: D · d ÷ 2. Círculo: πr². Setor de ângulo α: (α/360) · πr².",
         "<b>Heron</b>: com os três lados a, b, c e p = (a + b + c) ÷ 2, A = √(p(p − a)(p − b)(p − c)).",
         "Em problemas práticos (pisos, tinta), divida a área total pela área de cada peça ou pelo rendimento, e arredonde para cima."],
        [("Triângulo de lados 13, 14 e 15", ["p = 21", "√(21 · 8 · 7 · 6) = √7.056"], "84"),
         ("Paredes 2 · (4 + 3) · 2,5 = 35 m², lata para 20 m²", ["35 ÷ 20 = 1,75"], "2 latas")],
        [["Esquecer o ÷ 2", "Triângulos e losangos têm ÷ 2."],
         ["Usar o diâmetro em πr²", "Use o raio."],
         ["Arredondar as latas para baixo", "Faltaria tinta: arredonde para cima."]])
    faq = [("Como calcular a área de um terreno irregular?", "Divida o terreno em triângulos (triangulação), calcule a área de cada um e some. Com os vértices em coordenadas, também se pode usar a fórmula dos vértices."),
           ("O que a BNCC pede?", "Empregar diferentes métodos para a obtenção da medida da área de uma superfície (reconfigurações, aproximação por cortes etc.) e deduzir expressões de cálculo para aplicá-las em situações reais (EM13MAT307), e propor ou participar de ações adequadas às demandas da região que envolvam medições e cálculos de perímetro, área, volume, capacidade ou massa (EM13MAT201).")]
    unit(R, "areas-de-superficies", "M", ["EM13MAT307", "EM13MAT201"],
         "Empregar diferentes métodos para a obtenção da medida da área de uma superfície (reconfigurações, aproximação por cortes etc.) e deduzir expressões de cálculo para aplicá-las em situações reais (como o remanejamento e a distribuição de plantações, entre outros), com ou sem apoio de tecnologias digitais; propor ou participar de ações adequadas às demandas da região, preferencialmente para sua comunidade, envolvendo medições e cálculos de perímetro, de área, de volume, de capacidade ou de massa",
         "Áreas de superfícies planas", "Áreas de superfícies",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre áreas: polígonos no quadriculado, trapézio, losango, fórmula de Heron, setor circular, coroa, figuras compostas, pisos e tintas. 100 exercícios com gabarito.",
         "Decomponha e some as áreas", "Heron: A = √(p(p − a)(p − b)(p − c)).",
         body, faq, sets, 6, grade="2-serie")


if __name__ == "__main__":
    main()
