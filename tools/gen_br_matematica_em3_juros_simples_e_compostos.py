# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Juros simples e compostos (EM13MAT303)
  python3 tools/gen_br_matematica_em3_juros_simples_e_compostos.py
Juros simples J = C · i · t (crescimento linear) e juros compostos M = C · (1 + i)ᵗ (crescimento exponencial);
taxa, tempo e capital desconhecidos; comparar os dois regimes em tabelas e gráficos; taxas equivalentes simples.
Usa geradores do 9º ano (juros compostos, simples ou compostos) com outro sorteio.
Erros: usar a taxa em % sem dividir por 100, somar os juros compostos como se fossem simples, misturar taxa mensal com tempo em anos.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, R2, num, curva, tab

R = random.Random(93001)
j_comp, j_ou = use("gen_br_matematica_9_porcentagens_e_juros_compostos", 93901, "s3_compostos", "s3_simples_ou")


def s1_simples():
    k = R.choice(["J", "M", "i", "t", "C"])
    C = R.choice([500, 800, 1000, 1200, 1500, 2000, 2500, 3000, 5000])
    i = R.choice([1, 2, 3, 4, 5, 6, 8, 10])
    t = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
    J = F(C * i * t, 100)
    per = R.choice(["mês", "ano"])
    un = "meses" if per == "mês" else "anos"
    if k == "J":
        return M("Quanto rende de juros simples um capital de %s a %d%% ao %s durante %d %s?" % (R2(C), i, per, t, un), R2(J), [R2(C * i * t), R2(F(C * i, 100)), R2(C * (F(100 + i, 100) ** t - 1))],
                 "J = C · i · t = %s · 0,%s · %d = <b>%s</b>." % (num(C), str(i).rjust(2, "0"), t, R2(J)))
    if k == "M":
        return M("Qual é o montante de %s aplicado a juros simples de %d%% ao %s por %d %s?" % (R2(C), i, per, t, un), R2(C + J), [R2(J), R2(C * F(100 + i, 100) ** t), R2(C + F(C * i, 100))],
                 "J = %s; M = C + J = <b>%s</b>." % (R2(J), R2(C + J)))
    if k == "i":
        return M("Um capital de %s rendeu %s de juros simples em %d %s. Qual foi a taxa ao %s?" % (R2(C), R2(J), t, un, per), "%d%% ao %s" % (i, per), ["%d%% ao %s" % (i * t, per), "%s%% ao %s" % (d(F(i, t), 2), per) if t > 1 else "%d%% ao %s" % (i + 1, per), "%d%% ao %s" % (i + 1, per)],
                 "i = J ÷ (C · t) = %s ÷ (%s · %d) = %s = <b>%d%%</b>." % (num(J) if J.denominator == 1 else d(J), num(C), t, d(F(i, 100)), i))
    if k == "t":
        return M("Em quanto tempo %s, a juros simples de %d%% ao %s, rendem %s de juros?" % (R2(C), i, per, R2(J)), "%d %s" % (t, un), ["%d %s" % (t * 2, un), "%d %s" % (i, un) if i != t else "%d %s" % (t + 1, un), "%d %s" % (t - 1, un)],
                 "t = J ÷ (C · i) = %s ÷ %s = <b>%d %s</b>." % (d(J), d(F(C * i, 100)), t, un))
    return M("Que capital, a juros simples de %d%% ao %s, rende %s em %d %s?" % (i, per, R2(J), t, un), R2(C), [R2(J * t), R2(J / t), R2(C * 2)], "C = J ÷ (i · t) = %s ÷ (%s · %d) = <b>%s</b>." % (d(J), d(F(i, 100)), t, R2(C)))


def s2_compostos():
    k = R.choice(["M", "J", "M", "fator", "tabela"])
    C = R.choice([1000, 2000, 5000, 10000, 4000, 8000])
    i = R.choice([2, 5, 10, 20])
    t = R.choice([2, 3])
    Mo = C * F(100 + i, 100) ** t
    if k == "M":
        return M("Qual é o montante de %s aplicado a juros compostos de %d%% ao mês durante %d meses?" % (R2(C), i, t), R2(Mo), [R2(C * F(100 + i * t, 100)), R2(C * F(100 + i, 100) ** (t - 1)), R2(C * F(i, 100) ** t + C)],
                 "M = %s · %s%s = <b>%s</b>." % (num(C), d(F(100 + i, 100)), "²³"[t - 2], R2(Mo)))
    if k == "J":
        return M("Quanto rendem de juros compostos %s a %d%% ao mês durante %d meses?" % (R2(C), i, t), R2(Mo - C), [R2(C * F(i * t, 100)), R2(Mo), R2(C * F(i, 100) ** t)],
                 "M = %s; J = M − C = <b>%s</b>." % (R2(Mo), R2(Mo - C)))
    if k == "fator":
        i2 = R.choice([3, 4, 6, 8, 12, 15])
        return M("Uma aplicação rende %d%% ao mês a juros compostos. Por quanto o capital fica multiplicado a cada mês?" % i2, d(F(100 + i2, 100)), [d(F(i2, 100)), d(F(i2, 10)) if i2 < 10 else "%d" % i2, d(F(100 - i2, 100))], "1 + %s = <b>%s</b>." % (d(F(i2, 100)), d(F(100 + i2, 100))))
    rows = [["Mês", "Juros simples", "Juros compostos"]]
    for m in range(0, 4):
        rows.append([str(m), R2(C + C * F(i * m, 100)), R2(C * F(100 + i, 100) ** m)])
    dif = C * F(100 + i, 100) ** 3 - (C + C * F(i * 3, 100))
    return M(tab(rows) + "A tabela compara %s aplicados a %d%% ao mês. No 3º mês, quanto os juros compostos renderam a mais que os simples?" % (R2(C), i), R2(dif), [R2(0), R2(C * F(i, 100)), R2(dif * 2)],
             "%s − %s = <b>%s</b>." % (R2(C * F(100 + i, 100) ** 3), R2(C + C * F(i * 3, 100)), R2(dif)))


def s3_grafico():
    C = 1000
    i = R.choice([10, 20])
    g = curva([(lambda t: (C + C * i / 100 * t) / 1000, "simples"), (lambda t: C * (1 + i / 100) ** t / 1000, "compostos")], (0, 6, 1), (0, 3, 0.5), label="montante, em milhares de reais, a juros simples e compostos ao longo dos anos")
    k = R.choice(["qual", "forma", "antes"])
    if k == "qual":
        return M(g + "O gráfico mostra o montante (em milhares de reais) de R$ 1.000 a %d%% ao ano. Qual curva representa os juros compostos?" % i, "a curva que cresce cada vez mais rápido (exponencial)", ["a reta (linear)", "as duas são retas", "nenhuma das duas"], "Juros compostos crescem de forma <b>exponencial</b>; os simples, em linha reta.")
    if k == "forma":
        return M(g + "O montante a juros simples, em função do tempo, é uma função…", "afim (o gráfico é uma reta)", ["exponencial", "quadrática", "constante"], "M(t) = C + C · i · t: <b>função afim</b>.")
    return M(g + "No período de 0 a 1 ano, como se comparam os montantes a %d%% ao ano?" % i, "são iguais no fim do 1º período", ["o composto é muito maior", "o simples é muito maior", "o composto é menor"], "No 1º período, C · (1 + i) = C + C · i: <b>são iguais</b>; depois, o composto passa à frente.")


s4_conceitos = bank(R, [
    ("Nos juros simples, os juros de cada período são calculados sobre…", "o capital inicial", ["o montante do período anterior", "os juros anteriores", "a taxa"]),
    ("Nos juros compostos, os juros de cada período são calculados sobre…", "o montante do período anterior (juros sobre juros)", ["o capital inicial sempre", "metade do capital", "a taxa acumulada"]),
    ("Uma taxa de 2% ao mês, em juros simples, equivale a quantos % ao ano?", "24%", ["2%", "26,8%", "12%"]),
    ("Para usar a fórmula, a taxa de 5% deve ser escrita como…", "0,05", ["5", "0,5", "500"]),
    ("Se a taxa é ao mês, o tempo deve estar em…", "meses", ["anos", "dias", "qualquer unidade"]),
    ("Com a mesma taxa e mais de um período, o montante a juros compostos é ___ que a juros simples.", "maior", ["menor", "igual", "sempre o dobro"]),
    ("O cartão de crédito costuma cobrar juros…", "compostos", ["simples", "nenhum", "só uma vez"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Juros simples", mix(R, seen, [(s1_simples, 20)])),
        ("Taxa, tempo e capital", mix(R, seen, [(s1_simples, 16), (s4_conceitos, 4)])),
        ("Juros compostos", mix(R, seen, [(s2_compostos, 14), (j_comp, 6)])),
        ("Simples ou compostos?", mix(R, seen, [(s3_grafico, 3), (j_ou, 10), (s2_compostos, 4), (s4_conceitos, 3)])),
        ("Revisão", mix(R, seen, [(s1_simples, 10), (s2_compostos, 10)])),
    ]
    body = lesson(
        ["<b>Juros simples</b>: J = C · i · t e M = C + J. Os juros são sempre sobre o capital inicial: o montante cresce em linha reta (função afim).",
         "<b>Juros compostos</b>: M = C · (1 + i)ᵗ. Os juros entram no capital a cada período (juros sobre juros): crescimento exponencial.",
         "A taxa i vai na forma decimal (5% = 0,05) e o tempo t na mesma unidade da taxa (mês com mês, ano com ano).",
         "No 1º período os dois regimes dão o mesmo montante; depois, o composto fica cada vez maior."],
        [("R$ 2.000 a 10% ao mês por 3 meses", ["simples: 2.000 + 2.000 · 0,1 · 3 = 2.600", "compostos: 2.000 · 1,1³ = 2.662"], "R$ 2.600,00 e R$ 2.662,00")],
        [["Usar 5 em vez de 0,05", "Divida a taxa por 100."],
         ["Calcular compostos como simples", "Multiplique por (1 + i) a cada período."],
         ["Misturar meses e anos", "Converta antes."]],
        curva([(lambda t: 1 + 0.2 * t, "simples"), (lambda t: 1.2 ** t, "compostos")], (0, 6, 1), (0, 3, 0.5), label="R$ 1.000 a 20% ao ano: montante em milhares de reais"))
    faq = [("Qual é a diferença entre juros simples e compostos?", "Nos simples, os juros de cada período são sempre sobre o capital inicial. Nos compostos, são sobre o montante acumulado, ou seja, há juros sobre juros, e o crescimento é exponencial."),
           ("O que a BNCC pede?", "Interpretar e comparar situações que envolvam juros simples com as que envolvem juros compostos, por meio de representações gráficas ou análise de planilhas, destacando o crescimento linear ou exponencial de cada caso (EM13MAT303).")]
    unit(R, "juros-simples-e-compostos", "N", ["EM13MAT303"],
         "Interpretar e comparar situações que envolvam juros simples com as que envolvem juros compostos, por meio de representações gráficas ou análise de planilhas, destacando o crescimento linear ou exponencial de cada caso",
         "Juros simples e juros compostos", "Juros simples e compostos",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre matemática financeira: juros simples, juros compostos, montante, taxa, tempo e capital, comparação em tabelas e gráficos. 100 exercícios com gabarito.",
         "Simples: J = C · i · t", "Compostos: M = C · (1 + i)ᵗ.",
         body, faq, sets, 1, grade="3-serie")


if __name__ == "__main__":
    main()
