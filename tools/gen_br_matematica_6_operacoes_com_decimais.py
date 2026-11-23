# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Operações com números decimais (Números, EF06MA11)
  python3 tools/gen_br_matematica_6_operacoes_com_decimais.py
Adição e subtração (vírgula embaixo de vírgula); multiplicação e divisão por 10, 100 e 1.000; multiplicação de decimais
(soma das casas); divisão de decimal por natural e de natural por natural com quociente decimal; problemas com dinheiro e medidas.
Erros: alinhar pela direita em vez de pela vírgula, contar errado as casas no produto, esquecer o zero em 0,05 × 10.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, unit

R = random.Random(86008)


def dec(p, hi=50):
    return F(R.randint(1, hi * 10 ** p), 10 ** p)


def s1_addsub():
    a, b = dec(R.choice([1, 2, 3])), dec(R.choice([1, 2]))
    if R.random() < 0.5:
        r = a + b
        bad = F(int(a * 1000) + int(b * 1000 * (10 if (b * 100).denominator == 1 and (a * 100).denominator != 1 else 1)), 1000)
        return M("Quanto é %s + %s?" % (d(a), d(b)), d(r), [d(bad) if bad != r else d(r + F(1, 10)), d(r + 1), d(r - F(1, 10))], "Vírgula embaixo de vírgula: %s + %s = <b>%s</b>." % (d(a), d(b), d(r)))
    if a < b:
        a, b = b, a
    r = a - b
    if r == 0:
        return None
    return M("Quanto é %s − %s?" % (d(a), d(b)), d(r), [d(a + b), d(r + F(1, 10)), d(abs(r - 1))], "Complete com zeros e alinhe as vírgulas: %s − %s = <b>%s</b>." % (d(a), d(b), d(r)))


def s2_potencias():
    x = dec(R.choice([1, 2, 3]), 30)
    p = R.choice([10, 100, 1000])
    if R.random() < 0.5:
        return M("Quanto é %s × %s?" % (d(x), d(p)), d(x * p), [d(x * p / 10), d(x * p * 10), d(x / p, 6)], "Multiplicar por %s: a vírgula anda %d casa%s para a direita: <b>%s</b>." % (d(p), len(str(p)) - 1, "" if p == 10 else "s", d(x * p)))
    return M("Quanto é %s ÷ %s?" % (d(x), d(p)), d(x / p, 6), [d(x / p * 10, 6), d(x * p), d(x / p / 10, 7)], "Dividir por %s: a vírgula anda %d casa%s para a esquerda: <b>%s</b>." % (d(p), len(str(p)) - 1, "" if p == 10 else "s", d(x / p, 6)))


def s3_mult():
    a = F(R.randint(2, 99), R.choice([10, 100]))
    b = F(R.randint(2, 49), R.choice([1, 10, 10, 100]))
    if a.denominator == 1 and b.denominator == 1:
        return None
    r = a * b
    return M("Quanto é %s × %s?" % (d(a), d(b)), d(r), [d(r * 10), d(r / 10, 6), d(r + 1)], "Multiplique sem vírgula e dê ao resultado tantas casas quanto as dos dois fatores juntos: <b>%s</b>." % d(r))


def s4_div():
    k = R.choice(["dn", "nn"])
    if k == "dn":
        b = R.randint(2, 9)
        q = F(R.randint(11, 999), R.choice([10, 100]))
        a = q * b
        return M("Quanto é %s ÷ %d?" % (d(a), b), d(q), [d(q * 10), d(q / 10, 5), d(q + F(1, 10))], "%d × %s = %s, então %s ÷ %d = <b>%s</b>." % (b, d(q), d(a), d(a), b, d(q)))
    b = R.choice([2, 4, 5, 8, 20, 25])
    a = R.randint(1, 60)
    if a % b == 0:
        return None
    q = F(a, b)
    return M("Quanto é %d ÷ %d (com quociente decimal)?" % (a, b), d(q), ["%d,%d" % divmod(a, b), d(q * 10), d(q + 1)], "Continue a divisão acrescentando zeros ao resto: %d ÷ %d = <b>%s</b>." % (a, b, d(q)))


def s5_problemas():
    k = R.choice(["troco", "kg", "parcela", "combustivel", "tecido", "media"])
    if k == "troco":
        ps = [R.randint(150, 2990) for _ in range(3)]
        tot = sum(ps)
        n = R.choice([5000, 10000, 20000])
        if tot >= n:
            return None
        return M("Comprei itens de %s, %s e %s e paguei com %s. Qual foi o troco?" % (reais(ps[0]), reais(ps[1]), reais(ps[2]), reais(n)), reais(n - tot), [reais(tot), reais(n - tot + 100), reais(n - tot - 10)],
                 "Total %s; troco %s − %s = <b>%s</b>." % (reais(tot), reais(n), reais(tot), reais(n - tot)))
    if k == "kg":
        p, q = R.randint(399, 4999), F(R.randint(5, 35), 10)
        v = p * q
        if v.denominator != 1:
            return None
        return M("O quilo do queijo custa %s. Quanto custam %s kg?" % (reais(p), d(q)), reais(int(v)), [reais(int(v) * 10), reais(int(v / 10)), reais(p + int(q * 100))], "%s × %s = <b>%s</b>." % (reais(p), d(q), reais(int(v))))
    if k == "parcela":
        n = R.choice([4, 5, 8, 10, 12])
        v = R.randint(1000, 9999) * n
        return M("Um celular de %s foi dividido em %d parcelas iguais sem juros. Qual é o valor de cada parcela?" % (reais(v), n), reais(v // n), [reais(v // n * 10), reais(v // n + 100), reais(v // (n + 1)) if v % (n + 1) == 0 else reais(v // n - 50)],
                 "%s ÷ %d = <b>%s</b>." % (reais(v), n, reais(v // n)))
    if k == "combustivel":
        p, L = R.randint(549, 699), R.randint(10, 45)
        return M("O litro da gasolina custa %s. Quanto se paga por %d litros?" % (reais(p), L), reais(p * L), [reais(p * L // 10), reais(p + L * 100), reais(p * (L - 1))], "%s × %d = <b>%s</b>." % (reais(p), L, reais(p * L)))
    if k == "tecido":
        t = F(R.randint(30, 99), 10)
        n = R.randint(2, 6)
        p = F(R.randint(5, 15), 10)
        if n * p >= t:
            return None
        return M("Uma costureira tinha %s m de tecido e usou %d pedaços de %s m. Quanto sobrou?" % (d(t), n, d(p)), "%s m" % d(t - n * p), ["%s m" % d(t - p), "%s m" % d(n * p), "%s m" % d(t - n * p + F(1, 10))],
                 "%d × %s = %s; %s − %s = <b>%s m</b>." % (n, d(p), d(n * p), d(t), d(n * p), d(t - n * p)))
    xs = [F(R.randint(50, 100), 10) for _ in range(4)]
    m = sum(xs) / 4
    if (m * 100).denominator != 1:
        return None
    return M("As notas de Ana foram %s. Qual é a média?" % "; ".join(d(x) for x in xs), d(m), [d(sum(xs)), d(m + F(1, 2)), d(max(xs))], "(%s) ÷ 4 = %s ÷ 4 = <b>%s</b>." % (" + ".join(d(x) for x in xs), d(sum(xs)), d(m)))


def main():
    seen = set()
    sets = [
        ("Adição e subtração", mix(R, seen, [(s1_addsub, 20)])),
        ("Por 10, 100 e 1.000", mix(R, seen, [(s2_potencias, 20)])),
        ("Multiplicação", mix(R, seen, [(s3_mult, 20)])),
        ("Divisão", mix(R, seen, [(s4_div, 20)])),
        ("Problemas com dinheiro e medidas", mix(R, seen, [(s5_problemas, 20)])),
    ]
    body = lesson(
        ["Na adição e na subtração, coloque <b>vírgula embaixo de vírgula</b> e complete as casas vazias com zeros.",
         "Multiplicar por 10, 100 ou 1.000 desloca a vírgula 1, 2 ou 3 casas para a direita; dividir, para a esquerda.",
         "Na multiplicação, conte as casas decimais dos dois fatores: o produto tem a soma delas (1,2 × 0,3 = 0,36).",
         "Na divisão, quando sobra resto, coloque a vírgula no quociente e continue acrescentando zeros."],
        [("12,5 + 3,47", ["12,50 + 3,47"], "15,97"),
         ("2,4 × 0,15", ["24 × 15 = 360", "1 + 2 = 3 casas"], "0,360 = 0,36")],
        [["Alinhar pela direita", "Alinhe pela vírgula."],
         ["Contar errado as casas no produto", "Some as casas dos dois fatores."],
         ["Perder o zero", "0,05 × 10 = 0,5."]])
    faq = [("Como multiplicar números decimais?", "Multiplique como se não houvesse vírgula. Depois conte quantas casas decimais têm os dois fatores juntos e coloque a vírgula no produto com esse número de casas."),
           ("O que a BNCC pede no 6º ano?", "Resolver e elaborar problemas com números racionais positivos na representação decimal, envolvendo as quatro operações fundamentais e a potenciação, por meio de estratégias diversas (EF06MA11).")]
    unit(R, "operacoes-com-decimais", "N", ["EF06MA11"],
         "Resolver e elaborar problemas com números racionais positivos na representação decimal, envolvendo as quatro operações fundamentais e a potenciação, por meio de estratégias diversas, utilizando estimativas e arredondamentos para verificar a razoabilidade de respostas, com e sem uso de calculadora",
         "Operações com números decimais", "Operações com decimais",
         "Atividades de matemática para o 6º ano sobre operações com números decimais: adição, subtração, multiplicação e divisão, por 10, 100 e 1.000, e problemas com dinheiro e medidas. 100 exercícios com gabarito.",
         "Vírgula embaixo de vírgula.", "No produto, some as casas decimais dos fatores.",
         body, faq, sets, 8, grade="6-ano")


if __name__ == "__main__":
    main()
