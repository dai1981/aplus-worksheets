# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Modelos com funções (EM13MAT302, EM13MAT101, EM13MAT403)
  python3 tools/gen_br_matematica_em3_modelos_com_funcoes.py
Escolher o modelo pela tabela: diferenças constantes (afim), segundas diferenças constantes (quadrático),
razão constante (exponencial); escolher o modelo pelo gráfico ou pela situação; usar o modelo para prever; interpretar parâmetros.
Erros: escolher afim só porque os valores crescem, confundir crescimento por soma (afim) e por multiplicação (exponencial).
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, expr, bank, mix, lesson, unit, ntab, curva, num

R = random.Random(93004)
TIPOS = ["afim", "quadrático", "exponencial", "nenhum desses três"]


def s1_tabela():
    k = R.choice(["afim", "quad", "exp"])
    xs = [0, 1, 2, 3, 4]
    if k == "afim":
        a, b = R.choice([x for x in range(-5, 8) if x]), R.randint(-5, 20)
        ys = [a * x + b for x in xs]
        ans, why = "afim", "as diferenças são sempre %s" % d(a)
    elif k == "quad":
        a, b, c = R.choice([1, 2, -1, 3]), R.randint(-3, 3), R.randint(0, 9)
        ys = [a * x * x + b * x + c for x in xs]
        ans, why = "quadrático", "as segundas diferenças são sempre %s" % d(2 * a)
    else:
        a, q = R.choice([1, 2, 3, 5, 80, 162]), R.choice([2, 3, F(1, 2), F(1, 3)])
        ys = [a * F(q) ** x for x in xs]
        if any(y.denominator != 1 for y in ys):
            return None
        ans, why = "exponencial", "cada valor é o anterior × %s" % fq(q)
    return M(ntab(xs, [d(y) for y in ys]) + "Que tipo de modelo descreve a tabela?", ans, [t for t in TIPOS if t != ans], "Resposta: <b>%s</b>, porque %s." % (ans, why))


def s2_prever():
    k = R.choice(["afim", "exp", "quad"])
    if k == "afim":
        a, b = R.randint(2, 9), R.randint(10, 60)
        xs = [1, 2, 3, 4]
        t = R.choice([8, 10, 12, 15, 20])
        return M(ntab(xs, [a * x + b for x in xs], "mês", "assinantes (mil)") + "Mantendo o mesmo padrão, quantos mil assinantes haverá no mês %d?" % t, d(a * t + b), [d(b * t), d(a * t), d((a * 4 + b) * t // 4)],
                 "Sobe %d por mês: y = %dx + %d; y(%d) = <b>%s</b>." % (a, a, b, t, d(a * t + b)))
    if k == "exp":
        a, q = R.choice([(100, 2), (50, 2), (10, 3), (1000, 2), (20, 3)])
        xs = [0, 1, 2, 3]
        t = R.choice([5, 6, 7]) if q == 2 else R.choice([4, 5])
        return M(ntab(xs, [num(a * q ** x) for x in xs], "hora", "bactérias") + "Mantendo o mesmo padrão, quantas bactérias haverá na hora %d?" % t, num(a * q ** t), [num(a * q ** 3 + (t - 3) * (a * q ** 3 - a * q ** 2)), num(a * q * t), num(a * q ** (t - 1))],
                 "Multiplica por %d a cada hora: %s · %d%s = <b>%s</b>." % (q, num(a), q, "⁴⁵⁶⁷"[t - 4], num(a * q ** t)))
    v = R.choice([20, 30, 40])
    T = R.choice([3, 4, 5])
    h = v * T - 5 * T * T
    if h < 0:
        return None
    xs = [0, 1, 2]
    return M(ntab(xs, [v * x - 5 * x * x for x in xs], "t (s)", "altura (m)") + "A altura segue h(t) = %dt − 5t². Qual é a altura em t = %d s?" % (v, T), "%s m" % d(h),
             ["%s m" % d(v * T), "%s m" % d(v * T - 5 * T), "%s m" % d(5 * T * T), "%s m" % d(h + 5)],
             "h(%d) = %d · %d − 5 · %d = <b>%s m</b>." % (T, v, T, T * T, d(h)))


def s3_situacao():
    q, a = R.choice([
        ("O valor de uma corrida de táxi: bandeirada fixa mais um valor por km.", "afim"),
        ("Uma aplicação que rende 1% ao mês, com juros sobre juros.", "exponencial"),
        ("A altura de uma bola chutada para cima, ao longo do tempo.", "quadrático"),
        ("A área de um quadrado em função do lado.", "quadrático"),
        ("O número de pessoas que viram um vídeo que dobra a cada dia.", "exponencial"),
        ("A conta de água com tarifa única por m³ mais uma taxa fixa.", "afim"),
        ("A massa de um material radioativo que cai pela metade a cada 10 anos.", "exponencial"),
        ("O lucro de uma loja que, ao subir o preço, vende menos unidades (lucro com máximo).", "quadrático"),
        ("O salário de um vendedor: fixo mais 5% das vendas.", "afim"),
        ("O valor de um carro que perde 15% ao ano.", "exponencial"),
        ("A distância percorrida por um carro a 80 km/h constantes.", "afim"),
        ("A população de uma cidade que cresce 2% ao ano.", "exponencial"),
    ])
    return M("Que tipo de modelo descreve melhor esta situação? " + q, a, [t for t in TIPOS if t != a], "Resposta: <b>%s</b>." % a)


def s4_grafico():
    k = R.choice(["afim", "quadrático", "exponencial"])
    f = {"afim": lambda x: 1 + 1.5 * x, "quadrático": lambda x: 8 - (x - 3) ** 2, "exponencial": lambda x: 0.5 * 2 ** x}[k]
    g = curva([(f, "f")], (0, 6, 1), (0, 10, 2), label="gráfico de um modelo")
    return M(g + "Que tipo de modelo o gráfico mostra?", k, [t for t in TIPOS if t != k], {"afim": "Uma reta: <b>afim</b>.", "quadrático": "Uma parábola, com máximo: <b>quadrático</b>.", "exponencial": "Cresce cada vez mais rápido, multiplicando: <b>exponencial</b>."}[k])


s5_param = bank(R, [
    ("No modelo C(x) = 50 + 2x (custo em reais de x cópias), o número 50 representa…", "um custo fixo", ["o preço de cada cópia", "o total de cópias", "o lucro"]),
    ("No modelo C(x) = 50 + 2x, o número 2 representa…", "o custo de cada cópia", ["o custo fixo", "o número de cópias", "o desconto"]),
    ("No modelo P(t) = 5.000 · 1,03ᵗ, a população cresce…", "3% por período", ["3 pessoas por período", "1,03 pessoas por período", "300% por período"]),
    ("No modelo V(t) = 40.000 · 0,9ᵗ, o valor…", "cai 10% por ano", ["cai 0,9 por ano", "sobe 90% por ano", "cai 90% por ano"]),
    ("No modelo h(t) = −5t² + 30t, a altura máxima ocorre em…", "t = 3", ["t = 6", "t = 30", "t = 5"]),
    ("Um modelo afim com coeficiente angular negativo descreve uma grandeza que…", "diminui a uma taxa constante", ["cresce cada vez mais", "diminui pela metade", "fica constante"]),
    ("Uma tabela com x = 1, 2, 3, 4 e y = 3, 6, 12, 24 sugere um modelo…", "exponencial", ["afim", "quadrático", "constante"]),
], "s5_param")


def main():
    seen = set()
    sets = [
        ("Qual modelo? Pela tabela", mix(R, seen, [(s1_tabela, 20)])),
        ("Qual modelo? Pela situação", mix(R, seen, [(s3_situacao, 12), (s4_grafico, 3), (s5_param, 5)])),
        ("Prever com o modelo", mix(R, seen, [(s2_prever, 20)])),
        ("Interpretar parâmetros", mix(R, seen, [(s1_tabela, 18), (s5_param, 2)])),
        ("Revisão", mix(R, seen, [(s2_prever, 20)])),
    ]
    body = lesson(
        ["Olhe as <b>diferenças</b> entre valores seguidos de y (com x de 1 em 1): se forem constantes, o modelo é <b>afim</b>.",
         "Se as diferenças mudam, mas as <b>diferenças das diferenças</b> são constantes, o modelo é <b>quadrático</b>.",
         "Se cada valor é o anterior <b>multiplicado</b> pelo mesmo número, o modelo é <b>exponencial</b>.",
         "Situações: valor fixo + valor por unidade → afim; porcentagem por período → exponencial; áreas e lançamentos → quadrático."],
        [("y: 2, 5, 10, 17, 26", ["diferenças: 3, 5, 7, 9", "segundas diferenças: 2, 2, 2"], "quadrático"),
         ("y: 3, 6, 12, 24", ["razão 2"], "exponencial")],
        [["Chamar de afim tudo que cresce", "Confira se as diferenças são iguais."],
         ["Confundir soma e multiplicação", "Somar o mesmo valor: afim. Multiplicar: exponencial."],
         ["Prever sem checar o padrão", "Confirme o modelo com todos os pontos."]])
    faq = [("Como saber se uma tabela é de uma função afim, quadrática ou exponencial?", "Com x variando de 1 em 1: diferenças constantes indicam afim; segundas diferenças constantes, quadrática; razão constante, exponencial."),
           ("O que a BNCC pede?", "Construir modelos empregando as funções polinomiais de 1º ou 2º graus para resolver problemas em contextos diversos (EM13MAT302), interpretar situações que envolvam a variação de grandezas (EM13MAT101) e relacionar as representações das funções exponencial e logarítmica (EM13MAT403).")]
    unit(R, "modelos-com-funcoes", "A", ["EM13MAT302", "EM13MAT101", "EM13MAT403"],
         "Construir modelos empregando as funções polinomiais de 1º ou 2º graus, para resolver problemas em contextos diversos; interpretar criticamente situações que envolvam a variação de grandezas, pela análise dos gráficos das funções representadas e das taxas de variação; analisar e estabelecer relações entre as representações de funções exponencial e logarítmica expressas em tabelas e em plano cartesiano",
         "Modelos com funções: afim, quadrático ou exponencial", "Modelos com funções",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre modelos com funções: reconhecer modelos afim, quadrático e exponencial por tabelas, gráficos e situações, fazer previsões e interpretar parâmetros. 100 exercícios com gabarito.",
         "Diferenças constantes: afim", "Razão constante: exponencial; 2ªs diferenças constantes: quadrático.",
         body, faq, sets, 4, grade="3-serie")


if __name__ == "__main__":
    main()
