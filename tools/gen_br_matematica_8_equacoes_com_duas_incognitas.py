# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Equações do 1º grau com duas incógnitas (Álgebra, EF08MA07)
  python3 tools/gen_br_matematica_8_equacoes_com_duas_incognitas.py
Equação ax + by = c; verificar se um par ordenado é solução; achar y para um x dado; infinitas soluções; a reta no plano cartesiano;
escrever a equação de uma situação (moedas, ingressos, pontos).
Erros: trocar x e y no par ordenado, achar que só existe uma solução, isolar y com o sinal errado.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, expr, kosy, unit, bank

R = random.Random(88007)


def eq(a, b, c):
    return "%s = %s" % (expr([(a, "x"), (b, "y")]), d(c))


def P(x, y):
    return "(%s, %s)" % (d(x), d(y))


def s1_solucao():
    a, b = R.choice([1, 2, 3, -1, -2]), R.choice([1, 2, 3, -1, 4])
    x, y = R.randint(-4, 6), R.randint(-4, 6)
    c = a * x + b * y
    ok = R.random() < 0.5
    px, py = (x, y) if ok else R.choice([(y, x), (x + 1, y), (x, y - 1)])
    if not ok and a * px + b * py == c:
        return None
    ans = "sim" if ok else "não"
    return M("O par %s é solução da equação %s?" % (P(px, py), eq(a, b, c)), ans, ["não" if ok else "sim", "só se x = y", "não dá para saber"],
             "%s · %s + %s · %s = %s, que %s %s: <b>%s</b>." % (d(a), "(%s)" % d(px) if px < 0 else d(px), d(b), "(%s)" % d(py) if py < 0 else d(py), d(a * px + b * py), "é igual a" if a * px + b * py == c else "é diferente de", d(c), ans))


def s2_achar():
    a, b = R.choice([1, 2, 3, 4, -2]), R.choice([1, 2, -1])
    x, y = R.randint(-5, 8), R.randint(-6, 9)
    c = a * x + b * y
    return M("Na equação %s, qual é o valor de y quando x = %s?" % (eq(a, b, c), d(x)), "y = %s" % d(y), ["y = %s" % d(c - a * x) if c - a * x != y else "y = %s" % d(y + 1), "y = %s" % d(-y) if y else "y = 1", "y = %s" % d(F(c, b) - x) if (F(c, b) - x).denominator == 1 and F(c, b) - x != y else "y = %s" % d(y + 2)],
             "%s · %s + %s = %s → %s = %s → <b>y = %s</b>." % (d(a), "(%s)" % d(x) if x < 0 else d(x), expr([(b, "y")]), d(c), expr([(b, "y")]), d(c - a * x), d(y)))


def s3_grafico():
    m, n = R.choice([(1, 1), (2, -1), (-1, 3), (1, -2), (2, 1), (-2, 2), (1, 0), (-1, 0), (3, -2)])
    pic = kosy(lines=[(m, n, "#1f77b4", "r")], label="reta de uma equação com duas incógnitas")
    a, b, c = -m, 1, n
    ok = "y = %s" % expr([(m, "x"), (n, "")])
    return M(pic + "Qual equação tem como gráfico esta reta?", ok, ["y = %s" % expr([(n if n else 2, "x"), (m, "")]), "y = %s" % expr([(-m, "x"), (n, "")]), "y = %s" % expr([(m, "x"), (-n if n else 1, "")])],
             "A reta passa por (0, %s) e sobe %s a cada 1 para a direita: <b>%s</b>." % (d(n), d(m), ok))


def s4_situacao():
    k = R.choice(["moedas", "ingresso", "pontos"])
    if k == "moedas":
        a, b = R.choice([(5, 10), (10, 25), (25, 50), (10, 50)])
        x, y = R.randint(2, 15), R.randint(2, 15)
        t = a * x + b * y
        return M("Tenho x moedas de %d centavos e y moedas de %d centavos, que somam %d centavos. Qual equação representa a situação?" % (a, b, t), "%dx + %dy = %d" % (a, b, t), ["x + y = %d" % t, "%dx + %dy = %d" % (b, a, t), "%dx · %dy = %d" % (a, b, t)],
                 "Valor das moedas de %d (%dx) mais o das de %d (%dy): <b>%dx + %dy = %d</b>." % (a, a, b, b, a, b, t))
    if k == "ingresso":
        a, b = R.choice([(20, 10), (30, 15), (40, 20), (25, 12)])
        x, y = R.randint(3, 20), R.randint(3, 20)
        t = a * x + b * y
        q = "Num cinema, a inteira custa %s e a meia %s. Foram arrecadados %s com x inteiras e y meias. Qual par (x, y) é possível?" % (reais(a * 100), reais(b * 100), reais(t * 100))
        return M(q, P(x, y), [P(y, x) if a * y + b * x != t else P(x + 1, y), P(x + 1, y - 1) if a * (x + 1) + b * (y - 1) != t else P(x + 2, y), P(x, y + 2)],
                 "%d · %d + %d · %d = %d: <b>%s</b>." % (a, x, b, y, t, P(x, y)))
    a, b = R.choice([(3, 1), (2, 1), (3, 2)])
    v, e = R.randint(2, 10), R.randint(0, 6)
    t = a * v + b * e
    return M("Num campeonato, vitória vale %d pontos e empate vale %d. Um time fez %d pontos. Se teve %d vitórias, quantos empates teve?" % (a, b, t, v), d(e), [d(t - v), d(t - a * v + 1), d(v)], "%d · %d + %d · e = %d → <b>e = %d</b>." % (a, v, b, t, e))


s5_conceitos = bank(R, [
    ("Quantas soluções tem a equação x + y = 10 (com números reais)?", "infinitas", ["uma", "duas", "nenhuma"]),
    ("O gráfico de uma equação do 1º grau com duas incógnitas é…", "uma reta", ["uma parábola", "um círculo", "um ponto"]),
    ("Cada solução de x + 2y = 8 corresponde a…", "um ponto da reta no plano cartesiano", ["um ângulo", "uma área", "um número só"]),
    ("Na equação 2x + y = 7, isolando y, obtemos…", "y = 7 − 2x", ["y = 2x − 7", "y = 7 + 2x", "y = 7/2x"]),
    ("O par (3, 1) é solução de x − y = 2. O par (1, 3) também é?", "não, pois 1 − 3 = −2", ["sim, sempre", "sim, porque tem os mesmos números", "não dá para saber"]),
    ("Para desenhar a reta de uma equação, basta encontrar…", "duas soluções (dois pontos)", ["uma solução", "três ângulos", "o valor de x"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("É solução?", mix(R, seen, [(s1_solucao, 20)])),
        ("Achar o valor da outra incógnita", mix(R, seen, [(s2_achar, 20)])),
        ("A reta no plano cartesiano", mix(R, seen, [(s3_grafico, 9), (s5_conceitos, 6), (s2_achar, 5)])),
        ("Situações", mix(R, seen, [(s4_situacao, 20)])),
        ("Revisão", mix(R, seen, [(s1_solucao, 10), (s2_achar, 10)])),
    ]
    body = lesson(
        ["Uma equação como 2x + y = 7 tem <b>duas incógnitas</b> e <b>infinitas soluções</b>: cada par (x, y) que a torna verdadeira, como (1, 5), (2, 3), (3, 1)…",
         "Para achar uma solução, escolha um valor para x e calcule y.",
         "Marcando as soluções no plano cartesiano, todas ficam sobre uma <b>reta</b>."],
        [("x + 2y = 10, com x = 4", ["4 + 2y = 10", "2y = 6"], "y = 3: o par (4, 3)"),
         ("y = 2x − 1", ["(0, −1) e (2, 3)"], "a reta passa por esses pontos")],
        [["Trocar x e y no par", "No par (x, y), o x vem primeiro."],
         ["Achar que só há uma solução", "Uma equação sozinha tem infinitas soluções."],
         ["Errar o sinal ao isolar y", "2x + y = 7 → y = 7 − 2x."]],
        kosy(lines=[(2, -1, "#1f77b4", "r")]))
    faq = [("Quantas soluções tem uma equação com duas incógnitas?", "Infinitas. Cada solução é um par ordenado (x, y), e todas juntas formam uma reta no plano cartesiano."),
           ("O que a BNCC pede no 8º ano?", "Associar uma equação linear de 1º grau com duas incógnitas a uma reta no plano cartesiano (EF08MA07).")]
    unit(R, "equacoes-com-duas-incognitas", "A", ["EF08MA07"],
         "Associar uma equação linear de 1º grau com duas incógnitas a uma reta no plano cartesiano",
         "Equações do 1º grau com duas incógnitas", "Equações com duas incógnitas",
         "Atividades de matemática para o 8º ano sobre equações do 1º grau com duas incógnitas: pares ordenados que são solução, achar uma incógnita, a reta no plano cartesiano e situações do dia a dia. 100 exercícios com gabarito.",
         "Infinitas soluções que formam uma reta.", "Escolha x e calcule y.",
         body, faq, sets, 7, grade="8-ano")


if __name__ == "__main__":
    main()
