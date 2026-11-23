# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Figuras geométricas planas (Geometria, EF01MA14)
  python3 tools/gen_br_matematica_1_figuras_geometricas_planas.py
Círculo, quadrado, retângulo e triângulo: nome, em posições diferentes, lados e cantos, contar figuras num desenho,
o contorno das faces de objetos (carimbo), figuras no dia a dia. Usa geradores do 2º ano com outro sorteio.
Erros: achar que o triângulo de ponta para baixo não é triângulo, chamar a bola de círculo, confundir quadrado e retângulo.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, use, fig, relabel

R = random.Random(80113)
M2 = "gen_br_matematica_2_figuras_geometricas_planas"
f_nome, f_letras, f_lados, f_contar, f_carimbo, f_obj, f_prop, f_qr = use(M2, 80981, "s1_nome", "s1_letras", "s2_lados", "s3_contar", "s4_carimbo", "s5_objeto", "s2_prop", "s4_qr")


def main():
    seen = set()
    sets = [
        ("Que figura é esta?", mix(R, seen, [(f_nome, 20)])),
        ("Encontrar a figura", mix(R, seen, [(f_letras, 14), (f_qr, 6)])),
        ("Lados e cantos", mix(R, seen, [(f_lados, 12), (f_prop, 8)])),
        ("Contar figuras", mix(R, seen, [(f_contar, 20)])),
        ("Figuras nos objetos", mix(R, seen, [(f_obj, 10), (f_carimbo, 7), (f_qr, 3)])),
    ]
    body = lesson(
        ["As figuras planas são «achatadas», como um desenho no papel.",
         "O <b>círculo</b> é redondo. O <b>triângulo</b> tem 3 lados. O <b>quadrado</b> tem 4 lados iguais. O <b>retângulo</b> tem 4 lados, dois compridos e dois curtos.",
         "Girar a figura não muda o nome: um triângulo de ponta para baixo continua sendo triângulo.",
         "Se você carimbar o fundo de uma lata, aparece um círculo; a face de um dado, um quadrado."],
        [("Figura com 3 lados", ["conte os lados"], "triângulo"),
         ("Fundo de um copo carimbado", ["é redondo"], "círculo")],
        [["Achar que o triângulo girado é outra figura", "Conte os lados: 3 lados é triângulo."],
         ["Chamar a bola de círculo", "A bola é esfera; o círculo é plano."],
         ["Confundir quadrado e retângulo", "No quadrado, todos os lados são iguais."]],
        fig(relabel(k_pics.lettered_shapes_svg([("circle", "red"), ("triangle", "yellow"), ("square", "blue"), ("rectangle", "green")]), "círculo, triângulo, quadrado e retângulo")))
    faq = [("Que figuras planas o 1º ano estuda?", "A BNCC pede identificar e nomear círculo, quadrado, retângulo e triângulo em desenhos em diferentes posições e nos contornos das faces de sólidos."),
           ("Como praticar em casa?", "Procure figuras pela casa: a porta (retângulo), o relógio (círculo), o ladrilho (quadrado). Carimbe objetos com tinta para ver as formas.")]
    make_unit(R, "figuras-geometricas-planas", "G", ["EF01MA14"],
              "Identificar e nomear figuras planas (círculo, quadrado, retângulo e triângulo) em desenhos apresentados em diferentes disposições ou em contornos de faces de sólidos geométricos",
              "Figuras planas: círculo, quadrado, retângulo e triângulo", "Figuras planas",
              "Atividades de matemática para o 1º ano sobre figuras planas: círculo, quadrado, retângulo e triângulo em posições diferentes, lados e cantos, contornos de objetos. 100 exercícios com gabarito.",
              "Triângulo: 3 lados. Quadrado: 4 lados iguais.", "Girar não muda o nome da figura.",
              body, faq, sets, 13, grade="1-ano")


if __name__ == "__main__":
    main()
