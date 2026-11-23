# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Adição e subtração até 20 (Números, EF01MA06, EF01MA08)
  python3 tools/gen_br_matematica_1_adicao_e_subtracao_ate_20.py
Subtrair riscando figuras; tirar e ver quanto sobra; contar para trás; subtração pela adição (12 − 5: 5 + ? = 12);
família de fatos; adição ou subtração? Usa geradores do 2º ano (fatos básicos) com outro sorteio.
Erros: somar quando é para tirar, contar o número de partida ao contar para trás, tirar o maior do menor.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim, KINDS
from br_1 import riscados, nome, quantos, fem

R = random.Random(80107)
M2 = "gen_br_matematica_2_fatos_basicos_de_adicao_e_subtracao"
f_sub, f_familia, f_falta = use(M2, 80972, "s1_sub", "s3_familia", "s3_falta", preds=(lim(20, 0),))


def s1_riscar():
    kind = R.choice(KINDS)
    n = R.randint(4, 15)
    k = R.randint(1, n - 1)
    return mcq(riscados(n, kind, k) + "Havia %d %s. Tiramos %s. %s ficaram?" % (n, nome(kind), "as riscadas" if fem(kind) else "os riscados", quantos(kind)),
               str(n - k), [str(n + k), str(k), str(n - k + 1)], "%d − %d = <b>%d</b>." % (n, k, n - k))


def s1_tirar():
    n = R.randint(5, 20)
    k = R.randint(1, min(9, n - 1))
    q, a, b = R.choice([("Havia %d passarinhos no fio. Voaram %d. Quantos ficaram?", "passarinhos", ""),
                        ("Ana tinha %d balas. Comeu %d. Com quantas ficou?", "balas", ""),
                        ("No ônibus havia %d pessoas. Desceram %d. Quantas ficaram?", "pessoas", ""),
                        ("Rui tinha %d bolinhas de gude. Perdeu %d. Com quantas ficou?", "bolinhas", ""),
                        ("Havia %d biscoitos no pote. Lia pegou %d. Quantos sobraram?", "biscoitos", "")])
    return mcq(q % (n, k), str(n - k), [str(n + k), str(n - k + 1), str(n - k - 1) if n - k > 1 else str(k)], "%d − %d = <b>%d</b>." % (n, k, n - k))


def s2_tras():
    n = R.randint(6, 20)
    k = R.randint(1, 4)
    return mcq("Calcule %d − %d contando para trás." % (n, k), str(n - k), [str(n - k + 1), str(n - k - 1), str(n + k)],
               "Comece no %d e volte %d: %s. Resposta: <b>%d</b>." % (n, k, ", ".join(str(n - i) for i in range(1, k + 1)), n - k))


def s3_qual():
    a, b = R.randint(2, 9), R.randint(2, 9)
    k = R.choice(["+", "−"])
    if k == "+":
        q = R.choice(["Lia tinha %d figurinhas e ganhou %d. Que conta mostra com quantas ficou?", "Num vaso há %d flores. Puseram mais %d. Que conta mostra quantas há agora?"]) % (a, b)
        ok = "%d + %d" % (a, b)
        return mcq(q, ok, ["%d − %d" % (max(a, b), min(a, b)), "%d + %d" % (a, b + 1), "%d − %d" % (a + b, a)], "Ganhar e pôr mais é juntar: <b>%s</b>." % ok)
    s = a + b
    q = R.choice(["Havia %d maçãs. Comeram %d. Que conta mostra quantas sobraram?", "Davi tinha %d lápis e deu %d. Que conta mostra com quantos ficou?"]) % (s, a)
    ok = "%d − %d" % (s, a)
    return mcq(q, ok, ["%d + %d" % (s, a), "%d − %d" % (a, s) if a != s else "%d − %d" % (s, b), "%d + %d" % (a, b)], "Comer e dar é tirar: <b>%s</b>." % ok)


def main():
    seen = set()
    sets = [
        ("Tirar e riscar", mix(R, seen, [(s1_riscar, 14), (s2_tras, 6)])),
        ("Contar para trás", mix(R, seen, [(s2_tras, 10), (f_sub, 10)])),
        ("Família de fatos", mix(R, seen, [(f_familia, 12), (f_falta, 8)])),
        ("Somar ou tirar?", mix(R, seen, [(s3_qual, 20)])),
        ("Problemas", mix(R, seen, [(s1_tirar, 20)])),
    ]
    body = lesson(
        ["Subtrair é <b>tirar</b>: 7 bolas, tiro 3, ficam 4. Escrevemos 7 − 3 = 4.",
         "Para tirar pouco, conte <b>para trás</b>: 12 − 3 → 11, 10, 9.",
         "Use a adição para subtrair: 12 − 5 = ? porque 5 + 7 = 12.",
         "Se a quantidade aumenta, use +. Se diminui, use −."],
        [("15 − 2", ["volte 2: 14, 13"], "13"),
         ("9 − 4", ["4 + 5 = 9"], "5")],
        [["Somar quando é para tirar", "Comeu, perdeu, deu, voou: tire."],
         ["Contar o número de partida", "Em 12 − 3, comece a voltar no 11."],
         ["Tirar o maior do menor", "Na subtração, o número maior vem primeiro."]],
        riscados(9, "apple", 3))
    faq = [("Como ensinar subtração no 1º ano?", "Com objetos: ponha 8 tampinhas, tire 3 e conte as que ficam. A BNCC pede problemas de adição e subtração com os sentidos de juntar, acrescentar, separar e retirar."),
           ("Qual é a relação entre adição e subtração?", "Uma desfaz a outra: 5 + 3 = 8, então 8 − 3 = 5 e 8 − 5 = 3. É a família de fatos.")]
    make_unit(R, "adicao-e-subtracao-ate-20", "N", ["EF01MA06", "EF01MA08"],
              "Construir fatos básicos da adição e utilizá-los em procedimentos de cálculo para resolver problemas; resolver e elaborar problemas de adição e de subtração, envolvendo números de até dois algarismos, com os significados de juntar, acrescentar, separar e retirar",
              "Adição e subtração até 20", "Adição e subtração até 20",
              "Atividades de matemática para o 1º ano sobre adição e subtração até 20: tirar e riscar, contar para trás, família de fatos, somar ou tirar. 100 exercícios com gabarito.",
              "Subtrair é tirar.", "12 − 5 = 7 porque 5 + 7 = 12.",
              body, faq, sets, 7, grade="1-ano")


if __name__ == "__main__":
    main()
