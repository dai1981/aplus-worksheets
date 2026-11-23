# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Adição e subtração com naturais e decimais (Números, EF05MA07)
  python3 tools/gen_br_matematica_5_adicao_e_subtracao.py
Adição e subtração de números naturais até centenas de milhar (conta armada, reagrupamento, zeros);
adição e subtração de decimais (vírgula embaixo de vírgula); estimativa e prova real; problemas com dinheiro e medidas.
Erros: esquecer o «vai um», subtrair o menor do maior em cada coluna, alinhar os decimais pela direita (2,5 + 1,25 = 1,50).
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, dz, reais, armada, Kids

R = random.Random(80507)
K = Kids(R)


def digits(n):
    return [int(c) for c in str(n)]


def no_carry_add(a, b):
    """soma sem «vai um» (erro comum)"""
    s = ""
    A, B = str(a).rjust(7, "0"), str(b).rjust(7, "0")
    for x, y in zip(A, B):
        s += str((int(x) + int(y)) % 10)
    return int(s)


def small_minus_big(a, b):
    """em cada coluna, o maior menos o menor (erro comum)"""
    A, B = str(a).rjust(7, "0"), str(b).rjust(7, "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(A, B)))


def s1_adicao():
    a = R.randint(10000, 600000)
    b = R.randint(1000, 999999 - a)
    s = a + b
    if no_carry_add(a, b) == s:
        return None
    pic = armada([num(a), num(b)], "+") if R.random() < 0.5 else ""
    return mcq(pic + "Calcule %s + %s." % (num(a), num(b)), num(s), [num(no_carry_add(a, b)), num(s + 1000), num(s - 10), num(s + 100)],
               "Some coluna por coluna, da direita para a esquerda, e não esqueça o «vai um»: <b>%s</b>." % num(s))


def s1_tres():
    a, b, c = R.randint(10000, 90000), R.randint(10000, 90000), R.randint(1000, 9000)
    s = a + b + c
    return mcq("Calcule %s + %s + %s." % (num(a), num(b), num(c)), num(s), [num(s - 1000), num(s + 10000), num(no_carry_add(no_carry_add(a, b), c)), num(s + 10)],
               "%s + %s = %s; %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b), num(a + b), num(c), num(s)))


def s2_subtracao():
    k = R.choice(["normal", "zeros", "normal"])
    if k == "zeros":
        a = R.choice([100000, 200000, 300000, 500000, 400000, 700000, 600000]) + R.choice([0, 0, 1000, 10000])
    else:
        a = R.randint(100000, 999999)
    b = R.randint(10000, a - 1000)
    d = a - b
    w = small_minus_big(a, b)
    if w == d:
        return None
    pic = armada([num(a), num(b)], "−") if R.random() < 0.5 else ""
    return mcq(pic + "Calcule %s − %s." % (num(a), num(b)), num(d), [num(w), num(d + 1000), num(d - 10), num(d + 10)],
               "Subtraia coluna por coluna; quando o algarismo de cima for menor, troque 1 da ordem seguinte por 10. Prova real: %s + %s = %s. Resposta: <b>%s</b>." % (num(d), num(b), num(a), num(d)))


def s2_falta():
    a = R.randint(20000, 500000)
    b = R.randint(1000, 400000)
    if R.random() < 0.5:
        return mcq("Que número somado a %s dá %s?" % (num(a), num(a + b)), num(b), [num(a + a + b), num(b + 1000), num(b - 10) if b > 10 else num(b + 10), num(small_minus_big(a + b, a))],
                   "Use a operação inversa: %s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    return mcq("De que número tiramos %s para ficar com %s?" % (num(b), num(a)), num(a + b), [num(abs(a - b)), num(a + b + 1000), num(no_carry_add(a, b)) if no_carry_add(a, b) != a + b else num(a + b - 100)],
               "Faça a operação inversa: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def s3_decimais():
    ka, kb = R.choice([(1, 2), (2, 1), (1, 1), (2, 2), (1, 3), (3, 2)])
    a = R.randint(11, 99 * 10 ** (ka - 1) + 9)
    b = R.randint(11, 99 * 10 ** (kb - 1) + 9)
    k = max(ka, kb)
    A, B = a * 10 ** (k - ka), b * 10 ** (k - kb)
    op = R.choice(["+", "−"])
    if op == "−":
        if A == B:
            return None
        if A < B:
            a, b, ka, kb, A, B = b, a, kb, ka, B, A
        res = A - B
        wrong = abs(a - b)
    else:
        res = A + B
        wrong = a + b
    sa, sb = dz(a, ka), dz(b, kb)
    w = [dz(wrong, max(ka, kb)) if ka != kb else None, dz(res + 10 ** k, k), dz(res - 10 ** (k - 1), k) if res > 10 ** (k - 1) else None, dz(res + 10 ** (k - 1), k), dz(res + 2 * 10 ** (k - 1), k)]
    rows = [dz(A, k, True), dz(B, k, True)]
    pic = armada(rows, "+" if op == "+" else "−") if R.random() < 0.4 else ""
    return mcq(pic + "Calcule %s %s %s." % (sa, op, sb), dz(res, k), w,
               "Coloque vírgula embaixo de vírgula e complete com zeros: %s %s %s = <b>%s</b>." % (dz(A, k, True), op, dz(B, k, True), dz(res, k)))


def s3_inteiro():
    a = R.randint(2, 20)
    k = R.choice([1, 2])
    b = R.randint(1, 10 ** k * 3 - 1)
    if b % 10 == 0 or b >= a * 10 ** k:
        return None
    ip, fp_ = divmod(b, 10 ** k)
    if R.random() < 0.5:
        return mcq("Calcule %d − %s." % (a, dz(b, k)), dz(a * 10 ** k - b, k),
                   [dz((a - ip) * 10 ** k + fp_, k), dz(a * 10 ** k + b, k), dz(a * 10 ** k - b + 10 ** k, k), dz(a * 10 ** k - b - 10 ** (k - 1), k)],
                   "Escreva %d como %s e subtraia: <b>%s</b>." % (a, dz(a * 10 ** k, k, True), dz(a * 10 ** k - b, k)))
    return mcq("Calcule %d + %s." % (a, dz(b, k)), dz(a * 10 ** k + b, k), [dz(a + b, k), dz(b + a * 10 ** (k - 1), k), dz(a * 10 ** k + b + 10 ** k, k), dz(a * 10 ** k - b, k)],
               "%d = %s. %s + %s = <b>%s</b>." % (a, dz(a * 10 ** k, k, True), dz(a * 10 ** k, k, True), dz(b, k, True), dz(a * 10 ** k + b, k)))


def s4_estimar():
    a = R.randint(100000, 600000)
    b = R.randint(100000, 350000)
    op = R.choice(["+", "−"])
    ra, rb = (a + 50000) // 100000 * 100000, (b + 50000) // 100000 * 100000
    e = ra + rb if op == "+" else ra - rb
    if op == "−" and e <= 0:
        return None
    ex = a + b if op == "+" else a - b
    opts = sorted({e, e + 100000, e - 100000 if e > 100000 else e + 200000, e + 300000})
    return mcq("Arredonde para a centena de milhar mais próxima e estime %s %s %s." % (num(a), op, num(b)), "cerca de " + num(e), ["cerca de " + num(x) for x in opts if x != e],
               "%s ≈ %s e %s ≈ %s. %s %s %s = <b>%s</b> (a conta exata dá %s)." % (num(a), num(ra), num(b), num(rb), num(ra), op, num(rb), num(e), num(ex)))


def s4_prova():
    a = R.randint(50000, 900000)
    b = R.randint(10000, a - 1)
    d = a - b
    k = R.choice(["sub", "add"])
    if k == "sub":
        return mcq("%s fez %s − %s = %s. Qual conta serve de prova real?" % (K.next()[0], num(a), num(b), num(d)), "%s + %s = %s" % (num(d), num(b), num(a)),
                   ["%s + %s = %s" % (num(a), num(b), num(a + b)), "%s − %s = %s" % (num(d), num(b), num(abs(d - b))), "%s + %s = %s" % (num(a), num(d), num(a + d))],
                   "Na subtração, a prova real é somar o resultado com o número que foi tirado: <b>%s + %s = %s</b>." % (num(d), num(b), num(a)))
    w = d + R.choice([1000, -1000, 10000, 100])
    ok = R.random() < 0.5
    shown = d if ok else w
    return mcq("%s fez %s − %s = %s. Usando a prova real, a conta está certa?" % (K.next()[0], num(a), num(b), num(shown)),
               "Sim: %s + %s = %s" % (num(shown), num(b), num(a)) if ok else "Não: %s + %s = %s" % (num(shown), num(b), num(shown + b)),
               ["Não: %s + %s = %s" % (num(shown), num(b), num(shown + b + 1000)) if ok else "Sim: %s + %s = %s" % (num(shown), num(b), num(a)),
                "Só dá para saber fazendo a conta de novo", "Sim, porque o resultado é menor que %s" % num(a)],
               "Some o resultado com %s: %s + %s = %s%s. <b>%s</b>." % (num(b), num(shown), num(b), num(shown + b), "" if ok else " (diferente de %s)" % num(a), "Está certa" if ok else "Está errada; o certo é %s" % num(d)))


def s5_problema():
    k = R.choice(["compra", "troco", "corrida", "cidade", "estoque", "altura", "visitas"])
    p, g = K.next()
    if k == "compra":
        a, b = R.randint(1500, 9000), R.randint(500, 5000)
        return mcq("%s comprou um livro de %s e um caderno de %s. Quanto gastou ao todo?" % (p, reais(a), reais(b)), reais(a + b),
                   [reais(abs(a - b)), reais(a + b + 100), reais(a + b - 10), reais(no_carry_add(a, b)) if no_carry_add(a, b) != a + b else reais(a + b + 1000)],
                   "%s + %s = <b>%s</b>." % (reais(a), reais(b), reais(a + b)))
    if k == "troco":
        nota = R.choice([2000, 5000, 10000])
        c = R.randint(nota // 5, nota - 50)
        if c % 5:
            return None
        return mcq("%s pagou uma compra de %s com uma cédula de %s. Quanto recebeu de troco?" % (p, reais(c), reais(nota)), reais(nota - c),
                   [reais(nota + c), reais(nota - c + 100), reais(nota - c - 10) if nota - c > 10 else reais(nota - c + 10), reais(small_minus_big(nota, c)) if small_minus_big(nota, c) != nota - c else reais(nota - c + 1000)],
                   "%s − %s = <b>%s</b>." % (reais(nota), reais(c), reais(nota - c)))
    if k == "corrida":
        a, b = R.randint(15, 49) * 10 + R.randint(1, 9), R.randint(15, 49) * 10 + R.randint(1, 9)
        return mcq("%s correu %s km de manhã e %s km à tarde. Quantos quilômetros correu no dia?" % (p, dz(a, 1), dz(b, 1)), dz(a + b, 1) + " km",
                   [dz(a + b, 2) + " km", dz(abs(a - b), 1) + " km", dz(a + b + 10, 1) + " km"], "%s + %s = <b>%s km</b>." % (dz(a, 1), dz(b, 1), dz(a + b, 1)))
    if k == "cidade":
        a = R.randint(100000, 800000)
        b = R.randint(5000, 90000)
        if R.random() < 0.5:
            return mcq("Uma cidade tinha %s habitantes. Nos últimos anos chegaram mais %s. Quantos habitantes ela tem agora?" % (num(a), num(b)), num(a + b),
                       [num(a - b), num(no_carry_add(a, b)) if no_carry_add(a, b) != a + b else num(a + b + 10000), num(a + b + 1000)], "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
        return mcq("Um estádio tem %s lugares. Num jogo, %s lugares ficaram vazios. Quantas pessoas foram ao jogo?" % (num(b + a // 10), num(b // 10)), num(b + a // 10 - b // 10),
                   [num(b + a // 10 + b // 10), num(small_minus_big(b + a // 10, b // 10)) if small_minus_big(b + a // 10, b // 10) != b + a // 10 - b // 10 else num(b + a // 10 - b // 10 + 1000), num(b + a // 10 - b // 10 - 100)],
                   "%s − %s = <b>%s</b>." % (num(b + a // 10), num(b // 10), num(b + a // 10 - b // 10)))
    if k == "estoque":
        a = R.randint(20000, 90000)
        b, c = R.randint(1000, 9000), R.randint(1000, 9000)
        return mcq("Uma fábrica tinha %s garrafas. Vendeu %s e depois fabricou mais %s. Quantas garrafas ela tem agora?" % (num(a), num(b), num(c)), num(a - b + c),
                   [num(a + b + c), num(a - b - c), num(a + b - c)], "%s − %s + %s = <b>%s</b>." % (num(a), num(b), num(c), num(a - b + c)))
    if k == "altura":
        a, b = R.randint(130, 165), R.randint(5, 25)
        return mcq("%s media %s m. Em dois anos cresceu %s m. Quanto %s mede agora?" % (p, dz(a, 2), dz(b, 2), g), dz(a + b, 2) + " m",
                   [dz(x, 2) + " m" for x in (a + b * 10, a - b, a + b + 10, a + b - 1)],
                   "%s + %s = <b>%s m</b>." % (dz(a, 2), dz(b, 2, True), dz(a + b, 2)))
    a, b = R.randint(100000, 400000), R.randint(100000, 400000)
    if a == b:
        return None
    return mcq("Um museu recebeu %s visitantes num ano e %s no ano seguinte. Qual é a diferença entre os dois anos?" % (num(a), num(b)), num(abs(a - b)),
               [num(a + b), num(small_minus_big(max(a, b), min(a, b))) if small_minus_big(max(a, b), min(a, b)) != abs(a - b) else num(abs(a - b) + 1000), num(abs(a - b) + 10000)],
               "%s − %s = <b>%s</b>." % (num(max(a, b)), num(min(a, b)), num(abs(a - b))))


def main():
    seen = set()
    sets = [
        ("Adição de números naturais", mix(R, seen, [(s1_adicao, 14), (s1_tres, 6)])),
        ("Subtração de números naturais", mix(R, seen, [(s2_subtracao, 14), (s2_falta, 6)])),
        ("Adição e subtração de decimais", mix(R, seen, [(s3_decimais, 14), (s3_inteiro, 6)])),
        ("Estimativa e prova real", mix(R, seen, [(s4_estimar, 10), (s4_prova, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Na conta armada, coloque <b>unidade embaixo de unidade</b>, dezena embaixo de dezena… e calcule da direita para a esquerda.",
         "Quando a soma de uma coluna passa de 9, escreva as unidades e leve 1 para a coluna seguinte («vai um»).",
         "Na subtração, se o algarismo de cima for menor, troque 1 da ordem seguinte por 10.",
         "Com decimais, coloque <b>vírgula embaixo de vírgula</b> e complete com zeros: 2,5 + 1,25 = 2,50 + 1,25 = 3,75.",
         "Para conferir uma subtração, faça a <b>prova real</b>: resultado + número tirado = número inicial."],
        [("Calcule 304.000 − 128.450.", ["troque 1 milhar e as ordens vazias por 10", "prova: 175.550 + 128.450 = 304.000"], "175.550"),
         ("Calcule 7 − 2,35.", ["7 = 7,00", "7,00 − 2,35"], "4,65")],
        [["Esquecer o «vai um»", "Escreva o 1 pequeno em cima da coluna seguinte."],
         ["Em cada coluna, tirar o menor do maior", "Se em cima é menor, troque 1 da ordem seguinte por 10."],
         ["Alinhar os decimais pela direita: 2,5 + 1,25 = 1,50", "Vírgula embaixo de vírgula: 2,50 + 1,25 = 3,75."]],
        armada(["2,50", "1,25"], "+", result="3,75"))
    faq = [("O que o 5º ano faz com adição e subtração?", "A BNCC pede resolver e elaborar problemas de adição e subtração com números naturais e com números decimais, usando estratégias variadas, como cálculo por estimativa, cálculo mental e algoritmos."),
           ("Por que completar com zeros nos decimais?", "Para que cada ordem fique na mesma coluna: 2,5 = 2,50. Assim somamos décimos com décimos e centésimos com centésimos.")]
    make_unit(R, "adicao-e-subtracao", "N", ["EF05MA07"],
              "Resolver e elaborar problemas de adição e subtração com números naturais e com números racionais, cuja representação decimal seja finita, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos",
              "Adição e subtração com números naturais e decimais", "Adição e subtração",
              "Atividades de matemática para o 5º ano sobre adição e subtração com números naturais e decimais: conta armada, reagrupamento, vírgula embaixo de vírgula, estimativa, prova real e problemas. 100 exercícios com gabarito.",
              "Vírgula embaixo de vírgula; complete com zeros.", "Prova real: resultado + número tirado = número inicial.",
              body, faq, sets, 7, grade="5-ano")


if __name__ == "__main__":
    main()
