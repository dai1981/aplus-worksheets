# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: MMC e MDC (Números, EF06MA06)
  python3 tools/gen_br_matematica_6_mmc_e_mdc.py
Mínimo múltiplo comum e máximo divisor comum: listas de múltiplos e divisores, decomposição simultânea; números primos entre si;
problemas (encontros periódicos, cortar em pedaços iguais, formar grupos).
Erros: trocar MMC por MDC nos problemas, multiplicar os números em vez de achar o MMC, esquecer de usar só os fatores comuns no MDC.
"""
import random
from math import gcd
from br_common import lesson, mix
from br_9 import M, d, bank, unit

R = random.Random(86004)


def lcm(a, b):
    return a * b // gcd(a, b)


def pair():
    while True:
        a, b = R.sample(range(4, 61), 2)
        if gcd(a, b) > 1 and lcm(a, b) <= 400 and lcm(a, b) not in (a, b):
            return a, b


def s1_mmc():
    a, b = pair()
    m = lcm(a, b)
    return M("Qual é o MMC de %d e %d?" % (a, b), d(m), [d(a * b), d(gcd(a, b)), d(m * 2)],
             "Múltiplos de %d: %s… e de %d: %s… O menor comum é <b>%d</b>." % (a, ", ".join(str(a * i) for i in range(1, 5)), b, ", ".join(str(b * i) for i in range(1, 5)), m))


def s2_mdc():
    a, b = pair()
    g = gcd(a, b)
    return M("Qual é o MDC de %d e %d?" % (a, b), d(g), [d(lcm(a, b)), "1" if g != 1 else "2", d(g * 2) if a % (g * 2) or b % (g * 2) else d(g + 1), d(min(a, b))],
             "Divisores comuns de %d e %d: %s. O maior é <b>%d</b>." % (a, b, ", ".join(str(k) for k in range(1, g + 1) if a % k == 0 and b % k == 0), g))


def s3_tres():
    a, b, c = R.choice([(4, 6, 8), (6, 8, 12), (3, 4, 6), (10, 12, 15), (6, 9, 12), (12, 18, 24), (8, 12, 20), (5, 10, 15), (9, 12, 18), (4, 10, 15), (2, 3, 5), (6, 10, 15)])
    k = R.choice(["mmc", "mdc"])
    m = lcm(lcm(a, b), c)
    g = gcd(gcd(a, b), c)
    if k == "mmc":
        return M("Qual é o MMC de %d, %d e %d?" % (a, b, c), d(m), [d(a * b * c), d(g), d(m * 2)], "Decomposição simultânea: o menor múltiplo comum é <b>%d</b>." % m)
    return M("Qual é o MDC de %d, %d e %d?" % (a, b, c), d(g), [d(m), d(min(a, b, c)), d(g + 1) if g > 1 else "2"], "O maior número que divide os três é <b>%d</b>." % g)


def s4_primos_entre_si():
    a, b = R.sample(range(4, 40), 2)
    g = gcd(a, b)
    ans = "sim, MDC = 1" if g == 1 else "não, MDC = %d" % g
    return M("Os números %d e %d são primos entre si?" % (a, b), ans, ["sim, MDC = 1" if g != 1 else "não, MDC = 2", "só se os dois forem primos", "não, porque um deles é par" if g == 1 else "sim, porque são diferentes"],
             "Primos entre si têm MDC igual a 1. Aqui o MDC é %d: <b>%s</b>." % (g, ans))


def s5_problemas():
    k = R.choice(["onibus", "remedio", "fitas", "kits", "pisca", "corrida"])
    if k == "onibus":
        a, b = R.choice([(12, 18), (15, 20), (10, 25), (20, 30), (16, 24), (18, 30)])
        h = R.choice([6, 7, 8])
        m = lcm(a, b)
        return M("Um ônibus da linha A passa a cada %d minutos e um da linha B a cada %d minutos. Os dois passaram juntos às %dh. Depois de quantos minutos passarão juntos de novo?" % (a, b, h), "%d minutos" % m, ["%d minutos" % (a * b), "%d minutos" % gcd(a, b), "%d minutos" % (a + b)],
                 "É o MMC de %d e %d: <b>%d minutos</b>." % (a, b, m))
    if k == "remedio":
        a, b = R.choice([(4, 6), (6, 8), (8, 12), (4, 10), (6, 9)])
        m = lcm(a, b)
        return M("Um paciente toma um remédio a cada %d horas e outro a cada %d horas. Tomou os dois juntos agora. Daqui a quantas horas tomará os dois juntos de novo?" % (a, b), "%d horas" % m, ["%d horas" % (a * b) if a * b != m else "%d horas" % (m * 2), "%d horas" % gcd(a, b), "%d horas" % (a + b)],
                 "MMC(%d, %d) = <b>%d horas</b>." % (a, b, m))
    if k == "fitas":
        a, b = R.choice([(48, 72), (60, 84), (90, 120), (36, 60), (54, 90), (80, 120)])
        g = gcd(a, b)
        return M("Duas fitas medem %d cm e %d cm. Quero cortá-las em pedaços iguais, os maiores possíveis, sem sobras. Quanto medirá cada pedaço?" % (a, b), "%d cm" % g, ["%d cm" % lcm(a, b), "%d cm" % (g // 2), "%d cm" % (b - a)],
                 "É o MDC de %d e %d: <b>%d cm</b>." % (a, b, g))
    if k == "kits":
        a, b = R.choice([(24, 36), (30, 45), (40, 56), (36, 48), (42, 70), (60, 90)])
        g = gcd(a, b)
        return M("Uma professora tem %d lápis e %d borrachas e quer montar o maior número possível de kits iguais, sem sobrar nada. Quantos kits ela monta?" % (a, b), d(g), [d(lcm(a, b)), d(g // 2), d(a + b)],
                 "MDC(%d, %d) = <b>%d kits</b>, cada um com %d lápis e %d borrachas." % (a, b, g, a // g, b // g))
    if k == "pisca":
        a, b = R.choice([(3, 5), (4, 6), (6, 10), (8, 12), (5, 8)])
        m = lcm(a, b)
        return M("Uma luz pisca a cada %d segundos e outra a cada %d segundos. Piscaram juntas agora. Em quantos segundos piscarão juntas de novo?" % (a, b), "%d segundos" % m, ["%d segundos" % gcd(a, b), "%d segundos" % (a + b), "%d segundos" % (m * 2)],
                 "MMC(%d, %d) = <b>%d s</b>." % (a, b, m))
    a, b = R.choice([(6, 8), (9, 12), (10, 15), (8, 10)])
    m = lcm(a, b)
    return M("Num circuito, Ana dá uma volta a cada %d minutos e Bia a cada %d minutos. Partiram juntas. Quantas voltas Ana terá dado quando se encontrarem de novo na largada?" % (a, b), d(m // a), [d(m // b), d(m), d(b)],
             "Encontram-se depois de MMC(%d, %d) = %d minutos; Ana deu %d ÷ %d = <b>%d voltas</b>." % (a, b, m, m, a, m // a))


s6_conceitos = bank(R, [
    ("Para saber quando dois eventos que se repetem acontecem juntos de novo, usamos o…", "MMC", ["MDC", "produto sempre", "a diferença"]),
    ("Para dividir duas quantidades em grupos iguais, os maiores possíveis, usamos o…", "MDC", ["MMC", "a soma", "o quociente"]),
    ("Se a é múltiplo de b, então o MMC de a e b é…", "a", ["b", "a × b", "1"]),
    ("Se a é múltiplo de b, então o MDC de a e b é…", "b", ["a", "a × b", "1"]),
    ("Se dois números são primos entre si, o MMC deles é…", "o produto dos dois", ["1", "a soma dos dois", "o maior deles"]),
    ("Qual é sempre verdade para dois números naturais a e b?", "MDC × MMC = a × b", ["MDC + MMC = a + b", "MDC = MMC", "MMC &lt; MDC"]),
    ("O MDC de dois números diferentes é sempre…", "menor ou igual ao menor deles", ["maior que os dois", "igual ao produto", "um número primo"]),
    ("O MMC de dois números é sempre…", "maior ou igual ao maior deles", ["menor que os dois", "igual à soma", "um número primo"]),
], "s6_conceitos")


def main():
    seen = set()
    sets = [
        ("MMC de dois números", mix(R, seen, [(s1_mmc, 20)])),
        ("MDC de dois números", mix(R, seen, [(s2_mdc, 20)])),
        ("Três números e primos entre si", mix(R, seen, [(s3_tres, 12), (s4_primos_entre_si, 8)])),
        ("MMC ou MDC?", mix(R, seen, [(s6_conceitos, 8), (s5_problemas, 12)])),
        ("Problemas", mix(R, seen, [(s5_problemas, 20)])),
    ]
    body = lesson(
        ["O <b>MMC</b> (mínimo múltiplo comum) é o menor número, diferente de zero, que é múltiplo de todos. Use quando algo <b>se repete</b> e você quer saber quando coincide.",
         "O <b>MDC</b> (máximo divisor comum) é o maior número que divide todos. Use quando quer <b>dividir em partes iguais</b>, as maiores possíveis.",
         "Pela decomposição: MMC usa todos os fatores primos com o maior expoente; MDC usa só os fatores comuns com o menor expoente."],
        [("12 = 2² × 3 e 18 = 2 × 3²", ["MMC: 2² × 3² = 36", "MDC: 2 × 3 = 6"], "MMC 36 e MDC 6"),
         ("Ônibus a cada 12 e 18 min", ["MMC(12, 18)"], "juntos de novo em 36 min")],
        [["Trocar MMC por MDC", "Repetição → MMC; repartir → MDC."],
         ["Multiplicar os números", "12 × 18 = 216, mas o MMC é 36."],
         ["Usar fatores não comuns no MDC", "No MDC, só entram os fatores que os dois têm."]])
    faq = [("Qual é a diferença entre MMC e MDC?", "O MMC é o menor múltiplo comum (útil para eventos que se repetem e coincidem). O MDC é o maior divisor comum (útil para repartir em grupos ou pedaços iguais, os maiores possíveis)."),
           ("O que a BNCC pede no 6º ano?", "Resolver e elaborar problemas que envolvam as ideias de múltiplo e de divisor (EF06MA06).")]
    unit(R, "mmc-e-mdc", "N", ["EF06MA06"],
         "Resolver e elaborar problemas que envolvam as ideias de múltiplo e de divisor",
         "MMC e MDC: mínimo múltiplo comum e máximo divisor comum", "MMC e MDC",
         "Atividades de matemática para o 6º ano sobre MMC e MDC: múltiplos comuns, divisores comuns, números primos entre si e problemas de encontros e de repartir. 100 exercícios com gabarito.",
         "Repete e coincide: MMC. Reparte igual: MDC.", "MDC × MMC = a × b",
         body, faq, sets, 4, grade="6-ano")


if __name__ == "__main__":
    main()
