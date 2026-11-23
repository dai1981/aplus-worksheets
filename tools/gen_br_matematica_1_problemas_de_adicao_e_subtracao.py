# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Problemas de adição e subtração (Números, EF01MA08)
  python3 tools/gen_br_matematica_1_problemas_de_adicao_e_subtracao.py
Problemas com números até 99 com os significados de juntar, acrescentar, separar e retirar; problemas com figuras;
dezenas exatas (30 + 20); quanto falta. Usa geradores do 2º e do 3º ano com outro sorteio.
Erros: escolher a conta pela palavra «mais», responder sem a unidade, somar dezenas com unidades (30 + 4 = 70).
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim, Kids
from br_1 import riscados

R = random.Random(80108)
K = Kids(R)
L = (lim(99, 0),)
p_fig, p_dois = use("gen_br_matematica_2_problemas_de_adicao_e_subtracao", 80973, "s1_figura", "s2_dois_digitos", preds=L)
p_juntar, p_retirar = use("gen_br_matematica_3_problemas_de_adicao_e_subtracao", 80974, "s1_juntar", "s2_retirar", preds=L)


def s1_juntar():
    a, b = R.randint(2, 12), R.randint(2, 9)
    (p, g), (q, g2) = K.two()
    t = R.choice(["%s tem %d carrinhos e %s tem %d. Quantos carrinhos há ao todo?", "%s pegou %d conchas e %s pegou %d. Quantas conchas foram pegas ao todo?",
                  "%s plantou %d flores e %s plantou %d. Quantas flores foram plantadas?"])
    return mcq(t % (p, a, q, b), str(a + b), [str(a + b + 1), str(abs(a - b)) if a != b else str(a + b - 1), str(a + b + 10)], "Juntar: %d + %d = <b>%d</b>." % (a, b, a + b))


def s2_dezenas():
    a, b = R.randint(1, 7), R.randint(1, 5)
    if a + b > 9:
        return None
    if R.random() < 0.5:
        return mcq("Lia tem %d reais e ganhou %d reais. Com quantos reais ficou?" % (10 * a, 10 * b), "%d reais" % (10 * (a + b)), ["%d reais" % (a + b), "%d reais" % (10 * (a + b) + 10), "%d reais" % (10 * abs(a - b)) if a != b else "%d reais" % (10 * a)],
                   "%d dezenas + %d dezenas = %d dezenas: <b>%d reais</b>." % (a, b, a + b, 10 * (a + b)))
    s = a + b
    return mcq("Havia %d laranjas na banca. Venderam %d. Quantas sobraram?" % (10 * s, 10 * a), str(10 * b), [str(b), str(10 * s + 10 * a) if s + a <= 9 else str(10 * b + 10), str(10 * b - 10) if b > 1 else str(20)],
               "%d − %d = <b>%d</b>." % (10 * s, 10 * a, 10 * b))


def s2_dez_e_un():
    a, b = R.randint(2, 8) * 10, R.randint(1, 9)
    return mcq("Davi tem %d figurinhas no álbum e %d soltas. Quantas figurinhas ele tem?" % (a, b), str(a + b), [str(a // 10 + b), str(a + b * 10) if a + b * 10 < 100 else str(a + b + 1), str(a + b + 10)],
               "%d + %d = <b>%d</b> (as dezenas ficam, as unidades se juntam)." % (a, b, a + b))


FALTA = ["{p} tem {a} reais. Quer comprar uma bola de {t} reais. Quantos reais faltam?",
         "{p} já leu {a} páginas de um livro de {t} páginas. Quantas páginas faltam?",
         "Para completar a página do álbum, {p} precisa de {t} figurinhas. Já tem {a}. Quantas faltam?",
         "Na fila do brinquedo cabem {t} crianças. Já entraram {a}. Quantas ainda cabem?"]


def s3_falta():
    a = R.randint(3, 15)
    t = a + R.randint(2, 9)
    p, _ = K.next()
    q = R.choice(FALTA).format(p=p, a=a, t=t)
    return mcq(q, str(t - a), [str(t + a), str(t), str(t - a + 1)], "%d + ___ = %d. Faltam <b>%d</b>." % (a, t, t - a))


def s4_riscar():
    n = R.randint(8, 20)
    k = R.randint(2, n - 2)
    return mcq(riscados(n, "apple", k) + "Na cesta havia %d maçãs. As riscadas foram comidas. Quantas sobraram?" % n, str(n - k), [str(n + k), str(k), str(n - k + 1)],
               "%d − %d = <b>%d</b>." % (n, k, n - k))


def main():
    seen = set()
    sets = [
        ("Juntar e acrescentar", mix(R, seen, [(s1_juntar, 12), (p_juntar, 8)])),
        ("Separar e retirar", mix(R, seen, [(s4_riscar, 8), (p_fig, 6), (p_retirar, 6)])),
        ("Dezenas e unidades", mix(R, seen, [(s2_dezenas, 12), (s2_dez_e_un, 8)])),
        ("Quanto falta?", mix(R, seen, [(s3_falta, 20)])),
        ("Problemas com números maiores", mix(R, seen, [(p_dois, 20)])),
    ]
    body = lesson(
        ["Leia o problema e pense: as quantidades vão <b>juntar</b> ou <b>aumentar</b>? Então some.",
         "Uma parte vai <b>sair</b> (comer, perder, vender, dar)? Então subtraia.",
         "Para saber quanto <b>falta</b>, conte do número menor até o maior.",
         "Com dezenas exatas, use os fatos básicos: 30 + 20 é como 3 + 2 dezenas = 50."],
        [("Tinha 8 balas e ganhou 5", ["aumentou → +", "8 + 5"], "13 balas"),
         ("Tem 7 reais e a bola custa 12", ["7 + ___ = 12"], "faltam 5 reais")],
        [["Escolher a conta só pela palavra «mais»", "Pense no que acontece na história."],
         ["Responder só o número", "Diga o que é: 13 balas."],
         ["Somar dezenas com unidades: 30 + 4 = 70", "30 + 4 = 34."]],
        riscados(10, "apple", 4))
    faq = [("Que problemas o 1º ano resolve?", "A BNCC pede problemas de adição e subtração com números de até dois algarismos, com os sentidos de juntar, acrescentar, separar e retirar, usando desenhos, materiais e estratégias pessoais."),
           ("Como ajudar a criança a entender o problema?", "Peça que ela conte a história com objetos ou faça um desenho. Pergunte: no fim, ficou mais ou ficou menos?")]
    make_unit(R, "problemas-de-adicao-e-subtracao", "N", ["EF01MA08"],
              "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até dois algarismos, com os significados de juntar, acrescentar, separar e retirar, com o suporte de imagens e/ou material manipulável, utilizando estratégias e formas de registro pessoais",
              "Problemas de adição e subtração", "Problemas de adição e subtração",
              "Atividades de matemática para o 1º ano com problemas de adição e subtração: juntar, acrescentar, separar, retirar, dezenas exatas e quanto falta. 100 exercícios com gabarito.",
              "Junta ou aumenta: some. Sai: subtraia.", "Quanto falta: conte do menor até o maior.",
              body, faq, sets, 8, grade="1-ano")


if __name__ == "__main__":
    main()
