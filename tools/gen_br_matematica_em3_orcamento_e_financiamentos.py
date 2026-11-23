# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Orçamento, compras e financiamentos (EM13MAT203)
  python3 tools/gen_br_matematica_em3_orcamento_e_financiamentos.py
Orçamento doméstico (porcentagens da renda), à vista ou a prazo (juros embutidos), descontos e acréscimos sucessivos,
parcelamento com entrada, fórmulas de planilha (células e porcentagens), poupança mensal e metas.
Usa geradores do 9º ano (aumentos e descontos sucessivos, comprar e investir) com outro sorteio.
Erros: somar porcentagens sucessivas, calcular a taxa sobre o preço a prazo, esquecer a entrada no total pago.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, R2, num, tab

R = random.Random(93002)
p_suc, p_compra = use("gen_br_matematica_9_porcentagens_e_juros_compostos", 93902, "s2_sucessivos", "s4_compra")
GASTOS = ["aluguel", "alimentação", "transporte", "saúde", "energia e água", "internet e celular", "lazer"]   # do maior para o menor gasto típico


def s1_orcamento():
    renda = R.choice([2000, 2500, 3000, 3600, 4000, 5000, 6000])
    gs = sorted(R.sample(GASTOS, 4), key=GASTOS.index)
    ps = R.choice([(30, 25, 10, 5), (35, 20, 15, 10), (25, 30, 10, 5), (40, 20, 10, 5), (30, 20, 15, 10)])
    rows = [["Gasto", "% da renda"]] + [[g, "%d%%" % p] for g, p in zip(gs, ps)]
    k = R.choice(["valor", "sobra", "pct"])
    if k == "valor":
        i = R.randrange(4)
        return M(tab(rows) + "Uma família tem renda de %s por mês. Quanto gasta com %s?" % (R2(renda), gs[i]), R2(F(renda * ps[i], 100)), [R2(ps[i] * 10), R2(F(renda * (100 - ps[i]), 100)), R2(F(renda, 4))],
                 "%d%% de %s = <b>%s</b>." % (ps[i], num(renda), R2(F(renda * ps[i], 100))))
    if k == "sobra":
        s = 100 - sum(ps)
        return M(tab(rows) + "Uma família tem renda de %s e gasta conforme a tabela. Quanto sobra por mês?" % R2(renda), R2(F(renda * s, 100)), [R2(F(renda * sum(ps), 100)), R2(s * 10), R2(F(renda * (s + 5), 100))],
                 "Gastos: %d%%; sobram %d%% de %s = <b>%s</b>." % (sum(ps), s, num(renda), R2(F(renda * s, 100))))
    v = R.choice([300, 450, 600, 750, 900])
    p = F(v * 100, renda)
    if (p * 10).denominator != 1:
        return None
    return M("Uma pessoa ganha %s e gasta %s com transporte. Que porcentagem da renda vai para o transporte?" % (R2(renda), R2(v)), "%s%%" % d(p), ["%s%%" % d(F(renda, v), 1), "%d%%" % (v // 10), "%s%%" % d(100 - p)], "%s ÷ %s = <b>%s%%</b>." % (num(v), num(renda), d(p)))


def s2_prazo():
    k = R.choice(["juros", "total", "entrada", "avista"])
    P = R.choice([600, 800, 1000, 1200, 1500, 2000, 2400, 3000])
    if k == "juros":
        n = R.choice([4, 5, 6, 10, 12])
        parc = (P * F(R.choice([105, 110, 112, 115, 120]), 100)) / n
        if (parc * 100).denominator != 1:
            return None
        tot = parc * n
        return M("Um produto custa %s à vista ou %d parcelas de %s. Qual é o acréscimo, em porcentagem, do preço a prazo?" % (R2(P), n, R2(parc)), "%s%%" % d((tot - P) * 100 / P), ["%s%%" % d((tot - P) * 100 / tot, 1), "%s%%" % d(F(tot - P, n), 1), R2(tot - P)],
                 "Total a prazo: %d × %s = %s; acréscimo %s ÷ %s = <b>%s%%</b>." % (n, R2(parc), R2(tot), d(tot - P), num(P), d((tot - P) * 100 / P)))
    if k == "total":
        n = R.choice([3, 5, 6, 10, 12])
        parc = R.choice([F(9990, 100), F(149, 1), F(25990, 100), F(79, 1), F(19990, 100)])
        return M("Quanto se paga, no total, em %d parcelas de %s?" % (n, R2(parc)), R2(parc * n), [R2(parc * (n - 1)), R2(parc + n), R2(parc * n * F(11, 10))], "%d × %s = <b>%s</b>." % (n, R2(parc), R2(parc * n)))
    if k == "entrada":
        e = R.choice([F(1, 5), F(1, 4), F(3, 10)])
        n = R.choice([4, 5, 6, 10])
        resto = P * (1 - e)
        if (resto / n * 100).denominator != 1:
            return None
        return M("Uma loja vende um produto de %s com entrada de %s%% e o restante em %d parcelas iguais sem juros. Qual é o valor de cada parcela?" % (R2(P), d(e * 100), n), R2(resto / n), [R2(F(P, n)), R2(P * e), R2(resto / (n + 1))],
                 "Entrada %s; restam %s; ÷ %d = <b>%s</b>." % (R2(P * e), R2(resto), n, R2(resto / n)))
    desc = R.choice([5, 8, 10, 12, 15])
    n = R.choice([3, 4, 5])
    return M("Um celular custa %s em %d vezes sem juros, ou com %d%% de desconto à vista. Quanto se economiza pagando à vista?" % (R2(P), n, desc), R2(F(P * desc, 100)), [R2(F(P * (100 - desc), 100)), R2(F(P, n)), R2(desc * n)],
             "%d%% de %s = <b>%s</b>." % (desc, num(P), R2(F(P * desc, 100))))


def s3_planilha():
    k = R.choice(["formula", "formula", "valor", "meta"])
    if k == "formula":
        q, a, w = R.choice([
            ("Numa planilha, o preço está na célula B2. Qual fórmula calcula o preço com 10% de desconto?", "=B2*0,9", ["=B2*0,1", "=B2-10", "=B2*1,1"]),
            ("Numa planilha, o preço está na célula B2. Qual fórmula calcula o preço com 15% de aumento?", "=B2*1,15", ["=B2*0,15", "=B2+15", "=B2*0,85"]),
            ("Os gastos estão nas células B2 a B6. Qual fórmula dá o total?", "=SOMA(B2:B6)", ["=B2+B6", "=MÉDIA(B2:B6)", "=B2*B6"]),
            ("A renda está em B1 e o total de gastos em B8. Qual fórmula mostra quanto sobra?", "=B1-B8", ["=B8-B1", "=B1+B8", "=B1*B8"]),
            ("O capital está em B1 e a taxa mensal (em decimal) em B2. Qual fórmula dá o montante após 12 meses a juros compostos?", "=B1*(1+B2)^12", ["=B1*B2*12", "=B1*(1+B2*12)", "=B1+B2^12"]),
            ("Um gasto está em B3 e a renda em B1. Qual fórmula dá a porcentagem da renda (em decimal)?", "=B3/B1", ["=B1/B3", "=B3*B1", "=B1-B3"]),
        ])
        return M(q, a, w, "Resposta: <b>%s</b>." % a)
    if k == "valor":
        b2 = R.choice([120, 250, 400, 80, 1500])
        f, pct = R.choice([("1,1", 110), ("0,9", 90), ("1,25", 125), ("0,8", 80), ("1,05", 105)])
        return M("Se a célula B2 contém %s e a célula C2 contém a fórmula =B2*%s, qual valor aparece em C2?" % (num(b2), f), d(F(b2 * pct, 100)), [d(b2 + F(pct, 10)), d(F(b2 * (200 - pct), 100)), d(F(b2 * pct, 1000))], "%s × %s = <b>%s</b>." % (num(b2), f, d(F(b2 * pct, 100))))
    meta = R.choice([1200, 1800, 2400, 3000, 3600, 6000])
    m = R.choice([6, 10, 12, 15, 20])
    if meta % m:
        return None
    return M("Para juntar %s em %d meses (sem rendimento), quanto é preciso guardar por mês?" % (R2(meta), m), R2(F(meta, m)), [R2(F(meta, m + 2)), R2(meta * m // 100), R2(F(meta, m) * 2)], "%s ÷ %d = <b>%s</b>." % (num(meta), m, R2(F(meta, m))))


def main():
    seen = set()
    sets = [
        ("Orçamento doméstico", mix(R, seen, [(s1_orcamento, 20)])),
        ("À vista ou a prazo", mix(R, seen, [(s2_prazo, 20)])),
        ("Descontos e aumentos sucessivos", mix(R, seen, [(p_suc, 14), (p_compra, 6)])),
        ("Planilhas e metas", mix(R, seen, [(s3_planilha, 20)])),
        ("Revisão", mix(R, seen, [(s1_orcamento, 7), (s2_prazo, 8), (p_compra, 5)])),
    ]
    body = lesson(
        ["Um <b>orçamento</b> compara a renda com os gastos. Escrever cada gasto como porcentagem da renda ajuda a decidir onde economizar.",
         "Compra <b>a prazo</b>: some todas as parcelas (e a entrada) e compare com o preço à vista. O acréscimo % é (total − à vista) ÷ à vista.",
         "Aumentos e descontos <b>sucessivos</b> se multiplicam: +10% e depois −10% dá 1,1 · 0,9 = 0,99, uma perda de 1%.",
         "Em <b>planilhas</b>, as fórmulas usam células: =B2*0,9 dá 10% de desconto; =SOMA(B2:B6) soma um intervalo."],
        [("R$ 1.200 à vista ou 6 × R$ 220", ["total 1.320", "120 ÷ 1.200 = 0,1"], "10% a mais a prazo")],
        [["Somar porcentagens sucessivas", "Multiplique os fatores."],
         ["Calcular o acréscimo sobre o total a prazo", "A base é o preço à vista."],
         ["Esquecer a entrada", "Total pago = entrada + parcelas."]])
    faq = [("Como saber se vale a pena comprar a prazo?", "Some todas as parcelas e compare com o preço à vista. A diferença, dividida pelo preço à vista, é o acréscimo; se houver desconto à vista, compare também com o que o dinheiro renderia aplicado."),
           ("O que a BNCC pede?", "Planejar e executar ações envolvendo a criação e a utilização de aplicativos, jogos (digitais ou não), planilhas para o controle de orçamento familiar, simuladores de cálculos de juros compostos, dentre outros, para aplicar conceitos matemáticos e tomar decisões (EM13MAT203).")]
    unit(R, "orcamento-e-financiamentos", "N", ["EM13MAT203"],
         "Aplicar conceitos matemáticos no planejamento, na execução e na análise de ações envolvendo a utilização de aplicativos e a criação de planilhas (para o controle de orçamento familiar, simuladores de cálculos de juros simples e compostos, entre outros), para tomar decisões",
         "Orçamento, compras e financiamentos", "Orçamento e financiamentos",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre educação financeira: orçamento doméstico, à vista ou a prazo, entrada e parcelas, descontos sucessivos, fórmulas de planilha e metas de poupança. 100 exercícios com gabarito.",
         "Compare o total a prazo com o preço à vista", "Porcentagens sucessivas se multiplicam.",
         body, faq, sets, 2, grade="3-serie")


if __name__ == "__main__":
    main()
