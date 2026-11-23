# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Funções seno e cosseno e fenômenos periódicos (EM13MAT306)
  python3 tools/gen_br_matematica_em2_funcoes_seno_e_cosseno.py
f(x) = a + b · sen(cx) e f(x) = a + b · cos(cx): imagem, amplitude, período (2π ÷ |c|), valor máximo e mínimo;
ler o gráfico; modelos periódicos (marés, roda-gigante, temperatura, pressão arterial).
Erros: período = 2π · c, confundir amplitude com a distância entre máximo e mínimo, esquecer o deslocamento vertical a.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, unit, curva, pit

R = random.Random(92004)


def lei(a, b, c, fn):
    arg = "x" if c == 1 else "%sx" % d(c) if F(c).denominator == 1 else "(%s)x" % d(c)
    if F(c).denominator != 1:
        arg = "x/%d" % F(c).denominator if F(c).numerator == 1 else arg
    t = ("" if b == 1 else ("−" if b == -1 else "%s · " % d(b))) + "%s(%s)" % (fn, arg) if fn else ""
    if a:
        return "f(x) = %s %s %s" % (d(a), "+" if b > 0 else "−", (("" if abs(b) == 1 else "%s · " % d(abs(b))) + "%s(%s)" % (fn, arg)))
    return "f(x) = " + t


def s1_param():
    fn = R.choice(["sen", "cos"])
    a = R.randint(-3, 4)
    b = R.choice([1, 2, 3, 4, -2, -1])
    c = R.choice([1, 2, 3, 4, F(1, 2)])
    f = lei(a, b, c, fn)
    per = F(2) / F(c)
    k = R.choice(["img", "per", "max", "amp", "min"])
    if k == "img":
        return M("Qual é a imagem de %s?" % f, "[%s, %s]" % (d(a - abs(b)), d(a + abs(b))), ["[%s, %s]" % (d(-abs(b)), d(abs(b))), "[%s, %s]" % (d(a - 1), d(a + 1)) if abs(b) != 1 else "[0, %s]" % d(a + 2), "[%s, %s]" % (d(a), d(a + abs(b)))],
                 "%s varia de −1 a 1; multiplicado por %s e somado %s: <b>[%s, %s]</b>." % (fn, d(b), d(a), d(a - abs(b)), d(a + abs(b))))
    if k == "per":
        return M("Qual é o período de %s?" % f, pit(per), [pit(2 * F(c)) if 2 * F(c) != per else "π/4", pit(F(2)), pit(per * 2)] if per != 2 else [pit(F(1)), pit(F(4)), "π/2"],
                 "Período = 2π ÷ |c| = 2π ÷ %s = <b>%s</b>." % (d(c), pit(per)))
    if k == "max":
        return M("Qual é o valor máximo de %s?" % f, d(a + abs(b)), [d(abs(b)), d(a + 1) if abs(b) != 1 else d(a + 2), d(a - abs(b))], "Máximo = %s + %s = <b>%s</b>." % (d(a), d(abs(b)), d(a + abs(b))))
    if k == "min":
        return M("Qual é o valor mínimo de %s?" % f, d(a - abs(b)), [d(-abs(b)), d(a), d(a + abs(b))], "Mínimo = %s − %s = <b>%s</b>." % (d(a), d(abs(b)), d(a - abs(b))))
    return M("Qual é a amplitude de %s?" % f, d(abs(b)), [d(2 * abs(b)), d(a) if a != abs(b) else d(abs(b) + 1), pit(per)], "Amplitude = |b| = <b>%s</b>." % d(abs(b)))


def s2_valor():
    fn = R.choice(["sen", "cos"])
    a = R.randint(-2, 3)
    b = R.choice([1, 2, 3])
    deg = R.choice([0, 30, 90, 180, 270, 150, 60])
    from br_em import trig
    v = trig(deg, fn)
    if v is None or "√" in v:
        return None
    val = a + b * F(v.replace("−", "-"))
    f = lei(a, b, 1, fn)
    return M("Para %s, quanto vale f(%s)?" % (f, pit(F(deg, 180))), d(val), [d(a + b), d(a - b) if a - b != val else d(a), d(b * F(v.replace("−", "-")))],
             "%s(%s) = %s; f = %s + %s · %s = <b>%s</b>." % (fn, pit(F(deg, 180)), v, d(a), d(b), v if not v.startswith("−") else "(%s)" % v, d(val)))


def s3_grafico():
    fn = R.choice(["sen", "cos"])
    a = R.choice([0, 0, 1, 2, -1])
    b = R.choice([1, 2, 3])
    c = R.choice([1, 2, F(1, 2)])
    g = curva([(lambda x: a + b * (math.sin if fn == "sen" else math.cos)(float(c) * x), "f")], (0, 4 * math.pi + 0.01, math.pi / 2), (-5, 5, 1),
              W=420, H=250, label="gráfico de uma função trigonométrica", xlab=lambda k: pit(F(round(k / math.pi * 2), 2)))
    k = R.choice(["per", "img", "lei"])
    per = F(2) / F(c)
    if k == "per":
        return M(g + "Qual é o período da função do gráfico?", pit(per), [pit(per / 2), pit(per * 2), pit(per + 1)], "O gráfico se repete a cada <b>%s</b>." % pit(per))
    if k == "img":
        return M(g + "Qual é a imagem da função do gráfico?", "[%s, %s]" % (d(a - b), d(a + b)), ["[%s, %s]" % (d(-b), d(b)) if a else "[%s, %s]" % (d(-b - 1), d(b + 1)), "[0, %s]" % d(a + b), "[%s, %s]" % (d(a - b - 1), d(a + b + 1))],
                 "O menor valor é %s e o maior é %s: <b>[%s, %s]</b>." % (d(a - b), d(a + b), d(a - b), d(a + b)))
    ans = lei(a, b, c, fn)
    w = [lei(a, b, c, "cos" if fn == "sen" else "sen"), lei(a, b, F(1) / F(c) if c != 1 else 2, fn), lei(-a if a else 1, b, c, fn), lei(a, b + 1, c, fn)]
    return M(g + "Qual lei corresponde ao gráfico?", ans, w, "Em x = 0, f = %s (%s); amplitude %d; período %s: <b>%s</b>." % (d(a + (0 if fn == "sen" else b)), "começa no meio, subindo" if fn == "sen" else "começa no máximo", b, pit(per), ans))


def s4_modelo():
    k = R.choice(["mare", "roda", "temp", "pressao"])
    if k == "mare":
        m, A = R.choice([(3, 1), (4, 2), (5, 2), (2, 1)])
        t = R.choice([0, 3, 6, 9, 12])
        v = m + A * round(math.sin(math.pi * t / 6))
        q = R.choice(["max", "per", "val"])
        f = "h(t) = %d + %d · sen(πt/6)" % (m, A) if A != 1 else "h(t) = %d + sen(πt/6)" % m
        if q == "max":
            return M("A altura da maré num porto é %s, em metros, com t em horas. Qual é a maré mais alta?" % f, "%d m" % (m + A), ["%d m" % m, "%d m" % A, "%d m" % (m + 2 * A)], "Máximo quando sen = 1: %d + %d = <b>%d m</b>." % (m, A, m + A))
        if q == "per":
            return M("A altura da maré num porto é %s, em metros, com t em horas. De quanto em quanto tempo o ciclo se repete?" % f, "12 horas", ["6 horas", "24 horas", "%d horas" % m], "Período = 2π ÷ (π/6) = <b>12 horas</b>.")
        return M("A altura da maré num porto é %s, em metros, com t em horas. Qual é a altura em t = %d h?" % (f, t), "%d m" % v, ["%d m" % m if v != m else "%d m" % (m + A), "%d m" % (m - A) if v != m - A else "%d m" % (m + 2 * A), "%d m" % (m + A) if v != m + A else "%d m" % (m + 2)],
                 "sen(π · %d/6) = %d; h = %d + %d · %d = <b>%d m</b>." % (t, round(math.sin(math.pi * t / 6)), m, A, round(math.sin(math.pi * t / 6)), v))
    if k == "roda":
        h0, r = R.choice([(12, 10), (20, 18), (15, 13), (32, 30)])
        q = R.choice(["max", "min"])
        if q == "max":
            return M("A altura de uma cadeira de roda-gigante é h(t) = %d − %d · cos(πt/5), em metros. Qual é a altura máxima?" % (h0, r), "%d m" % (h0 + r), ["%d m" % h0, "%d m" % r, "%d m" % (h0 - r)], "cos = −1 dá h = %d + %d = <b>%d m</b>." % (h0, r, h0 + r))
        return M("A altura de uma cadeira de roda-gigante é h(t) = %d − %d · cos(πt/5), em metros. Qual é a altura mínima?" % (h0, r), "%d m" % (h0 - r), ["0 m", "%d m" % h0, "%d m" % (h0 + r)], "cos = 1 dá h = %d − %d = <b>%d m</b>." % (h0, r, h0 - r))
    if k == "temp":
        m, A = R.choice([(20, 5), (25, 4), (18, 6), (22, 3)])
        q = R.choice(["amp", "var"])
        if q == "amp":
            return M("A temperatura numa cidade ao longo do dia é T(t) = %d + %d · sen(π(t − 9)/12), em °C. Qual é a diferença entre a maior e a menor temperatura?" % (m, A), "%d °C" % (2 * A), ["%d °C" % A, "%d °C" % m, "%d °C" % (m + A)], "Máx. %d e mín. %d: diferença <b>%d °C</b>." % (m + A, m - A, 2 * A))
        return M("A temperatura numa cidade ao longo do dia é T(t) = %d + %d · sen(π(t − 9)/12), em °C. Qual é a temperatura máxima?" % (m, A), "%d °C" % (m + A), ["%d °C" % m, "%d °C" % (m + 2 * A), "%d °C" % A], "sen = 1: <b>%d °C</b>." % (m + A))
    m, A = R.choice([(100, 20), (110, 15), (95, 25)])
    return M("A pressão sanguínea de uma pessoa é P(t) = %d + %d · sen(8πt/3), em mmHg, com t em segundos. Quais são a pressão máxima e a mínima?" % (m, A), "%d e %d mmHg" % (m + A, m - A), ["%d e %d mmHg" % (m + 2 * A, m), "%d e %d mmHg" % (m, m - A), "%d e 0 mmHg" % (m + A)],
             "%d ± %d: <b>%d e %d mmHg</b>." % (m, A, m + A, m - A))


s5_conceitos = bank(R, [
    ("O período da função f(x) = sen x é…", "2π", ["π", "π/2", "1"]),
    ("A imagem de f(x) = cos x é…", "[−1, 1]", ["[0, 1]", "todos os reais", "[0, 2π]"]),
    ("O gráfico de f(x) = sen x passa pela origem porque…", "sen 0 = 0", ["cos 0 = 0", "sen 0 = 1", "o período é 2π"]),
    ("O gráfico de y = cos x é o de y = sen x deslocado…", "π/2 para a esquerda", ["π para cima", "1 para a direita", "2π para baixo"]),
    ("Um fenômeno periódico é aquele que…", "se repete em intervalos iguais", ["cresce sempre", "diminui sempre", "não muda"]),
    ("Multiplicar x por 2 em sen(2x)…", "divide o período por 2", ["dobra o período", "dobra a amplitude", "desloca o gráfico para cima"]),
    ("Em f(x) = 3 + 2 sen x, o número 3…", "desloca o gráfico 3 unidades para cima", ["é a amplitude", "é o período", "é o valor máximo"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Imagem, amplitude e período", mix(R, seen, [(s1_param, 20)])),
        ("Valores das funções", mix(R, seen, [(s2_valor, 14), (s5_conceitos, 6)])),
        ("Gráficos", mix(R, seen, [(s3_grafico, 20)])),
        ("Fenômenos periódicos", mix(R, seen, [(s4_modelo, 20)])),
        ("Revisão", mix(R, seen, [(s1_param, 12), (s4_modelo, 7), (s5_conceitos, 1)])),
    ]
    body = lesson(
        ["As funções <b>seno</b> e <b>cosseno</b> são periódicas: o gráfico se repete. Para f(x) = sen x e f(x) = cos x, o período é 2π e a imagem é [−1, 1].",
         "Em f(x) = a + b · sen(cx) (ou cos): <b>a</b> desloca para cima ou para baixo; <b>|b|</b> é a amplitude; o <b>período</b> é 2π ÷ |c|.",
         "Imagem: [a − |b|, a + |b|]. Máximo a + |b|, mínimo a − |b|.",
         "Marés, rodas-gigantes, temperaturas ao longo do dia e batimentos do coração podem ser modelados por essas funções."],
        [("f(x) = 2 + 3 sen(2x)", ["amplitude 3", "período 2π ÷ 2 = π", "imagem [2 − 3, 2 + 3]"], "imagem [−1, 5], período π")],
        [["Período = 2π · c", "É 2π ÷ |c|: c maior, período menor."],
         ["Amplitude = máximo − mínimo", "A amplitude é metade dessa distância."],
         ["Esquecer o a", "a desloca a imagem toda."]],
        curva([(math.sin, "sen x"), (math.cos, "cos x")], (0, 2 * math.pi + 0.01, math.pi / 2), (-2, 2, 1), W=420, label="gráficos de y = sen x e y = cos x", xlab=lambda k: pit(F(round(k / math.pi * 2), 2))))
    faq = [("Como calcular o período de f(x) = sen(cx)?", "Divida 2π por |c|. Para sen(3x), o período é 2π/3."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas em contextos que envolvem fenômenos periódicos reais (ondas sonoras, fases da lua, movimentos cíclicos, entre outros) e comparar suas representações com as funções seno e cosseno, no plano cartesiano (EM13MAT306).")]
    unit(R, "funcoes-seno-e-cosseno", "A", ["EM13MAT306"],
         "Resolver e elaborar problemas em contextos que envolvem fenômenos periódicos reais (ondas sonoras, fases da lua, movimentos cíclicos, entre outros) e comparar suas representações com as funções seno e cosseno, no plano cartesiano, com ou sem apoio de aplicativos de álgebra e geometria",
         "Funções seno e cosseno e fenômenos periódicos", "Funções seno e cosseno",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre funções seno e cosseno: imagem, amplitude, período, gráficos e fenômenos periódicos como marés e roda-gigante. 100 exercícios com gabarito.",
         "Período = 2π ÷ |c|", "Imagem de a + b sen(cx): [a − |b|, a + |b|].",
         body, faq, sets, 4, grade="2-serie")


if __name__ == "__main__":
    main()
