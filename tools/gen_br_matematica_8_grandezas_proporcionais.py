# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Grandezas proporcionais e suas leis (Álgebra, EF08MA12, EF08MA13)
  python3 tools/gen_br_matematica_8_grandezas_proporcionais.py
Identificar se duas grandezas são diretamente proporcionais, inversamente proporcionais ou não proporcionais; escrever a lei
(y = k · x ou x · y = k) e achar a constante; gráfico da proporção direta (reta que passa pela origem); problemas.
Usa geradores do 9º ano (grandezas proporcionais) com outro sorteio.
Erros: achar que toda reta é proporção direta, usar a regra direta em grandezas inversas, achar k pela diferença.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, ntab, kosy, unit

R = random.Random(88011)
g_tipo, g_tab, g_dir, g_inv = use("gen_br_matematica_9_grandezas_proporcionais", 88911, "s1_tipo", "s1_tabela", "s2_direta", "s3_inversa")


def s1_lei():
    k = R.choice(["dir", "inv"])
    xs = sorted(R.sample([1, 2, 3, 4, 5, 6, 8, 10, 12], 4))
    if k == "dir":
        c = R.choice([2, 3, 4, 5, 7, 12, 15])
        ys = [c * x for x in xs]
        ok = "y = %dx" % c
        return M(ntab(xs, ys) + "As grandezas são diretamente proporcionais. Qual é a lei que relaciona y e x?", ok, ["y = x + %d" % (ys[0] - xs[0]) if ys[0] != xs[0] else "y = x + 1", "x · y = %d" % (xs[0] * ys[0]), "y = %dx + %d" % (c, c)],
                     "y ÷ x é sempre %d: <b>%s</b>." % (c, ok))
    c = R.choice([24, 36, 48, 60, 72, 120])
    xs = [x for x in [1, 2, 3, 4, 6, 8, 12] if c % x == 0][:4]
    ys = [c // x for x in xs]
    ok = "x · y = %d" % c
    return M(ntab(xs, ys) + "As grandezas são inversamente proporcionais. Qual é a lei?", ok, ["y = %dx" % ys[0], "x + y = %d" % (xs[0] + ys[0]), "y = x − %d" % abs(xs[0] - ys[0])],
             "O produto x · y é sempre %d: <b>%s</b> (ou y = %d/x)." % (c, ok, c))


def s2_constante():
    k = R.choice(["dir", "inv"])
    if k == "dir":
        c = F(R.choice([F(3, 2), F(5, 2), 4, 6, F(12, 10), 8]))
        x = R.randint(2, 9) * 2
        y = c * x
        return M("y é diretamente proporcional a x. Quando x = %d, y = %s. Qual é y quando x = %d?" % (x, d(y), x + 6), d(c * (x + 6)), [d(y + 6), d(y * x / (x + 6), 2) if (y * x / (x + 6) * 100).denominator == 1 else d(c * (x + 6) + 1), d(c * (x + 6) * 2)],
                     "k = y ÷ x = %s; y = %s · %d = <b>%s</b>." % (d(c), d(c), x + 6, d(c * (x + 6))))
    c = R.choice([24, 36, 48, 60, 72, 120])
    x1, x2 = R.sample([x for x in range(2, 13) if c % x == 0], 2)
    return M("y é inversamente proporcional a x. Quando x = %d, y = %d. Qual é y quando x = %d?" % (x1, c // x1, x2), d(c // x2), [d(F(c // x1 * x2, x1), 1) if (F(c // x1 * x2, x1) * 10).denominator == 1 else d(c // x2 + 1), d(c // x1 + x2 - x1) if c // x1 + x2 - x1 > 0 else d(c), d(c)],
             "k = x · y = %d; y = %d ÷ %d = <b>%d</b>." % (c, c, x2, c // x2))


def s3_grafico():
    k = R.choice(["dir", "nao", "dir", "nao2"])
    if k == "dir":
        m = R.choice([1, 2, 3])
        pic = kosy(lines=[(m, 0, "#1f77b4", "")], lo=0, hi=8, label="gráfico de y em função de x")
        ans = "sim, é uma reta que passa pela origem"
    elif k == "nao":
        m, n = R.choice([(1, 2), (2, 1), (1, 3), (F(1, 2), 2)])
        pic = kosy(lines=[(float(m), n, "#1f77b4", "")], lo=0, hi=8, label="gráfico de y em função de x")
        ans = "não, a reta não passa pela origem"
    else:
        pic = kosy(pts=[(1, 6, ""), (2, 3, ""), (3, 2, ""), (6, 1, "")], lo=0, hi=8, label="pontos de y em função de x")
        ans = "não, mas x · y é constante (proporção inversa)"
    opts = ["sim, é uma reta que passa pela origem", "não, a reta não passa pela origem", "não, mas x · y é constante (proporção inversa)", "sim, toda reta indica proporção direta"]
    return M(pic + "O gráfico mostra uma relação entre x e y. As grandezas são diretamente proporcionais?", ans, [o for o in opts if o != ans],
             "Proporção direta: os pontos ficam numa reta que passa por (0, 0). Resposta: <b>%s</b>." % ans)


def main():
    seen = set()
    sets = [
        ("Direta, inversa ou nenhuma?", mix(R, seen, [(g_tipo, 10), (g_tab, 10)])),
        ("A lei da relação", mix(R, seen, [(s1_lei, 20)])),
        ("A constante de proporcionalidade", mix(R, seen, [(s2_constante, 20)])),
        ("Gráficos", mix(R, seen, [(s3_grafico, 8), (g_tab, 12)])),
        ("Problemas", mix(R, seen, [(g_dir, 10), (g_inv, 10)])),
    ]
    body = lesson(
        ["<b>Diretamente proporcionais</b>: y ÷ x é constante (k). A lei é y = k · x, e o gráfico é uma reta que passa pela origem.",
         "<b>Inversamente proporcionais</b>: x · y é constante (k). A lei é y = k ÷ x.",
         "Se nem o quociente nem o produto são constantes, as grandezas não são proporcionais (ex.: y = 2x + 3)."],
        [("x: 2, 4, 6 → y: 10, 20, 30", ["y ÷ x = 5"], "y = 5x"),
         ("x: 2, 4, 8 → y: 20, 10, 5", ["x · y = 40"], "y = 40/x")],
        [["Achar que toda reta é proporção direta", "Ela precisa passar pela origem."],
         ["Usar a regra direta na inversa", "Na inversa, o produto é constante."],
         ["Achar k pela diferença", "Use o quociente (direta) ou o produto (inversa)."]],
        kosy(lines=[(2, 0, "#1f77b4", "")], lo=0, hi=8))
    faq = [("Como saber se duas grandezas são diretamente proporcionais?", "Divida y por x em vários pares: se o resultado for sempre o mesmo, são diretamente proporcionais. No gráfico, os pontos ficam numa reta que passa pela origem."),
           ("O que a BNCC pede no 8º ano?", "Identificar a natureza da variação de duas grandezas, diretamente, inversamente proporcionais ou não proporcionais, expressando a relação existente por meio de sentença algébrica e representá-la no plano cartesiano (EF08MA12) e resolver e elaborar problemas que envolvam grandezas diretamente ou inversamente proporcionais (EF08MA13).")]
    unit(R, "grandezas-proporcionais", "A", ["EF08MA12", "EF08MA13"],
         "Identificar a natureza da variação de duas grandezas, diretamente, inversamente proporcionais ou não proporcionais, expressando a relação existente por meio de sentença algébrica e representá-la no plano cartesiano; resolver e elaborar problemas que envolvam grandezas diretamente ou inversamente proporcionais, por meio de estratégias variadas",
         "Grandezas proporcionais: leis e gráficos", "Grandezas proporcionais",
         "Atividades de matemática para o 8º ano sobre grandezas proporcionais: direta, inversa ou não proporcional, lei y = kx e x · y = k, constante de proporcionalidade, gráficos e problemas. 100 exercícios com gabarito.",
         "Direta: y = k · x. Inversa: x · y = k.", "Proporção direta: reta pela origem.",
         body, faq, sets, 11, grade="8-ano")


if __name__ == "__main__":
    main()
