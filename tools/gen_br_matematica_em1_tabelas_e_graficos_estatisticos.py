# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Tabelas e gráficos estatísticos (EM13MAT102, EM13MAT406)
  python3 tools/gen_br_matematica_em1_tabelas_e_graficos_estatisticos.py
Tabelas de frequência (absoluta, relativa e acumulada), classes e histogramas, gráficos de setores,
análise crítica de gráficos e pesquisas divulgados pela mídia (escalas, amostras inadequadas).
Usa geradores do 8º ano (classes, histograma) e do 9º ano (gráficos que enganam, leitura, frequência) com outro sorteio.
Erros: somar frequências relativas e não dar 100%, confundir frequência acumulada com relativa, acreditar num gráfico com eixo cortado.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, tab

R = random.Random(91014)
g_engan, g_ler = use("gen_br_matematica_9_graficos_e_estatistica", 91907, "s1_enganoso", "s3_ler")
g_freq = use("gen_br_matematica_9_pesquisa_amostral", 91908, "s4_frequencia")
c_classes, c_histo = use("gen_br_matematica_8_graficos_e_classes_de_frequencia", 91909, "s1_classes", "s3_histo")


def s1_acum():
    xs = [0, 1, 2, 3, 4]
    tot = R.choice([20, 25, 40, 50])
    while True:
        cuts = sorted(R.sample(range(1, tot), 4))
        fs = [cuts[0]] + [cuts[i] - cuts[i - 1] for i in range(1, 4)] + [tot - cuts[3]]
        if min(fs) >= 1:
            break
    t = tab([["Nº de irmãos", "Frequência"]] + [[str(x), str(f)] for x, f in zip(xs, fs)])
    k = R.choice(["acum", "rel", "pelo", "menos"])
    i = R.randint(1, 3)
    if k == "acum":
        a = sum(fs[:i + 1])
        return M(t + "Qual é a frequência acumulada até %d irmãos?" % i, str(a), [str(fs[i]), str(sum(fs[:i])), str(tot - a) if tot - a != a else str(a + 1)], "%s = <b>%d</b>." % (" + ".join(map(str, fs[:i + 1])), a))
    if k == "rel":
        p = F(fs[i] * 100, tot)
        return M(t + "Qual é a frequência relativa dos alunos com %d %s?" % (i, "irmão" if i == 1 else "irmãos"), "%s%%" % d(p), ["%d%%" % fs[i], "%s%%" % d(F(sum(fs[:i + 1]) * 100, tot)), "%s%%" % d(100 - p)],
                 "%d ÷ %d = <b>%s%%</b>." % (fs[i], tot, d(p)))
    if k == "pelo":
        a = sum(fs[i:])
        p = F(a * 100, tot)
        return M(t + "Que porcentagem dos alunos tem pelo menos %d %s?" % (i, "irmão" if i == 1 else "irmãos"), "%s%%" % d(p), ["%s%%" % d(F(fs[i] * 100, tot)), "%s%%" % d(100 - p), "%d%%" % a],
                 "(%s) ÷ %d = %d ÷ %d = <b>%s%%</b>." % (" + ".join(map(str, fs[i:])), tot, a, tot, d(p)))
    a = sum(fs[:i])
    return M(t + "Quantos alunos têm menos de %d irmãos?" % i, str(a), [str(sum(fs[:i + 1])), str(fs[i]), str(tot - a)], "%s = <b>%d</b>." % (" + ".join(map(str, fs[:i])), a))


s2_critica = bank(R, [
    ("Um site perguntou aos seus leitores se apoiam uma lei, e 80% disseram «sim». O problema dessa pesquisa é que…", "a amostra não representa a população (só leitores do site, que escolheram responder)", ["80% é muito", "faltou um gráfico", "o site é grande"]),
    ("Um gráfico de colunas compara vendas de 98 e 102 mil, mas o eixo vertical começa em 95 mil. Isso…", "exagera a diferença entre as colunas", ["esconde a diferença", "não muda nada", "deixa o gráfico mais exato"]),
    ("Uma propaganda diz «9 em cada 10 dentistas recomendam», mas ouviu só 10 dentistas escolhidos pela empresa. O resultado é…", "pouco confiável (amostra pequena e escolhida)", ["muito confiável", "exato", "um censo"]),
    ("Num gráfico de setores, as porcentagens somam 115%. Isso indica que…", "há um erro, ou cada pessoa pôde escolher mais de uma opção", ["está correto", "é um censo", "a amostra é grande"]),
    ("Uma notícia diz que «os acidentes dobraram», passando de 2 para 4 numa cidade pequena. Uma leitura crítica é…", "o número é pequeno; dobrar de 2 para 4 pode ser acaso", ["os acidentes estão fora de controle", "a cidade é perigosa", "dobrar é sempre grave"]),
    ("Para comparar o número de crimes em duas cidades de tamanhos diferentes, é melhor usar…", "a taxa por 100 mil habitantes", ["o número total", "a área da cidade", "a quantidade de ruas"]),
    ("Um gráfico de linhas sem título nem unidades nos eixos…", "não permite saber o que está sendo medido", ["é sempre correto", "é mais fácil de ler", "mostra só dados reais"]),
    ("Uma pesquisa eleitoral ouviu 2.000 pessoas sorteadas em todas as regiões, na proporção da população. Essa amostra é…", "representativa", ["viciada", "um censo", "pequena demais para qualquer conclusão"]),
    ("Um gráfico de pictogramas usa um ícone com o dobro da altura e o dobro da largura para mostrar o dobro. Isso…", "exagera a diferença (a área fica 4 vezes maior)", ["está correto", "esconde a diferença", "mostra a metade"]),
    ("A média salarial de uma empresa é alta porque o diretor ganha muito. A medida que representa melhor o salário típico é…", "a mediana", ["a média", "o maior salário", "a amplitude"]),
], "s2_critica")


def main():
    seen = set()
    sets = [
        ("Tabelas de frequência", mix(R, seen, [(s1_acum, 12), (g_freq, 8)])),
        ("Classes e histogramas", mix(R, seen, [(c_classes, 10), (c_histo, 10)])),
        ("Ler gráficos", mix(R, seen, [(g_ler, 14), (g_engan, 6)])),
        ("Leitura crítica", mix(R, seen, [(s2_critica, 10), (g_engan, 10)])),
        ("Revisão", mix(R, seen, [(s1_acum, 8), (c_histo, 6), (g_freq, 6)])),
    ]
    body = lesson(
        ["<b>Frequência absoluta</b>: quantas vezes um valor aparece. <b>Relativa</b>: frequência ÷ total (em %). <b>Acumulada</b>: soma das frequências até aquele valor.",
         "Dados numéricos contínuos são agrupados em <b>classes</b> (150 ⊢ 155) e mostrados num <b>histograma</b>.",
         "Leitura crítica: veja título, unidades, onde começa o eixo, o tamanho e a forma de escolha da amostra, e se as porcentagens somam 100%.",
         "Para comparar grupos de tamanhos diferentes, use taxas e porcentagens, não números absolutos."],
        [("Irmãos: 0 (6), 1 (9), 2 (4), 3 (1). Total 20", ["acumulada até 1: 6 + 9 = 15", "relativa de 1: 9 ÷ 20"], "15 alunos; 45%")],
        [["Relativas que não somam 100%", "Confira a soma; a diferença pode ser arredondamento ou erro."],
         ["Confundir acumulada e relativa", "Acumulada soma até o valor; relativa divide pelo total."],
         ["Confiar no tamanho das colunas", "Veja onde começa o eixo vertical."]])
    faq = [("O que é frequência acumulada?", "É a soma das frequências de um valor e de todos os valores anteriores. Ela responde perguntas como «quantos têm até 2 irmãos»."),
           ("O que a BNCC pede?", "Analisar tabelas, gráficos e amostras de pesquisas estatísticas apresentadas em relatórios divulgados por diferentes meios de comunicação, identificando inadequações que possam induzir a erros de interpretação (EM13MAT102), e construir e interpretar tabelas e gráficos de frequências com base em dados obtidos em pesquisas (EM13MAT406).")]
    unit(R, "tabelas-e-graficos-estatisticos", "E", ["EM13MAT102", "EM13MAT406"],
         "Analisar tabelas, gráficos e amostras de pesquisas estatísticas apresentadas em relatórios divulgados por diferentes meios de comunicação, identificando, quando for o caso, inadequações que possam induzir a erros de interpretação, como escalas e amostras não apropriadas; construir e interpretar tabelas e gráficos de frequências com base em dados obtidos em pesquisas por amostras estatísticas, incluindo ou não o uso de softwares que inter-relacionem estatística, geometria e álgebra",
         "Tabelas e gráficos estatísticos", "Tabelas e gráficos estatísticos",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre estatística: frequência absoluta, relativa e acumulada, classes e histogramas, leitura de gráficos e análise crítica de pesquisas. 100 exercícios com gabarito.",
         "Frequência relativa = frequência ÷ total", "Leia título, unidades e escala.",
         body, faq, sets, 14, grade="1-serie")


if __name__ == "__main__":
    main()
