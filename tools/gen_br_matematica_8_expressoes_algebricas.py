# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Expressões algébricas e polinômios (Álgebra, EF08MA06)
  python3 tools/gen_br_matematica_8_expressoes_algebricas.py
Valor numérico de expressões com uma e duas variáveis (fórmulas: área, perímetro, IMC); monômios semelhantes; adição e subtração
de polinômios; multiplicação de monômios e de monômio por polinômio; produto de binômios (x + a)(x + b); propriedades das operações.
Usa geradores do 7º ano (linguagem algébrica) com outro sorteio.
Erros: x · x = 2x, 3x · 2x = 6x, esquecer o sinal ao subtrair polinômio, (x + 2)(x + 3) = x² + 6.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, expr, P2, par, unit

R = random.Random(88006)
l_valor, l_semel = use("gen_br_matematica_7_linguagem_algebrica_e_expressoes", 88906, "s2_valor", "s3_semelhantes")
SUP = {1: "", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹"}


def mono(c, v, e):
    if e == 0:
        return d(c)
    return expr([(c, v + SUP[e])])


def s1_monomios():
    a, b = R.choice([2, 3, 4, 5, -2, -3]), R.choice([2, 3, 4, 5, -1, -4])
    m, n = R.randint(1, 3), R.randint(1, 3)
    k = R.choice(["mul", "div"])
    if k == "mul":
        ok = mono(a * b, "x", m + n)
        return M("Calcule (%s) · (%s)." % (mono(a, "x", m), mono(b, "x", n)), ok, [mono(a * b, "x", m * n) if m * n != m + n else mono(a + b, "x", m + n), mono(a + b, "x", m + n) if a + b else mono(a * b, "x", 1), mono(a * b, "x", 1) if m + n != 1 else mono(a * b, "x", 2)],
                 "Multiplique os coeficientes e some os expoentes: <b>%s</b>." % ok)
    e = m + n
    ok = mono(b, "x", n)
    return M("Calcule (%s) ÷ (%s)." % (mono(a * b, "x", e), mono(a, "x", m)), ok, [mono(b, "x", e - m + 1) if e - m + 1 != n else mono(b, "x", n + 1), mono(a * b - a, "x", n) if a * b - a else mono(-b, "x", n), mono(-b, "x", n)],
             "Divida os coeficientes e subtraia os expoentes: <b>%s</b>." % ok)


def s2_somar():
    p = [R.randint(-6, 6) for _ in range(3)]
    q = [R.randint(-6, 6) for _ in range(3)]
    if p[0] == 0 or q[0] == 0:
        return None
    op = R.choice(["+", "−"])
    r = [x + y if op == "+" else x - y for x, y in zip(p, q)]
    if r[0] == 0:
        return None
    w = [x + y if op == "−" else x - y for x, y in zip(p, q)]
    w2 = [p[0] - q[0], p[1] + q[1], p[2] + q[2]] if op == "−" else [p[0] + q[0], p[1] + q[1], p[2] - q[2]]
    return M("Calcule (%s) %s (%s)." % (P2(*p), op, P2(*q)), P2(*r), [P2(*w) if w[0] or w[1] or w[2] else "0", P2(*w2) if w2 != r else P2(r[0], r[1] + 1, r[2]), P2(r[0], r[1], -r[2]) if r[2] else P2(r[0], -r[1], 1)],
             ("Some os termos semelhantes" if op == "+" else "Troque os sinais do segundo polinômio e some") + ": <b>%s</b>." % P2(*r))


def s3_distributiva():
    a = R.choice([2, 3, 4, 5, -2, -3])
    b, c = R.randint(-6, 6), R.randint(-9, 9)
    if b == 0 or c == 0:
        return None
    k = R.choice(["mono", "x"])
    if k == "mono":
        ok = expr([(a * b, "x"), (a * c, "")])
        return M("Calcule %s(%s)." % (d(a), expr([(b, "x"), (c, "")])), ok, [expr([(a * b, "x"), (c, "")]), expr([(a + b, "x"), (a + c, "")]), expr([(a * b, "x"), (-a * c, "")])], "Multiplique %s por cada termo: <b>%s</b>." % (d(a), ok))
    ok = expr([(a, "x²"), (a * b, "x")])
    return M("Calcule %s(%s)." % (expr([(a, "x")]), expr([(1, "x"), (b, "")])), ok, [expr([(a, "x²"), (b, "x")]), expr([(a, "x"), (a * b, "")]), expr([(a + 1, "x²"), (a * b, "x")])], "%s · x + %s · %s = <b>%s</b>." % (expr([(a, "x")]), expr([(a, "x")]), par(b), ok))


def s4_binomios():
    a, b = R.choice([x for x in range(-7, 8) if x]), R.choice([x for x in range(-7, 8) if x])
    f = lambda t: "(x %s %d)" % ("+" if t > 0 else "−", abs(t))
    ok = P2(1, a + b, a * b)
    return M("Calcule %s%s." % (f(a), f(b)), ok, [P2(1, 0, a * b), P2(1, a * b, a + b) if a * b != a + b else P2(1, a + b + 1, a * b), P2(1, a + b, -a * b)],
             "x · x + x · (%s) + (%s) · x + (%s) · (%s) = <b>%s</b>." % (d(b), d(a), d(a), d(b), ok))


def s5_formulas():
    k = R.choice(["area", "imc", "temp", "custo"])
    if k == "area":
        b, h = R.randint(3, 15), R.randint(2, 12)
        return M("A área de um triângulo é A = b · h ÷ 2. Qual é a área para b = %d cm e h = %d cm?" % (b, h), "%s cm²" % d(F(b * h, 2)), ["%d cm²" % (b * h), "%d cm²" % (b + h), "%s cm²" % d(F(b + h, 2))], "%d · %d ÷ 2 = <b>%s cm²</b>." % (b, h, d(F(b * h, 2))))
    if k == "imc":
        m, h = R.choice([(45, F(15, 10)), (64, F(16, 10)), (81, F(18, 10)), (49, F(14, 10)), (72, F(15, 10))])
        v = F(m) / (h * h)
        return M("O IMC é calculado por IMC = massa ÷ altura². Qual é o IMC de uma pessoa de %d kg e %s m?" % (m, d(h)), d(v, 1), [d(F(m) / h, 1), d(F(m) / (2 * h), 1), d(v * 2, 1)], "%d ÷ %s² = %d ÷ %s ≈ <b>%s</b>." % (m, d(h), m, d(h * h), d(v, 1)))
    if k == "temp":
        c = R.choice([0, 10, 20, 25, 30, 35, 40, 100])
        f = F(9 * c, 5) + 32
        return M("Para passar de °C para °F, usamos F = 1,8 · C + 32. Quanto é %d °C em °F?" % c, "%s °F" % d(f), ["%s °F" % d(F(9 * c, 5)), "%s °F" % d(c + 32), "%s °F" % d(F(9 * (c + 32), 5))], "1,8 · %d + 32 = <b>%s °F</b>." % (c, d(f)))
    fx, v, n = R.randint(20, 80), R.randint(2, 9), R.randint(5, 40)
    return M("O custo de uma corrida de táxi é C = %d + %d · k (k = quilômetros). Qual é o custo de %d km?" % (fx, v, n), "R$ %d,00" % (fx + v * n), ["R$ %d,00" % ((fx + v) * n), "R$ %d,00" % (fx + v + n), "R$ %d,00" % (v * n)], "%d + %d · %d = <b>R$ %d,00</b>." % (fx, v, n, fx + v * n))


def main():
    seen = set()
    sets = [
        ("Valor numérico", mix(R, seen, [(l_valor, 10), (s5_formulas, 10)])),
        ("Monômios", mix(R, seen, [(s1_monomios, 20)])),
        ("Somar e subtrair polinômios", mix(R, seen, [(s2_somar, 14), (l_semel, 6)])),
        ("Propriedade distributiva", mix(R, seen, [(s3_distributiva, 20)])),
        ("Produto de binômios", mix(R, seen, [(s4_binomios, 20)])),
    ]
    body = lesson(
        ["<b>Valor numérico</b>: troque as letras pelos números e calcule, respeitando a ordem das operações.",
         "Monômios: na multiplicação, multiplique os coeficientes e some os expoentes (3x² · 2x = 6x³); na divisão, divida e subtraia.",
         "Para somar polinômios, junte os termos semelhantes. Para subtrair, troque os sinais do polinômio que está sendo subtraído.",
         "Produto de binômios: cada termo de um multiplica cada termo do outro. (x + 2)(x + 3) = x² + 3x + 2x + 6 = x² + 5x + 6."],
        [("(2x² − 3x + 1) − (x² + x − 4)", ["2x² − 3x + 1 − x² − x + 4"], "x² − 4x + 5"),
         ("(x − 4)(x + 1)", ["x² + x − 4x − 4"], "x² − 3x − 4")],
        [["x · x = 2x", "x · x = x²; x + x = 2x."],
         ["3x · 2x = 6x", "Some os expoentes: 6x²."],
         ["(x + 2)(x + 3) = x² + 6", "Faltam os termos do meio: 3x + 2x."]])
    faq = [("Como multiplicar dois binômios?", "Use a distributiva: multiplique cada termo do primeiro por cada termo do segundo e junte os termos semelhantes."),
           ("O que a BNCC pede no 8º ano?", "Resolver e elaborar problemas que envolvam cálculo do valor numérico de expressões algébricas, utilizando as propriedades das operações (EF08MA06).")]
    unit(R, "expressoes-algebricas-e-polinomios", "A", ["EF08MA06"],
         "Resolver e elaborar problemas que envolvam cálculo do valor numérico de expressões algébricas, utilizando as propriedades das operações",
         "Expressões algébricas e polinômios", "Expressões algébricas",
         "Atividades de matemática para o 8º ano sobre expressões algébricas: valor numérico e fórmulas, monômios, adição e subtração de polinômios, propriedade distributiva e produto de binômios. 100 exercícios com gabarito.",
         "Multiplique coeficientes, some expoentes.", "(x + a)(x + b) = x² + (a + b)x + ab",
         body, faq, sets, 6, grade="8-ano")


if __name__ == "__main__":
    main()
