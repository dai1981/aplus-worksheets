# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Frações (Números, EF06MA07)
  python3 tools/gen_br_matematica_6_fracoes.py
Fração como parte de um todo e como quociente; frações próprias, impróprias e números mistos; frações equivalentes,
simplificação e fração irredutível; comparar e ordenar frações (mesmo denominador, mesmo numerador, denominadores diferentes); reta numérica.
Erros: achar que 1/5 &gt; 1/3 porque 5 &gt; 3, somar o mesmo número ao numerador e ao denominador para achar equivalente, contar partes desiguais.
"""
import random
from math import gcd
from fractions import Fraction as F
from br_common import lesson, mix, disco, faixa
from br_9 import M, d, fq, bank, unit

R = random.Random(86005)


def s1_figura():
    den = R.choice([3, 4, 5, 6, 8, 10, 12])
    k = R.randint(1, den - 1)
    pic = R.choice([disco, faixa])(den, k)
    return M(pic + "Que fração da figura está pintada?", fq(F(k, den)) if gcd(k, den) == 1 else "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (k, den),
             ["<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (den - k, den), "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (k, den - k), "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (den, k)],
             "A figura tem %d partes iguais e %d estão pintadas: <b>%d/%d</b>." % (den, k, k, den))


def s2_tipos():
    k = R.choice(["misto", "impropria", "quociente", "classe"])
    if k == "misto":
        den = R.randint(2, 9)
        w, n = R.randint(1, 5), R.randint(1, den - 1)
        num = w * den + n
        return M("Qual número misto é igual a %s?" % fq(F(num, den)) if gcd(num, den) == 1 else None, "%d %s" % (w, fq(F(n, den))) if gcd(n, den) == 1 else None,
                 ["%d %s" % (n, fq(F(w, den))) if gcd(w, den) == 1 and w < den else "%d %s" % (w + 1, fq(F(n, den))), "%d %s" % (w - 1, fq(F(n, den))) if w > 1 else "%d %s" % (w + 2, fq(F(n, den))), "%d %s" % (num // 10 + 1, fq(F(n, den)))],
                 "%d ÷ %d = %d e resto %d: <b>%d %d/%d</b>." % (num, den, w, n, w, n, den)) if gcd(num, den) == 1 and gcd(n, den) == 1 else None
    if k == "impropria":
        den = R.randint(2, 9)
        w, n = R.randint(1, 5), R.randint(1, den - 1)
        if gcd(n, den) != 1:
            return None
        num = w * den + n
        return M("Escreva %d %s como fração imprópria." % (w, fq(F(n, den))), fq(F(num, den)), [fq(F(w * n + den, den)) if gcd(w * n + den, den) == 1 else fq(F(w + n, den)), fq(F(w + n, den)) if gcd(w + n, den) == 1 else fq(F(num + 1, den)), fq(F(num, n)) if n > 1 else fq(F(num + den, den))],
                 "%d × %d + %d = %d: <b>%d/%d</b>." % (w, den, n, num, num, den))
    if k == "quociente":
        a, b = R.randint(1, 9), R.randint(2, 9)
        if a % b == 0 or gcd(a, b) != 1:
            return None
        return M("%d pizzas iguais foram divididas igualmente entre %d pessoas. Que fração de pizza cada uma recebe?" % (a, b), fq(F(a, b)), [fq(F(b, a)) if a > 1 else str(b), fq(F(1, b)) if a > 1 else fq(F(1, a + b)), fq(F(a, a + b))],
                 "A fração é o quociente: %d ÷ %d = <b>%d/%d</b>." % (a, b, a, b))
    n, den = R.randint(1, 15), R.randint(2, 9)
    if n == den:
        return None
    a = "própria (menor que 1)" if n < den else "imprópria (maior que 1)"
    return M("A fração %s é…" % fq(F(n, den)) if gcd(n, den) == 1 else None, a, [x for x in ["própria (menor que 1)", "imprópria (maior que 1)", "igual a 1", "negativa"] if x != a],
             "Compare o numerador %d com o denominador %d: <b>%s</b>." % (n, den, a)) if gcd(n, den) == 1 else None


def s3_equivalentes():
    a, b = R.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6), (5, 6), (3, 8), (5, 8), (4, 9), (7, 10)])
    k = R.choice(["falta", "simp", "qual"])
    m = R.randint(2, 8)
    fr = lambda n, dd: "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, dd)
    if k == "falta":
        return M("Complete: %s = %s" % (fr(a, b), fr("?", b * m)), d(a * m), [d(a + b * m - b), d(a * m + 1), d(b * m - a)], "%d × %d = %d, então ? = %d × %d = <b>%d</b>." % (b, m, b * m, a, m, a * m))
    if k == "simp":
        return M("Simplifique %s até a fração irredutível." % fr(a * m, b * m), fr(a, b), [fr(a * m // gcd(m, 2) if m % 2 == 0 else a * 2, b * m // gcd(m, 2) if m % 2 == 0 else b * 2) if fr(a * m // gcd(m, 2), b * m // gcd(m, 2)) != fr(a, b) else fr(a + 1, b), fr(b, a) if a > 1 else fr(a, b + 1), fr(a * m - 1, b * m - 1)],
                 "Divida numerador e denominador pelo MDC, %d: <b>%d/%d</b>." % (gcd(a * m, b * m), a, b))
    ws = [fr(a + m, b + m), fr(a * m, b * m + 1), fr(a * m + 1, b * m)]
    return M("Qual fração é equivalente a %s?" % fr(a, b), fr(a * m, b * m), ws, "Multiplique numerador e denominador por %d: <b>%d/%d</b>. (Somar o mesmo número não dá fração equivalente.)" % (m, a * m, b * m))


def s4_comparar():
    k = R.choice(["mesmo_den", "mesmo_num", "dif", "ordem"])
    if k == "mesmo_den":
        den = R.randint(5, 12)
        a, b = R.sample(range(1, den), 2)
        x, y = F(a, den), F(b, den)
    elif k == "mesmo_num":
        n = R.randint(1, 5)
        a, b = R.sample(range(n + 1, 13), 2)
        x, y = F(n, a), F(n, b)
    else:
        x, y = F(R.randint(1, 8), R.randint(2, 9)), F(R.randint(1, 8), R.randint(2, 9))
    if x == y or x >= 1 or y >= 1:
        return None
    if k == "ordem":
        z = F(R.randint(1, 8), R.randint(2, 9))
        if z in (x, y) or z >= 1:
            return None
        xs = sorted([x, y, z])
        sh = [x, y, z]
        return M("Qual é a ordem crescente de %s?" % "; ".join(fq(t) for t in sh), " &lt; ".join(fq(t) for t in xs), [" &lt; ".join(fq(t) for t in xs[::-1]), " &lt; ".join(fq(t) for t in [xs[1], xs[0], xs[2]]), " &lt; ".join(fq(t) for t in [xs[0], xs[2], xs[1]])],
                 "Em decimal: %s. Ordem: <b>%s</b>." % ("; ".join(d(t, 2) + "…" if (t * 100).denominator != 1 else d(t) for t in xs), " &lt; ".join(fq(t) for t in xs)))
    big = max(x, y)
    return M("Qual é a maior fração: %s ou %s?" % (fq(x), fq(y)), fq(big), [fq(min(x, y)), "são iguais", "não dá para comparar"],
             ("Mesmo denominador: maior numerador. " if k == "mesmo_den" else "Mesmo numerador: menor denominador, partes maiores. " if k == "mesmo_num" else "Reduza ao mesmo denominador. ") + "Maior: <b>%s</b>." % fq(big))


s5_conceitos = bank(R, [
    ("Na fração 3/8, o denominador indica…", "em quantas partes iguais o inteiro foi dividido", ["quantas partes foram tomadas", "o resultado da divisão", "a parte que sobrou"]),
    ("Uma fração com numerador igual ao denominador vale…", "1 inteiro", ["0", "a metade", "2 inteiros"]),
    ("Qual fração é maior: 1/3 ou 1/5?", "1/3", ["1/5", "são iguais", "não dá para saber"]),
    ("Somando 1 ao numerador e 1 ao denominador de 2/3, obtemos uma fração…", "que não é equivalente a 2/3", ["equivalente a 2/3", "igual a 1", "imprópria"]),
    ("Uma fração é irredutível quando…", "o MDC do numerador e do denominador é 1", ["o numerador é 1", "o denominador é par", "é menor que 1"]),
    ("Qual fração está entre 0 e 1 na reta numérica?", "5/7", ["7/5", "9/4", "3/1"]),
    ("A fração 12/4 é igual a…", "3", ["4", "1/3", "8"]),
    ("Para comparar 3/4 e 5/6, é útil escrevê-las com denominador…", "12", ["10", "24/4", "9"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Fração de uma figura", mix(R, seen, [(s1_figura, 20)])),
        ("Própria, imprópria, mista e quociente", mix(R, seen, [(s2_tipos, 20)])),
        ("Frações equivalentes", mix(R, seen, [(s3_equivalentes, 20)])),
        ("Comparar e ordenar", mix(R, seen, [(s4_comparar, 20)])),
        ("Revisão", mix(R, seen, [(s5_conceitos, 8), (s3_equivalentes, 6), (s4_comparar, 6)])),
    ]
    body = lesson(
        ["Na fração a/b, o <b>denominador</b> b diz em quantas partes iguais o inteiro foi dividido, e o <b>numerador</b> a diz quantas partes foram tomadas.",
         "Uma fração também é uma divisão: 3/4 = 3 ÷ 4. Se o numerador é maior que o denominador, a fração é imprópria e pode virar número misto: 7/3 = 2 1/3.",
         "<b>Frações equivalentes</b> representam a mesma quantidade: multiplique ou divida numerador e denominador pelo mesmo número.",
         "Para comparar, reduza ao mesmo denominador. Com o mesmo numerador, a fração de menor denominador é a maior."],
        [("Simplificar 18/24", ["MDC(18, 24) = 6", "18 ÷ 6 e 24 ÷ 6"], "3/4"),
         ("Comparar 2/3 e 3/5", ["2/3 = 10/15", "3/5 = 9/15"], "2/3 &gt; 3/5")],
        [["Achar que 1/5 é maior que 1/3", "Mais partes, partes menores."],
         ["Somar o mesmo número em cima e embaixo", "Para equivalentes, multiplique ou divida."],
         ["Contar partes de tamanhos diferentes", "As partes precisam ser iguais."]],
        disco(8, 3))
    faq = [("O que é uma fração equivalente?", "É outra fração que representa a mesma quantidade, obtida multiplicando ou dividindo o numerador e o denominador pelo mesmo número: 2/3 = 4/6 = 6/9."),
           ("O que a BNCC pede no 6º ano sobre frações?", "Compreender, comparar e ordenar frações associadas às ideias de partes de inteiros e resultado de divisão, identificando frações equivalentes (EF06MA07).")]
    unit(R, "fracoes", "N", ["EF06MA07"],
         "Compreender, comparar e ordenar frações associadas às ideias de partes de inteiros e resultado de divisão, identificando frações equivalentes",
         "Frações: parte do inteiro, equivalência e comparação", "Frações",
         "Atividades de matemática para o 6º ano sobre frações: parte de um inteiro, fração como divisão, frações próprias e impróprias, números mistos, frações equivalentes, simplificação e comparação. 100 exercícios com gabarito.",
         "Multiplicar ou dividir em cima e embaixo pelo mesmo número não muda a fração.", "Para comparar, use o mesmo denominador.",
         body, faq, sets, 5, grade="6-ano")


if __name__ == "__main__":
    main()
