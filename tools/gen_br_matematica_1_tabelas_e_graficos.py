# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Tabelas e gráficos (Probabilidade e estatística, EF01MA21)
  python3 tools/gen_br_matematica_1_tabelas_e_graficos.py
Ler tabelas simples e gráficos de colunas: o mais votado e o menos votado, quanto vale uma coluna, quantos a mais,
total; gráficos de figuras (cada figura vale 1). Usa geradores do 2º e do 3º ano com outro sorteio.
Erros: ler a linha errada da tabela, achar que a coluna mais baixa é a maior, somar quando pedem quantos a mais.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, use, lim, grafico, text
from ws_common import svg_wrap, GREEN
from br_1 import pic

R = random.Random(80119)
g_qual = use("gen_br_matematica_2_tabelas_e_graficos", 80986, "s2_qual_grafico")
g_tab, g_graf = use("gen_br_matematica_3_tabelas_e_graficos", 80987, "s1_tabela", "s2_grafico", preds=(lim(20, 0),))
FRUTAS = [("apple", "maçã"), ("star", "estrela"), ("ball", "bola"), ("flower", "flor"), ("fish", "peixe"), ("duck", "pato")]


def picto(rows):
    s = []
    for i, (k, nm, v) in enumerate(rows):
        y = 26 + i * 40
        s.append(text(8, y + 6, nm, 15, anchor="start"))
        for j in range(v):
            s.append(k_pics.obj(k, 110 + j * 32, y, 13))
    W = 120 + max(v for _, _, v in rows) * 32
    return pic(svg_wrap(W, 16 + len(rows) * 40, "".join(s), "x"), "gráfico de figuras: " + "; ".join("%s %d" % (nm, v) for _, nm, v in rows))


def s1_picto():
    rows = [(k, nm, R.randint(1, 8)) for k, nm in R.sample(FRUTAS, 3)]
    vals = [v for _, _, v in rows]
    if len(set(vals)) < 3:
        return None
    k = R.choice(["mais", "menos", "um", "dif"])
    if k == "mais":
        i = vals.index(max(vals))
        return mcq(picto(rows) + "Que figura aparece mais vezes?", rows[i][1], [r[1] for r in rows if r != rows[i]] + ["todas iguais"], "A fileira mais comprida: <b>%s</b>." % rows[i][1])
    if k == "menos":
        i = vals.index(min(vals))
        return mcq(picto(rows) + "Que figura aparece menos vezes?", rows[i][1], [r[1] for r in rows if r != rows[i]] + ["todas iguais"], "A fileira mais curta: <b>%s</b>." % rows[i][1])
    if k == "um":
        i = R.randrange(3)
        return mcq(picto(rows) + "Quantas vezes aparece %s?" % rows[i][1], str(vals[i]), [str(vals[i] + 1), str(vals[i] - 1) if vals[i] > 1 else str(vals[i] + 2), str(sum(vals))],
                   "Conte a fileira: <b>%d</b>." % vals[i])
    a, b = vals.index(max(vals)), vals.index(min(vals))
    return mcq(picto(rows) + "Quantas vezes %s aparece a mais que %s?" % (rows[a][1], rows[b][1]),
               str(vals[a] - vals[b]), [str(vals[a] + vals[b]), str(vals[a]), str(vals[a] - vals[b] + 1)], "%d − %d = <b>%d</b>." % (vals[a], vals[b], vals[a] - vals[b]))


def main():
    seen = set()
    sets = [
        ("Gráficos de figuras", mix(R, seen, [(s1_picto, 20)])),
        ("Ler tabelas", mix(R, seen, [(g_tab, 20)])),
        ("Gráficos de colunas", mix(R, seen, [(g_qual, 20)])),
        ("Mais gráficos de colunas", mix(R, seen, [(g_graf, 20)])),
        ("Revisão", mix(R, seen, [(s1_picto, 8), (g_qual, 6), (g_tab, 6)])),
    ]
    body = lesson(
        ["Uma <b>tabela</b> mostra os dados em linhas e colunas. Leia o título para saber do que se trata.",
         "Num <b>gráfico de colunas</b>, a coluna mais alta mostra o que teve mais votos.",
         "Para saber quanto vale uma coluna, siga o topo dela até os números ao lado.",
         "Para saber quantos a mais, tire o menor do maior."],
        [("Banana 7, uva 4", ["7 é maior"], "banana teve mais"),
         ("7 − 4", ["banana tem 3 a mais"], "3")],
        [["Ler a linha errada da tabela", "Ponha o dedo na linha antes de ler."],
         ["Achar que a coluna mais baixa é a maior", "A coluna mais alta mostra a maior quantidade."],
         ["Somar quando pedem quantos a mais", "Quantos a mais: subtraia."]],
        grafico([("banana", 7), ("uva", 4), ("maçã", 5)], "crianças"))
    faq = [("Que gráficos o 1º ano lê?", "A BNCC pede ler dados expressos em tabelas e em gráficos de colunas simples. Gráficos de figuras ajudam a começar."),
           ("Como ajudar a criança a ler um gráfico?", "Comece pelo título e pelos nomes embaixo das colunas. Pergunte qual coluna é a mais alta e o que isso quer dizer.")]
    make_unit(R, "tabelas-e-graficos", "E", ["EF01MA21"],
              "Ler dados expressos em tabelas e em gráficos de colunas simples",
              "Tabelas e gráficos de colunas", "Tabelas e gráficos",
              "Atividades de matemática para o 1º ano sobre tabelas e gráficos: gráficos de figuras, tabelas simples, gráficos de colunas, mais votado e quantos a mais. 100 exercícios com gabarito.",
              "A coluna mais alta mostra o mais votado.", "Leia o título e os nomes das colunas.",
              body, faq, sets, 19, grade="1-ano")


if __name__ == "__main__":
    main()
