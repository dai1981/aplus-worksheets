# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Horas e intervalos de tempo (Grandezas e medidas, EF02MA19)
  python3 tools/gen_br_matematica_2_horas_e_intervalos_de_tempo.py
Ler o relógio digital; horas exatas e meias horas no relógio de ponteiros; hora, minuto e segundo;
horário de início e de fim e duração (em horas inteiras e em minutos); rotina do dia. Usa geradores do 3º ano com outro sorteio.
Erros: trocar horas e minutos no relógio digital, contar a hora de início na duração, achar que 1 hora tem 100 minutos.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim, hora, dur, digital, relogio

R = random.Random(80218)
M3 = "gen_br_matematica_3_horas_e_intervalos_de_tempo"
t_digital, t_ponteiros, t_unid, t_unidade, t_duracao, t_prob = use(M3, 80911, "s1_digital", "s1_ponteiros", "s2_unidades", "s4_unidade", "s3_duracao", "s5_problema", preds=(lim(200, 0),))

ATV = ["a aula de natação", "o filme", "o treino de futebol", "a aula de música", "o passeio ao zoológico", "a festa de aniversário", "a aula de inglês", "o almoço da família"]


def s1_exata():
    h = R.randint(1, 12)
    m = R.choice([0, 30])
    nm = hora(h, m)
    return mcq(relogio(h, m) + "Que horas o relógio marca?", nm, [hora(h % 12 + 1, m), hora(h, 30 - m), hora((h - 2) % 12 + 1, m)],
               ("O ponteiro grande está no 12 e o pequeno no %d: <b>%s</b> (%d em ponto)." % (h, nm, h)) if m == 0 else
               "O ponteiro grande está no 6 (meia hora) e o pequeno entre o %d e o %d: <b>%s</b>." % (h, h % 12 + 1, nm))


def s2_inicio_fim():
    a = R.randint(7, 18)
    am = R.choice([0, 0, 10, 15, 20, 30, 40])
    d = R.choice([60, 120, 180, 30, 20, 40, 45, 15])
    e = a * 60 + am + d
    eh, em = divmod(e, 60)
    atv = R.choice(ATV)
    pic = digital(a, am) + digital(eh, em)
    return mcq(pic + "O 1º relógio mostra quando começou %s e o 2º, quando terminou. Quanto tempo durou?" % atv,
               dur(d), [dur(d + 60) if d < 60 else dur(d + 30), dur(abs(d - 10)) if d > 10 else dur(d + 5), dur(d * 2)],
               "De %s até %s passam <b>%s</b>." % (hora(a, am), hora(eh, em), dur(d)))


def s2_fim():
    a = R.randint(7, 18)
    am = R.choice([0, 15, 30])
    d = R.choice([60, 120, 30, 15, 45])
    e = a * 60 + am + d
    eh, em = divmod(e, 60)
    atv = R.choice(ATV)
    return mcq(digital(a, am) + "O relógio mostra quando começou %s. Durou %s. A que horas terminou?" % (atv, dur(d)), hora(eh, em),
               [hora(eh + 1, em), hora(a, (am + d) % 60) if (am + d) % 60 != em or a != eh else hora(eh, (em + 15) % 60), hora(eh, (em + 30) % 60)],
               "%s + %s = <b>%s</b>." % (hora(a, am), dur(d), hora(eh, em)))


ROTINA = [("A que horas é mais provável uma criança acordar para ir à escola?", "7h", ["13h", "23h", "3h"]),
          ("A que horas é mais provável jantar?", "19h30", ["7h", "10h", "3h"]),
          ("A que horas é mais provável almoçar?", "12h", ["5h", "20h", "1h"]),
          ("A que horas é mais provável uma criança ir dormir?", "21h", ["10h", "15h", "6h"]),
          ("O que dura mais: um filme ou escovar os dentes?", "um filme", ["escovar os dentes", "os dois duram o mesmo", "não dá para saber"]),
          ("O que dura menos: um piscar de olhos ou um recreio?", "um piscar de olhos", ["um recreio", "os dois duram o mesmo", "não dá para saber"]),
          ("Que relógio usamos para marcar o tempo de uma corrida?", "o cronômetro", ["o calendário", "a régua", "a balança"]),
          ("No relógio digital, o número antes dos dois-pontos mostra…", "as horas", ["os minutos", "os segundos", "o dia"])]


def s3_rotina():
    q, a, w = R.choice(ROTINA)
    return mcq(q, a, w, "Pense no seu dia a dia. Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Ler o relógio digital", mix(R, seen, [(t_digital, 14), (s3_rotina, 6)])),
        ("Relógio de ponteiros: horas e meias horas", mix(R, seen, [(s1_exata, 14), (t_ponteiros, 6)])),
        ("Hora, minuto e segundo", mix(R, seen, [(t_unid, 12), (t_unidade, 8)])),
        ("Início, fim e duração", mix(R, seen, [(s2_inicio_fim, 12), (s2_fim, 8)])),
        ("Problemas com horas", mix(R, seen, [(t_duracao, 10), (t_prob, 10)])),
    ]
    body = lesson(
        ["No <b>relógio digital</b>, antes dos dois-pontos ficam as <b>horas</b> e depois, os <b>minutos</b>: 08:30 é 8h30.",
         "No relógio de ponteiros, o ponteiro pequeno marca as horas e o grande, os minutos. Grande no 12: hora exata. Grande no 6: meia hora.",
         "1 hora = 60 minutos e 1 minuto = 60 segundos. Meia hora = 30 minutos.",
         "Para achar a <b>duração</b>, veja o horário de início e o de fim e conte quanto tempo passou."],
        [("Início 14:00, fim 16:00", ["14h → 15h: 1 h", "15h → 16h: 1 h"], "2 horas"),
         ("Começou às 9h e durou 30 minutos", ["9h + 30 min"], "terminou às 9h30")],
        [["Ler 08:45 como 45 horas e 8 minutos", "Horas vêm antes dos dois-pontos."],
         ["Achar que 1 hora tem 100 minutos", "1 hora tem 60 minutos."],
         ["Contar a hora do início como 1 hora a mais", "De 14h a 16h passam 2 horas, não 3."]],
        digital(14, 0) + digital(16, 0))
    faq = [("O que o 2º ano aprende sobre horas?", "A BNCC pede medir a duração de um intervalo de tempo com o relógio digital e registrar o horário do início e do fim. Também é bom ler horas exatas e meias horas no relógio de ponteiros."),
           ("Como praticar em casa?", "Marque com a criança a hora em que começa e termina um desenho animado ou o banho, e calcule juntos quanto tempo durou.")]
    make_unit(R, "horas-e-intervalos-de-tempo", "M", ["EF02MA19"],
              "Medir a duração de um intervalo de tempo por meio de relógio digital e registrar o horário do início e do fim do intervalo",
              "Horas e intervalos de tempo: relógio digital", "Horas e duração",
              "Atividades de matemática para o 2º ano sobre horas: relógio digital, horas exatas e meias horas, hora, minuto e segundo, início, fim e duração. 100 exercícios com gabarito.",
              "08:30: horas antes dos dois-pontos, minutos depois.", "1 hora = 60 minutos.",
              body, faq, sets, 18, grade="2-ano")


if __name__ == "__main__":
    main()
