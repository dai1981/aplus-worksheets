# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Porcentagens (Números, EF08MA04)
  python3 tools/gen_br_matematica_8_porcentagens.py
Problemas com porcentagens: fator multiplicativo, acréscimos e descontos, porcentagens sucessivas, valor original, juros simples
e compostos (introdução), porcentagem de porcentagem; educação financeira (à vista ou a prazo).
Usa geradores do 7º e do 9º ano (porcentagem) com outro sorteio.
Erros: somar porcentagens sucessivas, calcular sobre o valor final, achar que juros compostos crescem igual aos simples.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use, reais
from br_9 import M, d, bank, unit

R = random.Random(88004)
q_final, q_qual, q_suc, q_juros = use("gen_br_matematica_7_porcentagem", 88904, "s2_final", "s3_qual", "s4_sucessivos", "s5_juros")
c_fator, c_comp = use("gen_br_matematica_9_porcentagens_e_juros_compostos", 88905, "s1_fator", "s3_compostos")


def rv(x):
    return reais(int(x * 100 + F(1, 2)))


def s1_vista_prazo():
    v = R.choice([600, 800, 1000, 1200, 1500, 2000])
    dsc = R.choice([5, 8, 10, 12, 15])
    n = R.choice([3, 4, 5, 6, 10])
    parc = F(v, n) * F(R.choice([100, 105, 110]), 100)
    if (parc * 100).denominator != 1:
        return None
    vista = v * F(100 - dsc, 100)
    prazo = parc * n
    k = R.choice(["dif", "qual"])
    if k == "dif":
        return M("Uma geladeira custa %s. À vista há %d%% de desconto; a prazo são %d parcelas de %s. Quanto se economiza pagando à vista?" % (reais(v * 100), dsc, n, rv(parc)), rv(prazo - vista), [rv(v - vista), rv(prazo - v), rv(vista)],
                     "À vista: %s; a prazo: %d × %s = %s; diferença <b>%s</b>." % (rv(vista), n, rv(parc), rv(prazo), rv(prazo - vista)))
    return M("Uma TV custa %s. À vista há %d%% de desconto; a prazo são %d parcelas de %s. Qual é o preço à vista?" % (reais(v * 100), dsc, n, rv(parc)), rv(vista), [rv(prazo), rv(v - dsc), rv(F(v * dsc, 100))],
             "%d × %s = <b>%s</b>." % (v, d(F(100 - dsc, 100)), rv(vista)))


def s2_de_de():
    a, b = R.choice([(50, 20), (40, 25), (60, 50), (20, 50), (30, 10), (25, 40), (80, 25)])
    n = R.choice([200, 400, 500, 800, 1000, 1200])
    v = F(a * b * n, 10000)
    if v.denominator != 1:
        return None
    ctx = R.choice([("Numa escola de %s alunos, %d%% são meninas e, delas, %d%% jogam vôlei. Quantas meninas jogam vôlei?", "meninas"), ("Num bairro de %s moradores, %d%% usam ônibus e, desses, %d%% vão ao trabalho de ônibus todo dia. Quantas pessoas são?", "pessoas")])
    return M(ctx[0] % (d(n), a, b), "%s %s" % (d(v), ctx[1]), ["%s %s" % (d(F((a + b) * n, 100)), ctx[1]), "%s %s" % (d(F(a * n, 100)), ctx[1]), "%s %s" % (d(F(b * n, 100)), ctx[1])],
             "%d%% de %d%% = %s%% do total; %s%% de %s = <b>%s</b>." % (b, a, d(F(a * b, 100)), d(F(a * b, 100)), d(n), d(v)))


s3_conceitos = bank(R, [
    ("Um aumento de 50% seguido de um desconto de 50% leva o preço a…", "75% do inicial", ["100% do inicial", "50% do inicial", "125% do inicial"]),
    ("Nos juros compostos, os juros de cada mês são calculados sobre…", "o montante do mês anterior", ["o capital inicial sempre", "os juros do primeiro mês", "o valor final"]),
    ("Depois de 2 meses a 10% ao mês, um capital de R$ 100,00 em juros compostos vira…", "R$ 121,00", ["R$ 120,00", "R$ 110,00", "R$ 200,00"]),
    ("Multiplicar por 0,92 corresponde a…", "um desconto de 8%", ["um aumento de 92%", "um desconto de 92%", "um aumento de 8%"]),
    ("Multiplicar por 1,05 corresponde a…", "um aumento de 5%", ["um desconto de 5%", "um aumento de 105%", "um aumento de 0,5%"]),
    ("O preço subiu de R$ 50,00 para R$ 60,00. O aumento foi de…", "20%", ["10%", "16,7%", "60%"]),
    ("O preço caiu de R$ 60,00 para R$ 50,00. A queda foi de cerca de…", "16,7%", ["20%", "10%", "50%"]),
], "s3_conceitos")


def main():
    seen = set()
    sets = [
        ("Fator multiplicativo", mix(R, seen, [(c_fator, 10), (q_final, 10)])),
        ("Quantos por cento?", mix(R, seen, [(q_qual, 14), (s3_conceitos, 6)])),
        ("Porcentagens sucessivas", mix(R, seen, [(q_suc, 14), (s2_de_de, 6)])),
        ("Juros simples e compostos", mix(R, seen, [(q_juros, 10), (c_comp, 10)])),
        ("À vista ou a prazo?", mix(R, seen, [(s1_vista_prazo, 20)])),
    ]
    body = lesson(
        ["Acréscimo de p%: multiplique por (1 + p/100). Desconto de p%: multiplique por (1 − p/100).",
         "Porcentagens sucessivas se multiplicam: +10% e depois +10% = × 1,1 × 1,1 = × 1,21 (21%).",
         "Juros simples: os juros são sempre sobre o capital. <b>Juros compostos</b>: os juros de cada mês entram no cálculo do mês seguinte.",
         "Para comparar à vista e a prazo, calcule o total de cada forma de pagamento."],
        [("R$ 500,00 com 12% de desconto", ["× 0,88"], "R$ 440,00"),
         ("R$ 1.000,00 a 2% ao mês, 2 meses, juros compostos", ["× 1,02 × 1,02 = 1,0404"], "R$ 1.040,40")],
        [["Somar porcentagens sucessivas", "Multiplique os fatores."],
         ["Calcular sobre o valor final", "A base é o valor de antes."],
         ["Confundir juros simples e compostos", "Compostos: juros sobre juros."]])
    faq = [("Qual é a diferença entre juros simples e compostos?", "Nos juros simples, cada mês rende a mesma quantia, calculada sobre o capital inicial. Nos compostos, os juros são calculados sobre o montante acumulado, então crescem a cada mês."),
           ("O que a BNCC pede no 8º ano?", "Resolver e elaborar problemas, envolvendo cálculo de porcentagens, incluindo o uso de tecnologias digitais (EF08MA04).")]
    unit(R, "porcentagens", "N", ["EF08MA04"],
         "Resolver e elaborar problemas, envolvendo cálculo de porcentagens, incluindo o uso de tecnologias digitais",
         "Porcentagens: fator, sucessivas e juros", "Porcentagens",
         "Atividades de matemática para o 8º ano sobre porcentagens: fator multiplicativo, acréscimos e descontos, porcentagens sucessivas, porcentagem de porcentagem, juros simples e compostos e compras à vista ou a prazo. 100 exercícios com gabarito.",
         "Acréscimo: × (1 + p/100). Desconto: × (1 − p/100).", "Sucessivas: multiplique os fatores.",
         body, faq, sets, 4, grade="8-ano")


if __name__ == "__main__":
    main()
