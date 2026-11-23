# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Tabelas e gráficos (Probabilidade e estatística, EF02MA22)
  python3 tools/gen_br_matematica_2_tabelas_e_graficos.py
Ler tabelas simples e de dupla entrada; ler gráficos de colunas; mais votado, menos votado, quantos a mais e total;
comparar informações de uma tabela e de um gráfico. Usa geradores do 3º ano (tabelas e gráficos) com outro sorteio.
Erros: ler a coluna errada, esquecer de olhar a escala do gráfico, somar quando a pergunta é «quantos a mais».
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim, grafico

R = random.Random(80221)
M3 = "gen_br_matematica_3_tabelas_e_graficos"
g_tab, g_graf, g_dupla, g_prob = use(M3, 80914, "s1_tabela", "s2_grafico", "s3_dupla", "s5_problema", preds=(lim(100, 0),))
FRUTAS = ["banana", "maçã", "uva", "manga", "laranja", "melancia", "caju", "goiaba"]


def s2_qual_grafico():
    cats = R.sample(FRUTAS, 3)
    vals = R.sample(range(2, 10), 3)
    data = list(zip(cats, vals))
    pic = grafico(data, "crianças")
    i = vals.index(max(vals))
    j = vals.index(min(vals))
    k = R.choice(["max", "min", "le", "dif"])
    if k == "max":
        return mcq(pic + "Qual fruta teve mais votos?", cats[i], [c for c in cats if c != cats[i]] + ["todas iguais"], "A coluna mais alta é a da fruta <b>%s</b>." % cats[i])
    if k == "min":
        return mcq(pic + "Qual fruta teve menos votos?", cats[j], [c for c in cats if c != cats[j]] + ["todas iguais"], "A coluna mais baixa é a da fruta <b>%s</b>." % cats[j])
    if k == "le":
        x = R.randrange(3)
        return mcq(pic + "Quantas crianças escolheram %s?" % cats[x], str(vals[x]), [str(vals[x] + 1), str(vals[x] - 1), str(sum(vals))], "Siga o topo da coluna até a escala: <b>%d</b>." % vals[x])
    return mcq(pic + "Quantos votos %s teve a mais que %s?" % (cats[i], cats[j]), str(vals[i] - vals[j]), [str(vals[i] + vals[j]), str(vals[i]), str(vals[i] - vals[j] + 1)],
               "%d − %d = <b>%d</b>." % (vals[i], vals[j], vals[i] - vals[j]))


def main():
    seen = set()
    sets = [
        ("Ler tabelas", mix(R, seen, [(g_tab, 20)])),
        ("Ler gráficos de colunas", mix(R, seen, [(g_graf, 12), (s2_qual_grafico, 8)])),
        ("Tabelas de dupla entrada", mix(R, seen, [(g_dupla, 20)])),
        ("Comparar informações", mix(R, seen, [(s2_qual_grafico, 12), (g_graf, 8)])),
        ("Problemas com tabelas", mix(R, seen, [(g_prob, 20)])),
    ]
    body = lesson(
        ["Uma <b>tabela</b> organiza os dados em linhas e colunas. Leia o título para saber do que ela trata.",
         "Numa <b>tabela de dupla entrada</b>, cruze a linha com a coluna para achar o número.",
         "No <b>gráfico de colunas</b>, a coluna mais alta mostra a maior quantidade. Leia o número na escala ao lado.",
         "Para saber quantos a mais, tire o menor do maior; para saber o total, some tudo."],
        [("Banana 8 votos, uva 5 votos", ["8 − 5"], "banana teve 3 votos a mais"),
         ("Gráfico: maçã chega no 6", ["siga o topo até a escala"], "6 votos")],
        [["Ler a coluna errada", "Ponha o dedo na linha e na coluna antes de ler."],
         ["Esquecer de olhar a escala", "Veja quanto vale cada linha da escala."],
         ["Somar quando pedem quantos a mais", "Quantos a mais: subtraia."]],
        grafico([("banana", 8), ("maçã", 6), ("uva", 5)], "crianças"))
    faq = [("Que tabelas e gráficos o 2º ano estuda?", "A BNCC pede comparar informações de pesquisas em tabelas de dupla entrada e em gráficos de colunas simples ou de barras, para entender melhor o que acontece no dia a dia."),
           ("Como ajudar a criança a ler um gráfico?", "Comece pelo título e pelos nomes embaixo das colunas. Depois pergunte qual coluna é a mais alta e o que isso quer dizer.")]
    make_unit(R, "tabelas-e-graficos", "E", ["EF02MA22"],
              "Comparar informações de pesquisas apresentadas por meio de tabelas de dupla entrada e em gráficos de colunas simples ou barras, para melhor compreender aspectos da realidade próxima",
              "Tabelas e gráficos de colunas", "Tabelas e gráficos",
              "Atividades de matemática para o 2º ano sobre tabelas e gráficos: tabelas simples e de dupla entrada, gráficos de colunas, mais votado, menos votado e quantos a mais. 100 exercícios com gabarito.",
              "A coluna mais alta mostra a maior quantidade.", "Na tabela de dupla entrada, cruze linha e coluna.",
              body, faq, sets, 21, grade="2-ano")


if __name__ == "__main__":
    main()
