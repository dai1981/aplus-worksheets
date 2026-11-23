# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Notação científica (Números, EF09MA04)
  python3 tools/gen_br_matematica_9_notacao_cientifica.py
Escrever números muito grandes e muito pequenos na forma a × 10ⁿ (1 ≤ a &lt; 10); voltar para a forma decimal; comparar;
multiplicar e dividir; problemas com distâncias, populações e tamanhos microscópicos.
Erros: deixar a fora do intervalo (25 × 10³), errar o sinal do expoente para números pequenos, somar os expoentes na divisão.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, unit

R = random.Random(89003)
SUP = str.maketrans("0123456789−", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def nc(a, e):
    return "%s × 10%s" % (d(a), (("−%d" % -e) if e < 0 else str(e)).translate(SUP))


def mant():
    k = R.choice([1, 2])
    a = F(R.randint(11, 99), 10) if k == 1 else F(R.randint(101, 999), 100)
    if a.denominator == 1:
        return None
    return a


def s1_grande():
    a = mant()
    if not a:
        return None
    e = R.randint(4, 9)
    n = a * 10 ** e
    return M("Escreva em notação científica: %s" % d(n), nc(a, e), [nc(a * 10, e - 1), nc(a, e + 1), nc(a, e - 1)],
             "A vírgula anda %d casas para a esquerda até ficar um só algarismo antes dela: <b>%s</b>." % (e, nc(a, e)))


def s1_pequeno():
    a = mant()
    if not a:
        return None
    e = -R.randint(2, 7)
    n = a * F(10) ** e
    return M("Escreva em notação científica: %s" % d(n), nc(a, e), [nc(a, -e), nc(a, e + 1), nc(a, e - 1)],
             "A vírgula anda %d casas para a direita; número pequeno tem expoente negativo: <b>%s</b>." % (-e, nc(a, e)))


def s2_voltar():
    a = mant()
    if not a:
        return None
    e = R.choice([R.randint(3, 7), -R.randint(2, 5)])
    n = a * F(10) ** e
    return M("Escreva na forma decimal: %s" % nc(a, e), d(n), [d(a * F(10) ** (e + 1)), d(a * F(10) ** (e - 1)), d(a * F(10) ** (-e))],
             "Ande com a vírgula %d casas para a %s: <b>%s</b>." % (abs(e), "direita" if e > 0 else "esquerda", d(n)))


def s2_certo():
    a = mant()
    if not a:
        return None
    e = R.randint(3, 8)
    ok = nc(a, e)
    return M("Qual destas é a notação científica correta de %s?" % d(a * 10 ** e), ok, ["%s × 10%s" % (d(a * 10), str(e - 1).translate(SUP)), "%s × 10%s" % (d(a / 10), str(e + 1).translate(SUP)), "%s × 10%s" % (d(a * 100), str(e - 2).translate(SUP))],
             "O número da frente precisa ficar entre 1 e 10: <b>%s</b>." % ok)


def s3_comparar():
    a, b = mant(), mant()
    if not a or not b:
        return None
    e1, e2 = R.randint(3, 9), R.randint(3, 9)
    if e1 == e2 and a == b:
        return None
    x, y = a * F(10) ** e1, b * F(10) ** e2
    big = nc(a, e1) if x > y else nc(b, e2)
    return M("Qual é maior: %s ou %s?" % (nc(a, e1), nc(b, e2)), big, [nc(b, e2) if x > y else nc(a, e1), "são iguais", "não dá para comparar"],
             ("Compare os expoentes: 10%s é maior" % str(max(e1, e2)).translate(SUP) if e1 != e2 else "Expoentes iguais: compare os números da frente") + ". Maior: <b>%s</b>." % big)


def s4_operar():
    a, b = R.randint(2, 4), R.randint(2, 3)
    e1, e2 = R.randint(2, 8), R.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])
    if e1 == e2 or e1 + e2 == 0:
        return None
    if R.random() < 0.5:
        p = a * b
        e = e1 + e2
        if p >= 10:
            return None
        return M("Calcule: (%s) · (%s)" % (nc(a, e1), nc(b, e2)), nc(p, e), [nc(p, e1 * e2), nc(a + b, e), nc(p, e1 - e2), nc(p, e + 1), nc(p, e - 1)],
                 "%d · %d = %d e some os expoentes: %d + (%d) = %d. Resposta: <b>%s</b>." % (a, b, p, e1, e2, e, nc(p, e)))
    p = a * b
    e = e1 - e2
    return M("Calcule: (%s) ÷ (%s)" % (nc(p, e1), nc(b, e2)), nc(a, e), [nc(a, e1 + e2), nc(p - b, e), nc(a, e2 - e1), nc(a, e + 1), nc(a, e - 1)],
             "%d ÷ %d = %d e subtraia os expoentes: %d − (%d) = %d. Resposta: <b>%s</b>." % (p, b, a, e1, e2, e, nc(a, e)))


CTX = [("A distância da Terra ao Sol é de cerca de 150.000.000 km. Em notação científica:", nc(F(15, 10), 8), [nc(15, 7), nc(F(15, 10), 7), nc(F(15, 10), 9)]),
       ("A população do Brasil é de cerca de 213.000.000 pessoas. Em notação científica:", nc(F(213, 100), 8), [nc(213, 6), nc(F(213, 100), 6), nc(F(213, 100), 9)]),
       ("A espessura de um fio de cabelo é de cerca de 0,00007 m. Em notação científica:", nc(7, -5), [nc(7, 5), nc(7, -4), nc(7, -6)]),
       ("Uma bactéria mede cerca de 0,000002 m. Em notação científica:", nc(2, -6), [nc(2, 6), nc(2, -5), nc(2, -7)]),
       ("A velocidade da luz é de cerca de 300.000 km/s. Em notação científica:", nc(3, 5), [nc(3, 4), nc(30, 4), nc(3, 6)]),
       ("A massa de um grão de areia é de cerca de 0,0006 g. Em notação científica:", nc(6, -4), [nc(6, 4), nc(6, -3), nc(6, -5)]),
       ("O diâmetro da Terra é de cerca de 12.700 km. Em notação científica:", nc(F(127, 100), 4), [nc(127, 2), nc(F(127, 100), 3), nc(F(127, 100), 5)]),
       ("Um vírus mede cerca de 0,0000001 m. Em notação científica:", nc(1, -7), [nc(1, 7), nc(1, -6), nc(1, -8)])]


def s5_ctx():
    q, a, w = R.choice(CTX)
    return M(q, a, w, "Um só algarismo antes da vírgula e a potência de 10 certa: <b>%s</b>." % a)


def s5_problema():
    a = R.randint(2, 9)
    n = R.randint(2, 5)
    return M("Um computador faz %s operações por segundo. Quantas operações faz em %d segundos?" % (nc(a, 9), n) if a * n < 10 else
             "Uma célula mede %s m. Quanto medem %d células em fila?" % (nc(a, -5), n),
             nc(a * n, 9) if a * n < 10 else nc(F(a * n, 10), -4), [nc(a * n, 9 * n) if a * n < 10 else nc(a * n, -5 * n), nc(a + n, 9) if a * n < 10 else nc(a * n, -6), nc(a * n, 10) if a * n < 10 else nc(F(a * n, 10), -5)],
             "Multiplique o número da frente por %d e ajuste: <b>%s</b>." % (n, nc(a * n, 9) if a * n < 10 else nc(F(a * n, 10), -4)))


def main():
    seen = set()
    sets = [
        ("Números muito grandes", mix(R, seen, [(s1_grande, 14), (s2_certo, 6)])),
        ("Números muito pequenos", mix(R, seen, [(s1_pequeno, 20)])),
        ("Da notação científica para o decimal", mix(R, seen, [(s2_voltar, 14), (s3_comparar, 6)])),
        ("Comparar, multiplicar e dividir", mix(R, seen, [(s3_comparar, 8), (s4_operar, 12)])),
        ("Problemas", mix(R, seen, [(s5_ctx, 8), (s5_problema, 12)])),
    ]
    body = lesson(
        ["Na <b>notação científica</b>, escrevemos a × 10ⁿ com <b>1 ≤ a &lt; 10</b>: 45.000 = 4,5 × 10⁴.",
         "Para números pequenos, o expoente é <b>negativo</b>: 0,0032 = 3,2 × 10⁻³.",
         "O expoente diz quantas casas a vírgula andou: para a esquerda (número grande) ou para a direita (número pequeno).",
         "Na multiplicação, multiplique os números da frente e <b>some</b> os expoentes; na divisão, divida e <b>subtraia</b>."],
        [("82.000.000", ["8,2 com a vírgula 7 casas à esquerda"], "8,2 × 10⁷"),
         ("(3 × 10⁴) · (2 × 10³)", ["3 · 2 = 6", "4 + 3 = 7"], "6 × 10⁷")],
        [["Deixar a fora do intervalo (25 × 10³)", "Use 2,5 × 10⁴."],
         ["Usar expoente positivo para número pequeno", "0,004 = 4 × 10⁻³."],
         ["Somar os expoentes na divisão", "Na divisão, subtraia."]],
        "<p>45.000 = 4,5 × 10⁴; 0,0032 = 3,2 × 10⁻³</p>")
    faq = [("Para que serve a notação científica?", "Para escrever e calcular com números muito grandes (distâncias no espaço, populações) ou muito pequenos (células, vírus) de forma curta. A BNCC pede resolver problemas com números reais em notação científica."),
           ("Como saber o expoente?", "Conte quantas casas a vírgula andou para deixar um só algarismo diferente de zero antes dela. Para a esquerda, o expoente é positivo; para a direita, negativo.")]
    unit(R, "notacao-cientifica", "N", ["EF09MA04"],
         "Resolver e elaborar problemas com números reais, inclusive em notação científica, envolvendo diferentes operações",
         "Notação científica: números muito grandes e muito pequenos", "Notação científica",
         "Atividades de matemática para o 9º ano sobre notação científica: escrever números grandes e pequenos, voltar para o decimal, comparar, multiplicar, dividir e problemas. 100 exercícios com gabarito.",
         "a × 10ⁿ com 1 ≤ a < 10.", "Número pequeno: expoente negativo.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
