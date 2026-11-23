# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Frações equivalentes (Números, EF05MA04)
  python3 tools/gen_br_matematica_5_fracoes_equivalentes.py
Frações equivalentes com figuras; multiplicar ou dividir numerador e denominador pelo mesmo número;
termo que falta; simplificar até a fração irredutível; reconhecer frações equivalentes; problemas.
Erros: somar o mesmo número aos dois termos, multiplicar só o numerador, achar que frações com números maiores são maiores.
"""
import random
from math import gcd
from br_common import mcq, lesson, make_unit, mix, fr, faixa, Kids

R = random.Random(80504)
K = Kids(R)


def base():
    b = R.choice([2, 3, 4, 5, 6])
    a = R.randint(1, b - 1)
    if gcd(a, b) > 1:
        return None
    return a, b


def s1_figura():
    ab = base()
    if not ab:
        return None
    a, b = ab
    m = R.choice([2, 3, 4])
    if b * m > 12:
        return None
    pic = faixa(b, a) + faixa(b * m, a * m)
    return mcq(pic + "As duas faixas são do mesmo tamanho e têm a mesma parte pintada. Complete: %s = ?/%d" % (fr(a, b), b * m), str(a * m),
               [str(a + b * m - b), str(a), str(b * m - a * m), str(a * m + 1), str(b * m), str(a * m - 1) if a * m > 2 else str(a * m + 2)],
               "A segunda faixa tem %d vezes mais partes, então também tem %d vezes mais partes pintadas: %s = <b>%s</b>." % (m, m, fr(a, b), fr(a * m, b * m)))


def s1_qual():
    ab = base()
    if not ab:
        return None
    a, b = ab
    m = R.choice([2, 3])
    if b * m > 12:
        return None
    w = [(a + 1, b * m), (a * m, b * m + 1) if b * m + 1 <= 12 else (a * m - 1, b * m), (a + m, b + m), (a, b * m), (b * m - a * m, b * m), (a * m + 1, b * m)]
    opts = [(a * m, b * m)] + [x for x in w if x[0] < x[1] and x != (a * m, b * m) and x[0] * b != x[1] * a]
    if len(opts) < 3:
        return None
    return mcq(faixa(b, a) + "Que faixa tem a mesma parte pintada que esta? (fração equivalente a %s)" % fr(a, b), fr(a * m, b * m), [fr(*x) for x in opts[1:]],
               "Multiplicando numerador e denominador por %d: %s = <b>%s</b>." % (m, fr(a, b), fr(a * m, b * m)))


def s2_falta():
    ab = base()
    if not ab:
        return None
    a, b = ab
    m = R.randint(2, 9)
    k = R.choice(["num", "den", "num"])
    if k == "num":
        return mcq("Complete: %s = ?/%d" % (fr(a, b), b * m), str(a * m), [str(a + b * m - b), str(a), str(a * m + m), str(b * m - a * m), str(a * m + 1), str(b * m)],
                   "%d × %d = %d, então o numerador também é multiplicado por %d: %d × %d = <b>%d</b>." % (b, m, b * m, m, a, m, a * m))
    return mcq("Complete: %s = %d/?" % (fr(a, b), a * m), str(b * m), [str(b + a * m - a), str(b), str(b * m + m), str(a * m + 1), str(b * m - 1), str(b * m + 1)],
               "%d × %d = %d, então o denominador também é multiplicado por %d: %d × %d = <b>%d</b>." % (a, m, a * m, m, b, m, b * m))


def s2_mult():
    ab = base()
    if not ab:
        return None
    a, b = ab
    m = R.randint(2, 10)
    return mcq("Multiplique o numerador e o denominador de %s por %d. Que fração você obtém?" % (fr(a, b), m), fr(a * m, b * m),
               [fr(a * m, b), fr(a + m, b + m), fr(a, b * m), fr(a * m, b + m)],
               "%d × %d = %d e %d × %d = %d: <b>%s</b>, equivalente a %s." % (a, m, a * m, b, m, b * m, fr(a * m, b * m), fr(a, b)))


def s3_simplificar():
    ab = base()
    if not ab:
        return None
    a, b = ab
    m = R.randint(2, 9)
    A, B = a * m, b * m
    sub = [d for d in range(2, m) if m % d == 0]
    w = [fr(A // sub[0], B // sub[0]) if sub else None, fr(A - 1, B - 1) if A > 1 else None, fr(b, a) if a > 1 else fr(a, b + 1), fr(A // 2, B) if A % 2 == 0 else fr(a, B), fr(a + 1, b)]
    return mcq("Simplifique %s até a fração irredutível." % fr(A, B), fr(a, b), w,
               "%d e %d podem ser divididos por %d: %d ÷ %d = %d e %d ÷ %d = %d. <b>%s</b> não pode mais ser simplificada." % (A, B, m, A, m, a, B, m, b, fr(a, b)))


def s3_irredutivel():
    fs = []
    while len(fs) < 4:
        b = R.randint(4, 15)
        a = R.randint(1, b - 1)
        if (a, b) not in fs:
            fs.append((a, b))
    irr = [x for x in fs if gcd(*x) == 1]
    red = [x for x in fs if gcd(*x) > 1]
    if R.random() < 0.5:
        if len(irr) != 1:
            return None
        return mcq("Qual destas frações já é irredutível? %s" % ", ".join(fr(*x) for x in fs), fr(*irr[0]), [fr(*x) for x in red],
                   "%s: %d e %d só podem ser divididos juntos por 1. As outras podem ser simplificadas. Resposta: <b>%s</b>." % (fr(*irr[0]), irr[0][0], irr[0][1], fr(*irr[0])))
    if len(red) != 1:
        return None
    a, b = red[0]
    g = gcd(a, b)
    return mcq("Qual destas frações ainda pode ser simplificada? %s" % ", ".join(fr(*x) for x in fs), fr(a, b), [fr(*x) for x in irr],
               "%d e %d podem ser divididos por %d: %s = %s. Resposta: <b>%s</b>." % (a, b, g, fr(a, b), fr(a // g, b // g), fr(a, b)))


def s4_sao():
    ab = base()
    if not ab:
        return None
    a, b = ab
    m = R.randint(2, 6)
    k = R.choice(["sim", "nao", "nao"])
    if k == "sim":
        x, y = a * m, b * m
    else:
        x, y = a + m, b + m
        if x * b == y * a:
            return None
    ok = x * b == y * a
    ans = "Sim, são equivalentes" if ok else "Não são equivalentes"
    return mcq("%s e %s são frações equivalentes?" % (fr(a, b), fr(x, y)), ans,
               ["Não são equivalentes" if ok else "Sim, são equivalentes", "Só se a figura for um círculo", "Não dá para saber"],
               ("%d × %d = %d e %d × %d = %d: os dois termos foram multiplicados por %d. <b>Sim.</b>" % (a, m, x, b, m, y, m)) if ok else
               ("Somar %d aos dois termos não dá uma fração equivalente: %s = %s, mas %s não. <b>Não são.</b>" % (m, fr(a, b), fr(a * 2, b * 2), fr(x, y))))


def s4_lista():
    ab = base()
    if not ab:
        return None
    a, b = ab
    ms = R.sample(range(2, 8), 2)
    good = [fr(a, b)] + [fr(a * m, b * m) for m in ms]
    bad1 = fr(a + 1, b + 1)
    w = [", ".join([good[0], good[1], bad1]), ", ".join([good[0], fr(a * ms[0], b), good[2]]), ", ".join([good[0], fr(a + ms[0], b + ms[0]), fr(b, a) if a > 1 else fr(a, b + 2)])]
    return mcq("Em qual lista <b>todas</b> as frações são equivalentes a %s?" % fr(a, b), ", ".join(good), w,
               "%s: numerador e denominador multiplicados pelo mesmo número. Resposta: <b>%s</b>." % (", ".join(good), ", ".join(good)))


def s5_problema():
    k = R.choice(["pizza", "chocolate", "receita", "tempo", "dinheiro"])
    p, g = K.next()
    q = K.next()[0]
    if p == q:
        return None
    if k == "pizza":
        ab = base()
        if not ab:
            return None
        a, b = ab
        m = R.choice([2, 3])
        if b * m > 12:
            return None
        return mcq("%s comeu %s de uma pizza. %s comeu %s de uma pizza igual. Quem comeu mais?" % (p, fr(a, b), q, fr(a * m, b * m)), "Comeram a mesma quantidade",
                   [p, q, "Não dá para saber"], "%s = %s (multiplicando os termos por %d): <b>comeram a mesma quantidade</b>." % (fr(a, b), fr(a * m, b * m), m))
    if k == "chocolate":
        b = R.choice([4, 6, 8, 10, 12])
        d = R.choice([x for x in (2, 3, 4) if b % x == 0])
        a = b // d
        return mcq("Uma barra de chocolate tem %d quadradinhos. %s comeu %d quadradinhos. Que fração irredutível da barra %s comeu?" % (b, p, a, g), fr(1, d),
                   [fr(a, b) if a > 1 else fr(1, b), fr(d, b), fr(1, a) if a != d else fr(1, d + 1), fr(b - a, b)],
                   "%d de %d = %s = <b>%s</b>." % (a, b, fr(a, b), fr(1, d)))
    if k == "receita":
        m = R.choice([2, 4])
        return mcq("Uma receita pede %s de xícara de açúcar. %s só tem uma colher que mede %s de xícara. Quantas colheres %s precisa usar?" % (fr(1, 2), p, fr(1, 2 * m), g), str(m),
                   [str(2 * m), "1", str(m + 1)], "%s = %s: são <b>%d</b> colheres de %s." % (fr(1, 2), fr(m, 2 * m), m, fr(1, 2 * m)))
    if k == "tempo":
        a, b = R.choice([(1, 2), (1, 4), (3, 4), (1, 3), (2, 3), (1, 6), (5, 6), (1, 5)])
        mins = 60 * a // b
        return mcq("%s de hora são quantos minutos? (1 hora = 60 minutos)" % fr(a, b), "%d minutos" % mins,
                   ["%d minutos" % x for x in (60 // b, 60 - mins, a * 10 + b, mins + 10, mins * 2) if x != mins],
                   "%s = %s: <b>%d minutos</b>." % (fr(a, b), fr(mins, 60), mins))
    a, b = R.choice([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (1, 10), (3, 10)])
    c = 100 * a // b
    return mcq("%s de 1 real são quantos centavos? (1 real = 100 centavos)" % fr(a, b), "%d centavos" % c,
               ["%d centavos" % x for x in (100 // b, 100 - c, a * 10 + b, c * 2 if c * 2 <= 100 else c - 5, c + 5) if x != c],
               "%s = %s: <b>%d centavos</b>." % (fr(a, b), fr(c, 100), c))


def main():
    seen = set()
    sets = [
        ("Frações equivalentes nas figuras", mix(R, seen, [(s1_figura, 12), (s1_qual, 8)])),
        ("O termo que falta", mix(R, seen, [(s2_falta, 12), (s2_mult, 8)])),
        ("Simplificar frações", mix(R, seen, [(s3_simplificar, 12), (s3_irredutivel, 8)])),
        ("São equivalentes?", mix(R, seen, [(s4_sao, 12), (s4_lista, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Frações <b>equivalentes</b> representam a mesma parte do inteiro: " + fr(1, 2) + " = " + fr(2, 4) + " = " + fr(4, 8) + ".",
         "Para obter uma fração equivalente, <b>multiplique</b> ou <b>divida</b> o numerador e o denominador pelo <b>mesmo número</b>.",
         "<b>Simplificar</b> é dividir os dois termos pelo mesmo número. Quando não dá mais, a fração é <b>irredutível</b>."],
        [("Complete: " + fr(3, 4) + " = ?/20", ["4 × 5 = 20", "3 × 5 = 15"], fr(15, 20)),
         ("Simplifique " + fr(12, 18) + ".", ["12 ÷ 6 = 2 e 18 ÷ 6 = 3"], fr(2, 3))],
        [["Somar o mesmo número aos dois termos: " + fr(1, 2) + " = " + fr(3, 4), "Some não: multiplique. " + fr(1, 2) + " = " + fr(2, 4) + "."],
         ["Multiplicar só o numerador", "Os dois termos mudam juntos, pelo mesmo número."],
         ["Achar que " + fr(4, 8) + " é maior que " + fr(1, 2) + " porque tem números maiores", "As partes são menores, mas há mais partes: é a mesma quantidade."]],
        faixa(2, 1) + faixa(4, 2) + faixa(8, 4))
    faq = [("O que são frações equivalentes?", "São frações que representam a mesma quantidade, como 1/2, 2/4 e 3/6. Obtemos uma da outra multiplicando ou dividindo os dois termos pelo mesmo número."),
           ("Para que serve simplificar?", "A fração irredutível é a forma mais simples de escrever a mesma quantidade. Fica mais fácil comparar e calcular.")]
    make_unit(R, "fracoes-equivalentes", "N", ["EF05MA04"],
              "Identificar frações equivalentes",
              "Frações equivalentes: completar, simplificar e reconhecer", "Frações equivalentes",
              "Atividades de matemática para o 5º ano sobre frações equivalentes: figuras, termo que falta, simplificação, fração irredutível e problemas. 100 exercícios com gabarito.",
              "Multiplique ou divida os dois termos pelo mesmo número.", "1/2 = 2/4 = 3/6 = 4/8",
              body, faq, sets, 4, grade="5-ano")


if __name__ == "__main__":
    main()
