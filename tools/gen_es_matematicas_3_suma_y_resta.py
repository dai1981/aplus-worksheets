# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º, 2.º y 3.º de Primaria: Suma y resta (Sentido numérico)
build(lv): lv = 1 → sumas y restas hasta 20 con dibujos; lv = 2 → hasta 999 en vertical con llevadas; lv = 3 → hasta 9999.
Términos (sumandos, suma, minuendo, sustraendo, diferencia), el número que falta, la prueba de la resta, propiedades.
Errores: olvidar la llevada, restar la cifra pequeña de la grande, contar el número de partida al sumar con los dedos.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, vertical
import es_pics as P

R = None
LV = 3
TOP = {1: 20, 2: 999, 3: 9999}


def sin_llevar(a, b):
    x, y = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str((int(p) + int(q)) % 10) for p, q in zip(x.rjust(len(y), "0"), y)))


def pequena(a, b):
    x, y = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(p) - int(q))) for p, q in zip(x, y)))


def s1_dibujos():
    if LV > 1:
        return None
    k = R.choice(["suma", "resta", "marco", "dados"])
    kind = R.choice(P.KINDS)
    if k == "suma":
        a, b = R.randint(1, 9), R.randint(1, 9)
        return mcq(P.dos_grupos(a, kind, b) + "¿Cuántos hay en total? %d + %d = ___" % (a, b), str(a + b), [str(a + b + 1), str(a + b - 1), str(abs(a - b)) if a != b else str(a + b + 2)], "%d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "resta":
        n, t = R.randint(5, 15), R.randint(1, 8)
        if t >= n:
            return None
        return mcq(P.tachados(n, kind, t) + "Hay %s y tachamos %d. ¿Cuántos quedan? %d − %d = ___" % (P.cosas(kind, n), t, n, t), str(n - t), [str(n + t), str(n - t + 1), str(n - t - 1) if n - t > 1 else str(n)], "%d − %d = <b>%d</b>." % (n, t, n - t))
    if k == "marco":
        n = R.randint(1, 9)
        return mcq(P.marco10(n) + "¿Cuántos puntos faltan para llegar a 10?", str(10 - n), [str(n), str(10 - n + 1), str(10 - n - 1) if 10 - n > 1 else str(3)], "%d + %d = 10: faltan <b>%d</b>." % (n, 10 - n, 10 - n))
    a, b = R.randint(1, 6), R.randint(1, 6)
    return mcq(P.dados([a, b]) + "¿Cuántos puntos hay entre los dos dados?", str(a + b), [str(a + b + 1), str(a + b - 1), str(a * b) if a * b != a + b else str(a + b + 2)], "%d + %d = <b>%d</b>." % (a, b, a + b))


def s2_calcular():
    if LV == 1:
        k = R.choice(["+", "-", "+10", "-10"])
        a = R.randint(2, 10)
        b = R.randint(1, 10)
        if k == "+":
            if a + b > 20:
                return None
            return mcq("Calcula: %d + %d" % (a, b), str(a + b), [str(a + b + 1), str(a + b - 1), str(abs(a - b)) if a != b else str(a + b + 2)], "<b>%d</b>." % (a + b))
        if k == "-":
            n = R.randint(8, 20)
            b = R.randint(2, min(10, n - 1))
            return mcq("Calcula: %d − %d" % (n, b), str(n - b), [str(n + b) if n + b <= 30 else str(n - b + 2), str(n - b + 1), str(n - b - 1)], "<b>%d</b>." % (n - b))
        if k == "+10":
            return mcq("Calcula: 10 + %d" % b, str(10 + b), [str(b), str(11 + b), str(9 + b)], "Una decena y %d unidades: <b>%d</b>." % (b, 10 + b)) if b < 10 else None
        return mcq("Calcula: %d − 10" % (10 + b), str(b), [str(10 + b), str(b + 1), str(b - 1) if b > 1 else str(2)], "<b>%d</b>." % b) if b < 10 else None
    k = R.choice(["+", "+", "-", "-"])
    lo = 10 ** (LV - 1) * 2
    if k == "+":
        a = R.randint(lo, TOP[LV] // 2)
        b = R.randint(lo // 2, TOP[LV] - a)
        s = a + b
        if s > TOP[LV] or sin_llevar(a, b) == s:
            return None
        return mcq(vertical([str(a), str(b)]) + "Calcula: %s + %s" % (num(a), num(b)), num(s), [num(sin_llevar(a, b)), num(s + 10), num(s - 100) if s > 100 else num(s + 1)], "Sumamos por columnas y nos llevamos cuando pasa de 9: <b>%s</b>." % num(s))
    a = R.randint(lo * 2, TOP[LV])
    b = R.randint(lo // 2, a - 1)
    r = a - b
    if pequena(a, b) == r:
        return None
    return mcq(vertical([str(a), str(b)], op="−") + "Calcula: %s − %s" % (num(a), num(b)), num(r), [num(pequena(a, b)), num(r + 10), num(r - 10) if r > 10 else num(r + 1)], "Si arriba hay una cifra menor, pedimos una a la columna de la izquierda: <b>%s</b>." % num(r))


def s3_falta():
    top = TOP[LV]
    if LV == 1:
        a, b = R.randint(1, 10), R.randint(1, 10)
    else:
        a, b = R.randint(10 ** (LV - 1), top // 2), R.randint(10 ** (LV - 1), top // 2)
    k = R.choice(["s1", "s2", "r1", "r2"])
    if k == "s1":
        return mcq("¿Qué número falta? %s + ___ = %s" % (num(a), num(a + b)), num(b), [num(a + b + a) if a + b + a <= top * 2 else num(b + 10), num(b + 1), num(b - 1) if b > 1 else num(b + 2)], "%s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    if k == "s2":
        return mcq("¿Qué número falta? ___ + %s = %s" % (num(b), num(a + b)), num(a), [num(a + 2 * b), num(a + 1), num(a - 1) if a > 1 else num(a + 2)], "%s − %s = <b>%s</b>." % (num(a + b), num(b), num(a)))
    if k == "r1":
        return mcq("¿Qué número falta? %s − ___ = %s" % (num(a + b), num(a)), num(b), [num(2 * a + b), num(b + 1), num(b - 1) if b > 1 else num(b + 2)], "%s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    return mcq("¿Qué número falta? ___ − %s = %s" % (num(b), num(a)), num(a + b), [num(abs(a - b)) if a != b else num(a + b + 1), num(a + b + 1), num(a + b - 1)], "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def s4_terminos():
    if LV == 1:
        q, a, w = R.choice([("Si 8 + 5 = 13, ¿cuánto es 5 + 8?", "13", ["3", "12", "85"]), ("Si 12 − 4 = 8, ¿cuánto es 8 + 4?", "12", ["4", "8", "16"]), ("¿Cuánto es 7 + 0?", "7", ["0", "70", "8"]),
                            ("¿Qué suma da 10?", "6 + 4", ["5 + 4", "6 + 3", "7 + 4"]), ("¿Qué resta da 5?", "12 − 7", ["12 − 6", "10 − 6", "9 − 3"]), ("¿Cuál es el doble de 6?", "12", ["8", "3", "66"]),
                            ("¿Cuánto es 9 + 9?", "18", ["17", "19", "99"]), ("¿Qué suma da 15?", "8 + 7", ["8 + 6", "9 + 7", "7 + 7"])])
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    a = R.randint(10 ** (LV - 1), TOP[LV] // 2)
    b = R.randint(10 ** (LV - 1), a)
    k = R.choice(["minuendo", "sustraendo", "diferencia", "prueba", "conm"])
    if k == "conm":
        return mcq("Si %s + %s = %s, ¿cuánto es %s + %s?" % (num(a), num(b), num(a + b), num(b), num(a)), num(a + b), [num(a - b), num(a + b + 1), num(b)], "El orden de los sumandos no cambia la suma: <b>%s</b>." % num(a + b))
    if k == "prueba":
        ok = R.random() < 0.5
        r = a - b if ok else a - b + R.choice([10, 1, 100 if LV == 3 else 10])
        return mcq("Hugo dice que %s − %s = %s. Prueba: %s + %s = %s. ¿Está bien?" % (num(a), num(b), num(r), num(r), num(b), num(r + b)), "sí" if ok else "no", ["no" if ok else "sí", "solo si es par", "no se puede saber"],
                   "La diferencia más el sustraendo debe dar el minuendo (%s): <b>%s</b>." % (num(a), "sí" if ok else "no"))
    w = {"minuendo": num(a), "sustraendo": num(b), "diferencia": num(a - b)}[k]
    return mcq("En %s − %s = %s, ¿cuál es el %s?" % (num(a), num(b), num(a - b), k), w, [x for x in (num(a), num(b), num(a - b)) if x != w] + [num(a + b)], "Minuendo − sustraendo = diferencia: el %s es <b>%s</b>." % (k, w))


def s5_problema():
    nombres = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo", "Alba", "Mario"]
    p = R.choice(nombres)
    k = R.choice(["junta", "quita", "mas", "falta"])
    if LV == 1:
        a, b = R.randint(3, 10), R.randint(2, 9)
    else:
        a, b = R.randint(10 ** (LV - 1) * 2, TOP[LV] // 2), R.randint(10 ** (LV - 1), TOP[LV] // 3)
    if k == "junta":
        thing = R.choice(["cromos", "canicas", "pegatinas", "cuentos"]) if LV == 1 else R.choice(["cromos", "puntos", "libros", "personas"])
        return mcq("%s tiene %s %s y le regalan %s. ¿Cuántos tiene ahora?" % (p, num(a), thing, num(b)) if thing != "personas" else "En un teatro hay %s personas y entran %s más. ¿Cuántas personas hay ahora?" % (num(a), num(b)),
                   num(a + b), [num(abs(a - b)), num(a + b + 1), num(a + b - 10) if a + b > 10 else num(a + b + 2)], "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "quita":
        a, b = max(a, b) + b, b
        return mcq("En un árbol hay %s pájaros y se van volando %s. ¿Cuántos quedan?" % (num(a), num(b)) if LV == 1 else "Una tienda tenía %s botellas de agua y vende %s. ¿Cuántas le quedan?" % (num(a), num(b)),
                   num(a - b), [num(a + b), num(a - b + 1), num(a - b - 1)], "%s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    if k == "mas":
        return mcq("%s tiene %s caramelos y su hermano tiene %s más. ¿Cuántos tiene su hermano?" % (p, num(a), num(b)),
                   num(a + b), [num(a - b) if a > b else num(a + b + 2), num(b), num(a + b + 1)], "Tiene %s más: %s + %s = <b>%s</b>." % (num(b), num(a), num(b), num(a + b)))
    hi, lo = max(a, b) + 1, min(a, b)
    return mcq("Un libro tiene %s páginas y %s ha leído %s. ¿Cuántas le faltan por leer?" % (num(hi), p, num(lo)), num(hi - lo), [num(hi + lo), num(hi - lo + 1), num(lo)], "%s − %s = <b>%s</b>." % (num(hi), num(lo), num(hi - lo)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30003 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("Sumar y restar con dibujos", mix(R, seen, [(s1_dibujos, 20)])), ("Sumas y restas hasta 20", mix(R, seen, [(s2_calcular, 20)])),
                ("El número que falta", mix(R, seen, [(s3_falta, 20)])), ("Sumas que dan lo mismo", mix(R, seen, [(s4_terminos, 8), (s2_calcular, 12)])), ("Problemas", mix(R, seen, [(s5_problema, 20)]))]
    else:
        sets = [("Sumas en vertical", mix(R, seen, [(s2_calcular, 20)])), ("Restas en vertical", mix(R, seen, [(s2_calcular, 20)])),
                ("El número que falta", mix(R, seen, [(s3_falta, 20)])), ("Términos y prueba de la resta", mix(R, seen, [(s4_terminos, 20)])), ("Problemas", mix(R, seen, [(s5_problema, 20)]))]
    if lv == 1:
        think = ["<b>Sumar</b> es juntar: 5 + 3 = 8. <b>Restar</b> es quitar: 8 − 3 = 5.", "Para sumar, empieza por el número mayor y cuenta hacia delante. Para restar, cuenta hacia atrás.", "Con 10 + 4 = 14, una decena y 4 unidades."]
        ex = [("7 + 5", ["7 + 3 = 10", "10 + 2 = 12"], "12"), ("14 − 6", ["14 − 4 = 10", "10 − 2 = 8"], "8")]
        mist = [["Contar el número de partida", "7 + 3: di 8, 9, 10 (no empieces en 7)."], ["Sumar cuando hay que quitar", "«Se van», «quedan» → restar."], ["Olvidar que el orden no importa al sumar", "3 + 9 = 9 + 3 = 12."]]
        pic = P.dos_grupos(5, "apple", 3)
    else:
        think = ["Coloca los números en columnas: unidades debajo de unidades, decenas debajo de decenas…", "En la suma, si una columna pasa de 9, escribe las unidades y <b>llévate</b> 1 a la siguiente.",
                 "En la resta, si la cifra de arriba es menor, pide <b>una</b> a la columna de la izquierda.", "<b>Prueba de la resta</b>: diferencia + sustraendo = minuendo."]
        if lv == 2:
            ex = [("367 + 258", ["Unidades: 7 + 8 = 15, escribo 5 y me llevo 1", "Decenas: 6 + 5 + 1 = 12, escribo 2 y me llevo 1", "Centenas: 3 + 2 + 1 = 6"], "625"),
                  ("503 − 178", ["Unidades: 3 es menor que 8, pido una: 13 − 8 = 5", "Decenas: ahora hay 9: 9 − 7 = 2", "Centenas: ahora hay 4: 4 − 1 = 3"], "325")]
        else:
            ex = [("4567 + 2385", ["Unidades: 7 + 5 = 12, me llevo 1", "Decenas: 6 + 8 + 1 = 15, me llevo 1", "Centenas: 5 + 3 + 1 = 9", "Millares: 4 + 2 = 6"], "6952"),
                  ("5003 − 1278", ["Unidades: 13 − 8 = 5", "Decenas: 9 − 7 = 2", "Centenas: 9 − 2 = 7", "Millares: 4 − 1 = 3"], "3725")]
        mist = [["Olvidar la llevada", "Escribe la llevada encima de la columna siguiente."], ["Restar la cifra pequeña de la grande", "En 52 − 18 no hagas 8 − 2: 12 − 8 = 4."], ["Descolocar las columnas", "Alinea los números por la derecha."]]
        pic = vertical(["367", "258"], result="625")
    body = lesson(think, ex, mist, pic)
    faq = [("¿Cómo se hace la prueba de la resta?", "Se suma la diferencia y el sustraendo. Si da el minuendo, la resta está bien."),
           ("¿Qué es llevarse una?", "Cuando una columna suma 10 o más, se escriben las unidades y la decena se suma a la columna de la izquierda.")]
    make_unit(R, {1: "sumas-y-restas-hasta-20", 2: "suma-y-resta-con-llevadas", 3: "suma-y-resta"}[lv], "N",
              "Suma y resta de números naturales %s; relación entre suma y resta; resolución de problemas" % {1: "hasta 20", 2: "hasta 999 con y sin llevadas", 3: "hasta 9999 con llevadas"}[lv],
              {1: "Sumas y restas hasta 20", 2: "Suma y resta con llevadas", 3: "Suma y resta"}[lv], {1: "Sumas y restas hasta 20", 2: "Suma y resta", 3: "Suma y resta"}[lv],
              "Fichas de matemáticas de %d.º de Primaria: %s, el número que falta y problemas. 100 ejercicios con soluciones." % (lv, {1: "sumas y restas hasta 20 con dibujos", 2: "sumas y restas en vertical con llevadas hasta 999", 3: "sumas y restas en vertical hasta 9999, prueba de la resta"}[lv]),
              {1: "Sumar es juntar; restar es quitar", 2: "Alinea las cifras por la derecha", 3: "Alinea las cifras por la derecha"}[lv], {1: "Cuenta desde el número mayor.", 2: "Empieza por las unidades.", 3: "Empieza por las unidades."}[lv],
              body, faq, sets, 3, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(3)
