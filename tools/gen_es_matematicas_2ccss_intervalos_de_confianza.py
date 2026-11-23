# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Intervalos de confianza (Sentido estocástico)
Nivel de confianza y valor crítico z_α/2, intervalo de confianza para la media (σ conocida), error máximo admisible, tamaño de la muestra,
intervalo para una proporción, interpretación (centro, amplitud, efecto de n y del nivel).
Errores: usar σ en lugar de σ/√n, tomar z = 1,645 para el 95 %, redondear hacia abajo el tamaño de la muestra, creer que más confianza da un intervalo más estrecho.
"""
import math
import random
from es_ccss import M, mix, num, unit, L, W, r2, dd, tabla

R = random.Random(54009)
ZC = [("80 %", 1.28), ("90 %", 1.645), ("95 %", 1.96), ("98 %", 2.33), ("99 %", 2.575)]


def zs(z):
    return dd(z, 3)


def fx(x, k=2):
    """k decimales fijos, coma"""
    m = 10 ** k
    v = int(math.floor(abs(x) * m + 0.5))
    e, f = divmod(v, m)
    return ("−" if x < 0 and v else "") + num(e) + ("," + str(f).rjust(k, "0") if k else "")


def rd(x, k=2):
    return math.floor(x * 10 ** k + 0.5) / 10 ** k


def ivl(a, b, k=2):
    return "(%s; %s)" % (fx(a, k), fx(b, k))


def s_critico():
    t = R.choice(["z", "z", "nivel", "alfa"])
    i = R.randrange(len(ZC))
    lv, z = ZC[i]
    if t == "z":
        return M("¿Cuál es el valor crítico z<sub>α/2</sub> para un nivel de confianza del %s?" % lv, zs(z), W([zs(v) for k, v in ZC if v != z]),
                 "Se busca z con P(−z ≤ Z ≤ z) = %s, es decir, P(Z ≤ z) = %s: <b>z = %s</b>." % (lv, dd(0.5 + float(lv[:-2]) / 200, 4), zs(z)))
    if t == "nivel":
        return M("Si z<sub>α/2</sub> = %s, ¿cuál es el nivel de confianza?" % zs(z), lv, W([k for k, v in ZC if v != z]), "P(−%s ≤ Z ≤ %s) ≈ %s: nivel del <b>%s</b>." % (zs(z), zs(z), dd(float(lv[:-2]) / 100), lv))
    a = 100 - float(lv[:-2])
    return M("Para un nivel de confianza del %s, ¿cuánto vale α y qué probabilidad deja z<sub>α/2</sub> a su derecha?" % lv, "α = %s; %s" % (dd(a / 100), dd(a / 200, 3)),
             W(["α = %s; %s" % (dd(a / 100), dd(a / 100)), "α = %s; %s" % (dd(1 - a / 100), dd(a / 200, 3)), "α = %s; %s" % (dd(a / 200, 3), dd(a / 100))]),
             "α = 1 − %s = %s; a cada lado queda α/2 = <b>%s</b>." % (dd(1 - a / 100), dd(a / 100), dd(a / 200, 3)))


PARES = [(12, 36), (10, 25), (8, 16), (15, 25), (20, 100), (6, 9), (14, 49), (9, 81), (30, 36), (18, 81), (24, 64), (5, 25), (16, 64), (21, 49), (40, 100)]
VARS = [("el gasto mensual en ocio de los jóvenes de una ciudad", "€", 40, 150), ("el tiempo diario de estudio de los alumnos de Bachillerato", "min", 60, 180),
        ("la duración de las llamadas a un servicio de atención", "s", 120, 400), ("el precio del alquiler por m² en un barrio", "€", 8, 20),
        ("las horas semanales de teletrabajo", "h", 6, 20), ("el gasto en la compra semanal de las familias", "€", 80, 200)]


def datos():
    sig, n = R.choice(PARES)
    v = R.choice(VARS)
    x = R.randrange(v[2], v[3] + 1)
    if sig > x / 2 and v[3] > 30:
        return None
    if v[3] <= 30:
        sig, n = R.choice([(2, 25), (3, 36), (4, 64), (5, 100), (2, 16), (3, 81)])
    lv, z = R.choice(ZC[1:])
    return sig, n, v, x, lv, z


def s_ic_media():
    r = datos()
    if not r:
        return None
    sig, n, v, x, lv, z = r
    E = rd(z * sig / math.sqrt(n))
    ok = ivl(x - E, x + E)
    zw = [w for k, w in ZC if w != z][R.randrange(4)]
    return M("X = %s sigue una normal con σ = %d %s. Una muestra de %d da x̄ = %d %s. Halla el intervalo de confianza para la media de X al %s." % (v[0], sig, v[1], n, x, v[1], lv), ok,
             W([ivl(x - z * sig, x + z * sig), ivl(x - z * sig / n, x + z * sig / n), ivl(x - zw * sig / math.sqrt(n), x + zw * sig / math.sqrt(n)), ivl(x - sig / math.sqrt(n), x + sig / math.sqrt(n))]),
             "E = z<sub>α/2</sub> · σ/√n = %s · %d/%d ≈ %s. Intervalo: %d ± %s = <b>%s</b>." % (zs(z), sig, int(math.sqrt(n)), fx(E), x, fx(E), ok))


def s_error():
    t = R.choice(["E", "E", "n4", "nivel", "desde"])
    if t in ("E", "desde"):
        r = datos()
        if not r:
            return None
        sig, n, v, x, lv, z = r
        E = rd(z * sig / math.sqrt(n))
        if t == "E":
            return M("Con σ = %d %s y una muestra de %d, ¿cuál es el error máximo admisible al %s?" % (sig, v[1], n, lv), "%s %s" % (fx(E), v[1]),
                     W(["%s %s" % (fx(z * sig), v[1]), "%s %s" % (fx(z * sig / n), v[1]), "%s %s" % (fx(sig / math.sqrt(n)), v[1]), "%s %s" % (fx(2 * E), v[1])]),
                     "E = %s · %d/√%d ≈ <b>%s %s</b>." % (zs(z), sig, n, fx(E), v[1]))
        a, b = x - E, x + E
        return M("Para X = %s, el intervalo de confianza para la media es %s. ¿Cuáles son la media muestral y el error?" % (v[0], ivl(a, b)), "x̄ = %s; E = %s" % (r2(x), fx(E)),
                 W(["x̄ = %s; E = %s" % (r2(x), fx(2 * E)), "x̄ = %s; E = %s" % (fx(b - a), fx(E)), "x̄ = %s; E = %s" % (fx(a), fx(b - a))]),
                 "Centro: (%s + %s)/2 = %s; error: la mitad de la amplitud, (%s − %s)/2 = <b>%s</b>." % (fx(a), fx(b), r2(x), fx(b), fx(a), fx(E)))
    if t == "n4":
        k = R.choice([4, 9, 16, 25])
        rt = int(math.sqrt(k))
        return M("Si el tamaño de la muestra se multiplica por %d (con el mismo nivel de confianza), ¿qué le pasa al error?" % k, "se divide entre %d" % rt,
                 W(["se divide entre %d" % k, "se multiplica por %d" % rt, "no cambia", "se multiplica por %d" % k]), "E = z · σ/√n: si n se multiplica por %d, √n se multiplica por %d. <b>Se divide entre %d</b>." % (k, rt, rt))
    q, a, w = R.choice([("Con la misma muestra, si se pasa del 90 % al 99 % de confianza, el intervalo…", "se hace más ancho", ["se hace más estrecho", "no cambia", "se desplaza a la derecha"]),
                        ("¿Qué significa un intervalo de confianza al 95 %?", "que el 95 % de los intervalos construidos así contienen la media de la población", ["que el 95 % de los datos están dentro", "que la media muestral está dentro con probabilidad 0,95", "que hay un 5 % de error en cada dato"]),
                        ("Para reducir el error sin perder confianza, hay que…", "aumentar el tamaño de la muestra", ["reducir el tamaño de la muestra", "bajar el nivel de confianza", "aumentar σ"]),
                        ("¿Dónde está siempre el centro del intervalo de confianza para la media?", "en la media muestral x̄", ["en μ", "en 0", "en z<sub>α/2</sub>"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_tamano():
    sig = R.choice([5, 6, 8, 10, 12, 15, 20, 25, 30])
    E = R.choice([1, 1.5, 2, 2.5, 3, 4, 5])
    if E >= sig:
        return None
    lv, z = R.choice(ZC[1:])
    v = (z * sig / E) ** 2
    ok = math.ceil(v - 1e-9)
    if ok == v:
        return None
    var = R.choice(["el gasto medio en libros", "el tiempo medio de desplazamiento al trabajo", "la estatura media de los alumnos", "el tiempo medio de sueño (en minutos)"])
    return M("Se quiere estimar %s con un error menor que %s y un nivel de confianza del %s. Si σ = %d, ¿qué tamaño mínimo debe tener la muestra?" % (var, r2(E), lv, sig), num(ok),
             W([num(math.floor(v)), num(math.ceil(z * sig / E)), num(math.ceil((sig / E) ** 2)), num(math.ceil((ZC[1][1] if z != ZC[1][1] else ZC[2][1]) ** 2 * sig ** 2 / E ** 2))]),
             "n ≥ (z<sub>α/2</sub> · σ/E)² = (%s · %d/%s)² ≈ %s → <b>n = %s</b> (se redondea hacia arriba)." % (zs(z), sig, r2(E), r2(v), num(ok)))


def s_proporcion():
    n = R.choice([100, 200, 250, 400, 500, 625, 800, 1000])
    k = R.randrange(int(n * 0.1), int(n * 0.9))
    p = k / n
    lv, z = R.choice(ZC[1:])
    tema = R.choice(["están a favor de ampliar el carril bici", "usan el transporte público a diario", "han comprado por internet este mes", "piensan votar en las próximas elecciones municipales",
                     "leen la prensa digital", "practican deporte cada semana"])
    t = R.choice(["ic", "ic", "ic", "E"])
    E = rd(z * math.sqrt(p * (1 - p) / n), 3)
    if t == "ic":
        ok = ivl(p - E, p + E, 3)
        return M("En una encuesta a %s personas, %s %s. Halla el intervalo de confianza al %s para la proporción de la población." % (num(n), num(k), tema, lv), ok,
                 W([ivl(p - z * math.sqrt(p * (1 - p)), p + z * math.sqrt(p * (1 - p)), 3) if p - z * math.sqrt(p * (1 - p)) > 0 else ivl(p - E / 2, p + E / 2, 3),
                    ivl(p - z * p * (1 - p) / n, p + z * p * (1 - p) / n, 3), ivl(p - z * math.sqrt(p / n), p + z * math.sqrt(p / n), 3), ivl(p - 2 * E, p + 2 * E, 3)]),
                 "p̂ = %s/%s = %s; E = %s · √(%s · %s/%s) ≈ %s → <b>%s</b>." % (num(k), num(n), dd(p, 3), zs(z), dd(p, 3), dd(1 - p, 3), num(n), fx(E, 3), ok))
    return M("En una encuesta a %s personas, %s %s. ¿Cuál es el error máximo al estimar la proporción con un nivel del %s?" % (num(n), num(k), tema, lv), fx(E, 3),
             W([fx(z * p * (1 - p) / n, 3), fx(z * math.sqrt(p * (1 - p)), 3), fx(math.sqrt(p * (1 - p) / n), 3), fx(2 * E, 3)]),
             "E = z<sub>α/2</sub> · √(p̂ q̂ / n) = %s · √(%s · %s/%s) ≈ <b>%s</b>." % (zs(z), dd(p, 3), dd(1 - p, 3), num(n), fx(E, 3)))


seen = set()
sets = [("Nivel de confianza y valor crítico", mix(R, seen, [(s_critico, 12), (s_error, 8)])), ("Intervalo para la media", mix(R, seen, [(s_ic_media, 20)])), ("Error máximo admisible", mix(R, seen, [(s_error, 20)])),
        ("Tamaño de la muestra", mix(R, seen, [(s_tamano, 20)])), ("Intervalo para una proporción", mix(R, seen, [(s_proporcion, 20)]))]
think = ["Un <b>intervalo de confianza</b> da un rango de valores en el que, con un nivel de confianza 1 − α, está el parámetro de la población.",
         "<b>Valores críticos</b>: 90 % → z<sub>α/2</sub> = 1,645; 95 % → 1,96; 99 % → 2,575.",
         "Para la media (σ conocida): (x̄ − E, x̄ + E), con <b>E = z<sub>α/2</sub> · σ/√n</b>. Para una proporción: p̂ ± z<sub>α/2</sub> · √(p̂ q̂ / n).",
         "<b>Tamaño de la muestra</b>: n ≥ (z<sub>α/2</sub> · σ/E)², redondeando siempre hacia arriba. Más confianza → intervalo más ancho; más muestra → más estrecho."]
ex = [("x̄ = 50, σ = 12, n = 36, 95 %", ["E = 1,96 · 12/6 = 3,92"], "(46,08; 53,92)"), ("σ = 10, E &lt; 2, 95 %", ["n ≥ (1,96 · 10/2)² = 96,04"], "n = 97")]
mist = [["Usar σ en lugar de σ/√n", "El error depende de la muestra: se divide entre √n."], ["Tomar 1,645 para el 95 %", "1,645 es para el 90 %; para el 95 %, 1,96."],
        ["Redondear n hacia abajo", "Con 96 no se llega: hace falta 97."]]
body = L(think, ex, mist, tabla(["Nivel de confianza", "α", "z<sub>α/2</sub>"], [["90 %", "0,10", "1,645"], ["95 %", "0,05", "1,96"], ["99 %", "0,01", "2,575"]]))
faq = [("¿Por qué un intervalo y no un solo número?", "Porque la media de una muestra casi nunca coincide con la de la población. El intervalo da un margen y dice cuánta confianza tenemos en él."),
       ("¿Cómo se consigue un intervalo más estrecho?", "Tomando una muestra más grande (el error baja con √n) o aceptando un nivel de confianza menor.")]
unit(2, R, "intervalos-de-confianza", "S", "Inferencia estadística: nivel de confianza, valor crítico, intervalos de confianza para la media y para la proporción, error máximo admisible y tamaño de la muestra",
     "Intervalos de confianza", "Intervalos de confianza", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: valor crítico, intervalos para la media y la proporción, error y tamaño de la muestra. 100 ejercicios.",
     "E = z · σ / √n", "Tamaño de la muestra: redondea hacia arriba.", body, faq, sets, 9)
