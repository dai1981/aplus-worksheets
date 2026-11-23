# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Muestreo y distribución de la media muestral (Sentido estocástico)
Población y muestra, tipos de muestreo (aleatorio simple, sistemático, estratificado con afijación proporcional), sesgo; distribución de la media muestral
X̄ ~ N(μ, σ/√n), teorema central del límite, probabilidades con medias muestrales; distribución de la proporción muestral.
Errores: usar σ en lugar de σ/√n, dividir entre n en lugar de √n, confundir parámetro y estadístico, repartir la muestra a partes iguales entre estratos.
"""
import math
import random
from es_ccss import M, mix, num, unit, L, W, r2, phi, dd, kurve, BLUE, RED

R = random.Random(54008)


def tz(z):
    return round(phi(round(z, 2)), 4)


def P4(x):
    return r2(x, 4)


def s_muestreo():
    t = R.choice(["estrat", "estrat", "estrat", "sistem", "sistem", "tipo", "teo", "teo"])
    if t == "estrat":
        k = R.choice([3, 4])
        Ns = [R.randrange(100, 801, 50) for _ in range(k)]
        N = sum(Ns)
        n = R.choice([40, 50, 60, 80, 100, 120])
        cuotas = [n * x / N for x in Ns]
        if any(abs(c - round(c)) > 1e-9 for c in cuotas):
            return None
        i = R.randrange(k)
        nom = ["1.º de ESO", "2.º de ESO", "3.º de ESO", "4.º de ESO"] if k == 4 else ["mañana", "tarde", "noche"]
        partes = ["%s de %s" % (num(x), nom[j]) if k == 4 else "%s en el turno de %s" % (num(x), nom[j]) for j, x in enumerate(Ns)]
        lista = ", ".join(partes[:-1]) + " y " + partes[-1]
        quien = ("Un instituto tiene %s alumnos" if k == 4 else "Una fábrica tiene %s trabajadores") % lista
        ok = int(round(cuotas[i]))
        return M("%s. Se elige una muestra de %d con muestreo estratificado proporcional. ¿Cuántos deben ser de %s?" % (quien, n, ("" if k == 4 else "el turno de ") + nom[i]),
                 str(ok), W([str(n // k), str(round(n * Ns[i] / max(Ns))), str(ok + 2), str(round(Ns[i] / 10))]),
                 "Afijación proporcional: n<sub>i</sub> = n · N<sub>i</sub>/N = %d · %s/%s = <b>%d</b>." % (n, num(Ns[i]), num(N), ok))
    if t == "sistem":
        n = R.choice([40, 50, 60, 80])
        k = R.choice([15, 20, 25, 30])
        N = n * k
        a = R.randint(1, k)
        j = R.randint(3, 9)
        ok = a + (j - 1) * k
        return M("De una lista de %s personas se quiere una muestra sistemática de %d. Se elige al azar el número %d para empezar. ¿Qué número tendrá la persona %d.ª de la muestra?" % (num(N), n, a, j), num(ok),
                 W([num(a + j * k), num(a * j), num(a + (j - 1) * n), num(ok + 1)]),
                 "Salto k = %s/%d = %d. La persona %d.ª: %d + %d · %d = <b>%s</b>." % (num(N), n, k, j, a, j - 1, k, num(ok)))
    if t == "tipo":
        q, a = R.choice([("Se numeran los 2 000 socios de un club y se eligen 100 números con un generador aleatorio.", "aleatorio simple"),
                         ("De una lista ordenada, se elige al azar uno de los 10 primeros y luego uno de cada 10.", "sistemático"),
                         ("Se divide la población por edades y se elige en cada grupo un número de personas proporcional a su tamaño.", "estratificado"),
                         ("Para saber la opinión de un barrio, se pregunta solo a los que pasan por la puerta de un gimnasio.", "no aleatorio (puede tener sesgo)"),
                         ("Se eligen al azar 5 clases de un colegio y se encuesta a todos sus alumnos.", "por conglomerados")])
        return M(q + " ¿Qué tipo de muestreo es?", a, [x for x in ("aleatorio simple", "sistemático", "estratificado", "no aleatorio (puede tener sesgo)", "por conglomerados") if x != a],
                 "Respuesta: <b>muestreo %s</b>." % a)
    q, a, w = R.choice([("La edad media de todos los votantes de una ciudad es…", "un parámetro de la población", ["un estadístico de la muestra", "una muestra", "un sesgo"]),
                        ("La nota media de 50 alumnos elegidos al azar es…", "un estadístico (calculado en la muestra)", ["un parámetro de la población", "la media de la población", "un error"]),
                        ("¿Por qué se usan muestras en lugar de estudiar a toda la población?", "porque es más barato y rápido, y a veces la población es enorme", ["porque la muestra siempre da el valor exacto", "porque así no hay error", "porque la ley lo obliga"]),
                        ("Una encuesta telefónica solo a teléfonos fijos puede tener…", "sesgo: deja fuera a quien no tiene fijo", ["más precisión", "error cero", "una muestra estratificada"]),
                        ("Al aumentar el tamaño de la muestra, la media muestral…", "se parece más, por lo general, a la media de la población", ["se aleja de la media de la población", "no cambia nunca", "es siempre igual a 0"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


PARES = [(12, 36), (10, 25), (8, 16), (15, 25), (20, 100), (6, 9), (14, 49), (9, 81), (30, 36), (18, 81), (24, 64), (5, 25)]


def s_distribucion():
    sig, n = R.choice(PARES)
    var = R.choice([("el gasto semanal en ocio", "€", 30, 90), ("el tiempo diario en redes sociales", "min", 90, 240), ("el peso de unos paquetes", "g", 200, 900),
                    ("la puntuación de un test de aptitud", "puntos", 100, 500), ("el consumo mensual de agua de los hogares", "litros", 3000, 9000)])
    mu = R.randrange(var[2], var[3] + 1, 5 if var[3] < 1000 else 100)
    if sig * 3 > mu:
        return None
    se = sig / math.sqrt(n)
    t = R.choice(["sd", "sd", "dist", "tcl", "n4"])
    if t == "sd":
        return M("%s sigue una normal de media %s %s y desviación típica %d %s. Para muestras de tamaño %d, ¿cuál es la desviación típica de la media muestral?" % (var[0].capitalize(), num(mu), var[1], sig, var[1], n), "%s %s" % (dd(se, 3), var[1]),
                 W(["%d %s" % (sig, var[1]), "%s %s" % (dd(sig / n, 3), var[1]), "%s %s" % (dd(sig * math.sqrt(n), 3), var[1]), "%s %s" % (dd(se * se, 3), var[1])]),
                 "σ/√n = %d/√%d = %d/%d = <b>%s %s</b>." % (sig, n, sig, int(math.sqrt(n)), dd(se, 3), var[1]))
    if t == "dist":
        ok = "N(%s, %s)" % (num(mu), dd(se, 3))
        return M("Una población sigue N(%s, %d). ¿Qué distribución sigue la media de las muestras de tamaño %d?" % (num(mu), sig, n), ok,
                 W(["N(%s, %d)" % (num(mu), sig), "N(%s, %s)" % (num(mu), dd(sig / n, 3)), "N(%s, %s)" % (dd(mu / n, 3), dd(se, 3)), "N(%s, %s)" % (num(mu), dd(sig * math.sqrt(n), 3))]),
                 "X̄ ~ N(μ, σ/√n) = <b>%s</b>." % ok)
    if t == "n4":
        k = R.choice([4, 9, 16, 100])
        rt = int(math.sqrt(k))
        return M("Si el tamaño de la muestra se multiplica por %d, ¿qué le pasa a la desviación típica de la media muestral?" % k, "se divide entre %d" % rt,
                 W(["se divide entre %d" % k, "se multiplica por %d" % rt, "no cambia", "se divide entre %d" % (k // 2) if k // 2 != rt else "se multiplica por %d" % k]),
                 "σ/√(%dn) = (σ/√n)/%d: <b>se divide entre %d</b>." % (k, rt, rt))
    q, a, w = R.choice([("Según el teorema central del límite, si n ≥ 30, la media muestral sigue…", "aproximadamente una normal, aunque la población no lo sea", ["siempre una binomial", "la misma distribución que la población", "una distribución uniforme"]),
                        ("¿Cuál es la media de la distribución de las medias muestrales?", "la media de la población, μ", ["μ/n", "μ/√n", "0"]),
                        ("Si la población es normal, la media muestral es normal…", "para cualquier tamaño de muestra", ["solo si n ≥ 30", "solo si n ≥ 100", "nunca"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_prob_media():
    sig, n = R.choice(PARES)
    se = sig / math.sqrt(n)
    var = R.choice([("El gasto mensual en transporte de los estudiantes", "€", 40, 120), ("El tiempo de espera en una consulta", "min", 20, 60), ("La caja diaria de los comercios de una calle", "€", 300, 1500), ("El tiempo de un trayecto", "min", 20, 90)])
    mu = R.randrange(var[2], var[3] + 1, 5 if var[3] < 1000 else 50)
    if sig * 3 > mu:
        return None
    z = R.choice([0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 0.25, 1.2, 1.4, 1.6, 1.8])
    a = mu + z * se
    if abs(a * 100 - round(a * 100)) > 1e-6:
        return None
    t = R.choice(["menor", "mayor", "entre"])
    p_ = tz(z)
    if t == "menor":
        return M("%s sigue N(%s, %d). Se toma una muestra de %d. ¿Cuál es la probabilidad de que la media muestral sea menor que %s %s?" % (var[0], num(mu), sig, n, dd(a, 2), var[1]), P4(p_),
                 W([P4(tz(z * se / sig)), P4(1 - p_), P4(tz(z / math.sqrt(n))), P4(p_ - 0.5)]),
                 "σ/√n = %s; z = (%s − %s)/%s = %s → P(Z ≤ %s) = <b>%s</b>." % (dd(se, 3), dd(a, 2), num(mu), dd(se, 3), r2(z), r2(z), P4(p_)))
    if t == "mayor":
        return M("%s sigue N(%s, %d). Se toma una muestra de %d. ¿Cuál es la probabilidad de que la media muestral supere %s %s?" % (var[0], num(mu), sig, n, dd(a, 2), var[1]), P4(1 - p_),
                 W([P4(p_), P4(1 - tz(z * se / sig)), P4(1 - tz(z / math.sqrt(n))), P4(p_ - 0.5)]),
                 "z = (%s − %s)/%s = %s → P(Z ≥ %s) = 1 − %s = <b>%s</b>." % (dd(a, 2), num(mu), dd(se, 3), r2(z), r2(z), P4(p_), P4(1 - p_)))
    b = mu - z * se
    v = 2 * p_ - 1
    return M("%s sigue N(%s, %d). Se toma una muestra de %d. ¿Cuál es la probabilidad de que la media muestral esté entre %s y %s %s?" % (var[0], num(mu), sig, n, dd(b, 2), dd(a, 2), var[1]), P4(v),
             W([P4(p_), P4(2 * tz(z * se / sig) - 1), P4(1 - p_), P4(2 * (1 - p_))]),
             "z = ±%s → P(−%s ≤ Z ≤ %s) = 2 · %s − 1 = <b>%s</b>." % (r2(z), r2(z), r2(z), P4(p_), P4(v)))


def s_proporcion():
    p = R.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 0.8])
    n = R.choice([100, 200, 300, 400, 500, 600, 1000])
    se = math.sqrt(p * (1 - p) / n)
    t = R.choice(["sd", "dist", "prob", "prob"])
    tema = R.choice(["usa el transporte público", "tiene mascota", "lee al menos un libro al mes", "hace deporte cada semana", "compra por internet"])
    if t == "sd":
        return M("El %d %% de la población %s. Para muestras de %d personas, ¿cuál es la desviación típica de la proporción muestral?" % (round(p * 100), tema, n), dd(se, 4),
                 W([dd(p * (1 - p) / n, 4), dd(math.sqrt(p / n), 4), dd(math.sqrt(p * (1 - p)), 4), dd(p * (1 - p) / math.sqrt(n), 4)]),
                 "√(p · q / n) = √(%s · %s / %d) ≈ <b>%s</b>." % (dd(p), dd(1 - p), n, dd(se, 4)))
    if t == "dist":
        ok = "N(%s; %s)" % (dd(p), dd(se, 4))
        return M("El %d %% de la población %s. ¿Qué distribución sigue, aproximadamente, la proporción muestral en muestras de %d?" % (round(p * 100), tema, n), ok,
                 W(["N(%s; %s)" % (dd(p), dd(p * (1 - p) / n, 4)), "B(%d; %s)" % (n, dd(p)), "N(%s; %s)" % (dd(p * n), dd(se, 4)), "N(%s; %s)" % (dd(p), dd(math.sqrt(p * (1 - p)), 4))]),
                 "p̂ ~ N(p, √(pq/n)) = <b>%s</b>." % ok)
    z = R.choice([0.5, 1, 1.5, 2, 1.25, 0.75])
    c = p + z * se
    c2 = round(c, 3)
    zz = (c2 - p) / se
    pz = tz(zz)
    return M("El %d %% de la población %s. En una muestra de %d personas, ¿cuál es la probabilidad de que la proporción muestral sea mayor que %s?" % (round(p * 100), tema, n, dd(c2, 3)), P4(1 - pz),
             W([P4(pz), P4(1 - tz((c2 - p) / math.sqrt(p * (1 - p)))), P4(1 - tz((c2 - p) / (p * (1 - p) / n))) if (p * (1 - p) / n) > 0.001 else P4(0.5 - pz / 2), P4(1 - pz / 2)]),
             "σ = √(%s · %s/%d) ≈ %s; z = (%s − %s)/%s ≈ %s → 1 − %s = <b>%s</b>." % (dd(p), dd(1 - p), n, dd(se, 4), dd(c2, 3), dd(p), dd(se, 4), r2(zz), P4(pz), P4(1 - pz)))


seen = set()
sets = [("Tipos de muestreo", mix(R, seen, [(s_muestreo, 20)])), ("La distribución de las medias", mix(R, seen, [(s_distribucion, 20)])), ("Probabilidades con la media muestral", mix(R, seen, [(s_prob_media, 20)])),
        ("Proporción muestral", mix(R, seen, [(s_proporcion, 20)])), ("Repaso", mix(R, seen, [(s_muestreo, 6), (s_distribucion, 4), (s_prob_media, 6), (s_proporcion, 4)]))]
think = ["La <b>población</b> es todo el grupo que se estudia; la <b>muestra</b>, la parte que se observa. Un valor de la población es un <b>parámetro</b> (μ, p); uno de la muestra, un <b>estadístico</b> (x̄, p̂).",
         "<b>Muestreo</b> aleatorio simple, sistemático (uno de cada k) o <b>estratificado</b>: en cada estrato, n<sub>i</sub> = n · N<sub>i</sub>/N (afijación proporcional).",
         "La media de las muestras de tamaño n sigue <b>X̄ ~ N(μ, σ/√n)</b>. Si la población no es normal, vale para n ≥ 30 (teorema central del límite).",
         "La proporción muestral sigue, aproximadamente, <b>p̂ ~ N(p, √(pq/n))</b> si n es grande."]
ex = [("Población N(100, 12), muestras de 36. P(X̄ ≤ 103)", ["σ/√n = 12/6 = 2", "z = (103 − 100)/2 = 1,5"], "P(Z ≤ 1,5) = 0,9332")]
mist = [["Usar σ en lugar de σ/√n", "Las medias varían menos que los datos sueltos."], ["Dividir entre n", "Se divide entre √n."], ["Repartir la muestra a partes iguales", "En el estratificado proporcional, cada estrato según su tamaño."]]
body = L(think, ex, mist, kurve([(lambda x: math.exp(-(x - 100) ** 2 / (2 * 144)) / (12 * math.sqrt(2 * math.pi)) * 300, "#90a4ae", "X"), (lambda x: math.exp(-(x - 100) ** 2 / 8) / (2 * math.sqrt(2 * math.pi)) * 300, BLUE, "X̄")],
                                (70, 130, 10), (0, 65, 10), W=330, H=220, label="los datos N(100, 12) y las medias de muestras de 36, N(100, 2)"))
faq = [("¿Qué dice el teorema central del límite?", "Que, para muestras grandes (n ≥ 30), la media muestral sigue aproximadamente una normal N(μ, σ/√n), sea cual sea la distribución de la población."),
       ("¿Qué es el muestreo estratificado?", "Se divide la población en grupos (estratos) y se elige en cada uno una parte de la muestra, normalmente proporcional a su tamaño.")]
unit(2, R, "muestreo-y-distribucion-de-medias", "S", "Muestreo: población, muestra, tipos de muestreo y sesgo; distribución de la media muestral, teorema central del límite y distribución de la proporción muestral",
     "Muestreo y distribución de medias", "Muestreo", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: tipos de muestreo, estratificado, distribución de la media muestral y de la proporción. 100 ejercicios.",
     "X̄ ~ N(μ, σ/√n)", "Las medias varían menos que los datos.", body, faq, sets, 8)
