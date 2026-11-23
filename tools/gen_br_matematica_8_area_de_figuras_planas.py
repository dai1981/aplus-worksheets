# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Área de figuras planas e do círculo (Grandezas e medidas, EF08MA19)
  python3 tools/gen_br_matematica_8_area_de_figuras_planas.py
Áreas de triângulos e quadriláteros (revisão); área do círculo A = πr² (π ≈ 3,14 ou resposta com π); semicírculo e coroa circular;
figuras compostas (retângulo com semicírculo, quadrado sem círculo); problemas (pizzas, canteiros, praças).
Usa geradores do 7º ano (área de figuras planas) com outro sorteio.
Erros: usar 2πr (comprimento) no lugar de πr², usar o diâmetro em r², esquecer de dividir por 2 no semicírculo.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use, reais
from br_9 import M, d, bank, circulo, unit

R = random.Random(88015)
a_texto, a_prob = use("gen_br_matematica_7_area_de_figuras_planas", 88915, "s2_texto", "s3_problemas")
PI = F(314, 100)


def s1_circulo():
    r = R.randint(1, 20)
    k = R.choice(["pi", "num", "diam"])
    if k == "pi":
        return M("Qual é a área de um círculo de raio %d cm? (Deixe a resposta com π.)" % r, "%dπ cm²" % (r * r), ["%dπ cm²" % (2 * r), "%dπ cm²" % (4 * r * r) if r > 1 else "4π cm²", "%dπ cm²" % r if r > 1 else "2π cm²"],
                     "A = π · r² = π · %d² = <b>%dπ cm²</b>." % (r, r * r))
    if k == "num":
        return M("Qual é a área de um círculo de raio %d m? (Use π = 3,14.)" % r, "%s m²" % d(PI * r * r), ["%s m²" % d(2 * PI * r), "%s m²" % d(PI * r), "%s m²" % d(PI * 4 * r * r)], "A = 3,14 · %d² = 3,14 · %d = <b>%s m²</b>." % (r, r * r, d(PI * r * r)))
    return M("Qual é a área de um círculo de diâmetro %d cm? (Deixe a resposta com π.)" % (2 * r), "%dπ cm²" % (r * r), ["%dπ cm²" % (4 * r * r), "%dπ cm²" % (2 * r), "%dπ cm²" % (r * r * 2)],
             "Raio = %d; A = π · %d² = <b>%dπ cm²</b>." % (r, r, r * r))


def s2_partes():
    r = R.randint(2, 12)
    k = R.choice(["semi", "coroa", "quarto"])
    if k == "semi":
        return M("Qual é a área de um semicírculo de raio %d cm? (Deixe com π.)" % r, ("%sπ cm²" % d(F(r * r, 2))).replace("1π", "π") if r * r != 2 else "π cm²", ["%dπ cm²" % (r * r), "%dπ cm²" % r, "%dπ cm²" % (2 * r)],
                 "Metade do círculo: π · %d² ÷ 2 = <b>%sπ cm²</b>." % (r, d(F(r * r, 2))))
    if k == "quarto":
        r = R.choice([2, 4, 6, 8, 10, 12])
        return M("Qual é a área de um quarto de círculo de raio %d cm? (Deixe com π.)" % r, "%sπ cm²" % d(F(r * r, 4)) if r * r != 4 else "π cm²", ["%dπ cm²" % (r * r), "%sπ cm²" % d(F(r * r, 2)), "%dπ cm²" % r],
                 "π · %d² ÷ 4 = <b>%sπ cm²</b>." % (r, d(F(r * r, 4))))
    R2 = r + R.randint(1, 5)
    return M("Uma coroa circular fica entre circunferências de raios %d cm e %d cm. Qual é a sua área? (Deixe com π.)" % (r, R2), "%dπ cm²" % (R2 * R2 - r * r), ["%dπ cm²" % ((R2 - r) ** 2), "%dπ cm²" % (R2 * R2 + r * r), "%dπ cm²" % (2 * (R2 - r))],
             "π · %d² − π · %d² = <b>%dπ cm²</b>." % (R2, r, R2 * R2 - r * r))


def s3_compostas():
    k = R.choice(["quad_menos", "ret_semi", "pizza", "praca"])
    if k == "quad_menos":
        L = R.choice([4, 6, 8, 10, 12, 20])
        r = L // 2
        A = L * L - PI * r * r
        return M("De uma placa quadrada de lado %d cm foi recortado o maior círculo possível. Qual é a área que sobra? (π = 3,14)" % L, "%s cm²" % d(A), ["%s cm²" % d(L * L - PI * r) if L * L - PI * r != A else "%s cm²" % d(PI * L), "%s cm²" % d(PI * r * r), "%s cm²" % d(L * L - 2 * PI * r)],
                 "Raio %d: %d² − 3,14 · %d² = %d − %s = <b>%s cm²</b>." % (r, L, r, L * L, d(PI * r * r), d(A)))
    if k == "ret_semi":
        c, l = R.choice([(10, 4), (12, 6), (8, 4), (20, 10), (14, 8)])
        A = c * l + PI * (l // 2) ** 2 / 2
        return M("Uma janela tem a forma de um retângulo de %d dm por %d dm com um semicírculo em cima, cujo diâmetro é o lado de %d dm. Qual é a área da janela? (π = 3,14)" % (c, l, l), "%s dm²" % d(A), ["%s dm²" % d(c * l + PI * (l // 2) ** 2), "%d dm²" % (c * l), "%s dm²" % d(c * l + PI * l * l / 2)],
                 "%d × %d + 3,14 · %d² ÷ 2 = <b>%s dm²</b>." % (c, l, l // 2, d(A)))
    if k == "pizza":
        r1, r2 = R.choice([(15, 20), (10, 15), (20, 25), (12, 18)])
        return M("Uma pizza média tem raio %d cm e uma grande, %d cm. Quantas vezes a área da grande é maior que a da média?" % (r1, r2), d(F(r2 * r2, r1 * r1), 2) + " vezes" if (F(r2 * r2, r1 * r1) * 100).denominator == 1 else "cerca de %s vezes" % d(F(r2 * r2, r1 * r1), 2),
                 [d(F(r2, r1), 2) + " vezes" if (F(r2, r1) * 100).denominator == 1 else "cerca de %s vezes" % d(F(r2, r1), 2), "%d vezes" % (r2 - r1), "as áreas são iguais"],
                 "A razão das áreas é (%d/%d)² = %d/%d ≈ <b>%s</b>." % (r2, r1, r2 * r2, r1 * r1, d(F(r2 * r2, r1 * r1), 2)))
    r = R.choice([5, 10, 15, 20])
    p = R.choice([20, 30, 40])
    A = PI * r * r
    return M("Uma praça circular de raio %d m vai receber grama, que custa %s o m². Quanto custa a grama? (π = 3,14)" % (r, reais(p * 100)), reais(int(A * p * 100)), [reais(int(2 * PI * r * p * 100)), reais(int(A * 100)), reais(int(PI * r * p * 100))],
             "Área = 3,14 · %d² = %s m²; × %s = <b>%s</b>." % (r, d(A), reais(p * 100), reais(int(A * p * 100))))


s4_conceitos = bank(R, [
    ("A área do círculo é calculada por…", "π · r²", ["2 · π · r", "π · d", "r²"]),
    ("Se o raio de um círculo dobra, a área fica…", "4 vezes maior", ["2 vezes maior", "igual", "8 vezes maior"]),
    ("Uma pizza de raio 20 cm tem área ___ que duas pizzas de raio 10 cm.", "maior", ["menor", "igual", "a metade"]),
    ("Para calcular a área de um círculo de diâmetro 10 cm, usamos r = …", "5 cm", ["10 cm", "20 cm", "3,14 cm"]),
    ("A área de um semicírculo é…", "metade da área do círculo", ["o dobro da área do círculo", "igual ao perímetro", "π · r"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Triângulos e quadriláteros", mix(R, seen, [(a_texto, 20)])),
        ("Área do círculo", mix(R, seen, [(s1_circulo, 20)])),
        ("Partes do círculo", mix(R, seen, [(s2_partes, 15), (s4_conceitos, 5)])),
        ("Figuras compostas", mix(R, seen, [(s3_compostas, 20)])),
        ("Problemas", mix(R, seen, [(a_prob, 12), (s1_circulo, 8)])),
    ]
    body = lesson(
        ["Revisão: retângulo b · h; paralelogramo b · h; triângulo b · h ÷ 2; trapézio (B + b) · h ÷ 2; losango D · d ÷ 2.",
         "<b>Área do círculo</b>: A = π · r² (π ≈ 3,14). Use o raio, a metade do diâmetro.",
         "Semicírculo: metade da área do círculo. Coroa circular: área do círculo maior − área do círculo menor.",
         "Figuras compostas: some ou subtraia as áreas das partes."],
        [("Círculo de raio 5 cm", ["3,14 · 25"], "78,5 cm²"),
         ("Quadrado de lado 10 sem o círculo inscrito", ["100 − 78,5"], "21,5 cm²")],
        [["Usar 2πr na área", "2πr é o comprimento; a área é πr²."],
         ["Usar o diâmetro em r²", "Divida o diâmetro por 2 antes."],
         ["Esquecer o ÷ 2 no semicírculo", "Semicírculo é metade."]],
        circulo({"A": 20}, [("O", "A")], label="círculo de centro O e raio OA"))
    faq = [("Como calcular a área de um círculo?", "Multiplique π (≈ 3,14) pelo raio ao quadrado: A = π · r². Se tiver o diâmetro, divida por 2 para achar o raio."),
           ("O que a BNCC pede no 8º ano?", "Resolver e elaborar problemas que envolvam medidas de área de figuras geométricas, utilizando expressões de cálculo de área (quadriláteros, triângulos e círculos), em situações como determinar medida de terrenos (EF08MA19).")]
    unit(R, "area-de-figuras-planas-e-do-circulo", "M", ["EF08MA19"],
         "Resolver e elaborar problemas que envolvam medidas de área de figuras geométricas, utilizando expressões de cálculo de área (quadriláteros, triângulos e círculos), em situações como determinar medida de terrenos",
         "Área de figuras planas e do círculo", "Área do círculo e de figuras planas",
         "Atividades de matemática para o 8º ano sobre áreas: triângulos e quadriláteros, área do círculo, semicírculo, coroa circular, figuras compostas e problemas. 100 exercícios com gabarito.",
         "Área do círculo: π · r²", "Use o raio, não o diâmetro.",
         body, faq, sets, 15, grade="8-ano")


if __name__ == "__main__":
    main()
