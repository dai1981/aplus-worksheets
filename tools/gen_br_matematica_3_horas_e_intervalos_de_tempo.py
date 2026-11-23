# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Horas e intervalos de tempo (Grandezas e medidas, EF03MA22, EF03MA23)
  python3 tools/gen_br_matematica_3_horas_e_intervalos_de_tempo.py
Ler horas em relógios de ponteiros e digitais, horas da tarde (14h = 2 horas da tarde), relação entre hora, minuto e
segundo, horário de início e de término e duração de uma atividade, escolher a unidade de tempo, problemas.
Erros: trocar os ponteiros, ler 8h45 como «9h45», contar a duração errado quando passa da hora cheia.
"""
import random
from br_common import mcq, lesson, make_unit, mix, relogio, digital, hora, dur, Kids

R = random.Random(80319)
K = Kids(R)


def s1_ponteiros():
    h = R.randint(1, 12)
    m = R.choice([0, 15, 30, 45, 5, 10, 20, 25, 35, 40, 50, 55])
    hh = h if h != 12 or m else 12
    swap_h = m // 5 if m else 12
    w = [hora(h % 12 + 1, m) if m >= 30 else hora(h - 1 if h > 1 else 12, m), hora(swap_h, h * 5 % 60) if swap_h != h else None, hora(h, (m + 5) % 60)]
    return mcq(relogio(h, m) + "Que horas o relógio está marcando?", hora(hh, m), [x for x in w if x and x != hora(hh, m)] + [hora(h, (m + 10) % 60)],
               "O ponteiro pequeno indica as horas (%d) e o grande, os minutos (%d): <b>%s</b>." % (h, m, hora(hh, m)))


def s1_digital():
    h = R.randint(0, 23)
    m = R.randint(0, 59)
    tarde = h >= 13
    nm = hora(h, m)
    if R.random() < 0.5 or not tarde:
        return mcq(digital(h, m) + "Que horário o relógio digital mostra?", nm, [hora(m, h) if m < 24 and m != h and h < 60 else None, hora(h, (m + 10) % 60), hora((h + 1) % 24, m)],
                   "Antes dos dois-pontos ficam as horas e depois, os minutos: <b>%s</b>." % nm)
    m = m % 30
    return mcq(digital(h, m) + "O relógio digital mostra um horário da tarde ou da noite. Num relógio de ponteiros, o ponteiro pequeno ficaria perto de que número?", str(h - 12),
               [str(h), str((h - 12) % 12 + 1), str(m // 5 if m >= 5 else 12)],
               "%d horas = %d horas da %s (%d − 12 = %d): o ponteiro pequeno fica perto do <b>%d</b>." % (h, h - 12, "tarde" if h < 19 else "noite", h, h - 12, h - 12))


def s2_tarde():
    h = R.randint(13, 23)
    k = R.choice(["para", "de"])
    per = "tarde" if h < 19 else "noite"
    if k == "para":
        return mcq("%d horas é o mesmo que…" % h, "%d horas da %s" % (h - 12, per), ["%d horas da manhã" % (h - 12), "%d horas da %s" % (h - 10, per), "%d horas da %s" % (h - 11, per)],
                   "Depois do meio-dia, tire 12: %d − 12 = <b>%d horas da %s</b>." % (h, h - 12, per))
    return mcq("%d horas da %s é o mesmo que…" % (h - 12, per), "%dh" % h, ["%dh" % (h - 12), "%dh" % (h + 12) if h + 12 < 24 else "%dh" % (h - 2), "%dh" % (h - 10)],
               "Depois do meio-dia, some 12: %d + 12 = <b>%dh</b>." % (h - 12, h))


def s2_unidades():
    k = R.choice(["hmin", "minseg", "meia", "quarto", "dia", "minh", "hmin2"])
    if k == "hmin":
        v = R.randint(2, 5)
        return mcq("Quantos minutos há em %d horas?" % v, "%d minutos" % (60 * v), ["%d minutos" % (100 * v), "%d minutos" % (10 * v), "%d minutos" % (60 + v)],
                   "1 hora = 60 minutos: %d × 60 = <b>%d minutos</b>." % (v, 60 * v))
    if k == "minseg":
        v = R.randint(2, 5)
        return mcq("Quantos segundos há em %d minutos?" % v, "%d segundos" % (60 * v), ["%d segundos" % (100 * v), "%d segundos" % (10 * v), "%d segundos" % (60 + v)],
                   "1 minuto = 60 segundos: %d × 60 = <b>%d segundos</b>." % (v, 60 * v))
    if k == "meia":
        return mcq("Meia hora tem quantos minutos?", "30 minutos", ["50 minutos", "15 minutos", "60 minutos"], "Metade de 60 minutos: <b>30 minutos</b>.")
    if k == "quarto":
        return mcq("Um quarto de hora tem quantos minutos?", "15 minutos", ["25 minutos", "30 minutos", "4 minutos"], "60 ÷ 4 = <b>15 minutos</b>.")
    if k == "dia":
        return mcq("Quantas horas tem um dia inteiro?", "24 horas", ["12 horas", "60 horas", "100 horas"], "Um dia tem <b>24 horas</b>: 12 até o meio-dia e mais 12 até a meia-noite.")
    if k == "minh":
        v = R.choice([120, 180, 240])
        return mcq("%d minutos são quantas horas?" % v, "%d horas" % (v // 60), ["%d horas" % (v // 100) if v // 100 != v // 60 else "%d horas" % (v // 60 + 1), "%d horas" % (v // 10), "1 hora"],
                   "60 minutos = 1 hora: %d ÷ 60 = <b>%d horas</b>." % (v, v // 60))
    h, m = R.randint(1, 2), R.choice([10, 15, 20, 30, 45])
    return mcq("%d hora%s e %d minutos são quantos minutos?" % (h, "s" if h > 1 else "", m), "%d minutos" % (60 * h + m),
               ["%d minutos" % (100 * h + m), "%d minutos" % (h + m), "%d minutos" % (60 + m)],
               "%d × 60 + %d = <b>%d minutos</b>." % (h, m, 60 * h + m))


def s3_duracao():
    a = R.randint(7, 17)
    am = R.choice([0, 10, 15, 20, 30, 40, 45])
    d = R.choice([20, 30, 40, 45, 50, 60, 75, 90, 100, 120])
    e = a * 60 + am + d
    eh, em = divmod(e, 60)
    atv = R.choice(["A aula de natação", "O filme", "O jogo de futebol", "A aula de música", "O passeio", "A festa"])
    k = R.choice(["dur", "fim", "inicio"])
    if k == "dur":
        return mcq("%s começou às %s e terminou às %s. Quanto tempo durou?" % (atv, hora(a, am), hora(eh, em)), dur(d),
                   [dur(d + 10), dur(abs(d - 10)), dur(d + 40) if (em - am) % 60 != 0 else dur(d + 30)],
                   "De %s até %s passam <b>%s</b>." % (hora(a, am), hora(eh, em), dur(d)))
    if k == "fim":
        return mcq("%s começou às %s e durou %s. A que horas terminou?" % (atv, hora(a, am), dur(d)), hora(eh, em),
                   [hora((eh + 1) % 24, em), hora(eh, (em + 10) % 60), hora(a + d // 100, (am + d % 100) % 60) if (a + d // 100, (am + d % 100) % 60) != (eh, em) else hora(eh, (em + 20) % 60)],
                   "%s + %s = <b>%s</b>." % (hora(a, am), dur(d), hora(eh, em)))
    return mcq("%s terminou às %s e durou %s. A que horas começou?" % (atv, hora(eh, em), dur(d)), hora(a, am),
               [hora(a - 1, am), hora(a, (am + 10) % 60), hora(eh + d // 60, em)],
               "Volte %s a partir de %s: <b>%s</b>." % (dur(d), hora(eh, em), hora(a, am)))


def s3_relogios():
    h = R.randint(1, 10)
    m = R.choice([0, 15, 30, 45])
    d = R.choice([15, 30, 45, 60, 90])
    e = h * 60 + m + d
    eh, em = divmod(e, 60)
    return mcq(relogio(h, m) + "O relógio mostra a hora em que a lição começou. A lição durou %s. A que horas terminou?" % dur(d),
               hora(eh if eh <= 12 else eh - 12, em), [hora(eh + 1 if eh < 12 else 1, em), hora(eh if eh <= 12 else eh - 12, (em + 15) % 60), hora(h, (m + d) % 60) if (m + d) % 60 != em or h != eh else hora(h, (em + 30) % 60)],
               "%s + %s = <b>%s</b>." % (hora(h, m), dur(d), hora(eh if eh <= 12 else eh - 12, em)))


UNID = [("Quanto tempo dura uma piscada de olho?", "menos de 1 segundo", ["1 hora", "1 minuto", "1 dia"]),
        ("Quanto tempo dura uma aula?", "cerca de 50 minutos", ["cerca de 50 segundos", "cerca de 50 horas", "cerca de 5 dias"]),
        ("Quanto tempo dura uma noite de sono de uma criança?", "cerca de 10 horas", ["cerca de 10 minutos", "cerca de 10 segundos", "cerca de 10 dias"]),
        ("Quanto tempo se leva para escovar os dentes?", "cerca de 2 minutos", ["cerca de 2 horas", "cerca de 2 segundos", "cerca de 2 dias"]),
        ("Que instrumento usamos para medir o tempo de uma corrida?", "o cronômetro", ["a balança", "a régua", "o termômetro"]),
        ("Quanto tempo dura uma partida de futebol (sem os acréscimos)?", "90 minutos", ["90 segundos", "90 horas", "9 minutos"]),
        ("Quanto tempo dura um ano escolar no Brasil, mais ou menos?", "cerca de 10 meses", ["cerca de 10 dias", "cerca de 10 semanas", "cerca de 10 horas"]),
        ("Quanto tempo leva para tomar um copo de água?", "alguns segundos", ["algumas horas", "alguns dias", "algumas semanas"])]


def s4_unidade():
    q, a, w = R.choice(UNID)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def s5_problema():
    p, g = K.next()
    k = R.choice(["onibus", "bolo", "treino", "acordar", "filme", "cronometro", "dormir"])
    if k == "onibus":
        a = R.randint(6, 8)
        m = R.choice([10, 20, 30, 40])
        d = R.choice([15, 25, 35, 40])
        e = a * 60 + m + d
        return mcq("%s pega o ônibus às %s e a viagem até a escola dura %d minutos. A que horas chega?" % (p, hora(a, m), d), hora(*divmod(e, 60)),
                   [hora(a, (m + d) % 60) if m + d >= 60 else hora(a + 1, (m + d) % 60), hora(*divmod(e + 10, 60)), hora(*divmod(e - 10, 60))],
                   "%s + %d min = <b>%s</b>." % (hora(a, m), d, hora(*divmod(e, 60))))
    if k == "bolo":
        a = R.randint(14, 17)
        d = R.choice([35, 40, 45, 50])
        e = a * 60 + 30 + d
        return mcq("Um bolo entrou no forno às %s e precisa assar %d minutos. A que horas deve sair?" % (hora(a, 30), d), hora(*divmod(e, 60)),
                   [hora(a, 30 + d - 60) if 30 + d >= 60 else hora(a + 1, 30 + d), hora(a + 1, 30), hora(*divmod(e + 5, 60))],
                   "%s + %d min = <b>%s</b>." % (hora(a, 30), d, hora(*divmod(e, 60))))
    if k == "treino":
        n, d = R.randint(2, 5), R.choice([30, 45, 60, 90])
        t = n * d
        return mcq("%s treina %s, %d vezes por semana. Quanto tempo treina por semana?" % (p, dur(d), n), dur(t), [dur(t + d), dur(t - 30), dur(n + d)],
                   "%d × %d min = %d min = <b>%s</b>." % (n, d, t, dur(t)))
    if k == "acordar":
        a, b = R.randint(6, 7), R.choice([0, 15, 30])
        s_ = R.randint(7, 8) if a == 6 else 8
        sm = R.choice([0, 15, 30])
        d = (s_ * 60 + sm) - (a * 60 + b)
        if d <= 0:
            return None
        return mcq("%s acorda às %s e sai de casa às %s. Quanto tempo leva para se arrumar?" % (p, hora(a, b), hora(s_, sm)), dur(d), [dur(d + 15), dur(abs(d - 15)) if d > 15 else dur(d + 30), dur(d + 60)],
                   "De %s até %s: <b>%s</b>." % (hora(a, b), hora(s_, sm), dur(d)))
    if k == "filme":
        a = R.randint(18, 20)
        d = R.choice([90, 100, 110, 120, 135])
        e = a * 60 + d
        return mcq("Um filme começa às %s e dura %s. A que horas termina?" % (hora(a, 0), dur(d)), hora(*divmod(e, 60)),
                   [hora(a + 1, d - 60 if d < 120 else d - 120), hora(*divmod(e + 30, 60)), hora(a + d // 100, d % 100 % 60)],
                   "%s + %s = <b>%s</b>." % (hora(a, 0), dur(d), hora(*divmod(e, 60))))
    if k == "cronometro":
        a, b = R.randint(40, 75), R.randint(40, 75)
        if a == b:
            return None
        (p2, _) = K.next()
        win = p if a < b else p2
        return mcq("Na corrida, %s fez o percurso em %d segundos e %s em %d segundos. Quem chegou primeiro?" % (p, a, p2, b), win,
                   [p2 if win == p else p, "chegaram juntos", "quem fez mais segundos"],
                   "Chega primeiro quem gasta <b>menos</b> tempo: %d s. Resposta: <b>%s</b>." % (min(a, b), win))
    a = R.randint(20, 22)
    b = R.randint(6, 7)
    d = (24 - a + b) * 60
    return mcq("%s dorme às %dh e acorda às %dh do dia seguinte. Quantas horas dorme?" % (p, a, b), "%d horas" % (24 - a + b),
               ["%d horas" % (a - b), "%d horas" % (24 - a + b + 1), "%d horas" % (24 - a + b - 1)],
               "Das %dh à meia-noite são %d horas; da meia-noite às %dh são %d: <b>%d horas</b>." % (a, 24 - a, b, b, 24 - a + b))


def main():
    seen = set()
    sets = [
        ("Ler o relógio de ponteiros", mix(R, seen, [(s1_ponteiros, 20)])),
        ("Relógio digital e horas da tarde", mix(R, seen, [(s1_digital, 12), (s2_tarde, 8)])),
        ("Hora, minuto e segundo", mix(R, seen, [(s2_unidades, 12), (s4_unidade, 8)])),
        ("Início, término e duração", mix(R, seen, [(s3_duracao, 14), (s3_relogios, 6)])),
        ("Problemas com horas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["No relógio de ponteiros, o ponteiro <b>pequeno</b> marca as horas e o <b>grande</b> marca os minutos. Cada número vale 5 minutos para o ponteiro grande.",
         "No relógio digital, antes dos dois-pontos ficam as horas e depois, os minutos: 14:35 = 14h35.",
         "Depois do meio-dia, contamos 13h, 14h… até 23h. Para saber a hora «da tarde», tire 12: 15h = 3 horas da tarde.",
         "1 hora = 60 minutos e 1 minuto = 60 segundos. Para achar a duração, conte do horário de início até o de término."],
        [("Começou às 8h40 e durou 35 minutos", ["8h40 + 20 min = 9h", "9h + 15 min = 9h15"], "9h15"),
         ("De 14h15 até 15h45", ["14h15 → 15h15: 1 h", "15h15 → 15h45: 30 min"], "1 h 30 min")],
        [["Trocar os ponteiros", "O pequeno é das horas; o grande, dos minutos."],
         ["Ler 8h45 como 9h45", "Se o ponteiro pequeno está entre o 8 e o 9, ainda são 8 horas."],
         ["8h40 + 35 min = 8h75", "Passou de 60 minutos: vira mais uma hora. 9h15."]],
        relogio(8, 45))
    faq = [("O que a BNCC pede sobre horas no 3º ano?", "Ler horas em relógios digitais e de ponteiros, relacionar hora, minuto e segundo e registrar o início, o término e a duração de atividades."),
           ("Como ensinar a ler o relógio de ponteiros?", "Use um relógio de verdade ou de papel. Primeiro só o ponteiro das horas, depois conte de 5 em 5 com o ponteiro dos minutos. Pergunte a hora em momentos da rotina.")]
    make_unit(R, "horas-e-intervalos-de-tempo", "M", ["EF03MA22", "EF03MA23"],
              "Ler e registrar medidas e intervalos de tempo, utilizando relógios (analógico e digital) para informar os horários de início e término de realização de uma atividade e sua duração; ler horas em relógios digitais e em relógios analógicos e reconhecer a relação entre hora e minutos e entre minuto e segundos",
              "Horas e intervalos de tempo: relógio de ponteiros e digital", "Horas e intervalos de tempo",
              "Atividades de matemática para o 3º ano sobre horas: relógio de ponteiros e digital, horas da tarde, hora, minuto e segundo, início, término e duração de atividades, problemas. 100 exercícios com gabarito.",
              "Ponteiro pequeno: horas. Ponteiro grande: minutos.", "1 hora = 60 minutos; 1 minuto = 60 segundos.",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
