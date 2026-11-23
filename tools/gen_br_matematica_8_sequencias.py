# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Sequências recursivas e não recursivas (Álgebra, EF08MA10, EF08MA11)
  python3 tools/gen_br_matematica_8_sequencias.py
Identificar a regularidade; termo seguinte; lei de formação recursiva (aₙ = aₙ₋₁ + 4) e não recursiva (aₙ = 4n − 1);
passar de uma forma para a outra; fluxograma que gera a sequência; termos de ordem alta; sequências de figuras.
Usa geradores do 7º ano (sequências) com outro sorteio.
Erros: usar a forma recursiva para achar o 100º termo à mão, errar o primeiro termo, confundir aₙ₋₁ com n − 1.
"""
import random
from br_common import lesson, mix, use
from br_9 import M, d, expr, bank, unit

R = random.Random(88010)
q_prox, q_geral, q_fig = use("gen_br_matematica_7_sequencias", 88910, "s1_proximo", "s2_geral", "s3_figuras")


def s1_recursiva():
    a1 = R.randint(-5, 10)
    k = R.choice(["soma", "mult", "misto"])
    if k == "soma":
        r = R.choice([-4, -3, 2, 3, 5, 7])
        t = [a1 + r * i for i in range(5)]
        lei = "a₁ = %s e aₙ = aₙ₋₁ %s %d" % (d(a1), "+" if r > 0 else "−", abs(r))
    elif k == "mult":
        a1 = R.randint(1, 4)
        r = R.choice([2, 3, -2])
        t = [a1 * r ** i for i in range(5)]
        lei = "a₁ = %d e aₙ = %s · aₙ₋₁" % (a1, d(r))
    else:
        a1 = R.randint(1, 4)
        t = [a1]
        for _ in range(4):
            t.append(2 * t[-1] + 1)
        lei = "a₁ = %d e aₙ = 2 · aₙ₋₁ + 1" % a1
    return M("Quais são os 5 primeiros termos da sequência %s?" % lei, ", ".join(d(x) for x in t), [", ".join(d(x) for x in t[1:] + [t[-1] + (t[-1] - t[-2])]), ", ".join(d(a1 + i) for i in range(5)), ", ".join(d(x) for x in [t[0]] + [x + 1 for x in t[1:]])],
             "Comece em a₁ e aplique a regra a cada passo: <b>%s</b>." % ", ".join(d(x) for x in t))


def s2_converter():
    r, c = R.choice([2, 3, 4, 5, -2, -3]), R.randint(-6, 9)
    a1 = r + c
    k = R.choice(["r2n", "n2r"])
    if k == "r2n":
        ok = "aₙ = %s" % expr([(r, "n"), (c, "")])
        return M("Qual lei não recursiva (pela posição n) gera a sequência a₁ = %s, aₙ = aₙ₋₁ %s %d?" % (d(a1), "+" if r > 0 else "−", abs(r)), ok, ["aₙ = %s" % expr([(r, "n"), (a1, "")]), "aₙ = %s" % expr([(a1, "n"), (r, "")]), "aₙ = %s" % expr([(r, "n"), (c - r, "")])],
                     "A diferença é %s: aₙ = %sn + b; com a₁ = %s, b = %s. <b>%s</b>." % (d(r), d(r), d(a1), d(c), ok))
    ok = "a₁ = %s e aₙ = aₙ₋₁ %s %d" % (d(a1), "+" if r > 0 else "−", abs(r))
    return M("Qual lei recursiva gera a mesma sequência que aₙ = %s?" % expr([(r, "n"), (c, "")]), ok, ["a₁ = %s e aₙ = aₙ₋₁ %s %d" % (d(c), "+" if r > 0 else "−", abs(r)), "a₁ = %s e aₙ = %s · aₙ₋₁" % (d(a1), d(r)), "a₁ = %s e aₙ = aₙ₋₁ %s %d" % (d(a1), "−" if r > 0 else "+", abs(r))],
             "a₁ = %s e cada termo aumenta %s: <b>%s</b>." % (d(a1), d(r), ok))


s3_fluxo = bank(R, [
    ("Um fluxograma: «comece com 3 → escreva o número → some 4 → volte a escrever». Os 4 primeiros números escritos são…", "3, 7, 11, 15", ["3, 4, 5, 6", "4, 8, 12, 16", "3, 12, 48, 192"]),
    ("Um fluxograma: «comece com 1 → escreva → multiplique por 3 → volte». Os 4 primeiros números são…", "1, 3, 9, 27", ["1, 4, 7, 10", "3, 6, 9, 12", "1, 3, 6, 9"]),
    ("Um fluxograma: «n = 1 → escreva 2n + 1 → n = n + 1 → volte». Os 4 primeiros números são…", "3, 5, 7, 9", ["1, 3, 5, 7", "2, 4, 6, 8", "3, 4, 5, 6"]),
    ("Um fluxograma: «comece com 100 → escreva → subtraia 15 → o número é negativo? não: volte; sim: pare». Quantos números são escritos?", "7", ["6", "8", "100"]),
    ("Um fluxograma: «comece com 2 → escreva → eleve ao quadrado → passou de 1.000? não: volte; sim: pare». O último número escrito é…", "256", ["16", "65.536", "1.000"]),
    ("Numa lei recursiva, para calcular um termo é preciso conhecer…", "o termo anterior", ["só a posição n", "o último termo", "a soma de todos"]),
    ("Numa lei não recursiva, para calcular o 50º termo basta…", "substituir n por 50", ["calcular os 49 termos antes", "conhecer o 49º termo", "somar 50"]),
    ("A sequência de Fibonacci (1, 1, 2, 3, 5, 8, …) é…", "recursiva", ["não recursiva", "constante", "decrescente"]),
], "s3_fluxo")


def main():
    seen = set()
    sets = [
        ("Regularidades", mix(R, seen, [(q_prox, 20)])),
        ("Leis recursivas", mix(R, seen, [(s1_recursiva, 20)])),
        ("Leis não recursivas", mix(R, seen, [(q_geral, 20)])),
        ("De uma forma para a outra", mix(R, seen, [(s2_converter, 14), (s3_fluxo, 6)])),
        ("Figuras e fluxogramas", mix(R, seen, [(q_fig, 18), (s3_fluxo, 2)])),
    ]
    body = lesson(
        ["Numa <b>lei recursiva</b>, cada termo vem do anterior: a₁ = 5 e aₙ = aₙ₋₁ + 3 dá 5, 8, 11, 14, …",
         "Numa <b>lei não recursiva</b>, o termo vem direto da posição n: aₙ = 3n + 2 dá os mesmos 5, 8, 11, 14, …",
         "Se a diferença entre termos seguidos é sempre r, as duas formas se ligam: aₙ = r · n + (a₁ − r).",
         "Para achar um termo distante (o 100º), use a lei não recursiva."],
        [("a₁ = 2, aₙ = aₙ₋₁ + 5", ["diferença 5", "b = 2 − 5 = −3"], "aₙ = 5n − 3")],
        [["Calcular o 100º termo pela recursiva", "Use aₙ = r · n + b."],
         ["Errar o primeiro termo", "Confira: n = 1 dá a₁?"],
         ["Confundir aₙ₋₁ com n − 1", "aₙ₋₁ é o termo anterior, não a posição."]])
    faq = [("Qual é a diferença entre sequência recursiva e não recursiva?", "Na recursiva, cada termo é calculado a partir do anterior. Na não recursiva, cada termo é calculado diretamente pela sua posição n."),
           ("O que a BNCC pede no 8º ano?", "Identificar a regularidade de uma sequência numérica ou figural não recursiva e construir um algoritmo por meio de um fluxograma que permita indicar os números ou as figuras seguintes (EF08MA10) e identificar a regularidade de uma sequência numérica recursiva e construir um algoritmo (EF08MA11).")]
    unit(R, "sequencias-recursivas-e-nao-recursivas", "A", ["EF08MA10", "EF08MA11"],
         "Identificar a regularidade de uma sequência numérica ou figural não recursiva e construir um algoritmo por meio de um fluxograma que permita indicar os números ou as figuras seguintes; identificar a regularidade de uma sequência numérica recursiva e construir um algoritmo por meio de um fluxograma que permita indicar os números seguintes",
         "Sequências recursivas e não recursivas", "Sequências",
         "Atividades de matemática para o 8º ano sobre sequências: regularidades, leis recursivas e não recursivas, passar de uma forma para a outra, fluxogramas e sequências de figuras. 100 exercícios com gabarito.",
         "Recursiva: a partir do anterior.", "Não recursiva: pela posição n.",
         body, faq, sets, 10, grade="8-ano")


if __name__ == "__main__":
    main()
