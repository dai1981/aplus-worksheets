# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Períodos do dia e sequência de acontecimentos (Grandezas e medidas, EF01MA16)
  python3 tools/gen_br_matematica_1_periodos_do_dia.py
Manhã, tarde e noite; o que vem antes e depois na rotina; ontem, hoje e amanhã; horas exatas no relógio de ponteiros
e no relógio digital; o que acontece primeiro.
Erros: achar que o almoço é de manhã cedo, trocar ontem e amanhã, ler o ponteiro grande como hora.
"""
import random
from br_common import mcq, lesson, make_unit, mix, relogio, digital, hora

R = random.Random(80115)
PERIODO = [("tomar o café da manhã", "manhã"), ("acordar para ir à escola", "manhã"), ("ver o sol nascer", "manhã"), ("almoçar depois da aula da manhã", "tarde"),
           ("lanchar depois do almoço", "tarde"), ("brincar no parque depois do almoço", "tarde"), ("jantar", "noite"), ("ver a lua e as estrelas", "noite"),
           ("dormir", "noite"), ("vestir o pijama", "noite"), ("escovar os dentes antes de dormir", "noite"), ("ver o pôr do sol", "tarde")]


def s1_periodo():
    a, p = R.choice(PERIODO)
    return mcq("Em que período do dia costumamos <b>%s</b>?" % a, p, [x for x in ("manhã", "tarde", "noite") if x != p] + ["madrugada"], "Costumamos %s à <b>%s</b>." % (a, p) if p != "manhã" else "Costumamos %s de <b>manhã</b>." % a)


ROTINA = ["acordar", "escovar os dentes", "tomar o café da manhã", "ir para a escola", "almoçar", "fazer a lição de casa", "jantar", "dormir"]


def s2_ordem():
    i, j = sorted(R.sample(range(len(ROTINA)), 2))
    k = R.choice(["antes", "depois", "primeiro"])
    if k == "primeiro":
        xs = R.sample(range(len(ROTINA)), 3)
        f = min(xs)
        return mcq("Na rotina de um dia de escola, o que acontece primeiro: %s?" % ", ".join(ROTINA[x] for x in xs), ROTINA[f], [ROTINA[x] for x in xs if x != f] + ["tudo ao mesmo tempo"],
                   "A ordem do dia é: %s. Primeiro: <b>%s</b>." % (", ".join(ROTINA[x] for x in sorted(xs)), ROTINA[f]))
    if k == "antes":
        return mcq("Num dia de escola, o que fazemos antes: %s ou %s?" % (ROTINA[j], ROTINA[i]), ROTINA[i], [ROTINA[j], "os dois ao mesmo tempo", "nenhum dos dois"],
                   "Primeiro vem <b>%s</b>, depois %s." % (ROTINA[i], ROTINA[j]))
    return mcq("Num dia de escola, o que fazemos depois: %s ou %s?" % (ROTINA[i], ROTINA[j]), ROTINA[j], [ROTINA[i], "os dois ao mesmo tempo", "nenhum dos dois"],
               "Primeiro %s, depois <b>%s</b>." % (ROTINA[i], ROTINA[j]))


DIAS = ["domingo", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado"]


def s3_ontem():
    i = R.randrange(7)
    k = R.choice(["ontem", "amanha", "depois"])
    d = DIAS
    if k == "ontem":
        return mcq("Hoje é %s. Que dia foi ontem?" % d[i], d[(i - 1) % 7], [d[(i + 1) % 7], d[i], d[(i - 2) % 7]], "Ontem é o dia antes de hoje: <b>%s</b>." % d[(i - 1) % 7])
    if k == "amanha":
        return mcq("Hoje é %s. Que dia será amanhã?" % d[i], d[(i + 1) % 7], [d[(i - 1) % 7], d[i], d[(i + 2) % 7]], "Amanhã é o dia depois de hoje: <b>%s</b>." % d[(i + 1) % 7])
    return mcq("Ontem foi %s. Que dia é hoje?" % d[i], d[(i + 1) % 7], [d[(i - 1) % 7], d[i], d[(i + 2) % 7]], "Hoje é o dia depois de ontem: <b>%s</b>." % d[(i + 1) % 7])


def s4_relogio():
    h = R.randint(1, 12)
    return mcq(relogio(h, 0) + "Que horas o relógio marca?", hora(h, 0), [hora(h % 12 + 1, 0), hora((h + 5) % 12 + 1, 0), hora(h, 30)],
               "O ponteiro grande está no 12 e o pequeno no %d: <b>%s</b> (%d em ponto)." % (h, hora(h, 0), h))


def s4_digital():
    h = R.randint(6, 21)
    act = {6: "acordar", 7: "tomar o café", 8: "começar a aula", 9: "fazer a roda de leitura", 10: "o recreio", 11: "a aula de artes", 12: "almoçar", 13: "descansar", 14: "brincar",
           15: "lanchar", 16: "fazer a lição", 17: "tomar banho", 18: "ver desenho", 19: "jantar", 20: "escovar os dentes", 21: "dormir"}[h]
    per = "manhã" if h < 12 else "tarde" if h < 18 else "noite"
    if R.random() < 0.5:
        return mcq(digital(h, 0) + "O relógio digital mostra a hora de %s. Que horas são?" % act, hora(h, 0), [hora(h + 1, 0), hora(h - 1, 0), hora(h, 30)], "Antes dos dois-pontos ficam as horas: <b>%s</b>." % hora(h, 0))
    return mcq(digital(h, 0) + "Este horário é de manhã, de tarde ou de noite?", per, [x for x in ("manhã", "tarde", "noite") if x != per] + ["madrugada"],
               "%s é à %s: <b>%s</b>." % (hora(h, 0), per, per) if per != "manhã" else "%s é de manhã: <b>manhã</b>." % hora(h, 0))


def main():
    seen = set()
    sets = [
        ("Manhã, tarde e noite", mix(R, seen, [(s1_periodo, 12), (s4_digital, 8)])),
        ("Antes e depois", mix(R, seen, [(s2_ordem, 20)])),
        ("Ontem, hoje e amanhã", mix(R, seen, [(s3_ontem, 20)])),
        ("Horas exatas", mix(R, seen, [(s4_relogio, 12), (s4_digital, 8)])),
        ("O meu dia", mix(R, seen, [(s2_ordem, 14), (s4_digital, 6)])),
    ]
    body = lesson(
        ["O dia tem períodos: <b>manhã</b> (acordar, ir à escola), <b>tarde</b> (almoço, lanche) e <b>noite</b> (jantar, dormir).",
         "As coisas acontecem numa ordem: primeiro acordamos, depois tomamos café.",
         "<b>Ontem</b> é o dia que passou; <b>amanhã</b> é o dia que vem.",
         "No relógio de ponteiros, quando o ponteiro grande está no 12, a hora é exata: o ponteiro pequeno mostra qual."],
        [("Escovar os dentes antes de dormir", ["à noite"], "noite"),
         ("Ponteiro pequeno no 3, grande no 12", ["hora exata"], "3h")],
        [["Achar que o almoço é de manhã cedo", "Almoçamos perto do meio-dia ou à tarde."],
         ["Trocar ontem e amanhã", "Ontem já passou; amanhã ainda vai chegar."],
         ["Ler o ponteiro grande como hora", "O ponteiro pequeno mostra as horas."]],
        relogio(3, 0))
    faq = [("O que o 1º ano aprende sobre o tempo?", "A BNCC pede contar a sequência de acontecimentos de um dia, usando os horários quando possível, e reconhecer os períodos do dia."),
           ("Como trabalhar a rotina em casa?", "Faça com a criança um quadro com desenhos da rotina (acordar, escola, almoço, banho, dormir) e marque as horas em que cada coisa acontece.")]
    make_unit(R, "periodos-do-dia", "M", ["EF01MA16"],
              "Relatar em linguagem verbal ou não verbal sequência de acontecimentos relativos a um dia, utilizando, quando possível, os horários dos eventos",
              "Períodos do dia: manhã, tarde e noite", "Períodos do dia",
              "Atividades de matemática para o 1º ano sobre os períodos do dia: manhã, tarde e noite, antes e depois, ontem, hoje e amanhã, horas exatas. 100 exercícios com gabarito.",
              "Manhã, tarde e noite.", "Ponteiro grande no 12: hora exata.",
              body, faq, sets, 15, grade="1-ano")


if __name__ == "__main__":
    main()
