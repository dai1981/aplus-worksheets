# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Igualdade e partilha (Álgebra, EF06MA14, EF06MA15)
  python3 tools/gen_br_matematica_6_igualdade_e_partilha.py
A igualdade não se altera quando somamos, subtraímos, multiplicamos ou dividimos os dois membros pelo mesmo número; balanças;
achar o valor desconhecido; partilha de uma quantidade em duas partes desiguais (uma é o dobro, o triplo, ou uma é x a mais) e
partes proporcionais (razão entre as partes e entre uma parte e o todo).
Erros: mexer só de um lado da igualdade, dividir em partes iguais quando são desiguais, confundir parte/parte com parte/todo.
"""
import random
from br_common import lesson, mix, reais
from br_9 import M, d, bank, unit

R = random.Random(86011)


def s1_propriedade():
    a, b = R.randint(5, 40), R.randint(2, 9)
    c = a + b
    op, k = R.choice([("+", R.randint(2, 20)), ("−", R.randint(1, 5)), ("×", R.randint(2, 6)), ("÷", 1)])
    if op == "÷":
        k = R.choice([x for x in (2, 3, 4, 5) if c % x == 0] or [None])
        if k is None or a % k or b % k:
            return None
    left = "%d + %d" % (a, b)
    res = {"+": c + k, "−": c - k, "×": c * k, "÷": c // k}[op]
    return M("Sabendo que %s = %d, se fizermos <b>%s %d</b> nos dois membros, a igualdade fica…" % (left, c, op, k), "(%s) %s %d = %d" % (left, op, k, res),
             ["(%s) %s %d = %d" % (left, op, k, c), "%s = %d %s %d" % (left, c, op, k), "(%s) %s %d = %d" % (left, op, k, res + 1)],
             "Fazendo a mesma operação nos dois lados, a igualdade continua verdadeira: <b>(%s) %s %d = %d</b>." % (left, op, k, res))


def s2_desconhecido():
    x = R.randint(2, 30)
    k = R.choice(["+", "−", "×", "÷", "2p"])
    if k == "+":
        a = R.randint(3, 50)
        return M("Qual valor de □ torna verdadeira a igualdade □ + %d = %d?" % (a, x + a), d(x), [d(x + 2 * a), d(a), d(x + 1)], "Subtraia %d dos dois lados: □ = %d − %d = <b>%d</b>." % (a, x + a, a, x))
    if k == "−":
        a = R.randint(3, 50)
        return M("Qual valor de □ torna verdadeira a igualdade □ − %d = %d?" % (a, x), d(x + a), [d(x), d(abs(x - a)) if x != a else d(x + 1), d(x + a + 1)], "Some %d dos dois lados: □ = %d + %d = <b>%d</b>." % (a, x, a, x + a))
    if k == "×":
        a = R.randint(2, 12)
        return M("Qual valor de □ torna verdadeira a igualdade %d × □ = %d?" % (a, a * x), d(x), [d(a * x - a), d(a * x * a), d(x + a)], "Divida os dois lados por %d: □ = %d ÷ %d = <b>%d</b>." % (a, a * x, a, x))
    if k == "÷":
        a = R.randint(2, 9)
        return M("Qual valor de □ torna verdadeira a igualdade □ ÷ %d = %d?" % (a, x), d(a * x), [d(x), d(x + a), d(a * x + a)], "Multiplique os dois lados por %d: □ = <b>%d</b>." % (a, a * x))
    a, b = R.randint(2, 6), R.randint(1, 20)
    return M("Qual valor de □ torna verdadeira a igualdade %d × □ + %d = %d?" % (a, b, a * x + b), d(x), [d(a * x + b - b), d((a * x + b) // a) if (a * x + b) // a != x else d(x + 1), d(x + b)],
             "Tire %d dos dois lados: %d × □ = %d; divida por %d: □ = <b>%d</b>." % (b, a, a * x, a, x))


def s3_balanca():
    x = R.randint(2, 15)
    n, m = R.randint(2, 4), R.randint(1, 20)
    tot = n * x + m
    return M("Numa balança em equilíbrio, de um lado há %d caixas iguais e um peso de %d kg; do outro, %d kg. Quanto pesa cada caixa?" % (n, m, tot), "%d kg" % x, ["%d kg" % (tot // n), "%d kg" % (tot - m), "%d kg" % (x + 2)] if tot % n else ["%d kg" % (tot // n + 1), "%d kg" % (tot - m), "%d kg" % (x + 2)],
             "Tire %d kg dos dois lados: %d caixas = %d kg; cada caixa: %d ÷ %d = <b>%d kg</b>." % (m, n, n * x, n * x, n, x))


def s4_partilha():
    k = R.choice(["dobro", "triplo", "mais", "razao"])
    a, b = None, None
    if k == "dobro" or k == "triplo":
        t = 2 if k == "dobro" else 3
        p = R.randint(10, 200)
        tot = p * (t + 1)
        return M("Ana e Bia dividiram %s de modo que Bia ficou com o %s do que ficou Ana. Quanto ficou com Ana?" % (reais(tot * 100), k), reais(p * 100), [reais(tot // 2 * 100), reais(p * t * 100), reais(tot // t * 100)],
                 "Ana tem 1 parte e Bia %d partes: %d partes ao todo; %d ÷ %d = <b>%s</b>." % (t, t + 1, tot, t + 1, reais(p * 100)))
    if k == "mais":
        p, e = R.randint(10, 150), R.randint(5, 60)
        tot = 2 * p + e
        return M("Dois irmãos dividiram %s. O mais velho recebeu %s a mais que o mais novo. Quanto recebeu o mais novo?" % (reais(tot * 100), reais(e * 100)), reais(p * 100), [reais(tot * 50) if tot % 2 == 0 else reais((p + e) * 100), reais((p + e) * 100), reais((tot - e) * 100)],
                 "Tire a diferença: %d − %d = %d; divida por 2: <b>%s</b>." % (tot, e, 2 * p, reais(p * 100)))
    r1, r2 = R.choice([(1, 2), (2, 3), (1, 3), (3, 5), (2, 5), (1, 4), (3, 4)])
    u = R.randint(5, 40)
    tot = (r1 + r2) * u
    return M("Uma receita usa farinha e açúcar na razão %d para %d (%d partes de farinha para %d de açúcar). Em %d g da mistura, quanto há de farinha?" % (r1, r2, r1, r2, tot), "%d g" % (r1 * u),
             ["%d g" % (r2 * u), "%d g" % (tot // 2) if tot % 2 == 0 else "%d g" % (tot // r2 if tot % r2 == 0 else r1 * u + 5), "%d g" % (tot * r1 // r2) if (tot * r1) % r2 == 0 else "%d g" % (r1 * u + u)],
             "São %d + %d = %d partes; cada parte = %d ÷ %d = %d g; farinha: %d × %d = <b>%d g</b> (%d/%d do total)." % (r1, r2, r1 + r2, tot, r1 + r2, u, r1, u, r1 * u, r1, r1 + r2))


s5_conceitos = bank(R, [
    ("Se 3 + 5 = 8, então 3 + 5 + 10 = 8 + 10. Essa ideia é…", "fazer a mesma operação nos dois membros", ["mudar só um membro", "trocar os membros de sinal", "uma igualdade falsa"]),
    ("Numa balança equilibrada, se tirarmos 2 kg de um prato só, a balança…", "desequilibra", ["continua equilibrada", "fica com o dobro", "não muda nunca"]),
    ("Numa partilha na razão 2 para 3, a primeira parte representa que fração do total?", "2/5", ["2/3", "3/5", "1/2"]),
    ("Dividir 60 em duas partes em que uma é o dobro da outra dá…", "20 e 40", ["30 e 30", "30 e 60", "15 e 45"]),
    ("Dividir 60 em duas partes em que uma tem 10 a mais que a outra dá…", "25 e 35", ["30 e 40", "20 e 40", "10 e 50"]),
    ("Se 4 × □ = 36, então □ = 36 ÷ 4. Que propriedade usamos?", "dividir os dois membros por 4", ["subtrair 4 dos dois membros", "somar 4", "multiplicar só um membro"]),
    ("A razão entre 6 meninas e 9 meninos de um grupo é…", "2 para 3", ["3 para 2", "6 para 15", "1 para 3"]),
    ("A razão entre 6 meninas e o total de 15 alunos é…", "2/5", ["2/3", "3/5", "6/9"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("A igualdade e suas propriedades", mix(R, seen, [(s1_propriedade, 14), (s5_conceitos, 6)])),
        ("O valor desconhecido", mix(R, seen, [(s2_desconhecido, 20)])),
        ("Balanças", mix(R, seen, [(s3_balanca, 14), (s2_desconhecido, 6)])),
        ("Partilha em partes desiguais", mix(R, seen, [(s4_partilha, 20)])),
        ("Revisão", mix(R, seen, [(s4_partilha, 10), (s3_balanca, 6), (s1_propriedade, 4)])),
    ]
    body = lesson(
        ["Uma <b>igualdade</b> continua verdadeira quando fazemos a mesma operação nos dois membros, como numa balança equilibrada.",
         "Isso ajuda a achar o valor desconhecido: em 3 × □ + 4 = 19, tire 4 dos dois lados (3 × □ = 15) e divida por 3 (□ = 5).",
         "<b>Partilha desigual</b>: conte as partes. Se uma pessoa recebe o dobro da outra, são 1 + 2 = 3 partes.",
         "Na razão 2 para 3, as partes são 2 e 3, e o todo tem 5 partes: a primeira é 2/5 do total."],
        [("90 em partes 1 e 2", ["3 partes", "90 ÷ 3 = 30"], "30 e 60"),
         ("100 em duas partes, uma com 20 a mais", ["100 − 20 = 80", "80 ÷ 2 = 40"], "40 e 60")],
        [["Mexer só de um lado", "Faça a mesma operação nos dois membros."],
         ["Dividir em partes iguais", "Conte quantas partes cada um recebe."],
         ["Confundir parte/parte com parte/todo", "2 para 3 é 2/5 do total, não 2/3."]])
    faq = [("O que é partilha em partes desiguais?", "É dividir uma quantidade em partes que não são iguais, por exemplo quando uma pessoa recebe o dobro da outra. Conte as partes (1 + 2 = 3), divida o total por esse número e multiplique."),
           ("O que a BNCC pede no 6º ano?", "Reconhecer que a relação de igualdade não se altera quando se adiciona, subtrai, multiplica ou divide os seus dois membros por um mesmo número (EF06MA14) e resolver problemas de partilha de uma quantidade em duas partes desiguais (EF06MA15).")]
    unit(R, "igualdade-e-partilha", "A", ["EF06MA14", "EF06MA15"],
         "Reconhecer que a relação de igualdade matemática não se altera ao adicionar, subtrair, multiplicar ou dividir os seus dois membros por um mesmo número e utilizar essa noção para determinar valores desconhecidos na resolução de problemas; resolver e elaborar problemas que envolvam a partilha de uma quantidade em duas partes desiguais, envolvendo relações aditivas e multiplicativas, bem como a razão entre as partes e entre uma das partes e o todo",
         "Igualdade e partilha em partes desiguais", "Igualdade e partilha",
         "Atividades de matemática para o 6º ano sobre igualdade e partilha: propriedades da igualdade, valor desconhecido, balanças, partilha em partes desiguais e razão entre as partes. 100 exercícios com gabarito.",
         "O que faz de um lado, faça do outro.", "Na partilha, conte as partes.",
         body, faq, sets, 11, grade="6-ano")


if __name__ == "__main__":
    main()
