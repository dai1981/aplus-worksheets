# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Funções e taxa de variação (EM13MAT101)
  python3 tools/gen_br_matematica_em1_funcoes_e_taxa_de_variacao.py
Função, domínio e imagem; ler gráficos (intervalos de crescimento e decrescimento, máximo, zeros);
taxa média de variação entre dois pontos (tabelas e gráficos); interpretar situações (população, temperatura, preços).
Usa geradores do 9º ano (valor de f(x), é função?) com outro sorteio.
Erros: trocar x e y na taxa (Δx/Δy), confundir domínio e imagem, dizer que a função cresce quando o gráfico está acima do eixo.
"""
import random
from fractions import Fraction as F
from br_em import M, d, par, bank, mix, lesson, use, num, unit, curva, tab, ntab

R = random.Random(91003)
f_valor, f_eh = use("gen_br_matematica_9_funcoes", 91904, "s1_valor", "s2_eh_funcao")


def poly(pts):
    def f(x):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if x1 <= x <= x2:
                return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
        return None
    return f


def iv(a, b):
    return "[%s, %s]" % (d(a), d(b))


def rand_pts():
    xs = [0, 2, 4, 6, 8]
    while True:
        ys = [R.randint(-3, 5) for _ in xs]
        ok = all(ys[i] != ys[i + 1] for i in range(4))
        if ok and len(set(ys)) >= 4:
            return list(zip(xs, ys))


def s1_grafico():
    pts = rand_pts()
    g = curva([(poly(pts), "f")], (0, 8, 1), (-4, 6, 1), label="gráfico da função f")
    ys = [y for _, y in pts]
    k = R.choice(["max", "min", "img", "cresce", "decresce", "valor"])
    if k == "max":
        y = max(ys)
        if ys.count(y) > 1:
            return None
        x = pts[ys.index(y)][0]
        return M(g + "Qual é o valor máximo da função f, no intervalo mostrado?", d(y), [d(x), d(min(ys)), d(ys[-1]) if ys[-1] != y else d(y + 1)], "O ponto mais alto é (%d, %s): o máximo é <b>%s</b>." % (x, d(y), d(y)))
    if k == "min":
        y = min(ys)
        if ys.count(y) > 1:
            return None
        x = pts[ys.index(y)][0]
        return M(g + "Para qual valor de x a função f atinge o valor mínimo?", "x = %d" % x, ["x = %s" % d(y), "x = %d" % pts[ys.index(max(ys))][0], "x = 0" if x else "x = 8"], "O ponto mais baixo é (%d, %s): <b>x = %d</b>." % (x, d(y), x))
    if k == "img":
        return M(g + "Qual é o conjunto imagem de f?", iv(min(ys), max(ys)), [iv(0, 8), iv(ys[0], ys[-1]) if (ys[0], ys[-1]) != (min(ys), max(ys)) else iv(0, max(ys)), iv(min(ys), 8) if max(ys) != 8 else iv(-4, 6)],
                 "Os valores de y vão de %s até %s: Im = <b>%s</b>." % (d(min(ys)), d(max(ys)), iv(min(ys), max(ys))))
    segs = [(pts[i][0], pts[i + 1][0], pts[i + 1][1] - pts[i][1]) for i in range(4)]
    if k in ("cresce", "decresce"):
        want = [(a, b) for a, b, dy in segs if (dy > 0) == (k == "cresce")]
        if len(want) != 1:
            return None
        a, b = want[0]
        others = [(x, y) for x, y, dy in segs if (x, y) != (a, b)]
        return M(g + "Em qual intervalo a função f é %s?" % ("crescente" if k == "cresce" else "decrescente"), iv(a, b), [iv(x, y) for x, y in others],
                 "Nesse trecho o gráfico %s: <b>%s</b>." % ("sobe" if k == "cresce" else "desce", iv(a, b)))
    x, y = R.choice(pts)
    return M(g + "Qual é o valor de f(%d)?" % x, d(y), [d(x) if x != y else d(y + 1), d(y + 1), d(y - 1)], "No gráfico, x = %d corresponde a y = %s: f(%d) = <b>%s</b>." % (x, d(y), x, d(y)))


def s2_taxa():
    k = R.choice(["tab", "lei", "ctx", "ctx"])
    if k == "tab":
        xs = sorted(R.sample(range(0, 11), 4))
        ys = [R.randint(-5, 30) for _ in xs]
        i, j = sorted(R.sample(range(4), 2))
        t = F(ys[j] - ys[i], xs[j] - xs[i])
        return M(ntab([d(x) for x in xs], [d(y) for y in ys]) + "Qual é a taxa média de variação de y entre x = %d e x = %d?" % (xs[i], xs[j]), d(t, 2) if (t * 100).denominator == 1 else "%s (aprox.)" % d(t, 2),
                 [d(F(xs[j] - xs[i], ys[j] - ys[i]), 2) if ys[j] != ys[i] else "1", d(ys[j] - ys[i]), d(-t, 2) if t else "1"],
                 "(%s − %s) ÷ (%d − %d) = %s ÷ %d = <b>%s</b>." % (d(ys[j]), par(ys[i]), xs[j], xs[i], d(ys[j] - ys[i]), xs[j] - xs[i], d(t, 2)))
    if k == "lei":
        a = R.choice([1, 2, -1, 3])
        b = R.randint(-5, 5)
        x1, x2 = sorted(R.sample(range(-3, 6), 2))
        f = lambda x: a * x * x + b
        t = F(f(x2) - f(x1), x2 - x1)
        return M("Para f(x) = %s, qual é a taxa média de variação entre x = %d e x = %d?" % (("x²" if a == 1 else ("−x²" if a == -1 else "%dx²" % a)) + (" + %d" % b if b > 0 else (" − %d" % -b if b < 0 else "")), x1, x2), d(t),
                 [d(f(x2) - f(x1)), d(F(x2 - x1, f(x2) - f(x1))) if f(x2) != f(x1) else "1", d(f(x2))],
                 "f(%d) = %s e f(%d) = %s; (%s − %s) ÷ (%s − %s) = <b>%s</b>." % (x2, d(f(x2)), x1, d(f(x1)), d(f(x2)), par(f(x1)), d(x2), par(x1), d(t)))
    ctx = R.choice(["pop", "temp", "preco", "dist"])
    if ctx == "pop":
        a1, a2 = R.choice([(2000, 2010), (2010, 2020), (2005, 2020), (2000, 2020)])
        p1 = R.randint(50, 200) * 1000
        t = R.choice([-500, 1000, 1500, 2000, 2500, 3000, 4000])
        p2 = p1 + t * (a2 - a1)
        return M("A população de uma cidade passou de %s habitantes em %d para %s em %d. Qual foi a taxa média de variação?" % (num(p1), a1, num(p2), a2), "%s habitantes por ano" % num(t) if t > 0 else "−%s habitantes por ano" % num(-t),
                 ["%s habitantes por ano" % num(abs(p2 - p1)), "%s habitantes por ano" % num(abs(t) * 10), "%s habitantes por ano" % num(p2 // (a2 - a1))],
                 "(%s − %s) ÷ (%d − %d) = <b>%s por ano</b>." % (num(p2), num(p1), a2, a1, num(t) if t > 0 else "−" + num(-t)))
    if ctx == "temp":
        h1, h2 = R.choice([(6, 14), (8, 12), (10, 16), (14, 20), (12, 18)])
        t1 = R.randint(12, 25)
        t2 = t1 + R.choice([-6, -4, 4, 6, 8, 10, 12])
        t = F(t2 - t1, h2 - h1)
        return M("A temperatura passou de %d °C às %dh para %d °C às %dh. Qual foi a taxa média de variação?" % (t1, h1, t2, h2), "%s °C por hora" % d(t), ["%s °C por hora" % d(t2 - t1), "%s °C por hora" % d(F(h2 - h1, t2 - t1)), "%s °C por hora" % d(-t)],
                 "(%d − %d) ÷ (%d − %d) = <b>%s °C por hora</b>." % (t2, t1, h2, h1, d(t)))
    if ctx == "preco":
        m1, m2 = 1, R.choice([4, 5, 6, 7])
        p1 = F(R.randint(400, 800), 100)
        t = F(R.choice([5, 10, 15, 20, 25]), 100)
        p2 = p1 + t * (m2 - m1)
        return M("O preço do litro de leite foi de R$ %s no mês 1 para R$ %s no mês %d. Qual foi a taxa média de variação por mês?" % (d(p1, 2, keep=True), d(p2, 2, keep=True), m2), "R$ %s por mês" % d(t, 2, keep=True),
                 ["R$ %s por mês" % d(p2 - p1, 2, keep=True), "R$ %s por mês" % d(F(p2 - p1, m2), 2, keep=True), "R$ %s por mês" % d(F(p2, m2), 2, keep=True)],
                 "(%s − %s) ÷ (%d − 1) = <b>R$ %s por mês</b>." % (d(p2, 2, keep=True), d(p1, 2, keep=True), m2, d(t, 2, keep=True)))
    v = R.choice([40, 50, 60, 80, 90])
    t1, t2 = sorted(R.sample(range(1, 7), 2))
    return M("Um carro estava no km %d às %dh e no km %d às %dh. Qual foi a taxa média de variação da posição?" % (v * t1, t1 + 6, v * t2, t2 + 6), "%d km/h" % v, ["%d km/h" % (v * t2), "%d km/h" % (v * (t2 - t1)), "%d km/h" % (v * t2 // (t2 + 6))],
             "(%d − %d) ÷ %d = <b>%d km/h</b>." % (v * t2, v * t1, t2 - t1, v))


s3_conceitos = bank(R, [
    ("O domínio de uma função é…", "o conjunto dos valores de x", ["o conjunto dos valores de y", "o maior valor de y", "o ponto onde o gráfico corta o eixo y"]),
    ("A imagem de uma função é…", "o conjunto dos valores de y que a função assume", ["o conjunto dos valores de x", "o gráfico inteiro", "o ponto mais alto"]),
    ("Se a taxa média de variação entre dois pontos é negativa, a função nesse intervalo…", "diminui, em média", ["aumenta", "é constante", "não existe"]),
    ("Uma função é crescente num intervalo quando…", "x aumenta e y também aumenta", ["y é positivo", "x é positivo", "o gráfico corta o eixo x"]),
    ("A taxa média de variação entre (1, 3) e (5, 11) é…", "2", ["8", "4", "0,5"]),
    ("Taxa média de variação = …", "Δy ÷ Δx", ["Δx ÷ Δy", "Δy × Δx", "y ÷ x"]),
    ("Num gráfico de distância × tempo, a taxa média de variação é…", "a velocidade média", ["a distância total", "o tempo total", "a aceleração"]),
    ("Os zeros de uma função são…", "os valores de x em que f(x) = 0", ["os valores de y quando x = 0", "o mínimo da função", "o domínio"]),
], "s3_conceitos")


def main():
    seen = set()
    sets = [
        ("Funções e valores", mix(R, seen, [(f_valor, 12), (f_eh, 8)])),
        ("Ler gráficos de funções", mix(R, seen, [(s1_grafico, 20)])),
        ("Domínio, imagem e crescimento", mix(R, seen, [(s1_grafico, 14), (s3_conceitos, 6)])),
        ("Taxa média de variação", mix(R, seen, [(s2_taxa, 20)])),
        ("Situações do dia a dia", mix(R, seen, [(s2_taxa, 18), (s3_conceitos, 2)])),
    ]
    body = lesson(
        ["Uma <b>função</b> associa a cada x do <b>domínio</b> um único y. O conjunto dos y obtidos é a <b>imagem</b>.",
         "No gráfico: a função é <b>crescente</b> onde sobe da esquerda para a direita e <b>decrescente</b> onde desce.",
         "<b>Taxa média de variação</b> entre dois pontos: (y₂ − y₁) ÷ (x₂ − x₁). Mostra quanto y muda, em média, para cada unidade de x.",
         "Em situações reais, a taxa tem unidade: habitantes por ano, °C por hora, km/h."],
        [("Pontos (2, 5) e (6, 17)", ["(17 − 5) ÷ (6 − 2) = 12 ÷ 4"], "3"),
         ("População: 80.000 em 2010, 95.000 em 2020", ["15.000 ÷ 10"], "1.500 habitantes por ano")],
        [["Fazer Δx ÷ Δy", "A variação de y vai em cima."],
         ["Confundir domínio e imagem", "Domínio: valores de x. Imagem: valores de y."],
         ["Dizer que cresce porque está acima do eixo", "Crescer é subir, não estar em cima."]])
    faq = [("Como calcular a taxa média de variação?", "Divida a variação de y pela variação de x entre dois pontos: (y₂ − y₁) ÷ (x₂ − x₁). Se der positivo, a função aumentou em média; se der negativo, diminuiu."),
           ("O que a BNCC pede?", "Interpretar criticamente situações econômicas, sociais e fatos relativos às Ciências da Natureza que envolvam a variação de grandezas, pela análise dos gráficos das funções representadas e das taxas de variação, com ou sem apoio de tecnologias digitais (EM13MAT101).")]
    unit(R, "funcoes-e-taxa-de-variacao", "A", ["EM13MAT101"],
         "Interpretar criticamente situações econômicas, sociais e fatos relativos às Ciências da Natureza que envolvam a variação de grandezas, pela análise dos gráficos das funções representadas e das taxas de variação, com ou sem apoio de tecnologias digitais",
         "Funções, gráficos e taxa média de variação", "Funções e taxa de variação",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre funções: domínio e imagem, leitura de gráficos, crescimento e decrescimento, máximo e mínimo e taxa média de variação. 100 exercícios com gabarito.",
         "Taxa média de variação = Δy ÷ Δx", "Crescente: o gráfico sobe.",
         body, faq, sets, 3, grade="1-serie")


if __name__ == "__main__":
    main()
