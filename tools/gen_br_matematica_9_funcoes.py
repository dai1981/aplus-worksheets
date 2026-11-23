# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Funções (Álgebra, EF09MA06)
  python3 tools/gen_br_matematica_9_funcoes.py
Função como relação em que cada x tem um único y; calcular f(x); descobrir a lei a partir de uma tabela; ler o gráfico
de uma função afim; zero da função; funções em situações (táxi, celular, combustível).
Erros: trocar x e y, achar que f(2) é f vezes 2, esquecer o termo fixo da lei (y = 3x em vez de y = 3x + 2).
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, expr, par, kosy, unit

R = random.Random(89005)


def lei(a, b):
    return "f(x) = %s" % expr([(a, "x"), (b, "")])


def s1_valor():
    a, b = R.choice([-3, -2, 2, 3, 4, 5]), R.randint(-9, 9)
    x = R.randint(-4, 6)
    if R.random() < 0.3:
        c = R.randint(-5, 5)
        y = x * x + c
        return M("Se f(x) = %s, quanto vale f(%s)?" % (expr([(1, "x²"), (c, "")]), d(x)), d(y), [d(2 * x + c), d(-x * x + c) if x else d(c + 1), d(y + 1)],
                 "f(%s) = %s² %s = %d %s = <b>%s</b>." % (d(x), par(x), ("+ %d" % c) if c >= 0 else "− %d" % -c, x * x, ("+ %d" % c) if c >= 0 else "− %d" % -c, d(y)))
    y = a * x + b
    return M("Se %s, quanto vale f(%s)?" % (lei(a, b), d(x)), d(y), [d(a + x + b), d(a * x - b), d(a * (x + b))],
             "Troque x por %s: %s · %s %s = <b>%s</b>." % (d(x), d(a), par(x), ("+ %d" % b) if b >= 0 else "− %d" % -b, d(y)))


def s1_inversa():
    a, b = R.choice([2, 3, 4, 5]), R.randint(-6, 9)
    x = R.randint(-3, 8)
    y = a * x + b
    return M("Se %s, para que valor de x temos f(x) = %s?" % (lei(a, b), d(y)), d(x), [d(a * y + b), d(x + 1), d(F(y, a)), d(y - b), d(x - 1)],
             "%s = %s → %dx = %s → x = <b>%s</b>." % (expr([(a, "x"), (b, "")]), d(y), a, d(y - b), d(x)))


def s2_tabela():
    a, b = R.choice([-2, 2, 3, 4, 5]), R.randint(-5, 6)
    xs = [0, 1, 2, 3]
    tb = "<table class='sn-table' style='width:auto'><tbody><tr><th>x</th>%s</tr><tr><th>y</th>%s</tr></tbody></table>" % ("".join("<td>%d</td>" % x for x in xs), "".join("<td>%s</td>" % d(a * x + b) for x in xs))
    ok = "y = %s" % expr([(a, "x"), (b, "")])
    return M(tb + "Qual é a lei da função?", ok, ["y = %s" % expr([(b, "x"), (a, "")]) if b else "y = %s" % expr([(a + 1, "x")]), "y = %s" % expr([(a, "x")]) if b else "y = %s" % expr([(a, "x"), (1, "")]), "y = %s" % expr([(a, "x"), (-b, "")]) if b else "y = %s" % expr([(-a, "x")]), "y = %s" % expr([(a + b, "x")]), "y = %s" % expr([(a, "x"), (b + a, "")])],
             "Quando x aumenta 1, y aumenta %s; quando x = 0, y = %s. Lei: <b>%s</b>." % (d(a), d(b), ok))


def s2_eh_funcao():
    ok_pairs = [(1, R.randint(1, 9)), (2, R.randint(1, 9)), (3, R.randint(1, 9)), (4, R.randint(1, 9))]
    bad = [(1, 2), (1, 5), (2, 3), (3, 4)]
    k = R.choice(["sim", "nao"])
    f = lambda L: "{" + "; ".join("(%d, %d)" % p for p in L) + "}"
    if k == "sim":
        return M("A relação %s (pares (x, y)) é uma função de x?" % f(ok_pairs), "sim, cada x tem um único y", ["não, porque há y repetidos", "não, porque x começa em 1", "só se y for maior que x"],
                 "Cada x aparece uma vez só: <b>sim, cada x tem um único y</b> (y repetido não atrapalha).")
    return M("A relação %s (pares (x, y)) é uma função de x?" % f(bad), "não, x = 1 tem dois valores de y", ["sim, cada x tem um único y", "sim, porque os números são inteiros", "não, porque y não está em ordem"],
             "x = 1 leva a 2 e a 5: <b>não, x = 1 tem dois valores de y</b>.")


def s3_grafico():
    a, b = R.choice([(1, 1), (2, -1), (-1, 3), (1, -2), (2, 1), (-2, 4), (1, 2), (-1, -1)])
    x = R.choice([x for x in range(-3, 4) if -5 <= a * x + b <= 5])
    pic = kosy(lines=[(a, b, "#1f77b4", "f")], label="gráfico da função f")
    k = R.choice(["valor", "zero"])
    if k == "valor":
        return M(pic + "Pelo gráfico, quanto vale f(%s)?" % d(x), d(a * x + b), [d(x), d(a * x + b + 1), d(a * x + b - 1), d(-(a * x + b)) if a * x + b else "2", d(a * (x + 1) + b)],
                 "Ache x = %s no eixo horizontal, suba até a reta e leia y: <b>%s</b>." % (d(x), d(a * x + b)))
    z = F(-b, a)
    if z.denominator != 1:
        return None
    return M(pic + "Em que valor de x o gráfico corta o eixo x (o zero da função)?", d(z), [d(b), d(-z) if z else "1", d(z + 1), d(z - 1), d(-b)],
             "O zero é onde y = 0: <b>x = %s</b>." % d(z))


def s4_situacao():
    k = R.choice(["taxi", "celular", "gas", "salario"])
    if k == "taxi":
        a, b, x = R.choice([3, 4, 5]), R.choice([5, 6, 8]), R.randint(4, 15)
        return M("Um táxi cobra %s fixos mais %s por km. Quanto custa uma corrida de %d km?" % (reais(b * 100), reais(a * 100), x), reais((a * x + b) * 100),
                 [reais(a * x * 100), reais((a + b) * x * 100), reais((a * x + b + a) * 100)], "f(x) = %dx + %d; f(%d) = %d + %d = <b>%s</b>." % (a, b, x, a * x, b, reais((a * x + b) * 100)))
    if k == "celular":
        a, b = R.choice([2, 3]), R.choice([20, 30, 40])
        x = R.randint(5, 20)
        return M("Um plano de celular custa %s por mês mais %s por GB extra. Qual é a lei do valor y para x GB extras?" % (reais(b * 100), reais(a * 100)), "y = %dx + %d" % (a, b),
                 ["y = %dx + %d" % (b, a), "y = %dx" % (a + b), "y = %dx − %d" % (a, b)], "Valor fixo %d mais %d por GB: <b>y = %dx + %d</b>." % (b, a, a, b))
    if k == "gas":
        p = F(R.randint(500, 640), 100)
        x = R.randint(10, 40)
        return M("O litro da gasolina custa %s. Quanto se paga por %d litros?" % (reais(int(p * 100)), x), reais(int(p * x * 100 + F(1, 2))), [reais(int(p * 100) + x * 100), reais(int(p * (x - 1) * 100 + F(1, 2))), reais(int(p * x * 10))],
                 "y = %s · x; y = %s · %d = <b>%s</b>." % (d(p), d(p), x, reais(int(p * x * 100 + F(1, 2)))))
    b, a = R.choice([1200, 1500, 1800]), R.choice([50, 80, 100])
    x = R.randint(3, 12)
    return M("Um vendedor ganha %s fixos mais %s por venda. Quanto ganha com %d vendas?" % (reais(b * 100), reais(a * 100), x), reais((b + a * x) * 100),
             [reais(a * x * 100), reais((b + a) * 100), reais((b * x) * 100)], "%d + %d · %d = <b>%s</b>." % (b, a, x, reais((b + a * x) * 100)))


def main():
    seen = set()
    sets = [
        ("Calcular f(x)", mix(R, seen, [(s1_valor, 14), (s2_eh_funcao, 6)])),
        ("Descobrir x", mix(R, seen, [(s1_inversa, 20)])),
        ("Lei de formação pela tabela", mix(R, seen, [(s2_tabela, 20)])),
        ("Gráficos de funções", mix(R, seen, [(s3_grafico, 20)])),
        ("Funções no dia a dia", mix(R, seen, [(s4_situacao, 20)])),
    ]
    body = lesson(
        ["Uma <b>função</b> liga cada valor de x a <b>um único</b> valor de y. Escrevemos y = f(x).",
         "Para calcular f(3), troque x por 3 na lei: se f(x) = 2x + 1, então f(3) = 2 · 3 + 1 = 7.",
         "Na função afim f(x) = ax + b, quando x aumenta 1, y aumenta a; e b é o valor de y quando x = 0.",
         "No gráfico, o <b>zero da função</b> é onde a reta corta o eixo x (y = 0)."],
        [("f(x) = 3x − 4; f(5)", ["3 · 5 − 4"], "11"),
         ("Tabela: x = 0, 1, 2 → y = 1, 4, 7", ["y sobe 3", "começa em 1"], "y = 3x + 1")],
        [["Trocar x e y", "f(2) pede o y quando x = 2."],
         ["Achar que f(2) é f vezes 2", "f(2) é a função calculada em x = 2."],
         ["Esquecer o termo fixo", "Veja o valor de y em x = 0."]],
        kosy(lines=[(2, 1, "#1f77b4", "f")], label="gráfico de f(x) = 2x + 1"))
    faq = [("O que é uma função no 9º ano?", "É uma relação em que cada valor de x corresponde a um único valor de y. A BNCC pede compreender funções e usar suas representações: lei, tabela e gráfico."),
           ("Como descobrir a lei pela tabela?", "Veja quanto y muda quando x aumenta 1 (é o a) e qual é o y quando x = 0 (é o b). A lei é y = ax + b.")]
    unit(R, "funcoes", "A", ["EF09MA06"],
         "Compreender as funções como relações de dependência unívoca entre duas variáveis e suas representações numérica, algébrica e gráfica e utilizar esse conceito para analisar situações que envolvam relações funcionais entre duas variáveis",
         "Funções: lei, tabela e gráfico", "Funções",
         "Atividades de matemática para o 9º ano sobre funções: calcular f(x), descobrir x, lei de formação pela tabela, gráficos, zero da função e situações do dia a dia. 100 exercícios com gabarito.",
         "Cada x tem um único y.", "f(x) = ax + b: a é a taxa, b é o valor inicial.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
