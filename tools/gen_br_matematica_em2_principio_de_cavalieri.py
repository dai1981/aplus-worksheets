# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Volumes e princípio de Cavalieri (EM13MAT504)
  python3 tools/gen_br_matematica_em2_principio_de_cavalieri.py
Princípio de Cavalieri (mesma altura e mesmas áreas de seção ⇒ mesmo volume); prismas e cilindros oblíquos;
pirâmide = 1/3 do prisma, cone = 1/3 do cilindro, esfera = 2/3 do cilindro circunscrito (Arquimedes);
pilhas de folhas ou moedas inclinadas; comparar volumes.
Erros: usar a aresta lateral inclinada como altura, achar que inclinar muda o volume, esquecer o 1/3.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, unit, num, _svg, _ln, _t, INK, BLUE

R = random.Random(92010)


def pilhas(n, shift):
    W, H = 340, 200
    s = []
    for j, sh in enumerate((0, shift)):
        x0 = 40 + j * 160
        for i in range(n):
            y = 170 - i * (130.0 / n)
            x = x0 + sh * i / n
            s.append("<rect x='%.1f' y='%.1f' width='90' height='%.1f' fill='#dfe9f7' stroke='%s' stroke-width='1'/>" % (x, y - 130.0 / n, 130.0 / n, INK))
    s.append(_t(85, 195, "pilha 1", 13, INK, bold=False) + _t(245 + shift / 2, 195, "pilha 2", 13, INK, bold=False))
    return _svg(W, H, "".join(s), "duas pilhas com as mesmas folhas, uma reta e outra inclinada")


def s1_obliquo():
    k = R.choice(["prisma", "cil", "pilha"])
    if k == "prisma":
        a, b = R.randint(2, 8), R.randint(2, 8)
        h = R.randint(3, 12)
        lat = h + R.randint(1, 4)
        return M("Um prisma oblíquo tem base retangular de %d cm × %d cm, altura %d cm e aresta lateral %d cm. Qual é o volume?" % (a, b, h, lat), "%d cm³" % (a * b * h), ["%d cm³" % (a * b * lat), "%s cm³" % d(F(a * b * h, 3)), "%d cm³" % (2 * (a * b + a * h + b * h))],
                 "Cavalieri: igual ao prisma reto de mesma base e altura: %d · %d · %d = <b>%d cm³</b>." % (a, b, h, a * b * h))
    if k == "cil":
        r, h = R.randint(1, 8), R.randint(3, 12)
        return M("Um cilindro oblíquo tem raio %d cm e altura (distância entre as bases) %d cm. Qual é o volume? (Deixe com π.)" % (r, h), "%dπ cm³" % (r * r * h), ["%dπ cm³" % (2 * r * h), "%sπ cm³" % d(F(r * r * h, 3)) if (r * r * h) % 3 == 0 else "%dπ cm³" % (r * h), "%dπ cm³" % (r * r * (h + 2))],
                 "Volume do cilindro reto de mesma base e altura: π · %d · %d = <b>%dπ cm³</b>." % (r * r, h, r * r * h))
    n = R.choice([100, 200, 500])
    e = R.choice([F(1, 10), F(2, 10), F(5, 100)])
    c, l = R.choice([(30, 20), (28, 21), (20, 15)])
    V = c * l * n * e
    g = pilhas(8, R.choice([30, 50]))
    return M(g + "Cada pilha tem %d folhas de %d cm × %d cm e %s mm de espessura. Qual é o volume da pilha 2, a inclinada?" % (n, c, l, d(e * 10)), "%s cm³" % d(V), ["menor que o da pilha 1", "maior que o da pilha 1", "%s cm³" % d(V * 2)],
             "Mesmas seções e mesma altura: mesmo volume da pilha reta, %d · %d · %s = <b>%s cm³</b>." % (c, l, d(n * e), d(V)))


def s2_razoes():
    k = R.choice(["pir", "cone", "esf", "inv"])
    if k == "pir":
        V = R.choice(range(30, 301, 15))
        return M("Um prisma e uma pirâmide têm a mesma base e a mesma altura. O prisma tem %d cm³. Qual é o volume da pirâmide?" % V, "%d cm³" % (V // 3), ["%d cm³" % V, "%d cm³" % (V // 2) if V % 2 == 0 else "%d cm³" % (3 * V), "%d cm³" % (3 * V)], "A pirâmide é 1/3 do prisma: <b>%d cm³</b>." % (V // 3))
    if k == "cone":
        V = R.choice(range(12, 121, 6))
        return M("Um cilindro e um cone têm a mesma base e a mesma altura. O cilindro comporta %d L. Quanto comporta o cone?" % V, "%d L" % (V // 3), ["%d L" % (V // 2), "%d L" % V, "%d L" % (2 * V // 3)], "O cone é 1/3 do cilindro: <b>%d L</b>." % (V // 3))
    if k == "esf":
        r = R.choice([1, 2, 3, 4, 5, 6])
        cil = 2 * r ** 3
        return M("Uma esfera de raio %d cm está dentro de um cilindro que a envolve exatamente (raio %d cm, altura %d cm). O volume do cilindro é %dπ cm³. Qual é o volume da esfera?" % (r, r, 2 * r, cil), ("%dπ/3 cm³" % (2 * cil) if (2 * cil) % 3 else "%dπ cm³" % (2 * cil // 3)),
                 ["%dπ cm³" % cil, "%dπ/3 cm³" % cil if cil % 3 else "%dπ cm³" % (cil // 3), "%dπ cm³" % (cil // 2)], "Arquimedes: a esfera é 2/3 do cilindro circunscrito: <b>%s</b>." % ("%dπ/3 cm³" % (2 * cil) if (2 * cil) % 3 else "%dπ cm³" % (2 * cil // 3)))
    V = R.choice(range(10, 81, 5))
    return M("Uma pirâmide tem %d cm³. Qual é o volume de um prisma de mesma base e mesma altura?" % V, "%d cm³" % (3 * V), ["%d cm³" % V, "%s cm³" % d(F(V, 3)) if V % 3 == 0 else "%d cm³" % (2 * V), "%d cm³" % (2 * V)], "O prisma é 3 vezes a pirâmide: <b>%d cm³</b>." % (3 * V))


s3_conceitos = bank(R, [
    ("O princípio de Cavalieri diz que dois sólidos de mesma altura têm o mesmo volume se…", "toda seção paralela à base tiver a mesma área nos dois", ["tiverem a mesma forma", "tiverem a mesma aresta lateral", "tiverem o mesmo número de faces"]),
    ("Uma pilha de moedas reta e outra inclinada, com as mesmas moedas, têm…", "o mesmo volume", ["volumes diferentes", "a inclinada maior volume", "a reta maior volume"]),
    ("No prisma oblíquo, a altura é…", "a distância entre as bases", ["a aresta lateral", "a diagonal", "a aresta da base"]),
    ("Pelo princípio de Cavalieri, o volume de qualquer prisma é…", "área da base × altura", ["área da base × aresta lateral", "perímetro × altura", "área da base ÷ 3"]),
    ("Duas pirâmides com bases de mesma área e mesma altura têm…", "o mesmo volume, mesmo com bases de formas diferentes", ["volumes diferentes", "a mesma forma", "a mesma área lateral"]),
    ("O volume do cone é que fração do volume do cilindro de mesma base e altura?", "1/3", ["1/2", "2/3", "3"]),
    ("Arquimedes mostrou que o volume da esfera é que fração do cilindro que a envolve?", "2/3", ["1/3", "1/2", "3/4"]),
    ("Inclinar um sólido, mantendo a altura e as seções,…", "não muda o volume", ["aumenta o volume", "diminui o volume", "muda a altura"]),
], "s3_conceitos")


def s4_comparar():
    a = R.choice([2, 3, 4, 6])
    h = R.choice([3, 6, 9, 12])
    k = R.choice(["piramides", "cubo_pir", "cil_cone"])
    if k == "piramides":
        return M("Uma pirâmide de base quadrada %d × %d e outra de base retangular %d × %d têm a mesma altura %d. Os volumes são…" % (a * 2, a * 2, a, a * 4, h), "iguais (bases de mesma área)", ["diferentes", "o da base quadrada é maior", "o da base retangular é o dobro"],
                 "Áreas das bases: %d e %d. Mesma área e altura: <b>volumes iguais</b> (%d cm³ cada)." % (4 * a * a, 4 * a * a, 4 * a * a * h // 3))
    if k == "cubo_pir":
        return M("Quantas pirâmides de base %d × %d e altura %d cabem, em volume, num cubo de aresta %d?" % (a, a, a, a), "3", ["2", "4", "6"], "V(cubo) = %d; V(pirâmide) = %d ÷ 3: <b>3</b>." % (a ** 3, a ** 3))
    return M("Um copo cilíndrico e um copo cônico têm o mesmo raio e a mesma altura. Quantos copos cônicos cheios enchem o cilíndrico?", "3", ["2", "1", "4"], "O cone é 1/3 do cilindro: <b>3</b>.") if a == 2 else \
        M("Um cilindro de raio %d e altura %d e um cone de raio %d e altura %d têm o mesmo volume?" % (a, h, a, 3 * h), "sim", ["não, o cilindro é maior", "não, o cone é maior", "não dá para saber"],
          "Cilindro: π · %d · %d = %dπ; cone: π · %d · %d ÷ 3 = %dπ: <b>sim</b>." % (a * a, h, a * a * h, a * a, 3 * h, a * a * h))


def main():
    seen = set()
    sets = [
        ("O princípio de Cavalieri", mix(R, seen, [(s3_conceitos, 8), (s1_obliquo, 12)])),
        ("Sólidos oblíquos", mix(R, seen, [(s1_obliquo, 20)])),
        ("Pirâmide, cone e esfera", mix(R, seen, [(s2_razoes, 20)])),
        ("Comparar volumes", mix(R, seen, [(s4_comparar, 14), (s2_razoes, 6)])),
        ("Revisão", mix(R, seen, [(s1_obliquo, 12), (s2_razoes, 8)])),
    ]
    body = lesson(
        ["<b>Princípio de Cavalieri</b>: se dois sólidos têm a mesma altura e, em cada nível, as seções paralelas à base têm a mesma área, então eles têm o <b>mesmo volume</b>.",
         "Por isso um prisma ou cilindro <b>oblíquo</b> tem o mesmo volume do reto de mesma base e mesma altura: V = Ab · h (a altura é a distância entre as bases).",
         "A pirâmide é 1/3 do prisma de mesma base e altura; o cone é 1/3 do cilindro; a esfera é 2/3 do cilindro que a envolve.",
         "Uma pilha de folhas inclinada tem o mesmo volume da pilha reta."],
        [("Prisma oblíquo: base 4 × 5, altura 6, aresta lateral 7", ["V = 20 · 6 (a aresta lateral não entra)"], "120 cm³")],
        [["Usar a aresta inclinada como altura", "A altura é a distância entre os planos das bases."],
         ["Achar que inclinar muda o volume", "As seções não mudam, então o volume não muda."],
         ["Esquecer o 1/3", "Pirâmides e cones: Ab · h ÷ 3."]],
        pilhas(8, 40))
    faq = [("O que é o princípio de Cavalieri?", "Dois sólidos com a mesma altura cujas seções, feitas na mesma altura, têm sempre a mesma área, têm o mesmo volume. Ele explica por que inclinar uma pilha de folhas não muda seu volume."),
           ("O que a BNCC pede?", "Investigar processos de obtenção da medida do volume de prismas, pirâmides, cilindros e cones, incluindo o princípio de Cavalieri, para a obtenção das fórmulas de cálculo da medida do volume dessas figuras (EM13MAT504).")]
    unit(R, "volumes-e-principio-de-cavalieri", "M", ["EM13MAT504"],
         "Investigar processos de obtenção da medida do volume de prismas, pirâmides, cilindros e cones, incluindo o princípio de Cavalieri, para a obtenção das fórmulas de cálculo da medida do volume dessas figuras",
         "Volumes e princípio de Cavalieri", "Princípio de Cavalieri",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre o princípio de Cavalieri: sólidos oblíquos, pilhas inclinadas, pirâmide como 1/3 do prisma, cone como 1/3 do cilindro e esfera de Arquimedes. 100 exercícios com gabarito.",
         "Mesma altura e mesmas seções: mesmo volume", "Pirâmide e cone: 1/3 do prisma e do cilindro.",
         body, faq, sets, 10, grade="2-serie")


if __name__ == "__main__":
    main()
