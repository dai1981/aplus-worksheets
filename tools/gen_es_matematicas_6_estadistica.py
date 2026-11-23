# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Estadística (Sentido estocástico)
Tipos de variables (cualitativa y cuantitativa), frecuencia absoluta y relativa, tablas, gráficos de barras, lineales y de sectores;
medidas: media, moda, mediana (6.º) y rango.
Errores: no ordenar los datos para la mediana, dividir entre un número equivocado de datos, confundir la moda con su frecuencia.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d, fr, table, sg
from es_common import grafico

R = None
LV = 6


def datos(n=None):
    n = n or R.choice([5, 6, 7, 8] if LV == 6 else [4, 5, 6])
    return [R.randint(1, 20) for _ in range(n)]


def s1_media():
    for _ in range(50):
        xs = datos()
        if sum(xs) % len(xs) == 0 or (LV == 6 and F(sum(xs), len(xs)).denominator in (2, 4, 5)):
            break
    else:
        return None
    m = F(sum(xs), len(xs))
    return M("Calcula la media de estos datos: %s" % ", ".join(map(str, xs)), d(m), [num(sum(xs)), d(F(sum(xs), len(xs) - 1)) if F(sum(xs), len(xs) - 1).denominator in (1, 2, 4, 5) else num(int(m) + 2), d(m + 1), num(max(xs))],
             "Sumamos (%d) y dividimos entre el número de datos (%d): <b>%s</b>." % (sum(xs), len(xs), d(m)))


def s2_moda_rango():
    k = R.choice(["moda", "rango"] + (["mediana", "mediana"] if LV == 6 else []))
    xs = datos()
    if k == "moda":
        v = R.choice(xs)
        xs = xs + [v, v]
        R.shuffle(xs)
        c = {x: xs.count(x) for x in xs}
        top = max(c.values())
        if list(c.values()).count(top) > 1:
            return None
        mo = [x for x in c if c[x] == top][0]
        return M("¿Cuál es la moda de estos datos? %s" % ", ".join(map(str, xs)), str(mo), [str(top) if top not in xs else str(max(xs)), str(max(xs)) if max(xs) != mo else str(min(xs)), str(xs[0]) if xs[0] != mo else str(xs[-1]), str(len(xs))],
                 "La moda es el dato que más se repite (%d veces): <b>%d</b>." % (top, mo))
    if k == "rango":
        return M("¿Cuál es el rango de estos datos? %s" % ", ".join(map(str, xs)), str(max(xs) - min(xs)), [str(max(xs)), str(max(xs) + min(xs)), str(len(xs)), str(max(xs) - min(xs) + 1)],
                 "Rango = mayor − menor = %d − %d = <b>%d</b>." % (max(xs), min(xs), max(xs) - min(xs)))
    if len(xs) % 2 == 0:
        xs = xs[:-1]
    s = sorted(xs)
    me = s[len(s) // 2]
    return M("¿Cuál es la mediana de estos datos? %s" % ", ".join(map(str, xs)), str(me), [str(xs[len(xs) // 2]) if xs[len(xs) // 2] != me else str(me + 1), d(F(sum(xs), len(xs))) if F(sum(xs), len(xs)).denominator == 1 and sum(xs) // len(xs) != me else str(me - 1), str(max(xs) - min(xs))],
             "Ordenamos: %s. El del centro es <b>%d</b>." % (", ".join(map(str, s)), me))


TEMAS = [("Deporte favorito", ["fútbol", "baloncesto", "natación", "tenis", "balonmano"]), ("Fruta favorita", ["manzana", "plátano", "fresa", "naranja", "uva"]),
         ("Medio de transporte al colegio", ["a pie", "en coche", "en autobús", "en bici"]), ("Mascota", ["perro", "gato", "pez", "pájaro", "ninguna"])]


def s3_frecuencias():
    t, cats = R.choice(TEMAS)
    n = 4
    tot = R.choice([20, 25, 40, 50])
    while True:
        vs = [R.randint(1, tot // 2) for _ in range(n - 1)]
        last = tot - sum(vs)
        if 1 <= last and len(set(vs + [last])) == n:
            vs.append(last)
            break
    tb = table(["Respuesta", "Frecuencia absoluta"], [[c, str(v)] for c, v in zip(cats, vs)])
    k = R.choice(["total", "rel", "moda", "pc"] if LV == 6 else ["total", "rel", "moda"])
    i = R.randrange(n)
    if k == "total":
        return M(tb + "%s. ¿Cuántas personas respondieron?" % t, str(tot), [str(tot - vs[-1]), str(max(vs)), str(n)], "%s = <b>%d</b>." % (" + ".join(map(str, vs)), tot))
    if k == "rel":
        return M(tb + "%s. ¿Cuál es la frecuencia relativa de «%s»?" % (t, cats[i]), fr(vs[i], tot), [fr(vs[i], 100) if tot != 100 else fr(vs[i], 10), fr(tot, vs[i]), fr(vs[i], tot - vs[i])], "Frecuencia absoluta / total: <b>%s</b>." % fr(vs[i], tot))
    if k == "moda":
        m = cats[vs.index(max(vs))]
        return M(tb + "%s. ¿Cuál es la moda?" % t, m, cats[:n] + [str(max(vs))], "La frecuencia más alta es %d: <b>%s</b>." % (max(vs), m))
    p = F(vs[i] * 100, tot)
    if p.denominator != 1:
        return None
    return M(tb + "%s. ¿Qué porcentaje eligió «%s»?" % (t, cats[i]), "%d %%" % int(p), ["%d %%" % vs[i], "%d %%" % (100 - int(p)), "%d %%" % (int(p) + 5)], "%d de %d = %s = <b>%d %%</b>." % (vs[i], tot, fr(int(p), 100), int(p)))


def sectores(vals, labels):
    import math
    s = []
    cols = ["#1f5fbf", "#c0392b", "#2e7d32", "#f2c14e", "#8e44ad"]
    tot = sum(vals)
    a0 = -90
    for i, v in enumerate(vals):
        a1 = a0 + 360.0 * v / tot
        x0, y0 = 100 + 80 * math.cos(math.radians(a0)), 100 + 80 * math.sin(math.radians(a0))
        x1, y1 = 100 + 80 * math.cos(math.radians(a1)), 100 + 80 * math.sin(math.radians(a1))
        s.append("<path d='M100 100 L%.1f %.1f A80 80 0 %d 1 %.1f %.1f Z' fill='%s' stroke='#fff' stroke-width='2'/>" % (x0, y0, 1 if a1 - a0 > 180 else 0, x1, y1, cols[i]))
        s.append("<rect x='200' y='%d' width='12' height='12' fill='%s'/><text x='218' y='%d' font-size='12' fill='#333'>%s</text>" % (30 + i * 20, cols[i], 41 + i * 20, labels[i]))
        a0 = a1
    return "<div class='fig'><svg viewBox='0 0 320 200' width='320' role='img' aria-label='gráfico de sectores'>%s</svg></div>" % "".join(s)


def s4_graficos():
    k = R.choice(["barras", "barras", "sectores"])
    t, cats = R.choice(TEMAS)
    if k == "barras":
        step = R.choice([2, 5])
        vs = [R.randint(1, 10) * step for _ in range(4)]
        if len(set(vs)) < 4:
            return None
        pic = grafico(list(zip(cats[:4], vs)), "alumnos", step)
        q = R.choice(["total", "dif", "media"])
        if q == "total":
            return M(pic + "%s. ¿Cuántos alumnos hay en total?" % t, str(sum(vs)), [str(sum(vs) - step), str(max(vs)), str(sum(vs) + step)], "%s = <b>%d</b>." % (" + ".join(map(str, vs)), sum(vs)))
        if q == "dif":
            return M(pic + "%s. ¿Cuántos alumnos más eligieron «%s» que «%s»?" % (t, cats[vs.index(max(vs))], cats[vs.index(min(vs))]), str(max(vs) - min(vs)), [str(max(vs)), str(max(vs) + min(vs)), str(max(vs) - min(vs) + step)],
                     "%d − %d = <b>%d</b>." % (max(vs), min(vs), max(vs) - min(vs)))
        m = F(sum(vs), 4)
        return M(pic + "%s. ¿Cuál es la media de alumnos por opción?" % t, d(m), [num(sum(vs)), d(m + 1), num(max(vs))], "%d : 4 = <b>%s</b>." % (sum(vs), d(m))) if m.denominator in (1, 2, 4) else None
    parts = R.choice([[50, 25, 25], [50, 25, 12.5, 12.5], [25, 25, 50], [75, 25], [40, 30, 20, 10], [60, 20, 20]])
    if any(p != int(p) for p in parts):
        return None
    n = R.choice([20, 40, 60, 100, 200])
    i = R.randrange(len(parts))
    pic = sectores(parts, cats[:len(parts)])
    v = n * parts[i] // 100
    return M(pic + "%s: preguntamos a %d alumnos. «%s» ocupa el %d %% del círculo. ¿Cuántos alumnos la eligieron?" % (t, n, cats[i], parts[i]), str(v), [str(parts[i]), str(n - v), str(v * 2) if v * 2 <= n else str(v // 2)],
             "%d %% de %d = <b>%d</b>." % (parts[i], n, v)) if n * parts[i] % 100 == 0 else None


def s5_problema():
    k = R.choice(["nota", "variable", "media_falta", "temp"])
    if k == "variable":
        q, a, w = R.choice([("¿Qué tipo de variable es «el color de pelo»?", "cualitativa", ["cuantitativa", "numérica", "continua"]),
                            ("¿Qué tipo de variable es «el número de hermanos»?", "cuantitativa", ["cualitativa", "de colores", "no es una variable"]),
                            ("¿Qué tipo de variable es «el deporte favorito»?", "cualitativa", ["cuantitativa", "numérica", "de medida"]),
                            ("¿Qué tipo de variable es «la altura en cm»?", "cuantitativa", ["cualitativa", "de colores", "no es una variable"]),
                            ("¿Qué medida se puede calcular con datos cualitativos?", "la moda", ["la media", "el rango", "la mediana"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    if k == "nota":
        xs = [R.randint(4, 10) for _ in range(4)]
        if sum(xs) % 4:
            return None
        return M("Las notas de Hugo en cuatro exámenes son %s. ¿Cuál es su nota media?" % ", ".join(map(str, xs)), str(sum(xs) // 4), [str(sum(xs)), str(max(xs)), str(sum(xs) // 4 + 1)], "%d : 4 = <b>%d</b>." % (sum(xs), sum(xs) // 4))
    if k == "media_falta":
        m, n = R.randint(5, 9), R.choice([3, 4, 5])
        xs = [R.randint(3, 10) for _ in range(n - 1)]
        last = m * n - sum(xs)
        if not 0 < last <= 10:
            return None
        return M("La media de %d notas es %d. Las primeras son %s. ¿Cuál es la última?" % (n, m, ", ".join(map(str, xs))), str(last), [str(m), str(m * n), str(last + 1)], "Total: %d × %d = %d; %d − %d = <b>%d</b>." % (m, n, m * n, m * n, sum(xs), last))
    xs = [R.randint(-2, 15) for _ in range(5)] if LV == 6 else [R.randint(5, 25) for _ in range(5)]
    if sum(xs) % 5:
        return None
    return M("Temperaturas máximas de cinco días (°C): %s. ¿Cuál es la temperatura media?" % ", ".join(map(lambda v: ("−%d" % -v) if v < 0 else str(v), xs)), "%s °C" % sg(sum(xs) // 5),
             ["%s °C" % sg(sum(xs)), "%s °C" % sg(max(xs)), "%s °C" % sg(max(xs) - min(xs))], "Sumamos (%s) y dividimos entre 5: <b>%s °C</b>." % (sg(sum(xs)), sg(sum(xs) // 5)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40021 + lv * 1000)
    seen = set()
    sets = [
        ("Tablas de frecuencias", mix(R, seen, [(s3_frecuencias, 20)])),
        ("Gráficos", mix(R, seen, [(s4_graficos, 20)])),
        ("La media aritmética", mix(R, seen, [(s1_media, 20)])),
        ("Moda, mediana y rango" if lv == 6 else "Moda y rango", mix(R, seen, [(s2_moda_rango, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["La <b>frecuencia absoluta</b> es las veces que aparece un dato; la <b>relativa</b>, esa frecuencia dividida entre el total.",
         "<b>Media</b>: suma todos los datos y divide entre cuántos hay. <b>Moda</b>: el dato que más se repite. <b>Rango</b>: mayor − menor." + (" <b>Mediana</b>: el dato del centro cuando están ordenados." if lv == 6 else ""),
         "En un gráfico de barras, mira la escala. En uno de sectores, cada parte del círculo es un porcentaje del total."],
        [("Media de 6, 9, 7, 10, 8", ["6 + 9 + 7 + 10 + 8 = 40", "40 : 5"], "8"),
         ("Mediana de 3, 9, 4, 7, 5" if lv == 6 else "Rango de 3, 9, 4, 7, 5", ["Ordenados: 3, 4, 5, 7, 9", "El del centro"] if lv == 6 else ["9 − 3"], "5" if lv == 6 else "6")],
        [["Dividir entre otro número", "La media se divide entre el número de datos."],
         ["No ordenar para la mediana" if lv == 6 else "Confundir moda y frecuencia", "Ordena los datos antes de buscar el centro." if lv == 6 else "La moda es el dato, no cuántas veces aparece."],
         ["Leer mal la escala", "Si cada línea vale 5, una barra entre 20 y 30 marca 25."]])
    faq = [("¿Cómo se calcula la media aritmética?", "Se suman todos los datos y se divide entre el número de datos. La media de 4, 6 y 8 es 18 : 3 = 6."),
           ("¿Qué diferencia hay entre media, moda y mediana?", "La media reparte el total por igual; la moda es el dato más repetido; la mediana es el dato central cuando se ordenan.")]
    make_unit(R, "estadistica", "S",
              "Organización y análisis de datos: variables cualitativas y cuantitativas, frecuencias absolutas y relativas, tablas y gráficos (barras, líneas y sectores); medidas de centralización (media, moda" + (", mediana" if lv == 6 else "") + ") y rango",
              "Estadística: tablas, gráficos y media", "Estadística",
              "Fichas de matemáticas de %d.º de Primaria: frecuencias, tablas, gráficos de barras y de sectores, media, moda%s y rango y problemas. 100 ejercicios con soluciones." % (lv, ", mediana" if lv == 6 else ""),
              "Media: suma y divide", "Moda: el dato que más se repite.",
              body, faq, sets, 21, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
