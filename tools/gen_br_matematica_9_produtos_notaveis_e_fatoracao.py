# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Produtos notáveis e fatoração (Álgebra, EF09MA09)
  python3 tools/gen_br_matematica_9_produtos_notaveis_e_fatoracao.py
Quadrado da soma, quadrado da diferença, produto da soma pela diferença; cálculo mental (51², 49 · 51);
fator comum em evidência; trinômio quadrado perfeito; diferença de dois quadrados; trinômio x² + bx + c.
Erros: (a + b)² = a² + b² (esquecer 2ab), sinal do termo do meio, (a − b)(a + b) = a² + b².
"""
import random
from br_common import lesson, mix
from br_9 import M, d, expr, P2, unit

R = random.Random(89008)
NB = " "


def sq_term(k, v):
    return expr([(k, v)])


def s1_quadrado():
    a = R.choice([1, 1, 2, 3])
    b = R.choice([1, 2, 3, 4, 5, 6, 7])
    s = R.choice([1, -1])
    x = "x" if a == 1 else "%dx" % a
    q = "(%s %s %d)²" % (x, "+" if s > 0 else "−", b)
    ok = P2(a * a, 2 * a * b * s, b * b)
    return M("Desenvolva %s." % q, ok, [P2(a * a, 0, b * b), P2(a * a, a * b * s, b * b), P2(a * a, 2 * a * b * s, -b * b), P2(a * a, -2 * a * b * s, b * b), P2(a, 2 * a * b * s, b * b)],
             "(a %s b)² = a² %s 2ab + b²: <b>%s</b>." % ("+" if s > 0 else "−", "+" if s > 0 else "−", ok))


def s1_somadif():
    a = R.choice([1, 1, 2, 3, 4, 5])
    b = R.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    x = "x" if a == 1 else "%dx" % a
    ok = P2(a * a, 0, -b * b)
    return M("Desenvolva (%s + %d)(%s − %d)." % (x, b, x, b), ok, [P2(a * a, 0, b * b), P2(a * a, -2 * a * b, -b * b), P2(a * a, 0, -2 * b), P2(a, 0, -b * b)],
             "(a + b)(a − b) = a² − b²: <b>%s</b>." % ok)


def s2_mental():
    k = R.choice(["sq+", "sq-", "sd"])
    if k == "sq+":
        n = R.choice([10, 20, 30, 40, 50, 60, 70, 100])
        m = R.choice([1, 2, 3])
        v = n + m
        return M("Use (a + b)² para calcular %d²." % v, d(v * v), [d(n * n + m * m), d(v * v - 2 * n * m + m), d(n * n + n * m + m * m)],
                 "%d² = %d² + 2 · %d · %d + %d² = %s + %s + %s = <b>%s</b>." % (v, n, n, m, m, d(n * n), d(2 * n * m), d(m * m), d(v * v)))
    if k == "sq-":
        n = R.choice([20, 30, 40, 50, 60, 70, 80, 100])
        m = R.choice([1, 2, 3])
        v = n - m
        return M("Use (a − b)² para calcular %d²." % v, d(v * v), [d(n * n - m * m), d(n * n + 2 * n * m + m * m), d(n * n - n * m + m * m)],
                 "%d² = %d² − 2 · %d · %d + %d² = <b>%s</b>." % (v, n, n, m, m, d(v * v)))
    n = R.choice([20, 30, 40, 50, 60, 100])
    m = R.choice([1, 2, 3, 4])
    return M("Use (a + b)(a − b) para calcular %d · %d." % (n - m, n + m), d(n * n - m * m), [d(n * n + m * m), d(n * n - 2 * m), d(n * n - m)],
             "%d · %d = %d² − %d² = %s − %d = <b>%s</b>." % (n - m, n + m, n, m, d(n * n), m * m, d(n * n - m * m)))


def s3_evidencia():
    k = R.choice([2, 3, 4, 5, 6])
    v = R.choice(["x", "a", "y"])
    p, q = R.sample([1, 2, 3, 5, 7], 2)
    if R.random() < 0.5:
        e = "%d%s² + %d%s" % (k * p, v, k * q, v)
        ok = "%d%s(%s + %d)" % (k, v, ("%d%s" % (p, v)) if p > 1 else v, q)
        w = ["%d(%s + %d)" % (k, ("%d%s²" % (p, v)) if p > 1 else v + "²", q), "%s(%d%s + %d)" % (v, k * p, v, q) if k * p > 1 else "x", "%d%s(%s + %d)" % (k, v, ("%d%s" % (p, v)) if p > 1 else v, k * q), "%d%s²(%d + %d)" % (k, v, p, q)]
    else:
        e = "%d%s − %d" % (k * p, v, k * q)
        ok = "%d(%s − %d)" % (k, ("%d%s" % (p, v)) if p > 1 else v, q)
        w = ["%d(%s − %d)" % (k, ("%d%s" % (p, v)) if p > 1 else v, k * q), "%s(%d − %d)" % (v, k * p, k * q), "%d(%s + %d)" % (k, ("%d%s" % (p, v)) if p > 1 else v, q)]
    return M("Fatore colocando o fator comum em evidência: %s." % e, ok, w, "O fator comum é %s: <b>%s</b>." % (ok.split("(")[0], ok))


def s4_fatorar():
    k = R.choice(["tqp", "dq", "tri"])
    if k == "tqp":
        b = R.randint(1, 9)
        s = R.choice([1, -1])
        e = P2(1, 2 * b * s, b * b)
        ok = "(x %s %d)²" % ("+" if s > 0 else "−", b)
        return M("Fatore o trinômio quadrado perfeito %s." % e, ok, ["(x %s %d)²" % ("−" if s > 0 else "+", b), "(x %s %d)²" % ("+" if s > 0 else "−", 2 * b), "(x + %d)(x − %d)" % (b, b)],
                 "√(x²) = x, √%d = %d e o termo do meio é %s2 · x · %d: <b>%s</b>." % (b * b, b, "" if s > 0 else "−", b, ok))
    if k == "dq":
        a = R.choice([1, 1, 2, 3, 5])
        b = R.randint(1, 10)
        e = P2(a * a, 0, -b * b)
        x = "x" if a == 1 else "%dx" % a
        ok = "(%s + %d)(%s − %d)" % (x, b, x, b)
        return M("Fatore a diferença de dois quadrados %s." % e, ok, ["(%s − %d)²" % (x, b), "(%s + %d)²" % (x, b), "(%s + %d)(%s − %d)" % (x, b * b, x, b * b) if b > 1 else "(%s + 2)(%s − 2)" % (x, x)],
                 "a² − b² = (a + b)(a − b), com a = %s e b = %d: <b>%s</b>." % (x, b, ok))
    r1, r2 = R.sample([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7], 2)
    e = P2(1, -(r1 + r2), r1 * r2)
    f = lambda r: "(x %s %d)" % ("−" if r > 0 else "+", abs(r))
    ok = f(r1) + f(r2)
    return M("Fatore %s." % e, ok, [f(-r1) + f(-r2), f(r1) + f(-r2), f(-r1) + f(r2)],
             "Procure dois números com soma %s e produto %s: %s e %s. <b>%s</b>." % (d(-(r1 + r2)), d(r1 * r2), d(-r1), d(-r2), ok))


def s5_aplicar():
    k = R.choice(["valor", "simpl", "area"])
    if k == "valor":
        a, b = R.randint(3, 12), R.randint(1, 9)
        if a == b:
            return None
        return M("Sabendo que a + b = %d e a − b = %d, quanto vale a² − b²?" % (a, b), d(a * b), [d(a * a - b * b), d(a + b), d(a * a + b * b)],
                 "a² − b² = (a + b)(a − b) = %d · %d = <b>%d</b>." % (a, b, a * b))
    if k == "simpl":
        b = R.randint(2, 9)
        return M("Simplifique (x² − %d) ÷ (x − %d), para x ≠ %d." % (b * b, b, b), "x + %d" % b, ["x − %d" % b, "x + %d" % (b * b), "x"],
                 "x² − %d = (x + %d)(x − %d); cortando (x − %d): <b>x + %d</b>." % (b * b, b, b, b, b))
    b = R.randint(2, 8)
    ok = P2(1, 2 * b, b * b)
    return M("Um quadrado tem lado (x + %d) cm. Qual expressão dá a sua área?" % b, ok + " cm²", [P2(1, 0, b * b) + " cm²", P2(1, b, b * b) + " cm²", "4x + %d cm²" % (4 * b)],
             "Área = (x + %d)² = <b>%s cm²</b>." % (b, ok))


def main():
    seen = set()
    sets = [
        ("Quadrado da soma e da diferença", mix(R, seen, [(s1_quadrado, 20)])),
        ("Produto da soma pela diferença e cálculo mental", mix(R, seen, [(s1_somadif, 8), (s2_mental, 12)])),
        ("Fator comum em evidência", mix(R, seen, [(s3_evidencia, 20)])),
        ("Fatoração de trinômios e diferença de quadrados", mix(R, seen, [(s4_fatorar, 20)])),
        ("Aplicações", mix(R, seen, [(s5_aplicar, 12), (s4_fatorar, 4), (s2_mental, 4)])),
    ]
    body = lesson(
        ["Os <b>produtos notáveis</b> são multiplicações que aparecem sempre:",
         "(a + b)² = a² + 2ab + b²; (a − b)² = a² − 2ab + b²; (a + b)(a − b) = a² − b².",
         "<b>Fatorar</b> é fazer o caminho de volta: escrever a expressão como um produto.",
         "Primeiro procure um fator comum (6x + 9 = 3(2x + 3)); depois veja se é um trinômio quadrado perfeito ou uma diferença de quadrados."],
        [("(x + 5)²", ["x² + 2 · x · 5 + 5²"], "x² + 10x + 25"),
         ("x² − 49", ["x² − 7²"], "(x + 7)(x − 7)"),
         ("49 · 51", ["(50 − 1)(50 + 1) = 2.500 − 1"], "2.499")],
        [["Dizer que (a + b)² = a² + b²", "Falta o termo 2ab."],
         ["Errar o sinal do termo do meio", "Em (a − b)², o termo do meio é −2ab."],
         ["Achar que (a + b)(a − b) = a² + b²", "O resultado é a² − b²."]])
    faq = [("Quais são os produtos notáveis do 9º ano?", "Quadrado da soma, quadrado da diferença e produto da soma pela diferença. A BNCC pede compreender esses produtos e usá-los para fatorar e resolver equações."),
           ("Como fatorar x² + 5x + 6?", "Procure dois números com soma 5 e produto 6: 2 e 3. Então x² + 5x + 6 = (x + 2)(x + 3).")]
    unit(R, "produtos-notaveis-e-fatoracao", "A", ["EF09MA09"],
         "Compreender os processos de fatoração de expressões algébricas, com base em suas relações com os produtos notáveis, para resolver e elaborar problemas que possam ser representados por equações polinomiais do 2º grau",
         "Produtos notáveis e fatoração", "Produtos notáveis e fatoração",
         "Atividades de matemática para o 9º ano sobre produtos notáveis e fatoração: quadrado da soma e da diferença, produto da soma pela diferença, fator comum, trinômio quadrado perfeito e diferença de quadrados. 100 exercícios com gabarito.",
         "(a + b)² = a² + 2ab + b²", "(a + b)(a − b) = a² − b²",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
