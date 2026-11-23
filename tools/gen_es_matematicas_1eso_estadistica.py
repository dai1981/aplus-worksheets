# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Estadística (Sentido estocástico)
build(lv): lv = 1 → variables, frecuencias, gráficos, media, mediana, moda (reutiliza 6.º de Primaria);
lv = 2 → tablas de frecuencias con frecuencias acumuladas, parámetros en tablas, datos agrupados, población y muestra;
lv = 3 → cuartiles, rango intercuartílico, diagrama de caja, varianza y desviación típica, coeficiente de variación;
lv = 4 → «estadistica-bidimensional»: tablas de doble entrada, nubes de puntos, correlación, recta de regresión.
Errores: calcular la mediana sin ordenar, dividir entre el número de valores distintos y no entre el total, confundir correlación con causalidad.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, d, fq, num, unit, L, Kids, tabla, use_, fig

R = None
LV = 1
K = None


def r2(x):
    """redondeo a centésimas con coma"""
    v = int(math.floor(float(x) * 100 + 0.5))
    return d(F(v, 100))


def media_txt(xs):
    return d(F(sum(xs), len(xs))) if F(sum(xs), len(xs)).denominator in (1, 2, 4, 5, 10, 20, 25, 50) else r2(F(sum(xs), len(xs)))


def s_variable():
    q, a, w = R.choice([("El color de pelo de los alumnos es una variable…", "cualitativa", ["cuantitativa discreta", "cuantitativa continua", "numérica"]),
                        ("El número de hermanos es una variable…", "cuantitativa discreta", ["cuantitativa continua", "cualitativa", "nominal"]),
                        ("La altura de los alumnos es una variable…", "cuantitativa continua", ["cuantitativa discreta", "cualitativa", "nominal"]),
                        ("El deporte favorito es una variable…", "cualitativa", ["cuantitativa discreta", "cuantitativa continua", "discreta"]),
                        ("El tiempo que se tarda en llegar al instituto es una variable…", "cuantitativa continua", ["cualitativa", "cuantitativa discreta", "nominal"]),
                        ("El número de libros leídos en un año es una variable…", "cuantitativa discreta", ["cualitativa", "cuantitativa continua", "ordinal"]),
                        ("Para una variable cualitativa, ¿qué parámetro se puede calcular?", "la moda", ["la media", "la mediana", "el rango"]),
                        ("¿Qué gráfico es más adecuado para mostrar porcentajes de un total?", "el diagrama de sectores", ["el histograma", "la nube de puntos", "el polígono de frecuencias"]),
                        ("¿Qué gráfico se usa para datos agrupados en intervalos?", "el histograma", ["el diagrama de sectores", "el pictograma", "la tabla de doble entrada"]),
                        ("Los alumnos encuestados de un instituto son…", "una muestra", ["la población", "una variable", "la frecuencia"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def tabla_frec():
    vals = sorted(R.sample(range(0, 8), 4))
    fs = [R.randint(2, 12) for _ in vals]
    return vals, fs


def s_tabla2():
    vals, fs = tabla_frec()
    n = sum(fs)
    pic = tabla(["x<sub>i</sub>"] + [str(v) for v in vals], [["f<sub>i</sub>"] + [str(f) for f in fs]])
    t = R.choice(["media", "moda", "N", "acum", "mediana", "rel"])
    if t == "media":
        m = F(sum(v * f for v, f in zip(vals, fs)), n)
        return M(pic + "Calcula la media de los datos de la tabla.", r2(m), [r2(F(sum(vals), len(vals))), r2(F(sum(v * f for v, f in zip(vals, fs)), len(vals))), r2(m + 1)],
                 "x̄ = Σxᵢfᵢ / N = %d / %d ≈ <b>%s</b>." % (sum(v * f for v, f in zip(vals, fs)), n, r2(m)))
    if t == "moda":
        if fs.count(max(fs)) > 1:
            return None
        mo = vals[fs.index(max(fs))]
        return M(pic + "¿Cuál es la moda?", str(mo), [str(max(fs)), str(vals[-1]) if vals[-1] != mo else str(vals[0]), str(vals[1]) if vals[1] != mo else str(vals[2])], "El valor con mayor frecuencia (%d): <b>%d</b>." % (max(fs), mo))
    if t == "N":
        return M(pic + "¿Cuántos datos hay en total?", str(n), [str(len(vals)), str(sum(vals)), str(max(fs))], "N = Σfᵢ = <b>%d</b>." % n)
    if t == "acum":
        i = R.randint(1, 3)
        Fi = sum(fs[:i + 1])
        return M(pic + "¿Cuál es la frecuencia absoluta acumulada del valor %d?" % vals[i], str(Fi), [str(fs[i]), str(n - Fi), str(Fi + fs[i])], "Sumamos las frecuencias hasta %d: <b>%d</b>." % (vals[i], Fi))
    if t == "rel":
        i = R.randrange(4)
        return M(pic + "¿Cuál es la frecuencia relativa del valor %d?" % vals[i], fq(F(fs[i], n)), [fq(F(fs[i], 100)) if n != 100 else fq(F(fs[i], 10)), fq(F(n, fs[i])), fq(F(fs[i], n - fs[i]))], "hᵢ = fᵢ / N = %d/%d = <b>%s</b>." % (fs[i], n, fq(F(fs[i], n))))
    if n % 2 == 0:
        return None
    pos = (n + 1) // 2
    acc = 0
    for v, f in zip(vals, fs):
        acc += f
        if acc >= pos:
            me = v
            break
    return M(pic + "¿Cuál es la mediana? (hay %d datos)" % n, str(me), [str(vals[len(vals) // 2]) if vals[len(vals) // 2] != me else str(vals[0]), str(fs[len(fs) // 2]), str(pos)], "El dato central es el que ocupa el lugar %d en las frecuencias acumuladas: <b>%d</b>." % (pos, me))


def s_agrupados():
    a = R.choice([0, 10, 20, 140, 150])
    w = R.choice([5, 10])
    k = 4
    fs = [R.randint(2, 12) for _ in range(k)]
    inter = ["[%d, %d)" % (a + i * w, a + (i + 1) * w) for i in range(k)]
    marcas = [F(2 * a + (2 * i + 1) * w, 2) for i in range(k)]
    pic = tabla(["Intervalo"] + inter, [["f<sub>i</sub>"] + [str(f) for f in fs]])
    t = R.choice(["marca", "media", "modal", "amp"])
    if t == "marca":
        i = R.randrange(k)
        return M(pic + "¿Cuál es la marca de clase del intervalo %s?" % inter[i], d(marcas[i]), [str(a + i * w), str(a + (i + 1) * w), d(marcas[i] + w)], "Punto medio del intervalo: (%d + %d) : 2 = <b>%s</b>." % (a + i * w, a + (i + 1) * w, d(marcas[i])))
    if t == "media":
        m = sum(c * f for c, f in zip(marcas, fs)) / sum(fs)
        return M(pic + "Calcula la media usando las marcas de clase.", r2(m), [r2(sum(marcas) / k), r2(m + w), r2(sum((a + i * w) * f for i, f in enumerate(fs)) / F(sum(fs)))], "x̄ = Σcᵢfᵢ / N ≈ <b>%s</b>." % r2(m))
    if t == "modal":
        if fs.count(max(fs)) > 1:
            return None
        i = fs.index(max(fs))
        return M(pic + "¿Cuál es el intervalo modal?", inter[i], [x for x in inter if x != inter[i]], "Es el de mayor frecuencia (%d): <b>%s</b>." % (max(fs), inter[i]))
    return M(pic + "¿Cuál es la amplitud de cada intervalo?", str(w), [str(k), str(a), str(2 * w)] if a not in (w, 2 * w) else [str(k), str(3 * w), str(2 * w)], "%d − %d = <b>%d</b>." % (a + w, a, w))


def datos_imp():
    n = R.choice([7, 9, 11, 13, 15])
    return sorted(R.randint(1, 30) for _ in range(n))


def quart(xs):
    n = len(xs)
    q1 = xs[math.ceil(n / 4) - 1]
    q3 = xs[math.ceil(3 * n / 4) - 1]
    return q1, xs[n // 2], q3


def caja(xs):
    q1, me, q3 = quart(xs)
    lo, hi = 0, 32
    X = lambda v: 20 + (v - lo) * 9.5
    s = ["<line x1='20' y1='80' x2='%d' y2='80' stroke='#333'/>" % X(hi)]
    for v in range(lo, hi + 1, 4):
        s.append("<line x1='%.1f' y1='76' x2='%.1f' y2='84' stroke='#333'/><text x='%.1f' y='100' font-size='12' text-anchor='middle' font-family='Arial, Helvetica, sans-serif'>%d</text>" % (X(v), X(v), X(v), v))
    s.append("<line x1='%.1f' y1='40' x2='%.1f' y2='40' stroke='#1565c0' stroke-width='2'/>" % (X(xs[0]), X(q1)))
    s.append("<line x1='%.1f' y1='40' x2='%.1f' y2='40' stroke='#1565c0' stroke-width='2'/>" % (X(q3), X(xs[-1])))
    s.append("<rect x='%.1f' y='25' width='%.1f' height='30' fill='#d6e2f6' stroke='#1565c0' stroke-width='2'/>" % (X(q1), X(q3) - X(q1)))
    s.append("<line x1='%.1f' y1='25' x2='%.1f' y2='55' stroke='#c62828' stroke-width='3'/>" % (X(me), X(me)))
    for v in (xs[0], xs[-1]):
        s.append("<line x1='%.1f' y1='32' x2='%.1f' y2='48' stroke='#1565c0' stroke-width='2'/>" % (X(v), X(v)))
    return fig("<svg viewBox='0 0 340 110' width='340' role='img' aria-label='diagrama de caja y bigotes'>%s</svg>" % "".join(s))


def s_cuartiles():
    xs = datos_imp()
    q1, me, q3 = quart(xs)
    show = ", ".join(map(str, R.sample(xs, len(xs))))
    t = R.choice(["me", "q1", "q3", "ri", "caja"])
    if t == "me":
        return M("Calcula la mediana de: %s" % show, str(me), [str(xs[len(xs) // 2 - 1]) if xs[len(xs) // 2 - 1] != me else str(me + 1), r2(F(sum(xs), len(xs))), str(xs[-1] - xs[0])], "Ordenamos (%s); el central es <b>%d</b>." % (", ".join(map(str, xs)), me))
    if t == "q1":
        return M("Calcula el primer cuartil Q₁ de: %s" % show, str(q1), [str(q3), str(me), str(xs[math.ceil(len(xs) / 4)]) if xs[math.ceil(len(xs) / 4)] != q1 else str(q1 + 1)],
                 "Ordenados, Q₁ ocupa el lugar %d (el primero que deja al menos el 25 %% por debajo): <b>%d</b>." % (math.ceil(len(xs) / 4), q1))
    if t == "q3":
        return M("Calcula el tercer cuartil Q₃ de: %s" % show, str(q3), [str(q1), str(me), str(xs[-1])] if xs[-1] != q3 else [str(q1), str(me), str(q3 - 1)],
                 "Ordenados, Q₃ ocupa el lugar %d: <b>%d</b>." % (math.ceil(3 * len(xs) / 4), q3))
    if t == "ri":
        return M("Datos ordenados: %s. ¿Cuál es el rango intercuartílico Q₃ − Q₁?" % ", ".join(map(str, xs)), str(q3 - q1), [str(xs[-1] - xs[0]), str(q3 + q1), str(me - q1)] if me - q1 != q3 - q1 else [str(xs[-1] - xs[0]), str(q3 + q1), str(q3 - q1 + 1)],
                 "Q₁ = %d y Q₃ = %d: <b>%d</b>." % (q1, q3, q3 - q1))
    if xs[-1] > 32:
        return None
    k = R.choice(["me", "q1", "q3", "min"])
    v = {"me": me, "q1": q1, "q3": q3, "min": xs[0]}[k]
    nm = {"me": "la mediana", "q1": "el primer cuartil", "q3": "el tercer cuartil", "min": "el valor mínimo"}[k]
    others = [x for x in (me, q1, q3, xs[0], xs[-1]) if x != v]
    if len(set(others)) < 3:
        return None
    return M(caja(xs) + "¿Qué valor marca %s en este diagrama de caja?" % nm, str(v), [str(x) for x in others], "La caja va de Q₁ a Q₃ y la línea roja es la mediana: <b>%d</b>." % v)


def s_dispersion():
    n = R.choice([4, 5, 6])
    for _ in range(200):
        xs = [R.randint(2, 20) for _ in range(n)]
        if sum(xs) % n == 0:
            break
    else:
        return None
    m = sum(xs) // n
    var = F(sum((x - m) ** 2 for x in xs), n)
    sd = math.sqrt(var)
    t = R.choice(["var", "sd", "cv", "comp"])
    show = ", ".join(map(str, xs))
    if t == "var":
        return M("Datos: %s (media %d). ¿Cuál es la varianza?" % (show, m), r2(var), [r2(sd), r2(F(sum((x - m) ** 2 for x in xs), n - 1)), r2(F(sum(abs(x - m) for x in xs), n))],
                 "σ² = Σ(xᵢ − x̄)² / N = %d / %d ≈ <b>%s</b>." % (sum((x - m) ** 2 for x in xs), n, r2(var)))
    if t == "sd":
        return M("Datos: %s (media %d). ¿Cuál es la desviación típica?" % (show, m), r2(sd), [r2(var), r2(math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))), r2(F(sum(abs(x - m) for x in xs), n))],
                 "σ = √(Σ(xᵢ − x̄)² / N) = √%s ≈ <b>%s</b>." % (r2(var), r2(sd)))
    if t == "cv":
        if not sd:
            return None
        cv = sd / m * 100
        return M("Unos datos tienen media %d y desviación típica %s. ¿Cuál es su coeficiente de variación?" % (m, r2(sd)), "%s %%" % r2(cv), ["%s %%" % r2(m / sd * 100) if sd else "0 %", "%s %%" % r2(sd * m), "%s %%" % r2(cv / 100)],
                 "CV = σ / x̄ · 100 = %s / %d · 100 ≈ <b>%s %%</b>." % (r2(sd), m, r2(cv)))
    a, b = R.sample([1, 2, 3, 4, 5, 6, 8], 2)
    m1, m2 = R.randint(20, 60), R.randint(20, 60)
    cv1, cv2 = F(a, m1), F(b, m2)
    if cv1 == cv2:
        return None
    ok = "el grupo A" if cv1 < cv2 else "el grupo B"
    return M("Grupo A: media %d, σ = %d. Grupo B: media %d, σ = %d. ¿Qué grupo es más homogéneo (menor coeficiente de variación)?" % (m1, a, m2, b), ok, ["el grupo B" if ok == "el grupo A" else "el grupo A", "los dos igual", "el de mayor media"],
             "CV A ≈ %s %%, CV B ≈ %s %%: <b>%s</b>." % (r2(cv1 * 100), r2(cv2 * 100), ok))


def nube(pts, xl, yl):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    X = lambda v: 40 + (v - x0) / float(x1 - x0) * 280
    Y = lambda v: 190 - (v - y0) / float(y1 - y0) * 170
    s = ["<line x1='40' y1='190' x2='325' y2='190' stroke='#333'/><line x1='40' y1='190' x2='40' y2='15' stroke='#333'/>"]
    s.append("<text x='320' y='208' font-size='12' text-anchor='end' font-family='Arial, Helvetica, sans-serif'>%s</text>" % xl)
    s.append("<text x='44' y='14' font-size='12' font-family='Arial, Helvetica, sans-serif'>%s</text>" % yl)
    for x, y in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='#1565c0'/>" % (X(x), Y(y)))
    return fig("<svg viewBox='0 0 340 215' width='340' role='img' aria-label='nube de puntos'>%s</svg>" % "".join(s))


def s_correlacion():
    kind = R.choice(["fpos", "fneg", "dpos", "dneg", "nula"])
    n = 12
    pts = []
    for i in range(n):
        x = R.uniform(0, 10)
        e = R.gauss(0, 0.4 if kind[0] == "f" else 1.8)
        y = {"fpos": x, "fneg": 10 - x, "dpos": x, "dneg": 10 - x, "nula": R.uniform(0, 10)}[kind] + (e if kind != "nula" else 0)
        pts.append((x, y))
    ctx = R.choice([("horas de estudio", "nota"), ("temperatura", "helados vendidos"), ("edad del coche", "precio"), ("altura", "peso"), ("número de calzado", "nota de mates")])
    ok = {"fpos": "correlación positiva fuerte", "fneg": "correlación negativa fuerte", "dpos": "correlación positiva débil", "dneg": "correlación negativa débil", "nula": "no hay correlación"}[kind]
    opts = ["correlación positiva fuerte", "correlación negativa fuerte", "correlación positiva débil", "correlación negativa débil", "no hay correlación"]
    return M(nube(pts, ctx[0], ctx[1]) + "¿Qué tipo de correlación muestra la nube de puntos?", ok, [o for o in opts if o != ok],
             "%s: <b>%s</b>." % ("Los puntos suben" if "pos" in kind else "Los puntos bajan" if "neg" in kind else "Los puntos no siguen ninguna tendencia", ok))


def s_bidim():
    t = R.choice(["r", "recta", "tabla", "causa"])
    if t == "r":
        rv = R.choice(["0,95", "−0,92", "0,35", "−0,30", "0,02", "0,78", "−0,81"])
        v = float(rv.replace(",", ".").replace("−", "-"))
        ok = ("positiva" if v > 0 else "negativa") + (" fuerte" if abs(v) >= 0.75 else " débil" if abs(v) >= 0.2 else "")
        if abs(v) < 0.2:
            ok = "prácticamente nula"
        opts = ["positiva fuerte", "negativa fuerte", "positiva débil", "negativa débil", "prácticamente nula"]
        return M("El coeficiente de correlación entre dos variables es r = %s. ¿Cómo es la correlación?" % rv, ok, [o for o in opts if o != ok], "El signo da el sentido y el valor absoluto, la fuerza: <b>%s</b>." % ok)
    if t == "recta":
        a = R.choice([2, 3, 4, 5])
        b = R.randint(10, 40)
        x = R.randint(3, 12)
        return M("La recta de regresión del gasto (y, en €) sobre los km recorridos (x) es y = %dx + %d. ¿Qué gasto se estima para %d km?" % (a, b, x), "%d €" % (a * x + b), ["%d €" % (a + b + x), "%d €" % (a * x), "%d €" % (b * x + a)], "y = %d · %d + %d = <b>%d €</b>." % (a, x, b, a * x + b))
    if t == "tabla":
        a, b, c, e = [R.randint(3, 20) for _ in range(4)]
        pic = tabla(["", "Sí hace deporte", "No hace deporte"], [["Chicas", str(a), str(b)], ["Chicos", str(c), str(e)]])
        k = R.choice(["total", "deporte", "chicas"])
        if k == "total":
            return M(pic + "¿Cuántas personas se encuestaron?", str(a + b + c + e), [str(a + b), str(a + c), str(a + b + c)], "%d + %d + %d + %d = <b>%d</b>." % (a, b, c, e, a + b + c + e))
        if k == "deporte":
            return M(pic + "¿Cuántas personas hacen deporte?", str(a + c), [str(a + b), str(b + e), str(a)], "%d + %d = <b>%d</b>." % (a, c, a + c))
        return M(pic + "¿Qué porcentaje de las chicas hace deporte?", "%s %%" % r2(F(100 * a, a + b)), ["%s %%" % r2(F(100 * a, a + b + c + e)), "%s %%" % r2(F(100 * a, a + c)), "%d %%" % a], "%d de %d chicas: %d/%d · 100 ≈ <b>%s %%</b>." % (a, a + b, a, a + b, r2(F(100 * a, a + b))))
    q, a, w = R.choice([("Si hay correlación fuerte entre dos variables, ¿una es siempre la causa de la otra?", "no necesariamente", ["sí, siempre", "solo si es positiva", "solo si r = 1"]),
                        ("¿Entre qué valores está el coeficiente de correlación r?", "entre −1 y 1", ["entre 0 y 1", "entre 0 y 100", "entre −100 y 100"]),
                        ("Si r = 1, los puntos de la nube están…", "exactamente sobre una recta creciente", ["muy dispersos", "sobre una recta decreciente", "en un círculo"]),
                        ("¿Para qué sirve la recta de regresión?", "para estimar una variable a partir de la otra", ["para calcular la moda", "para ordenar los datos", "para hacer un histograma"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(47013 + (lv - 1) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 1:
        frec, graf, med, moda, prob = use_("gen_es_matematicas_6_estadistica", 47915, "s3_frecuencias", "s4_graficos", "s1_media", "s2_moda_rango", "s5_problema")
        sets = [("Variables y gráficos", mix(R, seen, [(s_variable, 8), (graf, 12)])), ("Tablas de frecuencias", mix(R, seen, [(frec, 20)])), ("La media", mix(R, seen, [(med, 20)])),
                ("Moda, mediana y rango", mix(R, seen, [(moda, 20)])), ("Problemas", mix(R, seen, [(prob, 20)]))]
        think = ["Una variable es <b>cualitativa</b> (color, deporte) o <b>cuantitativa</b> (número de hermanos, altura).",
                 "La <b>frecuencia absoluta</b> es cuántas veces aparece un dato; la <b>relativa</b>, esa cantidad dividida entre el total.",
                 "Media: suma entre el número de datos. Mediana: el dato central, con los datos ordenados. Moda: el más repetido."]
        ex = [("Datos: 3, 7, 5, 7, 8", ["Media: 30 : 5 = 6", "Ordenados: 3, 5, 7, 7, 8"], "media 6, mediana 7, moda 7")]
        mist = [["Calcular la mediana sin ordenar", "Ordena primero los datos."], ["Dividir entre un número equivocado", "Divide entre el total de datos."], ["Usar la media con datos cualitativos", "Para colores o deportes solo hay moda."]]
        slug, title, short, kb, ks = "estadistica", "Estadística: tablas, gráficos y medias", "Estadística", "Media: suma : número de datos", "Mediana: el dato central, ya ordenado."
        meta = "Fichas de matemáticas de 1.º de ESO: tipos de variables, tablas de frecuencias, gráficos, media, mediana, moda y rango. 100 ejercicios con soluciones."
        std = "Variables estadísticas; tablas de frecuencias; gráficos estadísticos; medidas de centralización y rango"
        sort = 13
    elif lv == 2:
        sets = [("Variables y tablas", mix(R, seen, [(s_variable, 8), (s_tabla2, 12)])), ("Frecuencias acumuladas y relativas", mix(R, seen, [(s_tabla2, 20)])), ("Media, mediana y moda en tablas", mix(R, seen, [(s_tabla2, 20)])),
                ("Datos agrupados", mix(R, seen, [(s_agrupados, 20)])), ("Mediana y cuartiles", mix(R, seen, [(s_cuartiles, 20)]))]
        think = ["La <b>población</b> es todo el grupo que se estudia; la <b>muestra</b>, la parte que se encuesta.",
                 "En una tabla, la media es x̄ = Σxᵢfᵢ / N. La frecuencia acumulada suma las frecuencias hasta ese valor.",
                 "Con datos agrupados en intervalos se usa la <b>marca de clase</b> (el punto medio) en lugar de cada dato."]
        ex = [("Valores 1, 2, 3 con frecuencias 4, 5, 1", ["Σxᵢfᵢ = 4 + 10 + 3 = 17", "N = 10"], "x̄ = 1,7")]
        mist = [["Dividir entre el número de valores distintos", "Divide entre N, la suma de las frecuencias."], ["Olvidar multiplicar por la frecuencia", "Cada valor cuenta tantas veces como su frecuencia."], ["Usar el extremo del intervalo", "Usa la marca de clase."]]
        slug, title, short, kb, ks = "estadistica", "Estadística: frecuencias y parámetros", "Estadística", "x̄ = Σxᵢfᵢ / N", "N es el total de datos."
        meta = "Fichas de matemáticas de 2.º de ESO: población y muestra, frecuencias acumuladas, media, mediana y moda en tablas y datos agrupados. 100 ejercicios con soluciones."
        std = "Población y muestra; tablas de frecuencias absolutas, relativas y acumuladas; medidas de centralización; datos agrupados en intervalos"
        sort = 12
    elif lv == 3:
        sets = [("Mediana y cuartiles", mix(R, seen, [(s_cuartiles, 20)])), ("Diagramas de caja", mix(R, seen, [(s_cuartiles, 20)])), ("Varianza y desviación típica", mix(R, seen, [(s_dispersion, 20)])),
                ("Parámetros en tablas", mix(R, seen, [(s_tabla2, 20)])), ("Datos agrupados", mix(R, seen, [(s_agrupados, 20)]))]
        think = ["Los <b>cuartiles</b> Q₁, Q₂ (mediana) y Q₃ dividen los datos ordenados en cuatro partes iguales. El rango intercuartílico es Q₃ − Q₁.",
                 "El <b>diagrama de caja</b> muestra el mínimo, Q₁, la mediana, Q₃ y el máximo.",
                 "La <b>desviación típica</b> σ mide cuánto se separan los datos de la media: σ = √(Σ(xᵢ − x̄)² / N). El coeficiente de variación es σ / x̄ · 100."]
        ex = [("Datos: 2, 4, 4, 6, 9 (media 5)", ["Σ(xᵢ − x̄)² = 9 + 1 + 1 + 1 + 16 = 28", "σ² = 28 / 5 = 5,6"], "σ ≈ 2,37")]
        mist = [["Calcular cuartiles sin ordenar", "Ordena los datos primero."], ["Olvidar la raíz en la desviación típica", "σ es la raíz de la varianza."], ["Comparar dispersiones con σ si las medias son muy distintas", "Usa el coeficiente de variación."]]
        slug, title, short, kb, ks = "estadistica", "Estadística: cuartiles y dispersión", "Estadística", "σ: cuánto se alejan de la media", "Rango intercuartílico: Q₃ − Q₁."
        meta = "Fichas de matemáticas de 3.º de ESO: cuartiles, diagramas de caja, varianza, desviación típica, coeficiente de variación y tablas. 100 ejercicios con soluciones."
        std = "Medidas de posición (cuartiles) y de dispersión (rango, rango intercuartílico, varianza, desviación típica, coeficiente de variación); diagrama de caja y bigotes"
        sort = 11
    else:
        sets = [("Tablas de doble entrada", mix(R, seen, [(s_bidim, 20)])), ("Nubes de puntos", mix(R, seen, [(s_correlacion, 20)])), ("Coeficiente de correlación y regresión", mix(R, seen, [(s_bidim, 20)])),
                ("Dispersión y cuartiles", mix(R, seen, [(s_dispersion, 10), (s_cuartiles, 10)])), ("Interpretar estudios", mix(R, seen, [(s_correlacion, 10), (s_bidim, 10)]))]
        think = ["Una <b>variable bidimensional</b> estudia dos variables a la vez, por ejemplo horas de estudio y nota.",
                 "En la <b>nube de puntos</b> se ve la correlación: positiva si los puntos suben, negativa si bajan, fuerte si están cerca de una recta.",
                 "El coeficiente r está entre −1 y 1. La <b>recta de regresión</b> sirve para estimar un valor de y a partir de x. Correlación no significa causa."]
        ex = [("y = 3x + 20 para x = 10", ["3 · 10 + 20"], "50")]
        mist = [["Confundir correlación con causa", "Que dos variables vayan juntas no prueba que una cause la otra."], ["Pensar que r = −0,9 es débil", "El signo indica el sentido; |r| cerca de 1 es fuerte."], ["Estimar muy lejos de los datos", "La recta sirve cerca de los valores estudiados."]]
        slug, title, short, kb, ks = "estadistica-bidimensional", "Estadística bidimensional y correlación", "Estadística bidimensional", "r entre −1 y 1", "Cerca de ±1: correlación fuerte."
        meta = "Fichas de matemáticas de 4.º de ESO: tablas de doble entrada, nubes de puntos, correlación, recta de regresión y parámetros de dispersión. 100 ejercicios con soluciones."
        std = "Estadística bidimensional: tablas de doble entrada, nube de puntos, correlación y recta de regresión; medidas de dispersión; análisis crítico de estudios estadísticos"
        sort = 11
    body = L(think, ex, mist)
    faq = [("¿Qué diferencia hay entre media y mediana?", "La media reparte el total entre todos los datos; la mediana es el dato central. Si hay datos muy extremos, la mediana representa mejor al grupo."),
           ("¿Qué mide la desviación típica?", "Lo separados que están los datos de la media: cuanto mayor, más dispersos.")]
    unit(lv, R, slug, "S", std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(1)
