# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Equações do 2º grau do tipo ax² = b (Álgebra, EF08MA09)
  python3 tools/gen_br_matematica_8_equacoes_do_2_grau_do_tipo_ax2_b.py
Resolver x² = b e ax² = b (duas raízes opostas, uma raiz zero ou nenhuma raiz real); ax² + c = d; problemas de área de quadrados,
de números e de queda livre simples; quando a resposta negativa não serve.
Erros: esquecer a raiz negativa, dividir errado, aceitar lado negativo num problema de medida, achar raiz de número negativo.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, bank, unit

R = random.Random(88009)


def S(*xs):
    xs = sorted(set(xs))
    return "S = {" + "; ".join(fq(x) for x in xs) + "}" if xs else "S = ∅"


def s1_x2():
    r = R.randint(1, 15)
    k = R.choice(["x2", "ax2", "ax2c"])
    if k == "x2":
        return M("Resolva x² = %s." % d(r * r), S(r, -r), [S(r), S(r * r, -r * r), S(F(r * r, 2), -F(r * r, 2))], "x = ±√%s = ±%d: <b>%s</b>." % (d(r * r), r, S(r, -r)))
    if k == "ax2":
        a = R.randint(2, 6)
        return M("Resolva %dx² = %s." % (a, d(a * r * r)), S(r, -r), [S(a * r, -a * r), S(r), S(r * r, -r * r)], "x² = %s ÷ %d = %s; x = ±%d: <b>%s</b>." % (d(a * r * r), a, d(r * r), r, S(r, -r)))
    a, c = R.randint(1, 4), R.randint(1, 30)
    return M("Resolva %sx² + %d = %s." % ("" if a == 1 else a, c, d(a * r * r + c)), S(r, -r), [S(r), S(F(a * r * r + c, a)), S(r + 1, -r - 1)], "%sx² = %s; x² = %s; <b>%s</b>." % ("" if a == 1 else a, d(a * r * r), d(r * r), S(r, -r)))


def s2_especiais():
    k = R.choice(["neg", "zero", "frac"])
    if k == "neg":
        b = R.randint(1, 50)
        return M("Resolva x² = −%d (nos números reais)." % b, "S = ∅", ["S = {−%d; %d}" % (int(b ** 0.5) or 1, int(b ** 0.5) or 1), S(-b), "S = {0}"], "Nenhum número real elevado ao quadrado dá negativo: <b>S = ∅</b>.")
    if k == "zero":
        a = R.randint(2, 9)
        return M("Resolva %dx² = 0." % a, "S = {0}", ["S = ∅", S(a, -a), S(F(1, a))], "x² = 0 → <b>x = 0</b>.")
    p, q = R.randint(1, 7), R.choice([2, 3, 4, 5, 6])
    if p >= q * 2 or F(p, q).denominator != q:
        return None
    return M("Resolva x² = %s." % fq(F(p * p, q * q)), S(F(p, q), -F(p, q)), [S(F(p * p, q), -F(p * p, q)), S(F(p, q)), S(F(p, q * q), -F(p, q * q))], "x = ±√(%d/%d) = ±%d/%d: <b>%s</b>." % (p * p, q * q, p, q, S(F(p, q), -F(p, q))))


def s3_problemas():
    k = R.choice(["quad", "num", "dobro", "quadro"])
    if k == "quad":
        L = R.randint(3, 25)
        return M("Um terreno quadrado tem %s m² de área. Quanto mede o lado?" % d(L * L), "%d m" % L, ["−%d m e %d m" % (L, L), "%s m" % d(F(L * L, 4)) if L * L % 4 == 0 else "%d m" % (2 * L), "%s m" % d(F(L * L, 2)) if L * L % 2 == 0 else "%d m" % (L + 1)],
                 "x² = %s → x = ±%d; como é medida, só vale <b>%d m</b>." % (d(L * L), L, L))
    if k == "num":
        n = R.randint(2, 12)
        return M("O quadrado de um número positivo é %d. Qual é o número?" % (n * n), d(n), [d(-n), d(F(n * n, 2)) if (n * n) % 2 == 0 else d(n + 1), d(n * n * 2)], "x² = %d → x = ±%d; positivo: <b>%d</b>." % (n * n, n, n))
    if k == "dobro":
        n, a = R.randint(2, 10), R.choice([2, 3, 5])
        return M("O %s do quadrado de um número é %d. Quais são os números possíveis?" % ({2: "dobro", 3: "triplo", 5: "quíntuplo"}[a], a * n * n), "%d e −%d" % (n, n), ["só %d" % n, "%d e −%d" % (a * n, a * n), "%d e −%d" % (n * n, n * n)],
                 "%dx² = %d → x² = %d → <b>x = %d ou x = −%d</b>." % (a, a * n * n, n * n, n, n))
    L = R.randint(4, 12)
    k2 = R.choice([2, 4])
    return M("Um quadro quadrado tem área %s cm² e tem %d vezes a área de um azulejo quadrado. Quanto mede o lado do azulejo?" % (d(L * L * k2), k2), "%d cm" % L, ["%d cm" % (L * k2), "%s cm" % d(L * L), "%d cm" % (L + 2)],
             "Área do azulejo: %s ÷ %d = %s; lado = √%s = <b>%d cm</b>." % (d(L * L * k2), k2, d(L * L), d(L * L), L))


s4_conceitos = bank(R, [
    ("Quantas soluções reais tem x² = 49?", "duas: 7 e −7", ["uma: 7", "nenhuma", "infinitas"]),
    ("Quantas soluções reais tem x² = 0?", "uma: 0", ["duas", "nenhuma", "infinitas"]),
    ("Quantas soluções reais tem x² = −4?", "nenhuma", ["duas: 2 e −2", "uma: −2", "uma: 2"]),
    ("Num problema sobre o lado de um quadrado, a raiz negativa…", "não serve, porque medida não é negativa", ["também é resposta", "é a única resposta", "vale o dobro"]),
    ("(−6)² e 6² são…", "iguais a 36", ["−36 e 36", "−12 e 12", "diferentes"]),
    ("Para resolver 3x² = 75, o primeiro passo é…", "dividir os dois lados por 3", ["tirar a raiz de 75", "somar 3", "multiplicar por 3"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("x² = b", mix(R, seen, [(s1_x2, 20)])),
        ("ax² = b e ax² + c = d", mix(R, seen, [(s1_x2, 20)])),
        ("Casos especiais", mix(R, seen, [(s2_especiais, 14), (s4_conceitos, 6)])),
        ("Problemas", mix(R, seen, [(s3_problemas, 20)])),
        ("Revisão", mix(R, seen, [(s1_x2, 10), (s3_problemas, 10)])),
    ]
    body = lesson(
        ["Uma equação como x² = 25 tem <b>duas soluções</b>: x = 5 e x = −5, porque 5² = 25 e (−5)² = 25.",
         "Em ax² = b, divida por a primeiro: 3x² = 48 → x² = 16 → x = ±4.",
         "x² = 0 tem só a solução 0; x² = −9 não tem solução real.",
         "Em problemas de medida, a raiz negativa é descartada."],
        [("2x² − 3 = 47", ["2x² = 50", "x² = 25"], "S = {−5; 5}"),
         ("Quadrado de área 81 m²", ["x = ±9"], "lado 9 m")],
        [["Esquecer a raiz negativa", "x² = 16 → x = 4 ou x = −4."],
         ["Tirar a raiz antes de dividir", "Isole x² primeiro."],
         ["Aceitar medida negativa", "Comprimento é sempre positivo."]])
    faq = [("Por que x² = 25 tem duas soluções?", "Porque tanto 5 quanto −5, elevados ao quadrado, dão 25. Por isso escrevemos x = ±5."),
           ("O que a BNCC pede no 8º ano?", "Resolver e elaborar, com e sem uso de tecnologias, problemas que possam ser representados por equações polinomiais de 2º grau do tipo ax² = b (EF08MA09).")]
    unit(R, "equacoes-do-2-grau-do-tipo-ax2-b", "A", ["EF08MA09"],
         "Resolver e elaborar, com e sem uso de tecnologias, problemas que possam ser representados por equações polinomiais de 2º grau do tipo ax² = b",
         "Equações do 2º grau do tipo ax² = b", "Equações ax² = b",
         "Atividades de matemática para o 8º ano sobre equações do 2º grau do tipo ax² = b: duas raízes opostas, raiz zero, sem raiz real, frações e problemas de área. 100 exercícios com gabarito.",
         "x² = 25 → x = 5 ou x = −5", "Isole x² antes de tirar a raiz.",
         body, faq, sets, 9, grade="8-ano")


if __name__ == "__main__":
    main()
