# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Vistas ortogonais (Geometria, EF09MA17)
  python3 tools/gen_br_matematica_9_vistas_ortogonais.py
Vista de cima, vista frontal e vista lateral de sólidos feitos de cubos (desenho em perspectiva); planta com números
(quantos cubos em cada lugar); vistas de cilindro, cone, pirâmide, esfera e prismas; reconhecer o sólido pelas vistas.
Usa as figuras do gerador do Reino Unido (plans and elevations) com outro sorteio, com o texto em português.
Erros: trocar a vista frontal pela lateral, desenhar a vista espelhada, contar só os cubos visíveis.
"""
import random
import re
from br_common import lesson, mix, mcq
import gen_uk_maths_y9_plans_and_elevations as UK
from br_9 import unit

R = random.Random(89017)
UK.R = R

TR = [("Which drawing shows the <b>plan</b> (the view from above)?", "Qual desenho mostra a <b>vista de cima</b>?"),
      ("Which drawing shows the <b>front elevation</b> (the view from the front)?", "Qual desenho mostra a <b>vista frontal</b> (seta vermelha)?"),
      ("Which drawing shows the <b>side elevation</b> (the view from the side arrow)?", "Qual desenho mostra a <b>vista lateral</b> (seta azul)?"),
      ("The plan shows how many cubes are stacked in each place. How many cubes are there altogether?", "Os números mostram quantos cubos estão empilhados em cada lugar (vista de cima). Quantos cubos há ao todo?"),
      ("The plan shows how many cubes are stacked in each place. Which drawing is the <b>front elevation</b>?", "Os números mostram quantos cubos estão empilhados em cada lugar (vista de cima). Qual desenho é a <b>vista frontal</b>?"),
      ("From above you see one square for every column of cubes, whatever its height. The front is at the bottom of the plan.", "De cima, cada pilha de cubos aparece como um quadrado, seja qual for a altura. A frente fica embaixo no desenho."),
      ("From the front each column shows its tallest stack. Read the columns from left to right as you look at the front.", "De frente, cada coluna mostra a sua pilha mais alta. Leia as colunas da esquerda para a direita, olhando pela frente."),
      ("From the side each row of the solid shows its tallest stack. The front of the solid is on the left of this view.", "De lado, cada fileira mostra a sua pilha mais alta. A frente do sólido fica à esquerda nesta vista."),
      (">Front<", ">Frente<"), (">Side<", ">Lado<"),
      ("solid made of cubes with four views", "sólido feito de cubos e quatro vistas"), ("plan with heights and four views", "planta com números e quatro vistas"),
      ("plan with heights", "planta com o número de cubos em cada lugar")]


def pt(item):
    if not item:
        return item
    for k in ("q", "e"):
        s = item[k]
        for a, b in TR:
            s = s.replace(a, b)
        s = re.sub(r"Add the numbers on the plan: <b>(\d+)</b> cubes\.", r"Some os números: <b>\1</b> cubos.", s)
        s = re.sub(r"From the front, each column shows its tallest stack: ([\d, ]+), reading left to right\.", r"De frente, cada coluna mostra a pilha mais alta: \1, da esquerda para a direita.", s)
        item[k] = s
    return item


def uk(fn):
    def f():
        return pt(fn(R))
    f.__name__ = fn.__name__
    return f


s_cima, s_frente, s_lado, s_planta = uk(UK.one_plan), uk(UK.one_front), uk(UK.one_side), uk(UK.one_numbered)

SOL = [
    ("Um cilindro está em pé sobre a base. Qual é a sua vista de cima?", "um círculo", ["um retângulo", "um triângulo", "um quadrado"]),
    ("Um cilindro está em pé sobre a base. Qual é a sua vista frontal?", "um retângulo", ["um círculo", "um triângulo", "um trapézio"]),
    ("Um cone está em pé sobre a base. Qual é a sua vista frontal?", "um triângulo", ["um círculo", "um retângulo", "um trapézio"]),
    ("Um cone está em pé sobre a base. Qual é a sua vista de cima?", "um círculo com um ponto no centro", ["um triângulo", "um quadrado", "um retângulo"]),
    ("Quais são as vistas de uma esfera?", "as três são círculos", ["as três são quadrados", "de cima um círculo, de frente um retângulo", "de cima um quadrado, de frente um círculo"]),
    ("Uma pirâmide de base quadrada está apoiada na base. Qual é a sua vista de cima?", "um quadrado com as diagonais", ["um triângulo", "um círculo", "um quadrado sem nenhuma linha dentro"]),
    ("Uma pirâmide de base quadrada está apoiada na base. Qual é a sua vista frontal?", "um triângulo", ["um quadrado", "um círculo", "um retângulo"]),
    ("Um sólido tem vista de cima circular e vistas frontal e lateral retangulares. Que sólido é?", "um cilindro", ["um cone", "uma esfera", "um cubo"]),
    ("Um sólido tem vista de cima circular e vistas frontal e lateral triangulares. Que sólido é?", "um cone", ["um cilindro", "uma esfera", "uma pirâmide de base quadrada"]),
    ("Um sólido tem as três vistas quadradas e do mesmo tamanho. Que sólido é?", "um cubo", ["um paralelepípedo qualquer", "um cilindro", "uma pirâmide"]),
    ("Um paralelepípedo mede 5 cm de comprimento, 3 cm de largura e 2 cm de altura. Quais são as medidas da vista de cima?", "5 cm por 3 cm", ["5 cm por 2 cm", "3 cm por 2 cm", "5 cm por 5 cm"]),
    ("Um paralelepípedo mede 5 cm de comprimento, 3 cm de largura e 2 cm de altura. Olhando o lado comprido, quais são as medidas da vista frontal?", "5 cm por 2 cm", ["5 cm por 3 cm", "3 cm por 2 cm", "2 cm por 2 cm"]),
    ("Um prisma triangular está deitado sobre uma face retangular, com a ponta do triângulo para cima. Olhando de frente para a base triangular, o que se vê?", "um triângulo", ["um retângulo", "um círculo", "um quadrado"]),
    ("Um prisma triangular está deitado sobre uma face retangular. Qual é a sua vista de cima?", "um retângulo com uma linha no meio", ["um triângulo", "um círculo", "um pentágono"]),
    ("Por que dois sólidos diferentes podem ter a mesma vista de cima?", "porque a vista de cima não mostra as alturas", ["porque todo sólido tem a mesma vista de cima", "porque a vista de cima mostra a frente", "porque as vistas são sempre quadradas"]),
    ("Na vista frontal, um cubo escondido atrás de outro…", "não muda o desenho", ["acrescenta um quadrado", "deixa a vista mais alta", "aparece em outra cor"]),
    ("Que vista mostra a diferença entre um cilindro e um prisma de base quadrada de mesma altura?", "a vista de cima", ["a vista frontal", "nenhuma vista", "a vista lateral"]),
    ("Uma lata de refrigerante em pé, vista de cima, parece…", "um círculo", ["um retângulo", "um triângulo", "uma elipse achatada"]),
    ("Uma casa com telhado de duas águas, vista de lado (na direção da cumeeira), parece…", "um pentágono (retângulo com triângulo em cima)", ["um retângulo", "um triângulo", "um círculo"]),
    ("As vistas ortogonais de um objeto são desenhadas olhando…", "na direção perpendicular a cada face (de frente, de cima e de lado)", ["sempre em perspectiva", "de um canto do objeto", "só de cima"]),
]


def s_solidos():
    q, a, w = R.choice(SOL)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Vista de cima", mix(R, seen, [(s_cima, 20)])),
        ("Vista frontal", mix(R, seen, [(s_frente, 20)])),
        ("Vista lateral", mix(R, seen, [(s_lado, 20)])),
        ("Planta com números", mix(R, seen, [(s_planta, 20)])),
        ("Vistas de sólidos geométricos", mix(R, seen, [(s_solidos, 20)])),
    ]
    body = lesson(
        ["As <b>vistas ortogonais</b> mostram um objeto olhando bem de frente para ele: a <b>vista frontal</b>, a <b>vista de cima</b> e a <b>vista lateral</b>.",
         "Em cada vista, o que fica atrás não aparece. Numa pilha de cubos, cada coluna mostra só a pilha mais alta.",
         "Com as três vistas, podemos imaginar e desenhar o objeto em perspectiva."],
        [("Cilindro em pé", ["de cima: círculo", "de frente: retângulo"], "vistas de um cilindro"),
         ("Planta com 2, 1 e 3 cubos", ["2 + 1 + 3"], "6 cubos")],
        [["Trocar a vista frontal pela lateral", "Veja de que lado está cada seta."],
         ["Desenhar a vista espelhada", "Olhe como se você estivesse na posição da seta."],
         ["Contar só os cubos visíveis", "Na planta com números, some todos os números."]])
    faq = [("O que são vistas ortogonais?", "São os desenhos de um objeto visto de frente, de cima e de lado, olhando na direção perpendicular a cada face. Elas são usadas em plantas de casas, desenho técnico e projetos."),
           ("O que a BNCC pede no 9º ano?", "Reconhecer vistas ortogonais de figuras espaciais e aplicar esse conhecimento para desenhar objetos em perspectiva (EF09MA17).")]
    unit(R, "vistas-ortogonais", "G", ["EF09MA17"],
         "Reconhecer vistas ortogonais de figuras espaciais e aplicar esse conhecimento para desenhar objetos em perspectiva",
         "Vistas ortogonais: frente, cima e lado", "Vistas ortogonais",
         "Atividades de matemática para o 9º ano sobre vistas ortogonais: vista frontal, de cima e lateral de sólidos feitos de cubos, planta com números e vistas de cilindro, cone, pirâmide e esfera. 100 exercícios com gabarito.",
         "Frente, cima e lado.", "O que está atrás não aparece na vista.",
         body, faq, sets, 17)


if __name__ == "__main__":
    main()
