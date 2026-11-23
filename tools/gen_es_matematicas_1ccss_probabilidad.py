# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Probabilidad (Sentido estocástico)
Sucesos y operaciones, regla de Laplace, tablas de contingencia (encuestas), probabilidad condicionada e independencia, probabilidad total y teorema de Bayes.
Reutiliza los generadores de Matemáticas II con otra semilla. s_contingencia también lo usa 2.º CCSS.
Errores: confundir P(A|B) con P(B|A), dividir entre el total en una condicionada, sumar P(A) y P(B) sin restar la intersección.
"""
import random
from fractions import Fraction as F
from es_ccss import M, mix, num, unit, L, W, use_, tabla, d, fq

R = random.Random(53009)
PB = "gen_es_matematicas_2bach_probabilidad"
s_sucesos, s_laplace, s_independencia, s_condicionada, s_bayes = use_(PB, 53209, "s_sucesos", "s_laplace", "s_independencia", "s_condicionada", "s_bayes")


def p(x):
    x = F(x)
    try:
        return d(x)
    except ValueError:
        return fq(x)


ENCUESTAS = [("estudiantes de Bachillerato", (("Ciencias", "estudia Ciencias"), ("CC. SS.", "estudia Ciencias Sociales")), (("Bus", "va en transporte público"), ("No bus", "no va en transporte público"))),
             ("trabajadores de una empresa", (("Mañana", "trabaja de mañana"), ("Tarde", "trabaja de tarde")), (("Teletrabaja", "teletrabaja algún día"), ("No", "no teletrabaja"))),
             ("clientes de un supermercado", (("&lt; 40 años", "tiene menos de 40 años"), ("≥ 40 años", "tiene 40 años o más")), (("Móvil", "paga con el móvil"), ("Otro", "paga de otra forma"))),
             ("vecinos de un municipio", (("Centro", "vive en el centro"), ("Afueras", "vive en las afueras")), (("Bici", "usa la bicicleta"), ("No bici", "no usa la bicicleta"))),
             ("lectores de un periódico", (("Papel", "lo lee en papel"), ("Internet", "lo lee en internet")), (("Economía", "lee la sección de economía"), ("No", "no la lee")))]


def tabla_c():
    if R.random() < 0.35:
        r1, r2_ = R.choice([(2, 3), (3, 2), (1, 4), (3, 7), (2, 8), (1, 3), (3, 5)])
        c1, c2 = R.choice([(3, 2), (1, 1), (2, 3), (1, 4), (3, 1), (2, 1)])
        k = R.choice([10, 20, 25])
        m = [[r1 * c1 * k, r1 * c2 * k], [r2_ * c1 * k, r2_ * c2 * k]]
        if sum(map(sum, m)) > 600:
            return None
        return m
    N = R.choice([100, 120, 150, 200, 250, 300, 400])
    m = [R.randint(N // 20, N // 3) for _ in range(3)]
    m.append(N - sum(m))
    if m[3] < N // 20:
        return None
    return [m[:2], m[2:]]


def s_contingencia():
    quien, ((f1, F1), (f2, F2)), ((c1, C1), (c2, C2)) = R.choice(ENCUESTAS)
    m = tabla_c()
    if not m:
        return None
    N = sum(map(sum, m))
    T = tabla(["", c1, c2, "Total"], [[f1, str(m[0][0]), str(m[0][1]), str(sum(m[0]))], [f2, str(m[1][0]), str(m[1][1]), str(sum(m[1]))],
                                      ["Total", str(m[0][0] + m[1][0]), str(m[0][1] + m[1][1]), str(N)]])
    intro = T + "Se pregunta a %d %s y se elige uno al azar. Sean A = «%s» y B = «%s». " % (N, quien, F1, C1)
    fA, cB = sum(m[0]), m[0][0] + m[1][0]
    t = R.choice(["simple", "inter", "union", "cond", "cond", "cond2", "indep", "indep"])
    if t == "simple":
        return M(intro + "Calcula P(B).", p(F(cB, N)), W([p(F(m[0][0], N)), p(F(cB, fA)), p(F(N - cB, N)), p(F(m[0][0], cB))]), "Total de la columna «%s» entre el total: %d/%d = <b>%s</b>." % (c1, cB, N, p(F(cB, N))))
    if t == "inter":
        return M(intro + "Calcula P(A ∩ B).", p(F(m[0][0], N)), W([p(F(fA, N) * F(cB, N)), p(F(m[0][0], fA)), p(F(m[0][0], cB)), p(F(fA + cB, N)) if fA + cB <= N else None]),
                 "Casilla de A y B: %d/%d = <b>%s</b>." % (m[0][0], N, p(F(m[0][0], N))))
    if t == "union":
        u = fA + cB - m[0][0]
        return M(intro + "Calcula P(A ∪ B).", p(F(u, N)), W([p(F(fA + cB, N)) if fA + cB <= N else None, p(F(m[0][0], N)), p(F(fA, N)), p(F(N - u, N))]),
                 "P(A ∪ B) = (%d + %d − %d)/%d = <b>%s</b>. Hay que restar la intersección." % (fA, cB, m[0][0], N, p(F(u, N))))
    if t == "cond":
        return M(intro + "Calcula P(B|A).", p(F(m[0][0], fA)), W([p(F(m[0][0], N)), p(F(m[0][0], cB)), p(F(cB, N)), p(F(m[0][1], fA))]),
                 "Solo cuenta la fila «%s»: %d/%d = <b>%s</b>." % (f1, m[0][0], fA, p(F(m[0][0], fA))))
    if t == "cond2":
        return M(intro + "Calcula P(Ā|B).", p(F(m[1][0], cB)), W([p(F(m[1][0], N)), p(F(m[1][0], sum(m[1]))), p(F(m[0][0], cB)), p(F(sum(m[1]), N))]),
                 "Solo cuenta la columna «%s»; Ā es la fila «%s»: %d/%d = <b>%s</b>." % (c1, f2, m[1][0], cB, p(F(m[1][0], cB))))
    ind = F(m[0][0], N) == F(fA, N) * F(cB, N)
    ok = "sí, porque P(A ∩ B) = P(A) · P(B)" if ind else "no, porque P(A ∩ B) ≠ P(A) · P(B)"
    return M(intro + "¿Son A y B independientes?", ok, [x for x in ("sí, porque P(A ∩ B) = P(A) · P(B)", "no, porque P(A ∩ B) ≠ P(A) · P(B)", "no, porque son incompatibles", "sí, porque P(A ∩ B) ≠ 0") if x != ok],
             "P(A ∩ B) = %s y P(A) · P(B) = %s · %s = %s: <b>%s</b>." % (p(F(m[0][0], N)), p(F(fA, N)), p(F(cB, N)), p(F(fA, N) * F(cB, N)), ok))


if __name__ == "__main__":
    seen = set()
    sets = [("Sucesos y operaciones", mix(R, seen, [(s_sucesos, 20)])), ("Regla de Laplace", mix(R, seen, [(s_laplace, 20)])), ("Tablas de contingencia", mix(R, seen, [(s_contingencia, 20)])),
            ("Condicionada e independencia", mix(R, seen, [(s_condicionada, 10), (s_independencia, 10)])), ("Probabilidad total y Bayes", mix(R, seen, [(s_bayes, 20)]))]
    think = ["<b>Regla de Laplace</b>: P(A) = casos favorables / casos posibles (si todos son igual de probables).",
             "P(A ∪ B) = P(A) + P(B) − P(A ∩ B); P(Ā) = 1 − P(A).",
             "<b>Probabilidad condicionada</b>: P(A|B) = P(A ∩ B)/P(B). En una tabla de contingencia, se mira solo la fila o la columna de B.",
             "A y B son <b>independientes</b> si P(A ∩ B) = P(A) · P(B). <b>Probabilidad total</b> y <b>Bayes</b> se resuelven con un diagrama de árbol."]
    ex = [("200 encuestados; 80 de Ciencias, de ellos 50 van en bus. P(bus | Ciencias)", ["fila de Ciencias: 50 de 80"], "50/80 = 0,625")]
    mist = [["Confundir P(A|B) con P(B|A)", "La condición es lo que ya sabes: va detrás de la barra."], ["Dividir entre el total en una condicionada", "Divide entre el total de la fila o columna de la condición."],
            ["Sumar sin restar la intersección", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)."]]
    body = L(think, ex, mist)
    faq = [("¿Qué es una tabla de contingencia?", "Una tabla de doble entrada con los datos de dos características (por ejemplo, tipo de Bachillerato y medio de transporte). Permite calcular probabilidades simples, de intersecciones y condicionadas."),
           ("¿Qué dice el teorema de Bayes?", "Permite calcular la probabilidad de una causa sabiendo el resultado: P(A<sub>i</sub>|B) = P(A<sub>i</sub>) · P(B|A<sub>i</sub>) / P(B).")]
    unit(1, R, "probabilidad", "S", "Probabilidad: sucesos, regla de Laplace, tablas de contingencia, probabilidad condicionada, independencia, probabilidad total y teorema de Bayes",
         "Probabilidad", "Probabilidad", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: Laplace, tablas de contingencia, probabilidad condicionada, independencia y Bayes. 100 ejercicios.",
         "P(A|B) = P(A ∩ B) / P(B)", "En la tabla: mira solo la fila de la condición.", body, faq, sets, 9)
