# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Pesquisa amostral e relatório (EM13MAT202)
  python3 tools/gen_br_matematica_em3_pesquisa_amostral.py
Planejar uma pesquisa (população, amostra, tipo de amostragem, variáveis), evitar viés, estimar a população a partir da amostra,
margem de erro em pesquisas de opinião (empate técnico), escolher medidas e gráficos para o relatório.
Usa geradores do 8º e do 9º ano (amostragem, viés, estimativas, planejamento) com outro sorteio.
Erros: tratar o resultado da amostra como exato, ignorar a margem de erro, escolher amostras por conveniência.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, num

R = random.Random(93006)
p_pop, p_vies, p_tipos, p_est9 = use("gen_br_matematica_9_pesquisa_amostral", 93904, "s1_pop_amostra", "s2_vies", "s3_tipos", "s5_estimar")
p_estrat, p_plan = use("gen_br_matematica_8_pesquisa_amostral", 93905, "s2_estrat", "s3_planejar")


def s1_margem():
    k = R.choice(["intervalo", "empate", "empate", "tamanho"])
    if k == "intervalo":
        p = R.randint(20, 60)
        m = R.choice([2, 3, 4])
        return M("Uma pesquisa indica que %d%% dos eleitores aprovam um projeto, com margem de erro de %d pontos percentuais. Entre quais valores deve estar a aprovação real?" % (p, m), "entre %d%% e %d%%" % (p - m, p + m), ["exatamente %d%%" % p, "entre %d%% e %d%%" % (p, p + m), "entre %d%% e %d%%" % (p - 2 * m, p + 2 * m)],
                 "%d ± %d: <b>entre %d%% e %d%%</b>." % (p, m, p - m, p + m))
    if k == "empate":
        a = R.randint(30, 45)
        m = R.choice([2, 3])
        dif = R.choice([1, 2, 3, 4, 5, 6, 7, 8])
        b = a - dif
        emp = dif <= 2 * m
        ans = "empate técnico" if emp else "o candidato A está à frente"
        return M("Numa pesquisa, o candidato A tem %d%% e o B tem %d%%, com margem de erro de %d pontos para mais ou para menos. O que se pode concluir?" % (a, b, m), ans, ["o candidato A está à frente" if emp else "empate técnico", "o candidato B está à frente", "A vence com certeza"],
                 "Intervalos: A de %d%% a %d%% e B de %d%% a %d%%. %s" % (a - m, a + m, b - m, b + m, "Eles se sobrepõem: <b>empate técnico</b>." if emp else "Não se sobrepõem: <b>A à frente</b>."))
    return M("Mantendo o mesmo método de sorteio, aumentar bastante o tamanho da amostra costuma…", "diminuir a margem de erro", ["aumentar a margem de erro", "não mudar nada", "tornar a pesquisa um censo"], "Amostras maiores e aleatórias dão estimativas mais precisas: <b>margem de erro menor</b>.") if R.random() < 0.5 else \
        M("Uma amostra de 2.000 pessoas, sorteadas em todo o país, e outra de 20.000 pessoas que responderam a uma enquete num site. Qual tende a representar melhor a população?", "a de 2.000 pessoas sorteadas", ["a de 20.000 pessoas do site", "as duas igualmente", "nenhuma das duas"], "Sorteio evita o viés; tamanho grande não corrige uma amostra viciada: <b>a de 2.000 sorteadas</b>.")


s2_relatorio = bank(R, [
    ("Para mostrar a evolução mensal das vendas no relatório, o gráfico mais adequado é o de…", "linhas", ["setores", "pictograma", "histograma"]),
    ("Para mostrar a distribuição das alturas da amostra em intervalos, use…", "um histograma", ["um gráfico de setores", "um gráfico de linhas", "um pictograma"]),
    ("Na pesquisa, «idade», «renda» e «altura» são variáveis…", "quantitativas", ["qualitativas", "nominais", "categóricas"]),
    ("Na pesquisa, «cor preferida» e «time do coração» são variáveis…", "qualitativas", ["quantitativas contínuas", "quantitativas discretas", "numéricas"]),
    ("Se os salários da amostra têm alguns valores muito altos, o relatório deve destacar…", "a mediana", ["só a média", "só o maior valor", "a soma"]),
    ("Para mostrar se as notas estão concentradas ou espalhadas, o relatório deve incluir…", "uma medida de dispersão, como o desvio padrão", ["só a moda", "só o número de alunos", "só o nome da escola"]),
    ("Um relatório honesto de pesquisa amostral informa…", "o tamanho da amostra, como foi escolhida e a margem de erro", ["só os resultados que confirmam a ideia", "o nome dos entrevistados", "nada sobre a amostra"]),
    ("Número de irmãos é uma variável quantitativa…", "discreta", ["contínua", "qualitativa", "nominal"]),
], "s2_relatorio")


def main():
    seen = set()
    sets = [
        ("População, amostra e viés", mix(R, seen, [(p_pop, 10), (p_vies, 8), (s1_margem, 2)])),
        ("Tipos de amostragem", mix(R, seen, [(p_tipos, 12), (p_estrat, 8)])),
        ("Margem de erro e estimativas", mix(R, seen, [(s1_margem, 10), (p_est9, 10)])),
        ("Planejar a pesquisa", mix(R, seen, [(p_plan, 9), (p_estrat, 6), (s1_margem, 5)])),
        ("Relatório: medidas e gráficos", mix(R, seen, [(s2_relatorio, 8), (p_est9, 6), (p_tipos, 6)])),
    ]
    body = lesson(
        ["Planeje: <b>objetivo</b> → <b>população</b> → <b>amostra</b> (tamanho e forma de sorteio) → variáveis e perguntas → coleta → tabelas, gráficos e medidas → relatório.",
         "Escolha a amostra por <b>sorteio</b> (casual simples, sistemática ou estratificada). Amostras por conveniência ou voluntárias são <b>viciadas</b>.",
         "O resultado de uma amostra é uma <b>estimativa</b>: vem com uma <b>margem de erro</b>. 40% ± 3 significa entre 37% e 43%.",
         "Se os intervalos de dois candidatos se sobrepõem, há <b>empate técnico</b>."],
        [("A: 38%, B: 34%, margem de 3 pontos", ["A: 35% a 41%", "B: 31% a 37%", "intervalos se sobrepõem"], "empate técnico")],
        [["Tratar a estimativa como exata", "Sempre considere a margem de erro."],
         ["Achar que amostra grande corrige viés", "Uma enquete de site com muita gente continua viciada."],
         ["Escolher quem é mais fácil de ouvir", "Sorteie."]])
    faq = [("O que é empate técnico numa pesquisa?", "É quando a diferença entre dois candidatos é menor que a soma das margens de erro, ou seja, os intervalos de cada um se sobrepõem. Não dá para dizer quem está à frente."),
           ("O que a BNCC pede?", "Planejar e executar pesquisa amostral sobre questões relevantes, usando dados coletados diretamente ou em diferentes fontes, e comunicar os resultados por meio de relatório contendo gráficos e interpretação das medidas de tendência central e das medidas de dispersão (amplitude e desvio padrão), utilizando ou não recursos tecnológicos (EM13MAT202).")]
    unit(R, "pesquisa-amostral-e-relatorio", "E", ["EM13MAT202"],
         "Planejar e executar pesquisa amostral sobre questões relevantes, usando dados coletados diretamente ou em diferentes fontes, e comunicar os resultados por meio de relatório contendo gráficos e interpretação das medidas de tendência central e das medidas de dispersão (amplitude e desvio padrão), utilizando ou não recursos tecnológicos",
         "Pesquisa amostral, margem de erro e relatório", "Pesquisa amostral",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre pesquisa amostral: população e amostra, viés, tipos de amostragem, margem de erro, empate técnico, estimativas e relatório. 100 exercícios com gabarito.",
         "Estimativa ± margem de erro", "Sorteie a amostra para evitar viés.",
         body, faq, sets, 6, grade="3-serie")


if __name__ == "__main__":
    main()
