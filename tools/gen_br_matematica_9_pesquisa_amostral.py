# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Pesquisa amostral (Probabilidade e estatística, EF09MA23)
  python3 tools/gen_br_matematica_9_pesquisa_amostral.py
População e amostra; censo e pesquisa amostral; amostra representativa e viés; amostragem aleatória simples, sistemática
e estratificada; variáveis qualitativas e quantitativas; tabela de frequências (absoluta e relativa); estimar a população
a partir da amostra; etapas de uma pesquisa e relatório.
Erros: entrevistar só um grupo (amostra viciada), confundir população com amostra, achar que amostra grande sempre é boa.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, unit

R = random.Random(89022)


def s1_pop_amostra():
    pop, am, tema = R.choice([
        ("os 1.200 alunos da escola", "os 120 alunos sorteados", "o tempo que os alunos passam no celular"),
        ("os moradores de Fortaleza", "os 800 moradores entrevistados", "o meio de transporte usado"),
        ("as 5.000 lâmpadas fabricadas no dia", "as 50 lâmpadas testadas", "a duração das lâmpadas"),
        ("os eleitores de um estado", "os 2.000 eleitores ouvidos", "a intenção de voto"),
        ("os 600 funcionários de uma empresa", "os 60 funcionários escolhidos", "a satisfação no trabalho"),
        ("as famílias de um bairro", "as 150 famílias visitadas", "o gasto com energia elétrica"),
        ("os torcedores de um estádio", "os 300 torcedores entrevistados na saída", "a nota dada ao jogo"),
    ])
    k = R.choice(["pop", "am"])
    if k == "pop":
        return M("Numa pesquisa sobre %s, foram entrevistados %s, entre %s. Qual é a <b>população</b> da pesquisa?" % (tema, am, pop), pop, [am, tema, "só quem respondeu «sim»"],
                 "A população é o grupo todo que se quer estudar: <b>%s</b>." % pop)
    return M("Numa pesquisa sobre %s, foram entrevistados %s, entre %s. Qual é a <b>amostra</b>?" % (tema, am, pop), am, [pop, tema, "todos os habitantes do Brasil"],
             "A amostra é a parte da população que foi pesquisada: <b>%s</b>." % am)


def s2_vies():
    q, a, w = R.choice([
        ("Para saber o esporte preferido dos alunos da escola, Pedro entrevistou só os alunos do time de futebol. A amostra é boa?", "não, ela é viciada (favorece o futebol)", ["sim, porque são alunos da escola", "sim, se forem muitos alunos", "não, porque futebol não é esporte"]),
        ("Para saber quanto tempo as pessoas leem por semana, uma pesquisa foi feita só na porta de uma biblioteca. O resultado tende a…", "superestimar a leitura", ["subestimar a leitura", "ser exato", "não ter relação com a leitura"]),
        ("Para estimar a altura média dos alunos do 6º ao 9º ano, a melhor amostra é…", "alunos sorteados de todas as turmas", ["só os alunos do 9º ano", "só os alunos do time de basquete", "os 10 primeiros que chegarem"]),
        ("Uma pesquisa sobre o transporte usado pelos moradores de uma cidade foi feita só num ponto de ônibus. Qual é o problema?", "a amostra favorece quem anda de ônibus", ["a amostra é grande demais", "o ponto de ônibus é longe", "não há problema"]),
        ("Uma amostra é <b>representativa</b> quando…", "tem as mesmas características da população, em proporção", ["é formada só por voluntários", "tem pelo menos 1.000 pessoas", "é escolhida pelo pesquisador por amizade"]),
        ("Um site perguntou aos visitantes se gostam de jogos online. O resultado vale para toda a população?", "não, quem visita o site não representa todos", ["sim, porque é uma pesquisa", "sim, se responderem muitas pessoas", "não, porque jogos são proibidos"]),
        ("A pergunta «Você não acha que a escola deveria ter mais aulas de Matemática?» é…", "tendenciosa (induz a resposta)", ["neutra", "aberta", "impossível de responder"]),
        ("Para uma pesquisa ser confiável, a amostra deve ser…", "escolhida ao acaso e representativa", ["escolhida pelo pesquisador", "só de pessoas que concordam", "a menor possível"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def s3_tipos():
    k = R.choice(["tipo", "var", "sist", "estrat"])
    if k == "tipo":
        q, a, w = R.choice([
            ("Os nomes de todos os alunos vão para uma urna e se sorteiam 30. Que tipo de amostragem é essa?", "aleatória simples", ["sistemática", "estratificada", "por conveniência"]),
            ("Numa fila, entrevista-se uma pessoa a cada 10 que passam. Que tipo de amostragem é essa?", "sistemática", ["aleatória simples", "estratificada", "censo"]),
            ("A escola tem 60% de meninas e 40% de meninos; a amostra foi escolhida com 60% de meninas e 40% de meninos, por sorteio em cada grupo. Que tipo de amostragem é essa?", "estratificada", ["sistemática", "aleatória simples", "por conveniência"]),
            ("Entrevistar só os amigos mais próximos é uma amostragem…", "por conveniência (não é aleatória)", ["aleatória simples", "estratificada", "sistemática"]),
            ("Quando se pesquisa <b>toda</b> a população, a pesquisa se chama…", "censo", ["amostra", "sorteio", "estimativa"]),
            ("O IBGE visita todos os domicílios do país a cada 10 anos. Isso é um…", "censo", ["pesquisa amostral", "sorteio", "experimento aleatório"]),
        ])
        return M(q, a, w, "Resposta: <b>%s</b>." % a)
    if k == "var":
        v, a = R.choice([("cor dos olhos", "qualitativa"), ("número de irmãos", "quantitativa discreta"), ("altura em centímetros", "quantitativa contínua"),
                         ("time de futebol preferido", "qualitativa"), ("massa em quilogramas", "quantitativa contínua"), ("número de livros lidos no ano", "quantitativa discreta"),
                         ("meio de transporte para a escola", "qualitativa"), ("tempo de deslocamento em minutos", "quantitativa contínua"), ("número de pessoas na casa", "quantitativa discreta"),
                         ("estado onde nasceu", "qualitativa")])
        return M("A variável <b>%s</b> é…" % v, a, [x for x in ["qualitativa", "quantitativa discreta", "quantitativa contínua", "uma constante"] if x != a],
                 "Resposta: <b>%s</b>." % a)
    if k == "sist":
        N, n = R.choice([(500, 50), (1200, 60), (800, 40), (900, 30), (2000, 100), (600, 20)])
        return M("Numa lista de %s pessoas, queremos uma amostra sistemática de %d pessoas. De quantas em quantas pessoas da lista devemos escolher?" % (d(N), n), d(N // n), [d(n), d(N - n), d(N // n * 2)],
                 "%s ÷ %d = <b>%d</b>: escolhe-se uma pessoa a cada %d." % (d(N), n, N // n, N // n))
    tot = R.choice([40, 50, 60, 80, 100])
    a, b = R.choice([(60, 40), (70, 30), (55, 45), (65, 35), (75, 25)])
    return M("Numa escola, %d%% dos alunos estudam de manhã e %d%% à tarde. Numa amostra estratificada de %d alunos, quantos devem ser da manhã?" % (a, b, tot), d(tot * a // 100), [d(tot // 2), d(tot * b // 100), d(a)],
             "%d%% de %d = <b>%d</b>." % (a, tot, tot * a // 100))


def s4_frequencia():
    cats = R.sample(["futebol", "vôlei", "basquete", "natação", "handebol", "skate"], 4)
    tot = R.choice([20, 25, 40, 50])
    while True:
        cuts = sorted(R.sample(range(1, tot), 3))
        fs = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], tot - cuts[2]]
        if min(fs) >= 2 and len(set(fs)) == 4:
            break
    tb = "<table class='sn-table' style='width:auto'><tbody><tr><th>Esporte</th><th>Frequência</th></tr>%s</tbody></table>" % "".join("<tr><td>%s</td><td>%d</td></tr>" % (c, f) for c, f in zip(cats, fs))
    i = R.randrange(4)
    k = R.choice(["rel", "tot", "graus"])
    if k == "rel":
        p = F(fs[i] * 100, tot)
        return M(tb + "Numa amostra de %d alunos, qual é a frequência relativa de %s?" % (tot, cats[i]), "%s%%" % d(p), ["%d%%" % fs[i], "%s%%" % d(F(fs[i] * 100, 100)) if tot != 100 else "%d%%" % (fs[i] * 2), "%s%%" % d(F(100, 4))],
                 "%d ÷ %d = %s = <b>%s%%</b>." % (fs[i], tot, d(F(fs[i], tot)), d(p)))
    if k == "tot":
        return M(tb + "Quantos alunos foram entrevistados ao todo?", d(tot), [d(tot - fs[i]), d(max(fs)), d(4)], "%s = <b>%d</b>." % (" + ".join(map(str, fs)), tot))
    g = F(fs[i] * 360, tot)
    if (g * 10).denominator != 1:
        return None
    return M(tb + "Num gráfico de setores com estes %d alunos, quantos graus terá o setor de %s?" % (tot, cats[i]), "%s°" % d(g), ["%d°" % fs[i], "%s°" % d(F(fs[i] * 100, tot)), "%d°" % (360 // 4)],
             "%d/%d de 360° = <b>%s°</b>." % (fs[i], tot, d(g)))


def s5_estimar():
    k = R.choice(["prop", "peixes", "etapas"])
    if k == "prop":
        n, s = R.choice([(200, 50), (100, 30), (400, 120), (250, 75), (500, 160), (150, 45)])
        N = R.choice([2000, 3000, 5000, 10000, 1200])
        e = F(s * N, n)
        if e.denominator != 1:
            return None
        return M("Numa amostra aleatória de %d moradores, %d disseram usar bicicleta. O bairro tem %s moradores. Quantos devem usar bicicleta, aproximadamente?" % (n, s, d(N)), d(e), [d(s), d(F(N, n) + s), d(e * 2)],
                 "%d/%d = %s%%; %s%% de %s ≈ <b>%s</b>." % (s, n, d(F(s * 100, n)), d(F(s * 100, n)), d(N), d(e)))
    if k == "peixes":
        m, c, r = R.choice([(100, 50, 5), (60, 40, 4), (200, 100, 8), (80, 60, 6), (120, 50, 5)])
        N = m * c // r
        return M("Num lago, %d peixes foram marcados e soltos. Depois, numa captura de %d peixes, %d estavam marcados. Qual é a estimativa do total de peixes do lago?" % (m, c, r), d(N), [d(m + c), d(m * r), d(c * r)],
                 "%d/%d dos peixes estão marcados; %d ÷ (%d/%d) = <b>%d</b>." % (r, c, m, r, c, N))
    q, a, w = R.choice([
        ("Qual é a primeira etapa de uma pesquisa amostral?", "definir o objetivo e a população", ["fazer o gráfico", "escrever o relatório", "calcular a média"]),
        ("Depois de coletar os dados, a etapa seguinte é…", "organizar os dados em tabelas e gráficos", ["escolher a população", "escrever as perguntas", "sortear a amostra"]),
        ("No relatório final de uma pesquisa, deve aparecer…", "como a amostra foi escolhida e as conclusões", ["só o gráfico mais bonito", "só os dados que confirmam a hipótese", "o nome dos entrevistados"]),
        ("Antes de aplicar o questionário, é bom…", "testá-lo com poucas pessoas", ["publicar os resultados", "escolher as respostas", "excluir as perguntas fechadas"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("População e amostra", mix(R, seen, [(s1_pop_amostra, 14), (s3_tipos, 6)])),
        ("Amostras representativas e viés", mix(R, seen, [(s2_vies, 8), (s3_tipos, 12)])),
        ("Tipos de amostragem e variáveis", mix(R, seen, [(s3_tipos, 20)])),
        ("Tabelas de frequência", mix(R, seen, [(s4_frequencia, 20)])),
        ("Estimativas e etapas da pesquisa", mix(R, seen, [(s5_estimar, 20)])),
    ]
    body = lesson(
        ["A <b>população</b> é o grupo todo que se quer estudar; a <b>amostra</b> é a parte que é pesquisada. Pesquisar a população toda é um <b>censo</b>.",
         "Uma boa amostra é <b>aleatória</b> e <b>representativa</b>: tem as mesmas características da população. Se só um grupo é ouvido, a amostra é viciada.",
         "Tipos de amostragem: aleatória simples (sorteio), sistemática (um a cada k) e estratificada (sorteio dentro de cada grupo, na mesma proporção).",
         "Etapas: objetivo e população → plano da amostra → coleta → tabelas e gráficos → relatório com conclusões."],
        [("Amostra de 200 moradores, 50 usam bicicleta; bairro com 4.000 moradores", ["50/200 = 25%", "25% de 4.000"], "cerca de 1.000"),
         ("Lista de 1.200, amostra de 60", ["1.200 ÷ 60 = 20"], "uma pessoa a cada 20")],
        [["Ouvir só um grupo", "A amostra deve representar toda a população."],
         ["Confundir população com amostra", "A amostra é só a parte pesquisada."],
         ["Achar que amostra grande sempre é boa", "Uma amostra grande mas viciada também erra."]])
    faq = [("Qual é a diferença entre censo e pesquisa amostral?", "No censo, toda a população é pesquisada. Na pesquisa amostral, só uma parte (a amostra), que deve ser escolhida ao acaso e representar bem a população."),
           ("O que a BNCC pede no 9º ano?", "Planejar e executar pesquisa amostral envolvendo tema da realidade social e comunicar os resultados por meio de relatório contendo avaliação de medidas de tendência central e da amplitude, tabelas e gráficos adequados (EF09MA23).")]
    unit(R, "pesquisa-amostral", "E", ["EF09MA23"],
         "Planejar e executar pesquisa amostral envolvendo tema da realidade social e comunicar os resultados por meio de relatório contendo avaliação de medidas de tendência central e da amplitude, tabelas e gráficos adequados, construídos com o apoio de planilhas eletrônicas",
         "Pesquisa amostral: população, amostra e relatório", "Pesquisa amostral",
         "Atividades de matemática para o 9º ano sobre pesquisa amostral: população e amostra, censo, amostras representativas, tipos de amostragem, variáveis, tabelas de frequência e estimativas. 100 exercícios com gabarito.",
         "A amostra deve representar a população.", "Escolha ao acaso e em proporção.",
         body, faq, sets, 22)


if __name__ == "__main__":
    main()
