# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Sequências e padrões (Álgebra, EF01MA10)
  python3 tools/gen_br_matematica_1_sequencias_e_padroes.py
Sequências de figuras, cores e letras que se repetem; a figura que vem depois e a que falta; a parte que se repete;
sequências de números de 1 em 1, 2 em 2, 5 em 5 e 10 em 10 (crescentes e decrescentes), até 100.
Usa geradores do 2º ano (padrões e sequências) com outro sorteio.
Erros: olhar só a última figura, achar que a parte que se repete tem uma figura só, contar de 2 em 2 pulando errado.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim
from br_2 import padrao

R = random.Random(80110)
P2 = "gen_br_matematica_2_padroes_e_sequencias_repetitivas"
S2 = "gen_br_matematica_2_sequencias_numericas"
p_prox, p_falta, p_parte, p_letras = use(P2, 80975, "s1_proximo", "s1_falta", "s2_parte", "s4_letras")
L = (lim(100, 0),)
n_falta, n_reta = use(S2, 80976, "s2_falta", "s3_reta", preds=L)


def s4_contar():
    d = R.choice([1, 2, 5, 10])
    up = R.random() < 0.7
    a = R.randint(0, 20) if d < 5 else R.randint(0, 4) * d
    if not up:
        a += 5 * d
    xs = [a + (d if up else -d) * i for i in range(5)]
    if min(xs) < 0 or max(xs) > 100:
        return None
    nxt = xs[-1] + (d if up else -d)
    if not 0 < nxt <= 100:
        return None
    return mcq("Continue: %s, ___" % ", ".join(map(str, xs)), str(nxt), [str(nxt + 1), str(xs[-1] - (d if up else -d)), str(nxt + d if up else nxt - 1)],
               "A sequência %s de %d em %d: <b>%d</b>." % ("aumenta" if up else "diminui", d, d, nxt))


def main():
    seen = set()
    sets = [
        ("Qual vem depois?", mix(R, seen, [(p_prox, 14), (p_letras, 6)])),
        ("Qual figura falta?", mix(R, seen, [(p_falta, 14), (p_letras, 6)])),
        ("A parte que se repete", mix(R, seen, [(p_parte, 20)])),
        ("Sequências de números", mix(R, seen, [(s4_contar, 14), (n_reta, 6)])),
        ("Números que faltam", mix(R, seen, [(n_falta, 14), (s4_contar, 6)])),
    ]
    body = lesson(
        ["Numa <b>sequência que se repete</b>, uma parte aparece sempre igual: azul, vermelho, azul, vermelho…",
         "Para saber o que vem depois, ache a parte que se repete e continue.",
         "Numa sequência de números, veja quanto muda de um para o outro: de 2 em 2, de 5 em 5, de 10 em 10…",
         "Se os números aumentam, some; se diminuem, tire."],
        [("bola, estrela, bola, estrela, ___", ["repete bola, estrela"], "bola"),
         ("10, 20, 30, 40, ___", ["de 10 em 10"], "50")],
        [["Olhar só a última figura", "Ache a parte que se repete inteira."],
         ["Achar que a parte tem uma figura só", "Ela tem pelo menos duas figuras diferentes."],
         ["Pular errado de 2 em 2 (2, 4, 5)", "Some 2 de cada vez: 2, 4, 6."]],
        padrao([("obj", "ball"), ("obj", "star")] * 2 + [("obj", "ball")], 1))
    faq = [("O que é um padrão?", "É algo que se repete numa ordem, como cores num colar ou palmas numa música. A BNCC pede que o 1º ano descreva sequências que se repetem e descubra o que vem depois."),
           ("Como praticar sequências em casa?", "Monte filas com tampinhas de cores e peça para a criança continuar. Conte de 2 em 2 e de 10 em 10 subindo a escada.")]
    make_unit(R, "sequencias-e-padroes", "A", ["EF01MA10"],
              "Descrever, após o reconhecimento e a explicitação de um padrão (ou regularidade), os elementos ausentes em sequências recursivas de números naturais, objetos ou figuras",
              "Sequências e padrões", "Sequências e padrões",
              "Atividades de matemática para o 1º ano sobre sequências e padrões: figuras que se repetem, o que vem depois, o que falta, contar de 2 em 2, de 5 em 5 e de 10 em 10. 100 exercícios com gabarito.",
              "Ache a parte que se repete.", "Veja quanto muda de um número para o outro.",
              body, faq, sets, 10, grade="1-ano")


if __name__ == "__main__":
    main()
