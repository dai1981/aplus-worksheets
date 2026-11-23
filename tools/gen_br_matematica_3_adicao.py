# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Adição com reagrupamento (Números, EF03MA05)
  python3 tools/gen_br_matematica_3_adicao.py
Conta armada (algoritmo) com 3 e 4 algarismos, com e sem reagrupamento («vai um»), parcelas e soma,
três parcelas, algarismo que falta, propriedade comutativa, prova da adição pela subtração.
Erros: esquecer o «vai um», alinhar os números pela esquerda, somar o «vai um» duas vezes.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, armada, Kids, pl

R = random.Random(80304)
K = Kids(R)


def carries(a, b):
    c, k, out = 0, 0, 0
    while a or b:
        s = a % 10 + b % 10 + c
        c = 1 if s >= 10 else 0
        out += c
        a //= 10
        b //= 10
    return out


def no_carry_sum(a, b):
    """erro: esquece o «vai um»"""
    r, p = 0, 1
    while a or b:
        r += ((a % 10 + b % 10) % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return r


def wrong(a, b):
    s = a + b
    return [num(x) for x in (no_carry_sum(a, b), s + 10, s - 10, s + 100, s + 1) if x != s and x > 0]


def s1_sem():
    while True:
        a, b = R.randint(100, 899), R.randint(100, 899)
        if carries(a, b) == 0 and a + b < 1000:
            break
    s = a + b
    return mcq(armada([num(a), num(b)], "+") + "Quanto é %s + %s?" % (num(a), num(b)), num(s), [num(s + 10), num(s + 100), num(s - 1)],
               "Some unidades, dezenas e centenas: <b>%s</b>." % num(s))


def s1_um():
    while True:
        a, b = R.randint(100, 899), R.randint(100, 899)
        if carries(a, b) == 1 and a + b < 1000:
            break
    s = a + b
    return mcq(armada([num(a), num(b)], "+") + "Arme e efetue: %s + %s." % (num(a), num(b)), num(s), wrong(a, b),
               "Quando a soma de uma ordem passa de 9, troque 10 por 1 da ordem seguinte («vai um»): <b>%s</b>." % num(s))


def s2_dois():
    while True:
        a, b = R.randint(150, 899), R.randint(150, 899)
        if carries(a, b) >= 2:
            break
    s = a + b
    return mcq(armada([num(a), num(b)], "+") + "Quanto é %s + %s?" % (num(a), num(b)), num(s), wrong(a, b),
               "Unidades e dezenas passam de 9: «vai um» duas vezes. Resposta: <b>%s</b>." % num(s))


def s3_quatro():
    while True:
        a, b = R.randint(1000, 6999), R.randint(100, 2999)
        if carries(a, b) >= 1 and a + b < 10000:
            break
    s = a + b
    return mcq(armada([num(a), num(b)], "+") + "Arme e efetue: %s + %s." % (num(a), num(b)), num(s), wrong(a, b) + [num(s + 1000)],
               "Alinhe pela direita (unidade embaixo de unidade) e some cada ordem: <b>%s</b>." % num(s))


def s3_tres():
    a, b, c = R.randint(100, 499), R.randint(100, 399), R.randint(10, 199)
    s = a + b + c
    return mcq(armada([num(a), num(b), num(c)], "+") + "Some as três parcelas: %s + %s + %s." % (num(a), num(b), num(c)), num(s),
               [num(s + 10), num(s - 10), num(no_carry_sum(no_carry_sum(a, b), c)), num(a + b)],
               "Some primeiro as unidades das três parcelas, depois as dezenas e as centenas: <b>%s</b>." % num(s))


def s4_falta():
    a = R.randint(1000, 4999)
    b = R.randint(1000, 4999)
    s = a + b
    k = R.choice(["s", "a"])
    if k == "s":
        return mcq("Qual parcela falta? %s + ___ = %s" % (num(a), num(s)), num(b), [num(s + a), num(b + 10), num(b - 100)],
                   "A parcela que falta é a soma menos a outra parcela: %s − %s = <b>%s</b>." % (num(s), num(a), num(b)))
    return mcq("Qual é a soma de %s e %s?" % (num(a), num(b)), num(s), wrong(a, b), "%s + %s = <b>%s</b>." % (num(a), num(b), num(s)))


def s4_prop():
    a, b = R.randint(120, 880), R.randint(120, 880)
    k = R.choice(["com", "prova"])
    s = a + b
    if k == "com":
        return mcq("Sabendo que %s + %s = %s, quanto é %s + %s?" % (num(a), num(b), num(s), num(b), num(a)), num(s), [num(s + 1), num(a - b) if a > b else num(b - a), num(s + 10)],
                   "A ordem das parcelas não altera a soma (propriedade comutativa): <b>%s</b>." % num(s))
    return mcq("%s + %s = %s. Qual conta serve para conferir (prova real)?" % (num(a), num(b), num(s)), "%s − %s = %s" % (num(s), num(b), num(a)),
               ["%s − %s = %s" % (num(a), num(b), num(abs(a - b))), "%s + %s = %s" % (num(s), num(b), num(s + b)), "%s − %s = %s" % (num(b), num(a), num(abs(b - a)))],
               "Na prova real da adição, tire uma parcela da soma: deve dar a outra parcela. <b>%s − %s = %s</b>." % (num(s), num(b), num(a)))


def s5_problema():
    k = R.choice(["escola", "loja", "viagem", "doacao", "show", "fazenda"])
    p, _ = K.next()
    if k == "escola":
        a, b = R.randint(250, 480), R.randint(250, 480)
        return mcq("Uma escola tem %s alunos de manhã e %s à tarde. Quantos alunos tem ao todo?" % (num(a), num(b)), num(a + b), wrong(a, b),
                   "Juntar: %s + %s = <b>%s</b> alunos." % (num(a), num(b), num(a + b)))
    if k == "loja":
        a, b = R.randint(120, 690), R.randint(150, 890)
        return mcq("Uma loja vendeu %s camisetas em maio e %s em junho. Quantas camisetas vendeu nos dois meses?" % (num(a), num(b)), num(a + b), wrong(a, b),
                   "%s + %s = <b>%s</b> camisetas." % (num(a), num(b), num(a + b)))
    if k == "viagem":
        a, b = R.randint(180, 790), R.randint(180, 790)
        return mcq("Numa viagem, a família %s andou %s km no primeiro dia e %s km no segundo. Quantos quilômetros andou?" % (R.choice(["Silva", "Souza", "Oliveira", "Santos", "Costa"]), num(a), num(b)),
                   "%s km" % num(a + b), ["%s km" % x for x in wrong(a, b)],
                   "%s + %s = <b>%s km</b>." % (num(a), num(b), num(a + b)))
    if k == "doacao":
        a, b, c = R.randint(120, 380), R.randint(120, 380), R.randint(120, 380)
        return mcq("Numa campanha, o 1º ano doou %s brinquedos, o 2º ano doou %s e o 3º ano doou %s. Quantos brinquedos foram doados?" % (num(a), num(b), num(c)),
                   num(a + b + c), [num(a + b), num(a + b + c + 10), num(a + b + c - 100)],
                   "%s + %s + %s = <b>%s</b>." % (num(a), num(b), num(c), num(a + b + c)))
    if k == "show":
        a, b = R.randint(1200, 4800), R.randint(1200, 4800)
        return mcq("No sábado, %s pessoas foram ao show. No domingo, foram %s. Quantas pessoas foram nos dois dias?" % (num(a), num(b)), num(a + b), wrong(a, b),
                   "%s + %s = <b>%s</b> pessoas." % (num(a), num(b), num(a + b)))
    a, b = R.randint(1500, 5900), R.randint(250, 950)
    return mcq("Uma fazenda tinha %s pés de café e plantou mais %s. Quantos pés de café tem agora?" % (num(a), num(b)), num(a + b), wrong(a, b),
               "Acrescentar: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def main():
    seen = set()
    sets = [
        ("Adição sem e com «vai um»", mix(R, seen, [(s1_sem, 8), (s1_um, 12)])),
        ("Reagrupar duas vezes", mix(R, seen, [(s2_dois, 20)])),
        ("Números maiores e três parcelas", mix(R, seen, [(s3_quatro, 12), (s3_tres, 8)])),
        ("Parcela que falta e prova real", mix(R, seen, [(s4_falta, 10), (s4_prop, 10)])),
        ("Problemas de adição", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Na conta armada, escreva os números um embaixo do outro, <b>alinhados pela direita</b>: unidade embaixo de unidade, dezena embaixo de dezena.",
         "Some começando pelas <b>unidades</b>. Se a soma passar de 9, escreva as unidades e leve 1 dezena para a ordem seguinte («vai um»).",
         "Os números que somamos são as <b>parcelas</b>; o resultado é a <b>soma</b> (ou total).",
         "Para conferir, faça a <b>prova real</b>: soma − uma parcela = a outra parcela."],
        [("458 + 375", ["8 + 5 = 13: escreve 3, vai 1", "5 + 7 + 1 = 13: escreve 3, vai 1", "4 + 3 + 1 = 8"], "833"),
         ("Prova real de 458 + 375 = 833", ["833 − 375 = 458"], "Está certo")],
        [["Esquecer o «vai um»: 458 + 375 = 723", "Escreva o 1 em cima da ordem seguinte para não esquecer."],
         ["Alinhar pela esquerda", "Alinhe sempre pela direita: as unidades ficam na mesma coluna."],
         ["Somar o «vai um» duas vezes", "Some o 1 uma vez só, na ordem seguinte."]],
        armada(["458", "375"], "+", result="833"))
    faq = [("O que é reagrupamento na adição?", "É a troca de 10 unidades por 1 dezena (ou 10 dezenas por 1 centena) quando a soma de uma ordem passa de 9. Muita gente chama de «vai um»."),
           ("Por que ensinar a prova real?", "Porque a criança aprende que a subtração desfaz a adição e ganha um jeito de conferir sozinha o próprio resultado.")]
    make_unit(R, "adicao", "N", ["EF03MA05"],
              "Utilizar diferentes procedimentos de cálculo mental e escrito, inclusive os convencionais, para resolver problemas significativos envolvendo adição e subtração com números naturais",
              "Adição com reagrupamento: conta armada", "Adição",
              "Atividades de matemática para o 3º ano sobre adição: conta armada com e sem reagrupamento («vai um»), números de 3 e 4 algarismos, três parcelas, prova real e problemas. 100 exercícios com gabarito.",
              "Alinhe pela direita e some a partir das unidades.", "Passou de 9: escreve as unidades e vai um.",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
