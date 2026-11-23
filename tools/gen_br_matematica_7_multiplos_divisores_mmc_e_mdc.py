# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Múltiplos, divisores, MMC e MDC (Números, EF07MA01)
  python3 tools/gen_br_matematica_7_multiplos_divisores_mmc_e_mdc.py
Problemas com múltiplos e divisores (sem fórmula pronta): encontros periódicos, divisão em grupos, quadrados e ladrilhos,
quantidade de divisores, números que deixam o mesmo resto; MMC e MDC pela decomposição em fatores primos.
Usa o gerador do 6º ano (MMC e MDC) com outro sorteio.
Erros: usar MDC quando é MMC, esquecer o resto, contar só os divisores primos.
"""
import random
from math import gcd
from br_common import lesson, mix, use
from br_9 import M, d, unit

R = random.Random(87001)
m_mmc, m_mdc, m_prob = use("gen_br_matematica_6_mmc_e_mdc", 87901, "s1_mmc", "s2_mdc", "s5_problemas")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def fat(n):
    out, p = [], 2
    while n > 1:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            out.append((p, e))
        p += 1
    return out


def fs(f):
    return " × ".join(str(p) + (str(e).translate(SUP) if e > 1 else "") for p, e in f)


def s1_decomp():
    while True:
        a, b = R.sample(range(12, 200), 2)
        if gcd(a, b) > 2 and a * b // gcd(a, b) <= 3000:
            break
    fa, fb = fat(a), fat(b)
    k = R.choice(["mmc", "mdc"])
    m, g = a * b // gcd(a, b), gcd(a, b)
    if k == "mmc":
        return M("Com %d = %s e %d = %s, qual é o MMC(%d, %d)?" % (a, fs(fa), b, fs(fb), a, b), d(m), [d(g), d(a * b), d(m * 2)],
                 "Use todos os fatores, cada um com o maior expoente: <b>%s</b>." % d(m))
    return M("Com %d = %s e %d = %s, qual é o MDC(%d, %d)?" % (a, fs(fa), b, fs(fb), a, b), d(g), [d(m), "1" if g != 1 else "2", d(g * 2)],
             "Use só os fatores comuns, cada um com o menor expoente: <b>%d</b>." % g)


def s2_resto():
    a, b = R.choice([(2, 3), (3, 4), (4, 5), (3, 5), (4, 6), (5, 6), (6, 8)])
    r = R.randint(1, min(a, b) - 1)
    m = a * b // gcd(a, b)
    lo = R.choice([20, 30, 40, 50, 100])
    n = next(x for x in range(lo, lo + m + 1) if x % m == r)
    return M("Qual é o menor número maior que %d que, dividido por %d e por %d, deixa resto %d?" % (lo, a, b, r), d(n), [d(n - r), d(n + m), d(n + 1)],
             "Os números com resto %d são múltiplos de MMC(%d, %d) = %d mais %d: <b>%d</b>." % (r, a, b, m, r, n))


def s3_ladrilho():
    k = R.choice(["quadrado", "ladrilho", "cubos"])
    if k == "quadrado":
        a, b = R.choice([(6, 8), (4, 10), (6, 9), (8, 12), (10, 15), (12, 18)])
        m = a * b // gcd(a, b)
        return M("Juntando retângulos de %d cm por %d cm, todos na mesma posição, qual é o menor quadrado que se pode formar?" % (a, b), "%d cm de lado" % m, ["%d cm de lado" % gcd(a, b), "%d cm de lado" % (a * b), "%d cm de lado" % (a + b)],
                     "O lado precisa ser múltiplo de %d e de %d: MMC = <b>%d cm</b>." % (a, b, m))
    if k == "ladrilho":
        a, b = R.choice([(240, 180), (360, 300), (420, 280), (300, 450), (480, 360)])
        g = gcd(a, b)
        return M("Um piso de %d cm por %d cm será coberto por ladrilhos quadrados iguais, os maiores possíveis, sem cortes. Qual é o lado do ladrilho?" % (a, b), "%d cm" % g, ["%d cm" % (a * b // g), "%d cm" % (g // 2), "%d cm" % (a - b)],
                     "O lado precisa dividir %d e %d: MDC = <b>%d cm</b>." % (a, b, g))
    a, b, c = R.choice([(12, 18, 30), (8, 12, 20), (10, 15, 25), (6, 9, 15), (16, 24, 40)])
    g = gcd(gcd(a, b), c)
    return M("Uma caixa mede %d cm × %d cm × %d cm e será preenchida com cubos iguais, os maiores possíveis. Qual é a aresta do cubo?" % (a, b, c), "%d cm" % g, ["%d cm" % (g * 2) if a % (2 * g) else "%d cm" % (g + 1), "%d cm" % min(a, b, c), "1 cm" if g != 1 else "2 cm"],
             "MDC(%d, %d, %d) = <b>%d cm</b>." % (a, b, c, g))


def s4_divisores():
    n = R.choice([24, 36, 48, 60, 72, 90, 96, 100, 120, 144, 180, 200])
    f = fat(n)
    q = 1
    for _, e in f:
        q *= e + 1
    return M("Usando a decomposição %d = %s, quantos divisores naturais tem %d?" % (n, fs(f), n), d(q), [d(q - 2), d(sum(e for _, e in f)), d(q + 2)],
             "Multiplique (expoente + 1) de cada fator: %s = <b>%d</b>." % (" × ".join("(%d + 1)" % e for _, e in f), q))


def main():
    seen = set()
    sets = [
        ("MMC e MDC", mix(R, seen, [(m_mmc, 10), (m_mdc, 10)])),
        ("Pela decomposição em primos", mix(R, seen, [(s1_decomp, 20)])),
        ("Quantos divisores?", mix(R, seen, [(s4_divisores, 12), (s2_resto, 8)])),
        ("Quadrados, ladrilhos e cubos", mix(R, seen, [(s3_ladrilho, 15), (s2_resto, 5)])),
        ("Problemas", mix(R, seen, [(m_prob, 20)])),
    ]
    body = lesson(
        ["Decomponha os números em fatores primos. <b>MMC</b>: todos os fatores, com o maior expoente. <b>MDC</b>: só os fatores comuns, com o menor expoente.",
         "Problemas de <b>repetição</b> (encontros, menor quadrado formado com retângulos) pedem o MMC; problemas de <b>repartir</b> (ladrilhos, grupos, pedaços) pedem o MDC.",
         "Número de divisores: se n = 2³ × 3², tem (3 + 1) × (2 + 1) = 12 divisores."],
        [("60 = 2² × 3 × 5 e 90 = 2 × 3² × 5", ["MMC: 2² × 3² × 5", "MDC: 2 × 3 × 5"], "MMC 180, MDC 30"),
         ("Menor número com resto 1 por 4 e por 6", ["MMC(4, 6) = 12", "12 + 1"], "13")],
        [["Usar MDC quando é MMC", "Repete → MMC; reparte → MDC."],
         ["Esquecer o resto", "Some o resto ao múltiplo comum."],
         ["Contar só os divisores primos", "1, os primos e os compostos: todos contam."]])
    faq = [("Como achar o MMC e o MDC pela fatoração?", "Escreva os números como produto de primos. O MMC usa todos os fatores com os maiores expoentes; o MDC usa só os fatores comuns com os menores expoentes."),
           ("O que a BNCC pede no 7º ano?", "Resolver e elaborar problemas com números naturais, envolvendo as noções de divisor e de múltiplo, podendo incluir máximo divisor comum ou mínimo múltiplo comum, por meio de estratégias diversas, sem a aplicação de algoritmos (EF07MA01).")]
    unit(R, "multiplos-divisores-mmc-e-mdc", "N", ["EF07MA01"],
         "Resolver e elaborar problemas com números naturais, envolvendo as noções de divisor e de múltiplo, podendo incluir máximo divisor comum ou mínimo múltiplo comum, por meio de estratégias diversas, sem a aplicação de algoritmos",
         "Múltiplos, divisores, MMC e MDC: problemas", "Múltiplos e divisores",
         "Atividades de matemática para o 7º ano sobre múltiplos e divisores: MMC e MDC pela decomposição em primos, número de divisores, restos, ladrilhos, cubos e problemas. 100 exercícios com gabarito.",
         "Repete e coincide: MMC. Reparte igual: MDC.", "MMC: maiores expoentes. MDC: fatores comuns, menores expoentes.",
         body, faq, sets, 1, grade="7-ano")


if __name__ == "__main__":
    main()
