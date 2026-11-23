# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Função logarítmica (EM13MAT403, EM13MAT305)
  python3 tools/gen_br_matematica_em1_funcao_logaritmica.py
f(x) = log_b x: domínio (x > 0), ponto (1, 0), crescente (b > 1) ou decrescente; inversa da exponencial (gráficos
simétricos em relação a y = x); equações logarítmicas; equações exponenciais resolvidas com logaritmos.
Erros: esquecer a condição de existência, achar que o gráfico corta o eixo y, igualar o logaritmando à base.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, expr, bank, mix, lesson, unit, curva, num
import math

R = random.Random(91012)
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def lg(b, a):
    return "log%s %s" % (str(b).translate(SUB), a) if b != 10 else "log %s" % a


def s1_props():
    b = R.choice([2, 3, 5, 10])
    k = R.choice(["dom", "dom", "ponto", "tipo", "val", "inv"])
    if k == "dom":
        a, c = R.choice([1, 2, 3, -1]), R.randint(-6, 6)
        if c == 0:
            return None
        z = F(-c, a)
        sgn = "&gt;" if a > 0 else "&lt;"
        return M("Qual é o domínio de f(x) = %s?" % lg(b, "(%s)" % expr([(a, "x"), (c, "")])), "x %s %s" % (sgn, fq(z)), ["x %s %s" % ("&lt;" if a > 0 else "&gt;", fq(z)), "x &gt; 0", "x ≥ %s" % fq(z)],
                 "O logaritmando deve ser positivo: %s &gt; 0 ⇒ <b>x %s %s</b>." % (expr([(a, "x"), (c, "")]), sgn, fq(z)))
    if k == "ponto":
        return M("Em que ponto o gráfico de f(x) = %s corta o eixo x?" % lg(b, "x"), "(1, 0)", ["(0, 1)", "(%d, 0)" % b, "(0, 0)"], "%s = 0, então o ponto é <b>(1, 0)</b>." % lg(b, "1"))
    if k == "tipo":
        bb = R.choice([2, 3, 10, F(1, 2), F(1, 3)])
        bt = fq(bb) if F(bb).denominator != 1 else str(bb)
        txt = "log<sub>%s</sub> x" % bt
        return M("A função f(x) = %s é…" % txt, "crescente" if F(bb) > 1 else "decrescente", ["decrescente" if F(bb) > 1 else "crescente", "constante", "crescente só para x &gt; 1"],
                 "Base %s %s 1: <b>%s</b>." % (bt, "&gt;" if F(bb) > 1 else "&lt;", "crescente" if F(bb) > 1 else "decrescente"))
    if k == "val":
        x = R.randint(-2, 5 if b < 5 else 3)
        a = F(b) ** x
        txt = num(a) if a.denominator == 1 else fq(a)
        return M("Para f(x) = %s, quanto vale f(%s)?" % (lg(b, "x"), txt), d(x), [d(-x) if x else "1", num(a * b) if a.denominator == 1 else d(x + 1), d(x + 1)],
                 "%d%s = %s: f(%s) = <b>%s</b>." % (b, str(x).translate(SUP), txt, txt, d(x)))
    return M("A função inversa de f(x) = %d%s é…" % (b, "ˣ"), "g(x) = %s" % lg(b, "x"), ["g(x) = x%s" % str(b).translate(SUP), "g(x) = %s" % fq(F(1, b)) + "ˣ" if b < 10 else "g(x) = (0,1)ˣ", "g(x) = x ÷ %d" % b],
             "A inversa da exponencial de base %d é o <b>logaritmo de base %d</b>; os gráficos são simétricos em relação à reta y = x." % (b, b))


def s2_eq():
    b = R.choice([2, 3, 5, 10])
    k = R.choice(["simples", "linear", "soma"])
    if k == "simples":
        n = R.randint(1, 4 if b < 10 else 3)
        c = R.randint(-5, 5)
        x = b ** n - c
        return M("Resolva: %s = %d" % (lg(b, "(x %s)" % (("+ %d" % c) if c >= 0 else "− %d" % -c)), n), "x = %s" % num(x), ["x = %s" % num(b ** n + c) if c else "x = %d" % (b * n), "x = %d" % (b * n - c), "x = %d" % (n - c)],
                 "x %s = %d%s = %s ⇒ <b>x = %s</b> (e x %s &gt; 0, ok)." % (("+ %d" % c) if c >= 0 else "− %d" % -c, b, str(n).translate(SUP), num(b ** n), num(x), ("+ %d" % c) if c >= 0 else "− %d" % -c))
    if k == "linear":
        n = R.randint(1, 3)
        a = R.choice([2, 3, 4])
        c = R.randint(-6, 6)
        x = F(b ** n - c, a)
        if x.denominator != 1:
            return None
        return M("Resolva: %s = %d" % (lg(b, "(%s)" % expr([(a, "x"), (c, "")])), n), "x = %s" % d(x), ["x = %s" % d(F(b * n - c, a)) if F(b * n - c, a) != x else "x = %s" % d(x + 1), "x = %s" % d(b ** n - c), "x = %s" % d(F(b ** n + c, a))],
                 "%s = %s ⇒ <b>x = %s</b>." % (expr([(a, "x"), (c, "")]), num(b ** n), d(x)))
    p, q = R.choice([(2, 8), (4, 2), (2, 16), (4, 4), (8, 2), (2, 2)])
    b = 2
    x = p * q
    return M("Resolva: log₂ x = log₂ %d + log₂ %d" % (p, q), "x = %d" % x, ["x = %d" % (p + q), "x = %d" % (int(math.log2(p) + math.log2(q))), "x = %d" % (2 ** (p + q)) if p + q < 10 else "x = %d" % (x * 2)],
             "log₂ %d + log₂ %d = log₂ %d ⇒ <b>x = %d</b>." % (p, q, x, x))


LOG = {2: F(301, 1000), 3: F(477, 1000), 4: F(602, 1000), 5: F(699, 1000), 6: F(778, 1000), 7: F(845, 1000), 9: F(954, 1000), 10: F(1)}


def s3_exp_log():
    k = R.choice(["eq", "eq", "eq", "cresc"])
    if k == "eq":
        b = R.choice([2, 3, 5])
        a = R.choice([x for x in (2, 3, 5, 6, 7, 10) if x != b and not (b == 2 and x in (4,)) and not (b == 3 and x == 9)])
        v = LOG[a] / LOG[b]
        info = "log %d = %s e log %d = %s" % (b, d(LOG[b]), a, d(LOG[a])) if a != 10 else "log %d = %s" % (b, d(LOG[b]))
        return M("Resolva %d%s = %d usando %s." % (b, "ˣ", a, info), "x ≈ %s" % d(v, 2), ["x ≈ %s" % d(LOG[b] / LOG[a], 2), "x ≈ %s" % d(F(a, b), 2), "x ≈ %s" % d(LOG[a] - LOG[b], 2) if LOG[a] > LOG[b] else "x ≈ %s" % d(LOG[a] * LOG[b], 2)],
                 "x = log %d ÷ log %d = %s ÷ %s ≈ <b>%s</b>." % (a, b, d(LOG[a]), d(LOG[b]), d(v, 2)))
    n = R.choice([3, 5, 6, 10, 100, 1000])
    v = (LOG[n] if n in LOG else F({100: 2, 1000: 3}[n])) / LOG[2]
    lv = LOG[n] if n in LOG else F({100: 2, 1000: 3}[n])
    return M("Uma colônia de bactérias dobra a cada hora. Em quanto tempo ela fica %s vezes maior? (log 2 = 0,301%s)" % (num(n), "; log %d = %s" % (n, d(LOG[n])) if n in LOG and n != 10 else ""), "cerca de %s h" % d(v, 1), ["%s h" % d(F(n, 2), 1), "cerca de %s h" % d(v / 2, 1), "%s h" % d(lv, 1)],
             "2ᵗ = %s ⇒ t = %s ÷ 0,301 ≈ <b>%s h</b>." % (num(n), d(lv), d(v, 1)))


def s4_grafico():
    b = R.choice([2, 3, F(1, 2)])
    f = lambda x: math.log(x) / math.log(float(F(b)))
    g = curva([(f, "f")], (0, 9, 1), (-4, 4, 1), pts=[(1, 0, ""), (float(F(b)) if F(b) > 1 else 2, f(float(F(b))) if F(b) > 1 else -1, "")], label="gráfico de uma função logarítmica")
    bt = fq(b) if F(b).denominator != 1 else str(b)
    ans = "f(x) = log<sub>%s</sub> x" % bt
    others = ["f(x) = log<sub>%s</sub> x" % (fq(1 / F(b)) if F(1 / F(b)).denominator != 1 else str(1 / F(b))), "f(x) = %s<sup>x</sup>" % bt, "f(x) = log<sub>%d</sub> x" % (4 if b == 2 else (9 if b == 3 else 3))]
    return M(g + "Qual lei corresponde ao gráfico?", ans, others, "Passa por (1, 0) e por (%s, %s), e é %s: <b>%s</b>." % (bt if F(b) > 1 else "2", "1" if F(b) > 1 else "−1", "crescente" if F(b) > 1 else "decrescente", ans))


s5_conceitos = bank(R, [
    ("O gráfico de f(x) = log₂ x…", "não corta o eixo y", ["corta o eixo y em (0, 1)", "passa por (0, 0)", "é uma reta"]),
    ("O domínio de f(x) = log x é…", "x &gt; 0", ["todos os reais", "x ≥ 0", "x &gt; 1"]),
    ("Os gráficos de y = 2ˣ e y = log₂ x são simétricos em relação…", "à reta y = x", ["ao eixo x", "ao eixo y", "à origem"]),
    ("A imagem de f(x) = log₃ x é…", "todos os reais", ["y &gt; 0", "y ≥ 1", "x &gt; 0"]),
    ("Se log₂ x = 5, então x = …", "32", ["10", "25", "2,5"]),
    ("Para resolver 2ˣ = 7, usamos…", "logaritmos: x = log 7 ÷ log 2", ["x = 7 ÷ 2", "x = 7 − 2", "x = √7"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Domínio e propriedades", mix(R, seen, [(s1_props, 20)])),
        ("Gráficos", mix(R, seen, [(s4_grafico, 3), (s1_props, 11), (s5_conceitos, 6)])),
        ("Equações logarítmicas", mix(R, seen, [(s2_eq, 20)])),
        ("Equações exponenciais com log", mix(R, seen, [(s3_exp_log, 20)])),
        ("Revisão", mix(R, seen, [(s2_eq, 10), (s1_props, 10)])),
    ]
    body = lesson(
        ["<b>Função logarítmica</b>: f(x) = log_b x, com b &gt; 0 e b ≠ 1. Domínio: x &gt; 0. Imagem: todos os reais.",
         "O gráfico passa por (1, 0) e por (b, 1). b &gt; 1: crescente; 0 &lt; b &lt; 1: decrescente.",
         "É a <b>inversa</b> da exponencial: y = bˣ ⇔ x = log_b y. Os gráficos são simétricos em relação a y = x.",
         "<b>Equação logarítmica</b>: log_b A = n ⇒ A = bⁿ (confira que A &gt; 0). <b>Equação exponencial</b> sem base comum: aplique log nos dois lados."],
        [("log₃ (x + 1) = 2", ["x + 1 = 3² = 9"], "x = 8"),
         ("2ˣ = 5 (log 2 = 0,301; log 5 = 0,699)", ["x = 0,699 ÷ 0,301"], "x ≈ 2,32")],
        [["Esquecer a condição de existência", "O logaritmando tem de ser positivo."],
         ["Achar que corta o eixo y", "x = 0 não está no domínio."],
         ["Fazer log_b A = n ⇒ A = n · b", "A = bⁿ."]],
        curva([(lambda x: 2 ** x, "y = 2ˣ"), (lambda x: math.log2(x) if x > 0 else None, "y = log₂ x"), (lambda x: x, "#999", "y = x")], (-3, 6, 1), (-3, 6, 1), label="gráficos de y = 2ˣ, y = log₂ x e y = x"))
    faq = [("Qual é o domínio de uma função logarítmica?", "Os valores de x que tornam o logaritmando positivo. Para f(x) = log (x − 3), o domínio é x > 3."),
           ("O que a BNCC pede?", "Analisar e estabelecer relações entre as representações de funções exponencial e logarítmica expressas em tabelas e em plano cartesiano, identificando domínio, imagem e crescimento (EM13MAT403), e resolver problemas com funções logarítmicas (EM13MAT305).")]
    unit(R, "funcao-logaritmica", "A", ["EM13MAT403", "EM13MAT305"],
         "Analisar e estabelecer relações, com ou sem apoio de tecnologias digitais, entre as representações de funções exponencial e logarítmica expressas em tabelas e em plano cartesiano, para identificar as características fundamentais (domínio, imagem, crescimento) de cada função; resolver e elaborar problemas com funções logarítmicas",
         "Função logarítmica: domínio, gráfico e equações", "Função logarítmica",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre função logarítmica: domínio, gráfico, inversa da exponencial, equações logarítmicas e equações exponenciais resolvidas com logaritmos. 100 exercícios com gabarito.",
         "log_b x: domínio x > 0", "Inversa de bˣ; passa por (1, 0).",
         body, faq, sets, 12, grade="1-serie")


if __name__ == "__main__":
    main()
