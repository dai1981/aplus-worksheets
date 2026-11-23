# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Linguagem algébrica e expressões (Álgebra, EF07MA13, EF07MA16)
  python3 tools/gen_br_matematica_7_linguagem_algebrica_e_expressoes.py
Variável e incógnita; traduzir frases para a linguagem algébrica (o dobro de um número mais 5 → 2x + 5); valor numérico;
termos semelhantes e expressões equivalentes (3x + 2x = 5x; 2(x + 4) = 2x + 8); perímetro com letras.
Erros: x + x = x², 2(x + 4) = 2x + 4, «o dobro de x mais 3» como 2(x + 3), trocar a ordem na subtração.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, expr, par, bank, unit

R = random.Random(87007)


def s1_traduzir():
    a, b = R.randint(2, 9), R.randint(2, 15)
    t = R.choice([("o dobro de um número mais %d" % b, "2x + %d" % b, ["2(x + %d)" % b, "x² + %d" % b, "2 + x + %d" % b]),
                  ("o triplo de um número menos %d" % b, "3x − %d" % b, ["3(x − %d)" % b, "%d − 3x" % b, "x³ − %d" % b]),
                  ("a metade de um número mais %d" % b, "x/2 + %d" % b, ["(x + %d)/2" % b, "2x + %d" % b, "x − 2 + %d" % b]),
                  ("o quadrado de um número" , "x²", ["2x", "x + 2", "x · 2"]),
                  ("a soma de um número com o seu sucessor", "x + (x + 1)", ["x + 1", "2x", "x · (x + 1)"]),
                  ("%d vezes a soma de um número com %d" % (a, b), "%d(x + %d)" % (a, b), ["%dx + %d" % (a, b), "%d + x + %d" % (a, b), "x(%d + %d)" % (a, b)]),
                  ("a diferença entre %d e um número" % b, "%d − x" % b, ["x − %d" % b, "%dx" % b, "%d + x" % b]),
                  ("o dobro da soma de um número com %d" % b, "2(x + %d)" % b, ["2x + %d" % b, "x + 2 + %d" % b, "2 + x + %d" % b]),
                  ("um número aumentado de %d%%" % (b * 5), "x + %dx/100" % (b * 5), ["x + %d" % (b * 5), "%dx" % (b * 5), "x/%d" % (b * 5)])])
    return M("Como se escreve «%s» usando x para o número?" % t[0], t[1], t[2], "<b>%s</b>." % t[1])


def s2_valor():
    a, b, c = R.randint(2, 9) * R.choice([1, -1]), R.randint(-12, 12), R.randint(1, 3)
    x = R.choice([v for v in range(-5, 7) if v])
    k = R.choice(["lin", "quad", "duas"])
    if k == "lin":
        e = expr([(a, "x"), (b, "")])
        v = a * x + b
        return M("Qual é o valor numérico de %s para x = %s?" % (e, d(x)), d(v), [d(a + x + b), d(a * x - b) if b else d(v + 1), d(-v) if v else "1"], "Troque x por %s: %s · %s %s = <b>%s</b>." % (d(x), d(a), par(x), ("+ %d" % b) if b >= 0 else "− %d" % -b, d(v)))
    if k == "quad":
        v = x * x + b
        return M("Qual é o valor numérico de x² + %s para x = %s?" % (par(b) if b < 0 else d(b), d(x)), d(v), [d(2 * x + b), d(-x * x + b), d(v + 2)], "%s² = %d; %d + %s = <b>%s</b>." % (par(x), x * x, x * x, par(b), d(v)))
    y = R.randint(-4, 6)
    v = 2 * x - 3 * y
    return M("Qual é o valor de 2x − 3y para x = %s e y = %s?" % (d(x), d(y)), d(v), [d(2 * x + 3 * y), d(2 * y - 3 * x), d(-v) if v else "1"], "2 · %s − 3 · %s = %s − %s = <b>%s</b>." % (par(x), par(y), d(2 * x), par(3 * y), d(v)))


def s3_semelhantes():
    a, b, c, e = R.randint(1, 9), R.randint(1, 9) * R.choice([1, -1]), R.randint(1, 12), R.randint(1, 12) * R.choice([1, -1])
    if a + b == 0 or c + e == 0:
        return None
    q = "%s %s %s %s" % (expr([(a, "x"), (c, "")]), "+" if b > 0 else "−", expr([(abs(b), "x")]), ("+ %d" % e) if e > 0 else "− %d" % -e)
    ok = expr([(a + b, "x"), (c + e, "")])
    return M("Simplifique %s." % q, ok, [expr([(a + abs(b), "x"), (c + e, "")]) if b < 0 else expr([(a * b, "x"), (c + e, "")]), expr([(a + b + c + e, "x")]) if a + b + c + e else "x", expr([(a + b, "x²"), (c + e, "")])],
             "Junte os termos com x e os números: <b>%s</b>." % ok)


def s4_distributiva():
    a, b, c = R.randint(2, 9) * R.choice([1, 1, -1]), R.randint(1, 9) * R.choice([1, -1]), R.randint(2, 6)
    q = "%s(x %s %d)" % (d(a) if a != -1 else "−", "+" if b > 0 else "−", abs(b))
    ok = expr([(a, "x"), (a * b, "")])
    return M("Qual expressão é equivalente a %s?" % q, ok, [expr([(a, "x"), (b, "")]), expr([(a, "x"), (-a * b, "")]), expr([(a + b, "x")]) if a + b else "x"],
             "Multiplique %s por cada termo: <b>%s</b>." % (d(a), ok))


def s5_perimetro():
    a, b = R.randint(1, 5), R.randint(1, 9)
    k = R.choice(["ret", "quad", "tri"])
    if k == "ret":
        ok = expr([(2 * a + 2, "x"), (2 * b, "")])
        return M("Um retângulo tem lados x e %s. Qual expressão dá o seu perímetro?" % expr([(a, "x"), (b, "")]), ok, [expr([(a + 1, "x"), (b, "")]), expr([(a, "x²"), (b, "x")]), expr([(2 * a + 2, "x"), (b, "")])],
                 "2 · x + 2 · (%s) = <b>%s</b>." % (expr([(a, "x"), (b, "")]), ok))
    if k == "quad":
        ok = expr([(4, "x"), (4 * b, "")])
        return M("Um quadrado tem lado x + %d. Qual expressão dá o seu perímetro?" % b, ok, [expr([(4, "x"), (b, "")]), expr([(1, "x"), (4 * b, "")]), expr([(1, "x²"), (b * b, "")])], "4 · (x + %d) = <b>%s</b>." % (b, ok))
    ok = expr([(3 + a, "x"), (b, "")])
    return M("Um triângulo tem lados x, 2x e %s. Qual expressão dá o seu perímetro?" % expr([(a, "x"), (b, "")]), ok, [expr([(3, "x"), (b, "")]), expr([(2 * a, "x³"), (b, "")]), expr([(3 + a, "x")])], "x + 2x + %s = <b>%s</b>." % (expr([(a, "x"), (b, "")]), ok))


s6_conceitos = bank(R, [
    ("Em 2x + 5, o número 2 chama-se…", "coeficiente", ["incógnita", "termo independente", "expoente"]),
    ("x + x é igual a…", "2x", ["x²", "2", "xx"]),
    ("x · x é igual a…", "x²", ["2x", "x", "2"]),
    ("3x e 3x² são termos semelhantes?", "não, a parte literal é diferente", ["sim, têm o mesmo coeficiente", "sim, sempre", "só se x = 1"]),
    ("Numa fórmula como P = 4L, a letra L é…", "uma variável", ["um número fixo sempre igual a 4", "uma unidade de medida", "uma incógnita sem valor"]),
    ("Na equação x + 3 = 10, a letra x é…", "uma incógnita", ["um coeficiente", "uma constante igual a 3", "um expoente"]),
    ("As expressões 2(x + 3) e 2x + 6 são…", "equivalentes", ["diferentes para todo x", "iguais só se x = 0", "equações"]),
    ("O valor de 5x quando x = 0 é…", "0", ["5", "50", "não existe"]),
], "s6_conceitos")


def main():
    seen = set()
    sets = [
        ("Da frase para a expressão", mix(R, seen, [(s1_traduzir, 14), (s6_conceitos, 6)])),
        ("Valor numérico", mix(R, seen, [(s2_valor, 20)])),
        ("Termos semelhantes", mix(R, seen, [(s3_semelhantes, 20)])),
        ("Propriedade distributiva", mix(R, seen, [(s4_distributiva, 20)])),
        ("Perímetros com letras", mix(R, seen, [(s5_perimetro, 18), (s6_conceitos, 2)])),
    ]
    body = lesson(
        ["Na <b>linguagem algébrica</b>, usamos letras para representar números: «o dobro de um número mais 5» é 2x + 5.",
         "Uma letra pode ser <b>variável</b> (pode assumir vários valores, como em P = 4L) ou <b>incógnita</b> (um valor a descobrir numa equação).",
         "<b>Valor numérico</b>: troque a letra pelo número e calcule.",
         "Some só <b>termos semelhantes</b> (mesma parte literal): 3x + 2x = 5x. Na distributiva, multiplique cada termo: 2(x + 4) = 2x + 8."],
        [("3x − 4 para x = −2", ["3 · (−2) − 4"], "−10"),
         ("4(x − 3) + 2x", ["4x − 12 + 2x"], "6x − 12")],
        [["Escrever x + x = x²", "x + x = 2x; x · x = x²."],
         ["Distribuir só no primeiro termo", "2(x + 4) = 2x + 8."],
         ["«O dobro de x mais 3» como 2(x + 3)", "Primeiro dobre x, depois some 3: 2x + 3."]])
    faq = [("Qual é a diferença entre variável e incógnita?", "A variável representa números que podem mudar (como o lado L em P = 4L). A incógnita é um valor desconhecido e fixo que queremos descobrir numa equação."),
           ("O que a BNCC pede no 7º ano?", "Compreender a ideia de variável, representada por letra ou símbolo, para expressar relação entre duas grandezas, diferenciando-a da ideia de incógnita (EF07MA13) e reconhecer se duas expressões algébricas obtidas para descrever a regularidade de uma mesma sequência numérica são ou não equivalentes (EF07MA16).")]
    unit(R, "linguagem-algebrica-e-expressoes", "A", ["EF07MA13", "EF07MA16"],
         "Compreender a ideia de variável, representada por letra ou símbolo, para expressar relação entre duas grandezas, diferenciando-a da ideia de incógnita; reconhecer se duas expressões algébricas obtidas para descrever a regularidade de uma mesma sequência numérica são ou não equivalentes",
         "Linguagem algébrica e expressões", "Expressões algébricas",
         "Atividades de matemática para o 7º ano sobre linguagem algébrica: traduzir frases em expressões, valor numérico, termos semelhantes, propriedade distributiva, expressões equivalentes e perímetros com letras. 100 exercícios com gabarito.",
         "Some só termos semelhantes.", "2(x + 4) = 2x + 8",
         body, faq, sets, 7, grade="7-ano")


if __name__ == "__main__":
    main()
