# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Introdução à programação (EM13MAT405)
  python3 tools/gen_br_matematica_em3_programacao.py
Ler programas curtos em Python: variáveis e atribuição, operações (//, %, **), condicionais (if/else), laços (for, while),
listas e funções simples; prever a saída e completar programas para tarefas matemáticas (somas, médias, tabuada, múltiplos).
Erros: achar que range(1, n) inclui n, confundir = (atribuição) e == (comparação), esquecer que // é divisão inteira.
"""
import random
from br_em import M, d, bank, mix, lesson, unit, num, code
from fractions import Fraction as F

R = random.Random(93009)


def s1_saida():
    k = R.choice(["atrib", "ops", "if", "for", "while", "lista"])
    if k == "atrib":
        a, b = R.randint(2, 9), R.randint(2, 9)
        c = code("a = %d" % a, "b = %d" % b, "a = a + b", "b = a * 2", "print(b)")
        return M(c + "O que o programa mostra?", str((a + b) * 2), [str(a * 2), str(b * 2), str(a + b)], "a vira %d; b = %d · 2 = <b>%d</b>." % (a + b, a + b, (a + b) * 2))
    if k == "ops":
        a, b = R.randint(10, 60), R.randint(3, 9)
        op = R.choice(["//", "%", "**"])
        if op == "**":
            a, b = R.randint(2, 5), R.randint(2, 4)
            v = a ** b
            return M(code("print(%d ** %d)" % (a, b)) + "O que o programa mostra?", str(v), [str(a * b), str(b ** a), str(a + b)], "** é potência: %d%s = <b>%d</b>." % (a, "²³⁴"[b - 2], v))
        v = a // b if op == "//" else a % b
        w = [str(a % b) if op == "//" else str(a // b), d(F(a, b), 2), str(a * b)]
        return M(code("print(%d %s %d)" % (a, op, b)) + "O que o programa mostra?", str(v), w, "%s: <b>%d</b>." % ("// é o quociente inteiro" if op == "//" else "% é o resto da divisão", v))
    if k == "if":
        n = R.randint(1, 40)
        lim = R.choice([10, 18, 20, 25])
        c = code("n = %d" % n, "if n >= %d:" % lim, "    print('A')", "else:", "    print('B')")
        return M(c + "O que o programa mostra?", "A" if n >= lim else "B", ["B" if n >= lim else "A", "AB", "nada"], "%d %s %d: <b>%s</b>." % (n, "≥" if n >= lim else "&lt;", lim, "A" if n >= lim else "B"))
    if k == "for":
        a, b = R.randint(1, 4), R.randint(5, 10)
        t = R.choice(["soma", "conta", "mult"])
        if t == "soma":
            c = code("s = 0", "for i in range(%d, %d):" % (a, b), "    s = s + i", "print(s)")
            v = sum(range(a, b))
            return M(c + "O que o programa mostra?", str(v), [str(sum(range(a, b + 1))), str(b - a), str(sum(range(a + 1, b)))], "range(%d, %d) vai de %d a %d: soma <b>%d</b>." % (a, b, a, b - 1, v))
        if t == "conta":
            c = code("c = 0", "for i in range(%d):" % b, "    c = c + 2", "print(c)")
            return M(c + "O que o programa mostra?", str(2 * b), [str(2 * (b - 1)), str(b), str(2 * (b + 1))], "range(%d) repete %d vezes: <b>%d</b>." % (b, b, 2 * b))
        c = code("p = 1", "for i in range(1, %d):" % (a + 3), "    p = p * i", "print(p)")
        import math
        return M(c + "O que o programa mostra?", str(math.factorial(a + 2)), [str(math.factorial(a + 3)), str(sum(range(1, a + 3))), str(a + 2)], "1 · 2 · … · %d = <b>%d</b>." % (a + 2, math.factorial(a + 2)))
    if k == "while":
        x, lim = R.randint(1, 5), R.choice([30, 50, 100])
        c = code("x = %d" % x, "while x < %d:" % lim, "    x = x * 3", "print(x)")
        v = x
        while v < lim:
            v *= 3
        return M(c + "O que o programa mostra?", str(v), [str(v // 3), str(lim), str(v * 3)], "Multiplica por 3 até passar de %d: <b>%d</b>." % (lim, v))
    xs = R.sample(range(1, 30), 5)
    t = R.choice(["len", "sum", "max", "idx"])
    if t == "idx":
        i = R.randint(0, 4)
        return M(code("v = %s" % str(xs), "print(v[%d])" % i) + "O que o programa mostra?", str(xs[i]), [str(xs[i - 1]) if i else str(xs[1]), str(xs[(i + 1) % 5]), str(i)], "Os índices começam em 0: v[%d] = <b>%d</b>." % (i, xs[i]))
    v = {"len": len(xs), "sum": sum(xs), "max": max(xs)}[t]
    return M(code("v = %s" % str(xs), "print(%s(v))" % t) + "O que o programa mostra?", str(v), [str({"len": sum(xs), "sum": max(xs), "max": min(xs)}[t]), str(xs[-1]) if xs[-1] != v else str(v + 1), str(len(xs) + 1) if t != "len" else str(xs[0])],
             "%s: <b>%d</b>." % ({"len": "len dá a quantidade de elementos", "sum": "sum soma os elementos", "max": "max dá o maior"}[t], v))


def s2_completar():
    q, a, w = R.choice([
        ("Qual linha completa o programa para mostrar se n é par?" + code("n = int(input())", "if ______:", "    print('par')"), "n % 2 == 0", ["n / 2 == 0", "n % 2 = 0", "n // 2 == 1"]),
        ("Qual linha completa o programa para mostrar a tabuada do 7 (7, 14, …, 70)?" + code("for i in range(1, 11):", "    ______"), "print(7 * i)", ["print(7 + i)", "print(i)", "print(7 ** i)"]),
        ("Qual linha completa o programa para calcular a média de três notas a, b e c?" + code("a, b, c = 6, 8, 7", "media = ______", "print(media)"), "(a + b + c) / 3", ["a + b + c / 3", "(a + b + c) // 3", "a + b + c * 3"]),
        ("Qual comando repete um bloco 10 vezes?", "for i in range(10):", ["for i in range(1, 10):", "if i < 10:", "while i = 10:"]),
        ("Qual linha completa o programa para somar os números de 1 a 100?" + code("s = 0", "for i in range(______):", "    s = s + i"), "1, 101", ["1, 100", "100", "0, 100"]),
        ("Qual condição testa se x é múltiplo de 5?", "x % 5 == 0", ["x / 5 == 0", "x // 5 == 0", "x * 5 == 0"]),
        ("Qual linha calcula a área de um círculo de raio r (com pi = 3.14)?", "area = 3.14 * r ** 2", ["area = 3.14 * 2 * r", "area = 3.14 * r * 2", "area = (3.14 * r) ** 2"]),
        ("Qual linha completa a função que devolve o dobro de x?" + code("def dobro(x):", "    ______"), "return 2 * x", ["print(x)", "return x + x * x", "x = 2"]),
        ("Em Python, qual símbolo compara se dois valores são iguais?", "==", ["=", "!=", "=>"]),
        ("Qual comando lê um número inteiro digitado pelo usuário?", "n = int(input())", ["n = input(int)", "print(n)", "n == input()"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a.replace("<", "&lt;"))


def s3_funcao():
    a, b = R.randint(2, 6), R.choice([x_ for x_ in range(-5, 10) if x_])
    x = R.randint(-3, 6)
    k = R.choice(["lin", "quad", "cond"])
    if k == "lin":
        c = code("def f(x):", "    return %d * x %s %d" % (a, "+" if b >= 0 else "-", abs(b)), "print(f(%d))" % x)
        v = a * x + b
        return M(c + "O que o programa mostra?", d(v), [d(a * x - b) if b else d(v + 1), d(a + x + b), d(a * (x + b))], "f(%d) = %d · %s %s %d = <b>%s</b>." % (x, a, "(%d)" % x if x < 0 else str(x), "+" if b >= 0 else "−", abs(b), d(v)))
    if k == "quad":
        c = code("def g(x):", "    return x ** 2 - %d" % a, "print(g(%d))" % x)
        v = x * x - a
        return M(c + "O que o programa mostra?", d(v), [d(2 * x - a), d(-x * x - a), d(x * x + a)], "g(%d) = %d − %d = <b>%s</b>." % (x, x * x, a, d(v)))
    c = code("def h(x):", "    if x > 0:", "        return x", "    else:", "        return -x", "print(h(%d))" % x)
    return M(c + "O que o programa mostra?", d(abs(x)), [d(-abs(x)) if x else "1", d(x * x) if x * x != abs(x) else "2", "0" if x else "1"], "h é o valor absoluto: <b>%s</b>." % d(abs(x)))


def main():
    seen = set()
    sets = [
        ("Variáveis e operações", mix(R, seen, [(s1_saida, 20)])),
        ("Condicionais e laços", mix(R, seen, [(s1_saida, 20)])),
        ("Funções", mix(R, seen, [(s3_funcao, 20)])),
        ("Completar programas", mix(R, seen, [(s2_completar, 10), (s3_funcao, 10)])),
        ("Revisão", mix(R, seen, [(s1_saida, 20)])),
    ]
    body = lesson(
        ["Um programa executa instruções em ordem. <b>x = 5</b> guarda 5 em x (atribuição); <b>x == 5</b> pergunta se x vale 5 (comparação).",
         "Operações em Python: + − * /, <b>//</b> (quociente inteiro), <b>%</b> (resto), <b>**</b> (potência).",
         "<b>if/else</b> escolhe um caminho. <b>for i in range(a, b)</b> repete com i de a até b − 1. <b>while</b> repete enquanto a condição for verdadeira.",
         "<b>def</b> cria uma função; <b>return</b> devolve o resultado."],
        [("for i in range(1, 5): s = s + i (s começa em 0)", ["i = 1, 2, 3, 4"], "s = 10"),
         ("print(17 // 5, 17 % 5)", ["17 = 3 · 5 + 2"], "3 2")],
        [["Achar que range(1, n) inclui n", "Vai até n − 1."],
         ["Usar = para comparar", "Comparação é ==."],
         ["Confundir / e //", "17 / 5 = 3.4; 17 // 5 = 3."]])
    faq = [("Por que range(1, 10) não inclui o 10?", "Em Python, range(a, b) começa em a e para antes de b. Para ir de 1 a 10, use range(1, 11)."),
           ("O que a BNCC pede?", "Utilizar conceitos iniciais de uma linguagem de programação na implementação de algoritmos escritos em linguagem corrente e/ou matemática (EM13MAT405).")]
    unit(R, "introducao-a-programacao", "A", ["EM13MAT405"],
         "Utilizar conceitos iniciais de uma linguagem de programação na implementação de algoritmos escritos em linguagem corrente e/ou matemática",
         "Introdução à programação com Python", "Introdução à programação",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre programação em Python: variáveis, operações, condicionais, laços for e while, listas e funções. 100 exercícios com gabarito.",
         "range(a, b) vai de a até b − 1", "= atribui; == compara.",
         body, faq, sets, 9, grade="3-serie")


if __name__ == "__main__":
    main()
