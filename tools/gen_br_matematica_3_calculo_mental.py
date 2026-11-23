# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Cálculo mental (Números, EF03MA03, EF03MA05)
  python3 tools/gen_br_matematica_3_calculo_mental.py
Fatos básicos da adição e da subtração, dobros e metades, completar 10, 100 e 1.000, somar e subtrair dezenas,
centenas e milhares exatos, somar 9 ou 99 (somar 10 e tirar 1), decompor para calcular, estimar o resultado.
Erros: juntar algarismos (300 + 40 = 700), esquecer de compensar (+ 9 = + 10 − 1), completar 100 com 90 + 10 = 100 mas errar a unidade.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, Kids, reais

R = random.Random(80303)
K = Kids(R)


def s1_fatos():
    a, b = R.randint(3, 9), R.randint(3, 9)
    k = R.choice(["+", "+", "−", "dobro"])
    if k == "+":
        s = a + b
        return mcq("Quanto é %d + %d?" % (a, b), str(s), [str(s + 1), str(s - 1), str(s + 10 if s < 10 else s - 10)],
                   "%d + %d = <b>%d</b>." % (a, b, s))
    if k == "−":
        s = a + b
        return mcq("Quanto é %d − %d?" % (s, a), str(b), [str(b + 1), str(b - 1), str(s - b + a) if s - b + a != b else str(b + 2)],
                   "Pense na adição: %d + ? = %d. Resposta: <b>%d</b>." % (a, s, b))
    n = R.randint(6, 50)
    return mcq("Qual é o dobro de %d?" % n, str(2 * n), [str(n + 2), str(2 * n + 1), str(n // 2) if n % 2 == 0 else str(3 * n)],
               "Dobro é somar o número com ele mesmo: %d + %d = <b>%d</b>." % (n, n, 2 * n))


def s1_completar():
    k = R.choice(["10", "100", "100", "1000"])
    if k == "10":
        a = R.randint(1, 9)
        return mcq("Quanto falta para %d chegar a 10?" % a, str(10 - a), [str(a), str(11 - a), str(9 - a)],
                   "%d + %d = 10. Resposta: <b>%d</b>." % (a, 10 - a, 10 - a))
    if k == "100":
        a = R.randint(11, 89)
        if a % 10 == 0:
            return None
        c = 100 - a
        wrong = (10 - a // 10) * 10 + (10 - a % 10)
        return mcq("Quanto falta para %d chegar a 100?" % a, str(c), [str(wrong), str(c + 10), str(c - 1)],
                   "De %d até %d faltam %d; de %d até 100 faltam %d. Total: <b>%d</b>." % (a, (a // 10 + 1) * 10, 10 - a % 10, (a // 10 + 1) * 10, 100 - (a // 10 + 1) * 10, c))
    a = R.randint(1, 9) * 100 + R.choice([0, 50])
    c = 1000 - a
    return mcq("Quanto falta para %s chegar a 1.000?" % num(a), num(c), [num(c + 100), num(c - 50) if c > 50 else num(c + 50), num(1000 + a)],
               "%s + %s = 1.000. Resposta: <b>%s</b>." % (num(a), num(c), num(c)))


def s2_exatos():
    k = R.choice(["d", "c", "m", "cm", "dc"])
    if k == "d":
        a, b = R.randint(2, 9) * 10, R.randint(2, 9) * 10
        op = R.choice(["+", "−"])
        if op == "−" and a < b:
            a, b = b, a
        r = a + b if op == "+" else a - b
        if r == 0:
            return None
        return mcq("Calcule de cabeça: %d %s %d." % (a, op, b), num(r), [num(r + 10), num(r - 10) if r > 10 else num(r + 20), num(a // 10 + b // 10 if op == "+" else a // 10 - b // 10)],
                   "%d dezenas %s %d dezenas = %d dezenas = <b>%s</b>." % (a // 10, "mais" if op == "+" else "menos", b // 10, r // 10, num(r)))
    if k == "c":
        a, b = R.randint(1, 8) * 100, R.randint(1, 8) * 100
        op = R.choice(["+", "−"])
        if op == "−" and a < b:
            a, b = b, a
        r = a + b if op == "+" else a - b
        if r == 0:
            return None
        return mcq("Calcule de cabeça: %s %s %s." % (num(a), op, num(b)), num(r), [num(r + 100), num(r - 100) if r > 100 else num(r + 200), num(r // 10)],
                   "%d centenas %s %d centenas = %d centenas = <b>%s</b>." % (a // 100, "mais" if op == "+" else "menos", b // 100, r // 100, num(r)))
    if k == "m":
        a, b = R.randint(1, 6) * 1000, R.randint(1, 3) * 1000
        op = R.choice(["+", "−"])
        if op == "−" and a <= b:
            return None
        r = a + b if op == "+" else a - b
        return mcq("Calcule de cabeça: %s %s %s." % (num(a), op, num(b)), num(r), [num(r + 1000), num(r // 10), num(r + 100)],
                   "%d milhares %s %d milhares = <b>%s</b>." % (a // 1000, "mais" if op == "+" else "menos", b // 1000, num(r)))
    if k == "cm":
        a = R.randint(1, 8) * 1000
        b = R.randint(1, 9) * 100
        c = R.randint(1, 9) * 10
        r = a + b + c
        return mcq("Calcule: %s + %s + %s." % (num(a), num(b), num(c)), num(r), [num(a + b * 10 + c // 10), num(a // 100 + b + c), num(a + b + c * 10)],
                   "Cada número vai para a sua ordem: <b>%s</b>." % num(r))
    a = R.randint(2, 9) * 100 + R.randint(1, 9) * 10
    b = R.randint(1, 9) * 10
    if a % 100 + b < 100:
        return None
    r = a + b
    return mcq("Calcule de cabeça: %s + %d." % (num(a), b), num(r), [num(r - 100), num(r + 100), num(r + 10)],
               "%d dezenas + %d dezenas passam de 10 dezenas: formam mais uma centena. <b>%s</b>." % (a % 100 // 10, b // 10, num(r)))


def s3_compensar():
    k = R.choice(["9", "99", "-9", "-99", "11"])
    if k == "9":
        a = R.randint(23, 189)
        return mcq("Calcule %d + 9 (dica: some 10 e tire 1)." % a, num(a + 9), [num(a + 10), num(a + 8), num(a + 19)],
                   "%d + 10 = %d; %d − 1 = <b>%s</b>." % (a, a + 10, a + 10, num(a + 9)))
    if k == "99":
        a = R.randint(120, 880)
        return mcq("Calcule %s + 99 (dica: some 100 e tire 1)." % num(a), num(a + 99), [num(a + 100), num(a + 98), num(a + 199)],
                   "%s + 100 = %s; menos 1 = <b>%s</b>." % (num(a), num(a + 100), num(a + 99)))
    if k == "-9":
        a = R.randint(31, 190)
        return mcq("Calcule %d − 9 (dica: tire 10 e some 1)." % a, num(a - 9), [num(a - 10), num(a - 8) if (a - 8) != a - 9 else None, num(a - 11)],
                   "%d − 10 = %d; mais 1 = <b>%s</b>." % (a, a - 10, num(a - 9)))
    if k == "-99":
        a = R.randint(220, 980)
        return mcq("Calcule %s − 99 (dica: tire 100 e some 1)." % num(a), num(a - 99), [num(a - 100), num(a - 101), num(a - 98)],
                   "%s − 100 = %s; mais 1 = <b>%s</b>." % (num(a), num(a - 100), num(a - 99)))
    a = R.randint(25, 180)
    return mcq("Calcule %d + 11 (dica: some 10 e depois 1)." % a, num(a + 11), [num(a + 10), num(a + 12), num(a + 21)],
               "%d + 10 = %d; mais 1 = <b>%s</b>." % (a, a + 10, num(a + 11)))


def s3_decompor():
    a = R.randint(21, 79)
    b = R.randint(12, 49)
    if a % 10 + b % 10 < 10:
        return None
    r = a + b
    return mcq("Calcule %d + %d decompondo: %d + %d + %d + %d." % (a, b, a // 10 * 10, b // 10 * 10, a % 10, b % 10), str(r),
               [str(r - 10), str(r + 10), str(a // 10 * 10 + b // 10 * 10 + (a % 10 + b % 10) % 10)],
               "%d + %d = %d; %d + %d = %d; %d + %d = <b>%d</b>." % (a // 10 * 10, b // 10 * 10, a // 10 * 10 + b // 10 * 10, a % 10, b % 10, a % 10 + b % 10,
                                                                   a // 10 * 10 + b // 10 * 10, a % 10 + b % 10, r))


def s4_estimar():
    a = R.randint(110, 890)
    b = R.randint(110, 890)
    if a + b >= 1000:
        return None
    ra, rb = int(round(a / 100.0)) * 100, int(round(b / 100.0)) * 100
    if a % 100 == 50 or b % 100 == 50:
        return None
    est = ra + rb
    return mcq("Arredonde para a centena mais próxima e estime %s + %s." % (num(a), num(b)), "cerca de %s" % num(est),
               ["cerca de %s" % num(x) for x in (est + 100, est - 100, a // 100 * 100 + b // 100 * 100, est + 200, est - 200) if x != est and x > 0],
               "%s fica perto de %s e %s fica perto de %s: %s + %s = <b>cerca de %s</b> (o resultado exato é %s)." % (num(a), num(ra), num(b), num(rb), num(ra), num(rb), num(est), num(a + b)))


def s4_igual():
    a = R.randint(12, 48)
    b = R.randint(12, 48)
    r = a + b
    w = R.randint(1, 9)
    return mcq("Que conta dá o mesmo resultado que %d + %d?" % (a, b), "%d + %d" % (a + w, b - w),
               ["%d + %d" % (a + w, b + w), "%d + %d" % (a - w, b - w), "%d − %d" % (a + b, w)],
               "Se um número ganha %d e o outro perde %d, a soma não muda: %d + %d = %d. Resposta: <b>%d + %d</b>." % (w, w, a + w, b - w, r, a + w, b - w))


def s5_problema():
    k = R.choice(["album", "onibus", "dinheiro", "livro", "garrafas", "pontos"])
    p, _ = K.next()
    if k == "album":
        a = R.randint(3, 9) * 10
        b = R.randint(2, 9) * 10 + 9
        return mcq("%s tinha %d figurinhas e ganhou mais %d. Com quantas ficou?" % (p, a, b), str(a + b), [str(a + b - 1), str(a + b + 10), str(a + b + 1)],
                   "%d + %d = %d + %d − 1 = <b>%d</b>." % (a, b, a, b + 1, a + b))
    if k == "onibus":
        a = R.randint(25, 48)
        b = R.randint(9, 19)
        return mcq("Um ônibus tinha %d passageiros. Desceram %d. Quantos ficaram?" % (a, b), str(a - b), [str(a + b), str(a - b + 1), str(a - b - 10)],
                   "%d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "dinheiro":
        a = R.randint(2, 7) * 100
        b = R.randint(1, 9) * 10
        return mcq("%s tem %s e ganhou %s da avó. Quanto tem agora?" % (p, reais(a * 100), reais(b * 100)), reais((a + b) * 100),
                   [reais((a + b * 10) * 100), reais((a + b + 10) * 100), reais((a - b) * 100)],
                   "%d + %d = %d: <b>%s</b>." % (a, b, a + b, reais((a + b) * 100)))
    if k == "livro":
        t = R.randint(1, 9) * 100
        l = R.randint(1, 9) * 10
        if l >= t:
            return None
        return mcq("Um livro tem %d páginas. %s já leu %d. Quantas páginas faltam?" % (t, p, l), str(t - l), [str(t + l), str(t - l + 10), str(t - l - 10) if t - l > 10 else str(t - l + 20)],
                   "%d − %d = <b>%d</b>." % (t, l, t - l))
    if k == "garrafas":
        a = R.randint(2, 9) * 100
        b = R.randint(1, 9) * 100
        if a + b > 1000:
            return None
        return mcq("Uma escola juntou %d garrafas para reciclar em março e %d em abril. Quantas juntou nos dois meses?" % (a, b), num(a + b),
                   [num(a + b + 100), num(a + b - 100), num(a - b) if a > b else num(b - a + 200)],
                   "%d + %d = <b>%s</b>." % (a, b, num(a + b)))
    a = R.randint(150, 450)
    return mcq("%s fez %d pontos e precisa chegar a 500. Quantos pontos faltam?" % (p, a), str(500 - a), [str(500 + a), str(500 - a + 10), str(400 - a) if a < 400 else str(600 - a)],
               "Complete de %d até 500: <b>%d</b> pontos." % (a, 500 - a))


def main():
    seen = set()
    sets = [
        ("Fatos básicos e completar", mix(R, seen, [(s1_fatos, 12), (s1_completar, 8)])),
        ("Dezenas, centenas e milhares exatos", mix(R, seen, [(s2_exatos, 20)])),
        ("Truques: somar 9, 99, decompor", mix(R, seen, [(s3_compensar, 12), (s3_decompor, 8)])),
        ("Estimar e trocar por uma conta igual", mix(R, seen, [(s4_estimar, 10), (s4_igual, 10)])),
        ("Problemas de cálculo mental", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Os <b>fatos básicos</b> (como 7 + 8 = 15 e 15 − 8 = 7) ajudam em todas as contas. Saber os dobros ajuda também: 7 + 8 = 7 + 7 + 1.",
         "Com números exatos, conte só as dezenas, centenas ou milhares: 300 + 400 = 3 centenas + 4 centenas = 7 centenas = 700.",
         "Para somar 9, some 10 e tire 1. Para somar 99, some 100 e tire 1.",
         "Para <b>estimar</b>, arredonde cada número para a centena mais próxima e faça a conta com os números arredondados."],
        [("47 + 9", ["47 + 10 = 57", "57 − 1 = 56"], "56"),
         ("Quanto falta para 63 chegar a 100?", ["63 → 70: faltam 7", "70 → 100: faltam 30"], "37")],
        [["300 + 40 = 700", "300 são centenas e 40 são dezenas: 300 + 40 = 340."],
         ["47 + 9 = 57", "Somou 10 e esqueceu de tirar 1: o certo é 56."],
         ["Para chegar a 100 de 63, responder 47", "Conte 7 até 70 e 30 até 100: faltam 37."]])
    faq = [("Por que o cálculo mental é importante?", "Ele ajuda a conferir as contas armadas, a fazer estimativas e a resolver problemas do dia a dia, como calcular o troco."),
           ("Como treinar os fatos básicos em casa?", "Com jogos rápidos de 5 minutos por dia: dobros, pares que somam 10 e contas com dezenas exatas.")]
    make_unit(R, "calculo-mental", "N", ["EF03MA03", "EF03MA05"],
              "Construir e utilizar fatos básicos da adição e da multiplicação para o cálculo mental ou escrito; utilizar diferentes procedimentos de cálculo mental e escrito para resolver problemas significativos envolvendo adição e subtração com números naturais",
              "Cálculo mental: adição e subtração", "Cálculo mental",
              "Atividades de matemática para o 3º ano sobre cálculo mental: fatos básicos, completar 10, 100 e 1.000, dezenas e centenas exatas, somar 9 e 99, estimativas. 100 exercícios com gabarito.",
              "Some 10 e tire 1 para somar 9.", "Para estimar, arredonde para a centena mais próxima.",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
