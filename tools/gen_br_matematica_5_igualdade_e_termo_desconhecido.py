# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Igualdade e termo desconhecido (Álgebra, EF05MA10, EF05MA11)
  python3 tools/gen_br_matematica_5_igualdade_e_termo_desconhecido.py
A igualdade se mantém quando somamos, subtraímos, multiplicamos ou dividimos os dois lados pelo mesmo número;
sentenças verdadeiras e falsas; termo desconhecido na adição, subtração, multiplicação e divisão; balança em equilíbrio; problemas.
Erros: mudar só um lado, ler o sinal = como «o resultado é» (8 + 4 = □ + 5 → 12), usar a operação errada para achar o termo.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, wrap, text, line, INK, GREEN, Kids, reais

R = random.Random(80512)
K = Kids(R)
SQ = "□"


def balanca(esq, dir_):
    """balança de pratos em equilíbrio: esq e dir são textos"""
    s = [line(160, 20, 160, 108, INK, 3), "<polygon points='146,118 174,118 160,104' fill='%s'/>" % INK, line(40, 40, 280, 40, INK, 3),
         line(70, 40, 50, 80, INK, 1.2), line(70, 40, 90, 80, INK, 1.2), line(250, 40, 230, 80, INK, 1.2), line(250, 40, 270, 80, INK, 1.2),
         "<path d='M30 80 Q70 100 110 80 Z' fill='#e8d9b5' stroke='%s'/>" % INK, "<path d='M210 80 Q250 100 290 80 Z' fill='#e8d9b5' stroke='%s'/>" % INK,
         text(70, 112, esq, 14), text(250, 112, dir_, 14)]
    return wrap(320, 124, "".join(s), "balança em equilíbrio: %s de um lado e %s do outro" % (esq, dir_))


def s1_mesmo():
    a, b = R.randint(12, 90), R.randint(12, 90)
    c = R.randint(2, 30)
    k = R.choice(["+", "−", "×", "÷"])
    s = a + b
    if k == "+":
        q = "Sabemos que %d + %d = %d. Então %d + %d + %d = %d + %s. Que número fica no %s?" % (a, b, s, a, b, c, s, SQ, SQ)
        return mcq(q, str(c), [str(s + c), str(c + 1), str(a + c)], "Somamos %d de um lado; para a igualdade continuar, somamos %d do outro: <b>%d</b>." % (c, c, c))
    if k == "−":
        c = R.randint(2, min(a, 30))
        q = "Sabemos que %d + %d = %d. Então %d + %d − %d = %d − %s. Que número fica no %s?" % (a, b, s, a, b, c, s, SQ, SQ)
        return mcq(q, str(c), [str(s - c), str(c + 1), str(abs(b - c)), str(c * 2), str(c - 1)], "Tiramos %d de um lado; tiramos %d do outro: <b>%d</b>." % (c, c, c))
    if k == "×":
        c = R.randint(2, 9)
        q = "Sabemos que %d + %d = %d. Então (%d + %d) × %d = %d × %s. Que número fica no %s?" % (a, b, s, a, b, c, s, SQ, SQ)
        return mcq(q, str(c), [num(s * c), str(c + 1), str(c * 2)], "Multiplicamos um lado por %d; multiplicamos o outro também: <b>%d</b>." % (c, c))
    c = R.choice([d for d in range(2, 10) if s % d == 0] or [0])
    if not c:
        return None
    q = "Sabemos que %d + %d = %d. Então (%d + %d) ÷ %d = %d ÷ %s. Que número fica no %s?" % (a, b, s, a, b, c, s, SQ, SQ)
    return mcq(q, str(c), [str(s // c), str(c + 1), str(c * 2)], "Dividimos um lado por %d; dividimos o outro também: <b>%d</b>." % (c, c))


def s1_balanca():
    a = R.randint(3, 20)
    b = R.randint(3, 20)
    c = R.randint(2, 9)
    tot = a + b
    k = R.choice(["add", "tira"])
    pic = balanca("%d kg + %d kg" % (a, b), "%d kg" % tot)
    if k == "add":
        return mcq(pic + "A balança está em equilíbrio. Colocamos mais %d kg no prato da esquerda. Quanto precisamos pôr no prato da direita para continuar em equilíbrio?" % c,
                   "%d kg" % c, ["%d kg" % x for x in (tot + c, c * 2, tot)], "O que fazemos de um lado, fazemos do outro: <b>%d kg</b>." % c)
    m = R.choice([2, 3])
    return mcq(pic + "A balança está em equilíbrio. Se dobrarmos a massa do prato da esquerda, o que devemos fazer com o da direita?" if m == 2 else
               pic + "A balança está em equilíbrio. Se triplicarmos a massa do prato da esquerda, o que devemos fazer com o da direita?",
               "%s também: %d kg" % ("Dobrar" if m == 2 else "Triplicar", tot * m), ["Somar %d kg" % m, "Deixar como está", "%s também: %d kg" % ("Dobrar" if m == 2 else "Triplicar", tot + m)],
               "Multiplicamos os dois lados por %d: %d × %d = <b>%d kg</b>." % (m, tot, m, tot * m))


def s2_verdade():
    a, b = R.randint(15, 80), R.randint(15, 80)
    k = R.choice(["add", "sub", "mul"])
    if k == "add":
        d = R.randint(2, 9)
        good = "%d + %d = %d + %d" % (a, b, a + d, b - d)
        bad = ["%d + %d = %d + %d" % (a, b, a + d, b + d), "%d + %d = %d + %d" % (a, b, a - d, b - d), "%d + %d = %d" % (a, b, a + b + d)]
    elif k == "sub":
        d = R.randint(2, 9)
        a, b = max(a, b) + 10, min(a, b)
        good = "%d − %d = %d − %d" % (a, b, a + d, b + d)
        bad = ["%d − %d = %d − %d" % (a, b, a + d, b - d), "%d − %d = %d − %d" % (a, b, a - d, b + d), "%d − %d = %d" % (a, b, a - b + d)]
    else:
        a, b = R.randint(2, 9) * 2, R.randint(3, 12)
        good = "%d × %d = %d × %d" % (a, b, a // 2, b * 2)
        bad = ["%d × %d = %d × %d" % (a, b, a // 2, b + 2), "%d × %d = %d × %d" % (a, b, a + 2, b - 2), "%d × %d = %d" % (a, b, a * b + a)]
    left = good.split(" = ")[0]
    return mcq("Qual destas igualdades com %s é <b>verdadeira</b>?" % left, good, bad,
               "Calcule os dois lados: %s. Os dois lados dão o mesmo valor: <b>%s</b>." % ({"add": "%d = %d" % (a + b, a + b), "sub": "%d = %d" % (a - b, a - b), "mul": "%d = %d" % (a * b, a * b)}[k], good)) \



def s2_lado():
    a, b, c = R.randint(10, 60), R.randint(10, 60), R.randint(5, 40)
    if c >= a + b:
        return None
    ans = a + b - c
    return mcq("Que número torna a igualdade verdadeira? %d + %d = %s + %d" % (a, b, SQ, c), str(ans), [str(a + b), str(a + b + c), str(ans + 1), str(abs(a - c))],
               "%d + %d = %d. Que número somado a %d dá %d? %d − %d = <b>%d</b>." % (a, b, a + b, c, a + b, a + b, c, ans))


def s3_adsub():
    k = R.choice(["a+", "+b", "a-", "-b"])
    a = R.randint(120, 9000)
    b = R.randint(120, 9000)
    if k == "a+":
        return mcq("Qual é o número que falta? %s + %s = %s" % (SQ, num(a), num(a + b)), num(b), [num(a + a + b), num(b + 100), num(b - 10)],
                   "Use a operação inversa: %s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    if k == "+b":
        return mcq("Qual é o número que falta? %s + %s = %s" % (num(a), SQ, num(a + b)), num(b), [num(a + a + b), num(b + 1000), num(b + 10)],
                   "%s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    if k == "a-":
        return mcq("Qual é o número que falta? %s − %s = %s" % (SQ, num(b), num(a)), num(a + b), [num(abs(a - b)), num(a + b + 100), num(a)],
                   "O número que falta é o total: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    return mcq("Qual é o número que falta? %s − %s = %s" % (num(a + b), SQ, num(a)), num(b), [num(a + a + b), num(b + 10), num(a)],
               "%s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))


def s4_muldiv():
    k = R.choice(["x*", "*x", "x/", "/x"])
    a = R.randint(3, 15)
    b = R.randint(6, 80)
    if k == "x*":
        return mcq("Qual é o número que falta? %s × %d = %s" % (SQ, a, num(a * b)), num(b), [num(a * b - a), num(a * b * a), num(b + 1), num(a * b + a)],
                   "Use a divisão: %s ÷ %d = <b>%s</b>." % (num(a * b), a, num(b)))
    if k == "*x":
        return mcq("Qual é o número que falta? %d × %s = %s" % (a, SQ, num(a * b)), num(b), [num(a * b - a), num(b * 10), num(b - 1), num(a * b + a)],
                   "%s ÷ %d = <b>%s</b>." % (num(a * b), a, num(b)))
    if k == "x/":
        return mcq("Qual é o número que falta? %s ÷ %d = %d" % (SQ, a, b), num(a * b), [num(b // a) if b // a else num(a + b), num(a + b), num(a * b + a)],
                   "Use a multiplicação: %d × %d = <b>%s</b>." % (b, a, num(a * b)))
    return mcq("Qual é o número que falta? %s ÷ %s = %d" % (num(a * b), SQ, b), str(a), [num(a * b * b) if a * b * b < 100000 else num(a * b - b), num(a * b - b), str(a + 1)],
               "%s ÷ %d = <b>%d</b>, porque %d × %d = %s." % (num(a * b), b, a, b, a, num(a * b)))


def s4_dupla():
    a = R.randint(2, 9)
    b = R.randint(2, 30)
    c = R.randint(5, 60)
    tot = a * b + c
    return mcq("Qual é o número que falta? %d × %s + %d = %s" % (a, SQ, c, num(tot)), str(b), [str((tot + c) // a) if (tot + c) % a == 0 else str(b + 2), num(tot - c), str(b + 1), num(tot // a)],
               "Primeiro tire %d: %s − %d = %s. Depois divida por %d: %s ÷ %d = <b>%d</b>." % (c, num(tot), c, num(a * b), a, num(a * b), a, b))


def s5_problema():
    k = R.choice(["figur", "idade", "cofre", "caixa", "onibus", "preco", "balanca"])
    p, g = K.next()
    if k == "figur":
        a, b = R.randint(30, 150), R.randint(20, 120)
        return mcq("%s tinha algumas figurinhas. Ganhou %d e ficou com %d. Quantas figurinhas %s tinha? (%s + %d = %d)" % (p, a, a + b, g, SQ, a, a + b), str(b), [str(2 * a + b), str(b + 10), str(a)],
                   "%d − %d = <b>%d</b>." % (a + b, a, b))
    if k == "idade":
        f = R.randint(8, 12)
        m = R.randint(3, 4)
        return mcq("A mãe de %s tem %d anos e isso é %d vezes a idade de %s. Quantos anos %s tem? (%d × %s = %d)" % (p, f * m, m, p, p, m, SQ, f * m), "%d anos" % f,
                   ["%d anos" % x for x in (f * m - m, f * m * m, f + m)], "%d ÷ %d = <b>%d anos</b>." % (f * m, m, f))
    if k == "cofre":
        a, b = R.randint(20, 60) * 1000, R.randint(5, 40) * 1000
        return mcq("%s quer comprar uma bicicleta de %s. Já tem %s. Quanto ainda falta? (%s + %s = %s)" % (p, reais(a + b), reais(a), reais(a), SQ, reais(a + b)), reais(b),
                   [reais(2 * a + b), reais(b + 1000), reais(a)], "%s − %s = <b>%s</b>." % (reais(a + b), reais(a), reais(b)))
    if k == "caixa":
        a, b = R.randint(6, 24), R.randint(12, 40)
        return mcq("Uma loja colocou %d lápis em caixas iguais e encheu %d caixas. Quantos lápis vão em cada caixa? (%d × %s = %d)" % (a * b, a, a, SQ, a * b), str(b),
                   [str(a * b - a), str(b + 2), num(a * b * a) if a * b * a < 100000 else str(a)], "%d ÷ %d = <b>%d</b>." % (a * b, a, b))
    if k == "onibus":
        a, b, c = R.randint(20, 40), R.randint(5, 15), R.randint(3, 12)
        x = a - b + c
        return mcq("Um ônibus saiu com %d passageiros. No caminho desceram %d e subiram alguns. Chegou com %d. Quantos subiram? (%d − %d + %s = %d)" % (a, b, x, a, b, SQ, x), str(c),
                   [str(x + b), str(x + b - a + b), str(x), str(c + 1), str(a - b)], "%d − %d = %d. %d + %s = %d → %s = <b>%d</b>." % (a, b, a - b, a - b, SQ, x, SQ, c))
    if k == "preco":
        n = R.randint(3, 8)
        pr = R.randint(4, 25) * 100
        return mcq("%d cadernos iguais custaram %s. Qual é o preço de cada caderno? (%d × %s = %s)" % (n, reais(n * pr), n, SQ, reais(n * pr)), reais(pr),
                   [reais(n * pr - n * 100), reais(pr + 100), reais(n * pr * n)], "%s ÷ %d = <b>%s</b>." % (reais(n * pr), n, reais(pr)))
    a, b = R.randint(2, 6), R.randint(100, 500)
    return mcq(balanca("%d pacotes iguais" % a, "%s g" % num(a * b)) + "A balança está em equilíbrio. Quantos gramas tem cada pacote?", "%s g" % num(b),
               ["%s g" % num(x) for x in (a * b - a, a * b, b + a)], "%d × %s = %s → %s ÷ %d = <b>%s g</b>." % (a, SQ, num(a * b), num(a * b), a, num(b)))


def main():
    seen = set()
    sets = [
        ("A igualdade continua", mix(R, seen, [(s1_mesmo, 14), (s1_balanca, 6)])),
        ("Igualdades verdadeiras", mix(R, seen, [(s2_verdade, 10), (s2_lado, 10)])),
        ("Termo desconhecido: + e −", mix(R, seen, [(s3_adsub, 20)])),
        ("Termo desconhecido: × e ÷", mix(R, seen, [(s4_muldiv, 14), (s4_dupla, 6)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["O sinal <b>=</b> quer dizer que os dois lados têm o <b>mesmo valor</b>, como uma balança em equilíbrio.",
         "Se somamos, subtraímos, multiplicamos ou dividimos <b>os dois lados</b> pelo mesmo número, a igualdade continua.",
         "Para achar o termo desconhecido, use a <b>operação inversa</b>: a adição desfaz a subtração e a divisão desfaz a multiplicação.",
         "Em 8 + 4 = %s + 5, calcule o lado esquerdo (12) e pense: que número mais 5 dá 12?" % SQ],
        [("%s × 7 = 91" % SQ, ["a divisão desfaz a multiplicação", "91 ÷ 7"], "13"),
         ("Se 25 + 15 = 40, quanto vale %s em (25 + 15) × 3 = 40 × %s?" % (SQ, SQ), ["multiplicamos um lado por 3", "multiplicamos o outro por 3"], "3")],
        [["Mudar só um lado da igualdade", "O que você faz de um lado, faça do outro."],
         ["Ler = como «o resultado é»: 8 + 4 = %s + 5 → 12" % SQ, "Os dois lados valem 12: %s = 7." % SQ],
         ["Usar a operação errada: %s − 25 = 40 → 15" % SQ, "O número que falta é o total: 40 + 25 = 65."]],
        balanca("12 kg + 8 kg", "20 kg"))
    faq = [("O que é a relação de igualdade?", "É saber que o sinal = mostra dois lados com o mesmo valor, e que a igualdade se mantém quando fazemos a mesma operação com o mesmo número nos dois lados."),
           ("Isso já é equação?", "É a preparação para as equações do 6º e 7º anos. No 5º ano usamos o quadradinho (%s) para o termo desconhecido e resolvemos com operações inversas." % SQ)]
    make_unit(R, "igualdade-e-termo-desconhecido", "A", ["EF05MA10", "EF05MA11"],
              "Concluir, por meio de investigações, que a relação de igualdade existente entre dois membros permanece ao adicionar, subtrair, multiplicar ou dividir cada um desses membros por um mesmo número; resolver e elaborar problemas cuja conversão em sentença matemática seja uma igualdade com uma operação em que um dos termos é desconhecido",
              "Igualdade e termo desconhecido: a balança em equilíbrio", "Igualdade e termo desconhecido",
              "Atividades de matemática para o 5º ano sobre igualdade e termo desconhecido: a igualdade se mantém, balança em equilíbrio, sentenças verdadeiras e número que falta nas quatro operações. 100 exercícios com gabarito.",
              "O que você faz de um lado, faça do outro.", "Termo desconhecido: use a operação inversa.",
              body, faq, sets, 12, grade="5-ano")


if __name__ == "__main__":
    main()
