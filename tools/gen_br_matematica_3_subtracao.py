# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Subtração com reagrupamento (Números, EF03MA05)
  python3 tools/gen_br_matematica_3_subtracao.py
Conta armada com 3 e 4 algarismos, sem e com desagrupamento («empresta um»), zeros no minuendo (700 − 254),
minuendo, subtraendo e diferença, número que falta, prova real pela adição.
Erros: tirar o menor do maior em cada coluna (52 − 38 = 26), esquecer que a dezena emprestada diminuiu, problemas com zero.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, armada, Kids, reais

R = random.Random(80305)
K = Kids(R)


def borrows(a, b):
    out, br = 0, 0
    while a or b:
        d = a % 10 - br - b % 10
        br = 1 if d < 0 else 0
        out += br
        a //= 10
        b //= 10
    return out


def small_from_big(a, b):
    """erro: em cada coluna tira o menor do maior"""
    r, p = 0, 1
    while a or b:
        r += abs(a % 10 - b % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return r


def forgot(a, b):
    """erro: empresta mas não diminui a ordem seguinte"""
    r, p = 0, 1
    while a or b:
        d = a % 10 - b % 10
        r += (d + 10 if d < 0 else d) * p
        a //= 10
        b //= 10
        p *= 10
    return r


def wrong(a, b):
    d = a - b
    return [num(x) for x in (small_from_big(a, b), forgot(a, b), d + 10, d - 10, d + 100, a + b) if x != d and x >= 0]


def pair(lo, hi, nb):
    while True:
        a = R.randint(lo, hi)
        b = R.randint(lo // 2, a - 1)
        if borrows(a, b) == nb:
            return a, b


def s1_sem():
    a, b = pair(300, 999, 0)
    d = a - b
    return mcq(armada([num(a), num(b)], "−") + "Quanto é %s − %s?" % (num(a), num(b)), num(d), [num(d + 10), num(d + 100), num(a + b)],
               "Tire unidades de unidades, dezenas de dezenas, centenas de centenas: <b>%s</b>." % num(d))


def s1_um():
    a, b = pair(300, 999, 1)
    d = a - b
    return mcq(armada([num(a), num(b)], "−") + "Arme e efetue: %s − %s." % (num(a), num(b)), num(d), wrong(a, b),
               "Quando o algarismo de cima é menor, troque 1 da ordem seguinte por 10 («empresta um»): <b>%s</b>." % num(d))


def s2_dois():
    a, b = pair(300, 999, 2)
    d = a - b
    return mcq(armada([num(a), num(b)], "−") + "Quanto é %s − %s?" % (num(a), num(b)), num(d), wrong(a, b),
               "Desagrupe nas unidades e nas dezenas. Resposta: <b>%s</b>." % num(d))


def s2_zero():
    a = R.randint(2, 9) * 100 + R.choice([0, 0, 0, R.randint(1, 9)])
    b = R.randint(101, a - 1)
    if b % 10 == 0 or borrows(a, b) == 0:
        return None
    d = a - b
    return mcq(armada([num(a), num(b)], "−") + "Calcule %s − %s." % (num(a), num(b)), num(d), wrong(a, b),
               "Com zeros em cima, desagrupe 1 centena em 9 dezenas e 10 unidades. Resposta: <b>%s</b>." % num(d))


def s3_quatro():
    a = R.randint(2000, 9999)
    b = R.randint(1000, a - 100)
    if borrows(a, b) == 0:
        return None
    d = a - b
    return mcq(armada([num(a), num(b)], "−") + "Arme e efetue: %s − %s." % (num(a), num(b)), num(d), wrong(a, b) + [num(d + 1000)],
               "Alinhe pela direita e subtraia ordem por ordem, a partir das unidades: <b>%s</b>." % num(d))


def s3_mil():
    a = R.randint(2, 9) * 1000
    b = R.randint(101, 999)
    if b % 10 == 0:
        return None
    d = a - b
    return mcq("Calcule %s − %s." % (num(a), num(b)), num(d), wrong(a, b),
               "%s − %s = <b>%s</b>. Confira: %s + %s = %s." % (num(a), num(b), num(d), num(d), num(b), num(a)))


def s4_falta():
    a = R.randint(500, 9000)
    b = R.randint(100, a - 50)
    d = a - b
    k = R.choice(["sub", "min", "dif"])
    if k == "sub":
        return mcq("Que número falta? %s − ___ = %s" % (num(a), num(d)), num(b), [num(a + d), num(b + 10), num(b - 10)],
                   "O número que falta é %s − %s = <b>%s</b>." % (num(a), num(d), num(b)))
    if k == "min":
        return mcq("Que número falta? ___ − %s = %s" % (num(b), num(d)), num(a), [num(d - b) if d > b else num(b - d), num(a + 10), num(a - 100)],
                   "O número que falta é %s + %s = <b>%s</b>." % (num(d), num(b), num(a)))
    return mcq("Qual é a diferença entre %s e %s?" % (num(a), num(b)), num(d), wrong(a, b),
               "Diferença é o resultado da subtração: %s − %s = <b>%s</b>." % (num(a), num(b), num(d)))


def s4_prova():
    a = R.randint(400, 999)
    b = R.randint(120, a - 50)
    d = a - b
    return mcq("%s − %s = %s. Qual conta serve para conferir (prova real)?" % (num(a), num(b), num(d)), "%s + %s = %s" % (num(d), num(b), num(a)),
               ["%s − %s = %s" % (num(d), num(b), num(abs(d - b))), "%s + %s = %s" % (num(a), num(b), num(a + b)), "%s + %s = %s" % (num(d), num(a), num(d + a))],
               "Na prova real da subtração, some a diferença com o subtraendo: deve dar o minuendo. <b>%s + %s = %s</b>." % (num(d), num(b), num(a)))


def s5_problema():
    k = R.choice(["retirar", "comparar", "completar", "troco", "idade", "estoque"])
    p, _ = K.next()
    if k == "retirar":
        a = R.randint(400, 950)
        b = R.randint(130, a - 50)
        return mcq("Uma padaria fez %s pães. Já vendeu %s. Quantos pães ainda restam?" % (num(a), num(b)), num(a - b), wrong(a, b),
                   "Retirar: %s − %s = <b>%s</b> pães." % (num(a), num(b), num(a - b)))
    if k == "comparar":
        a = R.randint(1200, 4800)
        b = R.randint(500, a - 100)
        return mcq("A biblioteca A tem %s livros e a biblioteca B tem %s. Quantos livros a biblioteca A tem a mais?" % (num(a), num(b)), num(a - b), wrong(a, b),
                   "Comparar: %s − %s = <b>%s</b> livros a mais." % (num(a), num(b), num(a - b)))
    if k == "completar":
        a = R.randint(3, 9) * 100
        b = R.randint(100, a - 30)
        if b % 10 == 0:
            return None
        return mcq("%s quer juntar %s tampinhas. Já tem %s. Quantas faltam?" % (p, num(a), num(b)), num(a - b), wrong(a, b),
                   "Completar: %s − %s = <b>%s</b> tampinhas." % (num(a), num(b), num(a - b)))
    if k == "troco":
        c = R.choice([50, 100, 200])
        v = R.randint(12, c - 3)
        return mcq("%s comprou um jogo de %s e pagou com %s. Quanto recebeu de troco?" % (p, reais(v * 100), reais(c * 100)), reais((c - v) * 100),
                   [reais(x * 100) for x in (small_from_big(c, v), forgot(c, v), c - v + 10, c + v) if x != c - v],
                   "Troco: %d − %d = %d: <b>%s</b>." % (c, v, c - v, reais((c - v) * 100)))
    if k == "idade":
        a = R.randint(2010, 2018)
        b = 2026
        return mcq("Um prédio foi construído em %d. Quantos anos ele faz em %d?" % (a, b), str(b - a), [str(b - a + 1), str(b - a - 1), str(b - a + 10)],
                   "%d − %d = <b>%d</b> anos." % (b, a, b - a))
    a = R.randint(2000, 8000)
    b = R.randint(700, a - 300)
    return mcq("Um depósito tinha %s caixas. Saíram %s caixas num caminhão. Quantas caixas ficaram?" % (num(a), num(b)), num(a - b), wrong(a, b),
               "%s − %s = <b>%s</b> caixas." % (num(a), num(b), num(a - b)))


def main():
    seen = set()
    sets = [
        ("Subtração sem e com «empresta um»", mix(R, seen, [(s1_sem, 8), (s1_um, 12)])),
        ("Desagrupar duas vezes e com zeros", mix(R, seen, [(s2_dois, 12), (s2_zero, 8)])),
        ("Números de 4 algarismos", mix(R, seen, [(s3_quatro, 12), (s3_mil, 8)])),
        ("Número que falta e prova real", mix(R, seen, [(s4_falta, 12), (s4_prova, 8)])),
        ("Problemas de subtração", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Na conta armada, o número maior (<b>minuendo</b>) fica em cima e o que se tira (<b>subtraendo</b>) embaixo, alinhados pela direita. O resultado é a <b>diferença</b>.",
         "Comece pelas unidades. Se o algarismo de cima for menor, <b>desagrupe</b>: troque 1 dezena por 10 unidades (e a dezena de cima diminui 1).",
         "Com zeros em cima, como em 700 − 254, troque 1 centena por 9 dezenas e 10 unidades.",
         "Para conferir, faça a <b>prova real</b>: diferença + subtraendo = minuendo."],
        [("532 − 278", ["2 &lt; 8: desagrupe, 12 − 8 = 4", "Sobram 2 dezenas: 2 &lt; 7, desagrupe, 12 − 7 = 5", "4 − 2 = 2"], "254"),
         ("Prova real de 532 − 278 = 254", ["254 + 278 = 532"], "Está certo")],
        [["Tirar o menor do maior: 532 − 278 = 346", "Se em cima é menor, desagrupe; não troque a ordem dos números."],
         ["Esquecer que a dezena diminuiu", "Risque o algarismo emprestado e escreva o novo valor em cima."],
         ["700 − 254 = 554", "Com zeros, desagrupe a centena: 700 = 6 centenas, 9 dezenas e 10 unidades."]],
        armada(["532", "278"], "−", result="254"))
    faq = [("Qual é a diferença entre «emprestar» e «desagrupar»?", "É a mesma ideia: trocar 1 dezena por 10 unidades (ou 1 centena por 10 dezenas). «Desagrupar» ou «reagrupar» explica melhor o que acontece com os números."),
           ("Como ajudar com subtrações que têm zero?", "Use o material dourado: troque uma placa de 100 por 10 barras e uma barra por 10 cubinhos. A criança vê por que 700 vira 6 centenas, 9 dezenas e 10 unidades.")]
    make_unit(R, "subtracao", "N", ["EF03MA05"],
              "Utilizar diferentes procedimentos de cálculo mental e escrito, inclusive os convencionais, para resolver problemas significativos envolvendo adição e subtração com números naturais",
              "Subtração com reagrupamento: conta armada", "Subtração",
              "Atividades de matemática para o 3º ano sobre subtração: conta armada com e sem desagrupamento, subtração com zeros, números de 4 algarismos, prova real e problemas. 100 exercícios com gabarito.",
              "Em cima menor? Desagrupe 1 da ordem seguinte.", "Prova real: diferença + subtraendo = minuendo.",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
