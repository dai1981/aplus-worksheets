# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Pesquisa e organização de dados (Probabilidade e estatística, EF02MA23)
  python3 tools/gen_br_matematica_2_pesquisa_e_organizacao_de_dados.py
Fazer uma pesquisa com até 30 pessoas; anotar respostas com tracinhos (grupos de 5); passar uma lista para a tabela;
escolher a pergunta da pesquisa; conferir o total; montar o gráfico de colunas a partir da tabela.
Usa geradores do 3º ano (tabelas e gráficos) com outro sorteio.
Erros: contar uma pessoa duas vezes, esquecer que o grupo cortado vale 5, achar que o total pode passar do número de pessoas.
"""
import random
import de_common
from br_common import mcq, lesson, make_unit, mix, use, lim, relabel, fig, grafico, pl, Kids

R = random.Random(80222)
K = Kids(R)
p_pesq, p_escolha = use("gen_br_matematica_3_tabelas_e_graficos", 80915, "s4_pesquisa", "s4_escolha", preds=(lim(30, 0),))
TEMAS = [("Fruta preferida", ["banana", "maçã", "uva", "manga"]), ("Cor preferida", ["azul", "verde", "vermelho", "amarelo"]),
         ("Animal de estimação", ["cachorro", "gato", "peixe", "pássaro"]), ("Brincadeira preferida", ["pega-pega", "esconde-esconde", "amarelinha", "pular corda"]),
         ("Sabor de suco", ["laranja", "uva", "maracujá", "caju"]), ("Esporte preferido", ["futebol", "vôlei", "natação", "basquete"])]


def tally(n):
    return fig(relabel(de_common.strichliste(n), "%s" % pl(n, "tracinho", "tracinhos")))


def s1_tracinhos():
    n = R.randint(3, 19)
    return mcq(tally(n) + "Cada tracinho é um voto e cada grupo cortado vale 5. Quantos votos há?", str(n), [str(n + 1), str(n - 1), str(n // 5 + n % 5)],
               "%s: <b>%d</b>." % (" e ".join(x for x in (pl(n // 5, "grupo de 5", "grupos de 5") if n >= 5 else "", pl(n % 5, "tracinho", "tracinhos") if n % 5 else "") if x), n))


def s1_registrar():
    n = R.randint(6, 18)
    g, r = divmod(n, 5)
    ok = "%s e %s" % (pl(g, "grupo de 5", "grupos de 5"), pl(r, "tracinho solto", "tracinhos soltos")) if r else pl(g, "grupo de 5", "grupos de 5")
    w = ["%s" % pl(n, "tracinho solto", "tracinhos soltos"), "%s e %s" % (pl(g + 1, "grupo de 5", "grupos de 5"), pl(r, "tracinho solto", "tracinhos soltos")) if r else pl(g + 1, "grupo de 5", "grupos de 5"),
         "%s e %s" % (pl(g, "grupo de 5", "grupos de 5"), pl(r + 1, "tracinho solto", "tracinhos soltos"))]
    return mcq("Uma fruta teve %d votos. Como anotar com tracinhos em grupos de 5?" % n, ok, w, "%d = %s: <b>%s</b>." % (n, " + ".join(["5"] * g + ([str(r)] if r else [])), ok))


def lista():
    tema, cats = R.choice(TEMAS)
    cats = cats[:3]
    n = R.randint(8, 12)
    ans = [R.choice(cats) for _ in range(n)]
    if len(set(ans)) < 3:
        return None
    names = []
    while len(names) < n:
        p, _ = K.next()
        if p not in names:
            names.append(p)
    return tema, cats, list(zip(names, ans))


def s2_lista():
    r = lista()
    if not r:
        return None
    tema, cats, rows = r
    c = R.choice(cats)
    cnt = sum(1 for _, a in rows if a == c)
    tb = "<p><b>Pesquisa: %s</b></p>" % tema + "<table class='sn-table' style='width:auto'><thead><tr><th>Criança</th><th>Resposta</th></tr></thead><tbody>%s</tbody></table>" % "".join(
        "<tr><td>%s</td><td>%s</td></tr>" % (p, a) for p, a in rows)
    return mcq(tb + "Quantas crianças responderam «%s»?" % c, str(cnt), [str(cnt + 1), str(len(rows)), str(cnt - 1) if cnt > 1 else str(cnt + 2)],
               "Procure «%s» na lista e conte: <b>%d</b>." % (c, cnt))


def s2_total():
    r = lista()
    if not r:
        return None
    tema, cats, rows = r
    vals = [sum(1 for _, a in rows if a == c) for c in cats]
    tb = "<p><b>Pesquisa: %s</b></p>" % tema + "<table class='sn-table' style='width:auto'><thead><tr><th>Resposta</th><th>Votos</th></tr></thead><tbody>%s</tbody></table>" % "".join(
        "<tr><td>%s</td><td>%d</td></tr>" % (c, v) for c, v in zip(cats, vals))
    tot = sum(vals)
    return mcq(tb + "Cada criança votou uma vez. Quantas crianças participaram da pesquisa?", str(tot), [str(tot + 1), str(len(cats)), str(max(vals))],
               "%s = <b>%d crianças</b>." % (" + ".join(map(str, vals)), tot))


def s3_grafico():
    tema, cats = R.choice(TEMAS)
    cats = cats[:3]
    vals = R.sample(range(2, 10), 3)
    i = R.randrange(3)
    tab = "<p>Na tabela da pesquisa «%s»: %s.</p>" % (tema, "; ".join("%s: %d" % (c, v) for c, v in zip(cats, vals)))
    k = R.choice(["falta", "falta", "alta", "baixa"])
    if k == "falta":
        pic = grafico([(c, 0 if j == i else v) for j, (c, v) in enumerate(zip(cats, vals))], "votos")
        return mcq(tab + pic + "A coluna «%s» ainda não foi desenhada. Até que número ela deve chegar?" % cats[i],
                   str(vals[i]), [str(vals[(i + 1) % 3]), str(vals[i] + 1), str(sum(vals))], "Na tabela, «%s» tem %d votos: a coluna chega ao <b>%d</b>." % (cats[i], vals[i], vals[i]))
    j = vals.index(max(vals) if k == "alta" else min(vals))
    return mcq(tab + "Ao fazer o gráfico de colunas dessa tabela, qual coluna ficará %s?" % ("mais alta" if k == "alta" else "mais baixa"), cats[j],
               [c for c in cats if c != cats[j]] + ["todas da mesma altura"], "A resposta com %s votos tem a coluna %s: <b>%s</b>." % ("mais" if k == "alta" else "menos", "mais alta" if k == "alta" else "mais baixa", cats[j]))


PERG = [("Para saber o sabor de sorvete preferido da turma, a melhor pergunta é…", "«Qual é o seu sabor de sorvete preferido?»", ["«Você gosta de sorvete?»", "«Quantos anos você tem?»", "«Qual é o seu nome?»"]),
        ("Numa pesquisa, cada criança pode votar…", "uma vez", ["quantas vezes quiser", "nenhuma vez", "duas vezes sempre"]),
        ("A turma tem 25 crianças e todas votaram uma vez. A soma de todos os votos dá…", "25", ["50", "30", "20"]),
        ("Uma pesquisa deu: futebol 12, vôlei 8, natação 5. Qual frase está certa?", "o futebol foi o mais votado", ["a natação foi a mais votada", "todos tiveram os mesmos votos", "o vôlei teve mais que o futebol"]),
        ("Antes de começar uma pesquisa, é preciso escolher…", "a pergunta e as respostas possíveis", ["a cor do gráfico", "só o título", "o maior número"]),
        ("Depois de anotar os votos, para organizar melhor os dados usamos…", "uma tabela ou um gráfico", ["uma régua", "um relógio", "uma balança"]),
        ("Numa turma de 30 alunos, uma resposta pode ter 35 votos?", "não, cada aluno vota uma vez só", ["sim, sempre", "sim, se for a preferida", "só no gráfico"]),
        ("Para anotar os votos rapidamente, podemos usar…", "tracinhos em grupos de 5", ["só números grandes", "desenhos de cada pessoa", "uma régua"])]


def s4_pergunta():
    q, a, w = R.choice(PERG)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Contar tracinhos", mix(R, seen, [(s1_tracinhos, 12), (s1_registrar, 8)])),
        ("Da lista para a tabela", mix(R, seen, [(s2_lista, 14), (s2_total, 6)])),
        ("Contagem da pesquisa", mix(R, seen, [(p_pesq, 14), (s2_total, 6)])),
        ("Da tabela para o gráfico", mix(R, seen, [(s3_grafico, 20)])),
        ("Planejar a pesquisa", mix(R, seen, [(s4_pergunta, 8), (p_escolha, 4), (s2_lista, 8)])),
    ]
    body = lesson(
        ["Para fazer uma <b>pesquisa</b>, escolha uma pergunta e as respostas possíveis (até 3 ou 4).",
         "Pergunte a cada pessoa uma vez e anote com <b>tracinhos</b>. Cada grupo de 5 tem 4 tracinhos e 1 cortando.",
         "Conte os tracinhos e escreva os números numa <b>tabela</b>. A soma deve dar o número de pessoas.",
         "Com a tabela, faça o <b>gráfico de colunas</b>: cada coluna chega até o número de votos."],
        [("2 grupos de 5 e 3 tracinhos", ["5 + 5 + 3"], "13 votos"),
         ("Banana 6, maçã 4, uva 5", ["6 + 4 + 5"], "15 crianças participaram")],
        [["Contar uma pessoa duas vezes", "Risque o nome de quem já respondeu."],
         ["Esquecer que o grupo cortado vale 5", "Conte de 5 em 5 e depois os soltos."],
         ["Achar que o total pode passar do número de pessoas", "Cada pessoa vota uma vez só."]],
        tally(13))
    faq = [("O que o 2º ano aprende sobre pesquisas?", "A BNCC pede realizar pesquisas com até 30 pessoas, escolhendo até três variáveis categóricas, e organizar os dados em listas, tabelas e gráficos de colunas simples."),
           ("Como fazer uma pesquisa com a criança?", "Pergunte à família qual é a fruta preferida de cada um, anote com tracinhos, monte uma tabela e desenhe um gráfico de colunas.")]
    make_unit(R, "pesquisa-e-organizacao-de-dados", "E", ["EF02MA23"],
              "Realizar pesquisa em universo de até 30 elementos, escolhendo até três variáveis categóricas de seu interesse, organizando os dados coletados em listas, tabelas e gráficos de colunas simples",
              "Pesquisa e organização de dados", "Pesquisa e dados",
              "Atividades de matemática para o 2º ano sobre pesquisa e organização de dados: tracinhos em grupos de 5, listas, tabelas, total de votos e gráficos de colunas. 100 exercícios com gabarito.",
              "Cada pessoa vota uma vez.", "Grupo de tracinhos cortado vale 5.",
              body, faq, sets, 22, grade="2-ano")


if __name__ == "__main__":
    main()
