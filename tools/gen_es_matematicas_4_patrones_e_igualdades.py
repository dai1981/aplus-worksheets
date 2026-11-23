# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Patrones e igualdades (Sentido algebraico)
Series numéricas (sumar, restar, multiplicar), encontrar la regla y el término que falta, patrones con figuras,
el signo igual como equilibrio, igualdades con un hueco (12 + ___ = 20 − 3), igualdades verdaderas o falsas, tablas de entrada y salida.
Errores: pensar que el signo = significa «escribe el resultado» (12 + 8 = 20 + 5 = 25), mirar solo los dos primeros números de la serie.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, DIV, bank

R = random.Random(44023)
SH = {"c": "<circle cx='%d' cy='20' r='12' fill='#1f5fbf'/>", "t": "<polygon points='%d,8 %d,32 %d,32' fill='#c0392b'/>", "s": "<rect x='%d' y='8' width='24' height='24' fill='#2e7d32'/>"}
NOMBRE = {"c": "círculo azul", "t": "triángulo rojo", "s": "cuadrado verde"}


def dibuja(seq):
    s = []
    for i, k in enumerate(seq):
        x = 10 + i * 34
        if k == "?":
            s.append("<text x='%d' y='28' font-size='20' font-weight='700' fill='#333'>?</text>" % (x + 6))
        elif k == "c":
            s.append(SH["c"] % (x + 12))
        elif k == "t":
            s.append(SH["t"] % (x + 12, x, x + 24))
        else:
            s.append(SH["s"] % x)
    W = 20 + len(seq) * 34
    return "<div class='fig'><svg viewBox='0 0 %d 40' width='%d' role='img' aria-label='serie de figuras'>%s</svg></div>" % (W, W, "".join(s))


def s1_series():
    k = R.choice(["+", "+", "-", "x", "+big"])
    if k == "+":
        a, d = R.randint(1, 200), R.choice([3, 4, 6, 7, 8, 9, 11, 12, 15, 25, 50])
        xs = [a + i * d for i in range(6)]
        rule = "suma %d" % d
    elif k == "+big":
        a, d = R.randint(10, 900) * 100, R.choice([1000, 2500, 5000, 10000, 500])
        xs = [a + i * d for i in range(6)]
        rule = "suma %s" % num(d)
    elif k == "-":
        d = R.choice([3, 4, 6, 7, 8, 9, 11, 12, 25, 50, 100])
        a = d * 6 + R.randint(0, 300)
        xs = [a - i * d for i in range(6)]
        rule = "resta %d" % d
    else:
        a, m = R.choice([1, 2, 3, 5]), R.choice([2, 3])
        xs = [a * m ** i for i in range(6)]
        rule = "multiplica por %d" % m
    pos = R.choice([3, 4, 5])
    shown = [num(x) if i != pos else "___" for i, x in enumerate(xs[:pos + 1])] if pos < 5 else [num(x) for x in xs[:5]] + ["___"]
    if pos < 5:
        shown = [num(x) if i != pos else "___" for i, x in enumerate(xs)]
    ans = xs[pos]
    d1 = xs[1] - xs[0]
    return mcq("¿Qué número falta en la serie? %s" % ", ".join(shown), num(ans), [num(ans + d1) if ans + d1 > 0 else num(ans + 1), num(ans - d1 // 2) if k != "x" else num(xs[pos - 1] + d1), num(ans + 1), num(ans + 10)],
               "La regla es «%s»: <b>%s</b>." % (rule, num(ans)))


def s1_regla():
    k = R.choice(["+", "-", "x", ":"])
    if k == "+":
        d = R.randint(3, 40)
        a = R.randint(1, 300)
        xs = [a + i * d for i in range(5)]
        ok, ws = "sumar %d" % d, ["restar %d" % d, "sumar %d" % (d + 1), "multiplicar por %d" % (xs[1] // xs[0]) if xs[0] and xs[1] % xs[0] == 0 and xs[1] // xs[0] > 1 else "sumar %d" % (d * 2), "sumar %d" % (d - 1)]
    elif k == "-":
        d = R.randint(3, 40)
        a = 5 * d + R.randint(10, 300)
        xs = [a - i * d for i in range(5)]
        ok, ws = "restar %d" % d, ["sumar %d" % d, "restar %d" % (d + 1), "restar %d" % (d * 2), "restar %d" % (d - 1)]
    elif k == "x":
        m = R.choice([2, 3, 4, 5, 10])
        a = R.randint(1, 4)
        xs = [a * m ** i for i in range(5)]
        if xs[-1] > 99999:
            return None
        ok, ws = "multiplicar por %d" % m, ["sumar %d" % (xs[1] - xs[0]), "multiplicar por %d" % (m + 1), "sumar %d" % m]
    else:
        m = R.choice([2, 3, 10])
        a = R.randint(1, 5)
        xs = [a * m ** (4 - i) for i in range(5)]
        ok, ws = "dividir entre %d" % m, ["restar %d" % (xs[0] - xs[1]), "dividir entre %d" % (m + 1), "restar %d" % m]
    return mcq("¿Cuál es la regla de esta serie? %s, …" % ", ".join(num(x) for x in xs), ok, ws, "Cada número se obtiene al <b>%s</b> al anterior." % ok if k in "+-" else "Cada número se obtiene al <b>%s</b> el anterior." % ok)


def s2_figuras():
    L = R.choice([2, 3, 3, 4])
    pat = [R.choice("cts") for _ in range(L)]
    if len(set(pat)) < 2:
        return None
    seq = (pat * 5)[:R.randint(L * 2 + 1, L * 3 + 1)]
    nxt = pat[len(seq) % L]
    k = R.choice(["sig", "pos"])
    if k == "sig":
        return mcq(dibuja(seq + ["?"]) + "¿Qué figura va en el lugar de «?»?", NOMBRE[nxt], [NOMBRE[x] for x in "cts" if x != nxt] + ["ninguna"],
                   "El patrón se repite cada %d figuras: <b>%s</b>." % (L, NOMBRE[nxt]))
    n = R.choice([10, 12, 15, 20, 21, 24, 30])
    f = pat[(n - 1) % L]
    return mcq(dibuja(pat * 2) + "El patrón se repite siempre igual. ¿Qué figura está en el lugar %d?" % n, NOMBRE[f], [NOMBRE[x] for x in "cts" if x != f] + ["ninguna"],
               "Se repite cada %d: %d : %d = %d y resto %d, así que es la figura %d del grupo: <b>%s</b>." % (L, n, L, (n - 1) // L if (n % L) else n // L, n % L, (n - 1) % L + 1, NOMBRE[f]))


def s3_hueco():
    k = R.choice(["ss", "sr", "rs", "mm", "ms"])
    if k == "ss":
        a, b, c = R.randint(5, 60), R.randint(5, 60), R.randint(5, 60)
        x = a + b - c
        if x <= 0:
            return None
        q = "%d + %d = %d + ___" % (a, b, c)
    elif k == "sr":
        a, b, c = R.randint(5, 60), R.randint(5, 60), R.randint(5, 30)
        x = a + b + c
        q = "%d + %d = ___ − %d" % (a, b, c)
    elif k == "rs":
        a, b, c = R.randint(40, 99), R.randint(5, 30), R.randint(5, 30)
        x = a - b - c
        if x <= 0:
            return None
        q = "%d − %d = %d + ___" % (a, b, c)
    elif k == "mm":
        a, b = R.randint(2, 9), R.randint(2, 9)
        c = R.choice([d for d in range(2, 13) if (a * b) % d == 0 and d not in (a, b)] or [0])
        if not c:
            return None
        x = a * b // c
        q = "%d %s %d = %d %s ___" % (a, POR, b, c, POR)
    else:
        a, b = R.randint(2, 9), R.randint(2, 9)
        c = R.randint(1, a * b - 1)
        x = a * b - c
        q = "%d %s %d = %d + ___" % (a, POR, b, c)
    left = {"ss": a + b if k == "ss" else 0}
    lv = {"ss": a + b, "sr": a + b, "rs": a - b if k == "rs" else 0, "mm": a * b if k in ("mm", "ms") else 0, "ms": a * b if k in ("mm", "ms") else 0}[k]
    return mcq("¿Qué número va en el hueco para que la igualdad sea verdadera? %s" % q, str(x), [str(lv), str(x + 1), str(x - 1) if x > 1 else str(x + 2), str(lv + (c if k != "mm" else 0)) if lv + c != x else str(x + 10)],
               "El lado izquierdo vale %d; el derecho también tiene que valer %d: <b>%d</b>." % (lv, lv, x))


def s3_verdad():
    k = R.choice(["ok", "mal"])
    a, b = R.randint(10, 60), R.randint(10, 60)
    c = R.randint(5, a + b - 5)
    d = a + b - c if k == "ok" else a + b - c + R.choice([-2, -1, 1, 2, 10])
    if d <= 0:
        return None
    ok = (a + b == c + d)
    return mcq("¿Es verdadera esta igualdad? %d + %d = %d + %d" % (a, b, c, d), "verdadera" if ok else "falsa", ["falsa" if ok else "verdadera", "solo si se suman todos los números", "no se puede saber"],
               "%d + %d = %d y %d + %d = %d: es <b>%s</b>." % (a, b, a + b, c, d, c + d, "verdadera" if ok else "falsa"))


def s4_tabla():
    k = R.choice(["+", "x", "x+"])
    xs = sorted(R.sample(range(1, 12), 4))
    if k == "+":
        d = R.randint(3, 25)
        f = lambda v: v + d
        rule = "sumar %d" % d
    elif k == "x":
        m = R.randint(2, 9)
        f = lambda v: v * m
        rule = "multiplicar por %d" % m
    else:
        m, d = R.randint(2, 5), R.randint(1, 9)
        f = lambda v: v * m + d
        rule = "multiplicar por %d y sumar %d" % (m, d)
    tb = "<table class='sn-table' style='width:auto'><thead><tr><th>Entrada</th>%s</tr></thead><tbody><tr><th>Salida</th>%s</tr></tbody></table>" % (
        "".join("<td>%d</td>" % v for v in xs), "".join("<td>%s</td>" % (f(v) if i < 3 else "?") for i, v in enumerate(xs)))
    a = f(xs[3])
    return mcq(tb + "La máquina sigue siempre la misma regla. ¿Qué número sale en «?»?", str(a), [str(a + 1), str(f(xs[2]) + (f(xs[2]) - f(xs[1]))) if f(xs[2]) + (f(xs[2]) - f(xs[1])) != a else str(a + 2), str(xs[3] + (f(xs[0]) - xs[0])) if xs[3] + (f(xs[0]) - xs[0]) != a else str(a - 1), str(a * 2)],
               "La regla es «%s»: %d → <b>%d</b>." % (rule, xs[3], a))


s5_problemas = bank(R, [
    ("Un taxi cobra 3 € al subir y 2 € por cada kilómetro. ¿Cuánto cuesta un viaje de 6 km?", "15 €", ["12 €", "18 €", "11 €"]),
    ("En una fila de sillas, la primera tiene el número 5 y cada una suma 4. ¿Qué número tiene la quinta silla?", "21", ["25", "20", "9"]),
    ("Un árbol mide 120 cm y crece 15 cm cada año. ¿Cuánto medirá dentro de 4 años?", "180 cm", ["135 cm", "60 cm", "195 cm"]),
    ("Con 1 mesa se sientan 4 personas, con 2 mesas juntas 6, con 3 mesas juntas 8. ¿Cuántas con 5 mesas juntas?", "12", ["20", "10", "14"]),
    ("Hugo tiene 50 € y gasta 6 € cada semana. ¿Cuánto le quedará después de 5 semanas?", "20 €", ["30 €", "44 €", "26 €"]),
    ("Un cuadrado se hace con 4 palillos, dos cuadrados en fila con 7 y tres con 10. ¿Cuántos palillos hacen falta para 5 cuadrados?", "16", ["20", "13", "15"]),
    ("Si 3 cajas iguales pesan lo mismo que 12 kg, ¿cuánto pesa una caja?", "4 kg", ["9 kg", "36 kg", "15 kg"]),
    ("En una balanza hay 2 sandías iguales en un plato y 8 kg en el otro, y está equilibrada. ¿Cuánto pesa cada sandía?", "4 kg", ["8 kg", "16 kg", "6 kg"]),
    ("Pienso un número, le sumo 15 y obtengo 42. ¿Qué número he pensado?", "27", ["57", "37", "28"]),
    ("Pienso un número, lo multiplico por 6 y obtengo 54. ¿Qué número he pensado?", "9", ["48", "60", "8"]),
    ("Pienso un número, le resto 25 y obtengo 40. ¿Qué número he pensado?", "65", ["15", "55", "75"]),
    ("Un tren sale cada 20 minutos desde las 8:00. ¿A qué hora sale el quinto tren?", "9:20", ["9:40", "9:00", "8:50"]),
    ("Un libro tiene las páginas numeradas. Si lees de la página 15 a la 22 (las dos incluidas), ¿cuántas páginas lees?", "8", ["7", "22", "37"]),
    ("En una caja hay el doble de canicas rojas que azules. Si hay 14 azules, ¿cuántas canicas hay en total?", "42", ["28", "16", "21"]),
    ("Lucía tiene 8 años y su madre 36. ¿Cuántos años tendrá Lucía cuando su madre tenga 40?", "12", ["16", "4", "44"]),
    ("Pienso un número, lo divido entre 4 y obtengo 9. ¿Qué número he pensado?", "36", ["13", "5", "32"]),
    ("Una ficha avanza 3 casillas en cada turno empezando en la casilla 2. ¿En qué casilla está después de 6 turnos?", "20", ["18", "21", "17"]),
    ("El primer día de un mes es lunes. ¿Qué día de la semana es el día 15?", "lunes", ["domingo", "martes", "miércoles"]),
], "problemas")


def main():
    seen = set()
    sets = [
        ("Series de números", mix(R, seen, [(s1_series, 14), (s1_regla, 6)])),
        ("Patrones con figuras y reglas", mix(R, seen, [(s2_figuras, 10), (s1_regla, 10)])),
        ("Igualdades con hueco", mix(R, seen, [(s3_hueco, 20)])),
        ("Igualdades y tablas", mix(R, seen, [(s3_verdad, 10), (s4_tabla, 10)])),
        ("Problemas", mix(R, seen, [(s5_problemas, 16), (s4_tabla, 4)])),
    ]
    body = lesson(
        ["En una <b>serie</b> cada número se obtiene del anterior con la misma <b>regla</b>: sumar, restar, multiplicar o dividir. Comprueba la regla con varios números, no solo con los dos primeros.",
         "El signo <b>=</b> significa que los dos lados <b>valen lo mismo</b>, como una balanza en equilibrio.",
         "Para completar una igualdad con hueco, calcula primero el lado que está completo y después busca el número que hace que el otro lado valga lo mismo."],
        [("Serie: 7, 11, 15, 19, …", ["La regla es sumar 4", "19 + 4"], "23"),
         ("15 + 9 = 30 − ___", ["15 + 9 = 24", "30 − 6 = 24"], "6")],
        [["Pensar que = es «escribe el resultado»", "En 15 + 9 = ___ + 4, el hueco no es 24: es 20."],
         ["Mirar solo dos números de la serie", "Comprueba la regla con todos los números."],
         ["Contar mal la posición en un patrón", "Divide la posición entre lo que mide el grupo que se repite y mira el resto."]])
    faq = [("¿Qué significa el signo igual?", "Que lo que hay a un lado vale lo mismo que lo que hay al otro lado. Por eso 8 + 7 = 10 + 5 es verdadera."),
           ("¿Cómo se encuentra la regla de una serie?", "Se mira cuánto cambia cada número respecto al anterior. Si siempre aumenta lo mismo, la regla es sumar; si siempre se multiplica por el mismo número, es multiplicar.")]
    make_unit(R, "patrones-e-igualdades", "A",
              "Patrones: identificación, descripción y extensión de patrones numéricos y geométricos; relaciones de igualdad: el signo igual; igualdades con un término desconocido; tablas de entrada y salida",
              "Patrones, series e igualdades", "Patrones e igualdades",
              "Fichas de matemáticas de 4.º de Primaria: series de números, reglas, patrones con figuras, igualdades con hueco, el signo igual, tablas de entrada y salida y problemas. 100 ejercicios con soluciones.",
              "El = es una balanza equilibrada", "Comprueba la regla con todos los números.",
              body, faq, sets, 23)


if __name__ == "__main__":
    main()
