# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Relações entre as operações (Números e Álgebra, EF04MA04, EF04MA13)
  python3 tools/gen_br_matematica_4_relacoes_entre_as_operacoes.py
Adição e subtração são operações inversas; multiplicação e divisão são operações inversas; famílias de fatos;
multiplicação como adição de parcelas iguais e divisão como subtrações sucessivas; número que falta; desfazer operações («pensei num número»).
Erros: usar a mesma operação para desfazer (□ − 25 = 40 → 15), trocar dividendo e divisor, desfazer na ordem errada.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, Kids, reais

R = random.Random(80403)
K = Kids(R)
SQ = "□"


def s1_familia_ad():
    a, b = R.randint(120, 4800), R.randint(120, 4800)
    s = a + b
    k = R.choice(["sub1", "sub2", "add"])
    fact = "%s + %s = %s" % (num(a), num(b), num(s))
    if k == "add":
        d = s - b
        fact = "%s − %s = %s" % (num(s), num(b), num(d))
        good = "%s + %s = %s" % (num(d), num(b), num(s))
        w = ["%s − %s = %s" % (num(d), num(b), num(s)), "%s + %s = %s" % (num(s), num(b), num(d)), "%s − %s = %s" % (num(b), num(d), num(s))]
        return mcq("Sabendo que %s, qual destas contas também é verdadeira?" % fact, good, w,
                   "A adição desfaz a subtração: <b>%s</b>." % good)
    x, y = (a, b) if k == "sub1" else (b, a)
    good = "%s − %s = %s" % (num(s), num(y), num(x))
    w = ["%s − %s = %s" % (num(x), num(y), num(s)), "%s + %s = %s" % (num(s), num(y), num(x)), "%s − %s = %s" % (num(s), num(x), num(s - x + 10))]
    return mcq("Sabendo que %s, qual destas contas também é verdadeira?" % fact, good, w,
               "A subtração desfaz a adição: se %s, então <b>%s</b>." % (fact, good))


def s1_familia_md():
    a, b = R.randint(3, 12), R.randint(12, 250)
    p = a * b
    if R.random() < 0.5:
        fact = "%d × %d = %s" % (b, a, num(p))
        good = "%s ÷ %d = %d" % (num(p), a, b)
        w = ["%d ÷ %s = %d" % (a, num(p), b), "%s ÷ %d = %d" % (num(p), b, a + 1), "%s × %d = %d" % (num(p), a, b)]
        return mcq("Sabendo que %s, qual destas contas também é verdadeira?" % fact, good, w, "A divisão desfaz a multiplicação: <b>%s</b>." % good)
    fact = "%s ÷ %d = %d" % (num(p), a, b)
    good = "%d × %d = %s" % (b, a, num(p))
    w = ["%d ÷ %d = %s" % (b, a, num(p)), "%d × %d = %s" % (b, a, num(p + a)), "%s × %d = %d" % (num(p), b, a)]
    return mcq("Sabendo que %s, qual destas contas também é verdadeira?" % fact, good, w, "A multiplicação desfaz a divisão: <b>%s</b>." % good)


def s2_parcelas():
    a = R.randint(3, 9)
    b = R.randint(12, 99)
    k = R.choice(["mult", "div"])
    if k == "mult":
        soma = " + ".join([str(b)] * a)
        return mcq("Que multiplicação é igual a %s?" % soma, "%d × %d" % (a, b), ["%d + %d" % (a, b), "%d × %d" % (a + 1, b), "%d × %d" % (a, b + a)],
                   "São %d parcelas iguais a %d: <b>%d × %d</b> = %d." % (a, b, a, b, a * b))
    tot = a * b
    return mcq("Tirando %d de %d várias vezes, chegamos a zero. Quantas vezes tiramos?" % (b, tot), str(a),
               [str(a + 1), str(b), str(tot - b)], "Isso é a divisão %d ÷ %d = <b>%d</b>." % (tot, b, a))


def s2_inversa():
    k = R.choice(["ad", "md"])
    if k == "ad":
        n, d = R.randint(100, 9000), R.randint(100, 900)
        return mcq("Um número foi somado com %s e depois %s foi tirado. Que número sobrou?" % (num(d), num(d)), "o mesmo número do começo", ["zero", "o dobro do número", "o número mais %s" % num(d)],
                   "Somar e depois tirar o mesmo número desfaz a conta: fica <b>o mesmo número do começo</b>. Exemplo: %s + %s − %s = %s." % (num(n), num(d), num(d), num(n)))
    n, d = R.randint(10, 300), R.randint(2, 9)
    return mcq("Pense em %d. Multiplique por %d e depois divida o resultado por %d. Que número você obtém?" % (n, d, d), str(n), [num(n * d), str(n * d * d) if n * d * d < 100000 else str(n + d), str(d)],
               "Multiplicar e dividir pelo mesmo número se desfazem: %d × %d = %s; %s ÷ %d = <b>%d</b>." % (n, d, num(n * d), num(n * d), d, n))


def s3_falta_ad():
    a, b = R.randint(150, 9000), R.randint(150, 9000)
    k = R.choice(["x+b", "x-b", "a-x"])
    if k == "x+b":
        return mcq("Qual é o número que falta? %s + %s = %s" % (SQ, num(b), num(a + b)), num(a), [num(a + b + b), num(a + 100), num(b)],
                   "Desfaça a adição com uma subtração: %s − %s = <b>%s</b>." % (num(a + b), num(b), num(a)))
    if k == "x-b":
        return mcq("Qual é o número que falta? %s − %s = %s" % (SQ, num(b), num(a)), num(a + b), [num(abs(a - b)), num(a + b + 100), num(a)],
                   "Desfaça a subtração com uma adição: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    return mcq("Qual é o número que falta? %s − %s = %s" % (num(a + b), SQ, num(a)), num(b), [num(a + a + b), num(b + 10), num(a)],
               "%s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))


def s3_falta_md():
    a, b = R.randint(3, 12), R.randint(11, 150)
    k = R.choice(["x*a", "x/a", "p/x"])
    p = a * b
    if k == "x*a":
        return mcq("Qual é o número que falta? %s × %d = %s" % (SQ, a, num(p)), str(b), [num(p * a) if p * a < 100000 else num(p - a), num(p - a), str(b + 1)],
                   "Desfaça a multiplicação com uma divisão: %s ÷ %d = <b>%d</b>." % (num(p), a, b))
    if k == "x/a":
        return mcq("Qual é o número que falta? %s ÷ %d = %d" % (SQ, a, b), num(p), [str(b // a) if b // a > 1 else str(a + b), num(a + b), num(p + a)],
                   "Desfaça a divisão com uma multiplicação: %d × %d = <b>%s</b>." % (b, a, num(p)))
    return mcq("Qual é o número que falta? %s ÷ %s = %d" % (num(p), SQ, b), str(a), [num(p * b) if p * b < 100000 else num(p - b), num(p - b), str(a + 1)],
               "Que número vezes %d dá %s? %d × %d = %s: <b>%d</b>." % (b, num(p), a, b, num(p), a))


def s4_pensei():
    p, g = K.next()
    k = R.choice(["add_mul", "mul_add", "sub_div", "mul_sub"])
    x = R.randint(3, 40)
    if k == "add_mul":
        a, m = R.randint(2, 20), R.randint(2, 5)
        res = (x + a) * m
        steps = "somou %d e multiplicou o resultado por %d" % (a, m)
        e = "Desfaça de trás para a frente: %d ÷ %d = %d; %d − %d = <b>%d</b>." % (res, m, x + a, x + a, a, x)
        w = [res // m + a if res % m == 0 else res - a, res - a, res // m]
    elif k == "mul_add":
        m, a = R.randint(2, 6), R.randint(2, 30)
        res = x * m + a
        steps = "multiplicou por %d e somou %d" % (m, a)
        e = "Desfaça de trás para a frente: %d − %d = %d; %d ÷ %d = <b>%d</b>." % (res, a, x * m, x * m, m, x)
        w = [res // m - a if res // m > a else res - m, res - a, (res + a) // m]
    elif k == "sub_div":
        a, m = R.randint(2, 20), R.randint(2, 5)
        if x <= a or (x - a) % m:
            return None
        res = (x - a) // m
        steps = "tirou %d e dividiu o resultado por %d" % (a, m)
        e = "Desfaça de trás para a frente: %d × %d = %d; %d + %d = <b>%d</b>." % (res, m, x - a, x - a, a, x)
        w = [res * m - a if res * m > a else res + a, res + a, res * m]
    else:
        m, a = R.randint(2, 6), R.randint(2, 30)
        if x * m <= a:
            return None
        res = x * m - a
        steps = "multiplicou por %d e tirou %d" % (m, a)
        e = "Desfaça de trás para a frente: %d + %d = %d; %d ÷ %d = <b>%d</b>." % (res, a, x * m, x * m, m, x)
        w = [(res - a) // m if res > a else res + m, res + a, res // m if res // m != x else res]
    return mcq("%s pensou num número, %s. Deu %d. Em que número %s pensou?" % (p, steps, res, g), str(x), [str(v) for v in w if v > 0 and v != x] + [str(x + 1)], e)


def s5_problema():
    k = R.choice(["figur", "caixas", "ingressos", "dinheiro", "km", "fila", "pacotes"])
    p, g = K.next()
    if k == "figur":
        a, b = R.randint(30, 300), R.randint(20, 200)
        return mcq("%s ganhou %d figurinhas e ficou com %d. Quantas figurinhas %s tinha antes?" % (p, b, a + b, g), str(a), [str(a + b + b), str(a + 10), str(b)],
                   "Desfaça o «ganhou» com uma subtração: %d − %d = <b>%d</b>." % (a + b, b, a))
    if k == "caixas":
        a, b = R.randint(4, 12), R.randint(12, 48)
        return mcq("Uma loja arrumou %d lápis em caixas com %d lápis cada. Quantas caixas usou?" % (a * b, b), str(a), [str(a * b - b), str(a + 1), str(a * b * b) if a * b * b < 100000 else str(b)],
                   "%d ÷ %d = <b>%d</b>. Conferindo: %d × %d = %d." % (a * b, b, a, a, b, a * b))
    if k == "ingressos":
        n, pr = R.randint(3, 9), R.randint(15, 45)
        tot = n * pr
        return mcq("%s pagou %s por %d ingressos iguais. Quanto custou cada ingresso?" % (p, reais(tot * 100), n), reais(pr * 100),
                   [reais((tot - n) * 100), reais(tot * n * 100) if tot * n < 1000 else reais((pr + 5) * 100), reais((pr + 1) * 100)], "%s ÷ %d = <b>%s</b>, porque %d × %s = %s." % (reais(tot * 100), n, reais(pr * 100), n, reais(pr * 100), reais(tot * 100)))
    if k == "dinheiro":
        a, b = R.randint(50, 400), R.randint(20, 300)
        return mcq("%s gastou %s e ainda tem %s. Quanto %s tinha antes de gastar?" % (p, reais(b * 100), reais(a * 100), g), reais((a + b) * 100),
                   [reais(abs(a - b) * 100), reais((a + b + 10) * 100), reais(a * 100)], "Desfaça o gasto com uma adição: %s + %s = <b>%s</b>." % (reais(a * 100), reais(b * 100), reais((a + b) * 100)))
    if k == "km":
        d, v = R.randint(3, 8), R.randint(40, 90)
        return mcq("Um caminhão rodou %s km em %d dias, a mesma distância por dia. Quantos quilômetros rodou por dia?" % (num(d * v * 10), d), "%s km" % num(v * 10),
                   ["%s km" % num(x) for x in (d * v * 10 - d, v, v * 10 + 10)], "%s ÷ %d = <b>%s km</b>." % (num(d * v * 10), d, num(v * 10)))
    if k == "fila":
        f, c = R.randint(8, 25), R.randint(10, 30)
        return mcq("Um teatro tem %d cadeiras arrumadas em fileiras de %d. Quantas fileiras há?" % (f * c, c), str(f), [str(f * c - c), str(f + c), str(f + 1)],
                   "%d ÷ %d = <b>%d</b> fileiras; conferindo: %d × %d = %d." % (f * c, c, f, f, c, f * c))
    a, b, c = R.randint(5, 30), R.randint(3, 9), R.randint(2, 20)
    tot = a * b + c
    return mcq("%s tinha %d pacotes iguais de balas e mais %d balas soltas. Ao todo eram %d balas. Quantas balas tinha cada pacote?" % (p, b, c, tot), str(a),
               [str(tot // b), str((tot + c) // b) if (tot + c) // b != a else str(a + 1), str(tot - c)], "Tire as soltas: %d − %d = %d. Divida pelos pacotes: %d ÷ %d = <b>%d</b>." % (tot, c, tot - c, tot - c, b, a))


def main():
    seen = set()
    sets = [
        ("Adição e subtração são inversas", mix(R, seen, [(s1_familia_ad, 20)])),
        ("Multiplicação e divisão são inversas", mix(R, seen, [(s1_familia_md, 12), (s2_parcelas, 8)])),
        ("O número que falta", mix(R, seen, [(s3_falta_ad, 10), (s3_falta_md, 10)])),
        ("Desfazer as operações", mix(R, seen, [(s2_inversa, 6), (s4_pensei, 14)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["A <b>subtração desfaz a adição</b>: se 345 + 278 = 623, então 623 − 278 = 345 e 623 − 345 = 278.",
         "A <b>divisão desfaz a multiplicação</b>: se 24 × 6 = 144, então 144 ÷ 6 = 24.",
         "Para achar o número que falta, use a operação inversa: em %s − 125 = 340, faça 340 + 125." % SQ,
         "Para desfazer várias operações, comece pela última e vá voltando."],
        [("%s × 7 = 91" % SQ, ["a divisão desfaz a multiplicação", "91 ÷ 7"], "13"),
         ("Pensei num número, somei 8 e multipliquei por 3. Deu 45.", ["desfaça o × 3: 45 ÷ 3 = 15", "desfaça o + 8: 15 − 8 = 7"], "7")],
        [["Usar a mesma operação: %s − 25 = 40 → 40 − 25 = 15" % SQ, "Desfaça a subtração com adição: 40 + 25 = 65."],
         ["Trocar dividendo e divisor: 6 ÷ 144", "O número maior (o total) vem primeiro: 144 ÷ 6."],
         ["Desfazer na ordem errada", "Comece pela última operação."]])
    faq = [("O que são operações inversas?", "São operações que se desfazem: a adição e a subtração, a multiplicação e a divisão. Por isso uma serve para conferir a outra (prova real)."),
           ("Para que o 4º ano estuda isso?", "A BNCC pede usar as relações entre as operações para ampliar as estratégias de cálculo e para resolver problemas em que um número é desconhecido.")]
    make_unit(R, "relacoes-entre-as-operacoes", "A", ["EF04MA04", "EF04MA13"],
              "Utilizar as relações entre adição e subtração, bem como entre multiplicação e divisão, para ampliar as estratégias de cálculo; reconhecer, por meio de investigações, utilizando a calculadora quando necessário, as relações inversas entre as operações de adição e de subtração e de multiplicação e de divisão, para aplicá-las na resolução de problemas",
              "Relações entre as operações: inversas e famílias de fatos", "Operações inversas",
              "Atividades de matemática para o 4º ano sobre relações entre as operações: adição e subtração inversas, multiplicação e divisão inversas, número que falta e desfazer operações. 100 exercícios com gabarito.",
              "A subtração desfaz a adição; a divisão desfaz a multiplicação.", "Para desfazer, comece pela última operação.",
              body, faq, sets, 3, grade="4-ano")


if __name__ == "__main__":
    main()
