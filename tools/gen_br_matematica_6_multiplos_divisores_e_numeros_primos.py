# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Múltiplos, divisores e números primos (Números, EF06MA04, EF06MA05)
  python3 tools/gen_br_matematica_6_multiplos_divisores_e_numeros_primos.py
Múltiplos e divisores; critérios de divisibilidade por 2, 3, 4, 5, 6, 9 e 10; números primos e compostos; decomposição em
fatores primos; fluxograma para decidir se um número é par ou ímpar; números de divisores.
Erros: achar que 1 é primo, usar o último algarismo para testar o 3 ou o 9, esquecer que todo número é múltiplo de si mesmo.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, bank, unit

R = random.Random(86003)
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def divs(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def isprime(n):
    return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))


def fat(n):
    out, p = [], 2
    while n > 1:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            out.append((p, e))
        p += 1
    return " × ".join(str(p) + (str(e).translate(SUP) if e > 1 else "") for p, e in out)


def s1_criterio():
    k = R.choice([2, 3, 4, 5, 6, 9, 10])
    ok = R.random() < 0.5
    while True:
        n = R.randint(100, 99999)
        if (n % k == 0) == ok:
            break
    regra = {2: "o último algarismo é par", 3: "a soma dos algarismos é múltiplo de 3", 4: "os dois últimos algarismos formam múltiplo de 4", 5: "termina em 0 ou 5",
             6: "é divisível por 2 e por 3", 9: "a soma dos algarismos é múltiplo de 9", 10: "termina em 0"}[k]
    s = sum(int(c) for c in str(n))
    extra = " (soma = %d)" % s if k in (3, 9, 6) else ""
    ans = "sim" if ok else "não"
    return M("O número %s é divisível por %d?" % (d(n), k), ans, ["não" if ok else "sim", "só se for par", "não dá para saber sem dividir"],
             "Divisível por %d quando %s%s: <b>%s</b>." % (k, regra, extra, ans))


def s2_divisores():
    n = R.choice([12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 72, 75, 80, 84, 90, 96, 100])
    ds = divs(n)
    k = R.choice(["lista", "quant", "mult"])
    if k == "lista":
        return M("Quais são todos os divisores de %d?" % n, ", ".join(map(str, ds)), [", ".join(map(str, ds[1:-1])), ", ".join(map(str, ds[:-1])), ", ".join(str(n * i) for i in range(1, 5))],
                 "Procure os pares que dão %d: <b>%s</b>." % (n, ", ".join(map(str, ds))))
    if k == "quant":
        return M("Quantos divisores tem o número %d?" % n, d(len(ds)), [d(len(ds) - 2), d(len(ds) + 1), d(len(ds) - 1)], "D(%d) = {%s}: <b>%d divisores</b>." % (n, ", ".join(map(str, ds)), len(ds)))
    a = R.randint(3, 15)
    return M("Quais são os 5 primeiros múltiplos de %d (sem contar o zero)?" % a, ", ".join(str(a * i) for i in range(1, 6)), [", ".join(str(x) for x in divs(a * 6)[:5]) if len(divs(a * 6)) >= 5 else ", ".join(str(a + i) for i in range(5)), ", ".join(str(a * i) for i in range(2, 7)), ", ".join(str(a + i * 2) for i in range(5))],
             "Multiplique %d por 1, 2, 3, 4 e 5: <b>%s</b>." % (a, ", ".join(str(a * i) for i in range(1, 6))))


def s3_primo():
    n = R.choice([R.randint(2, 100), R.choice([51, 57, 87, 91, 93, 39, 49, 77, 1, 2, 97, 89, 83, 79, 71, 61, 59, 53, 47, 43, 41, 37, 31, 29, 23])])
    if R.random() < 0.5:
        if n == 1:
            a, why = "nem primo nem composto", "1 tem um só divisor"
        elif isprime(n):
            a, why = "primo", "só tem os divisores 1 e %d" % n
        else:
            dv = next(k for k in range(2, n) if n % k == 0)
            a, why = "composto", "%d = %d × %d" % (n, dv, n // dv)
        return M("O número %d é primo ou composto?" % n, a, [x for x in ["primo", "composto", "nem primo nem composto", "primo e composto"] if x != a], "%s: <b>%s</b>." % (why[0].upper() + why[1:], a))
    lo = R.randint(1, 80)
    pr = [x for x in range(lo, lo + 20) if isprime(x)]
    if not pr:
        return None
    return M("Quantos números primos há de %d a %d?" % (lo, lo + 19), d(len(pr)), [d(len(pr) + 1), d(len(pr) - 1) if len(pr) > 1 else "3", d(len(pr) + 3)],
             "São %s: <b>%d</b>." % (", ".join(map(str, pr)), len(pr)))


def s4_fatorar():
    while True:
        n = 1
        for p in R.choices([2, 2, 2, 3, 3, 5, 7, 11], k=R.randint(3, 5)):
            n *= p
        if 30 <= n <= 2000:
            break
    f = fat(n)
    w = [fat(n * 2), fat(n // 2) + " × 2 × 2" if n % 2 == 0 else fat(n * 3), f.replace("2", "4", 1) if "2" in f else fat(n * 5)]
    if R.random() < 0.6:
        return M("Qual é a decomposição em fatores primos de %s?" % d(n), f, w, "Divida por primos (2, 3, 5, 7…) até chegar a 1: <b>%s</b>." % f)
    return M("Qual número tem a decomposição %s?" % f, d(n), [d(n * 2), d(n // 2) if n % 2 == 0 else d(n + 1), d(n + 10)], "Multiplique os fatores: <b>%s</b>." % d(n))


s5_conceitos = bank(R, [
    ("Qual é o menor número primo?", "2", ["1", "0", "3"]),
    ("Qual é o único número primo par?", "2", ["4", "0", "não existe"]),
    ("O número 1 é…", "nem primo nem composto", ["primo", "composto", "par"]),
    ("O zero é múltiplo de…", "todos os números naturais", ["nenhum número", "só do 1", "só dele mesmo"]),
    ("Todo número natural (maior que zero) é divisor de…", "si mesmo", ["zero apenas", "1", "nenhum número"]),
    ("Se 6 é divisor de 42, então 42 é ___ de 6.", "múltiplo", ["divisor", "fator primo", "quociente"]),
    ("Quantos múltiplos tem um número natural diferente de zero?", "infinitos", ["10", "o próprio número", "nenhum"]),
    ("Num fluxograma para saber se um número é par, a pergunta certa é…", "«O resto da divisão por 2 é 0?»", ["«O número é maior que 2?»", "«O número termina em 5?»", "«O número é primo?»"]),
    ("Num fluxograma de paridade, se o resto da divisão por 2 é 1, a saída é…", "«ímpar»", ["«par»", "«primo»", "«múltiplo de 2»"]),
    ("Um número divisível por 2 e por 5 também é divisível por…", "10", ["7", "25", "3"]),
    ("Um número divisível por 9 também é divisível por…", "3", ["6", "18", "2"]),
    ("Qual é o maior divisor de um número natural?", "o próprio número", ["1", "a metade do número", "não existe"]),
    ("Um número com exatamente dois divisores é…", "primo", ["composto", "par", "quadrado perfeito"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Critérios de divisibilidade", mix(R, seen, [(s1_criterio, 20)])),
        ("Múltiplos e divisores", mix(R, seen, [(s2_divisores, 20)])),
        ("Números primos", mix(R, seen, [(s3_primo, 20)])),
        ("Decomposição em fatores primos", mix(R, seen, [(s4_fatorar, 20)])),
        ("Conceitos e fluxogramas", mix(R, seen, [(s5_conceitos, 12), (s1_criterio, 4), (s3_primo, 4)])),
    ]
    body = lesson(
        ["Se a divisão de a por b é exata, b é <b>divisor</b> de a, e a é <b>múltiplo</b> de b: 6 é divisor de 42; 42 é múltiplo de 6.",
         "Critérios: por 2 (último algarismo par), por 3 (soma dos algarismos múltiplo de 3), por 4 (dois últimos algarismos), por 5 (termina em 0 ou 5), por 6 (por 2 e por 3), por 9 (soma múltiplo de 9), por 10 (termina em 0).",
         "Um número <b>primo</b> tem exatamente dois divisores: 1 e ele mesmo. O 1 não é primo nem composto.",
         "Todo número composto pode ser escrito como produto de primos: 60 = 2² × 3 × 5."],
        [("Divisores de 18", ["1 × 18, 2 × 9, 3 × 6"], "1, 2, 3, 6, 9, 18"),
         ("Fatorar 84", ["84 ÷ 2 = 42", "42 ÷ 2 = 21", "21 ÷ 3 = 7"], "2² × 3 × 7")],
        [["Achar que 1 é primo", "O 1 tem um só divisor."],
         ["Testar o 3 pelo último algarismo", "Para o 3 e o 9, some os algarismos."],
         ["Esquecer o próprio número na lista de divisores", "D(18) termina com 18."]])
    faq = [("Como saber se um número é primo?", "Tente dividir pelos primos 2, 3, 5, 7… até o número cujo quadrado passe do valor testado. Se nenhuma divisão for exata, o número é primo."),
           ("O que a BNCC pede no 6º ano?", "Classificar números em primos e compostos, estabelecer relações entre números (ser múltiplo de, ser divisor de) e conhecer critérios de divisibilidade por 2, 3, 4, 5, 6, 8, 9, 10, 100 e 1000 (EF06MA05), além de construir algoritmo em fluxograma para identificar números pares e ímpares (EF06MA04).")]
    unit(R, "multiplos-divisores-e-numeros-primos", "N", ["EF06MA04", "EF06MA05"],
         "Construir algoritmo em linguagem natural e representá-lo por fluxograma que indique a resolução de um problema simples (por exemplo, se um número natural qualquer é par); classificar números naturais em primos e compostos, estabelecer relações entre números, expressas pelos termos «é múltiplo de», «é divisor de», «é fator de», e estabelecer, por meio de investigações, critérios de divisibilidade",
         "Múltiplos, divisores e números primos", "Múltiplos, divisores e primos",
         "Atividades de matemática para o 6º ano sobre múltiplos, divisores, critérios de divisibilidade, números primos e compostos, decomposição em fatores primos e fluxogramas. 100 exercícios com gabarito.",
         "Primo: exatamente dois divisores.", "Use os critérios de divisibilidade antes de dividir.",
         body, faq, sets, 3, grade="6-ano")


if __name__ == "__main__":
    main()
