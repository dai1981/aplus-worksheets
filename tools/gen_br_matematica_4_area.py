# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Área na malha quadriculada (Grandezas e medidas, EF04MA21)
  python3 tools/gen_br_matematica_4_area.py
Medir a área contando quadradinhos inteiros e metades; comparar e estimar áreas; figuras de formatos diferentes com a mesma área;
retângulos (linhas × colunas); área e perímetro não são a mesma coisa; problemas.
Usa geradores do 3º ano (área) e do 5º ano (perímetro e área) com outro sorteio.
Erros: contar os lados em vez dos quadradinhos, contar a metade como um inteiro, achar que a figura mais comprida tem mais área.
"""
import random
from br_common import lesson, make_unit, mix, use, lim

R = random.Random(80417)
A3 = "gen_br_matematica_3_area"
P5 = "gen_br_matematica_5_perimetro_e_area"
a_contar, a_ret, a_comp, a_mesma, a_metade, a_quiz, a_ret2, a_prob = use(A3, 80961, "s1_contar", "s1_retangulo", "s2_comparar", "s2_mesma", "s3_metade", "s4_quiz", "s4_ret", "s5_problema")
p_malha, p_mesma, p_unid = use(P5, 80962, "s1_malha", "s3_mesma_area", "s4_unidade", preds=(lim(9999, 0),))


def main():
    seen = set()
    sets = [
        ("Contar quadradinhos", mix(R, seen, [(a_contar, 12), (a_ret, 8)])),
        ("Inteiros e metades", mix(R, seen, [(a_metade, 12), (a_contar, 8)])),
        ("Comparar áreas", mix(R, seen, [(a_comp, 10), (a_mesma, 10)])),
        ("Área e perímetro", mix(R, seen, [(p_malha, 8), (p_mesma, 6), (a_ret2, 6)])),
        ("Problemas", mix(R, seen, [(a_prob, 12), (a_quiz, 4), (p_unid, 4)])),
    ]
    body = lesson(
        ["A <b>área</b> é o tamanho da superfície de uma figura. Na malha, conte quantos quadradinhos cabem dentro dela.",
         "Duas metades de quadradinho formam 1 quadradinho inteiro.",
         "Figuras com formatos diferentes podem ter a <b>mesma área</b>.",
         "Num retângulo, multiplique as linhas pelas colunas: 4 linhas de 6 quadradinhos = 24 quadradinhos.",
         "O <b>perímetro</b> é o contorno; a área é a superfície de dentro."],
        [("Uma figura tem 9 quadradinhos inteiros e 4 metades.", ["4 metades = 2 inteiros", "9 + 2"], "11 quadradinhos"),
         ("Retângulo de 3 linhas com 5 quadradinhos", ["3 × 5"], "15 quadradinhos")],
        [["Contar os lados em vez dos quadradinhos", "Área é o que está dentro; o contorno é o perímetro."],
         ["Contar a metade como um inteiro", "Junte as metades de duas em duas."],
         ["Achar que a figura mais comprida tem mais área", "Conte os quadradinhos: formatos diferentes podem ter a mesma área."]])
    faq = [("Como o 4º ano mede áreas?", "A BNCC pede medir, comparar e estimar a área de figuras desenhadas em malha quadriculada, contando quadradinhos ou metades de quadradinho."),
           ("Figuras diferentes podem ter a mesma área?", "Sim. Um retângulo de 2 por 6 e uma figura em L feita com 12 quadradinhos têm a mesma área: 12 quadradinhos, mesmo com formatos diferentes.")]
    make_unit(R, "area", "M", ["EF04MA21"],
              "Medir, comparar e estimar área de figuras planas desenhadas em malha quadriculada, pela contagem dos quadradinhos ou de metades de quadradinho, reconhecendo que duas figuras com formatos diferentes podem ter a mesma medida de área",
              "Área na malha quadriculada: quadradinhos e metades", "Área",
              "Atividades de matemática para o 4º ano sobre área: contar quadradinhos e metades na malha, comparar áreas, figuras diferentes com a mesma área, área e perímetro. 100 exercícios com gabarito.",
              "Área: quantos quadradinhos cabem dentro da figura.", "2 metades = 1 quadradinho.",
              body, faq, sets, 17, grade="4-ano")


if __name__ == "__main__":
    main()
