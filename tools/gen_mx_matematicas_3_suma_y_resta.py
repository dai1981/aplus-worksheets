# -*- coding: utf-8 -*-
"""
México 3.er grado de primaria: Suma y resta (Suma y resta, su relación como operaciones inversas — Fase 4)
Sumas de números de hasta tres cifras con agrupamiento, restas con desagrupamiento, el número que falta, la resta como inversa de la suma, problemas.
Errores: olvidar lo que se lleva, restar la cifra menor de la mayor en cada columna, alinear mal las columnas.
"""
import random
from mx_common import mcq, num, unit, mx_text, Kids
import es_common as ES

R = random.Random(63103)
K = Kids(R)


def V(a, b, op):
    return mx_text(ES.vertical([str(a), str(b)], op=op))


def sin_llevar(a, b):
    return int("".join(str((int(x) + int(y)) % 10) for x, y in zip(str(a).rjust(3, "0"), str(b).rjust(3, "0"))))


def resta_mal(a, b):
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a).rjust(3, "0"), str(b).rjust(3, "0"))))


def s_suma():
    a, b = R.randint(105, 899), R.randint(105, 899)
    s = a + b
    if (a % 10 + b % 10) < 10 and (a // 10 % 10 + b // 10 % 10) < 10:
        return None
    return mcq(V(a, b, "+") + "Calcula: %s + %s" % (num(a), num(b)), num(s), [num(sin_llevar(a, b) + (1000 if s >= 1000 else 0)) if sin_llevar(a, b) != s % 1000 else num(s + 10), num(s - 10), num(s + 100), num(s - 1)],
               "Sumamos por columnas, empezando por las unidades, y llevamos 1 cuando pasa de 9: <b>%s</b>." % num(s))


def s_resta():
    a = R.randint(300, 999)
    b = R.randint(102, a - 50)
    d = a - b
    if a % 10 >= b % 10 and a // 10 % 10 >= b // 10 % 10:
        return None
    return mcq(V(a, b, "−") + "Calcula: %s − %s" % (num(a), num(b)), num(d), [num(resta_mal(a, b)) if resta_mal(a, b) != d else num(d + 10), num(d + 10), num(d - 10) if d > 10 else num(d + 100), num(a + b)],
               "Si arriba hay una cifra menor, desagrupamos: cambiamos 1 de la columna de la izquierda por 10. <b>%s</b>." % num(d))


def s_falta():
    t = R.choice(["s1", "s2", "r1", "r2"])
    a, b = R.randint(120, 860), R.randint(110, 860)
    if t == "s1":
        return mcq("¿Qué número falta? %s + ___ = %s" % (num(a), num(a + b)), num(b), [num(2 * a + b), num(b + 10), num(b - 10)], "Restamos: %s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    if t == "s2":
        return mcq("¿Qué número falta? ___ + %s = %s" % (num(b), num(a + b)), num(a), [num(a + 2 * b), num(a + 10), num(a - 10)], "Restamos: %s − %s = <b>%s</b>." % (num(a + b), num(b), num(a)))
    if a <= b:
        a, b = b, a
    if a - b < 20:
        return None
    if t == "r1":
        return mcq("¿Qué número falta? %s − ___ = %s" % (num(a), num(a - b)), num(b), [num(2 * a - b), num(b + 10), num(b - 10)], "%s − %s = <b>%s</b>." % (num(a), num(a - b), num(b)))
    return mcq("¿Qué número falta? ___ − %s = %s" % (num(b), num(a - b)), num(a), [num(a - 2 * b) if a > 2 * b else num(a + 100), num(a + 10), num(a - 10)], "La resta es la inversa de la suma: %s + %s = <b>%s</b>." % (num(a - b), num(b), num(a)))


def s_prueba():
    a = R.randint(300, 999)
    b = R.randint(110, a - 40)
    t = R.choice(["ok", "mal", "op", "op"])
    if t == "op":
        return mcq("¿Con qué suma compruebas que %s − %s = %s?" % (num(a), num(b), num(a - b)), "%s + %s = %s" % (num(a - b), num(b), num(a)),
                   ["%s + %s = %s" % (num(a), num(b), num(a + b)), "%s − %s = %s" % (num(a), num(a - b), num(b)), "%s + %s = %s" % (num(a), num(a - b), num(2 * a - b))],
                   "La diferencia más el número que restaste da el primero: <b>%s + %s = %s</b>." % (num(a - b), num(b), num(a)))
    p, _ = K.next()
    d = a - b if t == "ok" else a - b + R.choice([10, -10, 100, 1])
    ok = "sí" if d == a - b else "no"
    return mcq("%s dice que %s − %s = %s. Comprueba con una suma. ¿Está bien?" % (p, num(a), num(b), num(d)), ok, ["no" if ok == "sí" else "sí", "solo si es par", "no se puede saber"],
               "%s + %s = %s%s: <b>%s</b>." % (num(d), num(b), num(d + b), "" if ok == "sí" else ", no da %s" % num(a), ok))


CTX = [("Un camión lleva %d pasajeros y suben %d más. ¿Cuántos pasajeros van ahora?", "+"), ("En la escuela hay %d niñas y %d niños. ¿Cuántos alumnos hay en total?", "+"),
       ("Una tiendita vendió %d paletas el sábado y %d el domingo. ¿Cuántas vendió en los dos días?", "+"), ("Una biblioteca tiene %d libros y recibe %d más. ¿Cuántos tiene ahora?", "+"),
       ("Un granjero tenía %d mazorcas y vendió %d. ¿Cuántas le quedan?", "−"), ("Una panadería horneó %d conchas y vendió %d. ¿Cuántas sobraron?", "−"),
       ("Un álbum tiene espacio para %d estampas y ya tiene %d. ¿Cuántas faltan para llenarlo?", "−"), ("En un estadio caben %d personas y hay %d. ¿Cuántos lugares quedan libres?", "−")]


def s_problema():
    tpl, op = R.choice(CTX)
    if op == "+":
        a, b = R.randint(120, 690), R.randint(110, 480)
        return mcq(tpl % (a, b), num(a + b), [num(abs(a - b)), num(a + b + 10), num(a + b - 100)], "Juntamos, así que sumamos: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    a = R.randint(300, 990)
    b = R.randint(110, a - 30)
    return mcq(tpl % (a, b), num(a - b), [num(a + b), num(a - b + 10), num(a - b - 10)], "Quitamos o buscamos lo que falta, así que restamos: %s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))


unit("suma-y-resta", 3, "S",
     "Resuelve situaciones que implican sumas de números naturales de hasta tres cifras y restas con agrupamientos y desagrupamientos; reconoce la suma y la resta como operaciones inversas",
     "Suma y resta", "Suma y resta",
     "Ejercicios de matemáticas de 3.er grado de primaria: sumas llevando, restas con desagrupamiento, el número que falta y la comprobación de la resta. 100 ejercicios con respuestas.",
     "Unidades bajo unidades", "Empieza siempre por las unidades.",
     ["Escribe los números en columna: <b>unidades bajo unidades</b>, decenas bajo decenas y centenas bajo centenas.",
      "En la suma, si una columna pasa de 9, escribe las unidades y <b>lleva</b> 1 a la columna siguiente.",
      "En la resta, si arriba hay una cifra menor, <b>desagrupa</b>: cambia 1 decena por 10 unidades (o 1 centena por 10 decenas).",
      "La resta es la operación inversa de la suma: para comprobar 532 − 178 = 354, suma 354 + 178 = 532."],
     [("Calcula 467 + 285", ["7 + 5 = 12: escribo 2 y llevo 1", "6 + 8 + 1 = 15: escribo 5 y llevo 1", "4 + 2 + 1 = 7"], "752"),
      ("Calcula 532 − 178", ["2 − 8 no se puede: desagrupo, 12 − 8 = 4", "2 − 7 no se puede: desagrupo, 12 − 7 = 5", "4 − 1 = 3"], "354")],
     [["Olvidar lo que se lleva", "Escribe el 1 pequeño arriba de la columna siguiente."], ["Restar la cifra menor de la mayor en cada columna", "En 52 − 18, no hagas 8 − 2: desagrupa."], ["Alinear mal las columnas", "Alinea los números por la derecha."]],
     [("¿Qué es desagrupar en una resta?", "Cuando la cifra de arriba es menor, se cambia 1 decena por 10 unidades (o 1 centena por 10 decenas) para poder restar."),
      ("¿Cómo compruebo una resta?", "Suma el resultado y el número que restaste: debe salir el primer número.")],
     [("Sumas llevando", [(s_suma, 20)]), ("Restas con desagrupamiento", [(s_resta, 20)]), ("El número que falta", [(s_falta, 20)]), ("Comprobar con la operación inversa", [(s_prueba, 20)]), ("Problemas", [(s_problema, 20)])],
     63003, pic=V(467, 285, "+"))
