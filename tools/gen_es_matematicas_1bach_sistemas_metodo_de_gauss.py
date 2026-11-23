# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Sistemas de ecuaciones. Método de Gauss (Sentido algebraico)
Comprobar soluciones, sistemas escalonados, método de Gauss con tres incógnitas, clasificación (compatible determinado, indeterminado, incompatible), problemas.
Errores: equivocarse de signo al restar filas, olvidar sustituir hacia arriba, confundir 0 = 0 (infinitas soluciones) con 0 = 5 (sin solución).
"""
import random
from es_bach import M, mix, sg, num, unit, L, E, eur, Kids, W

R = random.Random(51004)
K = Kids(R)
VARS = ("x", "y", "z")


def eq(cs, rhs):
    return "%s = %s" % (E(*[(c, v) for c, v in zip(cs, VARS)]), sg(rhs))


def sys_(rows):
    return "<span class='sys'>%s</span>" % "<br>".join(eq(cs, r) for cs, r in rows)


def T(x, y, z):
    return "(%s, %s, %s)" % (sg(x), sg(y), sg(z))


def rand_sol():
    return R.randint(-5, 6), R.randint(-5, 6), R.randint(-5, 6)


def make_rows(s, tri=False):
    while True:
        rows = []
        for i in range(3):
            cs = [R.randint(-3, 4) for _ in range(3)]
            if tri:
                cs = [0] * i + [R.choice([1, 1, 2, -1, 3])] + [R.randint(-3, 3) for _ in range(2 - i)]
            rows.append(cs)
        det = (rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1]) - rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0]) + rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0]))
        if det == 0 or (not tri and (sum(1 for r in rows for c in r if c == 0) > 2 or any(r[0] == 0 for r in rows[:1]))):
            continue
        if not tri and (rows[0][0] != 1 and rows[1][0] != 1 and rows[2][0] != 1):
            continue
        return [(cs, sum(c * v for c, v in zip(cs, s))) for cs in rows]


def wrong_triples(x, y, z):
    return [T(y, x, z), T(-x, y, z), T(x, -y, -z), T(x, y, z + 1), T(z, y, x)]


def s_comprobar():
    x, y, z = rand_sol()
    rows = make_rows((x, y, z))
    alts = W(wrong_triples(x, y, z))
    return M("¿Cuál es la solución del sistema? %s (comprueba las opciones)" % sys_(rows), T(x, y, z), alts, "Sustituyendo %s se cumplen las tres ecuaciones: <b>%s</b>." % (T(x, y, z), T(x, y, z)))


def s_escalonado():
    x, y, z = rand_sol()
    rows = make_rows((x, y, z), tri=True)
    return M("Resuelve el sistema escalonado: %s" % sys_(rows), T(x, y, z), W(wrong_triples(x, y, z)), "De la última ecuación sale z = %s; sustituimos hacia arriba: y = %s, x = %s. <b>%s</b>." % (sg(z), sg(y), sg(x), T(x, y, z)))


def s_gauss():
    x, y, z = rand_sol()
    rows = make_rows((x, y, z))
    rows.sort(key=lambda r: abs(r[0][0]) != 1)
    t = R.choice(["sol", "sol", "z"])
    if t == "z":
        return M("Resuelve por Gauss y da el valor de z: %s" % sys_(rows), "z = %s" % sg(z), W(["z = %s" % sg(v) for v in (x, y, -z, z + 1, z - 1) if v != z]), "Haciendo ceros bajo la diagonal y despejando: <b>z = %s</b> (x = %s, y = %s)." % (sg(z), sg(x), sg(y)))
    return M("Resuelve por el método de Gauss: %s" % sys_(rows), T(x, y, z), W(wrong_triples(x, y, z)), "Usamos la 1.ª ecuación para eliminar x en las otras, luego la 2.ª para eliminar y: <b>%s</b>." % T(x, y, z))


def s_clasificar():
    t = R.choice(["scd", "sci", "si"])
    a, b, c = R.randint(1, 3), R.randint(-3, 3), R.randint(-3, 3)
    d1, d2 = R.randint(-6, 6), R.randint(-6, 6)
    k = R.randint(1, 4)
    r3 = {"scd": "%dz = %s" % (k, sg(R.randint(-8, 8))) if k > 1 else "z = %s" % sg(R.randint(-8, 8)), "sci": "0z = 0", "si": "0z = %s" % sg(R.choice([-5, -3, -2, 2, 3, 4, 7]))}[t]
    rows = "<span class='sys'>%s<br>%s<br>%s</span>" % (eq([1, b, c], d1), eq([0, a, R.randint(-2, 3)], d2), r3)
    ok = {"scd": "compatible determinado (una solución)", "sci": "compatible indeterminado (infinitas soluciones)", "si": "incompatible (sin solución)"}[t]
    return M("Al aplicar Gauss se llega a este sistema. ¿Cómo es? %s" % rows, ok, [o for o in ["compatible determinado (una solución)", "compatible indeterminado (infinitas soluciones)", "incompatible (sin solución)", "no se puede saber"] if o != ok],
             "Mira la última ecuación: %s → <b>%s</b>." % (r3, ok))


def s_param():
    t = R.choice(["sci", "si", "teo"])
    if t == "teo":
        q, a, w = R.choice([("Si al escalonar sale la ecuación 0 = 0, el sistema…", "puede tener infinitas soluciones", ["no tiene solución", "tiene una única solución", "está mal resuelto"]),
                            ("Si al escalonar sale la ecuación 0 = 4, el sistema es…", "incompatible", ["compatible determinado", "compatible indeterminado", "homogéneo"]),
                            ("Un sistema con todas las ecuaciones igualadas a 0 se llama…", "homogéneo, y siempre tiene la solución (0, 0, 0)", ["incompatible", "triangular", "lineal sin solución"]),
                            ("¿Qué operación NO está permitida en el método de Gauss?", "multiplicar una ecuación por 0", ["intercambiar dos ecuaciones", "sumar a una ecuación otra multiplicada por un número", "multiplicar una ecuación por −2"]),
                            ("Un sistema compatible indeterminado con 3 incógnitas y 2 ecuaciones independientes depende de…", "un parámetro", ["dos parámetros", "ningún parámetro", "tres parámetros"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    a, b = R.randint(1, 4), R.randint(-5, 5)
    y0 = R.randint(-4, 4)
    # x + y + z = s ; y − z = y0 (z = λ)
    s = R.randint(-5, 8)
    ok = "x = %s − 2λ, y = %s + λ, z = λ" % (sg(s - y0), sg(y0))
    if t == "sci":
        return M("Resuelve el sistema (compatible indeterminado): <span class='sys'>x + y + z = %s<br>y − z = %s</span>" % (sg(s), sg(y0)), ok,
                 ["x = %s + 2λ, y = %s − λ, z = λ" % (sg(s - y0), sg(y0)), "x = %s, y = %s, z = 0" % (sg(s - y0), sg(y0)), "x = %s − λ, y = %s + λ, z = λ" % (sg(s), sg(y0))],
                 "z = λ → y = %s + λ → x = %s − (%s + λ) − λ = %s − 2λ. <b>%s</b>." % (sg(y0), sg(s), sg(y0), sg(s - y0), ok))
    return M("¿Qué valor de m hace incompatible el sistema? <span class='sys'>x + y = %s<br>%dx + %dy = m</span>" % (sg(b), a, a), "cualquier m ≠ %s" % sg(a * b), ["m = %s" % sg(a * b), "m = %d" % a, "ningún valor de m"],
             "La 2.ª ecuación es %d veces la 1.ª en el primer miembro: si m ≠ %s, es incompatible. <b>m ≠ %s</b>." % (a, sg(a * b), sg(a * b)))


def s_problema():
    t = R.choice(["tienda", "edades", "monedas", "examen", "mezcla"])
    if t == "tienda":
        a, b, c = R.randint(1, 6), R.randint(1, 6), R.randint(1, 6)
        q1, q2, q3 = (1, 1, 1), (2, 1, 0), (0, 1, 3)
        tot = [sum(p * v for p, v in zip(q, (a, b, c))) for q in (q1, q2, q3)]
        return M("Un bolígrafo, un cuaderno y una carpeta cuestan juntos %d €. Dos bolígrafos y un cuaderno, %d €. Un cuaderno y tres carpetas, %d €. ¿Cuánto cuesta cada cosa (bolígrafo, cuaderno, carpeta)?" % tuple(tot),
                 "%d €, %d € y %d €" % (a, b, c), W(["%d €, %d € y %d €" % v for v in ((b, a, c), (a, c, b), (c, b, a), (a + 1, b - 1, c), (a, b + 1, c - 1))]), "x + y + z = %d; 2x + y = %d; y + 3z = %d → <b>%d €, %d € y %d €</b>." % (tot[0], tot[1], tot[2], a, b, c))
    if t == "edades":
        h, m, p = R.randint(5, 15), R.randint(30, 45), R.randint(32, 48)
        return M("Entre un hijo, su madre y su padre suman %d años. La madre tiene %d años más que el hijo y el padre tiene %d años más que la madre. ¿Cuántos años tiene el hijo?" % (h + m + p, m - h, p - m) if p > m else None,
                 "%d" % h, ["%d" % m, "%d" % (h + 1), "%d" % (h - 2)], "x + y + z = %d, y = x + %d, z = y + %d → <b>%d años</b>." % (h + m + p, m - h, p - m, h)) if p > m else None
    if t == "monedas":
        a, b, c = R.randint(2, 10), R.randint(2, 10), R.randint(2, 10)
        n = a + b + c
        v = 10 * a + 20 * b + 50 * c
        return M("Una hucha tiene %d monedas de 10, 20 y 50 céntimos, que suman %s €. Hay %d monedas de 20 céntimos más que de 50. ¿Cuántas monedas hay de cada tipo (10, 20, 50)?" % (n, eur(v / 100) if False else ("%d,%02d" % divmod(v, 100)), b - c) if b > c else None,
                 "%d, %d y %d" % (a, b, c), W(["%d, %d y %d" % t_ for t_ in ((b, a, c), (c, b, a), (a + 1, b, c - 1), (a, b + 1, c - 1))]), "x + y + z = %d; 10x + 20y + 50z = %d; y = z + %d → <b>%d, %d y %d</b>." % (n, v, b - c, a, b, c)) if b > c else None
    if t == "examen":
        a, b, c = R.randint(4, 10), R.randint(4, 10), R.randint(4, 10)
        return M("En un examen tipo test hay %d preguntas de 1, 2 y 3 puntos que suman %d puntos. Hay %d preguntas más de 1 punto que de 3 puntos. ¿Cuántas hay de cada tipo (1, 2, 3 puntos)?" % (a + b + c, a + 2 * b + 3 * c, a - c) if a > c else None,
                 "%d, %d y %d" % (a, b, c), W(["%d, %d y %d" % t_ for t_ in ((c, b, a), (b, a, c), (a - 1, b + 2, c - 1), (a + 1, b - 2, c + 1))]), "x + y + z = %d; x + 2y + 3z = %d; x = z + %d → <b>%d, %d y %d</b>." % (a + b + c, a + 2 * b + 3 * c, a - c, a, b, c)) if a > c else None
    a, b = R.randint(2, 8), R.randint(2, 8)
    p1, p2 = R.choice([(4, 6), (3, 5), (5, 8), (6, 10)])
    return M("Se mezclan %d kg de café en total: uno de %d €/kg y otro de %d €/kg. La mezcla cuesta %d €. ¿Cuántos kg hay de cada café?" % (a + b, p1, p2, a * p1 + b * p2), "%d kg y %d kg" % (a, b), W(["%d kg y %d kg" % (b, a), "%d kg y %d kg" % (a + 1, b - 1), "%d kg y %d kg" % (a - 1, b + 1)]),
             "x + y = %d; %dx + %dy = %d → <b>%d kg y %d kg</b>." % (a + b, p1, p2, a * p1 + b * p2, a, b))


seen = set()
sets = [("Comprobar soluciones", mix(R, seen, [(s_comprobar, 20)])), ("Sistemas escalonados", mix(R, seen, [(s_escalonado, 20)])), ("Método de Gauss", mix(R, seen, [(s_gauss, 20)])),
        ("Clasificar sistemas", mix(R, seen, [(s_clasificar, 12), (s_param, 8)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
think = ["El <b>método de Gauss</b> transforma el sistema en uno <b>escalonado</b> (cada ecuación tiene una incógnita menos) sumando a una ecuación otra multiplicada por un número.",
         "Después se despeja de abajo arriba: primero z, luego y, luego x.",
         "Si aparece 0 = 0, el sistema es <b>compatible indeterminado</b> (infinitas soluciones, con un parámetro λ). Si aparece 0 = k (k ≠ 0), es <b>incompatible</b>."]
ex = [("x + y + z = 6; 2x − y + z = 3; x + 2y − z = 2", ["E2 − 2E1: −3y − z = −9", "E3 − E1: y − 2z = −4"], "(1, 2, 3)")]
mist = [["Restar mal los signos", "−(−y) = +y: usa paréntesis."], ["Olvidar sustituir hacia arriba", "Con z, calcula y; con y y z, calcula x."], ["Confundir 0 = 0 y 0 = 5", "0 = 0: infinitas; 0 = 5: ninguna."]]
body = L(think, ex, mist)
faq = [("¿Por qué el método de Gauss es el más usado?", "Porque funciona igual con 2, 3 o más incógnitas y sirve para saber si el sistema tiene una, infinitas o ninguna solución."),
       ("¿Qué es un parámetro?", "Una letra (λ) que toma cualquier valor; cada valor da una solución distinta del sistema indeterminado.")]
unit(1, R, "sistemas-metodo-de-gauss", "A", "Sistemas de ecuaciones lineales con tres incógnitas: método de Gauss, clasificación y resolución de problemas",
     "Sistemas de ecuaciones: método de Gauss", "Método de Gauss", "Fichas de Matemáticas I (1.º de Bachillerato): sistemas de tres ecuaciones, método de Gauss, sistemas escalonados, clasificación y problemas. 100 ejercicios con soluciones.",
     "Escalona y despeja de abajo arriba", "0 = 0: infinitas soluciones; 0 = 5: ninguna.", body, faq, sets, 4)
