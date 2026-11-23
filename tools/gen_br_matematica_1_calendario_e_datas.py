# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Calendário e datas (Grandezas e medidas, EF01MA17, EF01MA18)
  python3 tools/gen_br_matematica_1_calendario_e_datas.py
Dias da semana e meses do ano em ordem; ler o calendário; escrever datas por extenso e com números (dia/mês/ano);
datas comemorativas. Usa geradores do 2º ano (calendário) com outro sorteio.
Erros: escrever o mês antes do dia, achar que todo mês tem 30 dias, esquecer que depois de sábado vem domingo.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use
from br_2 import MESES, DIAS_MES, mes_svg

R = random.Random(80116)
M2 = "gen_br_matematica_2_calendario"
c_dias, c_meses, c_ler, c_sem = use(M2, 80983, "s1_dias", "s1_meses", "s2_ler", "s4_semanas")
ANO = 2027


def curta(d, m, a=ANO):
    return "%02d/%02d/%d" % (d, m, a)


def s3_escrever():
    m = R.randint(1, 12)
    d = R.randint(1, DIAS_MES[m - 1])
    if d == m:
        return None
    if R.random() < 0.5:
        return mcq("Como se escreve <b>%d de %s de %d</b> só com números?" % (d, MESES[m - 1], ANO), curta(d, m),
                   [curta(m, d) if d <= 12 else "%02d/%02d/%d" % (m, d, ANO), curta(d, m % 12 + 1), "%02d/%02d/%d" % (d, m, ANO - 1)],
                   "Primeiro o dia, depois o mês (%s é o mês %d) e o ano: <b>%s</b>." % (MESES[m - 1], m, curta(d, m)))
    ok = "%d de %s de %d" % (d, MESES[m - 1], ANO)
    return mcq("Que data está escrita em <b>%s</b>?" % curta(d, m), ok,
               ["%d de %s de %d" % (m, MESES[d - 1], ANO) if d <= 12 else "%d de %s de %d" % (d, MESES[m % 12], ANO), "%d de %s de %d" % (d, MESES[m - 2], ANO), "%d de %s de %d" % (d, MESES[m - 1], ANO + 1)],
               "Dia %d, mês %d (%s): <b>%s</b>." % (d, m, MESES[m - 1], ok))


FESTAS = [("o Natal", 25, 12), ("o Dia das Crianças", 12, 10), ("o Dia da Independência", 7, 9), ("o Ano-Novo", 1, 1), ("o Dia do Índio, hoje Dia dos Povos Indígenas", 19, 4)]


def s3_festa():
    n, d, m = R.choice(FESTAS)
    if R.random() < 0.5:
        return mcq("Em que mês é %s (dia %d)?" % (n, d), MESES[m - 1], [MESES[m % 12], MESES[m - 2], MESES[(m + 5) % 12]], "%s é em <b>%s</b>." % (n[0].upper() + n[1:], MESES[m - 1]))
    return mcq("%s é no dia %d de %s. Como se escreve essa data com números (dia/mês)?" % (n[0].upper() + n[1:], d, MESES[m - 1]), "%02d/%02d" % (d, m),
               ["%02d/%02d" % (m, d), "%02d/%02d" % (d, m % 12 + 1), "%02d/%02d" % (d + 1, m)], "Dia primeiro, depois o mês: <b>%02d/%02d</b>." % (d, m))


def s4_marcado():
    m = R.randint(1, 12)
    d = R.randint(1, DIAS_MES[m - 1])
    ok = "%d de %s" % (d, MESES[m - 1])
    return mcq(mes_svg(ANO, m, marks=(d,)) + "Que data está marcada com um círculo?", ok, ["%d de %s" % (d, MESES[m % 12]), "%d de %s" % (d + 1 if d < DIAS_MES[m - 1] else d - 1, MESES[m - 1]), "%d de %s" % (m, MESES[d - 1]) if d <= 12 and d != m else "%d de %s" % (d, MESES[m - 2])],
               "O título diz o mês (%s) e o círculo marca o dia %d: <b>%s</b>." % (MESES[m - 1], d, ok))


def main():
    seen = set()
    sets = [
        ("Dias da semana", mix(R, seen, [(c_dias, 16), (c_sem, 4)])),
        ("Meses do ano", mix(R, seen, [(c_meses, 18), (c_sem, 2)])),
        ("Ler o calendário", mix(R, seen, [(c_ler, 12), (s4_marcado, 8)])),
        ("Escrever datas", mix(R, seen, [(s3_escrever, 20)])),
        ("Datas especiais", mix(R, seen, [(s3_festa, 8), (s4_marcado, 6), (s3_escrever, 6)])),
    ]
    body = lesson(
        ["A semana tem <b>7 dias</b>: domingo, segunda, terça, quarta, quinta, sexta e sábado.",
         "O ano tem <b>12 meses</b>: janeiro, fevereiro, março… até dezembro.",
         "Para escrever a data, primeiro o <b>dia</b>, depois o <b>mês</b> e o <b>ano</b>: 5 de março de 2027 = 05/03/2027.",
         "No calendário, cada coluna é um dia da semana e o título diz o mês."],
        [("12 de outubro de 2027", ["dia 12, mês 10"], "12/10/2027"),
         ("Depois de sábado vem…", ["a semana recomeça"], "domingo")],
        [["Escrever o mês antes do dia (10/12 para 12 de outubro)", "No Brasil, o dia vem primeiro: 12/10."],
         ["Achar que todo mês tem 30 dias", "Alguns têm 31; fevereiro tem 28 ou 29."],
         ["Esquecer que depois de sábado vem domingo", "A semana recomeça no domingo."]],
        mes_svg(ANO, 3, marks=(5,)))
    faq = [("O que o 1º ano aprende sobre o calendário?", "A BNCC pede reconhecer e relacionar períodos do dia, dias da semana e meses do ano usando o calendário, e escrever a data com o dia, o mês e o ano."),
           ("Como praticar em casa?", "Escreva a data do dia junto com a criança, de manhã, e marque no calendário os aniversários da família.")]
    make_unit(R, "calendario-e-datas", "M", ["EF01MA17", "EF01MA18"],
              "Reconhecer e relacionar períodos do dia, dias da semana e meses do ano, utilizando calendário, quando necessário; produzir a escrita de uma data, apresentando o dia, o mês e o ano, e indicar o dia da semana de uma data, consultando calendários",
              "Calendário e datas: dias da semana e meses do ano", "Calendário e datas",
              "Atividades de matemática para o 1º ano sobre o calendário: dias da semana, meses do ano, ler o calendário e escrever datas com dia, mês e ano. 100 exercícios com gabarito.",
              "A semana tem 7 dias; o ano tem 12 meses.", "Na data, o dia vem primeiro: 05/03/2027.",
              body, faq, sets, 16, grade="1-ano")


if __name__ == "__main__":
    main()
