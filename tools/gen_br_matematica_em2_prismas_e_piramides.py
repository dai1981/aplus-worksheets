# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Prismas e pirâmides (EM13MAT309)
  python3 tools/gen_br_matematica_em2_prismas_e_piramides.py
Diagonal do cubo e do paralelepípedo; área lateral e total de prismas; volume de prismas (V = Ab · h);
pirâmide regular: apótema, área lateral e total, volume (V = Ab · h ÷ 3); relação de Euler; problemas (caixas, telhados, embalagens).
Usa geradores do 6º ano (Euler) e do 9º ano (volume do paralelepípedo e de prismas) com outro sorteio.
Erros: esquecer o ÷ 3 na pirâmide, usar a altura no lugar do apótema na área lateral, contar só uma base na área total.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, sq, num

R = random.Random(92008)
v_paral, v_prisma = use("gen_br_matematica_9_volume_de_prismas_e_cilindros", 92906, "s1_paral", "s2_prisma")
p_euler = use("gen_br_matematica_6_prismas_e_piramides", 92907, "s2_euler")


def s1_diag():
    k = R.choice(["cubo", "par", "par"])
    if k == "cubo":
        a = R.randint(2, 10)
        return M("Qual é a diagonal de um cubo de aresta %d cm?" % a, "%d√3 cm" % a, ["%d√2 cm" % a, "%d cm" % (3 * a), "%d√3 cm" % (a * a)], "D = a√3 = <b>%d√3 cm</b>." % a)
    a, b, c = R.choice([(3, 4, 12), (2, 3, 6), (1, 4, 8), (2, 6, 9), (4, 4, 7), (6, 6, 7), (2, 10, 11), (3, 4, 5), (2, 4, 4), (1, 2, 2)])
    D2 = a * a + b * b + c * c
    return M("Qual é a diagonal de um paralelepípedo de dimensões %d cm, %d cm e %d cm?" % (a, b, c), "%s cm" % sq(D2), ["%s cm" % sq(a * a + b * b), "%d cm" % (a + b + c), "%s cm" % sq(b * b + c * c)],
             "D = √(%d² + %d² + %d²) = √%d = <b>%s cm</b>." % (a, b, c, D2, sq(D2)))


def s2_area_prisma():
    k = R.choice(["cubo", "par", "tri", "hexa"])
    if k == "cubo":
        a = R.randint(2, 12)
        return M("Qual é a área total de um cubo de aresta %d cm?" % a, "%d cm²" % (6 * a * a), ["%d cm²" % (4 * a * a), "%d cm²" % (a ** 3), "%d cm²" % (6 * a)], "6 faces de %d²: <b>%d cm²</b>." % (a, 6 * a * a))
    if k == "par":
        a, b, c = R.randint(2, 10), R.randint(2, 10), R.randint(2, 10)
        At = 2 * (a * b + a * c + b * c)
        return M("Qual é a área total de um paralelepípedo de %d cm × %d cm × %d cm?" % (a, b, c), "%d cm²" % At, ["%d cm²" % (a * b * c), "%d cm²" % (At // 2), "%d cm²" % (2 * (a + b + c))], "2 · (%d · %d + %d · %d + %d · %d) = <b>%d cm²</b>." % (a, b, a, c, b, c, At))
    if k == "tri":
        a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13)])
        h = R.randint(4, 12)
        Al = (a + b + c) * h
        At = Al + a * b
        q = R.choice(["lat", "tot"])
        if q == "lat":
            return M("Um prisma tem como base um triângulo retângulo de lados %d, %d e %d cm e altura %d cm. Qual é a área lateral?" % (a, b, c, h), "%d cm²" % Al, ["%d cm²" % At, "%d cm²" % (a * b * h // 2), "%d cm²" % (c * h)], "Perímetro da base × altura = %d · %d = <b>%d cm²</b>." % (a + b + c, h, Al))
        return M("Um prisma tem como base um triângulo retângulo de lados %d, %d e %d cm e altura %d cm. Qual é a área total?" % (a, b, c, h), "%d cm²" % At, ["%d cm²" % Al, "%d cm²" % (Al + a * b // 2), "%d cm²" % (a * b * h // 2)],
                 "Lateral %d + 2 bases de %d = <b>%d cm²</b>." % (Al, a * b // 2, At))
    l = R.choice([2, 4, 6])
    h = R.randint(3, 10)
    return M("Um prisma hexagonal regular tem aresta da base %d cm e altura %d cm. Qual é a área lateral?" % (l, h), "%d cm²" % (6 * l * h), ["%d cm²" % (l * h), "%d cm²" % (6 * l + h), "%d cm²" % (12 * l * h)], "6 retângulos de %d × %d = <b>%d cm²</b>." % (l, h, 6 * l * h))


def s3_piramide():
    l, ap, h = R.choice([(6, 5, 4), (8, 5, 3), (10, 13, 12), (16, 10, 6), (12, 10, 8), (24, 13, 5), (14, 25, 24), (30, 17, 8)])
    k = R.choice(["vol", "lat", "tot", "ap", "h"])
    if k == "vol":
        V = F(l * l * h, 3)
        return M("Uma pirâmide quadrangular regular tem aresta da base %d cm e altura %d cm. Qual é o volume?" % (l, h), "%s cm³" % d(V), ["%d cm³" % (l * l * h), "%s cm³" % d(F(l * l * h, 2)), "%s cm³" % d(F(l * h, 3))],
                 "V = Ab · h ÷ 3 = %d · %d ÷ 3 = <b>%s cm³</b>." % (l * l, h, d(V)))
    if k == "lat":
        Al = 4 * F(l * ap, 2)
        return M("Uma pirâmide quadrangular regular tem aresta da base %d cm e apótema (altura de cada face) %d cm. Qual é a área lateral?" % (l, ap), "%s cm²" % d(Al), ["%s cm²" % d(4 * l * ap), "%s cm²" % d(Al + l * l), "%s cm²" % d(F(l * ap, 2))],
                 "4 triângulos: 4 · %d · %d ÷ 2 = <b>%s cm²</b>." % (l, ap, d(Al)))
    if k == "tot":
        At = 2 * l * ap + l * l
        return M("Uma pirâmide quadrangular regular tem aresta da base %d cm e apótema %d cm. Qual é a área total?" % (l, ap), "%d cm²" % At, ["%d cm²" % (2 * l * ap), "%d cm²" % (4 * l * ap + l * l), "%d cm²" % (At + l * l)],
                 "Lateral 2 · %d · %d = %d, mais a base %d²: <b>%d cm²</b>." % (l, ap, 2 * l * ap, l, At))
    if k == "ap":
        return M("Numa pirâmide quadrangular regular, a altura é %d cm e a aresta da base é %d cm. Quanto mede o apótema da pirâmide?" % (h, l), "%d cm" % ap, ["%d cm" % (h + l // 2), "%s cm" % sq(h * h + l * l), "%d cm" % (l // 2)],
                 "ap² = h² + (ℓ/2)² = %d + %d = %d ⇒ <b>%d cm</b>." % (h * h, (l // 2) ** 2, ap * ap, ap))
    return M("Numa pirâmide quadrangular regular, o apótema mede %d cm e a aresta da base, %d cm. Qual é a altura?" % (ap, l), "%d cm" % h, ["%d cm" % (ap - l // 2), "%s cm" % sq(ap * ap + (l // 2) ** 2), "%d cm" % ap],
             "h² = %d² − %d² = %d ⇒ <b>%d cm</b>." % (ap, l // 2, h * h, h))


s4_conceitos = bank(R, [
    ("O volume de uma pirâmide é ___ do volume do prisma de mesma base e mesma altura.", "1/3", ["1/2", "o dobro", "igual"]),
    ("A área lateral de um prisma é…", "o perímetro da base × a altura", ["a área da base × a altura", "a área da base × 2", "o volume ÷ altura"]),
    ("O apótema de uma pirâmide regular é…", "a altura de uma face lateral", ["a altura da pirâmide", "a aresta da base", "a diagonal da base"]),
    ("A diagonal de um cubo de aresta a é…", "a√3", ["a√2", "3a", "a²"]),
    ("Um prisma pentagonal tem quantas faces?", "7", ["5", "10", "15"]),
    ("Uma pirâmide hexagonal tem quantos vértices?", "7", ["6", "12", "13"]),
    ("Se a aresta de um cubo dobra, o volume fica…", "8 vezes maior", ["2 vezes maior", "4 vezes maior", "igual"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Diagonais e Euler", mix(R, seen, [(s1_diag, 12), (p_euler, 8)])),
        ("Área de prismas", mix(R, seen, [(s2_area_prisma, 20)])),
        ("Volume de prismas", mix(R, seen, [(v_paral, 10), (v_prisma, 10)])),
        ("Pirâmides", mix(R, seen, [(s3_piramide, 20)])),
        ("Revisão", mix(R, seen, [(s3_piramide, 7), (s2_area_prisma, 6), (s4_conceitos, 7)])),
    ]
    body = lesson(
        ["<b>Prisma</b>: duas bases iguais e paralelas, faces laterais retangulares. Área lateral = perímetro da base × altura; área total = lateral + 2 bases; volume = área da base × altura.",
         "Diagonal do paralelepípedo: D = √(a² + b² + c²). No cubo: D = a√3.",
         "<b>Pirâmide</b> regular: base regular e faces triangulares iguais. O apótema (altura da face) vem de Pitágoras: ap² = h² + (metade do lado)². Volume = área da base × altura ÷ 3.",
         "Relação de Euler para poliedros convexos: V − A + F = 2."],
        [("Pirâmide quadrangular: ℓ = 6, h = 4", ["ap = √(16 + 9) = 5", "Al = 4 · 6 · 5 ÷ 2 = 60", "V = 36 · 4 ÷ 3"], "Al = 60 cm², V = 48 cm³")],
        [["Esquecer o ÷ 3 na pirâmide", "A pirâmide é 1/3 do prisma de mesma base e altura."],
         ["Usar a altura na face lateral", "A área da face usa o apótema."],
         ["Contar uma base só", "O prisma tem duas bases."]])
    faq = [("Qual é a diferença entre altura e apótema da pirâmide?", "A altura vai do topo até o centro da base, por dentro. O apótema é a altura de uma face lateral. Eles se relacionam por Pitágoras: ap² = h² + (ℓ/2)²."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas que envolvem o cálculo de áreas totais e de volumes de prismas, pirâmides e corpos redondos em situações reais (como o cálculo do gasto de material para revestimento ou pinturas de objetos cujos formatos sejam composições dos sólidos estudados) (EM13MAT309).")]
    unit(R, "prismas-e-piramides", "M", ["EM13MAT309"],
         "Resolver e elaborar problemas que envolvem o cálculo de áreas totais e de volumes de prismas, pirâmides e corpos redondos em situações reais (como o cálculo do gasto de material para revestimento ou pinturas de objetos cujos formatos sejam composições dos sólidos estudados), com ou sem apoio de tecnologias digitais",
         "Prismas e pirâmides: áreas e volumes", "Prismas e pirâmides",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre prismas e pirâmides: diagonais, relação de Euler, área lateral e total, volume, apótema e altura da pirâmide. 100 exercícios com gabarito.",
         "Pirâmide: V = Ab · h ÷ 3", "Prisma: V = Ab · h.",
         body, faq, sets, 8, grade="2-serie")


if __name__ == "__main__":
    main()
