# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Expresiones y ecuaciones (Sentido algebraico)
Patrones y regla de una secuencia (término n), expresiones con letras (el doble de un número: 2 × n), valor de una expresión,
igualdades y ecuaciones sencillas (x + 7 = 15, 3 × x = 24, 2 × x + 5 = 17), plantear ecuaciones a partir de problemas.
Errores: hacer la operación contraria equivocada (x + 7 = 15 → x = 22), leer «el doble más 3» como 2 × (n + 3).
"""
import random
from es_c3 import M, mix, lesson, make_unit, num, POR, DIV

R = None
LV = 6


def s1_serie():
    a, s = R.randint(1, 20), R.randint(2, 9)
    xs = [a + s * i for i in range(5)]
    k = R.choice(["sig", "n", "regla"] if LV == 6 else ["sig", "regla"])
    if k == "sig":
        return M("¿Qué número sigue? %s, …" % ", ".join(map(str, xs)), str(xs[-1] + s), [str(xs[-1] + s + 1), str(xs[-1] + 2 * s), str(xs[-1] * 2)], "Cada término suma %d: <b>%d</b>." % (s, xs[-1] + s))
    if k == "n":
        n = R.choice([10, 15, 20, 30, 50])
        v = a + s * (n - 1)
        return M("Serie: %s, … ¿Qué número ocupa el lugar %d?" % (", ".join(map(str, xs)), n), str(v), [str(a + s * n), str(s * n), str(v + 1), str(a * n)],
                 "Al primero (%d) se le suma %d veces %d: %d + %d × %d = <b>%d</b>." % (a, n - 1, s, a, n - 1, s, v))
    ok = "sumar %d" % s
    return M("¿Cuál es la regla de la serie %s, …?" % ", ".join(map(str, xs)), ok, ["sumar %d" % (s + 1), "multiplicar por %d" % s, "sumar %d" % a if a != s else "restar %d" % s], "Cada término es el anterior más %d: <b>%s</b>." % (s, ok))


def s2_expresion():
    k = R.choice(["leer", "valor", "valor2"])
    n = R.randint(2, 15)
    a = R.randint(2, 9)
    if k == "leer":
        cases = [("el doble de un número n", "2 %s n" % POR, ["n + 2", "n %s 2" % DIV, "n %s n" % POR]),
                 ("el triple de un número n más 5", "3 %s n + 5" % POR, ["3 %s (n + 5)" % POR, "3 + n + 5", "n + 3 %s 5" % POR]),
                 ("la mitad de un número n", "n %s 2" % DIV, ["2 %s n" % POR, "n − 2", "2 %s n" % DIV]),
                 ("un número n menos 4", "n − 4", ["4 − n", "4 %s n" % POR, "n + 4"]),
                 ("el doble de la suma de un número n y 3", "2 %s (n + 3)" % POR, ["2 %s n + 3" % POR, "2 + n + 3", "n + 2 %s 3" % POR]),
                 ("el número siguiente a n", "n + 1", ["n − 1", "2 %s n" % POR, "n %s 1" % POR]),
                 ("la edad de Lucía dentro de 5 años, si ahora tiene n años", "n + 5", ["n − 5", "5 %s n" % POR, "n %s 5" % DIV]),
                 ("el precio de n cuadernos de 3 €", "3 %s n" % POR, ["n + 3", "n %s 3" % DIV, "3 − n"])]
        t, ok, w = R.choice(cases)
        return M("¿Qué expresión significa «%s»?" % t, ok, w, "<b>%s</b>." % ok)
    if k == "valor":
        e = R.choice(["%d %s n + %d" % (a, POR, a + 1), "%d %s n − %d" % (a, POR, a - 1), "n %s n" % POR, "%d %s (n + %d)" % (a, POR, a)])
        v = eval(e.replace(POR, "*").replace("−", "-").replace("n", str(n)))
        return M("Calcula el valor de %s cuando n = %d." % (e, n), num(v), [num(v + a), num(v - 1), num(eval(e.replace(POR, "+").replace("−", "-").replace("n", str(n)))), num(v * 2)],
                 "Sustituimos n por %d: <b>%s</b>." % (n, num(v)))
    p = R.randint(2, 8)
    return M("Un taxi cobra 3 € al subir y %d € por kilómetro. ¿Qué expresión da el precio de un viaje de k kilómetros?" % p, "3 + %d %s k" % (p, POR), ["(3 + %d) %s k" % (p, POR), "3 %s %d + k" % (POR, p), "3 + %d + k" % p],
             "Fijo 3 € más %d € por cada kilómetro: <b>3 + %d %s k</b>." % (p, p, POR))


def s3_ecuacion():
    x = R.randint(2, 30)
    a = R.randint(2, 15)
    k = R.choice(["+", "-", "×", ":"] + (["ax+b", "ax-b"] if LV == 6 else []))
    if k == "+":
        e, w = "x + %d = %d" % (a, x + a), x + 2 * a
    elif k == "-":
        e, w = "x − %d = %d" % (a, x), x - a if x > a else x + 2 * a + 1
        x, e = x + a, "x − %d = %d" % (a, x)
        w = x - 2 * a if x > 2 * a else x + a
    elif k == "×":
        a = R.randint(2, 9)
        e, w = "%d %s x = %d" % (a, POR, a * x), a * x - a
    elif k == ":":
        a = R.randint(2, 9)
        x2 = x
        x = x2 * a
        e, w = "x %s %d = %d" % (DIV, a, x2), x2 // a if x2 % a == 0 and x2 // a != x else x2 + a
    elif k == "ax+b":
        a = R.randint(2, 6)
        b = R.randint(1, 20)
        e, w = "%d %s x + %d = %d" % (a, POR, b, a * x + b), (a * x + b + b) // a if (a * x + 2 * b) % a == 0 else a * x
    else:
        a = R.randint(2, 6)
        b = R.randint(1, 20)
        e, w = "%d %s x − %d = %d" % (a, POR, b, a * x - b), (a * x - 2 * b) // a if a * x - 2 * b > 0 and (a * x - 2 * b) % a == 0 else a * x
    if w == x:
        w = x + 3
    return M("Resuelve: %s" % e, "x = %d" % x, ["x = %d" % w, "x = %d" % (x + 1), "x = %d" % (x - 1)], "Hacemos la operación contraria: <b>x = %d</b>. Comprobación: sustituye x en la ecuación." % x)


def s4_balanza():
    k = R.choice(["peso", "hueco", "verdad"])
    if k == "peso":
        n = R.randint(2, 5)
        p = R.randint(2, 9)
        extra = R.randint(1, 9)
        return M("En una balanza equilibrada hay %d cajas iguales y una pesa de %d kg en un plato, y %d kg en el otro. ¿Cuánto pesa cada caja?" % (n, extra, n * p + extra), "%d kg" % p, ["%d kg" % ((n * p + extra) // n), "%d kg" % (n * p), "%d kg" % (p + extra)] if (n * p + extra) // n != p else ["%d kg" % (p + 1), "%d kg" % (n * p), "%d kg" % (p + extra)],
                 "%d %s c + %d = %d → %d %s c = %d → <b>c = %d kg</b>." % (n, POR, extra, n * p + extra, n, POR, n * p, p))
    if k == "hueco":
        a, b, c = R.randint(5, 50), R.randint(5, 50), R.randint(2, 40)
        if a + b - c <= 0:
            return None
        return M("¿Qué número hace verdadera la igualdad %d + %d = %d + ___?" % (a, b, c), str(a + b - c), [str(a + b), str(a + b + c), str(a + b - c + 1)], "%d + %d = %d; %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b - c))
    a, b = R.randint(2, 9), R.randint(2, 9)
    c = R.randint(1, a * b - 1)
    ok = R.random() < 0.5
    rhs = a * b - c if ok else a * b - c + R.choice([1, 2, -1])
    return M("¿Es verdadera la igualdad %d %s %d = %d + %d?" % (a, POR, b, c, rhs), "sí" if ok else "no", ["no" if ok else "sí", "solo si se cambia el orden", "no se puede saber"],
             "%d %s %d = %d y %d + %d = %d: <b>%s</b>." % (a, POR, b, a * b, c, rhs, c + rhs, "sí" if ok else "no"))


def s5_problema():
    k = R.choice(["piensa", "edad", "compra", "reparto", "piensa2"])
    if k == "piensa":
        x, a = R.randint(5, 60), R.randint(5, 40)
        return M("Pienso un número, le sumo %d y obtengo %d. ¿Qué ecuación lo representa y cuál es el número?" % (a, x + a), "x + %d = %d; x = %d" % (a, x + a, x), ["x + %d = %d; x = %d" % (a, x + a, x + 2 * a), "x − %d = %d; x = %d" % (a, x + a, x + 2 * a), "%d %s x = %d; x = %d" % (a, POR, x + a, x)],
                 "x + %d = %d → x = %d − %d = <b>%d</b>." % (a, x + a, x + a, a, x))
    if k == "piensa2":
        x, a, b = R.randint(2, 15), R.randint(2, 6), R.randint(1, 15)
        return M("Pienso un número, lo multiplico por %d y le sumo %d. Obtengo %d. ¿Qué número pensé?" % (a, b, a * x + b), str(x), [str((a * x + b) // a), str(a * x + b - b // a), str(x + b)] if (a * x + b) // a != x else [str(x + 1), str(a * x), str(x + b)],
                 "%d %s x + %d = %d → %d %s x = %d → <b>x = %d</b>." % (a, POR, b, a * x + b, a, POR, a * x, x))
    if k == "edad":
        x, d_ = R.randint(8, 12), R.randint(24, 32)
        return M("La madre de Hugo tiene %d años más que él. Entre los dos suman %d años. ¿Cuántos años tiene Hugo?" % (d_, 2 * x + d_), "%d años" % x, ["%d años" % (x + d_), "%d años" % ((2 * x + d_) // 2), "%d años" % (2 * x + d_ - d_)],
                 "x + x + %d = %d → 2 %s x = %d → <b>x = %d</b>." % (d_, 2 * x + d_, POR, 2 * x, x))
    if k == "compra":
        n, p, t = R.randint(2, 6), R.randint(2, 9), R.randint(1, 9)
        return M("Compro %d cuadernos iguales y una regla de %d €. Pago %d € en total. ¿Cuánto cuesta cada cuaderno?" % (n, t, n * p + t), "%d €" % p, ["%d €" % ((n * p + t) // n) if (n * p + t) // n != p else "%d €" % (p + 1), "%d €" % (n * p), "%d €" % (p + t)],
                 "%d %s c + %d = %d → %d %s c = %d → <b>c = %d €</b>." % (n, POR, t, n * p + t, n, POR, n * p, p))
    n, x = R.randint(3, 8), R.randint(4, 20)
    return M("Repartimos unos cromos entre %d amigos y cada uno recibe %d. ¿Cuántos cromos había? (x : %d = %d)" % (n, x, n, x), str(n * x), [str(x // n) if x // n else str(x + n), str(x + n), str(x)], "x = %d %s %d = <b>%d</b>." % (x, POR, n, n * x))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40012 + lv * 1000)
    seen = set()
    sets = [
        ("Series y regularidades", mix(R, seen, [(s1_serie, 20)])),
        ("Expresiones con letras", mix(R, seen, [(s2_expresion, 20)])),
        ("Igualdades y balanzas", mix(R, seen, [(s4_balanza, 20)])),
        ("Resolver ecuaciones", mix(R, seen, [(s3_ecuacion, 20)])),
        ("Problemas con ecuaciones", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Usamos <b>letras</b> para representar un número desconocido: «el doble de un número» = 2 × n.",
         "Una <b>ecuación</b> es una igualdad con un número desconocido. Resolverla es encontrar ese número.",
         "Para resolver, haz la <b>operación contraria</b>: si x + 7 = 15, x = 15 − 7 = 8. Si 3 × x = 24, x = 24 : 3 = 8. Comprueba siempre sustituyendo."],
        [("x + 9 = 23", ["Restamos 9: 23 − 9"], "x = 14"),
         ("2 × x + 5 = 17", ["Restamos 5: 2 × x = 12", "Dividimos entre 2"], "x = 6")],
        [["Hacer la operación equivocada", "x + 7 = 15 → x = 15 − 7, no 15 + 7."],
         ["Leer mal la expresión", "«El doble de n más 3» es 2 × n + 3, no 2 × (n + 3)."],
         ["No comprobar", "Sustituye el resultado en la ecuación para ver si se cumple."]])
    faq = [("¿Cómo se resuelve una ecuación sencilla?", "Se deja sola la letra haciendo la operación contraria: si suma, se resta; si multiplica, se divide. Después se comprueba sustituyendo."),
           ("¿Para qué sirven las letras en matemáticas?", "Para representar números que no conocemos o que pueden cambiar, y escribir reglas generales como «precio = 3 × n».")]
    make_unit(R, "expresiones-y-ecuaciones", "A",
              "Patrones y regularidades; expresiones con letras; relaciones de igualdad; ecuaciones sencillas con una incógnita; resolución de problemas mediante ecuaciones",
              "Expresiones y ecuaciones", "Expresiones y ecuaciones",
              "Fichas de matemáticas de %d.º de Primaria: series, expresiones con letras, igualdades, balanzas, ecuaciones sencillas y problemas con ecuaciones. 100 ejercicios con soluciones." % lv,
              "Haz la operación contraria", "x + 7 = 15 → x = 15 − 7 = 8.",
              body, faq, sets, 12, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
