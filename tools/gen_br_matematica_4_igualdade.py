# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Igualdade e número desconhecido (Álgebra, EF04MA14, EF04MA15)
  python3 tools/gen_br_matematica_4_igualdade.py
A igualdade continua quando somamos ou subtraímos o mesmo número dos dois lados (balança em equilíbrio);
igualdades verdadeiras e compensação (25 + 17 = 27 + 15); número desconhecido nas quatro operações; problemas.
Usa os geradores do 5º ano (sem × e ÷ nos dois lados) e do 3º ano com outro sorteio.
Erros: mudar só um lado, ler o = como «dá o resultado», usar a operação errada para achar o número que falta.
"""
import random
import gen_br_matematica_5_igualdade_e_termo_desconhecido as I5
from br_common import lesson, make_unit, mix, use, lim

R = random.Random(80411)
M5 = "gen_br_matematica_5_igualdade_e_termo_desconhecido"
M3 = "gen_br_matematica_3_igualdade"


def so_ad(it):
    t = it["q"] + it["e"]
    return "×" not in t and "÷" not in t and "dobr" not in t and "tripl" not in t


s_mesmo, s_bal = use(M5, 80951, "s1_mesmo", "s1_balanca", preds=(so_ad,))
s_verdade, s_lado, s_adsub, s_muldiv, s_dupla, s_prob = use(M5, 80951, "s2_verdade", "s2_lado", "s3_adsub", "s4_muldiv", "s4_dupla", "s5_problema", preds=(lim(99999, 0),))
s3_compensa, s3_vf = use(M3, 80952, "s3_compensa", "s2_vf")


def main():
    seen = set()
    sets = [
        ("A igualdade continua", mix(R, seen, [(s_mesmo, 14), (s_bal, 6)])),
        ("Igualdades verdadeiras", mix(R, seen, [(s_verdade, 8), (s3_compensa, 6), (s_lado, 6)])),
        ("Número desconhecido: + e −", mix(R, seen, [(s_adsub, 20)])),
        ("Número desconhecido: × e ÷", mix(R, seen, [(s_muldiv, 14), (s_dupla, 6)])),
        ("Problemas", mix(R, seen, [(s_prob, 20)])),
    ]
    body = lesson(
        ["O sinal <b>=</b> quer dizer que os dois lados têm o <b>mesmo valor</b>, como uma balança em equilíbrio.",
         "Se somamos ou tiramos o <b>mesmo número dos dois lados</b>, a igualdade continua: 12 + 8 = 20, então 12 + 8 + 5 = 20 + 5.",
         "Para achar o número desconhecido, use a operação inversa: em □ + 245 = 600, faça 600 − 245.",
         "Em 25 + 17 = 27 + □, compare: 27 tem 2 a mais que 25, então □ tem 2 a menos que 17."],
        [("□ − 125 = 340", ["a adição desfaz a subtração", "340 + 125"], "465"),
         ("Se 30 + 15 = 45, quanto vale □ em 30 + 15 − 6 = 45 − □?", ["tiramos 6 de um lado", "tiramos 6 do outro"], "6")],
        [["Mudar só um lado da igualdade", "O que você faz de um lado, faça do outro."],
         ["Ler = como «o resultado é»: 8 + 4 = □ + 5 → 12", "Os dois lados valem 12: □ = 7."],
         ["Usar a operação errada: □ − 25 = 40 → 15", "O número que falta é o total: 40 + 25 = 65."]],
        I5.balanca("12 kg + 8 kg", "20 kg"))
    faq = [("O que o 4º ano estuda sobre igualdade?", "A BNCC pede reconhecer que a igualdade continua quando somamos ou subtraímos o mesmo número dos dois lados, e determinar o número desconhecido que torna uma igualdade verdadeira."),
           ("Como explicar o sinal de igual?", "Use a balança: os dois pratos têm o mesmo peso. Se colocar 5 kg num prato, precisa colocar 5 kg no outro para continuar em equilíbrio.")]
    make_unit(R, "igualdade", "A", ["EF04MA14", "EF04MA15"],
              "Reconhecer e mostrar, por meio de exemplos, que a relação de igualdade existente entre dois termos permanece quando se adiciona ou se subtrai um mesmo número a cada um desses termos; determinar o número desconhecido que torna verdadeira uma igualdade que envolve as operações fundamentais com números naturais",
              "Igualdade e número desconhecido: a balança em equilíbrio", "Igualdade",
              "Atividades de matemática para o 4º ano sobre igualdade: a igualdade continua, balança em equilíbrio, igualdades verdadeiras, compensação e número desconhecido nas quatro operações. 100 exercícios com gabarito.",
              "O que você faz de um lado, faça do outro.", "Número desconhecido: use a operação inversa.",
              body, faq, sets, 11, grade="4-ano")


if __name__ == "__main__":
    main()
