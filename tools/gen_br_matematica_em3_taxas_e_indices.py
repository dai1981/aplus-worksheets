# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Taxas e índices socioeconômicos (EM13MAT104)
  python3 tools/gen_br_matematica_em3_taxas_e_indices.py
Variação percentual, inflação acumulada (fatores multiplicados), poder de compra e reajuste real,
taxas por mil e por 100 mil habitantes, renda per capita, taxa de desemprego, índices entre 0 e 1 (como o IDH) e pontos percentuais.
Valores das situações são fictícios.
Erros: somar inflações mensais, confundir pontos percentuais com porcentagem, comparar números absolutos de populações diferentes.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, unit, R2, num, tab

R = random.Random(93003)


def s1_variacao():
    k = R.choice(["var", "var", "acum", "acum", "pp"])
    if k == "var":
        a = R.choice([200, 250, 400, 500, 800, 1000, 1200, 1500])
        p = R.choice([-20, -15, -10, -5, 5, 8, 10, 12, 15, 20, 25, 40])
        b = a * F(100 + p, 100)
        return M("Um preço passou de %s para %s. Qual foi a variação percentual?" % (R2(a), R2(b)), ("+" if p > 0 else "−") + "%d%%" % abs(p), [("+" if p > 0 else "−") + "%s%%" % d(abs(b - a) * 100 / b, 1), ("−" if p > 0 else "+") + "%d%%" % abs(p), ("+" if p > 0 else "−") + "%s%%" % d(abs(b - a))],
                 "(%s − %s) ÷ %s = <b>%s%d%%</b>." % (d(b), num(a), num(a), "+" if p > 0 else "−", abs(p)))
    if k == "acum":
        rs = R.choice([(10, 10), (5, 4), (10, 20), (2, 3), (20, 10), (5, 10), (10, -10), (50, -20)])
        f = F(100 + rs[0], 100) * F(100 + rs[1], 100)
        tot = (f - 1) * 100
        return M("Num período, a inflação foi de %d%% e, no seguinte, de %s%d%%. Qual foi a variação acumulada?" % (rs[0], "−" if rs[1] < 0 else "", abs(rs[1])), ("+" if tot >= 0 else "−") + "%s%%" % d(abs(tot)), ["+%d%%" % (rs[0] + rs[1]) if rs[0] + rs[1] >= 0 else "−%d%%" % abs(rs[0] + rs[1]), "+%s%%" % d(abs(tot) + 1), "+%d%%" % (rs[0] * rs[1]) if rs[0] * rs[1] > 0 else "0%"],
                 "%s · %s = %s ⇒ <b>%s%s%%</b>." % (d(F(100 + rs[0], 100)), d(F(100 + rs[1], 100)), d(f), "+" if tot >= 0 else "−", d(abs(tot))))
    a, b = R.sample(range(5, 16), 2)
    return M("A taxa de desemprego passou de %d%% para %d%%. Qual foi a variação, em pontos percentuais?" % (a, b), "%s%d pontos percentuais" % ("+" if b > a else "−", abs(b - a)), ["%s%s%%" % ("+" if b > a else "−", d(F(abs(b - a) * 100, a), 1)), "%s%d pontos percentuais" % ("−" if b > a else "+", abs(b - a)), "%d pontos percentuais" % (a + b)],
             "%d − %d = <b>%s%d p.p.</b> (em porcentagem da taxa antiga, seria %s%%)." % (b, a, "+" if b > a else "−", abs(b - a), d(F(abs(b - a) * 100, a), 1)))


def s2_poder():
    k = R.choice(["real", "real", "compra"])
    if k == "real":
        rj, inf = R.choice([(10, 10), (5, 5), (8, 4), (12, 5), (6, 10), (15, 10), (4, 4), (3, 5), (7, 3), (9, 6), (10, 4), (20, 10), (2, 6), (6, 3)])
        real = (F(100 + rj, 100) / F(100 + inf, 100) - 1) * 100
        txt = ("ganho real de cerca de %s%%" % d(real, 1)) if real > 0 else ("perda real de cerca de %s%%" % d(-real, 1)) if real < 0 else "nenhum ganho real (0%)"
        w = ["ganho real de %d%%" % (rj - inf) if rj != inf else "ganho real de %d%%" % rj, "perda real de cerca de %s%%" % d(abs(real) + 2, 1), "ganho real de %d%%" % rj]
        return M("Um salário teve reajuste de %d%% num ano em que a inflação foi de %d%%. O que aconteceu com o poder de compra?" % (rj, inf), txt, w,
                 "%s ÷ %s = %s ⇒ <b>%s</b>." % (d(F(100 + rj, 100)), d(F(100 + inf, 100)), d(F(100 + rj, 100) / F(100 + inf, 100), 4), txt))
    inf = R.choice([10, 20, 25, 40, 50, 60, 100])
    return M("Os preços subiram %d%% e o salário não mudou. Que fração do que se comprava antes ainda se compra?" % inf, "cerca de %s%%" % d(F(100, 100 + inf) * 100, 1), ["%d%%" % (100 - inf), "%d%%" % (100 + inf), "100%"],
             "1 ÷ %s ≈ %s: <b>cerca de %s%%</b>." % (d(F(100 + inf, 100)), d(F(100, 100 + inf), 3), d(F(100, 100 + inf) * 100, 1)))


def s3_taxas():
    k = R.choice(["mil", "cemmil", "percapita", "desemprego", "comparar"])
    if k == "mil":
        pop = R.choice([50000, 80000, 120000, 200000, 250000])
        t = R.choice([10, 12, 14, 15, 16, 18])
        n = pop * t // 1000
        return M("Uma cidade de %s habitantes teve %s nascimentos num ano. Qual é a taxa de natalidade, por mil habitantes?" % (num(pop), num(n)), "%d por mil" % t, ["%s por mil" % d(F(n * 100, pop), 1), "%s por mil" % num(n), "%d por mil" % (t * 10)], "%s ÷ %s × 1.000 = <b>%d por mil</b>." % (num(n), num(pop), t))
    if k == "cemmil":
        pop = R.choice([200000, 500000, 1000000, 2000000])
        t = R.choice([5, 8, 10, 12, 20, 25])
        n = pop * t // 100000
        return M("Num estado com %s habitantes houve %s casos de uma doença. Qual é a taxa por 100 mil habitantes?" % (num(pop), num(n)), "%d por 100 mil" % t, ["%s por 100 mil" % num(n), "%s por 100 mil" % d(F(n * 1000, pop), 1), "%d por 100 mil" % (t * 10)], "%s ÷ %s × 100.000 = <b>%d</b>." % (num(n), num(pop), t))
    if k == "percapita":
        pib = R.choice([2, 3, 5, 6, 12])
        pop = R.choice([40000, 50000, 60000, 100000, 120000])
        v = F(pib * 10 ** 9, pop)
        if v.denominator != 1:
            return None
        return M("Um município tem PIB de R$ %d bilhões e %s habitantes. Qual é o PIB per capita?" % (pib, num(pop)), R2(v), [R2(v / 10), R2(v * 10), R2(F(pib * 10 ** 6, pop))], "%d.000.000.000 ÷ %s = <b>%s</b> por habitante." % (pib, num(pop), R2(v)))
    if k == "desemprego":
        fo = R.choice([1000, 2000, 5000, 8000, 10000])
        p = R.choice([6, 8, 9, 10, 12, 14])
        des = fo * p // 100
        return M("Numa cidade, a força de trabalho (pessoas trabalhando ou procurando trabalho) é de %s pessoas, e %s estão desocupadas. Qual é a taxa de desemprego?" % (num(fo), num(des)), "%d%%" % p, ["%s%%" % d(F(des * 100, fo + des), 1), "%d%%" % (100 - p), "%s%%" % num(des)], "%s ÷ %s = <b>%d%%</b>." % (num(des), num(fo), p))
    a, pa, b, pb = R.choice([(300, 100000, 500, 400000), (120, 50000, 200, 200000), (80, 20000, 150, 100000), (600, 300000, 900, 900000)])
    ta, tb = F(a * 100000, pa), F(b * 100000, pb)
    mais = "a cidade A" if ta > tb else "a cidade B"
    return M("A cidade A (%s hab.) teve %d acidentes; a cidade B (%s hab.) teve %d. Proporcionalmente à população, qual teve mais acidentes?" % (num(pa), a, num(pb), b), mais, ["a cidade B" if mais == "a cidade A" else "a cidade A", "as duas igualmente", "não dá para comparar"],
             "Por 100 mil hab.: A = %s; B = %s ⇒ <b>%s</b>." % (d(ta), d(tb), mais))


s4_indices = bank(R, [
    ("O IDH (Índice de Desenvolvimento Humano) varia…", "de 0 a 1", ["de 0 a 100", "de 1 a 10", "de −1 a 1"]),
    ("O IDH combina indicadores de…", "saúde, educação e renda", ["só renda", "só população", "clima e área"]),
    ("Um país com IDH 0,85 em relação a outro com IDH 0,60 tem…", "desenvolvimento humano maior", ["menos habitantes", "mais renda com certeza", "menor área"]),
    ("A inflação mede…", "o aumento geral dos preços num período", ["o aumento dos salários", "a quantidade de dinheiro no banco", "o PIB per capita"]),
    ("Uma inflação de 1% ao mês durante 12 meses dá, no ano, …", "um pouco mais de 12%", ["exatamente 12%", "1%", "menos de 12%"]),
    ("Se a taxa de juros passa de 10% para 12%, ela subiu…", "2 pontos percentuais (20%)", ["2%", "12 pontos percentuais", "20 pontos percentuais"]),
    ("Para comparar a violência em duas cidades de tamanhos diferentes, deve-se usar…", "taxas por 100 mil habitantes", ["o número total de casos", "a área das cidades", "o número de bairros"]),
    ("O PIB per capita é…", "o PIB dividido pela população", ["o PIB multiplicado pela população", "o salário mínimo", "a renda da pessoa mais rica"]),
    ("Um reajuste salarial igual à inflação mantém…", "o mesmo poder de compra", ["um ganho real", "uma perda real", "o salário igual em reais"]),
], "s4_indices")


def main():
    seen = set()
    sets = [
        ("Variação percentual", mix(R, seen, [(s1_variacao, 20)])),
        ("Inflação e poder de compra", mix(R, seen, [(s2_poder, 12), (s1_variacao, 8)])),
        ("Taxas por mil e por 100 mil", mix(R, seen, [(s3_taxas, 20)])),
        ("Índices socioeconômicos", mix(R, seen, [(s4_indices, 9), (s3_taxas, 11)])),
        ("Revisão", mix(R, seen, [(s1_variacao, 8), (s2_poder, 6), (s3_taxas, 6)])),
    ]
    body = lesson(
        ["<b>Variação percentual</b> = (valor novo − valor antigo) ÷ valor antigo.",
         "Taxas de períodos seguidos se <b>multiplicam</b>: 10% e 10% dão 1,1 · 1,1 = 1,21, ou seja, 21%.",
         "<b>Ganho real</b>: (1 + reajuste) ÷ (1 + inflação) − 1. Se o salário sobe menos que a inflação, o poder de compra cai.",
         "Para comparar lugares de tamanhos diferentes, use <b>taxas</b>: por mil, por 100 mil habitantes, per capita.",
         "Diferença entre duas porcentagens é medida em <b>pontos percentuais</b> (de 10% para 12%: +2 p.p.)."],
        [("Inflação de 5% e depois 4%", ["1,05 · 1,04 = 1,092"], "9,2% acumulados"),
         ("Reajuste de 8% com inflação de 4%", ["1,08 ÷ 1,04 ≈ 1,038"], "ganho real de cerca de 3,8%")],
        [["Somar inflações", "Multiplique os fatores."],
         ["Confundir p.p. e %", "De 10% para 12% são 2 p.p., mas 20% de aumento."],
         ["Comparar números absolutos", "Divida pela população."]])
    faq = [("Como calcular a inflação acumulada?", "Multiplique os fatores de cada período e subtraia 1. Com 10% e 5%: 1,10 · 1,05 = 1,155, ou seja, 15,5% acumulados."),
           ("O que a BNCC pede?", "Interpretar taxas e índices de natureza socioeconômica (índice de desenvolvimento humano, taxas de inflação, entre outros), investigando os processos de cálculo desses números, para analisar criticamente a realidade e produzir argumentos (EM13MAT104).")]
    unit(R, "taxas-e-indices", "N", ["EM13MAT104"],
         "Interpretar taxas e índices de natureza socioeconômica (índice de desenvolvimento humano, taxas de inflação, entre outros), investigando os processos de cálculo desses números, para analisar criticamente a realidade e produzir argumentos",
         "Taxas e índices socioeconômicos", "Taxas e índices",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre taxas e índices: variação percentual, inflação acumulada, poder de compra, pontos percentuais, taxas por mil e por 100 mil habitantes, PIB per capita e IDH. 100 exercícios com gabarito.",
         "Taxas seguidas se multiplicam", "Compare lugares com taxas, não com totais.",
         body, faq, sets, 3, grade="3-serie")


if __name__ == "__main__":
    main()
