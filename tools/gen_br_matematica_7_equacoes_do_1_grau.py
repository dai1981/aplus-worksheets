# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Equações do 1º grau (Álgebra, EF07MA18)
  python3 tools/gen_br_matematica_7_equacoes_do_1_grau.py
Resolver ax + b = c, equações com incógnita dos dois lados, com parênteses e com frações simples; verificar a solução;
montar a equação a partir de um problema (idades, números consecutivos, compras, perímetro) e resolver.
Erros: passar um termo sem trocar o sinal, dividir só um dos termos, errar o sinal ao distribuir −(x − 3).
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, fq, expr, unit

R = random.Random(87009)


def eqs(a, b):
    return expr([(a, "x"), (b, "")])


def s1_simples():
    x = R.randint(-10, 15)
    a = R.choice([2, 3, 4, 5, 6, 7, 8, -2, -3, -4])
    b = R.randint(-20, 20)
    c = a * x + b
    return M("Resolva %s = %s." % (eqs(a, b), d(c)), "x = %s" % d(x), ["x = %s" % d(F(c + b, a)) if (F(c + b, a)).denominator == 1 and F(c + b, a) != x else "x = %s" % d(x + 1), "x = %s" % d(c - b - a) if c - b - a != x else "x = %s" % d(-x - 1), "x = %s" % d(-x) if x else "x = 1"],
             "%s = %s − %s = %s → x = %s ÷ %s = <b>%s</b>." % (eqs(a, 0), d(c), par(b), d(c - b), d(c - b), par(a), d(x)))


def par(v):
    return "(%s)" % d(v) if v < 0 else d(v)


def s2_dois_lados():
    x = R.randint(-8, 12)
    a, c = R.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    b = R.randint(-15, 15)
    e = (a - c) * x + b
    return M("Resolva %s = %s." % (eqs(a, b), eqs(c, e)), "x = %s" % d(x), ["x = %s" % d(-x) if x else "x = 1", "x = %s" % d(F(e - b, a + c)) if (F(e - b, a + c)).denominator == 1 and F(e - b, a + c) != x else "x = %s" % d(x + 2), "x = %s" % d(x - 1)],
             "Letras de um lado e números do outro: %s = %s → x = <b>%s</b>." % (eqs(a - c, 0), d(e - b), d(x)))


def s3_parenteses():
    x = R.randint(-6, 10)
    a, b, c = R.choice([2, 3, 4, 5, -2, -3]), R.randint(-6, 6), R.randint(-10, 10)
    if b == 0:
        return None
    r = a * (x + b) + c
    q = "%s(x %s %d) %s = %s" % (d(a) if a != -1 else "−", "+" if b > 0 else "−", abs(b), ("+ %d" % c) if c >= 0 else "− %d" % -c, d(r))
    w = F(r - c - b, a)
    return M("Resolva %s." % q, "x = %s" % d(x), ["x = %s" % (d(w) if w.denominator == 1 and w != x else d(x + 1)), "x = %s" % d(-x) if x else "x = 2", "x = %s" % d(x + 3)],
             "Distribua: %s %s = %s; resolva: <b>x = %s</b>." % (eqs(a, a * b), ("+ %d" % c) if c >= 0 else "− %d" % -c, d(r), d(x)))


def s4_fracao():
    x = R.randint(1, 12) * R.choice([2, 3, 4, 6])
    k = R.choice([2, 3, 4, 6])
    if x % k:
        return None
    b = R.randint(-6, 8)
    r = x // k + b
    return M("Resolva x/%d %s = %s." % (k, ("+ %d" % b) if b >= 0 else "− %d" % -b, d(r)), "x = %s" % d(x), ["x = %s" % d(r - b), "x = %s" % d((r + b) * k) if (r + b) * k != x else "x = %s" % d(x + k), "x = %s" % d(r * k)],
             "x/%d = %s → x = %s · %d = <b>%s</b>." % (k, d(r - b), d(r - b), k, d(x)))


def s5_problemas():
    k = R.choice(["idade", "consec", "compra", "perim", "dobro", "soma"])
    if k == "idade":
        f, t = R.randint(6, 14), R.choice([3, 4])
        return M("A idade de uma mãe é %d vezes a do filho, e as duas somam %d anos. Quantos anos tem o filho?" % (t, f * (t + 1)), "%d anos" % f, ["%d anos" % (f * t), "%d anos" % (f * (t + 1) // 2), "%d anos" % (f + t)],
                 "x + %dx = %d → %dx = %d → <b>x = %d anos</b>." % (t, f * (t + 1), t + 1, f * (t + 1), f))
    if k == "consec":
        n, m = R.randint(10, 60), R.choice([2, 3])
        s = sum(n + i for i in range(m))
        return M("A soma de %s números inteiros consecutivos é %d. Qual é o menor deles?" % ("dois" if m == 2 else "três", s), d(n), [d(n + 1), d(s // m), d(n - 1)],
                 "%s = %d → <b>x = %d</b>." % (" + ".join("(x + %d)" % i if i else "x" for i in range(m)), s, n))
    if k == "compra":
        p, q, t = R.randint(3, 12), R.randint(2, 6), R.randint(5, 30)
        tot = p * q + t
        return M("Comprei %d cadernos iguais e uma mochila de %s, gastando %s ao todo. Quanto custou cada caderno?" % (q, reais(t * 100), reais(tot * 100)), reais(p * 100), [reais(tot * 100 // q) if tot % q == 0 else reais((p + 1) * 100), reais((tot - t) * 100), reais((tot + t) * 100 // q) if (tot + t) % q == 0 else reais((p + 2) * 100)],
                 "%dx + %d = %d → %dx = %d → <b>x = %s</b>." % (q, t, tot, q, p * q, reais(p * 100)))
    if k == "perim":
        x, a = R.randint(3, 15), R.randint(2, 9)
        P = 2 * (x + x + a)
        return M("Um retângulo tem comprimento %d cm maior que a largura e perímetro de %d cm. Qual é a largura?" % (a, P), "%d cm" % x, ["%d cm" % (x + a), "%d cm" % (P // 4), "%d cm" % (P // 2 - a)],
                 "2x + 2(x + %d) = %d → 4x + %d = %d → <b>x = %d cm</b>." % (a, P, 2 * a, P, x))
    if k == "dobro":
        x, b = R.randint(3, 30), R.randint(2, 20)
        return M("O dobro de um número, mais %d, é igual a %d. Qual é o número?" % (b, 2 * x + b), d(x), [d(2 * x + b - b // 2) if 2 * x + b - b // 2 != x else d(x + 1), d((2 * x + b + b) // 2), d(2 * x)],
                 "2x + %d = %d → 2x = %d → <b>x = %d</b>." % (b, 2 * x + b, 2 * x, x))
    x, a = R.randint(10, 80), R.randint(5, 30)
    return M("Ana e Bia têm juntas %s. Bia tem %s a mais que Ana. Quanto tem Ana?" % (reais((2 * x + a) * 100), reais(a * 100)), reais(x * 100), [reais((x + a) * 100), reais((2 * x + a) * 50) if (2 * x + a) % 2 == 0 else reais((x + 1) * 100), reais((2 * x) * 100)],
             "x + (x + %d) = %d → 2x = %d → <b>x = %s</b>." % (a, 2 * x + a, 2 * x, reais(x * 100)))


def main():
    seen = set()
    sets = [
        ("Equações simples", mix(R, seen, [(s1_simples, 20)])),
        ("Incógnita dos dois lados", mix(R, seen, [(s2_dois_lados, 20)])),
        ("Parênteses e frações", mix(R, seen, [(s3_parenteses, 12), (s4_fracao, 8)])),
        ("Montar a equação", mix(R, seen, [(s5_problemas, 20)])),
        ("Revisão", mix(R, seen, [(s2_dois_lados, 6), (s3_parenteses, 6), (s5_problemas, 8)])),
    ]
    body = lesson(
        ["Uma <b>equação</b> é uma igualdade com uma incógnita. Resolver é achar o valor que a torna verdadeira.",
         "Faça a mesma operação nos dois membros: some ou subtraia para juntar os termos com x de um lado e os números do outro; depois divida pelo coeficiente.",
         "Com parênteses, use a distributiva primeiro. Confira a solução substituindo na equação.",
         "Em problemas, chame de x o que se quer descobrir, escreva a equação e resolva."],
        [("5x − 7 = 2x + 8", ["5x − 2x = 8 + 7", "3x = 15"], "x = 5"),
         ("3(x − 2) = 12", ["3x − 6 = 12", "3x = 18"], "x = 6")],
        [["Mudar de lado sem trocar o sinal", "Subtraia dos dois lados: o termo «passa» com sinal trocado."],
         ["Dividir só um termo", "Divida o membro inteiro."],
         ["Errar −(x − 3)", "−(x − 3) = −x + 3."]])
    faq = [("Como resolver uma equação do 1º grau?", "Use as propriedades da igualdade: some, subtraia, multiplique ou divida os dois membros pelo mesmo número até ficar com x sozinho de um lado. Depois confira substituindo o valor."),
           ("O que a BNCC pede no 7º ano?", "Resolver e elaborar problemas que possam ser representados por equações polinomiais de 1º grau, redutíveis à forma ax + b = c, fazendo uso das propriedades da igualdade (EF07MA18).")]
    unit(R, "equacoes-do-1-grau", "A", ["EF07MA18"],
         "Resolver e elaborar problemas que possam ser representados por equações polinomiais de 1º grau, redutíveis à forma ax + b = c, fazendo uso das propriedades da igualdade",
         "Equações do 1º grau", "Equações do 1º grau",
         "Atividades de matemática para o 7º ano sobre equações do 1º grau: ax + b = c, incógnita dos dois lados, parênteses, frações e problemas com idades, números consecutivos, compras e perímetro. 100 exercícios com gabarito.",
         "O que faz de um lado, faça do outro.", "Confira substituindo x na equação.",
         body, faq, sets, 9, grade="7-ano")


if __name__ == "__main__":
    main()
