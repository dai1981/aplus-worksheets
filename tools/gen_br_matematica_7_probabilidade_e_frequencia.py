# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Probabilidade e frequência relativa (Probabilidade e estatística, EF07MA34)
  python3 tools/gen_br_matematica_7_probabilidade_e_frequencia.py
Experimentos aleatórios; espaço amostral (inclusive com dois dados e duas moedas); probabilidade teórica; frequência relativa em
experimentos repetidos e estimativa da probabilidade; prever quantas vezes um resultado deve ocorrer.
Usa geradores do 6º ano (probabilidade) com outro sorteio.
Erros: contar (1, 2) e (2, 1) como um só resultado, achar que a soma 7 tem a mesma chance que a soma 2, confundir frequência com probabilidade.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, fq, bank, tab, unit

R = random.Random(87018)
p_urna, p_dado = use("gen_br_matematica_6_probabilidade", 87918, "s1_urna", "s2_dado")


def s1_dois_dados():
    k = R.choice(["soma", "iguais", "maior"])
    if k == "soma":
        s = R.randint(2, 12)
        n = 6 - abs(7 - s)
        return M("Lançando dois dados comuns, qual é a probabilidade de a soma ser %d?" % s, fq(F(n, 36)), [fq(F(1, 11)), fq(F(n, 12)) if F(n, 12) < 1 else fq(F(1, 6)), fq(F(n + 1, 36))],
                 "São 36 resultados (6 × 6); a soma %d aparece em %d deles: <b>%s</b>." % (s, n, fq(F(n, 36))))
    if k == "iguais":
        return M("Lançando dois dados comuns, qual é a probabilidade de saírem números iguais?", fq(F(6, 36)), [fq(F(1, 36)), fq(F(1, 2)), fq(F(2, 36))], "(1,1), (2,2), …, (6,6): 6 de 36 = <b>1/6</b>.")
    t = R.randint(2, 5)
    n = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b > 12 - t)
    return M("Lançando dois dados comuns, qual é a probabilidade de a soma ser maior que %d?" % (12 - t), fq(F(n, 36)), [fq(F(t, 11)), fq(F(n, 12)) if F(n, 12) < 1 else fq(F(n + 2, 36)), fq(F(n + 1, 36))],
             "Conte na tabela dos 36 resultados: %d resultados: <b>%s</b>." % (n, fq(F(n, 36))))


def s2_moedas():
    n = R.choice([2, 3])
    k = R.randint(0, n)
    from math import comb
    p = F(comb(n, k), 2 ** n)
    w = {0: "nenhuma cara", 1: "exatamente 1 cara", 2: "exatamente 2 caras", 3: "3 caras"}[k]
    return M("Lançando %d moedas, qual é a probabilidade de sair %s?" % (n, w), fq(p), [fq(F(1, n + 1)), fq(F(1, 2 ** n)) if p != F(1, 2 ** n) else fq(F(1, 2)), fq(F(k, n)) if k and F(k, n) != p else fq(F(3, 4))],
             "O espaço amostral tem %d resultados; %d deles têm %s: <b>%s</b>." % (2 ** n, comb(n, k), w, fq(p)))


def s3_frequencia():
    n = R.choice([50, 100, 200, 400, 500])
    cats = R.sample(["azul", "vermelho", "verde", "amarelo"], 3)
    while True:
        a, b = R.randint(n // 10, n // 2), R.randint(n // 10, n // 3)
        c = n - a - b
        if c > 0 and len({a, b, c}) == 3:
            break
    t = tab([["Cor", "Vezes"]] + [[x, str(v)] for x, v in zip(cats, [a, b, c])])
    i = R.randrange(3)
    v = [a, b, c][i]
    k = R.choice(["fr", "prev"])
    if k == "fr":
        return M(t + "Uma roleta foi girada %d vezes. Qual foi a frequência relativa da cor %s?" % (n, cats[i]), "%s%%" % d(F(v * 100, n)), ["%d%%" % v if v != F(v * 100, n) else "%d%%" % (v + 5), "%s%%" % d(F(100, 3), 1), "%s%%" % d(F((n - v) * 100, n))],
                 "%d ÷ %d = %s = <b>%s%%</b>." % (v, n, d(F(v, n)), d(F(v * 100, n))))
    m = R.choice([1000, 2000, 5000])
    return M(t + "Uma roleta foi girada %d vezes. Se for girada %s vezes, quantas vezes se espera a cor %s?" % (n, d(m), cats[i]), "cerca de %s" % d(F(v * m, n)), ["cerca de %s" % d(v * 10), "cerca de %s" % d(F(m, 3), 0), "cerca de %s" % d(F((n - v) * m, n))],
             "Frequência relativa %s; × %s ≈ <b>%s</b>." % (d(F(v, n)), d(m), d(F(v * m, n))))


s4_conceitos = bank(R, [
    ("Quantos resultados tem o espaço amostral de lançar dois dados?", "36", ["12", "11", "6"]),
    ("Lançando dois dados, qual soma é mais provável?", "7", ["12", "2", "todas têm a mesma chance"]),
    ("(1, 2) e (2, 1) no lançamento de dois dados são…", "resultados diferentes", ["o mesmo resultado", "impossíveis", "a mesma soma e o mesmo resultado"]),
    ("Frequência relativa é…", "quantas vezes ocorreu ÷ total de repetições", ["a probabilidade teórica", "o número de repetições", "o resultado mais comum"]),
    ("Repetindo um experimento muitas vezes, a frequência relativa tende a…", "ficar perto da probabilidade teórica", ["ficar igual a 1", "ficar igual a 0", "variar cada vez mais"]),
    ("Um dado foi lançado 60 vezes e saiu 6 em 15 delas. Isso sugere que o dado…", "pode estar viciado (esperado: cerca de 10)", ["é perfeito com certeza", "nunca sai 6", "tem 15 faces"]),
    ("Lançando 3 moedas, quantos resultados tem o espaço amostral?", "8", ["6", "3", "9"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Um dado e uma urna", mix(R, seen, [(p_dado, 9), (p_urna, 11)])),
        ("Dois dados", mix(R, seen, [(s1_dois_dados, 16), (s4_conceitos, 4)])),
        ("Moedas", mix(R, seen, [(s2_moedas, 7), (p_urna, 10), (s4_conceitos, 3)])),
        ("Frequência relativa", mix(R, seen, [(s3_frequencia, 20)])),
        ("Revisão", mix(R, seen, [(s3_frequencia, 10), (p_urna, 10)])),
    ]
    body = lesson(
        ["Liste o <b>espaço amostral</b>. Com dois dados há 6 × 6 = 36 resultados; (1, 2) e (2, 1) são diferentes.",
         "Probabilidade = casos favoráveis ÷ casos possíveis (todos igualmente prováveis).",
         "Num experimento repetido, a <b>frequência relativa</b> (vezes que ocorreu ÷ total) estima a probabilidade; quanto mais repetições, melhor a estimativa."],
        [("Soma 7 com dois dados", ["(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)"], "6/36 = 1/6"),
         ("Roleta: azul 45 vezes em 150", ["45 ÷ 150 = 0,3"], "30%")],
        [["Contar (1, 2) e (2, 1) como um só", "São dois resultados diferentes."],
         ["Achar que todas as somas têm a mesma chance", "A soma 7 tem 6 maneiras; a soma 2, só 1."],
         ["Confundir frequência e probabilidade", "Frequência vem do experimento; probabilidade, da contagem."]])
    faq = [("Qual é a diferença entre probabilidade e frequência relativa?", "A probabilidade é calculada contando casos favoráveis e possíveis. A frequência relativa vem de um experimento: quantas vezes o resultado ocorreu dividido pelo número de repetições."),
           ("O que a BNCC pede no 7º ano?", "Planejar e realizar experimentos aleatórios ou simulações que envolvem cálculo de probabilidades ou estimativas por meio de frequência de ocorrências (EF07MA34).")]
    unit(R, "probabilidade-e-frequencia", "E", ["EF07MA34"],
         "Planejar e realizar experimentos aleatórios ou simulações que envolvem cálculo de probabilidades ou estimativas por meio de frequência de ocorrências",
         "Probabilidade e frequência relativa", "Probabilidade e frequência",
         "Atividades de matemática para o 7º ano sobre probabilidade: espaço amostral com dois dados e moedas, probabilidade teórica, frequência relativa e previsões em experimentos. 100 exercícios com gabarito.",
         "Dois dados: 36 resultados.", "Frequência relativa ≈ probabilidade.",
         body, faq, sets, 18, grade="7-ano")


if __name__ == "__main__":
    main()
