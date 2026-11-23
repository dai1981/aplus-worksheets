# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Funções definidas por mais de uma sentença (EM13MAT404)
  python3 tools/gen_br_matematica_em1_funcoes_definidas_por_partes.py
Calcular valores de uma função definida por partes; ler o gráfico; conta de água por faixas de consumo,
estacionamento (primeira hora + horas adicionais), frete, imposto progressivo com tabela simplificada (valores fictícios).
Erros: aplicar a taxa da última faixa a todo o valor, usar a sentença errada para o x dado, esquecer a parte fixa.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, expr, bank, mix, lesson, unit, curva, tab, R2, num

R = random.Random(91007)


def chave(rows):
    return "<span class='sys'>%s</span>" % "<br>".join(rows)


def s1_valor():
    a1, b1 = R.choice([1, 2, 3, -1, -2]), R.randint(-5, 5)
    a2, b2 = R.choice([1, 2, -1, 3, 0]), R.randint(-5, 8)
    c = R.randint(-1, 3)
    rows = ["%s, se x &lt; %s" % (expr([(a1, "x"), (b1, "")]), d(c)), "%s, se x ≥ %s" % (expr([(a2, "x"), (b2, "")]), d(c))]
    x = R.choice([c - 2, c - 1, c, c + 1, c + 3])
    v = a1 * x + b1 if x < c else a2 * x + b2
    o = a2 * x + b2 if x < c else a1 * x + b1
    return M("f(x) = " + chave(rows) + "<br>Quanto vale f(%s)?" % d(x), d(v), [d(o) if o != v else d(v + 1), d(v + 1), d(-v) if v else d(2)],
             "%s %s %s, usamos a %s sentença: f(%s) = <b>%s</b>." % (d(x), "&lt;" if x < c else "≥", d(c), "1ª" if x < c else "2ª", d(x), d(v)))


def s2_grafico():
    c = R.randint(1, 4)
    a1, b1 = R.choice([1, 2, -1]), R.randint(0, 3)
    y0 = a1 * c + b1
    k2 = R.choice([0, -1, 1])
    f = lambda x: a1 * x + b1 if x < c else y0 + k2 * (x - c)
    g = curva([(f, "f")], (0, 7, 1), (-4, 8, 2), label="gráfico de uma função definida por partes")
    x = R.choice([0, 1, 5, 6, 7])
    v = f(x)
    if not (-4 <= v <= 8):
        return None
    k = R.choice(["val", "const"]) if k2 == 0 else "val"
    if k == "const":
        return M(g + "Em qual intervalo a função f é constante?", "x ≥ %d" % c, ["x ≤ %d" % c, "0 ≤ x ≤ %d" % c, "x ≥ 0"], "A partir de x = %d o gráfico fica horizontal: <b>x ≥ %d</b>." % (c, c))
    return M(g + "Qual é o valor de f(%d)?" % x, d(v), [d(v + 1), d(v - 1), d(x)], "No gráfico, x = %d corresponde a y = <b>%s</b>." % (x, d(v)))


def agua(m3, fx, faixas):
    """fx: valor fixo até 10 m³; faixas [(limite, preço por m³)]"""
    tot = F(fx)
    lo = 10
    for lim, p in faixas:
        if m3 > lo:
            q = min(m3, lim) - lo
            tot += q * p
        lo = lim
    return tot


def s3_contas():
    k = R.choice(["agua", "estac", "frete", "ir", "ir"])
    if k == "agua":
        fx = R.choice([40, 45, 50, 60])
        p1, p2 = R.choice([(F(5), F(8)), (F(6), F(9)), (F(4), F(7)), (F(5), F(10))])
        m3 = R.randint(12, 30)
        v = agua(m3, fx, [(20, p1), (999, p2)])
        q = tab([["Consumo", "Valor"], ["até 10 m³", "%s (fixo)" % R2(fx)], ["de 10 a 20 m³", "%s por m³" % R2(p1)], ["acima de 20 m³", "%s por m³" % R2(p2)]])
        return M(q + "Quanto paga uma casa que consumiu %d m³ de água?" % m3, R2(v), [R2(fx + (m3 - 10) * p1), R2(m3 * p2), R2(fx + m3 * p1)],
                 "%s + %s %s= <b>%s</b>." % (R2(fx), "%d × %s" % (min(m3, 20) - 10, R2(p1)), ("+ %d × %s " % (m3 - 20, R2(p2))) if m3 > 20 else "", R2(v)))
    if k == "estac":
        p1, p2 = R.choice([(10, 5), (12, 4), (8, 3), (15, 6)])
        h = R.randint(2, 7)
        v = p1 + (h - 1) * p2
        return M("Um estacionamento cobra R$ %d pela primeira hora e R$ %d por hora adicional. Quanto paga quem fica %d horas?" % (p1, p2, h), R2(v), [R2(p1 * h), R2(p1 + h * p2), R2(p2 * h)],
                 "%d + (%d − 1) × %d = <b>%s</b>." % (p1, h, p2, R2(v)))
    if k == "frete":
        lim = R.choice([100, 150, 200])
        fr = R.choice([15, 20, 25])
        c = R.choice([lim - R.randint(10, 60), lim + R.randint(0, 80)])
        v = c + (fr if c < lim else 0)
        return M("Uma loja cobra frete de R$ %d para compras abaixo de R$ %d; a partir de R$ %d o frete é grátis. Quanto paga, no total, quem compra R$ %d?" % (fr, lim, lim, c), R2(v), [R2(c + fr) if c >= lim else R2(c), R2(c - fr), R2(lim + fr)],
                 "%d %s %d: %s." % (c, "&lt;" if c < lim else "≥", lim, "paga frete, <b>%s</b>" % R2(v) if c < lim else "frete grátis, <b>%s</b>" % R2(v)))
    # imposto progressivo (tabela simplificada, valores fictícios)
    l1, l2 = 2000, 4000
    t1, t2 = F(10, 100), F(20, 100)
    s = R.choice([2500, 3000, 3500, 4500, 5000, 6000])
    v = (min(s, l2) - l1) * t1 + (max(s - l2, 0)) * t2
    q = tab([["Parte da renda", "Alíquota"], ["até R$ 2.000", "isento"], ["de R$ 2.000 a R$ 4.000", "10%"], ["acima de R$ 4.000", "20%"]])
    wrong = [R2(s * (t2 if s > l2 else t1)), R2((s - l1) * t1), R2(s * t1)]
    return M(q + "Numa tabela de imposto simplificada (valores fictícios), cada parte da renda paga sua alíquota. Quanto paga quem ganha R$ %s?" % num(s), R2(v), wrong,
             "%s%s= <b>%s</b>." % ("(%s − 2.000) × 10%% " % num(min(s, l2)), "+ (%s − 4.000) × 20%% " % num(s) if s > l2 else "", R2(v)))


s4_conceitos = bank(R, [
    ("Numa função definida por partes, para calcular f(x) devemos…", "escolher a sentença que vale para aquele x", ["somar todas as sentenças", "usar sempre a primeira sentença", "usar a última sentença"]),
    ("Num imposto progressivo, a alíquota maior incide…", "só sobre a parte da renda acima do limite", ["sobre toda a renda", "só sobre a primeira faixa", "sobre nenhuma parte"]),
    ("Uma conta de luz com tarifa diferente por faixa de consumo é um exemplo de…", "função definida por mais de uma sentença", ["função constante", "função quadrática", "função exponencial"]),
    ("O gráfico de uma função definida por partes pode ter…", "trechos de retas diferentes", ["só uma reta", "só parábolas", "nenhum ponto"]),
    ("Um estacionamento cobra preço fixo até 1 hora e depois por hora. O gráfico do preço é…", "formado por trechos", ["uma parábola", "uma única reta pela origem", "um círculo"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Calcular valores", mix(R, seen, [(s1_valor, 20)])),
        ("Gráficos por partes", mix(R, seen, [(s2_grafico, 16), (s4_conceitos, 4)])),
        ("Contas por faixas", mix(R, seen, [(s3_contas, 20)])),
        ("Imposto e tarifas", mix(R, seen, [(s3_contas, 20)])),
        ("Revisão", mix(R, seen, [(s1_valor, 10), (s3_contas, 9), (s4_conceitos, 1)])),
    ]
    body = lesson(
        ["Uma função pode ter <b>uma regra para cada intervalo</b> de x. Primeiro veja em qual intervalo está o x, depois use a regra dele.",
         "Contas de água e de luz, estacionamentos e impostos costumam ser cobrados <b>por faixas</b>.",
         "No imposto progressivo, cada parte da renda paga a alíquota da sua faixa: a alíquota maior vale só para o que passa do limite."],
        [("Água: R$ 50 fixos até 10 m³; R$ 5/m³ de 10 a 20; R$ 8/m³ acima de 20. Consumo: 25 m³", ["50 + 10 × 5 + 5 × 8"], "R$ 140,00")],
        [["Aplicar a maior taxa a tudo", "Cada faixa tem a sua taxa."],
         ["Usar a sentença errada", "Confira se x &lt; c ou x ≥ c."],
         ["Esquecer a parte fixa", "Some o valor mínimo da conta."]])
    faq = [("O que é uma função definida por partes?", "É uma função com regras diferentes para intervalos diferentes de x, como uma conta de água que cobra preços diferentes por faixa de consumo."),
           ("O que a BNCC pede?", "Analisar funções definidas por uma ou mais sentenças (tabela do Imposto de Renda, contas de luz, água, gás etc.), em suas representações algébrica e gráfica, identificando domínios de validade, imagem, crescimento e decrescimento, e convertendo essas representações de uma para outra (EM13MAT404).")]
    unit(R, "funcoes-definidas-por-partes", "A", ["EM13MAT404"],
         "Analisar funções definidas por uma ou mais sentenças (tabela do Imposto de Renda, contas de luz, água, gás etc.), em suas representações algébrica e gráfica, identificando domínios de validade, imagem, crescimento e decrescimento, e convertendo essas representações de uma para outra, com ou sem apoio de tecnologias digitais",
         "Funções definidas por mais de uma sentença", "Funções definidas por partes",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre funções definidas por partes: valores, gráficos, conta de água por faixas, estacionamento, frete e imposto progressivo. 100 exercícios com gabarito.",
         "Uma regra para cada intervalo", "Veja primeiro em qual faixa está o x.",
         body, faq, sets, 7, grade="1-serie")


if __name__ == "__main__":
    main()
