# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Algoritmos e fluxogramas (EM13MAT315)
  python3 tools/gen_br_matematica_em3_algoritmos_e_fluxogramas.py
Seguir um algoritmo passo a passo (linguagem natural e fluxograma); decisões (se/senão) e repetições;
algoritmo de Euclides para o MDC; conversão para binário; algoritmos de cálculo (IMC, desconto progressivo); símbolos do fluxograma.
Erros: parar a repetição antes ou depois da hora, trocar o caminho «sim» e «não», esquecer de atualizar a variável.
"""
import random
from math import gcd
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, unit, num, code, fluxo, R2

R = random.Random(93008)


def s1_seguir():
    k = R.choice(["dobra", "soma", "par", "maior"])
    if k == "dobra":
        a, lim = R.randint(1, 9), R.choice([50, 100, 200, 500])
        x, n = a, 0
        while x <= lim:
            x *= 2
            n += 1
        alg = code("1. Comece com x = %d." % a, "2. Enquanto x ≤ %d, troque x por 2 · x." % lim, "3. Mostre x.")
        return M(alg + "Qual número o algoritmo mostra?", str(x), [str(x // 2), str(x * 2), str(lim)], "%s: <b>%d</b>." % (" → ".join(str(a * 2 ** i) for i in range(n + 1)), x))
    if k == "soma":
        n = R.randint(4, 12)
        alg = code("1. Faça s = 0 e i = 1.", "2. Enquanto i ≤ %d: some i a s e aumente i em 1." % n, "3. Mostre s.")
        return M(alg + "Qual número o algoritmo mostra?", str(n * (n + 1) // 2), [str(n * (n - 1) // 2), str(n), str(n * n)], "s = 1 + 2 + … + %d = <b>%d</b>." % (n, n * (n + 1) // 2))
    if k == "par":
        n = R.randint(10, 99)
        g = fluxo([("ini", "Início"), ("es", "Leia n = %d" % n), ("dec", "n é par?"), ("proc", "Sim: y = n ÷ 2 | Não: y = 3n + 1"), ("es", "Mostre y"), ("ini", "Fim")], label="fluxograma com uma decisão")
        y = n // 2 if n % 2 == 0 else 3 * n + 1
        return M(g + "Qual valor o fluxograma mostra?", str(y), [str(3 * n + 1) if n % 2 == 0 else str(n // 2), str(n), str(2 * n)], "%d é %s: y = <b>%d</b>." % (n, "par" if n % 2 == 0 else "ímpar", y))
    a, b, c = R.sample(range(1, 60), 3)
    alg = code("1. Leia a = %d, b = %d, c = %d." % (a, b, c), "2. Faça m = a.", "3. Se b > m, faça m = b.", "4. Se c > m, faça m = c.", "5. Mostre m.")
    return M(alg + "O que o algoritmo mostra?", str(max(a, b, c)), [str(min(a, b, c)), str(a), str(sorted([a, b, c])[1])], "Ele guarda o maior valor visto: <b>%d</b>." % max(a, b, c))


def s2_euclides():
    a, b = R.randint(20, 200), R.randint(10, 150)
    if a < b:
        a, b = b, a
    g = gcd(a, b)
    k = R.choice(["mdc", "passos"])
    if k == "mdc":
        alg = code("1. Divida a pelo b e ache o resto r.", "2. Se r = 0, o MDC é b. Pare.", "3. Senão, faça a = b e b = r, e volte ao passo 1.")
        return M(alg + "Usando o algoritmo de Euclides, qual é o MDC de %d e %d?" % (a, b), str(g), [str(a % b) if a % b != g else str(g * 2), str(b), str(a * b // g) if a * b // g < 10000 else "1"],
                 "Divisões sucessivas até o resto zero: <b>MDC = %d</b>." % g)
    steps, x, y = 0, a, b
    while y:
        x, y = y, x % y
        steps += 1
    return M("No algoritmo de Euclides para %d e %d, quantas divisões são feitas até obter resto zero?" % (a, b), str(steps), [str(steps + 1), str(steps - 1) if steps > 1 else "3", str(g)], "Divisões até o resto zero: <b>%d</b>." % steps)


def s3_binario():
    k = R.choice(["para", "de"])
    n = R.randint(5, 60)
    b = bin(n)[2:]
    if k == "para":
        return M("Pelo algoritmo das divisões sucessivas por 2, como se escreve %d na base 2?" % n, b, [b[::-1] if b[::-1] != b else b + "0", bin(n + 1)[2:], bin(n - 1)[2:]], "Restos lidos de baixo para cima: <b>%s</b>." % b)
    return M("Qual número decimal o binário %s representa?" % b, str(n), [str(int(b[::-1], 2)) if int(b[::-1], 2) != n else str(n + 2), str(len(b)), str(n + 1)], "%s = <b>%d</b>." % (" + ".join(str(2 ** i) for i, c in enumerate(b[::-1]) if c == "1"), n))


def s4_calculo():
    k = R.choice(["imc", "desconto", "frete"])
    if k == "imc":
        m = R.choice([50, 60, 64, 72, 81, 90])
        h = R.choice([F(16, 10), F(17, 10), F(18, 10), F(15, 10)])
        imc = F(m) / (h * h)
        c = "abaixo do peso" if imc < F(185, 10) else ("peso adequado" if imc < 25 else ("sobrepeso" if imc < 30 else "obesidade"))
        alg = code("1. Calcule IMC = massa ÷ (altura · altura).", "2. Se IMC < 18,5, mostre «abaixo do peso».", "3. Senão, se IMC < 25, mostre «peso adequado».", "4. Senão, se IMC < 30, mostre «sobrepeso».", "5. Senão, mostre «obesidade».")
        return M(alg + "O que o algoritmo mostra para massa %d kg e altura %s m?" % (m, d(h)), c, [x for x in ("abaixo do peso", "peso adequado", "sobrepeso", "obesidade") if x != c], "IMC = %d ÷ %s ≈ %s: <b>%s</b>." % (m, d(h * h), d(imc, 1), c))
    if k == "desconto":
        v = R.choice([80, 150, 250, 400, 600])
        p = 0 if v < 100 else (10 if v < 300 else 20)
        alg = code("1. Leia o valor da compra v.", "2. Se v < 100, desconto = 0%.", "3. Senão, se v < 300, desconto = 10%.", "4. Senão, desconto = 20%.", "5. Mostre v com o desconto.")
        return M(alg + "Para uma compra de R$ %d, qual valor o algoritmo mostra?" % v, R2(F(v * (100 - p), 100)), [R2(v), R2(F(v * 90, 100)) if p != 10 else R2(F(v * 80, 100)), R2(F(v * p, 100)) if p else R2(v - 10)],
                 "%d está na faixa de %d%%: <b>%s</b>." % (v, p, R2(F(v * (100 - p), 100))))
    kg = R.randint(1, 12)
    alg = code("1. Leia o peso p (kg).", "2. Se p ≤ 2, frete = R$ 15.", "3. Senão, frete = R$ 15 + R$ 5 por kg acima de 2.", "4. Mostre o frete.")
    fr = 15 if kg <= 2 else 15 + 5 * (kg - 2)
    return M(alg + "Qual é o frete para %d kg?" % kg, R2(fr), [R2(15 + 5 * kg), R2(5 * kg), R2(fr + 5)], "<b>%s</b>." % R2(fr))


s5_conceitos = bank(R, [
    ("Num fluxograma, o losango representa…", "uma decisão (pergunta com sim ou não)", ["o início", "uma entrada de dados", "o fim"]),
    ("Num fluxograma, a forma oval (arredondada) representa…", "o início ou o fim", ["uma decisão", "um cálculo", "uma repetição"]),
    ("Num fluxograma, o retângulo representa…", "um processo (uma ação ou cálculo)", ["uma decisão", "o início", "uma pergunta"]),
    ("Um algoritmo é…", "uma sequência finita de passos bem definidos para resolver um problema", ["um tipo de gráfico", "um número muito grande", "uma fórmula de área"]),
    ("Uma estrutura de repetição serve para…", "executar passos várias vezes enquanto uma condição for verdadeira", ["escolher entre dois caminhos uma única vez", "terminar o algoritmo", "ler um dado"]),
    ("Se a condição de uma repetição nunca fica falsa, o algoritmo…", "nunca termina (laço infinito)", ["termina na hora certa", "dá erro de conta", "pula a repetição"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Seguir algoritmos", mix(R, seen, [(s1_seguir, 20)])),
        ("Fluxogramas e decisões", mix(R, seen, [(s1_seguir, 8), (s4_calculo, 6), (s5_conceitos, 6)])),
        ("Algoritmo de Euclides", mix(R, seen, [(s2_euclides, 20)])),
        ("Sistema binário", mix(R, seen, [(s3_binario, 20)])),
        ("Algoritmos do dia a dia", mix(R, seen, [(s4_calculo, 20)])),
    ]
    body = lesson(
        ["Um <b>algoritmo</b> é uma sequência finita de passos bem definidos. Siga-o com cuidado, anotando o valor de cada variável a cada passo.",
         "<b>Decisão</b> (se… senão): o caminho depende de uma condição. <b>Repetição</b> (enquanto…): os passos se repetem até a condição ficar falsa.",
         "No <b>fluxograma</b>: oval = início/fim; paralelogramo = entrada ou saída; retângulo = processo; losango = decisão.",
         "<b>Euclides</b>: MDC(a, b) = MDC(b, resto de a ÷ b), até o resto ser 0. <b>Binário</b>: divida por 2 e leia os restos de baixo para cima."],
        [("MDC(84, 36)", ["84 = 2 · 36 + 12", "36 = 3 · 12 + 0"], "12"),
         ("13 na base 2", ["13 → 6 r1 → 3 r0 → 1 r1 → 0 r1"], "1101")],
        [["Errar a hora de parar", "Teste a condição antes de cada repetição."],
         ["Trocar «sim» e «não»", "Leia a pergunta do losango com atenção."],
         ["Esquecer de atualizar a variável", "Anote os valores numa tabela a cada passo."]],
        fluxo([("ini", "Início"), ("es", "Leia n"), ("dec", "n é par?"), ("proc", "Sim: y = n ÷ 2 | Não: y = 3n + 1"), ("es", "Mostre y"), ("ini", "Fim")], label="exemplo de fluxograma"))
    faq = [("Como funciona o algoritmo de Euclides?", "Divida o maior número pelo menor. Troque o maior pelo menor e o menor pelo resto, e repita. Quando o resto for zero, o último divisor é o MDC."),
           ("O que a BNCC pede?", "Investigar e registrar, por meio de um fluxograma, quando possível, um algoritmo que resolve um problema (EM13MAT315).")]
    unit(R, "algoritmos-e-fluxogramas", "A", ["EM13MAT315"],
         "Investigar e registrar, por meio de um fluxograma, quando possível, um algoritmo que resolve um problema",
         "Algoritmos e fluxogramas", "Algoritmos e fluxogramas",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre algoritmos: seguir passos, decisões e repetições, fluxogramas, algoritmo de Euclides, sistema binário e algoritmos do dia a dia. 100 exercícios com gabarito.",
         "Algoritmo: passos finitos e bem definidos", "Losango = decisão; oval = início ou fim.",
         body, faq, sets, 8, grade="3-serie")


if __name__ == "__main__":
    main()
