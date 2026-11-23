# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Lenguaje algebraico (Sentido algebraico)
Traducir enunciados, valor numérico, monomios (coeficiente, parte literal, grado, semejantes), reducir términos semejantes y quitar paréntesis, expresiones en contexto.
Errores: escribir x² por «el doble», sumar monomios no semejantes (2x + 3 = 5x), olvidar multiplicar todos los términos del paréntesis.
"""
import random
from es_eso import M, mix, E, sg, par, num, unit, L, Kids, nz, sup

R = random.Random(47007)
K = Kids(R)


def s_traducir():
    a = R.randint(2, 9)
    items = [("el doble de un número", "2x", ["x²", "x + 2", "2 + x²"]), ("el triple de un número", "3x", ["x³", "x + 3", "3 + x"]),
             ("la mitad de un número", "x/2", ["2x", "x − 2", "x²/2"]), ("el cuadrado de un número", "x²", ["2x", "x + 2", "x · 2"]),
             ("un número más %d" % a, "x + %d" % a, ["%dx" % a, "x − %d" % a, "x%s" % sup(a)]), ("un número menos %d" % a, "x − %d" % a, ["%d − x" % a, "x + %d" % a, "−%dx" % a]),
             ("el doble de un número más %d" % a, "2x + %d" % a, ["2(x + %d)" % a, "x² + %d" % a, "2x + %dx" % a]),
             ("el doble de la suma de un número y %d" % a, "2(x + %d)" % a, ["2x + %d" % a, "x + %d · 2" % a, "2 + x + %d" % a]),
             ("el siguiente de un número", "x + 1", ["x − 1", "2x", "x²"]), ("el anterior de un número", "x − 1", ["x + 1", "1 − x", "−x"]),
             ("la suma de dos números consecutivos", "2x + 1", ["x + x", "2x", "x + 2"]), ("un número par cualquiera", "2x", ["x + 2", "x²", "2x + 1"]),
             ("un número impar cualquiera", "2x + 1", ["2x", "x + 1", "x²"]), ("el %d %% de un número" % (a * 10), "0,%dx" % a if a * 10 < 100 else "x", ["%dx" % (a * 10), "x + 0,%d" % a, "x : %d" % (a * 10)]),
             ("la tercera parte de un número menos %d" % a, "x/3 − %d" % a, ["3x − %d" % a, "(x − %d)/3" % a, "x − %d/3" % a]),
             ("el cuadrado de un número menos su doble", "x² − 2x", ["2x − x²", "(x − 2)²", "x² − x²"])]
    k, ok, w = R.choice(items)
    return M("Escribe en lenguaje algebraico: «%s»." % k, ok, w, "Llamamos x al número: <b>%s</b>." % ok)


def s_valor():
    x = nz(R, -6, 6)
    a, b, c = nz(R, -5, 5), nz(R, -9, 9), R.randint(2, 5)
    t = R.choice(["lin", "cuad", "dos"])
    if t == "lin":
        r = a * x + b
        return M("Calcula el valor numérico de %s para x = %s." % (E((a, "x"), (b, "")), sg(x)), sg(r), [sg(a + x + b), sg(-r) if r else "1", sg(a * x - b)], "%s · %s %s %d = <b>%s</b>." % (sg(a), par(x), "+" if b > 0 else "−", abs(b), sg(r)))
    if t == "cuad":
        r = x * x + b * x
        return M("Calcula el valor numérico de %s para x = %s." % (E((1, "x²"), (b, "x")), sg(x)), sg(r), [sg(-x * x + b * x), sg(2 * x + b * x), sg(r + 1)], "%s² %s %d · %s = %d %s %d = <b>%s</b>." % (par(x), "+" if b > 0 else "−", abs(b), par(x), x * x, "+" if b * x >= 0 else "−", abs(b * x), sg(r)))
    y = nz(R, -5, 5)
    r = a * x + c * y
    return M("Calcula el valor numérico de %s para x = %s e y = %s." % (E((a, "x"), (c, "y")), sg(x), sg(y)), sg(r), [sg(a * y + c * x) if a * y + c * x != r else sg(r + 2), sg(a + x + c + y), sg(-r) if r else "1"], "Sustituimos: <b>%s</b>." % sg(r))


def s_monomio():
    a = nz(R, -12, 12)
    ex = {"x": R.randint(1, 4)}
    if R.random() < 0.5:
        ex["y"] = R.randint(1, 3)
    lit = "".join(v + sup(e) for v, e in sorted(ex.items()))
    g = sum(ex.values())
    mono = E((a, lit))
    t = R.choice(["coef", "grado", "parte", "seme"])
    if t == "coef":
        return M("¿Cuál es el coeficiente del monomio %s?" % mono, sg(a), [sg(-a), str(g), lit], "El coeficiente es el número: <b>%s</b>." % sg(a))
    if t == "grado":
        return M("¿Cuál es el grado del monomio %s?" % mono, str(g), [str(abs(a)), str(max(ex.values())), str(g + 1)] if abs(a) != g else [str(g + 2), str(max(ex.values())) if max(ex.values()) != g else str(g - 1), str(g + 1)],
                 "El grado es la suma de los exponentes de las letras: <b>%d</b>." % g)
    if t == "parte":
        return M("¿Cuál es la parte literal del monomio %s?" % mono, lit, [sg(a), lit.replace("x", "y") if "y" not in lit else lit.replace("y", "z"), "x" if lit != "x" else "x²"], "Son las letras con sus exponentes: <b>%s</b>." % lit)
    b = nz(R, -9, 9)
    ok = E((b, lit))
    w = [E((b, lit + "z")), E((b, "x" + sup(ex["x"] + 1) + ("y" + sup(ex["y"]) if "y" in ex else ""))), E((b, lit.replace("x", "a")))]
    return M("¿Qué monomio es semejante a %s?" % mono, ok, w, "Semejantes: la misma parte literal. <b>%s</b>." % ok)


def s_reducir():
    t = R.choice(["sum", "sum", "par", "par2", "mult"])
    a, b, c, e = nz(R, -9, 9), nz(R, -9, 9), nz(R, -9, 9), nz(R, -9, 9)
    if t == "sum":
        q = E((a, "x"), (c, ""), (b, "x"), (e, ""))
        ok = E((a + b, "x"), (c + e, ""))
        return M("Reduce: %s" % q, ok, [E((a + b + c + e, "x")), E((a - b, "x"), (c + e, "")), E((a + b, "x"), (c - e, ""))], "Sumamos los términos con x y los números por separado: <b>%s</b>." % ok)
    if t == "par":
        k = nz(R, -6, 6)
        ok = E((k * a, "x"), (k * c, ""))
        return M("Quita el paréntesis: %s(%s)" % (sg(k) if k != -1 else "−", E((a, "x"), (c, ""))), ok, [E((k * a, "x"), (c, "")), E((k + a, "x"), (k + c, "")), E((-k * a, "x"), (k * c, ""))], "Multiplicamos %s por cada término: <b>%s</b>." % (sg(k), ok))
    if t == "par2":
        ok = E((a - b, "x"), (c - e, ""))
        return M("Reduce: %s − (%s)" % (E((a, "x"), (c, "")), E((b, "x"), (e, ""))), ok, [E((a - b, "x"), (c + e, "")), E((a + b, "x"), (c + e, "")), E((a - b, "x"), (e - c, ""))], "El signo − cambia el signo de todo el paréntesis: <b>%s</b>." % ok)
    m, n = R.randint(1, 4), R.randint(1, 4)
    ok = E((a * b, "x" + sup(m + n)))
    return M("Multiplica: (%s) · (%s)" % (E((a, "x" + sup(m))), E((b, "x" + sup(n)))), ok, [E((a * b, "x" + sup(m * n))) if m * n != m + n else E((a * b, "x" + sup(m + n + 1))), E((a + b, "x" + sup(m + n))), E((a * b, "x"))],
             "Multiplicamos coeficientes y sumamos exponentes: <b>%s</b>." % ok)


def s_problema():
    p, q = K.two()
    t = R.choice(["edad", "perim", "precio", "rect", "dinero"])
    a = R.randint(2, 9)
    if t == "edad":
        return M("%s tiene x años. %s tiene %d años más que %s. ¿Cuántos años tendrá %s dentro de 5 años?" % (p[0], q[0], a, p[0], q[0]), "x + %d" % (a + 5), ["x + %d" % a, "%dx + 5" % a, "x + 5", "x − %d" % (a + 5)], "x + %d + 5 = <b>x + %d</b>." % (a, a + 5))
    if t == "perim":
        return M("Un rectángulo mide x cm de ancho y %d cm más de largo. ¿Cuál es su perímetro?" % a, "4x + %d" % (2 * a), ["2x + %d" % a, "x(x + %d)" % a, "4x + %d" % a], "2 · x + 2 · (x + %d) = <b>4x + %d</b>." % (a, 2 * a))
    if t == "rect":
        return M("Un cuadrado tiene lado x cm. ¿Qué expresión da su área?", "x²", ["4x", "2x", "x + 4"], "Lado por lado: <b>x²</b>.") if a == 2 else \
            M("Un rectángulo mide x cm de ancho y %d veces x de largo. ¿Qué expresión da su área?" % a, "%dx²" % a, ["%dx" % (2 * a + 2), "%dx" % a, "x + %dx" % a], "x · %dx = <b>%dx²</b>." % (a, a))
    if t == "precio":
        b = R.randint(2, 6)
        return M("Un bolígrafo cuesta x € y un cuaderno cuesta %d € más. ¿Cuánto cuestan %d bolígrafos y un cuaderno?" % (a, b), "%dx + %d" % (b + 1, a), ["%dx + %d" % (b, a), "%dx" % (b + a), "x + %d" % (b + a)], "%dx + (x + %d) = <b>%dx + %d</b>." % (b, a, b + 1, a))
    b = R.randint(2, 9)
    return M("%s tiene x €. Gasta %d € y después le dan el doble de lo que le queda. ¿Cuánto dinero tiene ahora?" % (p[0], b), "3x − %d" % (3 * b), ["2x − %d" % b, "x − %d" % b, "3x − %d" % b],
             "Le quedan x − %d; recibe 2(x − %d); total 3(x − %d) = <b>3x − %d</b>." % (b, b, b, 3 * b))


seen = set()
sets = [("Traducir al lenguaje algebraico", mix(R, seen, [(s_traducir, 16), (s_problema, 4)])), ("Valor numérico", mix(R, seen, [(s_valor, 20)])),
        ("Monomios", mix(R, seen, [(s_monomio, 20)])), ("Reducir y quitar paréntesis", mix(R, seen, [(s_reducir, 20)])), ("Expresiones en problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["El <b>lenguaje algebraico</b> usa letras para números desconocidos: «el doble de un número» es 2x.",
          "El <b>valor numérico</b> se obtiene sustituyendo la letra por un número.",
          "Un <b>monomio</b> tiene coeficiente (número) y parte literal (letras). Solo se pueden sumar los monomios <b>semejantes</b>: 3x + 5x = 8x, pero 3x + 5 no se puede juntar."],
         [("Valor de 3x − 2 para x = −4", ["3 · (−4) − 2", "−12 − 2"], "−14"), ("2(3x − 1) − (x + 4)", ["6x − 2 − x − 4"], "5x − 6")],
         [["Escribir x² por «el doble»", "El doble es 2x; el cuadrado es x²."], ["Sumar términos no semejantes", "2x + 3 no es 5x."], ["Multiplicar solo el primer término del paréntesis", "3(x + 2) = 3x + 6."]])
faq = [("¿Qué son monomios semejantes?", "Monomios con la misma parte literal, como 4x² y −7x². Se pueden sumar sumando sus coeficientes."),
       ("¿Cómo se calcula el grado de un monomio?", "Sumando los exponentes de todas sus letras: 5x²y³ tiene grado 5.")]
unit(1, R, "lenguaje-algebraico", "A", "Lenguaje algebraico: traducción de enunciados, valor numérico, monomios y operaciones con expresiones algebraicas sencillas",
     "Lenguaje algebraico y monomios", "Lenguaje algebraico",
     "Fichas de matemáticas de 1.º de ESO: traducir al lenguaje algebraico, valor numérico, monomios, reducir términos y quitar paréntesis. 100 ejercicios con soluciones.",
     "Solo se suman monomios semejantes", "3x + 5x = 8x, pero 3x + 5 se queda igual.", body, faq, sets, 7)
