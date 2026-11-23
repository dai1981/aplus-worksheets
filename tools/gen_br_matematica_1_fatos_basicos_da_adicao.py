# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Fatos básicos da adição (Números, EF01MA06)
  python3 tools/gen_br_matematica_1_fatos_basicos_da_adicao.py
Somar juntando figuras, dados e quadros de dez; contar a partir do maior; somar 0 e 1; pares que formam 10; dobros;
a ordem não muda a soma; completar a adição. Usa geradores do 2º ano (fatos básicos) com outro sorteio.
Erros: contar tudo de novo desde o 1, contar o primeiro número duas vezes, achar que 5 + 0 = 0.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim, KINDS
from br_1 import dois_grupos, dados, quadro_dez, nome, quantos

R = random.Random(80106)
M2 = "gen_br_matematica_2_fatos_basicos_de_adicao_e_subtracao"
f_soma, f_dez, f_dobro, f_prob = use(M2, 80971, "s1_soma", "s2_dez", "s2_dobro", "s5_problema", preds=(lim(20, 0),))


def add_only(it):
    return "−" not in it["q"] + it["e"]


f_prob_add = use(M2, 80971, "s5_problema", preds=(lim(20, 0), add_only))


def s1_figuras():
    kind = R.choice(KINDS)
    a, b = R.randint(1, 6), R.randint(1, 5)
    return mcq(dois_grupos(a, kind, b) + "%s %s há ao todo?" % (quantos(kind), nome(kind)), str(a + b), [str(a + b + 1), str(a + b - 1), str(abs(a - b)) if a != b else str(a + b + 2)],
               "%d + %d = <b>%d</b>." % (a, b, a + b))


def s1_dados():
    a, b = R.randint(1, 6), R.randint(1, 6)
    return mcq(dados([a, b]) + "Quanto dá %d + %d?" % (a, b), str(a + b), [str(a + b + 1), str(a + b - 1), str(a * 10 + b)],
               "Comece no %d e conte mais %d: <b>%d</b>." % (max(a, b), min(a, b), a + b))


def s2_quadro():
    a = R.randint(5, 9)
    b = R.randint(2, 9)
    if a + b > 20 or a + b <= 10:
        return None
    return mcq(quadro_dez(a + b, 2) + "O quadro mostra %d + %d. Quanto é?" % (a, b), str(a + b), [str(a + b - 1), str(a + b + 1), str(10 + b)],
               "Complete o 10: %d + %d = 10, e sobram %d. 10 + %d = <b>%d</b>." % (a, 10 - a, b - (10 - a), b - (10 - a), a + b))


def s2_maior():
    a, b = R.randint(1, 4), R.randint(6, 9)
    return mcq("Calcule %d + %d. Dica: comece pelo maior." % (a, b), str(a + b), [str(a + b + 1), str(a + b - 1), str(b - a)],
               "Comece no %d e conte mais %d: %s. Resposta: <b>%d</b>." % (b, a, ", ".join(str(b + i) for i in range(1, a + 1)), a + b))


def s3_zero_um():
    n = R.randint(2, 19)
    k = R.choice(["0", "1", "ordem"])
    if k == "0":
        return mcq("Quanto é %d + 0?" % n, str(n), ["0", str(n + 1), str(n * 10) if n < 10 else str(n - 1)], "Somar 0 não muda o número: <b>%d</b>." % n)
    if k == "1":
        return mcq("Quanto é %d + 1?" % n, str(n + 1), [str(n), str(n + 10) if n < 10 else str(n - 1), str(n + 2)], "Somar 1 é dizer o número seguinte: <b>%d</b>." % (n + 1))
    a, b = R.randint(2, 9), R.randint(2, 9)
    if a == b:
        return None
    return mcq("Se %d + %d = %d, quanto é %d + %d?" % (a, b, a + b, b, a), str(a + b), [str(a + b + 1), str(abs(a - b)), str(a + b - 1)],
               "A ordem não muda a soma: <b>%d</b>." % (a + b))


def s4_completar():
    a = R.randint(1, 9)
    s = R.randint(a + 1, min(a + 9, 18))
    return mcq("Complete: %d + ___ = %d" % (a, s), str(s - a), [str(s), str(s - a + 1), str(s + a) if s + a <= 20 else str(s - a - 1)],
               "Conte do %d até o %d: faltam <b>%d</b>." % (a, s, s - a))


def main():
    seen = set()
    sets = [
        ("Juntar figuras", mix(R, seen, [(s1_figuras, 10), (s1_dados, 10)])),
        ("Contar a partir do maior", mix(R, seen, [(s2_maior, 8), (s3_zero_um, 8), (f_soma, 4)])),
        ("Formar 10 e passar do 10", mix(R, seen, [(f_dez, 8), (s2_quadro, 12)])),
        ("Dobros e completar", mix(R, seen, [(f_dobro, 10), (s4_completar, 10)])),
        ("Problemas", mix(R, seen, [(f_prob_add, 20)])),
    ]
    body = lesson(
        ["Somar é <b>juntar</b>: 3 bolas e mais 2 bolas são 5 bolas. Escrevemos 3 + 2 = 5.",
         "Para somar, comece pelo número <b>maior</b> e conte o menor: 8 + 3 → 9, 10, 11.",
         "Somar 0 não muda nada; somar 1 é dizer o número seguinte.",
         "Use os pares que formam 10 (7 + 3, 6 + 4) e os dobros (5 + 5)."],
        [("2 + 7", ["comece no 7: 8, 9"], "9"),
         ("8 + 5", ["8 + 2 = 10", "10 + 3 = 13"], "13")],
        [["Contar tudo de novo desde o 1", "Comece no maior número."],
         ["Contar o primeiro número de novo (8 + 3: 8, 9, 10)", "Comece depois do 8: 9, 10, 11."],
         ["Achar que 5 + 0 = 0", "Somar 0 deixa o número igual: 5 + 0 = 5."]],
        dois_grupos(4, "apple", 3, "apple"))
    faq = [("O que são fatos básicos da adição?", "São as somas com números de 0 a 10, como 6 + 3 e 8 + 7. A BNCC pede que o 1º ano construa esses fatos e os use para resolver problemas."),
           ("Como praticar em casa?", "Jogue dois dados e some os pontos. Comece contando a partir do número maior e depois tente dizer de cabeça.")]
    make_unit(R, "fatos-basicos-da-adicao", "N", ["EF01MA06"],
              "Construir fatos básicos da adição e utilizá-los em procedimentos de cálculo para resolver problemas",
              "Fatos básicos da adição", "Fatos básicos da adição",
              "Atividades de matemática para o 1º ano sobre fatos básicos da adição: juntar figuras, dados, contar a partir do maior, formar 10, dobros e completar. 100 exercícios com gabarito.",
              "Comece pelo número maior.", "Use os pares que formam 10.",
              body, faq, sets, 6, grade="1-ano")


if __name__ == "__main__":
    main()
