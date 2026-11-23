# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Função quadrática (EM13MAT302, EM13MAT402, EM13MAT502)
  python3 tools/gen_br_matematica_em1_funcao_quadratica.py
f(x) = ax² + bx + c: concavidade, ponto em que corta o eixo y, zeros (Bhaskara, Δ), vértice;
ler o gráfico (parábola) e achar a lei; y = ax² (se x dobra, y quadruplica).
Usa geradores do 9º ano (discriminante, Bhaskara) com outro sorteio.
Erros: concavidade pelo sinal de c, xv = b ÷ 2a sem o sinal de menos, achar que y dobra quando x dobra em y = ax².
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, P2, expr, bank, mix, lesson, use, unit, curva, ntab

R = random.Random(91005)
q_delta, q_bhask = use("gen_br_matematica_9_equacoes_do_2_grau", 91905, "s3_delta", "s4_bhaskara")


def lei(a, b, c):
    return "f(x) = " + P2(a, b, c)


def s1_partes():
    a = R.choice([-3, -2, -1, 1, 2, 3])
    b = R.randint(-6, 6)
    c = R.randint(-8, 8)
    k = R.choice(["conc", "c", "xv", "yv", "valor"])
    if k == "conc":
        return M("A parábola de %s tem a concavidade voltada para…" % lei(a, b, c), "cima" if a > 0 else "baixo", ["baixo" if a > 0 else "cima", "a direita", "a esquerda"],
                 "a = %d é %s: concavidade para <b>%s</b>." % (a, "positivo" if a > 0 else "negativo", "cima" if a > 0 else "baixo"))
    if k == "c":
        return M("Em que ponto a parábola de %s corta o eixo y?" % lei(a, b, c), "(0, %s)" % d(c), ["(%s, 0)" % d(c), "(0, %s)" % d(a), "(0, %s)" % d(b) if b != c else "(0, %s)" % d(c + 1)], "f(0) = c = %s: <b>(0, %s)</b>." % (d(c), d(c)))
    xv = F(-b, 2 * a)
    if k == "xv":
        if b == 0:
            return None
        return M("Qual é o x do vértice da parábola de %s?" % lei(a, b, c), fq(xv), [fq(-xv), fq(F(-b, a)), fq(F(b, 2))], "xᵥ = −b ÷ 2a = %s ÷ %s = <b>%s</b>." % (d(-b), par(2 * a), fq(xv)))
    if k == "yv":
        yv = a * xv * xv + b * xv + c
        return M("Qual é o vértice da parábola de %s?" % lei(a, b, c), "(%s, %s)" % (fq(xv), fq(yv)), ["(%s, %s)" % (fq(-xv), fq(a * xv * xv - b * xv + c)) if b else "(%s, %s)" % (fq(xv), fq(c + 1)), "(%s, %s)" % (fq(yv), fq(xv)) if xv != yv else "(0, %s)" % fq(c + 2), "(%s, %s)" % (fq(xv), d(c)) if yv != c else "(%s, %s)" % (fq(xv), d(c - 1))],
                 "xᵥ = −b ÷ 2a = %s; yᵥ = f(%s) = %s. Vértice <b>(%s, %s)</b>." % (fq(xv), fq(xv), fq(yv), fq(xv), fq(yv)))
    x = R.randint(-3, 4)
    v = a * x * x + b * x + c
    return M("Para %s, quanto vale f(%s)?" % (lei(a, b, c), d(x)), d(v), [d(a * 2 * x + b * x + c), d(-a * x * x + b * x + c) if x else d(v + 1), d(a * x * x - b * x + c) if b and x else d(v - 2)],
             "%s · %s² %s · %s %s = <b>%s</b>." % (d(a), par(x), "+ %s" % d(b) if b >= 0 else "− %s" % d(-b), par(x), "+ %s" % d(c) if c >= 0 else "− %s" % d(-c), d(v)))


def s2_grafico():
    r1, r2 = sorted(R.sample(range(-4, 5), 2))
    a = R.choice([1, -1])
    f = lambda x: a * (x - r1) * (x - r2)
    xv = F(r1 + r2, 2)
    yv = f(xv)
    if abs(yv) > 8:
        return None
    b, c = -a * (r1 + r2), a * r1 * r2
    g = curva([(f, "f")], (-5, 5, 1), (-9, 9, 3) if abs(yv) > 4 else (-6, 6, 2), label="gráfico da função quadrática f")
    k = R.choice(["zeros", "lei", "vert", "sinal"])
    if k == "zeros":
        return M(g + "Quais são os zeros da função f?", "x = %s e x = %s" % (d(r1), d(r2)), ["x = %s e x = %s" % (d(-r1), d(-r2)), "x = %s e x = %s" % (fq(xv), fq(yv)), "x = 0 e x = %s" % d(c) if c else "x = 0 e x = 1"],
                 "A parábola corta o eixo x em <b>%s e %s</b>." % (d(r1), d(r2)))
    if k == "lei":
        return M(g + "Qual é a lei da função f?", lei(a, b, c), [lei(-a, -b, -c), lei(a, -b, c) if b else lei(a, 1, c), lei(a, b, -c) if c else lei(a, b, 1)],
                 "Zeros %s e %s e concavidade para %s: f(x) = %s(x %s)(x %s) = <b>%s</b>." % (d(r1), d(r2), "cima" if a > 0 else "baixo", "" if a > 0 else "−", "− %s" % d(r1) if r1 >= 0 else "+ %s" % d(-r1), "− %s" % d(r2) if r2 >= 0 else "+ %s" % d(-r2), P2(a, b, c)))
    if k == "vert":
        return M(g + "Qual é o vértice da parábola?", "(%s, %s)" % (fq(xv), fq(yv)), ["(%s, %s)" % (fq(yv), fq(xv)) if xv != yv else "(0, 0)", "(%s, %s)" % (fq(-xv), fq(yv)) if xv else "(1, %s)" % fq(yv), "(%s, %s)" % (fq(xv), fq(-yv))],
                 "O vértice é o ponto %s: <b>(%s, %s)</b>." % ("mais baixo" if a > 0 else "mais alto", fq(xv), fq(yv)))
    return M(g + "Para quais valores de x temos f(x) %s 0?" % ("<" if a > 0 else ">"), "%s < x < %s" % (d(r1), d(r2)), ["x < %s ou x > %s" % (d(r1), d(r2)), "x > %s" % d(r2), "x < %s" % fq(xv)],
             "Entre os zeros, a parábola fica %s do eixo x: <b>%s < x < %s</b>." % ("abaixo" if a > 0 else "acima", d(r1), d(r2)))


def s3_ax2():
    k = R.choice(["dobra", "tab", "queda", "area"])
    if k == "dobra":
        m = R.choice([2, 3, 4, 10])
        return M("Em y = ax², se x é multiplicado por %d, y fica multiplicado por…" % m, str(m * m), [str(m), str(2 * m), str(m + 2) if m + 2 != m * m else str(m * 3)], "y = a(%dx)² = %d · ax²: <b>%d</b>." % (m, m * m, m * m))
    if k == "tab":
        a = R.choice([2, 3, 4, 5, F(1, 2)])
        xs = [1, 2, 3, 4]
        ys = [a * x * x for x in xs]
        return M(ntab(xs, [d(y) for y in ys]) + "Qual lei relaciona x e y?", "y = %sx²" % ("" if a == 1 else d(a)), ["y = " + expr([(a, "x")]), "y = " + expr([(3 * a, "x"), (-2 * a, "")]), "y = " + expr([(1, "x²"), (a - 1, "")]) if a != 1 else "y = 2x²"],
                 "y ÷ x² é sempre %s: <b>y = %sx²</b>." % (d(a), d(a)))
    if k == "queda":
        t = R.choice([1, 2, 3, 4])
        return M("A distância de queda livre é d = 5t² (d em metros, t em segundos). Quanto um objeto cai em %d s?" % t, "%d m" % (5 * t * t), ["%d m" % (5 * t), "%d m" % (10 * t), "%d m" % (25 * t * t)], "d = 5 · %d² = <b>%d m</b>." % (t, 5 * t * t))
    lado = R.choice([3, 4, 5, 6, 8])
    return M("Se o lado de um quadrado passa de %d cm para %d cm, a área…" % (lado, 2 * lado), "fica 4 vezes maior", ["dobra", "fica 8 vezes maior", "aumenta %d cm²" % lado], "A = ℓ²: de %d para %d cm², <b>4 vezes maior</b>." % (lado * lado, 4 * lado * lado))


s4_conceitos = bank(R, [
    ("O gráfico de uma função quadrática é…", "uma parábola", ["uma reta", "uma hipérbole", "uma circunferência"]),
    ("Se Δ < 0, a parábola…", "não corta o eixo x", ["corta o eixo x em dois pontos", "toca o eixo x em um ponto", "passa pela origem"]),
    ("Se Δ = 0, a função quadrática tem…", "um zero (duas raízes iguais)", ["dois zeros diferentes", "nenhum zero", "infinitos zeros"]),
    ("Na função f(x) = ax² + bx + c, o valor de c indica…", "onde a parábola corta o eixo y", ["a concavidade", "o x do vértice", "o número de zeros"]),
    ("O eixo de simetria da parábola passa…", "pelo vértice", ["pela origem", "pelos zeros", "pelo ponto (0, c)"]),
    ("Se a < 0, o vértice é…", "o ponto de máximo", ["o ponto de mínimo", "um zero", "o ponto (0, 0)"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Concavidade, valores e vértice", mix(R, seen, [(s1_partes, 20)])),
        ("Zeros: Δ e Bhaskara", mix(R, seen, [(q_delta, 10), (q_bhask, 10)])),
        ("Gráfico da parábola", mix(R, seen, [(s2_grafico, 20)])),
        ("y = ax² e proporcionalidade", mix(R, seen, [(s3_ax2, 14), (s4_conceitos, 6)])),
        ("Revisão", mix(R, seen, [(s1_partes, 8), (s2_grafico, 8), (q_bhask, 4)])),
    ]
    body = lesson(
        ["<b>Função quadrática</b>: f(x) = ax² + bx + c, com a ≠ 0. O gráfico é uma <b>parábola</b>.",
         "a > 0: concavidade para cima (vértice é mínimo). a < 0: para baixo (vértice é máximo). c: onde corta o eixo y.",
         "<b>Zeros</b>: Δ = b² − 4ac; x = (−b ± √Δ) ÷ 2a. Δ > 0: dois zeros; Δ = 0: um; Δ < 0: nenhum.",
         "<b>Vértice</b>: xᵥ = −b ÷ 2a e yᵥ = f(xᵥ) (ou −Δ ÷ 4a).",
         "Em y = ax², y é proporcional ao <b>quadrado</b> de x: se x dobra, y fica 4 vezes maior."],
        [("f(x) = x² − 6x + 5", ["Δ = 36 − 20 = 16", "x = (6 ± 4) ÷ 2", "xᵥ = 3, yᵥ = 9 − 18 + 5"], "zeros 1 e 5; vértice (3, −4)")],
        [["Olhar o sinal de c para a concavidade", "A concavidade depende de a."],
         ["Esquecer o sinal em xᵥ = −b ÷ 2a", "Com b = −6: xᵥ = 6 ÷ 2 = 3."],
         ["Achar que y dobra quando x dobra", "Em y = ax², y quadruplica."]],
        curva([(lambda x: x * x - 6 * x + 5, "f")], (-1, 7, 1), (-5, 10, 5), label="parábola de f(x) = x² − 6x + 5"))
    faq = [("Como encontrar o vértice da parábola?", "Calcule xᵥ = −b ÷ 2a e depois yᵥ = f(xᵥ). Em f(x) = x² − 6x + 5, xᵥ = 3 e yᵥ = −4."),
           ("O que a BNCC pede?", "Construir modelos com funções polinomiais de 2º grau (EM13MAT302), converter representações algébricas dessas funções em representações geométricas no plano cartesiano, distinguindo os casos de proporcionalidade com o quadrado (EM13MAT402), e investigar relações em tabelas que levem a y = ax² (EM13MAT502).")]
    unit(R, "funcao-quadratica", "A", ["EM13MAT302", "EM13MAT402", "EM13MAT502"],
         "Construir modelos empregando as funções polinomiais de 2º grau para resolver problemas em contextos diversos; converter representações algébricas de funções polinomiais de 2º grau em representações geométricas no plano cartesiano, distinguindo os casos nos quais uma variável for diretamente proporcional ao quadrado da outra; investigar relações entre números expressos em tabelas para representá-los no plano cartesiano, identificando padrões e criando conjecturas para generalizar e expressar algebricamente essa generalização (y = ax²)",
         "Função quadrática: parábola, zeros e vértice", "Função quadrática",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre função quadrática: concavidade, zeros com Δ e Bhaskara, vértice, gráfico da parábola, lei a partir do gráfico e y = ax². 100 exercícios com gabarito.",
         "f(x) = ax² + bx + c: o gráfico é uma parábola", "xᵥ = −b ÷ 2a; a > 0: concavidade para cima.",
         body, faq, sets, 5, grade="1-serie")


if __name__ == "__main__":
    main()
