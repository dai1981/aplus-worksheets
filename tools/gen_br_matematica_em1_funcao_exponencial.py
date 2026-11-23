# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Função exponencial (EM13MAT304, EM13MAT403)
  python3 tools/gen_br_matematica_em1_funcao_exponencial.py
f(x) = a · bˣ: valores, crescente (b > 1) ou decrescente (0 < b < 1), ponto (0, a), imagem (y > 0);
equações exponenciais (mesma base); gráficos; modelos de crescimento e decaimento (população, meia-vida, juros).
Erros: achar que 2ˣ é decrescente para x negativo, igualar expoentes sem igualar bases, usar a função afim para crescimento percentual.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, bank, mix, lesson, unit, curva, R2, num

R = random.Random(91010)
SUP = str.maketrans("0123456789-+x", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ˣ")


def pw(b, e):
    return (("(%s)" % fq(b)) if F(b).denominator != 1 else d(b)) + str(e).translate(SUP)


def s1_valor():
    k = R.choice(["val", "val", "tipo", "ponto", "img"])
    b = R.choice([2, 3, 4, 5, 10, F(1, 2), F(1, 3)])
    a = R.choice([1, 1, 2, 3, 5])
    if k == "val":
        x = R.randint(-3, 4)
        v = a * F(b) ** x
        if abs(v) > 10 ** 5:
            return None
        fx = ("f(x) = %s" % ("" if a == 1 else "%d · " % a)) + pw(b, "x")
        return M("Para %s, quanto vale f(%s)?" % (fx, d(x)), fq(v), [fq(a * F(b) * x) if x else fq(a * F(b)), fq(a * F(b) ** (-x)) if x else fq(v + 1), fq((a * F(b)) ** x) if a != 1 else fq(F(b) ** (x + 1))],
                 "%s%s = <b>%s</b>." % ("%d · " % a if a != 1 else "", pw(b, x), fq(v)))
    fx = ("f(x) = %s" % ("" if a == 1 else "%d · " % a)) + pw(b, "x")
    if k == "tipo":
        return M("A função %s é…" % fx, "crescente" if F(b) > 1 else "decrescente", ["decrescente" if F(b) > 1 else "crescente", "constante", "crescente só para x &gt; 0"],
                 "Base %s %s 1: <b>%s</b>." % (fq(b), "&gt;" if F(b) > 1 else "&lt;", "crescente" if F(b) > 1 else "decrescente"))
    if k == "ponto":
        return M("Em que ponto o gráfico de %s corta o eixo y?" % fx, "(0, %d)" % a, ["(0, 0)", "(%d, 0)" % a, "(0, %s)" % fq(a * F(b))], "f(0) = %s%s⁰ = %d: <b>(0, %d)</b>." % ("%d · " % a if a != 1 else "", fq(b), a, a))
    return M("Qual é o conjunto imagem de %s?" % fx, "y &gt; 0", ["todos os reais", "y ≥ %d" % a, "y &lt; 0"], "bˣ é sempre positivo: Im = { <b>y &gt; 0</b> }.")


def s2_equacao():
    b = R.choice([2, 3, 5])
    k = R.choice(["simples", "linear", "fração", "base"])
    if k == "simples":
        x = R.randint(2, 7 if b == 2 else 4)
        return M("Resolva: %d%s = %s" % (b, "ˣ", num(b ** x)), "x = %d" % x, ["x = %d" % (b ** x // b), "x = %d" % (x + 1), "x = %d" % (x - 1)], "%s = %d%s ⇒ <b>x = %d</b>." % (num(b ** x), b, str(x).translate(SUP), x))
    if k == "linear":
        c = R.randint(-3, 3)
        x = R.randint(1, 4)
        e = x + c
        if e < 1 or b ** e > 10 ** 5:
            return None
        return M("Resolva: %d%s = %s" % (b, ("x" + ("+%d" % c if c > 0 else ("-%d" % -c if c < 0 else ""))).translate(SUP), num(b ** e)), "x = %d" % x, ["x = %d" % e, "x = %d" % (e + c), "x = %d" % (x + 1)],
                 "%s = %d%s ⇒ x %s = %d ⇒ <b>x = %d</b>." % (num(b ** e), b, str(e).translate(SUP), ("+ %d" % c) if c >= 0 else "− %d" % -c, e, x))
    if k == "fração":
        x = R.randint(1, 4 if b == 2 else 3)
        return M("Resolva: %d%s = %s" % (b, "ˣ", fq(F(1, b ** x))), "x = −%d" % x, ["x = %d" % x, "x = %s" % fq(F(1, x)), "x = −%d" % (x + 1)], "%s = %d%s ⇒ <b>x = −%d</b>." % (fq(F(1, b ** x)), b, ("-" + str(x)).translate(SUP), x))
    x = R.randint(2, 5)
    if b ** (2 * x) > 10 ** 6:
        return None
    return M("Resolva: %d%s = %s" % (b * b, "ˣ", num(b ** (2 * x))), "x = %d" % x, ["x = %d" % (2 * x), "x = %d" % (x + 1), "x = %s" % fq(F(x, 2))], "%d = %d², então %d²ˣ = %d%s ⇒ 2x = %d ⇒ <b>x = %d</b>." % (b * b, b, b, b, str(2 * x).translate(SUP), 2 * x, x))


def s3_grafico():
    b = R.choice([2, 3, F(1, 2), F(1, 3)])
    a = R.choice([1, 2])
    f = lambda x: a * float(F(b)) ** x
    g = curva([(f, "f")], (-3, 3, 1), (0, 9, 1), pts=[(0, a, "")], label="gráfico de uma função exponencial")
    fx = ("f(x) = %s" % ("" if a == 1 else "%d · " % a)) + pw(b, "x")
    others = [("f(x) = %s" % ("" if a == 1 else "%d · " % a)) + pw(1 / F(b), "x"), ("f(x) = %s" % ("" if a == 2 else "2 · ")) + pw(b, "x"), "f(x) = %sx + %d" % (fq(b) if F(b).denominator == 1 else "", a)]
    return M(g + "Qual lei corresponde ao gráfico?", fx, others, "Passa por (0, %d) e (1, %s), e é %s: <b>%s</b>." % (a, fq(a * F(b)), "crescente" if F(b) > 1 else "decrescente", fx))


def s4_modelo():
    k = R.choice(["pop", "meia", "cresc", "juros", "virus"])
    if k == "pop":
        p0 = R.choice([10000, 20000, 50000])
        t = R.choice([10, 20])
        n = R.choice([2, 3])
        return M("Uma população de %s habitantes cresce %d%% ao ano: P(t) = %s · %s%s. Qual é a população em %d anos?" % (num(p0), t, num(p0), d(F(100 + t, 100)), "ᵗ", n),
                 num(p0 * F(100 + t, 100) ** n), [num(p0 * F(100 + t * n, 100)), num(p0 * F(100 + t, 100) ** (n + 1)), num(p0 * F(t, 100) * n)],
                 "%s · %s%s = <b>%s</b>." % (num(p0), d(F(100 + t, 100)), str(n).translate(SUP), num(p0 * F(100 + t, 100) ** n)))
    if k == "meia":
        m0 = R.choice([80, 100, 160, 200, 320, 400, 640])
        h = R.choice([5, 8, 10, 30])
        n = R.choice([2, 3, 4])
        m = F(m0, 2 ** n)
        return M("Um material radioativo tem meia-vida de %d anos. De %d g, quanto resta depois de %d anos?" % (h, m0, h * n), "%s g" % d(m), ["%s g" % d(F(m0, 2 * n)), "%s g" % d(m0 - h * n) if m0 > h * n else "0 g", "%s g" % d(F(m0, 2 ** (n + 1)))],
                 "%d meias-vidas: %d ÷ 2%s = <b>%s g</b>." % (n, m0, str(n).translate(SUP), d(m)))
    if k == "cresc":
        return M("Qual modelo descreve uma quantidade que aumenta 5% ao mês, a partir de 200?", "Q(t) = 200 · 1,05ᵗ", ["Q(t) = 200 + 5t", "Q(t) = 200 · 0,95ᵗ", "Q(t) = 200 · 5ᵗ"], "Aumentar 5% é multiplicar por 1,05 a cada mês: <b>200 · 1,05ᵗ</b>.") if R.random() < 0.5 else \
            M("Qual modelo descreve um valor que perde 10% ao ano, a partir de R$ 30.000?", "V(t) = 30.000 · 0,9ᵗ", ["V(t) = 30.000 − 10t", "V(t) = 30.000 · 1,1ᵗ", "V(t) = 30.000 · 0,1ᵗ"], "Perder 10% é multiplicar por 0,9: <b>30.000 · 0,9ᵗ</b>.")
    if k == "juros":
        c = R.choice([1000, 2000, 4000])
        i = R.choice([10, 20])
        n = R.choice([2, 3])
        return M("Um capital de R$ %s rende juros compostos de %d%% ao ano: M(t) = %s · %s%s. Qual é o montante em %d anos?" % (num(c), i, num(c), d(F(100 + i, 100)), "ᵗ", n), R2(c * F(100 + i, 100) ** n),
                 [R2(c * F(100 + i * n, 100)), R2(c * F(100 + i, 100) ** (n - 1)), R2(c * F(i, 100) ** n)], "%s · %s%s = <b>%s</b>." % (num(c), d(F(100 + i, 100)), str(n).translate(SUP), R2(c * F(100 + i, 100) ** n)))
    n0 = R.choice([3, 5, 10])
    b = R.choice([2, 3])
    t = R.randint(3, 6)
    return M("O número de pessoas que recebeu uma mensagem é N(t) = %d · %d%s, t em horas. Quantas pessoas a receberam em %d horas?" % (n0, b, "ᵗ", t), num(n0 * b ** t), [num(n0 * b * t), num((n0 * b) ** t) if (n0 * b) ** t < 10 ** 9 else num(n0 * b ** (t + 1)), num(n0 * b ** (t - 1))],
             "%d · %d%s = <b>%s</b>." % (n0, b, str(t).translate(SUP), num(n0 * b ** t)))


s5_conceitos = bank(R, [
    ("Na função f(x) = bˣ, a base b deve ser…", "positiva e diferente de 1", ["qualquer número", "negativa", "maior que 10"]),
    ("Todo gráfico de f(x) = bˣ passa pelo ponto…", "(0, 1)", ["(1, 0)", "(0, 0)", "(1, 1)"]),
    ("O gráfico de f(x) = 2ˣ…", "nunca toca o eixo x", ["corta o eixo x em (0, 0)", "corta o eixo x em (1, 0)", "é uma reta"]),
    ("Uma grandeza que cresce sempre a mesma porcentagem por período segue um modelo…", "exponencial", ["afim", "quadrático", "constante"]),
    ("Se f(x) = 3ˣ, então f(x + 1) = …", "3 · f(x)", ["f(x) + 3", "f(x) + 1", "3 + f(x)"]),
    ("A função f(x) = (0,5)ˣ é…", "decrescente", ["crescente", "constante", "negativa"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Valores e propriedades", mix(R, seen, [(s1_valor, 20)])),
        ("Equações exponenciais", mix(R, seen, [(s2_equacao, 20)])),
        ("Gráficos", mix(R, seen, [(s3_grafico, 8), (s1_valor, 6), (s5_conceitos, 6)])),
        ("Crescimento e decaimento", mix(R, seen, [(s4_modelo, 20)])),
        ("Revisão", mix(R, seen, [(s2_equacao, 8), (s4_modelo, 8), (s1_valor, 4)])),
    ]
    body = lesson(
        ["<b>Função exponencial</b>: f(x) = a · bˣ, com b &gt; 0 e b ≠ 1. O gráfico passa por (0, a) e nunca toca o eixo x.",
         "b &gt; 1: <b>crescente</b>. 0 &lt; b &lt; 1: <b>decrescente</b>.",
         "<b>Equação exponencial</b>: escreva os dois lados na mesma base e iguale os expoentes: 2ˣ⁺¹ = 32 = 2⁵ ⇒ x + 1 = 5.",
         "Crescer i% por período é multiplicar por (1 + i%) a cada período: Q(t) = Q₀ · (1 + i)ᵗ. Perder i% é multiplicar por (1 − i)."],
        [("3ˣ⁻¹ = 81", ["81 = 3⁴", "x − 1 = 4"], "x = 5"),
         ("R$ 1.000 a 10% ao ano por 2 anos", ["1.000 · 1,1²"], "R$ 1.210,00")],
        [["Igualar expoentes com bases diferentes", "Primeiro escreva tudo na mesma base."],
         ["Usar soma para crescimento percentual", "Porcentagem fixa por período é multiplicação: modelo exponencial."],
         ["Achar que bˣ pode ser negativo", "bˣ &gt; 0 para todo x."]],
        curva([(lambda x: 2 ** x, "y = 2ˣ"), (lambda x: 0.5 ** x, "y = (1/2)ˣ")], (-3, 3, 1), (0, 8, 1), label="gráficos de y = 2ˣ e y = (1/2)ˣ"))
    faq = [("Como saber se uma função exponencial é crescente?", "Olhe a base: se b > 1, é crescente; se 0 < b < 1, é decrescente."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas com funções exponenciais nos quais seja necessário compreender e interpretar a variação das grandezas envolvidas, em contextos como o da Matemática Financeira, entre outros (EM13MAT304), e analisar e estabelecer relações entre as representações de funções exponencial e logarítmica, identificando domínio de validade, imagem, crescimento e decrescimento (EM13MAT403).")]
    unit(R, "funcao-exponencial", "A", ["EM13MAT304", "EM13MAT403"],
         "Resolver e elaborar problemas com funções exponenciais nos quais seja necessário compreender e interpretar a variação das grandezas envolvidas, em contextos como o da Matemática Financeira, entre outros; analisar e estabelecer relações, com ou sem apoio de tecnologias digitais, entre as representações de funções exponencial e logarítmica expressas em tabelas e em plano cartesiano, para identificar as características fundamentais (domínio, imagem, crescimento) de cada função",
         "Função exponencial: gráficos, equações e modelos", "Função exponencial",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre função exponencial: valores, crescimento e decrescimento, gráficos, equações exponenciais, meia-vida, população e juros compostos. 100 exercícios com gabarito.",
         "f(x) = a · bˣ", "b > 1: crescente; 0 < b < 1: decrescente.",
         body, faq, sets, 10, grade="1-serie")


if __name__ == "__main__":
    main()
