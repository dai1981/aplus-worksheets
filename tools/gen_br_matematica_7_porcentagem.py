# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Porcentagem: acréscimos e decréscimos (Números, EF07MA02)
  python3 tools/gen_br_matematica_7_porcentagem.py
Porcentagem de uma quantidade; acréscimos e descontos (valor final em uma etapa: × 1,10, × 0,85); que porcentagem foi o aumento
ou o desconto; descontos sucessivos; juros simples; achar o valor original.
Erros: somar porcentagens sucessivas, calcular a porcentagem sobre o valor final, achar que 20% de aumento e 20% de desconto se anulam.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, bank, unit

R = random.Random(87006)


def rv(x):
    return reais(int(x * 100 + F(1, 2)))


def s1_de():
    p = R.choice([3, 4, 6, 8, 12, 15, 18, 35, 45, 65, 120, 150])
    v = R.choice([50, 80, 120, 150, 200, 240, 300, 450, 500, 800, 1200])
    r = F(p * v, 100)
    if (r * 100).denominator != 1:
        return None
    return M("Quanto é %d%% de %s?" % (p, d(v)), d(r), [d(r * 10), d(F(v, p), 2) if (F(v, p) * 100).denominator == 1 else d(r + 5), d(v - r) if p < 100 else d(v + r)],
             "%d%% = %s; %s × %s = <b>%s</b>." % (p, d(F(p, 100)), d(F(p, 100)), d(v), d(r)))


def s2_final():
    p = R.choice([5, 8, 10, 12, 15, 20, 25, 30, 40])
    v = R.choice([60, 80, 120, 150, 200, 250, 360, 400, 600, 1500])
    up = R.random() < 0.5
    f = F(100 + p, 100) if up else F(100 - p, 100)
    r = v * f
    txt = "Um produto de %s %s %d%%. Qual é o novo preço?" % (reais(v * 100), "teve aumento de" if up else "teve desconto de", p)
    return M(txt, rv(r), [rv(v * F(100 - p, 100) if up else v * F(100 + p, 100)), rv(F(p * v, 100)), rv(v + p if up else v - p)],
             "Multiplique por %s: %d × %s = <b>%s</b>." % (d(f), v, d(f), rv(r)))


def s3_qual():
    v = R.choice([40, 50, 80, 120, 200, 250, 400, 500])
    p = R.choice([5, 10, 15, 20, 25, 30, 40])
    up = R.random() < 0.5
    n = v * F(100 + p, 100) if up else v * F(100 - p, 100)
    if (n * 100).denominator != 1:
        return None
    return M("Um preço passou de %s para %s. De quantos por cento foi o %s?" % (rv(v), rv(n), "aumento" if up else "desconto"), "%d%%" % p, ["%s%%" % d(abs(n - v)) if abs(n - v) != p else "%d%%" % (p + 10), "%s%%" % d(abs(n - v) * 100 / n, 1), "%d%%" % (100 - p)],
             "Variação: %s; %s ÷ %s = %s = <b>%d%%</b>." % (rv(abs(n - v)), d(abs(n - v)), d(v), d(F(p, 100)), p))


def s4_sucessivos():
    k = R.choice(["dd", "ad", "orig"])
    if k == "dd":
        a, b = R.choice([(10, 10), (20, 10), (10, 20), (20, 20), (30, 10), (50, 20)])
        f = F(100 - a, 100) * F(100 - b, 100)
        return M("Um preço teve desconto de %d%% e, depois, mais %d%% sobre o novo preço. Qual foi o desconto total?" % (a, b), "%s%%" % d((1 - f) * 100), ["%d%%" % (a + b), "%s%%" % d((1 - f) * 100 + 2), "%d%%" % max(a, b)],
                     "Multiplique: %s × %s = %s; o preço caiu <b>%s%%</b> (não %d%%)." % (d(F(100 - a, 100)), d(F(100 - b, 100)), d(f), d((1 - f) * 100), a + b))
    if k == "ad":
        p = R.choice([10, 20, 25, 50])
        f = F(100 + p, 100) * F(100 - p, 100)
        v = R.choice([100, 200, 400, 1000])
        return M("Um produto de %s teve aumento de %d%% e depois desconto de %d%%. Qual é o preço final?" % (reais(v * 100), p, p), rv(v * f), [reais(v * 100), rv(v * F(100 + p, 100)), rv(v * F(100 - p, 100))],
                 "%d × %s × %s = <b>%s</b> (aumento e desconto iguais não se anulam)." % (v, d(F(100 + p, 100)), d(F(100 - p, 100)), rv(v * f)))
    p = R.choice([10, 20, 25, 40, 50])
    o = R.choice([40, 80, 120, 200, 300, 500])
    n = o * F(100 - p, 100)
    return M("Com desconto de %d%%, uma blusa saiu por %s. Qual era o preço sem desconto?" % (p, rv(n)), rv(o), [rv(n * F(100 + p, 100)), rv(n + p), rv(n / F(100 + p, 100))],
             "%s é %d%% do preço: %s ÷ %s = <b>%s</b>." % (rv(n), 100 - p, d(n), d(F(100 - p, 100)), rv(o)))


def s5_juros():
    c, i, t = R.choice([500, 800, 1000, 1200, 2000, 5000]), R.choice([1, 2, 3, 5]), R.randint(2, 12)
    j = F(c * i * t, 100)
    k = R.choice(["j", "m"])
    if k == "j":
        return M("Quanto rendem %s aplicados a juros simples de %d%% ao mês durante %d meses?" % (reais(c * 100), i, t), rv(j), [rv(F(c * i, 100)), rv(c + j), rv(j * 10)], "Juros por mês: %s; × %d = <b>%s</b>." % (rv(F(c * i, 100)), t, rv(j)))
    return M("%s foram aplicados a juros simples de %d%% ao mês. Qual é o montante após %d meses?" % (reais(c * 100), i, t), rv(c + j), [rv(j), rv(c + F(c * i, 100)), rv(c * F(100 + i * t, 100) + F(c * i, 100))],
             "Juros: %s; montante = %s + %s = <b>%s</b>." % (rv(j), rv(c), rv(j), rv(c + j)))


s6_conceitos = bank(R, [
    ("Aumentar um valor em 15% é o mesmo que multiplicá-lo por…", "1,15", ["0,15", "15", "0,85"]),
    ("Dar 30% de desconto é o mesmo que multiplicar o preço por…", "0,7", ["0,3", "1,3", "30"]),
    ("Um aumento de 100% faz o preço…", "dobrar", ["ficar igual", "triplicar", "zerar"]),
    ("Um preço subiu 10% e depois caiu 10%. Em relação ao preço inicial, ele…", "ficou 1% menor", ["ficou igual", "ficou 1% maior", "ficou 20% menor"]),
    ("Dois descontos seguidos de 10% equivalem a um desconto de…", "19%", ["20%", "10%", "21%"]),
    ("Se 40% de um valor é R$ 80,00, o valor é…", "R$ 200,00", ["R$ 32,00", "R$ 120,00", "R$ 320,00"]),
    ("Nos juros simples, os juros de cada mês são calculados sobre…", "o valor inicial (capital)", ["o montante do mês anterior", "os juros", "o valor final"]),
], "s6_conceitos")


def main():
    seen = set()
    sets = [
        ("Porcentagem de uma quantidade", mix(R, seen, [(s1_de, 14), (s6_conceitos, 6)])),
        ("Acréscimos e descontos", mix(R, seen, [(s2_final, 20)])),
        ("Quantos por cento?", mix(R, seen, [(s3_qual, 20)])),
        ("Sucessivos e valor original", mix(R, seen, [(s4_sucessivos, 20)])),
        ("Juros simples", mix(R, seen, [(s5_juros, 19), (s6_conceitos, 1)])),
    ]
    body = lesson(
        ["Para um <b>acréscimo</b> de p%, multiplique por (1 + p/100): aumento de 15% → × 1,15. Para um <b>desconto</b> de p%, multiplique por (1 − p/100): desconto de 15% → × 0,85.",
         "A porcentagem do aumento ou do desconto é sempre calculada sobre o valor <b>inicial</b>: variação ÷ valor inicial.",
         "Porcentagens sucessivas se multiplicam, não se somam: 10% e depois 10% de desconto = × 0,9 × 0,9 = × 0,81 (19%).",
         "<b>Juros simples</b>: os juros de cada mês são iguais, calculados sobre o capital."],
        [("R$ 250,00 com 20% de desconto", ["× 0,8"], "R$ 200,00"),
         ("R$ 80,00 → R$ 92,00", ["12 ÷ 80 = 0,15"], "aumento de 15%")],
        [["Somar porcentagens sucessivas", "Multiplique os fatores."],
         ["Calcular sobre o valor final", "A base é o valor inicial."],
         ["Achar que +20% e −20% se anulam", "1,2 × 0,8 = 0,96."]])
    faq = [("Como calcular um desconto de cabeça?", "Ache 10% (divida por 10), multiplique para chegar à porcentagem e subtraia do preço. Ou multiplique o preço direto por 0,9, 0,8, 0,75…"),
           ("O que a BNCC pede no 7º ano?", "Resolver e elaborar problemas que envolvam porcentagens, como os que lidam com acréscimos e decréscimos simples, utilizando estratégias pessoais, cálculo mental e calculadora, no contexto de educação financeira (EF07MA02).")]
    unit(R, "porcentagem-acrescimos-e-descontos", "N", ["EF07MA02"],
         "Resolver e elaborar problemas que envolvam porcentagens, como os que lidam com acréscimos e decréscimos simples, utilizando estratégias pessoais, cálculo mental e calculadora, no contexto de educação financeira, entre outros",
         "Porcentagem: acréscimos, descontos e juros simples", "Porcentagem",
         "Atividades de matemática para o 7º ano sobre porcentagem: porcentagem de uma quantidade, acréscimos e descontos, quantos por cento, porcentagens sucessivas, valor original e juros simples. 100 exercícios com gabarito.",
         "Acréscimo de p%: × (1 + p/100).", "Desconto de p%: × (1 − p/100).",
         body, faq, sets, 6, grade="7-ano")


if __name__ == "__main__":
    main()
