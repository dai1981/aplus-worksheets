# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Calendário: dias, semanas e meses (Grandezas e medidas, EF02MA18)
  python3 tools/gen_br_matematica_2_calendario.py
Dias da semana e meses do ano em ordem; ontem, hoje e amanhã; ler a folha do calendário; em que dia da semana cai uma data;
quantos dias faltam ou passaram entre duas datas; semanas e agenda.
Erros: contar o dia de hoje junto ao calcular quantos dias faltam, achar que todo mês tem 30 dias, começar a semana no dia errado.
"""
import random
from br_common import mcq, lesson, make_unit, mix, Kids
from br_2 import DIAS, MESES, DIAS_MES, mes_svg, dia_semana

R = random.Random(80217)
K = Kids(R)
ANO = 2027
ORD = ["1º", "2º", "3º", "4º", "5º", "6º", "7º", "8º", "9º", "10º", "11º", "12º"]


def s1_dias():
    i = R.randrange(7)
    k = R.choice(["depois", "antes", "amanha", "ontem", "dois"])
    d = DIAS
    if k == "depois":
        return mcq("Que dia da semana vem logo depois de %s?" % d[i], d[(i + 1) % 7], [d[(i - 1) % 7], d[(i + 2) % 7], d[(i + 3) % 7]], "Depois de %s vem <b>%s</b>." % (d[i], d[(i + 1) % 7]))
    if k == "antes":
        return mcq("Que dia da semana vem logo antes de %s?" % d[i], d[(i - 1) % 7], [d[(i + 1) % 7], d[(i - 2) % 7], d[(i + 3) % 7]], "Antes de %s vem <b>%s</b>." % (d[i], d[(i - 1) % 7]))
    if k == "amanha":
        return mcq("Hoje é %s. Que dia será amanhã?" % d[i], d[(i + 1) % 7], [d[(i - 1) % 7], d[i], d[(i + 2) % 7]], "Amanhã é o dia seguinte: <b>%s</b>." % d[(i + 1) % 7])
    if k == "ontem":
        return mcq("Hoje é %s. Que dia foi ontem?" % d[i], d[(i - 1) % 7], [d[(i + 1) % 7], d[i], d[(i - 2) % 7]], "Ontem é o dia anterior: <b>%s</b>." % d[(i - 1) % 7])
    n = R.choice([2, 3])
    return mcq("Hoje é %s. Que dia da semana será daqui a %d dias?" % (d[i], n), d[(i + n) % 7], [d[(i + n - 1) % 7], d[(i + n + 1) % 7], d[(i - n) % 7]],
               "Conte %d dias para a frente: %s. Resposta: <b>%s</b>." % (n, ", ".join(d[(i + j) % 7] for j in range(1, n + 1)), d[(i + n) % 7]))


def s1_meses():
    i = R.randrange(12)
    k = R.choice(["depois", "antes", "ordem", "qual", "dias"])
    m = MESES
    if k == "depois":
        return mcq("Que mês vem logo depois de %s?" % m[i], m[(i + 1) % 12], [m[(i - 1) % 12], m[(i + 2) % 12], m[(i + 6) % 12]], "Depois de %s vem <b>%s</b>." % (m[i], m[(i + 1) % 12]))
    if k == "antes":
        return mcq("Que mês vem logo antes de %s?" % m[i], m[(i - 1) % 12], [m[(i + 1) % 12], m[(i - 2) % 12], m[(i + 6) % 12]], "Antes de %s vem <b>%s</b>." % (m[i], m[(i - 1) % 12]))
    if k == "ordem":
        return mcq("Qual é o %s mês do ano?" % ORD[i], m[i], [m[(i + 1) % 12], m[(i - 1) % 12], m[(i + 3) % 12]], "Janeiro é o 1º. O %s mês é <b>%s</b>." % (ORD[i], m[i]))
    if k == "qual":
        return mcq("%s é o mês número…" % m[i].capitalize(), str(i + 1), [str((i + 1) % 12 + 1), str(i if i else 12), str((i + 3) % 12 + 1)], "Contando a partir de janeiro, %s é o mês <b>%d</b>." % (m[i], i + 1))
    nd = DIAS_MES[i]
    return mcq("Quantos dias tem o mês de %s (num ano que não é bissexto)?" % m[i], str(nd), [str(x) for x in (28, 29, 30, 31) if x != nd],
               "%s tem <b>%d dias</b>. Dica: conte nos nós dos dedos — os nós têm 31 dias." % (m[i].capitalize(), nd))


def s2_ler():
    mes = R.randint(1, 12)
    nd = DIAS_MES[mes - 1]
    pic = mes_svg(ANO, mes)
    k = R.choice(["dia", "dia", "quantos", "primeiro", "ultimo"])
    if k == "dia":
        d = R.randint(2, nd - 1)
        ans = dia_semana(ANO, mes, d)
        i = DIAS.index(ans)
        return mcq(pic + "Em que dia da semana cai o dia %d?" % d, ans, [DIAS[(i + 1) % 7], DIAS[(i - 1) % 7], DIAS[(i + 3) % 7]],
                   "Procure o %d e suba até a letra da coluna: <b>%s</b>." % (d, ans))
    if k == "quantos":
        w = R.randrange(7)
        c = sum(1 for d in range(1, nd + 1) if dia_semana(ANO, mes, d) == DIAS[w])
        return mcq(pic + "%s %s tem esse mês?" % ("Quantos" if w in (0, 6) else "Quantas", DIAS[w] + "s" if w in (0, 6) else DIAS[w].replace("-feira", "s-feiras")), str(c), [str(x) for x in (3, 4, 5, 6) if x != c],
                   "Conte os números da coluna %s: <b>%d</b>." % ("DSTQQSS"[w], c))
    if k == "primeiro":
        w = R.choice([0, 6, 1, 5])
        d = next(d for d in range(1, 8) if dia_semana(ANO, mes, d) == DIAS[w])
        return mcq(pic + "Que data é %s %s desse mês?" % ("o primeiro" if w in (0, 6) else "a primeira", DIAS[w]), "dia %d" % d, ["dia %d" % x for x in (d + 7, d + 1 if d < 7 else d - 1, d + 2 if d < 6 else d - 2)],
                   "Olhe a primeira data na coluna %s: <b>dia %d</b>." % ("DSTQQSS"[w], d))
    ans = dia_semana(ANO, mes, nd)
    i = DIAS.index(ans)
    return mcq(pic + "Em que dia da semana termina esse mês?", ans, [DIAS[(i + 1) % 7], DIAS[(i - 1) % 7], DIAS[(i + 2) % 7]], "O último dia é %d: <b>%s</b>." % (nd, ans))


def s3_intervalo():
    mes = R.randint(1, 12)
    nd = DIAS_MES[mes - 1]
    a = R.randint(1, nd - 10)
    b = a + R.randint(3, 14)
    pic = mes_svg(ANO, mes, marks=(a, b))
    k = R.choice(["faltam", "semana"])
    if k == "faltam":
        p, _ = K.next()
        return mcq(pic + "Hoje é dia %d. O aniversário de %s é no dia %d (os dois dias estão marcados). Quantos dias faltam?" % (a, p, b), str(b - a), [str(b - a + 1), str(b - a - 1), str(b + a) if b + a <= 31 else str(b - a + 2)],
                   "Do dia %d até o dia %d: %d − %d = <b>%d dias</b> (não conte o dia de hoje)." % (a, b, b, a, b - a))
    a = R.randint(1, nd - 14)
    n = R.choice([1, 2])
    return mcq(mes_svg(ANO, mes, marks=(a,)) + "Hoje é dia %d (marcado). Que dia será daqui a %s?" % (a, "1 semana" if n == 1 else "2 semanas"), "dia %d" % (a + 7 * n),
               ["dia %d" % (a + 7 * n - 1), "dia %d" % (a + n), "dia %d" % (a + 7 * n + 1)],
               "1 semana = 7 dias. %d + %d = <b>%d</b>, no mesmo dia da semana." % (a, 7 * n, a + 7 * n))


def s4_semanas():
    k = R.choice(["dias", "semanas", "mes", "ano", "fim"])
    if k == "dias":
        n = R.randint(2, 4)
        return mcq("Quantos dias há em %d semanas?" % n, str(7 * n), [str(5 * n), str(7 + n), str(7 * n + 1)], "%s = <b>%d dias</b>." % (" + ".join(["7"] * n), 7 * n))
    if k == "semanas":
        n = R.randint(2, 4)
        return mcq("%d dias são quantas semanas?" % (7 * n), str(n), [str(7 * n), str(n + 1), str(n * 2)], "Cada semana tem 7 dias: <b>%d semanas</b>." % n)
    if k == "mes":
        return mcq(R.choice(["Um mês tem cerca de quantas semanas?", "Quantas semanas inteiras cabem em um mês, mais ou menos?"]), "cerca de 4 semanas", ["cerca de 2 semanas", "cerca de 7 semanas", "cerca de 12 semanas"],
                   "Um mês tem de 28 a 31 dias, e 4 semanas são 28 dias: <b>cerca de 4 semanas</b>.")
    if k == "ano":
        return mcq(R.choice(["Quantos meses tem um ano?", "Um ano tem quantos meses?"]), "12", ["7", "10", "30"], "De janeiro a dezembro: <b>12 meses</b>.")
    return mcq("Quais são os dias do fim de semana?", "sábado e domingo", ["sexta-feira e sábado", "segunda-feira e terça-feira", "domingo e segunda-feira"], "O fim de semana é <b>sábado e domingo</b>.")


def s5_agenda():
    p, g = K.next()
    k = R.choice(["festa", "viagem", "feriado", "mes", "prova"])
    if k == "festa":
        a, b = R.randint(2, 15), R.randint(18, 28)
        return mcq("Hoje é dia %d de maio. A festa junina da escola é no dia %d de maio. Quantos dias faltam?" % (a, b), "%d dias" % (b - a), ["%d dias" % (b - a + 1), "%d dias" % (b + a), "%d dias" % (b - a - 1)],
                   "%d − %d = <b>%d dias</b>." % (b, a, b - a))
    if k == "viagem":
        i = R.randrange(7)
        n = R.randint(3, 6)
        ans = DIAS[(i + n) % 7]
        return mcq("A família de %s viajou %s %s e voltou %d dias depois. Em que dia da semana voltou?" % (p, "num" if i in (0, 6) else "numa", DIAS[i], n), ans, [DIAS[(i + n - 1) % 7], DIAS[(i + n + 1) % 7], DIAS[(i - n) % 7]],
                   "Conte %d dias depois de %s: <b>%s</b>." % (n, DIAS[i], ans))
    if k == "feriado":
        f = R.choice([("o Natal", 12, 25), ("o Dia das Crianças", 10, 12), ("a Independência do Brasil", 9, 7), ("o Dia de Tiradentes", 4, 21), ("o Dia do Trabalho", 5, 1)])
        ans = MESES[f[1] - 1]
        return mcq("Em que mês é %s (dia %d)?" % (f[0], f[2]), ans, [MESES[f[1] % 12], MESES[f[1] - 2], MESES[(f[1] + 4) % 12]], "%s é em <b>%s</b>." % (f[0][0].upper() + f[0][1:], ans))
    if k == "mes":
        i = R.randrange(12)
        n = R.randint(2, 5)
        ans = MESES[(i + n) % 12]
        return mcq("Estamos em %s. Que mês será daqui a %d meses?" % (MESES[i], n), ans, [MESES[(i + n - 1) % 12], MESES[(i + n + 1) % 12], MESES[(i - n) % 12]],
                   "Conte %d meses: %s. Resposta: <b>%s</b>." % (n, ", ".join(MESES[(i + j) % 12] for j in range(1, n + 1)), ans))
    n = R.randint(1, 3)
    i = R.randrange(1, 6)
    return mcq("%s tem natação toda %s. Quantas aulas terá em %d semanas?" % (p, DIAS[i], n + 1), str(n + 1), [str(7 * (n + 1)), str(n), str(n + 2)],
               "Uma aula por semana: <b>%d aulas</b>." % (n + 1))


def main():
    seen = set()
    sets = [
        ("Dias da semana", mix(R, seen, [(s1_dias, 16), (s4_semanas, 4)])),
        ("Meses do ano", mix(R, seen, [(s1_meses, 18), (s4_semanas, 2)])),
        ("Ler o calendário", mix(R, seen, [(s2_ler, 20)])),
        ("Quantos dias faltam?", mix(R, seen, [(s3_intervalo, 16), (s4_semanas, 4)])),
        ("Agenda e problemas", mix(R, seen, [(s5_agenda, 20)])),
    ]
    body = lesson(
        ["A semana tem <b>7 dias</b>: domingo, segunda-feira, terça-feira, quarta-feira, quinta-feira, sexta-feira e sábado.",
         "O ano tem <b>12 meses</b>, de janeiro a dezembro. Os meses têm 28, 29, 30 ou 31 dias.",
         "No calendário, cada coluna é um dia da semana. Para saber o dia da semana de uma data, suba pela coluna.",
         "Para saber quantos dias faltam, tire a data de hoje da data marcada: do dia 8 ao dia 15 faltam 15 − 8 = 7 dias."],
        [("Hoje é quarta-feira. Daqui a 2 dias será…", ["quinta-feira, sexta-feira"], "sexta-feira"),
         ("Do dia 3 ao dia 10 do mesmo mês", ["10 − 3"], "7 dias (1 semana)")],
        [["Contar o dia de hoje junto", "Do dia 8 ao dia 15 são 7 dias, não 8."],
         ["Achar que todo mês tem 30 dias", "Janeiro tem 31; fevereiro, 28 ou 29."],
         ["Esquecer que depois de sábado vem domingo", "A semana recomeça: sábado, domingo, segunda…"]],
        mes_svg(ANO, 3, marks=(8, 15)))
    faq = [("O que o 2º ano aprende sobre o calendário?", "A BNCC pede indicar a duração de intervalos de tempo entre duas datas, como dias da semana e meses do ano, usando o calendário para planejar e organizar a agenda."),
           ("Como usar o calendário em casa?", "Pendure um calendário e marque datas importantes (aniversários, passeios). Pergunte todo dia: que dia é hoje? Quantos dias faltam para o aniversário?")]
    make_unit(R, "calendario", "M", ["EF02MA18"],
              "Indicar a duração de intervalos de tempo entre duas datas, como dias da semana e meses do ano, utilizando calendário, para planejamentos e organização de agenda",
              "Calendário: dias da semana, meses e datas", "Calendário",
              "Atividades de matemática para o 2º ano sobre o calendário: dias da semana, meses do ano, ler o calendário, quantos dias faltam entre duas datas e agenda. 100 exercícios com gabarito.",
              "A semana tem 7 dias; o ano tem 12 meses.", "Dias que faltam: data marcada − data de hoje.",
              body, faq, sets, 17, grade="2-ano")


if __name__ == "__main__":
    main()
