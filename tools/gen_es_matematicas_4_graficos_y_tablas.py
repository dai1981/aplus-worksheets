# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Gráficos y tablas (Sentido estocástico)
Recoger datos con recuento (marcas de cinco en cinco), tablas de frecuencias y de doble entrada, gráficos de barras,
pictogramas y gráficos lineales; leer, comparar y calcular con los datos (total, diferencia); la moda.
Errores: leer mal la escala del gráfico, contar los símbolos del pictograma sin mirar cuánto vale cada uno.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, grafico, bank, POR
import fr_common as _F

R = random.Random(44024)
TEMAS = [
    ("Fruta favorita de 4.º A", ["manzana", "plátano", "fresa", "naranja", "uva"], "alumnos"),
    ("Deporte favorito", ["fútbol", "baloncesto", "natación", "tenis", "balonmano"], "alumnos"),
    ("Libros leídos en el trimestre", ["Lucía", "Hugo", "Martina", "Pablo", "Sofía"], "libros"),
    ("Animales de la granja escuela", ["gallinas", "cabras", "ovejas", "cerdos", "vacas"], "animales"),
    ("Medio de transporte para ir al colegio", ["a pie", "en coche", "en autobús", "en bici", "en patinete"], "alumnos"),
    ("Color favorito", ["azul", "rojo", "verde", "amarillo", "morado"], "alumnos"),
]


def datos(step):
    t, cats, u = R.choice(TEMAS)
    n = R.randint(4, 5)
    cs = cats[:n]
    vs = R.sample(range(1, 11), n)
    vs = [v * step for v in vs]
    return t, list(zip(cs, vs)), u


def s1_barras():
    step = R.choice([1, 2, 5, 10])
    t, d, u = datos(step)
    pic = grafico(d, u, step if step > 1 else None)
    k = R.choice(["valor", "max", "min", "dif", "total"])
    names = [c for c, _ in d]
    vals = dict(d)
    if k == "valor":
        c = R.choice(names)
        v = vals[c]
        return mcq(pic + "%s. ¿Cuántos %s hay en «%s»?" % (t, u, c), str(v), [str(v + step), str(v - step) if v > step else str(v + 2 * step), str(v // step) if step > 1 else str(v + 1), str(max(vals.values()))],
                   "La barra de «%s» llega a %d: <b>%d</b>." % (c, v, v))
    if k in ("max", "min"):
        f = max if k == "max" else min
        c = f(names, key=lambda x: vals[x])
        return mcq(pic + "%s. ¿Qué categoría tiene %s %s?" % (t, "más" if k == "max" else "menos", u), c, names, "La barra %s es la de <b>%s</b> (%d)." % ("más alta" if k == "max" else "más baja", c, vals[c]))
    if k == "dif":
        a, b = R.sample(names, 2)
        if vals[a] == vals[b]:
            return None
        hi, lo = (a, b) if vals[a] > vals[b] else (b, a)
        dd = vals[hi] - vals[lo]
        return mcq(pic + "%s. ¿Cuántos %s más hay en «%s» que en «%s»?" % (t, u, hi, lo), str(dd), [str(vals[hi] + vals[lo]), str(dd + step), str(vals[hi]), str(dd - step) if dd > step else str(dd + 2 * step)],
                   "%d − %d = <b>%d</b>." % (vals[hi], vals[lo], dd))
    tot = sum(vals.values())
    return mcq(pic + "%s. ¿Cuántos %s hay en total?" % (t, u), str(tot), [str(tot + step), str(tot - step), str(max(vals.values())), str(len(vals))],
               "%s = <b>%d</b>." % (" + ".join(str(v) for v in vals.values()), tot))


def picto(d, each):
    s = []
    y = 10
    for c, v in d:
        s.append("<text x='4' y='%d' font-size='13' fill='#333'>%s</text>" % (y + 16, c))
        full, half = divmod(v, each)
        for i in range(full):
            s.append("<circle cx='%d' cy='%d' r='10' fill='#f2c14e' stroke='#333'/>" % (130 + i * 26, y + 11))
        if half:
            x = 130 + full * 26
            s.append("<path d='M%d %d A10 10 0 0 0 %d %d Z' fill='#f2c14e' stroke='#333'/>" % (x, y + 1, x, y + 21))
        y += 30
    s.append("<circle cx='14' cy='%d' r='10' fill='#f2c14e' stroke='#333'/><text x='30' y='%d' font-size='13' fill='#333'>= %d</text>" % (y + 14, y + 19, each))
    H = y + 30
    return "<div class='fig'><svg viewBox='0 0 400 %d' width='400' role='img' aria-label='pictograma'>%s</svg></div>" % (H, "".join(s))


def s2_picto():
    each = R.choice([2, 4, 10])
    t, cats, u = R.choice(TEMAS)
    n = 4
    vals = [R.randint(1, 8) * each + (each // 2 if R.random() < 0.3 else 0) for _ in range(n)]
    d = list(zip(cats[:n], vals))
    pic = picto(d, each)
    k = R.choice(["valor", "valor", "total", "dif"])
    if k == "valor":
        c, v = R.choice(d)
        return mcq(pic + "%s. Cada círculo vale %d. ¿Cuántos %s hay en «%s»?" % (t, each, u, c), str(v), [str(v // each) if v % each == 0 else str(v // each + 1), str(v + each), str(v - each // 2) if v > each else str(v + each // 2), str(v * 2)],
                   "Cada círculo vale %d (medio círculo, %d): <b>%d</b>." % (each, each // 2, v))
    if k == "total":
        tot = sum(vals)
        return mcq(pic + "%s. Cada círculo vale %d. ¿Cuántos %s hay en total?" % (t, each, u), str(tot), [str(sum(v // each for v in vals)), str(tot + each), str(tot - each), str(max(vals))],
                   "%s = <b>%d</b>." % (" + ".join(map(str, vals)), tot))
    (a, va), (b, vb) = R.sample(d, 2)
    if va == vb:
        return None
    hi, lo = ((a, va), (b, vb)) if va > vb else ((b, vb), (a, va))
    return mcq(pic + "%s. Cada círculo vale %d. ¿Cuántos %s más hay en «%s» que en «%s»?" % (t, each, u, hi[0], lo[0]), str(hi[1] - lo[1]), [str((hi[1] - lo[1]) // each) if (hi[1] - lo[1]) // each != hi[1] - lo[1] else str(hi[1] - lo[1] + 1), str(hi[1] + lo[1]), str(hi[1] - lo[1] + each), str(hi[1])],
               "%d − %d = <b>%d</b>." % (hi[1], lo[1], hi[1] - lo[1]))


def marcas(n):
    g, r = divmod(n, 5)
    return " ".join(["<s>||||</s>"] * g + (["|" * r] if r else []))


def s3_tablas():
    k = R.choice(["recuento", "frec", "doble", "moda"])
    if k == "recuento":
        n = R.randint(6, 28)
        return mcq("En un recuento se han hecho estas marcas: <span style='font-family:monospace;font-size:1.2em'>%s</span>. Cada grupo tachado son 5. ¿Cuántas son?" % marcas(n), str(n),
                   [str(n + 1), str(n - 1), str(n // 5 + n % 5), str(n + 5)], "%d grupos de 5 y %d sueltas: <b>%d</b>." % (n // 5, n % 5, n))
    if k == "frec":
        t, cats, u = R.choice([x for x in TEMAS if x[2] == "alumnos"])
        vs = R.sample(range(2, 15), 4)
        tb = _F.table(["Respuesta", "Frecuencia"], [[c, str(v)] for c, v in zip(cats, vs)])
        tot = sum(vs)
        return mcq(tb + "%s. ¿Cuántos datos se han recogido en total?" % t, str(tot), [str(tot - vs[-1]), str(max(vs)), str(tot + 1), str(len(vs))], "%s = <b>%d</b>." % (" + ".join(map(str, vs)), tot))
    if k == "doble":
        cls = ["4.º A", "4.º B"]
        act = ["teatro", "ajedrez", "robótica"]
        vs = [[R.randint(3, 15) for _ in act] for _ in cls]
        tb = _F.table(["", ] + act, [[c] + [str(v) for v in row] for c, row in zip(cls, vs)])
        i, j = R.randrange(2), R.randrange(3)
        kk = R.choice(["celda", "col", "fila"])
        if kk == "celda":
            v = vs[i][j]
            return mcq(tb + "Actividades extraescolares. ¿Cuántos alumnos de %s van a %s?" % (cls[i], act[j]), str(v), [str(vs[1 - i][j]), str(vs[i][(j + 1) % 3]), str(vs[0][j] + vs[1][j]), str(v + 1)],
                       "Fila «%s», columna «%s»: <b>%d</b>." % (cls[i], act[j], v))
        if kk == "col":
            v = vs[0][j] + vs[1][j]
            return mcq(tb + "Actividades extraescolares. ¿Cuántos alumnos en total van a %s?" % act[j], str(v), [str(vs[0][j]), str(vs[1][j]), str(sum(vs[0])), str(v + 1)],
                       "%d + %d = <b>%d</b>." % (vs[0][j], vs[1][j], v))
        v = sum(vs[i])
        return mcq(tb + "Actividades extraescolares. ¿Cuántos alumnos de %s van a alguna actividad (cada alumno a una sola)?" % cls[i], str(v), [str(sum(vs[1 - i])) if sum(vs[1 - i]) != v else str(v + 2), str(vs[i][0] + vs[i][1]), str(v + 1), str(max(vs[i]))],
                   "%s = <b>%d</b>." % (" + ".join(map(str, vs[i])), v))
    t, cats, u = R.choice([x for x in TEMAS if x[2] == "alumnos"])
    vs = R.sample(range(2, 15), 4)
    tb = _F.table(["Respuesta", "Frecuencia"], [[c, str(v)] for c, v in zip(cats, vs)])
    m = cats[vs.index(max(vs))]
    return mcq(tb + "%s. ¿Cuál es la moda (el dato que más se repite)?" % t, m, cats[:4] + [str(max(vs))], "La frecuencia más alta es %d: la moda es <b>%s</b>." % (max(vs), m))


def lineal(vals, labels, unit):
    W, H, x0, y0 = 380, 180, 44, 14
    top = max(vals)
    step = 5 if top <= 30 else 10
    top = (top // step + 1) * step
    s = []
    for v in range(0, top + 1, step):
        y = y0 + H - v / float(top) * H
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#ddd'/><text x='%d' y='%.1f' font-size='11' text-anchor='end' fill='#333'>%d</text>" % (x0, y, W - 6, y, x0 - 4, y + 4, v))
    gap = (W - x0 - 20) / float(len(vals) - 1)
    pts = []
    for i, (v, l) in enumerate(zip(vals, labels)):
        x = x0 + 10 + i * gap
        y = y0 + H - v / float(top) * H
        pts.append("%.1f,%.1f" % (x, y))
        s.append("<text x='%.1f' y='%d' font-size='11' text-anchor='middle' fill='#333'>%s</text>" % (x, y0 + H + 16, l))
    s.append("<polyline points='%s' fill='none' stroke='#1f5fbf' stroke-width='2.5'/>" % " ".join(pts))
    for p in pts:
        x, y = p.split(",")
        s.append("<circle cx='%s' cy='%s' r='4' fill='#1f5fbf'/>" % (x, y))
    s.append("<text x='4' y='10' font-size='11' fill='#333'>%s</text>" % unit)
    return "<div class='fig'><svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='gráfico lineal'>%s</svg></div>" % (W, y0 + H + 26, W, "".join(s))


def s4_lineal():
    k = R.choice(["temp", "altura"])
    if k == "temp":
        labels = ["lun", "mar", "mié", "jue", "vie", "sáb"]
        vals = [R.randint(10, 30) for _ in labels]
        if len(set(vals)) < 6:
            return None
        pic = lineal(vals, labels, "°C")
        q = R.choice(["dia", "max", "sube", "dif"])
        if q == "dia":
            i = R.randrange(6)
            return mcq(pic + "Temperatura máxima de cada día. ¿Qué temperatura hubo el %s?" % {"lun": "lunes", "mar": "martes", "mié": "miércoles", "jue": "jueves", "vie": "viernes", "sáb": "sábado"}[labels[i]],
                       "%d °C" % vals[i], ["%d °C" % vals[(i + 1) % 6], "%d °C" % (vals[i] + 5), "%d °C" % (vals[i] - 2)], "Leemos el punto de ese día: <b>%d °C</b>." % vals[i])
        if q == "max":
            i = vals.index(max(vals))
            full = {"lun": "el lunes", "mar": "el martes", "mié": "el miércoles", "jue": "el jueves", "vie": "el viernes", "sáb": "el sábado"}
            return mcq(pic + "¿Qué día hizo más calor?", full[labels[i]], [full[l] for l in labels], "El punto más alto es %s (%d °C)." % (full[labels[i]], vals[i]))
        if q == "sube":
            ups = [i for i in range(5) if vals[i + 1] - vals[i] == max(vals[j + 1] - vals[j] for j in range(5))]
            if len(ups) != 1 or vals[ups[0] + 1] <= vals[ups[0]]:
                return None
            i = ups[0]
            full = {"lun": "lunes", "mar": "martes", "mié": "miércoles", "jue": "jueves", "vie": "viernes", "sáb": "sábado"}
            ok = "del %s al %s" % (full[labels[i]], full[labels[i + 1]])
            return mcq(pic + "¿Entre qué dos días subió más la temperatura?", ok, ["del %s al %s" % (full[labels[j]], full[labels[j + 1]]) for j in range(5) if j != i],
                       "La línea sube más %s: %d − %d = %d °C." % (ok, vals[i + 1], vals[i], vals[i + 1] - vals[i]))
        a, b = R.sample(range(6), 2)
        dd = abs(vals[a] - vals[b])
        full = {"lun": "el lunes", "mar": "el martes", "mié": "el miércoles", "jue": "el jueves", "vie": "el viernes", "sáb": "el sábado"}
        return mcq(pic + "¿Cuántos grados de diferencia hubo entre %s y %s?" % (full[labels[a]], full[labels[b]]), "%d °C" % dd, ["%d °C" % (vals[a] + vals[b]), "%d °C" % (dd + 2), "%d °C" % (dd + 5) if dd else "%d °C" % 3],
                   "%d − %d = <b>%d °C</b>." % (max(vals[a], vals[b]), min(vals[a], vals[b]), dd)) if dd else None
    labels = ["2020", "2021", "2022", "2023", "2024", "2025"]
    base = R.randint(5, 15)
    vals = [base + sum(R.randint(1, 6) for _ in range(i)) for i in range(6)]
    pic = lineal(vals, labels, "cm")
    i, j = sorted(R.sample(range(6), 2))
    return mcq(pic + "Altura de un arbolito medida cada año. ¿Cuántos centímetros creció de %s a %s?" % (labels[i], labels[j]), "%d cm" % (vals[j] - vals[i]),
               ["%d cm" % vals[j], "%d cm" % (vals[j] + vals[i]), "%d cm" % (vals[j] - vals[i] + 2)], "%d − %d = <b>%d cm</b>." % (vals[j], vals[i], vals[j] - vals[i]))


def main():
    seen = set()
    sets = [
        ("Recuento y tablas", mix(R, seen, [(s3_tablas, 20)])),
        ("Gráficos de barras", mix(R, seen, [(s1_barras, 20)])),
        ("Pictogramas", mix(R, seen, [(s2_picto, 20)])),
        ("Gráficos lineales", mix(R, seen, [(s4_lineal, 20)])),
        ("Repaso con datos", mix(R, seen, [(s1_barras, 8), (s2_picto, 6), (s3_tablas, 6)])),
    ]
    body = lesson(
        ["Para recoger datos hacemos un <b>recuento</b> con marcas (de 5 en 5) y lo pasamos a una <b>tabla de frecuencias</b>: la frecuencia es el número de veces que aparece cada dato.",
         "En un <b>gráfico de barras</b>, mira la escala del eje: cada línea puede valer 1, 2, 5 o 10.",
         "En un <b>pictograma</b>, cada dibujo vale una cantidad: mira la leyenda.",
         "Un <b>gráfico lineal</b> muestra cómo cambia un dato con el tiempo. La <b>moda</b> es el dato con mayor frecuencia."],
        [("Pictograma: cada círculo vale 4 y hay 3 círculos y medio", ["3 × 4 = 12", "medio círculo = 2"], "14"),
         ("Barras: fútbol 25 y tenis 10", ["25 − 10"], "15 más en fútbol")],
        [["Leer mal la escala", "Si cada línea vale 5, la barra entre 20 y 30 marca 25."],
         ["Contar dibujos sin mirar la leyenda", "3 dibujos que valen 10 cada uno son 30, no 3."],
         ["Confundir la moda con el número mayor", "La moda es el dato que más se repite (la categoría), no su frecuencia."]],
        grafico([("lunes", 12), ("martes", 8), ("miércoles", 15)], "alumnos"))
    faq = [("¿Qué es la frecuencia de un dato?", "Es el número de veces que aparece. En una tabla de frecuencias se escribe al lado de cada dato."),
           ("¿Qué es la moda?", "Es el dato que tiene la frecuencia más alta, es decir, el que más se repite.")]
    make_unit(R, "graficos-y-tablas", "S",
              "Recogida, organización y representación de datos: recuento, tablas de frecuencias y de doble entrada, gráficos de barras, pictogramas y gráficos lineales; interpretación de datos; la moda",
              "Gráficos y tablas", "Gráficos y tablas",
              "Fichas de matemáticas de 4.º de Primaria: recuento, tablas de frecuencias y de doble entrada, gráficos de barras, pictogramas, gráficos lineales y la moda. 100 ejercicios con soluciones.",
              "Mira siempre la escala y la leyenda", "Frecuencia: cuántas veces aparece un dato. Moda: el que más se repite.",
              body, faq, sets, 24)


if __name__ == "__main__":
    main()
