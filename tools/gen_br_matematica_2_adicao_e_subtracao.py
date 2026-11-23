# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Adição e subtração com conta armada (Números, EF02MA05, EF02MA06)
  python3 tools/gen_br_matematica_2_adicao_e_subtracao.py
Adição e subtração de números de 2 algarismos sem e com reagrupamento («vai um», «empresta um»);
números de 3 algarismos até 999; somar dezenas e unidades separadamente; conferir com a operação inversa.
Usa geradores do 3º ano (adição e subtração) com outro sorteio.
Erros: esquecer o «vai um», tirar o menor do maior em cada ordem (52 − 17 → 45), não alinhar unidades com unidades.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, armada, use, lim

R = random.Random(80206)
L = (lim(999, 0),)
a_sem, a_um = use("gen_br_matematica_3_adicao", 80902, "s1_sem", "s1_um", preds=L)
b_sem, b_um = use("gen_br_matematica_3_subtracao", 80903, "s1_sem", "s1_um", preds=L)


def nc_sum(a, b):
    """soma sem o «vai um»"""
    return int("".join(str((int(x) + int(y)) % 10) for x, y in zip(str(a).rjust(3, "0"), str(b).rjust(3, "0"))))


def nb_sub(a, b):
    """tira o menor do maior em cada ordem"""
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a).rjust(3, "0"), str(b).rjust(3, "0"))))


def s1_soma2(carry):
    while True:
        a, b = R.randint(11, 79), R.randint(11, 59)
        c = (a % 10 + b % 10) >= 10
        if c == carry and a + b < 100:
            break
    s = a + b
    w = [s + 10, s - 10 if carry else s + 1, nc_sum(a, b), s - 1]
    return mcq(armada([str(a), str(b)], "+") + "Quanto é %d + %d?" % (a, b), str(s), [str(x) for x in w if x != s and x > 0],
               ("Unidades: %d + %d = %d, fica %d e <b>vai 1</b> dezena. Dezenas: %d + %d + 1 = %d. Resultado: <b>%d</b>." % (a % 10, b % 10, a % 10 + b % 10, (a + b) % 10, a // 10, b // 10, s // 10, s))
               if carry else "Unidades: %d + %d = %d. Dezenas: %d + %d = %d. Resultado: <b>%d</b>." % (a % 10, b % 10, s % 10, a // 10, b // 10, s // 10, s))


def s1_sem():
    return s1_soma2(False)


def s1_vai():
    return s1_soma2(True)


def s2_sub2(borrow):
    while True:
        a, b = R.randint(31, 99), R.randint(11, 69)
        if a > b + 5 and (a % 10 < b % 10) == borrow:
            break
    d = a - b
    w = [nb_sub(a, b), d + 10, d - 1, d + 1]
    return mcq(armada([str(a), str(b)], "−") + "Quanto é %d − %d?" % (a, b), str(d), [str(x) for x in w if x != d and x > 0],
               ("%d − %d não dá: <b>empresta 1</b> dezena. %d − %d = %d. Dezenas: %d − %d = %d. Resultado: <b>%d</b>." % (a % 10, b % 10, a % 10 + 10, b % 10, d % 10, a // 10 - 1, b // 10, d // 10, d))
               if borrow else "Unidades: %d − %d = %d. Dezenas: %d − %d = %d. Resultado: <b>%d</b>." % (a % 10, b % 10, d % 10, a // 10, b // 10, d // 10, d))


def s2_sem():
    return s2_sub2(False)


def s2_empresta():
    return s2_sub2(True)


def s3_dez_uni():
    a, b = R.randint(12, 68), R.randint(12, 31)
    if a + b >= 100:
        return None
    if R.random() < 0.5:
        return mcq("Calcule %d + %d separando dezenas e unidades: %d + %d = ___ e %d + %d = ___. Qual é o resultado?" % (a, b, a // 10 * 10, b // 10 * 10, a % 10, b % 10),
                   str(a + b), [str(a + b + 10), str(a // 10 * 10 + b // 10 * 10), str(nc_sum(a, b))],
                   "%d + %d = %d e %d + %d = %d. %d + %d = <b>%d</b>." % (a // 10 * 10, b // 10 * 10, a // 10 * 10 + b // 10 * 10, a % 10, b % 10, a % 10 + b % 10, a // 10 * 10 + b // 10 * 10, a % 10 + b % 10, a + b))
    t = R.randint(2, 6) * 10
    return mcq("Calcule %d + %d (dica: some as dezenas)." % (a, t), str(a + t), [str(a + t // 10), str(a + t + 10), str(a + t - 1)],
               "Só as dezenas mudam: <b>%d</b>." % (a + t))


def s4_prova():
    a, b = R.randint(31, 98), R.randint(12, 29)
    if a <= b:
        return None
    d = a - b
    if R.random() < 0.5:
        ok = "%d + %d = %d" % (d, b, a)
        return mcq("Qual conta confere (tira a prova de) %d − %d = %d?" % (a, b, d), ok, ["%d − %d = %d" % (a, d, b), "%d + %d = %d" % (a, b, a + b), "%d + %d = %d" % (d, a, d + a)],
                   "Some o resultado com o número que foi tirado: <b>%s</b>." % ok)
    s = a + b
    ok = "%d − %d = %d" % (s, b, a)
    return mcq("Qual conta confere %d + %d = %d?" % (a, b, s), ok, ["%d + %d = %d" % (s, b, s + b), "%d − %d = %d" % (a, b, a - b), "%d + %d = %d" % (b, a, s + 1)],
               "Do total, tire uma parcela: <b>%s</b>." % ok)


def s5_problema():
    k = R.choice(["alunos", "livros", "figurinhas", "garrafas", "pontos", "frutas"])
    if k == "alunos":
        a, b = R.randint(110, 450), R.randint(110, 450)
        return mcq("Uma escola tem %s alunos de manhã e %s à tarde. Quantos alunos ao todo?" % (num(a), num(b)), num(a + b), [num(a + b + 10), num(a + b - 10), num(nc_sum(a, b)) if nc_sum(a, b) != a + b else num(a + b + 100)],
                   "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "livros":
        a, b = R.randint(250, 900), R.randint(110, 240)
        return mcq("A biblioteca tinha %s livros e emprestou %s. Quantos livros ficaram?" % (num(a), num(b)), num(a - b), [num(a + b), num(nb_sub(a, b)) if nb_sub(a, b) != a - b else num(a - b + 100), num(a - b + 10)],
                   "%s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    a, b = R.randint(23, 78), R.randint(14, 49)
    if k == "figurinhas":
        if a + b >= 100:
            return None
        return mcq("Bia tem %d figurinhas e ganhou %d. Quantas tem agora?" % (a, b), str(a + b), [str(a + b - 10), str(a + b + 10), str(nc_sum(a, b)) if nc_sum(a, b) != a + b else str(a + b + 1)],
                   "%d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "garrafas":
        if a <= b:
            return None
        return mcq("Havia %d garrafas de suco na festa. Foram tomadas %d. Quantas sobraram?" % (a, b), str(a - b), [str(a + b), str(nb_sub(a, b)) if nb_sub(a, b) != a - b else str(a - b + 10), str(a - b - 1)],
                   "%d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "pontos":
        x, y = max(a, b), min(a, b)
        if x == y:
            return None
        return mcq("Num jogo, o time azul fez %d pontos e o vermelho fez %d. Quantos pontos o azul fez a mais?" % (x, y), str(x - y), [str(x + y), str(nb_sub(x, y)) if nb_sub(x, y) != x - y else str(x - y + 10), str(x - y + 1)],
                   "%d − %d = <b>%d</b>." % (x, y, x - y))
    if a + b >= 100:
        return None
    return mcq("Na feira, Davi comprou %d laranjas e %d bananas. Quantas frutas comprou?" % (a, b), str(a + b), [str(a + b + 10), str(nc_sum(a, b)) if nc_sum(a, b) != a + b else str(a + b - 1), str(a - b) if a > b else str(b - a)],
               "%d + %d = <b>%d</b>." % (a, b, a + b))


def main():
    seen = set()
    sets = [
        ("Adição com 2 algarismos", mix(R, seen, [(s1_sem, 8), (s1_vai, 12)])),
        ("Subtração com 2 algarismos", mix(R, seen, [(s2_sem, 8), (s2_empresta, 12)])),
        ("Números de 3 algarismos", mix(R, seen, [(a_sem, 6), (a_um, 4), (b_sem, 6), (b_um, 4)])),
        ("Dezenas e unidades e prova real", mix(R, seen, [(s3_dez_uni, 10), (s4_prova, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Na <b>conta armada</b>, ponha unidades embaixo de unidades e dezenas embaixo de dezenas.",
         "Comece sempre pelas <b>unidades</b>, à direita.",
         "Na adição, se as unidades passam de 9, troque 10 unidades por 1 dezena: <b>vai um</b>.",
         "Na subtração, se não dá para tirar, troque 1 dezena por 10 unidades: <b>empresta um</b>."],
        [("38 + 25", ["8 + 5 = 13: fica 3, vai 1", "3 + 2 + 1 = 6"], "63"),
         ("52 − 17", ["2 − 7 não dá: 12 − 7 = 5", "4 − 1 = 3"], "35")],
        [["Esquecer o «vai um» (38 + 25 = 53)", "Some a dezena que subiu."],
         ["Tirar o menor do maior (52 − 17 = 45)", "Empreste 1 dezena: 12 − 7."],
         ["Não alinhar as ordens", "Unidades embaixo de unidades."]],
        armada(["38", "25"], "+"))
    faq = [("Quando a criança aprende o «vai um»?", "No 2º ano, com números de 2 e 3 algarismos. A BNCC pede problemas de adição e subtração com números de até três ordens, usando estratégias pessoais e a conta armada."),
           ("Como explicar o «empresta um»?", "Use o material dourado ou palitos: troque uma barra (10) por 10 cubinhos para conseguir tirar as unidades.")]
    make_unit(R, "adicao-e-subtracao", "N", ["EF02MA05", "EF02MA06"],
              "Construir fatos básicos da adição e subtração e utilizá-los no cálculo mental ou escrito; resolver e elaborar problemas de adição e de subtração, envolvendo números de até três ordens, com os significados de juntar, acrescentar, separar, retirar, utilizando estratégias pessoais ou convencionais",
              "Adição e subtração com conta armada", "Adição e subtração",
              "Atividades de matemática para o 2º ano sobre adição e subtração com conta armada: números de 2 e 3 algarismos, vai um, empresta um e prova real. 100 exercícios com gabarito.",
              "Comece pelas unidades.", "Vai um na adição, empresta um na subtração.",
              body, faq, sets, 6, grade="2-ano")


if __name__ == "__main__":
    main()
