# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Porcentagens sucessivas e juros compostos (Números, EF09MA05)
  python3 tools/gen_br_matematica_9_porcentagens_e_juros_compostos.py
Fator de aumento e de desconto (1,2 e 0,85); aumentos e descontos sucessivos (10% + 10% = 21%); juros simples e compostos;
montante M = C · (1 + i)ᵗ; comparar opções de compra e de investimento.
Erros: somar as porcentagens (10% + 10% = 20%), achar que aumento e desconto de 10% se anulam, calcular juros compostos como simples.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais, Kids
from br_9 import M, d, unit

R = random.Random(89004)
K = Kids(R)


def rs(x):
    """Fraction de reais → R$ com centavos"""
    return reais(int(F(x) * 100 + F(1, 2)))


def pct(x):
    return d(x) + "%"


def s1_fator():
    p = R.choice([5, 10, 12, 15, 20, 25, 30, 40, 50])
    if R.random() < 0.5:
        return M("Aumentar um valor em %d%% é o mesmo que multiplicar por…" % p, d(1 + F(p, 100)), [d(F(p, 100)), d(1 - F(p, 100)), d(p)],
                 "100%% + %d%% = %d%% = <b>%s</b>." % (p, 100 + p, d(1 + F(p, 100))))
    return M("Dar um desconto de %d%% é o mesmo que multiplicar por…" % p, d(1 - F(p, 100)), [d(F(p, 100)), d(1 + F(p, 100)), d(100 - p)],
             "100%% − %d%% = %d%% = <b>%s</b>." % (p, 100 - p, d(1 - F(p, 100))))


def s1_valor():
    v = R.randint(4, 60) * 50
    p = R.choice([10, 15, 20, 25, 30, 40])
    up = R.random() < 0.5
    f = 1 + F(p, 100) if up else 1 - F(p, 100)
    return M("Um produto de %s teve %s de %d%%. Qual é o novo preço?" % (rs(v), "aumento" if up else "desconto", p), rs(v * f),
             [rs(v * F(p, 100)), rs(v * (2 - f)), rs(v + p if up else v - p)], "%s · %s = <b>%s</b>." % (rs(v), d(f), rs(v * f)))


def s2_sucessivos():
    a, b = R.choice([(10, 10), (20, 10), (10, 20), (20, 20), (50, 10), (30, 10), (10, 5), (25, 20)])
    k = R.choice(["aa", "dd", "ad"])
    if k == "aa":
        f = (1 + F(a, 100)) * (1 + F(b, 100))
        tot = (f - 1) * 100
        return M("Um preço teve um aumento de %d%% e depois outro de %d%%. Qual foi o aumento total?" % (a, b), pct(tot), [pct(a + b), pct(a * b), pct(tot + 1)],
                 "%s · %s = %s, ou seja, aumento de <b>%s</b> (não %d%%)." % (d(1 + F(a, 100)), d(1 + F(b, 100)), d(f), pct(tot), a + b))
    if k == "dd":
        f = (1 - F(a, 100)) * (1 - F(b, 100))
        tot = (1 - f) * 100
        return M("Uma loja deu um desconto de %d%% e depois mais %d%% sobre o novo preço. Qual foi o desconto total?" % (a, b), pct(tot), [pct(a + b), pct(tot - 1), pct(abs(a - b)) if a != b else pct(tot + 2)],
                 "%s · %s = %s, ou seja, desconto de <b>%s</b>." % (d(1 - F(a, 100)), d(1 - F(b, 100)), d(f), pct(tot)))
    f = (1 + F(a, 100)) * (1 - F(a, 100))
    return M("Um preço aumentou %d%% e depois diminuiu %d%%. Em relação ao preço inicial, o preço final…" % (a, a), "ficou %s menor" % pct((1 - f) * 100),
             ["voltou ao mesmo valor", "ficou %s maior" % pct((1 - f) * 100), "ficou %d%% menor" % a], "%s · %s = %s: <b>ficou %s menor</b>." % (d(1 + F(a, 100)), d(1 - F(a, 100)), d(f), pct((1 - f) * 100)))


def s3_compostos():
    C = R.randint(2, 20) * 500
    i = R.choice([5, 10, 20])
    t = R.choice([2, 3])
    Mt = C * (1 + F(i, 100)) ** t
    simples = C * (1 + F(i * t, 100))
    k = R.choice(["m", "j"])
    if k == "m":
        return M("Aplicando %s a juros compostos de %d%% ao mês, qual é o montante após %d meses?" % (rs(C), i, t), rs(Mt), [rs(simples), rs(C * F(i, 100) * t), rs(Mt - C)],
                 "M = %s · %s%s = <b>%s</b>." % (rs(C), d(1 + F(i, 100)), "²" if t == 2 else "³", rs(Mt)))
    return M("Aplicando %s a juros compostos de %d%% ao ano, quanto se ganha de juros em %d anos?" % (rs(C), i, t), rs(Mt - C), [rs(simples - C), rs(Mt), rs(C * F(i, 100))],
             "Montante: %s · %s%s = %s. Juros: %s − %s = <b>%s</b>." % (rs(C), d(1 + F(i, 100)), "²" if t == 2 else "³", rs(Mt), rs(Mt), rs(C), rs(Mt - C)))


def s3_simples_ou():
    C = R.randint(2, 10) * 1000
    i = R.choice([5, 10])
    t = R.choice([2, 3])
    s = C * F(i * t, 100)
    c = C * ((1 + F(i, 100)) ** t - 1)
    return M("%s aplicados por %d anos a %d%% ao ano: quanto rende a mais nos juros compostos do que nos juros simples?" % (rs(C), t, i), rs(c - s), [rs(c), rs(s), rs(0)],
             "Simples: %s. Compostos: %s. Diferença: <b>%s</b>." % (rs(s), rs(c), rs(c - s)))


def s4_compra():
    p, g = K.next()
    v = R.randint(6, 40) * 50
    n = R.choice([2, 3, 4, 5, 10])
    dv = R.choice([5, 10, 15])
    acr = R.choice([0, 5, 10])
    vista = v * (1 - F(dv, 100))
    prazo = v * (1 + F(acr, 100))
    ok = "à vista, %s mais barato" % rs(prazo - vista)
    return M("Uma TV custa %s. À vista há %d%% de desconto; a prazo, em %d parcelas, há %d%% de acréscimo. Qual é a melhor opção para %s?" % (rs(v), dv, n, acr, p) if acr else
             "Uma TV custa %s. À vista há %d%% de desconto; a prazo são %d parcelas sem acréscimo. Qual é a melhor opção para %s?" % (rs(v), dv, n, p),
             ok, ["a prazo, %s mais barato" % rs(prazo - vista), "as duas custam o mesmo", "à vista, %s mais barato" % rs(v * F(dv, 100) + 10)],
             "À vista: %s. A prazo: %s. <b>%s</b>." % (rs(vista), rs(prazo), ok))


def main():
    seen = set()
    sets = [
        ("Fator de aumento e de desconto", mix(R, seen, [(s1_fator, 10), (s1_valor, 10)])),
        ("Aumentos e descontos sucessivos", mix(R, seen, [(s2_sucessivos, 16), (s1_valor, 4)])),
        ("Juros compostos", mix(R, seen, [(s3_compostos, 20)])),
        ("Juros simples e compostos", mix(R, seen, [(s3_simples_ou, 12), (s1_valor, 8)])),
        ("Comprar e investir", mix(R, seen, [(s4_compra, 14), (s1_fator, 6)])),
    ]
    body = lesson(
        ["Aumentar <b>p%</b> é multiplicar por (1 + p/100); descontar p% é multiplicar por (1 − p/100). Ex.: +15% → · 1,15; −20% → · 0,8.",
         "Em porcentagens <b>sucessivas</b>, multiplique os fatores: +10% e +10% = 1,1 · 1,1 = 1,21, ou seja, +21%.",
         "Nos <b>juros compostos</b>, os juros de cada período entram no cálculo do próximo: M = C · (1 + i)ᵗ.",
         "Nos juros simples, os juros são sempre sobre o valor inicial; por isso os compostos rendem mais."],
        [("R$ 1.000,00 a 10% ao mês por 2 meses (compostos)", ["1.000 · 1,1 = 1.100", "1.100 · 1,1 = 1.210"], "R$ 1.210,00"),
         ("+20% e depois −20%", ["1,2 · 0,8 = 0,96"], "4% a menos")],
        [["Somar as porcentagens: 10% + 10% = 20%", "Multiplique os fatores: 1,1 · 1,1 = 1,21."],
         ["Achar que +10% e −10% se anulam", "1,1 · 0,9 = 0,99: fica 1% menor."],
         ["Calcular juros compostos como simples", "Juros compostos: os juros também rendem juros."]],
        "<p>Juros compostos: M = C · (1 + i)ᵗ (C = capital, i = taxa, t = tempo)</p>")
    faq = [("O que são juros compostos?", "São juros calculados sobre o montante do período anterior (juros sobre juros). A BNCC pede resolver problemas com porcentagens sucessivas e cálculo de juros compostos, ligados à educação financeira."),
           ("Por que 10% + 10% não é 20%?", "Porque o segundo aumento é calculado sobre o valor já aumentado: 100 → 110 → 121. O aumento total é 21%.")]
    unit(R, "porcentagens-e-juros-compostos", "N", ["EF09MA05"],
         "Resolver e elaborar problemas que envolvam porcentagens, com a ideia de aplicação de percentuais sucessivos e a determinação das taxas percentuais, preferencialmente com o uso de tecnologias digitais, no contexto da educação financeira",
         "Porcentagens sucessivas e juros compostos", "Juros compostos",
         "Atividades de matemática para o 9º ano sobre porcentagens sucessivas e juros compostos: fator de aumento e desconto, aumentos sucessivos, juros simples e compostos. 100 exercícios com gabarito.",
         "Multiplique os fatores: +10% e +10% = +21%.", "M = C · (1 + i)ᵗ.",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
