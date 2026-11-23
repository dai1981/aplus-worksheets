# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Equações do 2º grau (Álgebra, EF09MA09)
  python3 tools/gen_br_matematica_9_equacoes_do_2_grau.py
Equações incompletas (x² = 49, x² − 5x = 0), resolver por fatoração, fórmula de Bhaskara (discriminante Δ),
número de raízes, soma e produto das raízes, problemas (área, números, idades).
Erros: esquecer a raiz negativa em x² = 49, dividir por x e perder a raiz 0, errar o sinal de −b, Δ com sinal errado.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, P2, sq, unit

R = random.Random(89009)


def sol(rs):
    rs = sorted(set(rs))
    return "S = {" + "; ".join(fq(r) for r in rs) + "}"


def s1_incompleta():
    k = R.choice(["x2", "ax2", "fator"])
    if k == "x2":
        r = R.randint(2, 13)
        return M("Resolva x² = %d." % (r * r), sol([r, -r]), [sol([r]), sol([r * r, -r * r]), sol([r * r // 2]) if r % 2 == 0 else sol([-r]), sol([r, 0])],
                 "x = ±√%d = ±%d: <b>%s</b>." % (r * r, r, sol([r, -r])))
    if k == "ax2":
        a, r = R.choice([2, 3, 4, 5]), R.randint(2, 8)
        return M("Resolva %s = 0." % P2(a, 0, -a * r * r), sol([r, -r]), [sol([r]), sol([r * r, -r * r]), sol([a * r, -a * r]), "S = ∅"],
                 "%dx² = %d → x² = %d → <b>%s</b>." % (a, a * r * r, r * r, sol([r, -r])))
    a, r = R.choice([1, 1, 2, 3]), R.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8])
    e = P2(a, -a * r, 0)
    return M("Resolva %s = 0." % e, sol([0, r]), [sol([r]), sol([0, -r]), sol([r, -r]), sol([a * r]) if a > 1 else sol([0])],
             "Fator comum: %sx(x %s %d) = 0, então x = 0 ou x = %s: <b>%s</b>." % ("" if a == 1 else str(a), "−" if r > 0 else "+", abs(r), d(r), sol([0, r])))


def s2_fatoracao():
    r1, r2 = R.sample([-7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 8], 2)
    e = P2(1, -(r1 + r2), r1 * r2)
    return M("Resolva %s = 0 por fatoração." % e, sol([r1, r2]), [sol([-r1, -r2]), sol([r1, -r2]), sol([-r1, r2]), sol([r1 * r2])],
             "Dois números com soma %s e produto %s: %s = (x %s %d)(x %s %d). <b>%s</b>." % (d(r1 + r2), d(r1 * r2), e, "−" if r1 > 0 else "+", abs(r1), "−" if r2 > 0 else "+", abs(r2), sol([r1, r2])))


def s3_delta():
    a = R.choice([1, 1, 2, 3, -1])
    b, c = R.randint(-9, 9), R.randint(-9, 9)
    if b == 0 or c == 0:
        return None
    D = b * b - 4 * a * c
    k = R.choice(["valor", "num"])
    e = P2(a, b, c)
    if k == "valor":
        return M("Calcule o discriminante Δ = b² − 4ac de %s = 0." % e, d(D), [d(b * b + 4 * a * c), d(-b * b - 4 * a * c), d(b - 4 * a * c), d(b * b - 4 * c)],
                 "Δ = %s² − 4 · %s · %s = %s %s %s = <b>%s</b>." % ("(%d)" % b if b < 0 else b, "(%d)" % a if a < 0 else a, "(%d)" % c if c < 0 else c, d(b * b), "−" if 4 * a * c >= 0 else "+", d(abs(4 * a * c)), d(D)))
    ans = "duas raízes reais diferentes" if D > 0 else ("uma raiz real (duas iguais)" if D == 0 else "nenhuma raiz real")
    return M("Quantas raízes reais tem %s = 0?" % e, ans, [x for x in ["duas raízes reais diferentes", "uma raiz real (duas iguais)", "nenhuma raiz real", "infinitas raízes"] if x != ans],
             "Δ = %s, que é %s: <b>%s</b>." % (d(D), "positivo" if D > 0 else ("zero" if D == 0 else "negativo"), ans))


def s4_bhaskara():
    k = R.choice(["int", "int", "frac", "irr"])
    if k == "int":
        a = R.choice([1, 2, 3])
        r1, r2 = R.sample(range(-6, 8), 2)
        b, c = -a * (r1 + r2), a * r1 * r2
        if b == 0 or c == 0:
            return None
        return M("Use a fórmula de Bhaskara para resolver %s = 0." % P2(a, b, c), sol([r1, r2]), [sol([-r1, -r2]), sol([r1 * a, r2 * a]) if a > 1 else sol([r1, -r2]), sol([r1]), sol([F(r1, 2), F(r2, 2)]) if a == 1 else sol([-r1, r2])],
                 "Δ = %s; x = (%s ± %s) ÷ %d: <b>%s</b>." % (d(b * b - 4 * a * c), d(-b), d(abs(a * (r1 - r2))), 2 * a, sol([r1, r2])))
    if k == "frac":
        p, q = R.choice([(2, 1), (2, 3), (3, 1), (3, 2), (2, 5)])
        r1 = F(q, p) * R.choice([1, -1])
        r2 = R.choice([-3, -2, -1, 1, 2, 3])
        a, b, c = p, -(p * r2 + p * r1), p * r1 * r2
        if b.denominator != 1 or c.denominator != 1 or b == 0:
            return None
        b, c = int(b), int(c)
        return M("Resolva %s = 0." % P2(a, b, c), sol([r1, r2]), [sol([-r1, -r2]), sol([r1 * p, r2]), sol([F(1) / r1, r2]), sol([r2])],
                 "Δ = %s; x = (%s ± %s) ÷ %d: <b>%s</b>." % (d(b * b - 4 * a * c), d(-b), d(abs(p * (r1 - r2))), 2 * a, sol([r1, r2])))
    b, c = R.choice([(2, -1), (4, 1), (6, 4), (-2, -2), (2, -4), (-4, -1), (6, 7), (-6, 2)])
    D = b * b - 4 * c
    h = -b // 2
    rt = sq(D // 4)
    ok = "S = {%s − %s; %s + %s}" % (d(h), rt, d(h), rt) if h else "S = {−%s; %s}" % (rt, rt)
    return M("Resolva %s = 0 (deixe a raiz quadrada na resposta)." % P2(1, b, c), ok, ["S = {%s − %s; %s + %s}" % (d(-h), rt, d(-h), rt) if h else "S = {%s}" % rt, "S = {%s − √%d; %s + √%d}" % (d(h), D, d(h), D), "S = ∅"],
             "Δ = %d; x = (%s ± √%d) ÷ 2 = %s ± %s: <b>%s</b>." % (D, d(-b), D, d(h), rt, ok))


def s5_soma_produto():
    r1, r2 = R.sample(range(-5, 9), 2)
    if r1 == 0 or r2 == 0 or r1 + r2 == 0:
        return None
    e = P2(1, -(r1 + r2), r1 * r2)
    k = R.choice(["s", "p"])
    if k == "s":
        return M("Sem resolver, qual é a soma das raízes de %s = 0?" % e, d(r1 + r2), [d(-(r1 + r2)), d(r1 * r2), d(-r1 * r2)], "Soma = −b ÷ a = <b>%s</b>." % d(r1 + r2))
    return M("Sem resolver, qual é o produto das raízes de %s = 0?" % e, d(r1 * r2), [d(-(r1 * r2)), d(r1 + r2), d(-(r1 + r2))], "Produto = c ÷ a = <b>%s</b>." % d(r1 * r2))


def s6_problemas():
    k = R.choice(["area", "num", "consec", "quad"])
    if k == "area":
        w = R.randint(3, 12)
        e = R.randint(2, 6)
        A = w * (w + e)
        return M("Um terreno retangular tem comprimento %d m maior que a largura e área de %d m². Qual é a largura?" % (e, A), "%d m" % w, ["%d m" % (w + e), "%d m" % (A // 4), "%d m" % (w - 1)],
                 "x(x + %d) = %d → %s = 0; a raiz positiva é <b>%d m</b>." % (e, A, P2(1, e, -A), w))
    if k == "num":
        n = R.randint(3, 15)
        m = R.randint(2, 6)
        return M("O quadrado de um número positivo menos %d vezes esse número é igual a %d. Qual é o número?" % (m, n * n - m * n), d(n), [d(n - m) if n - m > 0 else d(n + 1), d(n + m), d(n * n)],
                 "x² − %dx = %d → %s = 0; a raiz positiva é <b>%d</b>." % (m, n * n - m * n, P2(1, -m, -(n * n - m * n)), n))
    if k == "consec":
        n = R.randint(4, 20)
        return M("O produto de dois números inteiros positivos consecutivos é %d. Qual é o menor deles?" % (n * (n + 1)), d(n), [d(n + 1), d(n * (n + 1) // 2), d(n - 1)],
                 "x(x + 1) = %d → %s = 0; x = <b>%d</b>." % (n * (n + 1), P2(1, 1, -n * (n + 1)), n))
    s = R.randint(4, 15)
    m = R.randint(1, 5)
    return M("Uma praça quadrada ganhou %d m a mais em cada lado e ficou com %d m² de área. Qual era o lado antes?" % (m, (s + m) ** 2), "%d m" % s, ["%d m" % (s + m), "%d m" % (s - m), "%d m" % ((s + m) ** 2 // 4)],
             "(x + %d)² = %d → x + %d = %d → x = <b>%d m</b>." % (m, (s + m) ** 2, m, s + m, s))


def main():
    seen = set()
    sets = [
        ("Equações incompletas", mix(R, seen, [(s1_incompleta, 20)])),
        ("Resolver por fatoração", mix(R, seen, [(s2_fatoracao, 14), (s5_soma_produto, 6)])),
        ("Discriminante Δ", mix(R, seen, [(s3_delta, 20)])),
        ("Fórmula de Bhaskara", mix(R, seen, [(s4_bhaskara, 20)])),
        ("Problemas com equações do 2º grau", mix(R, seen, [(s6_problemas, 20)])),
    ]
    body = lesson(
        ["Uma <b>equação do 2º grau</b> tem a forma ax² + bx + c = 0, com a ≠ 0.",
         "Incompletas: x² = 49 dá x = 7 ou x = −7; x² − 5x = 0 vira x(x − 5) = 0, então x = 0 ou x = 5.",
         "Completas: calcule <b>Δ = b² − 4ac</b> e use x = (−b ± √Δ) ÷ 2a. Se Δ > 0, há duas raízes; se Δ = 0, uma; se Δ &lt; 0, nenhuma raiz real.",
         "Soma das raízes = −b ÷ a; produto = c ÷ a."],
        [("x² − 5x + 6 = 0", ["Δ = 25 − 24 = 1", "x = (5 ± 1) ÷ 2"], "S = {2; 3}"),
         ("x² = 49", ["x = ±7"], "S = {−7; 7}")],
        [["Esquecer a raiz negativa", "x² = 49 tem duas raízes: 7 e −7."],
         ["Dividir por x e perder o zero", "Em x² = 5x, coloque x em evidência: x = 0 ou x = 5."],
         ["Errar o sinal de −b", "Se b = −5, então −b = 5."]])
    faq = [("O que é a fórmula de Bhaskara?", "É a fórmula x = (−b ± √Δ) ÷ 2a, com Δ = b² − 4ac, que dá as raízes de qualquer equação do 2º grau ax² + bx + c = 0."),
           ("O que a BNCC pede sobre equações do 2º grau no 9º ano?", "Resolver e elaborar problemas que possam ser representados por equações polinomiais do 2º grau, usando a fatoração e os produtos notáveis.")]
    unit(R, "equacoes-do-2-grau", "A", ["EF09MA09"],
         "Compreender os processos de fatoração de expressões algébricas, com base em suas relações com os produtos notáveis, para resolver e elaborar problemas que possam ser representados por equações polinomiais do 2º grau",
         "Equações do 2º grau: fatoração e fórmula de Bhaskara", "Equações do 2º grau",
         "Atividades de matemática para o 9º ano sobre equações do 2º grau: equações incompletas, fatoração, discriminante, fórmula de Bhaskara, soma e produto das raízes e problemas. 100 exercícios com gabarito.",
         "Δ = b² − 4ac e x = (−b ± √Δ) ÷ 2a", "Δ > 0: duas raízes; Δ = 0: uma; Δ < 0: nenhuma real.",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
