# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Tabelas, gráficos, pesquisas e fluxogramas (Probabilidade e estatística, EF06MA31–EF06MA34)
  python3 tools/gen_br_matematica_6_tabelas_e_graficos.py
Ler tabelas simples e de dupla entrada; gráficos de colunas, barras e linhas (título, eixos, fonte, escala); variáveis
qualitativas e quantitativas; etapas de uma pesquisa; fluxogramas simples.
Usa geradores do 5º ano (tabelas e gráficos) e do 9º ano (ler gráficos) com outro sorteio.
Erros: ler o valor da coluna errada, não olhar a escala, confundir variável qualitativa e quantitativa.
"""
import random
from br_common import lesson, mix, use
from br_9 import M, bank, unit

R = random.Random(86021)
t_dupla, t_col, t_lin = use("gen_br_matematica_5_tabelas_e_graficos", 86921, "s1_dupla", "s2_colunas", "s3_linhas")
g_ler, g_linhas = use("gen_br_matematica_9_graficos_e_estatistica", 86922, "s3_ler", "s6_linhas")

VAR = [("cor dos olhos", "qualitativa"), ("número de irmãos", "quantitativa"), ("altura em cm", "quantitativa"), ("esporte preferido", "qualitativa"), ("idade em anos", "quantitativa"),
       ("sabor de sorvete preferido", "qualitativa"), ("tempo de estudo por dia (min)", "quantitativa"), ("bairro onde mora", "qualitativa"), ("número do calçado", "quantitativa"),
       ("meio de transporte para a escola", "qualitativa"), ("massa da mochila (kg)", "quantitativa"), ("estação do ano preferida", "qualitativa")]


def s1_variavel():
    v, a = R.choice(VAR)
    return M("Numa pesquisa com a turma, a variável <b>%s</b> é…" % v, a, [x for x in ["qualitativa", "quantitativa", "uma constante", "um gráfico"] if x != a],
             "%s: <b>%s</b>." % ("Os valores são números (contagens ou medidas)" if a == "quantitativa" else "Os valores são categorias, não números", a))


s2_pesquisa = bank(R, [
    ("Qual é a primeira etapa de uma pesquisa?", "definir o tema e a pergunta", ["fazer o gráfico", "escrever a conclusão", "calcular a média"]),
    ("Depois de coletar os dados, o próximo passo é…", "organizar os dados em tabelas", ["escolher o tema", "apagar os dados repetidos", "escrever a pergunta"]),
    ("Num gráfico, a <b>fonte</b> indica…", "de onde vieram os dados", ["o maior valor", "a cor das colunas", "o título"]),
    ("Para comparar a quantidade de alunos de cada turma, o melhor gráfico é o…", "de colunas", ["de linhas", "de setores sem números", "nenhum"]),
    ("Para mostrar a temperatura ao longo dos dias da semana, o melhor gráfico é o…", "de linhas", ["de setores", "de colunas empilhadas sem datas", "pictograma de animais"]),
    ("Numa tabela de dupla entrada, cada número está no cruzamento de…", "uma linha e uma coluna", ["duas linhas", "dois gráficos", "dois títulos"]),
    ("Todo gráfico deve ter…", "título, eixos com nomes e fonte", ["só as colunas", "só o título", "cores diferentes"]),
    ("Uma planilha eletrônica ajuda a…", "organizar dados e fazer gráficos", ["inventar dados", "escolher o tema", "responder a pesquisa"]),
], "s2_pesquisa")


s3_fluxo = bank(R, [
    ("Num fluxograma, o losango representa…", "uma pergunta (decisão sim/não)", ["o início", "o fim", "um cálculo"]),
    ("Num fluxograma, o retângulo representa…", "uma ação ou cálculo", ["uma pergunta", "o início e o fim", "um erro"]),
    ("Um fluxograma: «Leia N → N é divisível por 2? → sim: escreva PAR; não: escreva ÍMPAR». Para N = 15, a saída é…", "ÍMPAR", ["PAR", "15", "nenhuma"]),
    ("Um fluxograma: «Leia N → multiplique por 3 → some 4 → escreva o resultado». Para N = 5, a saída é…", "19", ["27", "12", "17"]),
    ("Um fluxograma: «Leia N → N &gt; 10? → sim: subtraia 10; não: some 10 → escreva». Para N = 7, a saída é…", "17", ["−3", "7", "10"]),
    ("Um fluxograma: «Leia N → divida por 2 → some 1 → escreva». Para N = 30, a saída é…", "16", ["15", "31", "14"]),
    ("Um fluxograma: «Leia a nota → nota ≥ 6? → sim: APROVADO; não: RECUPERAÇÃO». Para a nota 5,5, a saída é…", "RECUPERAÇÃO", ["APROVADO", "5,5", "6"]),
    ("Um fluxograma: «Comece com 1 → dobre → o número passou de 50? → não: volte e dobre; sim: escreva». A saída é…", "64", ["32", "50", "128"]),
    ("Num fluxograma, as setas mostram…", "a ordem dos passos", ["os números", "as respostas certas", "a fonte"]),
], "s3_fluxo")


def main():
    seen = set()
    sets = [
        ("Tabelas", mix(R, seen, [(t_dupla, 14), (s2_pesquisa, 6)])),
        ("Gráficos de colunas", mix(R, seen, [(t_col, 10), (g_ler, 10)])),
        ("Gráficos de linhas", mix(R, seen, [(t_lin, 10), (g_linhas, 10)])),
        ("Variáveis e pesquisas", mix(R, seen, [(s1_variavel, 12), (s2_pesquisa, 2), (g_ler, 6)])),
        ("Fluxogramas", mix(R, seen, [(s3_fluxo, 9), (t_dupla, 5), (t_col, 6)])),
    ]
    body = lesson(
        ["Leia sempre o <b>título</b>, os <b>nomes dos eixos</b>, a <b>escala</b> e a <b>fonte</b> antes de tirar conclusões.",
         "Gráfico de colunas compara categorias; gráfico de linhas mostra como algo muda ao longo do tempo.",
         "Uma variável é <b>qualitativa</b> quando os valores são categorias (cor, esporte) e <b>quantitativa</b> quando são números (idade, altura).",
         "Um <b>fluxograma</b> mostra os passos de um processo: retângulos para ações, losangos para perguntas, setas para a ordem."],
        [("Pesquisa «esporte preferido»", ["variável qualitativa", "tabela de frequência", "gráfico de colunas"], "organizar e comunicar")],
        [["Ler a coluna errada", "Siga a coluna até o eixo com o dedo ou a régua."],
         ["Ignorar a escala", "Veja quanto vale cada linha do eixo."],
         ["Confundir os tipos de variável", "Número de irmãos é quantitativa; cor dos olhos é qualitativa."]])
    faq = [("O que é uma tabela de dupla entrada?", "É uma tabela com duas variáveis: uma nas linhas e outra nas colunas. Cada número está no cruzamento de uma linha com uma coluna."),
           ("O que a BNCC pede no 6º ano?", "Identificar as variáveis e suas frequências e os elementos constitutivos de gráficos (EF06MA31), interpretar e resolver situações que envolvam dados de pesquisas em tabelas e gráficos (EF06MA32), planejar e coletar dados de pesquisa (EF06MA33) e interpretar e desenvolver fluxogramas simples (EF06MA34).")]
    unit(R, "tabelas-e-graficos", "E", ["EF06MA31", "EF06MA32", "EF06MA33", "EF06MA34"],
         "Identificar as variáveis e suas frequências e os elementos constitutivos (título, eixos, legendas, fontes e datas) em diferentes tipos de gráfico; interpretar e resolver situações que envolvam dados de pesquisas sobre contextos ambientais, sustentabilidade, trânsito, consumo responsável, entre outros, apresentadas pela mídia em tabelas e em diferentes tipos de gráficos; planejar e coletar dados de pesquisa referente a práticas sociais escolhidas pelos alunos; interpretar e desenvolver fluxogramas simples",
         "Tabelas, gráficos, pesquisas e fluxogramas", "Tabelas e gráficos",
         "Atividades de matemática para o 6º ano sobre tabelas e gráficos: tabelas de dupla entrada, gráficos de colunas e de linhas, variáveis qualitativas e quantitativas, etapas de uma pesquisa e fluxogramas. 100 exercícios com gabarito.",
         "Título, eixos, escala e fonte.", "Colunas comparam; linhas mostram o tempo.",
         body, faq, sets, 21, grade="6-ano")


if __name__ == "__main__":
    main()
