# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Operações com frações (Números, EF06MA09, EF06MA10)
  python3 tools/gen_br_matematica_6_operacoes_com_fracoes.py
Fração de uma quantidade (2/5 de 40); achar o todo a partir da parte; adição e subtração com o mesmo denominador e com
denominadores diferentes (MMC); números mistos; problemas.
Erros: somar numeradores e denominadores (1/2 + 1/3 = 2/5), dividir pelo numerador em vez do denominador, esquecer de simplificar.
"""
import random
from math import gcd
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, fq, unit

R = random.Random(86006)


def fr(n, dd):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, dd)


def s1_de_quantidade():
    den = R.choice([2, 3, 4, 5, 6, 8, 10])
    n = R.randint(1, den - 1)
    if gcd(n, den) != 1:
        return None
    q = den * R.randint(3, 30)
    v = q * n // den
    return M("Quanto é %s de %d?" % (fr(n, den), q), d(v), [d(q // den), d(q * den // n) if (q * den) % n == 0 and n > 1 else d(v + n), d(q - v) if q - v != v else d(v * 2)],
             "%d ÷ %d = %d; × %d = <b>%s</b>." % (q, den, q // den, n, d(v)))


def s2_todo():
    den = R.choice([3, 4, 5, 6, 8])
    n = R.randint(1, den - 1)
    if gcd(n, den) != 1:
        return None
    tot = den * R.randint(3, 15)
    p = tot * n // den
    k = R.choice(["livro", "turma", "dinheiro"])
    if k == "livro":
        q = "Li %s de um livro, o que dá %d páginas. Quantas páginas tem o livro?" % (fr(n, den), p)
        u = " páginas"
    elif k == "turma":
        q = "%s dos alunos de uma escola são %d alunos. Quantos alunos tem a escola?" % (fr(n, den), p)
        u = " alunos"
    else:
        q = "Gastei %s do meu dinheiro, o que deu %s. Quanto eu tinha?" % (fr(n, den), reais(p * 100))
        return M(q, reais(tot * 100), [reais(p * n * 100 // den) if (p * n) % den == 0 else reais((p + den) * 100), reais(p * den * 100), reais((tot - p) * 100)],
                 "%d ÷ %d = %d por parte; × %d = <b>%s</b>." % (p, n, p // n, den, reais(tot * 100)))
    return M(q, d(tot) + u, [d(p * den) + u if p * den != tot else d(tot + den) + u, d(tot - p) + u, d(p + den) + u],
             "Cada parte: %d ÷ %d = %d; o todo tem %d partes: <b>%s%s</b>." % (p, n, p // n, den, d(tot), u))


def opq(a, b, op):
    r = a + b if op == "+" else a - b
    return r


def s3_mesmo():
    den = R.randint(3, 15)
    a, b = R.sample(range(1, 2 * den), 2)
    op = R.choice(["+", "−"])
    if op == "−" and a < b:
        a, b = b, a
    r = opq(F(a, den), F(b, den), op)
    if r <= 0:
        return None
    raw = fr(a + b if op == "+" else a - b, den)
    ans = fq(r)
    ws = [fr(a + b if op == "+" else a - b, 2 * den), fq(F(a + b, den)) if op == "−" else fq(F(a - b, den)) if a > b else fr(a * b, den), raw if raw != ans else fq(r + F(1, den))]
    return M("Calcule %s %s %s (simplifique)." % (fr(a, den), op, fr(b, den)), ans, ws, "Mesmo denominador: %s os numeradores e mantenha o denominador: %s = <b>%s</b>." % ("some" if op == "+" else "subtraia", raw, ans))


def s4_diferentes():
    b1, b2 = R.sample([2, 3, 4, 5, 6, 8, 9, 10, 12], 2)
    a1, a2 = R.randint(1, b1 - 1), R.randint(1, b2 - 1)
    x, y = F(a1, b1), F(a2, b2)
    op = R.choice(["+", "−"])
    if op == "−" and x < y:
        x, y = y, x
    r = x + y if op == "+" else x - y
    if r <= 0 or x.denominator == y.denominator:
        return None
    m = x.denominator * y.denominator // gcd(x.denominator, y.denominator)
    bad = fq(F(x.numerator + y.numerator if op == "+" else abs(x.numerator - y.numerator) or 1, x.denominator + y.denominator))
    return M("Calcule %s %s %s." % (fq(x), op, fq(y)), fq(r), [bad, fq(r + F(1, m)), fq(x + y if op == "−" else abs(x - y)) if (x + y if op == "−" else abs(x - y)) != 0 else fq(F(1, m))],
             "MMC dos denominadores = %d: %s %s %s = <b>%s</b>." % (m, fr(x.numerator * m // x.denominator, m), op, fr(y.numerator * m // y.denominator, m), fq(r)))


def s5_problemas():
    k = R.choice(["pizza", "terreno", "garrafa", "tempo", "salario", "corrida"])
    if k == "pizza":
        a, b = R.choice([(F(1, 4), F(1, 3)), (F(1, 2), F(1, 3)), (F(3, 8), F(1, 4)), (F(1, 6), F(1, 3)), (F(2, 5), F(1, 4))])
        r = 1 - a - b
        return M("Ana comeu %s de uma pizza e Bruno comeu %s. Que fração da pizza sobrou?" % (fq(a), fq(b)), fq(r), [fq(a + b), fq(F(a.numerator + b.numerator, a.denominator + b.denominator)), fq(1 - a)],
                 "Comeram %s + %s = %s; sobrou 1 − %s = <b>%s</b>." % (fq(a), fq(b), fq(a + b), fq(a + b), fq(r)))
    if k == "terreno":
        a, b = R.choice([(F(2, 5), F(1, 3)), (F(1, 4), F(1, 2)), (F(3, 10), F(2, 5)), (F(1, 6), F(1, 2))])
        A = R.choice([600, 900, 1200, 1800])
        if (A * (1 - a - b)).denominator != 1:
            return None
        return M("Num terreno de %s m², %s é horta e %s é jardim. Quantos m² sobram?" % (d(A), fq(a), fq(b)), "%s m²" % d(A * (1 - a - b)), ["%s m²" % d(A * (a + b)), "%s m²" % d(A * (1 - a)), "%s m²" % d(A * b)],
                 "Sobra 1 − %s − %s = %s; %s de %s = <b>%s m²</b>." % (fq(a), fq(b), fq(1 - a - b), fq(1 - a - b), d(A), d(A * (1 - a - b))))
    if k == "garrafa":
        a, b = R.choice([(F(3, 4), F(1, 2)), (F(2, 3), F(1, 4)), (F(5, 6), F(1, 3)), (F(7, 8), F(1, 2))])
        return M("Uma jarra tinha %s de litro de suco. Bebemos %s de litro. Quanto sobrou?" % (fq(a), fq(b)), fq(a - b) + " de litro", [fq(a + b) + " de litro", fq(F(a.numerator - b.numerator, a.denominator - b.denominator)) + " de litro" if a.denominator != b.denominator and a.numerator > b.numerator else fq(b) + " de litro", fq(a - b + F(1, 12)) + " de litro"],
                 "%s − %s = <b>%s</b> de litro." % (fq(a), fq(b), fq(a - b)))
    if k == "tempo":
        a, b = R.choice([(F(1, 4), F(1, 3)), (F(1, 2), F(1, 4)), (F(1, 3), F(1, 6)), (F(3, 4), F(1, 6))])
        r = a + b
        return M("Estudei %s de hora de manhã e %s de hora à tarde. Quantos minutos estudei?" % (fq(a), fq(b)), "%s minutos" % d(r * 60), ["%s minutos" % d((a - b) * 60 if a > b else (b - a) * 60), "%s minutos" % d(a * 60), "%s minutos" % d(r * 60 + 10)],
                 "%s + %s = %s de hora = <b>%s minutos</b>." % (fq(a), fq(b), fq(r), d(r * 60)))
    if k == "salario":
        s = R.choice([1800, 2400, 3000, 3600])
        a, b = R.choice([(F(1, 3), F(1, 4)), (F(2, 5), F(1, 6)), (F(1, 2), F(1, 5)), (F(1, 4), F(1, 6))])
        if (s * (1 - a - b)).denominator != 1:
            return None
        return M("Lia ganha %s. Gasta %s com aluguel e %s com comida. Quanto sobra?" % (reais(s * 100), fq(a), fq(b)), reais(int(s * (1 - a - b)) * 100), [reais(int(s * (a + b)) * 100), reais(int(s * (1 - a)) * 100), reais(int(s * a) * 100)],
                 "Sobra %s do salário: %s de %d = <b>%s</b>." % (fq(1 - a - b), fq(1 - a - b), s, reais(int(s * (1 - a - b)) * 100)))
    tot = R.choice([10, 12, 15, 20, 21])
    a = R.choice([F(1, 2), F(1, 3), F(2, 5), F(3, 4)])
    if (tot * a).denominator != 1:
        return None
    return M("Numa corrida de %d km, Rui já correu %s do percurso. Quantos km faltam?" % (tot, fq(a)), "%s km" % d(tot * (1 - a)), ["%s km" % d(tot * a), "%s km" % d(tot - a.numerator), "%s km" % d(tot * (1 - a) + 1)],
             "Faltam %s de %d = <b>%s km</b>." % (fq(1 - a), tot, d(tot * (1 - a))))


def main():
    seen = set()
    sets = [
        ("Fração de uma quantidade", mix(R, seen, [(s1_de_quantidade, 20)])),
        ("Achar o todo pela parte", mix(R, seen, [(s2_todo, 20)])),
        ("Somar e subtrair com o mesmo denominador", mix(R, seen, [(s3_mesmo, 20)])),
        ("Denominadores diferentes", mix(R, seen, [(s4_diferentes, 20)])),
        ("Problemas", mix(R, seen, [(s5_problemas, 20)])),
    ]
    body = lesson(
        ["Para achar 3/5 de 40: divida pelo denominador e multiplique pelo numerador: 40 ÷ 5 × 3 = 24.",
         "Para achar o todo: se 3/5 do livro são 60 páginas, cada 1/5 tem 20 páginas e o livro tem 5 × 20 = 100.",
         "Com o mesmo denominador, some ou subtraia só os numeradores: 2/7 + 3/7 = 5/7.",
         "Com denominadores diferentes, primeiro escreva frações equivalentes com o mesmo denominador (use o MMC)."],
        [("1/2 + 1/3", ["MMC(2, 3) = 6", "3/6 + 2/6"], "5/6"),
         ("3/4 − 1/6", ["MMC(4, 6) = 12", "9/12 − 2/12"], "7/12")],
        [["Somar numeradores e denominadores", "1/2 + 1/3 não é 2/5."],
         ["Dividir pelo numerador", "3/5 de 40: divida por 5."],
         ["Não simplificar o resultado", "4/8 = 1/2."]])
    faq = [("Como somar frações com denominadores diferentes?", "Encontre o MMC dos denominadores, escreva frações equivalentes com esse denominador e some os numeradores. Depois simplifique, se der."),
           ("O que a BNCC pede no 6º ano?", "Resolver e elaborar problemas que envolvam o cálculo da fração de uma quantidade (EF06MA09) e problemas de adição ou subtração com números racionais positivos na forma fracionária (EF06MA10).")]
    unit(R, "operacoes-com-fracoes", "N", ["EF06MA09", "EF06MA10"],
         "Resolver e elaborar problemas que envolvam o cálculo da fração de uma quantidade e cujo resultado seja um número natural, com e sem uso de calculadora; resolver e elaborar problemas que envolvam adição ou subtração com números racionais positivos na representação fracionária",
         "Operações com frações: fração de quantidade, adição e subtração", "Operações com frações",
         "Atividades de matemática para o 6º ano sobre operações com frações: fração de uma quantidade, achar o todo, adição e subtração com o mesmo denominador e com denominadores diferentes e problemas. 100 exercícios com gabarito.",
         "Denominadores diferentes: use o MMC.", "3/5 de 40 = 40 ÷ 5 × 3",
         body, faq, sets, 6, grade="6-ano")


if __name__ == "__main__":
    main()
