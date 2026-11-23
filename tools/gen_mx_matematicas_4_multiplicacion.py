# -*- coding: utf-8 -*-
"""México 4.º grado: Multiplicación de números de hasta tres cifras por números de hasta dos cifras (Multiplicación y división). Reutiliza España 4.º con otra semilla."""
import random
from mx_common import src, unit, mx_text, mcq, num
import es_common as ES

una, prop, probl = src("gen_es_matematicas_4_multiplicacion", 64206, "s1_una", "s4_prop", "s5_problema", mx_=99999)
R = random.Random(64106)


def dos():
    a = R.randint(100, 999) if R.random() < 0.7 else R.randint(21, 99)
    b = R.randint(12, 99)
    if b % 10 == 0:
        return None
    p = a * b
    t, u = divmod(b, 10)
    return mcq(mx_text(ES.vertical([str(a), str(b)], op="×")) + "Calcula: %s × %d" % (num(a), b), num(p), [num(a * u + a * t), num(a * u + a * t * 100), num(p + a), num(p - 10)],
               "%s × %d = %s; %s × %d = %s (corremos un lugar a la izquierda); %s + %s = <b>%s</b>." % (num(a), u, num(a * u), num(a), t * 10, num(a * t * 10), num(a * u), num(a * t * 10), num(p)))


def ceros():
    k = R.choice(["10", "100", "1000", "dec"])
    if k == "dec":
        a, m = R.randint(12, 99), R.choice([20, 30, 40, 50, 60, 70, 80, 90, 200, 300, 400, 500])
        if a * m > 99999:
            return None
        d = m // (10 if m < 100 else 100)
        z = 1 if m < 100 else 2
        return mcq("Calcula: %d × %s" % (a, num(m)), num(a * m), [num(a * d), num(a * m * 10) if a * m * 10 <= 99999 else num(a * m + m), num(a * m // 10 * (10 if z == 2 else 1) + 1)],
                   "%d × %d = %s y añadimos %s: <b>%s</b>." % (a, d, num(a * d), "un cero" if z == 1 else "dos ceros", num(a * m)))
    m = int(k)
    a = R.randint(12, 99999 // m)
    if a > 999:
        a = a // 10
    z = len(k) - 1
    return mcq("Calcula: %s × %s" % (num(a), num(m)), num(a * m), [num(a * m // 10), num(a + m), num(a * m * 10) if a * m * 10 <= 99999 else num(a * m // 100 if m >= 100 else a * m + 1)],
               "Multiplicar por %s es añadir %d %s a la derecha: <b>%s</b>." % (num(m), z, "cero" if z == 1 else "ceros", num(a * m)))


unit("multiplicacion", 4, "P",
     "Resuelve multiplicaciones de números de hasta tres cifras por números de hasta dos cifras con el algoritmo convencional; multiplica por 10, 100 y 1 000 y por decenas; usa las propiedades; resuelve problemas",
     "Multiplicación", "Multiplicación",
     "Ejercicios de matemáticas de 4.º grado de primaria: multiplicar por una y dos cifras, por 10, 100 y 1 000, propiedades de la multiplicación y problemas. 100 ejercicios con respuestas.",
     "Dos productos parciales y una suma", "El segundo producto se corre un lugar.",
     ["Para multiplicar por una cifra, multiplica cada cifra empezando por las unidades y lleva lo que pase de 9.",
      "Para 324 × 26: primero 324 × 6 = 1 944; después 324 × 20 = 6 480, que se escribe <b>corrido un lugar</b> a la izquierda; al final se suman: 8 424.",
      "Multiplicar por 10, 100 o 1 000 es añadir uno, dos o tres ceros. Para 34 × 20, calcula 34 × 2 = 68 y añade un cero: 680."],
     [("Calcula 324 × 26", ["324 × 6 = 1 944", "324 × 20 = 6 480", "1 944 + 6 480"], "8 424"), ("Calcula 45 × 300", ["45 × 3 = 135", "añado dos ceros"], "13 500")],
     [["No correr el segundo producto", "324 × 2 decenas vale 6 480, no 648."], ["Olvidar lo que se lleva", "Súmalo en la columna siguiente."], ["Poner mal los ceros", "45 × 300 = 13 500."]],
     [("¿Por qué se corre un lugar el segundo producto?", "Porque la cifra de las decenas vale diez veces más: en 324 × 26, el 2 vale 20 y 324 × 20 = 6 480."),
      ("¿Qué es la propiedad distributiva?", "Multiplicar una suma es lo mismo que multiplicar cada sumando y sumar: 7 × (10 + 3) = 70 + 21 = 91.")],
     [("Por una cifra", [(una, 20)]), ("Por dos cifras", [(dos, 20)]), ("Por 10, 100, 1 000 y decenas", [(ceros, 20)]), ("Propiedades", [(prop, 20)]), ("Problemas", [(probl, 20)])],
     64004, pic=mx_text(ES.vertical(["324", "26"], op="×")), lv=4)
