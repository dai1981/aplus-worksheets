# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Dízimas periódicas e fração geratriz (Números, EF08MA05)
  python3 tools/gen_br_matematica_8_dizimas_periodicas.py
Decimais exatos e dízimas periódicas a partir de frações (quando o denominador só tem fatores 2 e 5, o decimal é exato); período;
dízimas simples (0,777… = 7/9; 0,2727… = 27/99) e compostas (0,1666… = 15/90 = 1/6); fração geratriz; comparar dízimas.
Erros: 0,333… = 3/10, esquecer de tirar a parte que não se repete na dízima composta, chamar 0,25 de dízima.
"""
import random
from math import gcd
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, bank, unit

R = random.Random(88005)


def dz(x, n=6):
    """dízima com 6 casas e reticências"""
    ip = int(x)
    r = x - ip
    s = ""
    for _ in range(n):
        r *= 10
        s += str(int(r))
        r -= int(r)
    return "%d,%s…" % (ip, s)


def s1_exata_ou():
    b = R.choice([2, 4, 5, 8, 10, 16, 20, 25, 40, 3, 6, 7, 9, 11, 12, 15, 30, 45])
    a = R.randint(1, b - 1)
    if gcd(a, b) != 1:
        return None
    f = F(a, b)
    only25 = all(p in (2, 5) for p in [q for q in range(2, b + 1) if b % q == 0 and all(q % r for r in range(2, q))])
    ans = "decimal exato" if only25 else "dízima periódica"
    return M("A fração %s, escrita como decimal, é…" % fq(f), ans, ["dízima periódica" if only25 else "decimal exato", "número irracional", "número inteiro"],
             "O denominador %d %s: <b>%s</b>%s." % (b, "só tem os fatores primos 2 e 5" if only25 else "tem fator primo diferente de 2 e 5", ans, " (%s)" % d(f) if only25 else " (%s)" % dz(f)))


def s2_simples():
    k = R.choice([1, 2])
    if k == 1:
        a = R.randint(1, 8)
        f = F(a, 9)
        return M("Qual é a fração geratriz de %s (o %d se repete)?" % (dz(f), a), fq(f), [fq(F(a, 10)), fq(F(a, 99)) if F(a, 99) != f else fq(F(a, 90)), fq(F(a, 90))],
                 "Período de 1 algarismo: %d/9 = <b>%s</b>." % (a, fq(f)))
    p = R.randint(10, 98)
    if p % 11 == 0:
        return None
    f = F(p, 99)
    return M("Qual é a fração geratriz de %s (o %02d se repete)?" % (dz(f), p), fq(f), [fq(F(p, 100)), fq(F(p, 9)) if F(p, 9) < 1 else fq(F(p, 999)), fq(F(p, 90))],
             "Período de 2 algarismos: %d/99 = <b>%s</b>." % (p, fq(f)))


def s3_composta():
    a, p = R.randint(1, 9), R.randint(1, 9)
    if a == p:
        return None
    f = F(a * 10 + p - a, 90)
    return M("Qual é a fração geratriz de 0,%d%d%d%d… (só o %d se repete)?" % (a, p, p, p, p), fq(f), [fq(F(a * 10 + p, 99)), fq(F(a * 10 + p, 90)), fq(F(p, 9))],
             "Composta: (%d%d − %d)/90 = %d/90 = <b>%s</b>." % (a, p, a, a * 10 + p - a, fq(f)))


def s4_inteiro():
    ip, a = R.randint(1, 5), R.randint(1, 8)
    f = ip + F(a, 9)
    return M("Qual fração é igual a %s?" % dz(f), fq(f), [fq(ip + F(a, 10)), fq(F(ip * 10 + a, 9)) if F(ip * 10 + a, 9) != f else fq(F(ip + a, 9)), fq(F(ip + a, 9))],
             "%d + %d/9 = <b>%s</b>." % (ip, a, fq(f)))


s5_conceitos = bank(R, [
    ("O período da dízima 0,454545… é…", "45", ["4", "5", "0,45"]),
    ("0,999… é igual a…", "1", ["0,9", "9/10", "um número menor que 1 que não existe"]),
    ("0,333… é igual a…", "1/3", ["3/10", "33/100", "0,3"]),
    ("Toda dízima periódica é um número…", "racional", ["irracional", "inteiro", "natural"]),
    ("Qual destes é decimal exato?", "7/20", ["2/3", "5/6", "1/7"]),
    ("Qual destes gera uma dízima periódica?", "4/15", ["3/8", "9/25", "7/40"]),
    ("Na dízima 0,1666…, a parte que não se repete é…", "1", ["6", "16", "nenhuma"]),
    ("Qual é maior: 0,3 ou 0,333…?", "0,333…", ["0,3", "são iguais", "não dá para comparar"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Decimal exato ou dízima?", mix(R, seen, [(s1_exata_ou, 20)])),
        ("Dízimas simples", mix(R, seen, [(s2_simples, 20)])),
        ("Dízimas compostas", mix(R, seen, [(s3_composta, 20)])),
        ("Com parte inteira", mix(R, seen, [(s4_inteiro, 14), (s5_conceitos, 6)])),
        ("Revisão", mix(R, seen, [(s2_simples, 8), (s3_composta, 8), (s5_conceitos, 2), (s1_exata_ou, 2)])),
    ]
    body = lesson(
        ["Dividindo o numerador pelo denominador, uma fração vira <b>decimal exato</b> (se o denominador só tem os fatores 2 e 5) ou <b>dízima periódica</b> (algarismos que se repetem para sempre).",
         "Dízima simples: o período fica sobre tantos 9 quantos forem os seus algarismos. 0,777… = 7/9; 0,2727… = 27/99 = 3/11.",
         "Dízima composta: (número formado até o fim do primeiro período − parte que não se repete) ÷ (um 9 para cada algarismo do período e um 0 para cada algarismo que não se repete). 0,1666… = (16 − 1)/90 = 15/90 = 1/6."],
        [("0,555…", ["período 5"], "5/9"),
         ("0,1222…", ["(12 − 1)/90"], "11/90")],
        [["0,333… = 3/10", "3/10 = 0,3. A dízima é 3/9 = 1/3."],
         ["Esquecer a parte que não se repete", "Na composta, subtraia essa parte e use 90, 900…"],
         ["Chamar 0,25 de dízima", "0,25 termina: é decimal exato."]])
    faq = [("O que é fração geratriz?", "É a fração que, ao ser dividida, gera a dízima periódica. Por exemplo, 1/3 é a fração geratriz de 0,333…"),
           ("O que a BNCC pede no 8º ano?", "Reconhecer e utilizar procedimentos para a obtenção de uma fração geratriz para uma dízima periódica (EF08MA05).")]
    unit(R, "dizimas-periodicas", "N", ["EF08MA05"],
         "Reconhecer e utilizar procedimentos para a obtenção de uma fração geratriz para uma dízima periódica",
         "Dízimas periódicas e fração geratriz", "Dízimas periódicas",
         "Atividades de matemática para o 8º ano sobre dízimas periódicas: decimal exato ou dízima, período, fração geratriz de dízimas simples e compostas e dízimas com parte inteira. 100 exercícios com gabarito.",
         "0,777… = 7/9", "0,2727… = 27/99",
         body, faq, sets, 5, grade="8-ano")


if __name__ == "__main__":
    main()
