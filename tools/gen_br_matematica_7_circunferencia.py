# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Circunferência e seu comprimento (Geometria, EF07MA22; Grandezas e medidas, EF07MA33)
  python3 tools/gen_br_matematica_7_circunferencia.py
Elementos (centro, raio, diâmetro, corda, arco); circunferência como lugar dos pontos à mesma distância do centro; o número π como
comprimento ÷ diâmetro; comprimento C = 2πr = πd (π ≈ 3,14); voltas de rodas e pistas; achar o raio a partir do comprimento.
Erros: usar o diâmetro no lugar do raio em 2πr, confundir corda com raio, achar que π = 3 exatamente.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, bank, circulo, unit

R = random.Random(87015)
PI = F(314, 100)


def s1_elementos():
    k = R.choice(["raio", "diam", "corda"])
    if k == "raio":
        pic = circulo({"A": R.uniform(0, 360)}, [("O", "A")], label="circunferência com centro O e o segmento OA")
        return M(pic + "O segmento OA, que liga o centro a um ponto da circunferência, chama-se…", "raio", ["diâmetro", "corda", "arco"], "Do centro até a circunferência: <b>raio</b>.")
    if k == "diam":
        t = R.uniform(0, 180)
        pic = circulo({"A": t, "B": t + 180}, [("A", "B")], label="circunferência com o segmento AB passando pelo centro O")
        return M(pic + "O segmento AB passa pelo centro O. Ele se chama…", "diâmetro", ["raio", "arco", "tangente"], "Corda que passa pelo centro: <b>diâmetro</b> (o dobro do raio).")
    t = R.uniform(0, 360)
    pic = circulo({"A": t, "B": t + R.uniform(60, 140)}, [("A", "B")], label="circunferência com uma corda AB")
    return M(pic + "O segmento AB liga dois pontos da circunferência sem passar pelo centro. Ele se chama…", "corda", ["raio", "diâmetro", "arco"], "Segmento com as duas pontas na circunferência: <b>corda</b>.")


def s2_comprimento():
    r = R.randint(1, 30)
    k = R.choice(["r", "d", "pi"])
    if k == "r":
        C = 2 * PI * r
        return M("Qual é o comprimento de uma circunferência de raio %d cm? (Use π = 3,14.)" % r, "%s cm" % d(C), ["%s cm" % d(PI * r), "%s cm" % d(PI * r * r), "%s cm" % d(4 * PI * r)], "C = 2 · π · r = 2 · 3,14 · %d = <b>%s cm</b>." % (r, d(C)))
    if k == "d":
        C = PI * 2 * r
        return M("Qual é o comprimento de uma circunferência de diâmetro %d cm? (Use π = 3,14.)" % (2 * r), "%s cm" % d(C), ["%s cm" % d(2 * PI * 2 * r), "%s cm" % d(PI * r), "%s cm" % d(PI + 2 * r)], "C = π · d = 3,14 · %d = <b>%s cm</b>." % (2 * r, d(C)))
    return M("Qual é o comprimento de uma circunferência de raio %d cm? (Deixe a resposta com π.)" % r, "%dπ cm" % (2 * r), ["%dπ cm" % r, "%dπ cm" % (r * r), "%dπ cm" % (4 * r)], "C = 2πr = <b>%dπ cm</b>." % (2 * r))


def s3_inverso():
    r = R.choice([5, 10, 15, 20, 25, 50])
    C = 2 * PI * r
    k = R.choice(["r", "d"])
    if k == "r":
        return M("Uma circunferência tem comprimento %s cm. Qual é o raio? (π = 3,14)" % d(C), "%d cm" % r, ["%d cm" % (2 * r), "%s cm" % d(C / PI), "%d cm" % (r + 5)], "r = C ÷ (2π) = %s ÷ 6,28 = <b>%d cm</b>." % (d(C), r))
    return M("Uma circunferência tem comprimento %s cm. Qual é o diâmetro? (π = 3,14)" % d(C), "%d cm" % (2 * r), ["%d cm" % r, "%d cm" % (4 * r), "%s cm" % d(C / 2)], "d = C ÷ π = %s ÷ 3,14 = <b>%d cm</b>." % (d(C), 2 * r))


def s4_problemas():
    k = R.choice(["roda", "pista", "voltas", "medir"])
    if k == "roda":
        r, v = R.choice([30, 35, 40, 50]), R.choice([10, 50, 100, 500])
        dist = 2 * PI * r * v
        return M("A roda de uma bicicleta tem raio %d cm. Quantos metros a bicicleta anda quando a roda dá %d voltas? (π = 3,14)" % (r, v), "%s m" % d(dist / 100), ["%s m" % d(PI * r * v / 100), "%s m" % d(dist), "%s m" % d(dist / 1000)],
                 "1 volta: 2 · 3,14 · %d = %s cm; × %d = %s cm = <b>%s m</b>." % (r, d(2 * PI * r), v, d(dist), d(dist / 100)))
    if k == "pista":
        r, n = R.choice([10, 20, 25, 50]), R.randint(2, 10)
        dist = 2 * PI * r * n
        return M("Uma pista circular tem raio %d m. Quantos metros corre quem dá %d voltas? (π = 3,14)" % (r, n), "%s m" % d(dist), ["%s m" % d(PI * r * n), "%s m" % d(2 * PI * r), "%s m" % d(PI * r * r * n)],
                 "1 volta: %s m; × %d = <b>%s m</b>." % (d(2 * PI * r), n, d(dist)))
    if k == "voltas":
        r = R.choice([25, 50])
        dist = R.choice([157, 314, 628, 1570])
        v = F(dist * 100, 2 * PI * r)
        if v.denominator != 1:
            return None
        return M("Uma roda de raio %d cm percorreu %s m. Quantas voltas deu? (π = 3,14)" % (r, d(dist)), d(v), [d(v * 2), d(v / 2), d(v * 10)], "1 volta = %s cm; %s cm ÷ %s = <b>%s voltas</b>." % (d(2 * PI * r), d(dist * 100), d(2 * PI * r), d(v)))
    dm = R.choice([7, 10, 14, 20, 21])
    C = F(22, 7) * dm
    return M("Ana mediu com um barbante o contorno de um prato: %s cm. O diâmetro do prato é %d cm. Quanto dá o contorno dividido pelo diâmetro (aproximado)?" % (d(C, 1), dm), "cerca de 3,14 (o número π)", ["cerca de 2", "cerca de 6,28", "exatamente 3"],
             "C ÷ d ≈ %s ÷ %d ≈ 3,14: é o número <b>π</b>." % (d(C, 1), dm))


s5_conceitos = bank(R, [
    ("Todos os pontos de uma circunferência estão…", "à mesma distância do centro", ["à mesma distância de um diâmetro", "dentro do círculo", "sobre o raio"]),
    ("O diâmetro de uma circunferência é…", "o dobro do raio", ["a metade do raio", "igual ao raio", "o comprimento dela"]),
    ("A maior corda de uma circunferência é…", "o diâmetro", ["o raio", "um arco", "qualquer corda"]),
    ("O número π é o resultado de…", "comprimento da circunferência ÷ diâmetro", ["raio ÷ diâmetro", "diâmetro ÷ raio", "área ÷ raio"]),
    ("O valor de π é aproximadamente…", "3,14", ["3", "2,14", "6,28"]),
    ("Qual é a diferença entre circunferência e círculo?", "circunferência é a linha; círculo é a região com o interior", ["não há diferença", "círculo é a linha; circunferência é a região", "circunferência é só metade"]),
    ("Se o raio dobra, o comprimento da circunferência…", "dobra", ["quadruplica", "não muda", "fica pela metade"]),
    ("Com um compasso aberto 5 cm, desenhamos uma circunferência de…", "raio 5 cm", ["diâmetro 5 cm", "comprimento 5 cm", "raio 10 cm"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Elementos da circunferência", mix(R, seen, [(s1_elementos, 12), (s5_conceitos, 8)])),
        ("Comprimento da circunferência", mix(R, seen, [(s2_comprimento, 20)])),
        ("Achar o raio e o diâmetro", mix(R, seen, [(s3_inverso, 12), (s2_comprimento, 8)])),
        ("Rodas e pistas", mix(R, seen, [(s4_problemas, 20)])),
        ("Revisão", mix(R, seen, [(s2_comprimento, 10), (s4_problemas, 10)])),
    ]
    body = lesson(
        ["A <b>circunferência</b> é a linha formada pelos pontos que estão à mesma distância (o <b>raio</b>) de um ponto (o <b>centro</b>). O <b>diâmetro</b> é o dobro do raio.",
         "Dividindo o comprimento de qualquer circunferência pelo seu diâmetro, sempre obtemos o mesmo número: <b>π ≈ 3,14</b>.",
         "Comprimento: <b>C = 2πr</b> (ou C = πd). Uma volta de uma roda anda exatamente esse comprimento."],
        [("Raio 10 cm", ["C = 2 · 3,14 · 10"], "62,8 cm"),
         ("C = 31,4 m", ["d = 31,4 ÷ 3,14"], "d = 10 m")],
        [["Usar o diâmetro em 2πr", "Em 2πr, use o raio; com o diâmetro, use πd."],
         ["Confundir corda e raio", "O raio sai do centro."],
         ["Achar que π = 3", "π ≈ 3,14159…"]],
        circulo({"A": 30, "B": 210}, [("A", "B"), ("O", "A")]))
    faq = [("Como calcular o comprimento de uma circunferência?", "Multiplique o diâmetro por π (≈ 3,14), ou multiplique 2 · π pelo raio: C = 2πr."),
           ("O que a BNCC pede no 7º ano?", "Construir circunferências, utilizando compasso, reconhecê-las como lugar geométrico (EF07MA22) e estabelecer o número π como a razão entre a medida de uma circunferência e seu diâmetro, para compreender e resolver problemas (EF07MA33).")]
    unit(R, "circunferencia-e-comprimento", "G", ["EF07MA22", "EF07MA33"],
         "Construir circunferências, utilizando compasso, reconhecê-las como lugar geométrico e utilizá-las para fazer composições artísticas e resolver problemas que envolvam objetos equidistantes; estabelecer o número π como a razão entre a medida de uma circunferência e seu diâmetro, para compreender e resolver problemas, inclusive os de natureza histórica",
         "Circunferência: elementos e comprimento", "Circunferência",
         "Atividades de matemática para o 7º ano sobre a circunferência: centro, raio, diâmetro e corda, o número π, comprimento da circunferência, raio a partir do comprimento e problemas com rodas e pistas. 100 exercícios com gabarito.",
         "C = 2πr", "π ≈ 3,14 = comprimento ÷ diâmetro",
         body, faq, sets, 15, grade="7-ano")


if __name__ == "__main__":
    main()
