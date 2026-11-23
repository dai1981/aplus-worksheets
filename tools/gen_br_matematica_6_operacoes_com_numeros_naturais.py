# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Operações com números naturais (Números, EF06MA03)
  python3 tools/gen_br_matematica_6_operacoes_com_numeros_naturais.py
Adição, subtração, multiplicação e divisão com números naturais; divisão com resto e relação fundamental;
expressões numéricas com parênteses, colchetes e chaves; propriedades (comutativa, associativa, distributiva, elemento neutro);
cálculo mental e problemas.
Erros: resolver a expressão da esquerda para a direita ignorando a prioridade, esquecer o resto, trocar dividendo e divisor.
"""
import random
from br_common import lesson, mix, reais
from br_9 import M, d, bank, unit

R = random.Random(86002)


def s1_contas():
    k = R.choice(["+", "−", "×", "÷"])
    if k == "+":
        a, b = R.randint(10000, 900000), R.randint(1000, 90000)
        return M("Quanto é %s + %s?" % (d(a), d(b)), d(a + b), [d(a + b - 1000), d(a + b + 10), d(a + b + 10000)], "%s + %s = <b>%s</b>." % (d(a), d(b), d(a + b)))
    if k == "−":
        a, b = R.randint(20000, 900000), R.randint(1000, 19999)
        return M("Quanto é %s − %s?" % (d(a), d(b)), d(a - b), [d(a - b + 1000), d(a - b - 10), d(a + b)], "%s − %s = <b>%s</b>. Confira: %s + %s = %s." % (d(a), d(b), d(a - b), d(a - b), d(b), d(a)))
    if k == "×":
        a, b = R.randint(120, 999), R.randint(12, 99)
        return M("Quanto é %s × %s?" % (d(a), d(b)), d(a * b), [d(a * (b // 10) + a * (b % 10)), d(a * b + a), d(a * b - 10 * a)], "%s × %s = <b>%s</b>." % (d(a), d(b), d(a * b)))
    b, q = R.randint(12, 48), R.randint(105, 999)
    return M("Quanto é %s ÷ %d?" % (d(b * q), b), d(q), [d(q * 10), d(q + 10), d(q - 1)], "%d × %s = %s, então %s ÷ %d = <b>%s</b>." % (b, d(q), d(b * q), d(b * q), b, d(q)))


def s2_resto():
    b, q, r = R.randint(6, 35), R.randint(12, 250), None
    r = R.randint(1, b - 1)
    n = b * q + r
    k = R.choice(["q", "r", "rel"])
    if k == "q":
        return M("Na divisão de %s por %d, qual é o quociente?" % (d(n), b), d(q), [d(q + 1), d(r), d(q * 10)], "%d × %s = %s e sobram %d: quociente <b>%s</b>." % (b, d(q), d(b * q), r, d(q)))
    if k == "r":
        return M("Na divisão de %s por %d, qual é o resto?" % (d(n), b), d(r), [d(b - r), d(r + 1) if r + 1 < b else d(r - 1), "0"], "%d × %s = %s; %s − %s = <b>%d</b>." % (b, d(q), d(b * q), d(n), d(b * q), r))
    return M("Numa divisão, o divisor é %d, o quociente é %s e o resto é %d. Qual é o dividendo?" % (b, d(q), r), d(n), [d(b * q), d(b * q - r), d(b * (q + r))],
             "Dividendo = divisor × quociente + resto = %d × %s + %d = <b>%s</b>." % (b, d(q), r, d(n)))


def expr_q():
    t = R.choice(range(6))
    a, b, c, e = R.randint(2, 9), R.randint(2, 9), R.randint(2, 12), R.randint(2, 6)
    if t == 0:
        return "%d + %d × %d" % (c, a, b), c + a * b, (c + a) * b
    if t == 1:
        return "(%d + %d) × %d" % (c, a, b), (c + a) * b, c + a * b
    if t == 2:
        return "%d − %d × %d + %d" % (a * b + c + 10, a, b, e), a * b + c + 10 - a * b + e, (a * b + c + 10 - a) * b + e
    if t == 3:
        return "%d ÷ %d + %d × %d" % (a * b * 2, a, c, e), b * 2 + c * e, (b * 2 + c) * e
    if t == 4:
        return "[%d + (%d − %d) × %d] ÷ %d" % (a * e, b + c, c, a, a), (a * e + b * a) // a, None
    return "{%d × [%d + (%d − %d)]} − %d" % (e, a, b + c, c, a), e * (a + b) - a, e * a + b - a


def s3_expressoes():
    q, v, w = expr_q()
    if v < 0 or (w is not None and w == v):
        return None
    ws = [d(w) if w is not None and w >= 0 else d(v + 2), d(v + 1), d(v * 2), d(v - 3) if v > 3 else d(v + 5)]
    return M("Calcule: %s" % q, d(v), ws, "Primeiro os parênteses, colchetes e chaves; depois × e ÷; por fim + e −. Resultado: <b>%s</b>." % d(v))


s4_props = bank(R, [
    ("A propriedade usada em 25 × 37 × 4 = 25 × 4 × 37 é a…", "comutativa", ["distributiva", "do elemento neutro", "da subtração"]),
    ("A conta 8 × 47 = 8 × 40 + 8 × 7 usa a propriedade…", "distributiva", ["comutativa", "associativa da adição", "do elemento neutro"]),
    ("Qual é o elemento neutro da multiplicação?", "1", ["0", "10", "não existe"]),
    ("Qual é o elemento neutro da adição?", "0", ["1", "10", "não existe"]),
    ("Qual operação <b>não</b> é comutativa?", "a subtração", ["a adição", "a multiplicação", "todas são comutativas"]),
    ("Por que não existe divisão por zero?", "nenhum número vezes 0 dá um número diferente de 0", ["porque o resultado é sempre 0", "porque o resultado é 1", "porque 0 é ímpar"]),
    ("(17 + 25) + 75 = 17 + (25 + 75) usa a propriedade…", "associativa", ["distributiva", "comutativa da multiplicação", "do elemento neutro"]),
    ("Para calcular 99 × 6 de cabeça, um bom caminho é…", "100 × 6 − 6", ["99 + 6", "90 × 6 + 6", "100 × 6 + 6"]),
    ("Qual é o resultado de 0 ÷ 9?", "0", ["9", "não existe", "1"]),
    ("Se a × b = 0, então…", "a ou b é zero", ["a e b são 1", "a = b", "a é sempre 0"]),
    ("O dobro de um número mais o triplo do mesmo número é igual a…", "5 vezes o número", ["6 vezes o número", "o número", "2 vezes o número"]),
    ("Numa divisão, o resto é sempre…", "menor que o divisor", ["maior que o divisor", "igual ao quociente", "zero"]),
], "s4_props")


def s5_mental():
    k = R.choice(["x5", "x25", "x99", "soma", "x11"])
    if k == "x5":
        n = R.randint(12, 99) * 2
        return M("Calcule de cabeça: %d × 5 (dica: × 10 ÷ 2)." % n, d(n * 5), [d(n * 10), d(n * 5 + 10), d(n // 2)], "%d × 10 = %s; ÷ 2 = <b>%s</b>." % (n, d(n * 10), d(n * 5)))
    if k == "x25":
        n = R.randint(3, 40) * 4
        return M("Calcule de cabeça: %d × 25 (dica: × 100 ÷ 4)." % n, d(n * 25), [d(n * 100), d(n * 25 + 25), d(n * 20)], "%d × 100 = %s; ÷ 4 = <b>%s</b>." % (n, d(n * 100), d(n * 25)))
    if k == "x99":
        n = R.randint(3, 60)
        return M("Calcule de cabeça: %d × 99." % n, d(n * 99), [d(n * 100), d(n * 100 + n), d(n * 99 + 9)], "%d × 100 − %d = <b>%s</b>." % (n, n, d(n * 99)))
    if k == "x11":
        n = R.randint(12, 89)
        return M("Calcule de cabeça: %d × 11." % n, d(n * 11), [d(n * 10), d(n * 11 + 11), d(n * 12)], "%d × 10 + %d = <b>%s</b>." % (n, n, d(n * 11)))
    a = R.randint(101, 899)
    b = 1000 - a + R.randint(-3, 3)
    return M("Calcule de cabeça: %d + %d + %d." % (a, 250, b), d(a + 250 + b), [d(a + b), d(a + 250 + b + 100), d(a + 250 + b - 10)], "%d + %d = %s; + 250 = <b>%s</b>." % (a, b, d(a + b), d(a + 250 + b)))


def s6_problemas():
    k = R.choice(["onibus", "caixas", "salario", "estoque", "parcelas", "km"])
    if k == "onibus":
        n, c = R.randint(150, 900), R.choice([40, 42, 44, 46, 48])
        q, r = divmod(n, c)
        if r == 0:
            return None
        return M("Uma escola vai levar %d alunos a uma excursão em ônibus de %d lugares. Quantos ônibus, no mínimo, são necessários?" % (n, c), d(q + 1), [d(q), d(r), d(q + 2)],
                 "%d ÷ %d = %d e resto %d; os %d alunos que sobram precisam de mais um ônibus: <b>%d</b>." % (n, c, q, r, r, q + 1))
    if k == "caixas":
        n, c = R.randint(500, 3000), R.choice([12, 24, 30, 36])
        q, r = divmod(n, c)
        if r == 0:
            return None
        return M("Uma fábrica produziu %s ovos e os coloca em caixas de %d. Quantas caixas ficam completas?" % (d(n), c), d(q), [d(q + 1), d(r), d(n // 10)], "%s ÷ %d = %d e resto %d: <b>%d caixas</b> completas." % (d(n), c, q, r, q))
    if k == "salario":
        s, g = R.choice([1800, 2100, 2500, 3200]), R.choice([650, 720, 890, 1150])
        o = R.randint(150, 400)
        return M("Ana recebe %s por mês. Gasta %s com aluguel e %s com mercado. Quanto sobra?" % (reais(s * 100), reais(g * 100), reais(o * 100)), reais((s - g - o) * 100), [reais((s - g + o) * 100), reais((g + o) * 100), reais((s - g) * 100)],
                 "%d − %d − %d = <b>%s</b>." % (s, g, o, reais((s - g - o) * 100)))
    if k == "estoque":
        c, p, v = R.randint(12, 40), R.randint(24, 60), R.randint(100, 500)
        return M("Uma loja recebeu %d caixas com %d cadernos cada e já vendeu %d cadernos. Quantos cadernos ainda há?" % (c, p, v), d(c * p - v), [d(c * p + v), d(c * p), d(c + p - v) if c + p > v else d(c * p - v + 10)],
                 "%d × %d = %s; %s − %d = <b>%s</b>." % (c, p, d(c * p), d(c * p), v, d(c * p - v)))
    if k == "parcelas":
        n, v = R.choice([10, 12, 15, 18, 24]), R.randint(35, 250)
        e = R.choice([100, 200, 300, 500])
        return M("Uma TV foi paga com uma entrada de %s e mais %d parcelas de %s. Qual foi o preço total?" % (reais(e * 100), n, reais(v * 100)), reais((e + n * v) * 100), [reais(n * v * 100), reais((e + v) * n * 100), reais((e + n + v) * 100)],
                 "%d + %d × %d = <b>%s</b>." % (e, n, v, reais((e + n * v) * 100)))
    v, h = R.choice([60, 70, 80, 90]), R.randint(3, 9)
    t = R.randint(20, 120)
    return M("Um caminhão percorre %d km por hora. Depois de %d horas, faltam %d km para chegar. Qual é a distância total da viagem?" % (v, h, t), "%s km" % d(v * h + t), ["%s km" % d(v * h), "%s km" % d(v * h - t), "%s km" % d(v + h + t)],
             "%d × %d = %d; %d + %d = <b>%s km</b>." % (v, h, v * h, v * h, t, d(v * h + t)))


def main():
    seen = set()
    sets = [
        ("As quatro operações", mix(R, seen, [(s1_contas, 20)])),
        ("Divisão com resto", mix(R, seen, [(s2_resto, 20)])),
        ("Expressões numéricas", mix(R, seen, [(s3_expressoes, 20)])),
        ("Propriedades e cálculo mental", mix(R, seen, [(s4_props, 10), (s5_mental, 10)])),
        ("Problemas", mix(R, seen, [(s6_problemas, 20)])),
    ]
    body = lesson(
        ["Nas <b>expressões numéricas</b>, resolva primeiro os parênteses ( ), depois os colchetes [ ] e as chaves { }.",
         "Dentro de cada um, faça antes a multiplicação e a divisão (na ordem em que aparecem) e depois a adição e a subtração.",
         "Na divisão com resto: dividendo = divisor × quociente + resto, e o resto é sempre menor que o divisor.",
         "As propriedades ajudam no cálculo mental: 25 × 4 = 100, 8 × 47 = 8 × 40 + 8 × 7."],
        [("5 + 3 × 4", ["3 × 4 = 12", "5 + 12"], "17"),
         ("(5 + 3) × 4", ["5 + 3 = 8", "8 × 4"], "32"),
         ("125 ÷ 9", ["9 × 13 = 117", "125 − 117 = 8"], "13 e resto 8")],
        [["Fazer as contas da esquerda para a direita", "× e ÷ vêm antes de + e −."],
         ["Esquecer o resto nos problemas", "Sobraram alunos? Precisa de mais um ônibus."],
         ["Achar que dá para dividir por zero", "A divisão por zero não existe."]])
    faq = [("Qual é a ordem das operações numa expressão numérica?", "Primeiro o que está dentro de parênteses, colchetes e chaves; depois multiplicações e divisões; por último adições e subtrações, sempre da esquerda para a direita."),
           ("O que o 6º ano estuda sobre operações?", "Resolver e elaborar problemas com as quatro operações com números naturais, usando estratégias variadas, com compreensão dos processos (EF06MA03).")]
    unit(R, "operacoes-com-numeros-naturais", "N", ["EF06MA03"],
         "Resolver e elaborar problemas que envolvam cálculos (mentais ou escritos, exatos ou aproximados) com números naturais, por meio de estratégias variadas, com compreensão dos processos neles envolvidos com e sem uso de calculadora",
         "Operações com números naturais e expressões numéricas", "Operações com números naturais",
         "Atividades de matemática para o 6º ano sobre operações com números naturais: as quatro operações, divisão com resto, expressões numéricas, propriedades, cálculo mental e problemas. 100 exercícios com gabarito.",
         "Parênteses → × e ÷ → + e −", "Dividendo = divisor × quociente + resto",
         body, faq, sets, 2, grade="6-ano")


if __name__ == "__main__":
    main()
