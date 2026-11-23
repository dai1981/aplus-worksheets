# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Sistemas de equações do 1º grau (Álgebra, EF08MA08)
  python3 tools/gen_br_matematica_8_sistemas_de_equacoes.py
Sistemas de duas equações com duas incógnitas: verificar a solução, método da substituição, método da adição, interpretação
gráfica (ponto de encontro das retas) e problemas (soma e diferença, animais e patas, preços, idades).
Erros: substituir só numa equação, somar as equações sem eliminar uma incógnita, responder só x quando pedem os dois valores.
"""
import random
from br_common import lesson, mix, reais
from br_9 import M, d, expr, kosy, unit

R = random.Random(88008)


def sis(a, b, c, e, f, g):
    return "<span class='sys'>%s = %s<br>%s = %s</span>" % (expr([(a, "x"), (b, "y")]), d(c), expr([(e, "x"), (f, "y")]), d(g))


def P(x, y):
    return "x = %s e y = %s" % (d(x), d(y))


def gen():
    while True:
        x, y = R.randint(-5, 9), R.randint(-5, 9)
        a, b, e, f = [R.choice([1, 1, 2, 3, -1, -2]) for _ in range(4)]
        if a * f - b * e != 0:
            return x, y, a, b, e, f


def s1_verificar():
    x, y, a, b, e, f = gen()
    c, g = a * x + b * y, e * x + f * y
    ok = R.random() < 0.5
    px, py = (x, y) if ok else R.choice([(y, x), (x + 1, y), (x, y + 1)])
    good = a * px + b * py == c and e * px + f * py == g
    ans = "sim" if good else "não"
    return M("O par (%s, %s) é solução do sistema?<br>%s" % (d(px), d(py), sis(a, b, c, e, f, g)), ans, ["não" if good else "sim", "só da primeira equação", "não dá para saber"],
             "Substitua nas duas equações: %s. <b>%s</b>." % ("as duas ficam verdadeiras" if good else "pelo menos uma fica falsa", ans.capitalize()))


def s2_substituicao():
    x, y = R.randint(-4, 9), R.randint(-4, 9)
    a, b = R.choice([1, 2, 3, -1]), R.choice([2, 3, -2, 1])
    m, n = R.choice([1, 2, 3, -1, -2]), R.randint(-5, 5)
    y = m * x + n
    c = a * x + b * y
    if a + b * m == 0:
        return None
    q = "<span class='sys'>y = %s<br>%s = %s</span>" % (expr([(m, "x"), (n, "")]), expr([(a, "x"), (b, "y")]), d(c))
    return M("Resolva o sistema pelo método da substituição:<br>%s" % q, P(x, y), [P(y, x) if x != y else P(x + 1, y), P(x, y + 1), P(-x, y) if x else P(x, -y)],
             "Troque y por %s na 2ª equação: %s = %s → x = %s; y = %s. <b>%s</b>." % (expr([(m, "x"), (n, "")]), expr([(a + b * m, "x"), (b * n, "")]), d(c), d(x), d(y), P(x, y)))


def s3_adicao():
    x, y = R.randint(-4, 9), R.randint(-4, 9)
    a, b = R.choice([1, 2, 3]), R.choice([1, 2, 3, 4])
    e = R.choice([1, 2, -1, 3])
    f = -b
    c, g = a * x + b * y, e * x + f * y
    if a + e == 0:
        return None
    return M("Resolva o sistema pelo método da adição:<br>%s" % sis(a, b, c, e, f, g), P(x, y), [P(y, x) if x != y else P(x + 2, y), P(x, -y) if y else P(x, 1), P(x + 1, y - 1)],
             "Somando as equações, y some: %s = %s → x = %s; substituindo: y = %s. <b>%s</b>." % (expr([(a + e, "x")]), d(c + g), d(x), d(y), P(x, y)))


def s4_grafico():
    x, y = R.randint(-3, 3), R.randint(-3, 3)
    m1, m2 = R.sample([-2, -1, 1, 2], 2)
    n1, n2 = y - m1 * x, y - m2 * x
    if abs(n1) > 5 or abs(n2) > 5:
        return None
    pic = kosy(lines=[(m1, n1, "#1f77b4", "r"), (m2, n2, "#c0392b", "s")], label="duas retas que se cruzam")
    return M(pic + "As retas r e s representam as equações de um sistema. Qual é a solução do sistema?", "(%s, %s)" % (d(x), d(y)), ["(%s, %s)" % (d(y), d(x)) if x != y else "(%s, %s)" % (d(x + 1), d(y)), "(0, %s)" % d(n1) if (0, n1) != (x, y) else "(0, %s)" % d(n2), "(%s, 0)" % d(x) if y else "(%s, 1)" % d(x)],
             "A solução é o ponto onde as retas se cruzam: <b>(%s, %s)</b>." % (d(x), d(y)))


def s5_problemas():
    k = R.choice(["somadif", "patas", "precos", "idades", "notas"])
    if k == "somadif":
        x, y = R.randint(10, 60), R.randint(2, 40)
        if x <= y:
            return None
        return M("A soma de dois números é %d e a diferença é %d. Quais são os números?" % (x + y, x - y), "%d e %d" % (x, y), ["%d e %d" % (x + 1, y - 1), "%d e %d" % ((x + y) // 2, (x + y) // 2 + (x + y) % 2), "%d e %d" % (x - y, y)],
                 "x + y = %d e x − y = %d; somando: 2x = %d → x = %d, y = %d. <b>%d e %d</b>." % (x + y, x - y, 2 * x, x, y, x, y))
    if k == "patas":
        g, c = R.randint(3, 20), R.randint(3, 20)
        return M("Num sítio há galinhas e cabras: %d cabeças e %d patas. Quantas são as cabras?" % (g + c, 2 * g + 4 * c), "%d cabras" % c, ["%d cabras" % g, "%d cabras" % ((2 * g + 4 * c) // 4), "%d cabras" % ((g + c) // 2)],
                 "g + c = %d e 2g + 4c = %d. Tirando 2 × (1ª): 2c = %d → <b>c = %d</b>." % (g + c, 2 * g + 4 * c, 2 * c, c))
    if k == "precos":
        a, b = R.randint(3, 15), R.randint(2, 10)
        p, q = R.randint(1, 4), R.randint(1, 4)
        r, s = R.randint(1, 4), R.randint(1, 4)
        if p * s - q * r == 0:
            return None
        su = lambda n: "%d suco%s" % (n, "" if n == 1 else "s")
        pa = lambda n: "%d %s" % (n, "pastel" if n == 1 else "pastéis")
        return M("%s e %s custam %s; %s e %s custam %s. Quanto custa um suco?" % (su(p), pa(q), reais((p * a + q * b) * 100), su(r), pa(s), reais((r * a + s * b) * 100)), reais(a * 100), [reais(b * 100), reais((a + b) * 100), reais((a + 1) * 100)],
                 "Montando o sistema e resolvendo: suco %s e pastel %s. <b>%s</b>." % (reais(a * 100), reais(b * 100), reais(a * 100)))
    if k == "idades":
        f, dif = R.randint(5, 20), R.randint(20, 35)
        return M("Pai e filho têm juntos %d anos. O pai tem %d anos a mais que o filho. Qual é a idade do filho?" % (2 * f + dif, dif), "%d anos" % f, ["%d anos" % (f + dif), "%d anos" % ((2 * f + dif) // 2), "%d anos" % (f + 1)],
                 "p + f = %d e p − f = %d; subtraindo: 2f = %d → <b>f = %d anos</b>." % (2 * f + dif, dif, 2 * f, f))
    x, y = R.randint(5, 20), R.randint(5, 20)
    a, b = R.choice([(2, 5), (5, 10), (10, 20), (20, 50)])
    return M("Tenho %d notas, umas de R$ %d,00 e outras de R$ %d,00, somando R$ %d,00. Quantas notas de R$ %d,00 tenho?" % (x + y, a, b, a * x + b * y, b), d(y), [d(x), d((a * x + b * y) // b), d(y + 1)],
             "x + y = %d e %dx + %dy = %d → <b>y = %d</b>." % (x + y, a, b, a * x + b * y, y))


def main():
    seen = set()
    sets = [
        ("Verificar a solução", mix(R, seen, [(s1_verificar, 20)])),
        ("Método da substituição", mix(R, seen, [(s2_substituicao, 20)])),
        ("Método da adição", mix(R, seen, [(s3_adicao, 20)])),
        ("Interpretação gráfica", mix(R, seen, [(s4_grafico, 20)])),
        ("Problemas", mix(R, seen, [(s5_problemas, 20)])),
    ]
    body = lesson(
        ["Um <b>sistema</b> tem duas equações; a solução é o par (x, y) que satisfaz as duas ao mesmo tempo.",
         "<b>Substituição</b>: isole uma incógnita numa equação e troque na outra.",
         "<b>Adição</b>: some (ou subtraia) as equações para eliminar uma incógnita; se precisar, multiplique uma delas antes.",
         "No gráfico, a solução é o ponto onde as duas retas se cruzam."],
        [("x + y = 10 e x − y = 4", ["somando: 2x = 14", "x = 7", "y = 3"], "x = 7 e y = 3")],
        [["Substituir na mesma equação", "Use a expressão isolada na outra equação."],
         ["Somar sem eliminar nada", "Ajuste os coeficientes para uma incógnita sumir."],
         ["Responder só o x", "A solução é o par (x, y)."]],
        kosy(lines=[(1, 1, "#1f77b4", "r"), (-1, 3, "#c0392b", "s")]))
    faq = [("Como resolver um sistema de equações?", "Pelo método da substituição (isolar uma incógnita e trocar na outra equação) ou pelo método da adição (somar as equações para eliminar uma incógnita). Depois, calcule a outra incógnita."),
           ("O que a BNCC pede no 8º ano?", "Resolver e elaborar problemas relacionados ao seu contexto próximo, que possam ser representados por sistemas de equações de 1º grau com duas incógnitas e interpretá-los, utilizando, inclusive, o plano cartesiano como recurso (EF08MA08).")]
    unit(R, "sistemas-de-equacoes", "A", ["EF08MA08"],
         "Resolver e elaborar problemas relacionados ao seu contexto próximo, que possam ser representados por sistemas de equações de 1º grau com duas incógnitas e interpretá-los, utilizando, inclusive, o plano cartesiano como recurso",
         "Sistemas de equações do 1º grau", "Sistemas de equações",
         "Atividades de matemática para o 8º ano sobre sistemas de equações do 1º grau: verificar a solução, métodos da substituição e da adição, interpretação gráfica e problemas. 100 exercícios com gabarito.",
         "A solução satisfaz as duas equações.", "No gráfico: o ponto de encontro das retas.",
         body, faq, sets, 8, grade="8-ano")


if __name__ == "__main__":
    main()
