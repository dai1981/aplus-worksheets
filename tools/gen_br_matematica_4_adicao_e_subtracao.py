# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Adição e subtração (Números, EF04MA03)
  python3 tools/gen_br_matematica_4_adicao_e_subtracao.py
Adição e subtração de números naturais até 99.999: conta armada com reagrupamento (vai um, trocas, zeros no minuendo);
cálculo mental (compensação, decomposição); estimativa por arredondamento; prova real; problemas de juntar, tirar, comparar e completar.
Erros: esquecer o «vai um», tirar o menor do maior em cada coluna, errar as trocas quando há zeros (4.000 − 1.257).
"""
import random
import gen_br_matematica_5_adicao_e_subtracao as A5
from br_common import mcq, num, lesson, make_unit, mix, reais, armada, Kids

R = random.Random(80402)
K = Kids(R)
nc, smb = A5.no_carry_add, A5.small_minus_big


def s1_adicao():
    a = R.randint(1000, 60000)
    b = R.randint(100, 99999 - a)
    s = a + b
    if nc(a, b) == s:
        return None
    pic = armada([num(a), num(b)], "+") if R.random() < 0.5 else ""
    return mcq(pic + "Calcule %s + %s." % (num(a), num(b)), num(s), [num(nc(a, b)), num(s + 1000), num(s - 10), num(s + 100)],
               "Some coluna por coluna, da direita para a esquerda, e não esqueça o «vai um»: <b>%s</b>." % num(s))


def s1_tres():
    a, b, c = R.randint(1000, 30000), R.randint(1000, 30000), R.randint(100, 9000)
    s = a + b + c
    return mcq("Calcule %s + %s + %s." % (num(a), num(b), num(c)), num(s), [num(s - 1000), num(s + 1000), num(nc(nc(a, b), c)), num(s + 10)],
               "%s + %s = %s; %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b), num(a + b), num(c), num(s)))


def s2_subtracao():
    k = R.choice(["normal", "zeros", "normal"])
    if k == "zeros":
        a = R.choice([1000, 2000, 3000, 5000, 10000, 20000, 40000, 50000, 60000]) + R.choice([0, 0, 100, 1000])
    else:
        a = R.randint(10000, 99999)
    b = R.randint(100, a - 100)
    d = a - b
    w = smb(a, b)
    if w == d:
        return None
    pic = armada([num(a), num(b)], "−") if R.random() < 0.5 else ""
    return mcq(pic + "Calcule %s − %s." % (num(a), num(b)), num(d), [num(w), num(d + 1000), num(d - 10), num(d + 10)],
               "Quando o algarismo de cima for menor, troque 1 da ordem seguinte por 10. Prova real: %s + %s = %s. Resposta: <b>%s</b>." % (num(d), num(b), num(a), num(d)))


def s2_falta():
    a = R.randint(2000, 50000)
    b = R.randint(100, 40000)
    if R.random() < 0.5:
        return mcq("Que número somado a %s dá %s?" % (num(a), num(a + b)), num(b), [num(b + 1000), num(b + 10), num(smb(a + b, a)), num(b - 100) if b > 100 else num(b + 100)],
                   "Use a operação inversa: %s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    return mcq("De que número tiramos %s para ficar com %s?" % (num(b), num(a)), num(a + b), [num(abs(a - b)), num(a + b + 1000), num(nc(a, b)) if nc(a, b) != a + b else num(a + b - 100)],
               "Faça a operação inversa: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def s3_compensar():
    a = R.randint(120, 9800)
    k = R.choice([9, 99, 999, 8, 98, 998])
    if a < k:
        return None
    op = R.choice(["+", "−"])
    r = {9: 10, 8: 10, 99: 100, 98: 100, 999: 1000, 998: 1000}[k]
    d = r - k
    if op == "+":
        res = a + k
        return mcq("Calcule de cabeça: %s + %d." % (num(a), k), num(res), [num(a + r), num(a + r + d), num(res + 10)],
                   "Some %s e tire %d: %s + %s − %d = <b>%s</b>." % (num(r), d, num(a), num(r), d, num(res)))
    res = a - k
    return mcq("Calcule de cabeça: %s − %d." % (num(a), k), num(res), [num(a - r), num(a - r - d), num(res - 10)],
               "Tire %s e devolva %d: %s − %s + %d = <b>%s</b>." % (num(r), d, num(a), num(r), d, num(res)))


def s3_decompor():
    a = R.randint(11, 99) * 1000
    b = R.randint(11, 89) * 100
    op = R.choice(["+", "−"])
    if op == "+":
        res = a + b
        return mcq("Calcule de cabeça: %s + %s." % (num(a), num(b)), num(res), [num(a + b * 10), num(a + b // 10), num(res + 1000)],
                   "%s + %s = %s; depois some %s: <b>%s</b>." % (num(a), num(b // 1000 * 1000), num(a + b // 1000 * 1000), num(b % 1000), num(res)))
    res = a - b
    return mcq("Calcule de cabeça: %s − %s." % (num(a), num(b)), num(res), [num(a - b // 10), num(res + 1000), num(res - 1000), num(smb(a, b))],
               "%s − %s = %s; depois tire %s: <b>%s</b>." % (num(a), num(b // 1000 * 1000), num(a - b // 1000 * 1000), num(b % 1000), num(res)))


def s4_estimar():
    a = R.randint(10000, 60000)
    b = R.randint(10000, 35000)
    op = R.choice(["+", "−"])
    if a % 10000 // 1000 == 5 or b % 10000 // 1000 == 5 or (op == "−" and a < b):
        return None
    ra, rb = (a + 5000) // 10000 * 10000, (b + 5000) // 10000 * 10000
    e = ra + rb if op == "+" else ra - rb
    if e <= 0:
        return None
    ex = a + b if op == "+" else a - b
    opts = sorted({e + 10000, e - 10000 if e > 10000 else e + 20000, e + 30000})
    return mcq("Arredonde para a dezena de milhar mais próxima e estime %s %s %s." % (num(a), op, num(b)), "cerca de " + num(e), ["cerca de " + num(x) for x in opts if x != e],
               "%s ≈ %s e %s ≈ %s. %s %s %s = <b>%s</b> (a conta exata dá %s)." % (num(a), num(ra), num(b), num(rb), num(ra), op, num(rb), num(e), num(ex)))


def s4_prova():
    a = R.randint(5000, 90000)
    b = R.randint(1000, a - 1)
    d = a - b
    p = K.next()[0]
    if R.random() < 0.5:
        return mcq("%s fez %s − %s = %s. Qual conta serve de prova real?" % (p, num(a), num(b), num(d)), "%s + %s = %s" % (num(d), num(b), num(a)),
                   ["%s + %s = %s" % (num(a), num(b), num(a + b)), "%s − %s = %s" % (num(d), num(b), num(abs(d - b))), "%s + %s = %s" % (num(a), num(d), num(a + d))],
                   "Na subtração, a prova real é somar o resultado com o número que foi tirado: <b>%s + %s = %s</b>." % (num(d), num(b), num(a)))
    ok = R.random() < 0.5
    shown = d if ok else d + R.choice([1000, -1000, 100, 10])
    return mcq("%s fez %s − %s = %s. Usando a prova real, a conta está certa?" % (p, num(a), num(b), num(shown)),
               "Sim: %s + %s = %s" % (num(shown), num(b), num(a)) if ok else "Não: %s + %s = %s" % (num(shown), num(b), num(shown + b)),
               ["Não: %s + %s = %s" % (num(shown), num(b), num(shown + b + 1000)) if ok else "Sim: %s + %s = %s" % (num(shown), num(b), num(a)),
                "Só dá para saber fazendo a conta de novo", "Sim, porque o resultado é menor que %s" % num(a)],
               "Some o resultado com %s: %s + %s = %s%s. <b>%s</b>." % (num(b), num(shown), num(b), num(shown + b), "" if ok else " (diferente de %s)" % num(a), "Está certa" if ok else "Está errada; o certo é %s" % num(d)))


def s5_problema():
    k = R.choice(["compra", "troco", "estadio", "estoque", "livros", "comparar", "completar", "viagem"])
    p, g = K.next()
    if k == "compra":
        a, b = R.randint(300, 2500) * 100, R.randint(50, 900) * 100
        return mcq("%s comprou uma geladeira de %s e um micro-ondas de %s. Quanto gastou ao todo?" % (p, reais(a), reais(b)), reais(a + b),
                   [reais(abs(a - b)), reais(a + b + 10000), reais(nc(a, b)) if nc(a, b) != a + b else reais(a + b - 1000)], "%s + %s = <b>%s</b>." % (reais(a), reais(b), reais(a + b)))
    if k == "troco":
        nota = R.choice([10000, 20000, 50000])
        c = R.randint(nota // 500, nota // 100 - 1) * 100
        return mcq("%s pagou uma compra de %s com %s. Quanto recebeu de troco?" % (p, reais(c), reais(nota)), reais(nota - c),
                   [reais(nota + c), reais(nota - c + 1000), reais(smb(nota // 100, c // 100) * 100) if smb(nota // 100, c // 100) * 100 != nota - c else reais(nota - c - 100)],
                   "%s − %s = <b>%s</b>." % (reais(nota), reais(c), reais(nota - c)))
    if k == "estadio":
        a = R.randint(30, 78) * 1000 + R.randint(0, 999)
        b = R.randint(1000, 9000)
        return mcq("Um estádio tem %s lugares. Num jogo, %s lugares ficaram vazios. Quantas pessoas foram ao jogo?" % (num(a), num(b)), num(a - b),
                   [num(a + b), num(smb(a, b)) if smb(a, b) != a - b else num(a - b + 1000), num(a - b - 100)], "%s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    if k == "estoque":
        a = R.randint(20000, 60000)
        b, c = R.randint(1000, 9000), R.randint(1000, 9000)
        return mcq("Uma fábrica tinha %s garrafas. Vendeu %s e depois fabricou mais %s. Quantas garrafas ela tem agora?" % (num(a), num(b), num(c)), num(a - b + c),
                   [num(a + b + c), num(a - b - c), num(a + b - c)], "%s − %s + %s = <b>%s</b>." % (num(a), num(b), num(c), num(a - b + c)))
    if k == "livros":
        a, b = R.randint(5000, 30000), R.randint(2000, 20000)
        return mcq("A biblioteca da cidade tinha %s livros e recebeu uma doação de %s livros. Quantos livros tem agora?" % (num(a), num(b)), num(a + b),
                   [num(abs(a - b)), num(nc(a, b)) if nc(a, b) != a + b else num(a + b + 1000), num(a + b - 10)], "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "comparar":
        a, b = R.randint(20000, 90000), R.randint(10000, 80000)
        if a == b:
            return None
        A, B = R.sample(["Cuiabá", "Campo Grande", "Goiânia", "Palmas", "Teresina", "Natal", "Maceió", "Aracaju"], 2)
        return mcq("Num fim de semana, %s pessoas visitaram a feira de %s e %s pessoas visitaram a feira de %s. Quantas pessoas a mais visitaram a feira mais cheia?" % (num(a), A, num(b), B),
                   num(abs(a - b)), [num(a + b), num(smb(max(a, b), min(a, b))) if smb(max(a, b), min(a, b)) != abs(a - b) else num(abs(a - b) + 1000), num(abs(a - b) + 10)],
                   "Para comparar, subtraia: %s − %s = <b>%s</b>." % (num(max(a, b)), num(min(a, b)), num(abs(a - b))))
    if k == "completar":
        meta = R.choice([10000, 20000, 25000, 50000])
        tem = R.randint(meta // 10, meta - 100)
        return mcq("Uma escola quer juntar %s tampinhas para a reciclagem. Já juntou %s. Quantas faltam?" % (num(meta), num(tem)), num(meta - tem),
                   [num(meta + tem), num(smb(meta, tem)) if smb(meta, tem) != meta - tem else num(meta - tem + 1000), num(meta - tem - 100) if meta - tem > 100 else num(meta - tem + 100)],
                   "Quanto falta é uma subtração: %s − %s = <b>%s</b>." % (num(meta), num(tem), num(meta - tem)))
    a, b = R.randint(120, 980), R.randint(120, 980)
    return mcq("Numa viagem, um ônibus rodou %d km no primeiro dia e %d km no segundo. Quantos quilômetros rodou nos dois dias?" % (a, b), num(a + b) + " km",
               [num(abs(a - b)) + " km", num(nc(a, b)) + " km" if nc(a, b) != a + b else num(a + b + 100) + " km", num(a + b + 10) + " km"], "%d + %d = <b>%s km</b>." % (a, b, num(a + b)))


def main():
    seen = set()
    sets = [
        ("Adição com reagrupamento", mix(R, seen, [(s1_adicao, 14), (s1_tres, 6)])),
        ("Subtração com trocas", mix(R, seen, [(s2_subtracao, 14), (s2_falta, 6)])),
        ("Cálculo mental", mix(R, seen, [(s3_compensar, 12), (s3_decompor, 8)])),
        ("Estimativa e prova real", mix(R, seen, [(s4_estimar, 10), (s4_prova, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Na conta armada, coloque <b>unidade embaixo de unidade</b>, dezena embaixo de dezena… e calcule da direita para a esquerda.",
         "Quando a soma de uma coluna passa de 9, escreva as unidades e leve 1 para a coluna seguinte («vai um»).",
         "Na subtração, se o algarismo de cima for menor, troque 1 da ordem seguinte por 10. Com zeros, troque de mais longe.",
         "De cabeça, use números redondos: 3.457 + 99 = 3.457 + 100 − 1.",
         "Antes de calcular, estime; depois confira com a <b>prova real</b>."],
        [("Calcule 40.000 − 12.583.", ["troque 1 dezena de milhar e vá trocando até as unidades", "prova: 27.417 + 12.583 = 40.000"], "27.417"),
         ("Calcule de cabeça 6.240 − 98.", ["6.240 − 100 = 6.140", "devolva 2: 6.142"], "6.142")],
        [["Esquecer o «vai um»", "Escreva o 1 pequeno em cima da coluna seguinte."],
         ["Em cada coluna, tirar o menor do maior", "Se em cima é menor, troque 1 da ordem seguinte por 10."],
         ["Compensar para o lado errado: 6.240 − 98 = 6.140 − 2", "Tirou 100, que é 2 a mais: devolva 2."]],
        armada(["40.000", "12.583"], "−", result="27.417"))
    faq = [("O que o 4º ano faz com adição e subtração?", "A BNCC pede resolver e elaborar problemas de adição e subtração com números naturais, usando estratégias diversas, como cálculo, cálculo mental e algoritmos, além de fazer estimativas do resultado."),
           ("Como subtrair quando há zeros, como em 40.000 − 12.583?", "Troque 1 dezena de milhar por 10 unidades de milhar, depois 1 unidade de milhar por 10 centenas, e assim até as unidades. Confira com a prova real.")]
    make_unit(R, "adicao-e-subtracao", "N", ["EF04MA03"],
              "Resolver e elaborar problemas com números naturais envolvendo adição e subtração, utilizando estratégias diversas, como cálculo, cálculo mental e algoritmos, além de fazer estimativas do resultado",
              "Adição e subtração com números até 99.999", "Adição e subtração",
              "Atividades de matemática para o 4º ano sobre adição e subtração: conta armada com reagrupamento, trocas com zeros, cálculo mental, estimativa, prova real e problemas. 100 exercícios com gabarito.",
              "Calcule da direita para a esquerda, com trocas.", "Estime antes; confira com a prova real.",
              body, faq, sets, 2, grade="4-ano")


if __name__ == "__main__":
    main()
