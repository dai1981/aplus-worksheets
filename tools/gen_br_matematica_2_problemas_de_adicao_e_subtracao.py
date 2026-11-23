# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Problemas de adição e subtração (Números, EF02MA06)
  python3 tools/gen_br_matematica_2_problemas_de_adicao_e_subtracao.py
Problemas com números até 999 com os significados de juntar, acrescentar, separar e retirar; completar e comparar;
escolher a operação; problemas com números de 2 algarismos e com figuras. Usa geradores do 3º ano com outro sorteio.
Erros: somar quando o problema pede o que sobrou, usar a palavra «mais» como sinal de soma sem ler o problema.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, use, lim, relabel, fig, coisas, COISAS, KINDS, Kids

R = random.Random(80207)
K = Kids(R)
M3 = "gen_br_matematica_3_problemas_de_adicao_e_subtracao"
L = (lim(999, 0),)
p_juntar, p_acresc, p_retirar, p_separar, p_comparar, p_operacao, p_desc = use(M3, 80904, "s1_juntar", "s1_acrescentar", "s2_retirar", "s2_separar", "s3_comparar", "s4_operacao", "s4_desconhecido", preds=L)


def s1_figura():
    kind = R.choice(KINDS)
    n, k = R.randint(7, 15), R.randint(2, 6)
    if k >= n:
        return None
    svg = k_pics.crossed_row_svg(n, kind, k, per_row=8)
    pic = fig(relabel(svg, "%s, %d riscadas" % (coisas(kind, n), k) if COISAS[kind][2] == "f" else "%s, %d riscados" % (coisas(kind, n), k)))
    nm, f = COISAS[kind][1], COISAS[kind][2] == "f"
    return mcq(pic + "Havia %d %s. %s foram tirad%ss. %s ficaram?" % (n, nm, "As riscadas" if f else "Os riscados", "a" if f else "o", "Quantas" if f else "Quantos"),
               str(n - k), [str(n + k), str(k), str(n - k + 1)], "Retirar: %d − %d = <b>%d</b>." % (n, k, n - k))


def s2_dois_digitos():
    (p, g), (q, g2) = K.two()
    a, b = R.randint(15, 68), R.randint(12, 31)
    k = R.choice(["junta", "acr", "ret", "sep"])
    if k == "junta":
        if a + b > 99:
            return None
        return mcq("%s tem %d bolinhas de gude e %s tem %d. Quantas bolinhas há ao todo?" % (p, a, q, b), str(a + b), [str(a - b), str(a + b + 10), str(a + b - 1)],
                   "Juntar: %d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "acr":
        if a + b > 99:
            return None
        return mcq("Um ônibus tinha %d passageiros. No ponto subiram %d. Quantos passageiros há agora?" % (a, b), str(a + b), [str(a - b), str(a + b + 1), str(a + b - 10)],
                   "Acrescentar: %d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "ret":
        if a <= b:
            return None
        return mcq("%s tinha %d reais. Gastou %d reais num livro. Quantos reais sobraram?" % (p, a, b), str(a - b), [str(a + b), str(a - b + 10), str(b)],
                   "Retirar: %d − %d = <b>%d</b>." % (a, b, a - b))
    a, b = R.randint(22, 35), R.randint(9, 17)
    return mcq("Numa sala há %d crianças. %d são meninas. Quantos são meninos?" % (a, b), str(a - b), [str(a + b), str(b), str(a - b - 1)],
               "Separar: %d − %d = <b>%d</b>." % (a, b, a - b))


def main():
    seen = set()
    sets = [
        ("Juntar e acrescentar", mix(R, seen, [(p_juntar, 8), (p_acresc, 8), (s2_dois_digitos, 4)])),
        ("Retirar e separar", mix(R, seen, [(p_retirar, 7), (p_separar, 7), (s1_figura, 6)])),
        ("Problemas com números de 2 algarismos", mix(R, seen, [(s2_dois_digitos, 14), (s1_figura, 6)])),
        ("Qual é a conta?", mix(R, seen, [(p_operacao, 12), (p_desc, 8)])),
        ("Comparar e completar", mix(R, seen, [(p_comparar, 12), (p_juntar, 4), (p_retirar, 4)])),
    ]
    body = lesson(
        ["Leia o problema e pense: as quantidades vão <b>juntar</b> ou <b>aumentar</b>? Então é adição.",
         "Uma parte vai <b>sair</b> ou <b>ser separada</b>? Então é subtração.",
         "Para saber quantos <b>a mais</b> ou quanto <b>falta</b>, tire o menor do maior.",
         "Escreva a conta, resolva e responda com uma frase: «Sobraram 23 balas»."],
        [("Tinha 45 figurinhas e deu 18", ["sair → subtração", "45 − 18"], "27 figurinhas"),
         ("Na sala há 12 meninas e 15 meninos", ["juntar → adição", "12 + 15"], "27 crianças")],
        [["Somar quando o problema pede o que sobrou", "«Sobrou» e «ficou» depois de sair pedem subtração."],
         ["Ver a palavra «mais» e sempre somar", "«Quantos a mais» pede subtração."],
         ["Responder só o número", "Diga também o que é: 27 figurinhas."]],
        fig(relabel(k_pics.crossed_row_svg(10, "apple", 3, per_row=10), "10 maçãs, 3 riscadas")))
    faq = [("Que problemas de adição e subtração o 2º ano resolve?", "A BNCC pede problemas com números de até três ordens com os significados de juntar, acrescentar, separar e retirar, usando estratégias pessoais ou convencionais."),
           ("Como ajudar a criança a escolher a conta?", "Peça que ela conte o problema com as próprias palavras ou faça um desenho. Pergunte: a quantidade aumentou ou diminuiu?")]
    make_unit(R, "problemas-de-adicao-e-subtracao", "N", ["EF02MA06"],
              "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até três ordens, com os significados de juntar, acrescentar, separar, retirar, utilizando estratégias pessoais",
              "Problemas de adição e subtração", "Problemas de adição e subtração",
              "Atividades de matemática para o 2º ano com problemas de adição e subtração: juntar, acrescentar, separar, retirar, comparar e completar, com números até 999. 100 exercícios com gabarito.",
              "Junta ou aumenta: adição. Sai ou separa: subtração.", "Quantos a mais: tire o menor do maior.",
              body, faq, sets, 7, grade="2-ano")


if __name__ == "__main__":
    main()
