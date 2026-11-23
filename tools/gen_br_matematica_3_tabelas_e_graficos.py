# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Tabelas e gráficos (Probabilidade e estatística, EF03MA26, EF03MA27, EF03MA28)
  python3 tools/gen_br_matematica_3_tabelas_e_graficos.py
Ler tabelas simples e de dupla entrada, gráficos de colunas; maior e menor, quanto a mais, total; organizar os dados de
uma pesquisa (contagem com tracinhos) em tabela e gráfico; escolher o gráfico certo; problemas.
Erros: ler a coluna errada na tabela de dupla entrada, ler a altura da coluna sem olhar a escala, somar só uma linha.
"""
import random
from br_common import mcq as _mcq, lesson, make_unit, mix, table, grafico, num, pl

R = random.Random(80321)


def mcq(q, a, w, e):
    return _mcq(q.replace("Quantos crianças", "Quantas crianças"), a, w, e)
TEMAS = [("Fruta preferida da turma", "fruta", ["maçã", "banana", "uva", "laranja", "manga"], "crianças"),
         ("Esporte preferido", "esporte", ["futebol", "vôlei", "natação", "basquete", "judô"], "alunos"),
         ("Animal de estimação", "animal", ["cachorro", "gato", "peixe", "pássaro", "coelho"], "crianças"),
         ("Sabor de sorvete mais vendido", "sabor", ["chocolate", "morango", "creme", "flocos", "limão"], "sorvetes"),
         ("Livros emprestados na biblioteca", "dia", ["segunda", "terça", "quarta", "quinta", "sexta"], "livros"),
         ("Cor preferida", "cor", ["azul", "verde", "vermelho", "amarelo", "roxo"], "crianças"),
         ("Meio de transporte para a escola", "transporte", ["a pé", "ônibus", "carro", "bicicleta", "van"], "alunos")]


def dados(lo=2, hi=15, n=None, gente=False):
    t, k, cats, u = R.choice([x for x in TEMAS if not gente or x[3] in ("crianças", "alunos")])
    n = n or R.randint(3, 5)
    cats = cats[:n]
    while True:
        vals = [R.randint(lo, hi) for _ in cats]
        if len(set(vals)) == len(vals):
            return t, k, cats, vals, u


def tab(t, k, cats, vals, u):
    return "<p><b>%s</b></p>" % t + table([k.capitalize(), "Quantidade de %s" % u], [[c, num(v)] for c, v in zip(cats, vals)])


def pergunta(cats, vals, u, kind, k="item"):
    i, j = R.sample(range(len(cats)), 2)
    if kind == "max":
        m = max(vals)
        return ("Qual %s teve mais votos?" % k if u in ("crianças", "alunos") else "Qual teve o maior número?"), cats[vals.index(m)], [c for c in cats if c != cats[vals.index(m)]] + ["todos têm o mesmo número"], \
            "O maior número é %d: <b>%s</b>." % (m, cats[vals.index(m)])
    if kind == "min":
        m = min(vals)
        return "Qual teve o menor número?", cats[vals.index(m)], [c for c in cats if c != cats[vals.index(m)]] + ["todos têm o mesmo número"], "O menor número é %d: <b>%s</b>." % (m, cats[vals.index(m)])
    if kind == "dif":
        a, b = max(vals[i], vals[j]), min(vals[i], vals[j])
        ca = cats[i] if vals[i] > vals[j] else cats[j]
        cb = cats[j] if ca == cats[i] else cats[i]
        return ("Quantos %s a mais escolheram «%s» do que «%s»?" if u in ("crianças", "alunos") else "Quantos %s a mais em «%s» do que em «%s»?") % (u, ca, cb), str(a - b), [str(a + b), str(a), str(a - b + 1)], "%d − %d = <b>%d</b>." % (a, b, a - b)
    if kind == "tot":
        s = sum(vals)
        return "Quantos %s ao todo?" % u, str(s), [str(s + 1), str(s - max(vals)), str(len(vals))], "%s = <b>%d</b>." % (" + ".join(str(v) for v in vals), s)
    c = cats[i]
    return ("Quantos %s escolheram «%s»?" if u in ("crianças", "alunos") else "Quantos %s em «%s»?") % (u, c), str(vals[i]), [str(v) for v in vals if v != vals[i]] + [str(vals[i] + 1)], "Na linha de «%s» está <b>%d</b>." % (c, vals[i])


def s1_tabela():
    t, k, cats, vals, u = dados()
    q, a, w, e = pergunta(cats, vals, u, R.choice(["max", "min", "dif", "tot", "um"]), k)
    return mcq(tab(t, k, cats, vals, u) + q, a, w, e)


def s2_grafico():
    step = R.choice([1, 2, 5])
    t, k, cats, vals, u = dados(1, 10)
    vals = [v * step for v in vals]
    q, a, w, e = pergunta(cats, vals, u, R.choice(["max", "min", "dif", "tot", "um", "um"]), k)
    return mcq("<p><b>%s</b></p>" % t + grafico(list(zip(cats, vals)), u, step) + q, a, w,
               e + (" Atenção: cada linha do gráfico vale %d." % step if step > 1 else ""))


GRID = [("Alunos que almoçam na escola", ["1º ano", "2º ano", "3º ano"], ["meninas", "meninos"]),
        ("Livros lidos no mês", ["março", "abril", "maio"], ["turma A", "turma B"]),
        ("Ingressos vendidos para a festa junina", ["sábado", "domingo"], ["adultos", "crianças"]),
        ("Pontos no campeonato", ["1º jogo", "2º jogo", "3º jogo"], ["Azul", "Verde"])]


def s3_dupla():
    t, rows, cols = R.choice(GRID)
    v = [[R.randint(5, 30) for _ in cols] for _ in rows]
    tb = "<p><b>%s</b></p>" % t + table([""] + cols, [[r] + [str(x) for x in vv] for r, vv in zip(rows, v)])
    k = R.choice(["cel", "linha", "coluna", "dif"])
    i, j = R.randrange(len(rows)), R.randrange(len(cols))
    if k == "cel":
        a = v[i][j]
        other = v[i][1 - j]
        return mcq(tb + "Quanto é «%s» em «%s»?" % (cols[j], rows[i]), str(a), [str(other), str(v[(i + 1) % len(rows)][j]), str(a + other)],
                   "Procure a linha «%s» e a coluna «%s»: <b>%d</b>." % (rows[i], cols[j], a))
    if k == "linha":
        s = sum(v[i])
        return mcq(tb + "Qual é o total de «%s»?" % rows[i], str(s), [str(v[i][0]), str(sum(r[0] for r in v)), str(s + 10)],
                   "Some a linha «%s»: %s = <b>%d</b>." % (rows[i], " + ".join(str(x) for x in v[i]), s))
    if k == "coluna":
        s = sum(r[j] for r in v)
        return mcq(tb + "Qual é o total de «%s»?" % cols[j], str(s), [str(sum(v[0])), str(s - v[0][j]), str(s + 5)],
                   "Some a coluna «%s»: %s = <b>%d</b>." % (cols[j], " + ".join(str(r[j]) for r in v), s))
    a, b = v[i][0], v[i][1]
    if a == b:
        return None
    return mcq(tb + "Em «%s», quantos «%s» a mais que «%s»?" % (rows[i], cols[0] if a > b else cols[1], cols[1] if a > b else cols[0]), str(abs(a - b)),
               [str(a + b), str(max(a, b)), str(abs(a - b) + 2)], "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))


def tracos(n):
    return " ".join(["||||" + "/"] * (n // 5) + ["|" * (n % 5)] if n % 5 else ["||||" + "/"] * (n // 5))


def s4_pesquisa():
    t, k, cats, vals, u = dados(3, 14, 3, gente=True)
    i = R.randrange(3)
    tb = "<p><b>Pesquisa: %s</b></p>" % t + table([k.capitalize(), "Contagem"], [[c, "<span style='font-family:monospace;letter-spacing:1px'>%s</span>" % tracos(v)] for c, v in zip(cats, vals)])
    return mcq(tb + "Cada tracinho é um voto e cada grupo cortado vale 5. Quantos votos teve «%s»?" % cats[i], str(vals[i]),
               [str(vals[i] + 1), str(vals[i] - 1), str(vals[i] // 5 + vals[i] % 5)],
               "%s: <b>%d</b>." % (" e ".join(x for x in (pl(vals[i] // 5, "grupo de 5", "grupos de 5") if vals[i] >= 5 else "", pl(vals[i] % 5, "tracinho", "tracinhos") if vals[i] % 5 else "") if x), vals[i]))


ESCOLHA = [("Para mostrar quantos alunos preferem cada fruta, o melhor é…", "um gráfico de colunas", ["uma lista de nomes", "um relógio", "uma régua"]),
           ("Num gráfico de colunas, a coluna mais alta mostra…", "a maior quantidade", ["a menor quantidade", "o primeiro item", "o último item"]),
           ("Numa tabela de dupla entrada, para achar um número, olhamos…", "a linha e a coluna", ["só a primeira linha", "só o título", "só o total"]),
           ("Numa pesquisa com 30 alunos, cada aluno votou uma vez. Quanto dá a soma de todos os votos?", "30", ["1", "15", "60"]),
           ("O título de uma tabela serve para…", "dizer do que trata a tabela", ["mostrar o maior número", "contar os votos", "enfeitar"]),
           ("Num gráfico, cada linha da escala vale 2. Uma coluna chega à 4ª linha. Quanto ela vale?", "8", ["4", "6", "2"])]


def s4_escolha():
    q, a, w = R.choice(ESCOLHA)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def s5_problema():
    t, k, cats, vals, u = dados(4, 20, 4)
    kind = R.choice(["metade", "juntos", "faltam", "dobro"])
    i, j = R.sample(range(4), 2)
    tb = tab(t, k, cats, vals, u)
    if kind == "juntos":
        return mcq(tb + "Quantos %s há em «%s» e «%s» juntos?" % (u, cats[i], cats[j]), str(vals[i] + vals[j]), [str(abs(vals[i] - vals[j])), str(sum(vals)), str(vals[i] + vals[j] + 1)],
                   "%d + %d = <b>%d</b>." % (vals[i], vals[j], vals[i] + vals[j]))
    if kind == "faltam":
        alvo = (max(vals) // 10 + 1) * 10 + 10
        return mcq(tb + "Quantos %s faltam para «%s» chegar a %d?" % (u, cats[i], alvo), str(alvo - vals[i]), [str(alvo + vals[i]), str(vals[i]), str(alvo - vals[i] + 1)],
                   "%d − %d = <b>%d</b>." % (alvo, vals[i], alvo - vals[i]))
    if kind == "dobro":
        d = vals[i] * 2
        return mcq(tb + "Se «%s» tivesse o dobro do que tem, quanto teria?" % cats[i], str(d), [str(vals[i] + 2), str(vals[i] // 2), str(d + 1)],
                   "2 × %d = <b>%d</b>." % (vals[i], d))
    s = sum(vals)
    tot = s - vals[i]
    return mcq(tb + "Quantos %s NÃO escolheram «%s»?" % (u, cats[i]) if u in ("crianças", "alunos") else tb + "Tirando «%s», quanto há nos outros?" % cats[i], str(tot),
               [str(s), str(vals[i]), str(tot + 1)], "%d − %d = <b>%d</b>." % (s, vals[i], tot))


def main():
    seen = set()
    sets = [
        ("Ler tabelas simples", mix(R, seen, [(s1_tabela, 20)])),
        ("Ler gráficos de colunas", mix(R, seen, [(s2_grafico, 20)])),
        ("Tabelas de dupla entrada", mix(R, seen, [(s3_dupla, 20)])),
        ("Pesquisas e contagem", mix(R, seen, [(s4_pesquisa, 14), (s4_escolha, 6)])),
        ("Problemas com tabelas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Numa <b>tabela simples</b>, cada linha mostra um item e a sua quantidade. Leia sempre o título primeiro.",
         "Numa <b>tabela de dupla entrada</b>, o número fica no encontro de uma linha com uma coluna.",
         "Num <b>gráfico de colunas</b>, a altura da coluna mostra a quantidade. Olhe a escala: cada linha pode valer 1, 2, 5…",
         "Numa <b>pesquisa</b>, contamos os votos com tracinhos e depois organizamos os dados em tabela e gráfico."],
        [("Tabela: futebol 12, vôlei 7. Quantos a mais escolheram futebol?", ["12 − 7"], "5"),
         ("Coluna chega à 4ª linha; cada linha vale 5", ["4 × 5"], "20")],
        [["Ler a coluna errada", "Siga a linha com o dedo até encontrar a coluna certa."],
         ["Ignorar a escala do gráfico", "Veja quanto vale cada linha antes de ler."],
         ["Somar só uma linha para o total", "O total soma todas as linhas (ou todas as colunas)."]])
    faq = [("Que gráficos o 3º ano estuda?", "Tabelas simples, tabelas de dupla entrada e gráficos de barras ou de colunas. A BNCC também pede que a criança faça pesquisas com até 50 elementos e organize os dados."),
           ("Como fazer uma pesquisa com a criança?", "Escolha uma pergunta (fruta preferida da família, por exemplo), anote as respostas com tracinhos, monte uma tabela e desenhe um gráfico de colunas em papel quadriculado.")]
    make_unit(R, "tabelas-e-graficos", "E", ["EF03MA26", "EF03MA27", "EF03MA28"],
              "Resolver problemas cujos dados estão apresentados em tabelas de dupla entrada, gráficos de barras ou de colunas; ler, interpretar e comparar dados apresentados em tabelas de dupla entrada, gráficos de barras ou de colunas, envolvendo resultados de pesquisas significativas; realizar pesquisa envolvendo variáveis categóricas em um universo de até 50 elementos, organizar os dados coletados utilizando listas, tabelas simples ou de dupla entrada e representá-los em gráficos de colunas simples",
              "Tabelas e gráficos de colunas", "Tabelas e gráficos",
              "Atividades de matemática para o 3º ano sobre tabelas e gráficos: tabelas simples e de dupla entrada, gráficos de colunas, pesquisas com contagem de votos e problemas. 100 exercícios com gabarito.",
              "Leia o título, depois as linhas e as colunas.", "No gráfico, confira quanto vale cada linha.",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
