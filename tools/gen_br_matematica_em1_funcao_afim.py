# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Função afim (EM13MAT302, EM13MAT401, EM13MAT501)
  python3 tools/gen_br_matematica_em1_funcao_afim.py
f(x) = ax + b: coeficiente angular e linear, zero da função, crescente ou decrescente; lei a partir de dois pontos,
de uma tabela ou do gráfico; função linear (proporcionalidade, b = 0); modelos (táxi, planos, salário com comissão).
Erros: trocar a e b, calcular a como Δx/Δy, achar o zero fazendo x = b/a com o sinal errado.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, expr, bank, mix, lesson, num, unit, kosy, ntab, R2

R = random.Random(91004)


def lei(a, b):
    return "f(x) = " + expr([(a, "x"), (b, "")])


def s1_coef():
    a = R.choice([x for x in range(-6, 7) if x] + [F(1, 2), F(-3, 2)])
    b = R.choice([x for x in range(-9, 10)])
    k = R.choice(["a", "b", "zero", "sinal", "valor"])
    if k == "a":
        return M("Qual é o coeficiente angular de %s?" % lei(a, b), fq(a), [fq(b) if b != a else fq(a + 1), fq(-a), "x"], "É o número que multiplica x: <b>%s</b>." % fq(a))
    if k == "b":
        if b == 0:
            return None
        return M("Em que ponto o gráfico de %s corta o eixo y?" % lei(a, b), "(0, %s)" % d(b), ["(%s, 0)" % d(b), "(0, %s)" % fq(a), "(%s, 0)" % fq(-F(b) / a)], "x = 0 dá f(0) = %s: <b>(0, %s)</b>." % (d(b), d(b)))
    if k == "zero":
        z = -F(b) / a
        return M("Qual é o zero (raiz) de %s?" % lei(a, b), "x = %s" % fq(z), ["x = %s" % fq(-z) if z else "x = 1", "x = %s" % fq(b), "x = %s" % fq(F(a) / b) if b else "x = %s" % fq(a)],
                 "%s = 0 ⇒ x = %s ÷ %s = <b>%s</b>." % (expr([(a, "x"), (b, "")]), d(-b), par(a), fq(z)))
    if k == "sinal":
        return M("A função %s é…" % lei(a, b), "crescente" if a > 0 else "decrescente", ["decrescente" if a > 0 else "crescente", "constante", "crescente só para x > 0"],
                 "a = %s é %s: <b>%s</b>." % (fq(a), "positivo" if a > 0 else "negativo", "crescente" if a > 0 else "decrescente"))
    x = R.randint(-4, 6)
    v = a * x + b
    return M("Para %s, quanto vale f(%s)?" % (lei(a, b), d(x)), fq(v), [fq(a * x - b) if b else fq(v + 1), fq(a + x + b), fq(x * b + a)], "%s · %s %s = <b>%s</b>." % (fq(a), par(x), ("+ %s" % d(b)) if b >= 0 else "− %s" % d(-b), fq(v)))


def s2_lei():
    k = R.choice(["pts", "tab", "graf", "graf"])
    if k in ("pts", "tab"):
        a = R.choice([x for x in range(-5, 6) if x])
        b = R.randint(-8, 8)
        xs = sorted(R.sample(range(-3, 7), 2 if k == "pts" else 4))
        ys = [a * x + b for x in xs]
        w = [lei(b, a) if b else lei(a, 1), lei(F(1, a), b) if abs(a) != 1 else lei(a, -b) if b else lei(2 * a, 0), lei(a, ys[0]) if ys[0] != b else lei(a, b + 1)]
        if k == "pts":
            q = "Qual é a lei da função afim cujo gráfico passa por (%s, %s) e (%s, %s)?" % (d(xs[0]), d(ys[0]), d(xs[1]), d(ys[1]))
        else:
            q = ntab([d(x) for x in xs], [d(y) for y in ys]) + "Qual é a lei da função afim da tabela?"
        return M(q, lei(a, b), w, "a = (%s − %s) ÷ (%s − %s) = %s; b = %s − %s · %s = %s. <b>%s</b>." % (d(ys[1]), par(ys[0]), d(xs[1]), par(xs[0]), d(a), d(ys[0]), d(a), par(xs[0]), d(b), lei(a, b)))
    a = R.choice([x for x in range(-3, 4) if x] + [F(1, 2), F(-1, 2)])
    b = R.randint(-3, 3)
    g = kosy(lines=[(a, b, "#1f5fbf", "f")], label="gráfico da função afim f")
    w = [lei(-a, b), lei(a, -b) if b else lei(a, 1), lei(F(1, a), b) if abs(a) != 1 else lei(2 * a, b), lei(b, a) if b else lei(a, 2)]
    return M(g + "Qual é a lei da função f do gráfico?", lei(a, b), w, "Corta o eixo y em %s (b = %s) e, para cada 1 em x, y muda %s (a = %s): <b>%s</b>." % (d(b), d(b), fq(a), fq(a), lei(a, b)))


def s3_modelo():
    k = R.choice(["taxi", "plano", "salario", "agua", "prop"])
    if k == "taxi":
        b = R.choice([F(5), F(550, 100), F(6), F(450, 100)])
        a = R.choice([F(3), F(250, 100), F(320, 100), F(280, 100)])
        km = R.randint(3, 25)
        v = a * km + b
        return M("Num táxi, a bandeirada é %s e cada km custa %s. Quanto custa uma corrida de %d km?" % (R2(b), R2(a), km), R2(v), [R2(a * km), R2((a + b) * km), R2(b * km + a)],
                 "f(x) = %s · x + %s; f(%d) = <b>%s</b>." % (d(a, 2, keep=True), d(b, 2, keep=True), km, R2(v)))
    if k == "plano":
        f1, c1 = R.choice([(40, 2), (50, 1), (30, 3), (60, 1)])
        f2, c2 = R.choice([(0, 4), (10, 3), (20, 2), (0, 5)])
        if c1 == c2 or (f1 - f2) % (c2 - c1) or (f1 - f2) // (c2 - c1) <= 0:
            return None
        x = (f1 - f2) // (c2 - c1)
        pb = ("%s fixos mais %s por hora" % (R2(f2), R2(c2))) if f2 else ("só %s por hora, sem valor fixo" % R2(c2))
        return M("Plano A: %s fixos mais %s por hora. Plano B: %s. Com quantas horas os dois planos custam o mesmo?" % (R2(f1), R2(c1), pb), "%d h" % x, ["%d h" % (f1 + f2), "%d h" % (x + c1), "%d h" % abs(f1 - f2)],
                 "%d + %dx = %d + %dx ⇒ %dx = %d ⇒ <b>x = %d</b>." % (f1, c1, f2, c2, c2 - c1, f1 - f2, x))
    if k == "salario":
        fx = R.choice([1500, 1800, 2000, 2200])
        p = R.choice([2, 3, 4, 5])
        v = R.choice([5000, 8000, 10000, 12000, 15000])
        s = fx + F(p, 100) * v
        return M("Um vendedor recebe R$ %s fixos mais %d%% sobre as vendas. Quanto recebe num mês em que vendeu R$ %s?" % (num(fx), p, num(v)), R2(s), [R2(F(p, 100) * v), R2(fx + p * v), R2(fx * F(100 + p, 100))],
                 "S(x) = %s + 0,0%d · x; S(%s) = %s + %s = <b>%s</b>." % (num(fx), p, num(v), num(fx), d(F(p, 100) * v), R2(s)))
    if k == "agua":
        h0 = R.choice([20, 30, 40, 50])
        r = R.choice([2, 3, 4, 5])
        t = R.randint(2, 8)
        return M("Um tanque tem %d cm de água e o nível sobe %d cm por minuto. Qual é o nível depois de %d minutos?" % (h0, r, t), "%d cm" % (h0 + r * t), ["%d cm" % (h0 * r * t), "%d cm" % (r * t), "%d cm" % (h0 + r + t)],
                 "h(t) = %d + %dt; h(%d) = <b>%d cm</b>." % (h0, r, t, h0 + r * t))
    c = R.choice(["lin", "afim"])
    a, b = R.randint(2, 9), R.randint(1, 9)
    xs = [1, 2, 3, 4]
    ys = [a * x + (0 if c == "lin" else b) for x in xs]
    return M(ntab(xs, ys) + "As grandezas x e y da tabela são diretamente proporcionais?", "sim, y = %dx" % a if c == "lin" else "não, y = %dx + %d (b ≠ 0)" % (a, b),
             ["não, y = %dx + %d (b ≠ 0)" % (a, b) if c == "lin" else "sim, y = %dx" % a, "sim, porque y aumenta", "não, porque y aumenta"],
             "Proporcional só quando y ÷ x é sempre o mesmo (b = 0). Aqui: <b>%s</b>." % ("sim" if c == "lin" else "não"))


s4_conceitos = bank(R, [
    ("O gráfico de uma função afim é…", "uma reta", ["uma parábola", "uma curva exponencial", "um círculo"]),
    ("Na função f(x) = ax + b, o coeficiente a indica…", "quanto y varia quando x aumenta 1", ["onde a reta corta o eixo y", "o zero da função", "o valor máximo"]),
    ("Uma função linear (f(x) = ax) representa grandezas…", "diretamente proporcionais", ["inversamente proporcionais", "sem relação", "que crescem como x²"]),
    ("Se a < 0, a função afim é…", "decrescente", ["crescente", "constante", "quadrática"]),
    ("O gráfico de f(x) = 3 é…", "uma reta horizontal", ["uma reta vertical", "uma reta que passa pela origem", "uma parábola"]),
    ("A reta de f(x) = 2x + 5 e a de g(x) = 2x − 1 são…", "paralelas", ["perpendiculares", "a mesma reta", "concorrentes na origem"]),
    ("Na função afim, a taxa de variação é…", "constante e igual a a", ["igual a b", "sempre 1", "diferente em cada ponto"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Coeficientes e valores", mix(R, seen, [(s1_coef, 20)])),
        ("Zero e crescimento", mix(R, seen, [(s1_coef, 14), (s4_conceitos, 6)])),
        ("Lei a partir de pontos e tabelas", mix(R, seen, [(s2_lei, 20)])),
        ("Gráficos", mix(R, seen, [(s2_lei, 20)])),
        ("Modelos com função afim", mix(R, seen, [(s3_modelo, 19), (s4_conceitos, 1)])),
    ]
    body = lesson(
        ["<b>Função afim</b>: f(x) = ax + b. O gráfico é uma reta.",
         "<b>a</b> (coeficiente angular): quanto y varia quando x aumenta 1. a > 0: crescente; a < 0: decrescente. a = (y₂ − y₁) ÷ (x₂ − x₁).",
         "<b>b</b> (coeficiente linear): onde a reta corta o eixo y, no ponto (0, b).",
         "<b>Zero</b>: o x em que f(x) = 0, ou seja, x = −b ÷ a. Se b = 0, a função é <b>linear</b> e x e y são proporcionais."],
        [("Reta por (1, 5) e (3, 11)", ["a = (11 − 5) ÷ (3 − 1) = 3", "5 = 3 · 1 + b ⇒ b = 2"], "f(x) = 3x + 2"),
         ("Zero de f(x) = 2x − 8", ["2x − 8 = 0"], "x = 4")],
        [["Trocar a e b", "a multiplica x; b é o termo sozinho."],
         ["Calcular a como Δx ÷ Δy", "a = Δy ÷ Δx."],
         ["Errar o sinal do zero", "x = −b ÷ a: em 2x − 8, x = 8 ÷ 2 = 4."]],
        kosy(lines=[(3, 2, "#1f5fbf", "f")], label="gráfico de f(x) = 3x + 2"))
    faq = [("Como achar a lei de uma função afim a partir de dois pontos?", "Calcule a = (y₂ − y₁) ÷ (x₂ − x₁). Depois substitua um dos pontos em y = ax + b para achar b."),
           ("O que a BNCC pede?", "Construir modelos empregando as funções polinomiais de 1º grau para resolver problemas (EM13MAT302), converter representações algébricas de funções polinomiais de 1º grau em representações geométricas no plano cartesiano (EM13MAT401) e investigar relações entre números em tabelas, reconhecendo funções de 1º grau (EM13MAT501).")]
    unit(R, "funcao-afim", "A", ["EM13MAT302", "EM13MAT401", "EM13MAT501"],
         "Construir modelos empregando as funções polinomiais de 1º grau para resolver problemas em contextos diversos; converter representações algébricas de funções polinomiais de 1º grau em representações geométricas no plano cartesiano, distinguindo os casos nos quais o comportamento é proporcional; investigar relações entre números expressos em tabelas para representá-los no plano cartesiano, identificando padrões e criando conjecturas para generalizar e expressar algebricamente essa generalização",
         "Função afim: coeficientes, gráfico e modelos", "Função afim",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre função afim: coeficiente angular e linear, zero, crescimento, lei por dois pontos, tabela e gráfico, e modelos como táxi e planos. 100 exercícios com gabarito.",
         "f(x) = ax + b: o gráfico é uma reta", "a = Δy ÷ Δx; b = onde corta o eixo y.",
         body, faq, sets, 4, grade="1-serie")


if __name__ == "__main__":
    main()
