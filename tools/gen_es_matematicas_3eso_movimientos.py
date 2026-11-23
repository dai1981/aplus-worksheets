# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de ESO: Movimientos en el plano (Sentido espacial)
Vectores (coordenadas y módulo), traslaciones, giros de 90° y 180° respecto al origen, simetrías axiales (ejes X, Y, y = x) y central,
reconocer el movimiento en una figura, composición de movimientos, ejes y orden de simetría, frisos y mosaicos.
Errores: restar al revés las coordenadas del vector, girar en sentido horario cuando el giro es positivo, cambiar el signo de la coordenada equivocada en la simetría.
"""
import random
from es_eso import M, mix, sg, num, unit, L, MINUS
from ws_common import text, line
from de_common import wrap

R = random.Random(49009)
BLUE, RED, GRID, INK = "#1565c0", "#c62828", "#d5dbe3", "#263238"
NOMBRE = {3: "triángulo equilátero", 4: "cuadrado", 5: "pentágono regular", 6: "hexágono regular", 8: "octógono regular", 10: "decágono regular", 12: "dodecágono regular"}


def P(x, y, n=""):
    return "%s(%s, %s)" % (n, sg(x), sg(y))


def V(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


def plano(polys, lo=-7, hi=7, u=20, label="figuras en el plano cartesiano", axis=None):
    n = hi - lo
    W = H = n * u + 40
    X = lambda x: 20 + (x - lo) * u
    Y = lambda y: 20 + (hi - y) * u
    s = []
    for i in range(lo, hi + 1):
        s.append(line(X(i), Y(lo), X(i), Y(hi), GRID, 1) + line(X(lo), Y(i), X(hi), Y(i), GRID, 1))
    s.append(line(X(lo), Y(0), X(hi) + 6, Y(0), INK, 2) + line(X(0), Y(lo), X(0), Y(hi) - 6, INK, 2))
    s.append(text(X(hi) + 4, Y(0) - 7, "x", 15, italic=True) + text(X(0) + 10, Y(hi) - 2, "y", 15, italic=True))
    for i in (lo + 1, hi - 1):
        s.append(text(X(i), Y(0) + 16, sg(i), 12) + text(X(0) - 6, Y(i) + 4, sg(i), 12, anchor="end"))
    if axis == "y=x":
        s.append(line(X(lo), Y(lo), X(hi), Y(hi), "#6a1b9a", 2))
    for pts, col, lab in polys:
        s.append("<polygon points='%s' fill='%s' fill-opacity='0.18' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in pts), col, col))
        if lab:
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            s.append(text(X(cx), Y(cy) + 5, lab, 15, col=col, weight=700))
    return wrap(W, H, "".join(s), label, lg=True)


MOV = {
    "sx": ("simetría respecto al eje X", lambda x, y: (x, -y)),
    "sy": ("simetría respecto al eje Y", lambda x, y: (-x, y)),
    "sd": ("simetría respecto a la recta y = x", lambda x, y: (y, x)),
    "c": ("simetría central respecto al origen (giro de 180°)", lambda x, y: (-x, -y)),
    "g90": ("giro de 90° respecto al origen (sentido antihorario)", lambda x, y: (-y, x)),
    "g270": ("giro de −90° respecto al origen (sentido horario)", lambda x, y: (y, -x)),
}


def s_vector():
    t = R.choice(["coord", "coord", "modulo", "extremo"])
    x1, y1 = R.randint(-8, 8), R.randint(-8, 8)
    if t == "modulo":
        a, b = R.choice([(3, 4), (6, 8), (5, 12), (8, 6), (4, 3), (12, 5), (0, 7), (9, 12), (8, 15)])
        a, b = a * R.choice([1, -1]), b * R.choice([1, -1])
        m = int((a * a + b * b) ** 0.5)
        return M("¿Cuál es el módulo del vector %s?" % V(a, b), num(m), [num(abs(a) + abs(b)), num(a * a + b * b), num(abs(abs(a) - abs(b)))], "|v| = √(%s² + %s²) = √%d = <b>%d</b>." % (sg(a), sg(b), a * a + b * b, m))
    a, b = R.randint(-7, 7), R.randint(-7, 7)
    if a == 0 and b == 0:
        return None
    x2, y2 = x1 + a, y1 + b
    if t == "coord":
        return M("¿Cuáles son las coordenadas del vector AB, con %s y %s?" % (P(x1, y1, "A"), P(x2, y2, "B")), V(a, b), [V(-a, -b), V(x1 + x2, y1 + y2), V(b, a) if a != b else V(a, -b), V(a + 1, b), V(a, b - 1)],
                 "Extremo menos origen: (%s − %s, %s − %s) = <b>%s</b>." % (sg(x2), "(%s)" % sg(x1) if x1 < 0 else sg(x1), sg(y2), "(%s)" % sg(y1) if y1 < 0 else sg(y1), V(a, b)))
    return M("El vector AB es %s y el origen es %s. ¿Cuál es el extremo B?" % (V(a, b), P(x1, y1, "A")), P(x2, y2, "B"), [P(x1 - a, y1 - b, "B"), P(a - x1, b - y1, "B"), P(x1 + b, y1 + a, "B")], "B = A + AB = <b>%s</b>." % P(x2, y2, "B"))


def s_traslacion():
    x, y = R.randint(-7, 7), R.randint(-7, 7)
    a, b = R.randint(-6, 6), R.randint(-6, 6)
    if a == 0 or b == 0:
        return None
    t = R.choice(["img", "img", "orig", "vec"])
    if t == "img":
        return M("Aplicamos al punto %s la traslación de vector %s. ¿Cuál es el punto imagen?" % (P(x, y, "P"), V(a, b)), P(x + a, y + b, "P′"), [P(x - a, y - b, "P′"), P(x + b, y + a, "P′"), P(x * a, y * b, "P′") if (x * a, y * b) != (x + a, y + b) else P(a, b, "P′"), P(x + a, y - b, "P′"), P(x - a, y + b, "P′")],
                 "Sumamos el vector: (%s + %s, %s + %s) = <b>%s</b>." % (sg(x), "(%s)" % sg(a) if a < 0 else sg(a), sg(y), "(%s)" % sg(b) if b < 0 else sg(b), P(x + a, y + b, "P′")))
    if t == "orig":
        return M("Con la traslación de vector %s, la imagen de P es %s. ¿Cuál es P?" % (V(a, b), P(x + a, y + b, "P′")), P(x, y, "P"), [P(x + 2 * a, y + 2 * b, "P"), P(x + a - b, y + b - a, "P") if a != b else P(-x, -y, "P"), P(-x, y, "P") if x else P(y, x, "P")],
                 "Restamos el vector: <b>%s</b>." % P(x, y, "P"))
    return M("Una traslación lleva %s a %s. ¿Cuál es el vector de la traslación?" % (P(x, y, "A"), P(x + a, y + b, "A′")), V(a, b), [V(-a, -b), V(2 * x + a, 2 * y + b), V(b, a) if a != b else V(a, -b), V(a + 1, b), V(a, b - 1)], "A′ − A = <b>%s</b>." % V(a, b))


def s_giro_sim():
    k = R.choice(list(MOV))
    nm, f = MOV[k]
    x, y = R.randint(-8, 8), R.randint(-8, 8)
    if x == 0 or y == 0 or abs(x) == abs(y):
        return None
    ok = P(*f(x, y), n="P′")
    w = [P(*MOV[j][1](x, y), n="P′") for j in MOV if j != k]
    R.shuffle(w)
    rule = {"sx": "(x, y) → (x, −y)", "sy": "(x, y) → (−x, y)", "sd": "(x, y) → (y, x)", "c": "(x, y) → (−x, −y)", "g90": "(x, y) → (−y, x)", "g270": "(x, y) → (y, −x)"}[k]
    return M("Halla la imagen de %s por una %s." % (P(x, y, "P"), nm), ok, w, "%s: <b>%s</b>." % (rule.replace("−", MINUS), ok))


def tri():
    while True:
        pts = [(R.randint(1, 6), R.randint(1, 6)) for _ in range(3)]
        (ax, ay), (bx, by), (cx, cy) = pts
        area = (bx - ax) * (cy - ay) - (cx - ax) * (by - ay)
        ds = sorted([(ax - bx) ** 2 + (ay - by) ** 2, (bx - cx) ** 2 + (by - cy) ** 2, (ax - cx) ** 2 + (ay - cy) ** 2])
        if abs(area) >= 4 and len(set(ds)) == 3:
            q = R.choice([(1, 1), (-1, 1), (-1, -1), (1, -1)])
            return [(x * q[0], y * q[1]) for x, y in pts]


def s_reconocer():
    pts = tri()
    k = R.choice(list(MOV) + ["t", "t"])
    if k == "t":
        a, b = R.choice([-5, -4, -3, 3, 4, 5]), R.choice([-5, -4, -3, 3, 4, 5])
        img = [(x + a, y + b) for x, y in pts]
        if any(abs(c) > 7 for p in img for c in p):
            return None
        ok = "traslación de vector %s" % V(a, b)
        w = ["traslación de vector %s" % V(-a, -b), MOV["sy"][0], MOV["g90"][0]]
    else:
        nm, f = MOV[k]
        img = [f(x, y) for x, y in pts]
        if sorted(img) == sorted(pts):
            return None
        ok = nm
        others = [MOV[j][0] for j in MOV if j != k and sorted(MOV[j][1](x, y) for x, y in pts) != sorted(img)]
        R.shuffle(others)
        w = others[:3]
    pic = plano([(pts, BLUE, "F"), (img, RED, "F′")], axis="y=x" if k == "sd" else None)
    return M(pic + "¿Qué movimiento transforma la figura azul F en la roja F′? (vértice %s → %s)" % (V(*pts[0]), V(*img[0])), ok, w, "Comprueba con un vértice: %s → %s. <b>%s</b>." % (V(*pts[0]), V(*img[0]), ok))


def s_compuesto():
    t = R.choice(["dos", "dos", "teoria"])
    if t == "teoria":
        q, a, w = R.choice([("¿Qué se obtiene al componer dos simetrías de ejes paralelos?", "una traslación", ["un giro", "otra simetría", "la figura deformada"]),
                            ("¿Qué se obtiene al componer dos simetrías de ejes que se cortan?", "un giro", ["una traslación", "otra simetría axial", "una homotecia"]),
                            ("¿Qué propiedad conservan todos los movimientos?", "las distancias y los ángulos", ["solo las distancias", "solo la posición", "la orientación siempre"]),
                            ("¿Qué movimiento cambia la orientación de la figura (la «da la vuelta»)?", "la simetría axial", ["la traslación", "el giro", "la simetría central"]),
                            ("¿Qué se obtiene al componer dos traslaciones?", "otra traslación", ["un giro", "una simetría", "nada"]),
                            ("Un giro de 180° respecto a un punto es lo mismo que…", "una simetría central respecto a ese punto", ["una simetría axial", "una traslación", "un giro de 90°"]),
                            ("¿Qué se obtiene al componer dos giros de 90° con el mismo centro?", "un giro de 180°", ["un giro de 90°", "una traslación", "una simetría axial"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    if x == 0 or y == 0:
        return None
    a, b = R.randint(-4, 4), R.randint(-4, 4)
    if a == 0 or b == 0:
        return None
    k = R.choice(["sx", "sy", "c", "g90"])
    nm, f = MOV[k]
    order = R.random() < 0.5
    if order:
        r = f(x + a, y + b)
        alt = (f(x, y)[0] + a, f(x, y)[1] + b)
        q = "Al punto %s le aplicamos primero la traslación de vector %s y después la %s. ¿Dónde acaba?" % (P(x, y, "P"), V(a, b), nm)
        e = "Traslación: %s. %s: <b>%s</b>." % (P(x + a, y + b), nm[0].upper() + nm[1:], P(*r))
    else:
        r0 = f(x, y)
        r = (r0[0] + a, r0[1] + b)
        alt = f(x + a, y + b)
        q = "Al punto %s le aplicamos primero la %s y después la traslación de vector %s. ¿Dónde acaba?" % (P(x, y, "P"), nm, V(a, b))
        e = "%s: %s. Traslación: <b>%s</b>." % (nm[0].upper() + nm[1:], P(*r0), P(*r))
    if alt == r:
        return None
    return M(q, P(*r), [P(*alt), P(x + a, y + b), P(*f(x, y))], e)


def s_simetrias_figuras():
    t = R.choice(["ejes", "orden", "angulo", "letra", "friso"])
    n = R.choice(list(NOMBRE))
    if t == "ejes":
        return M("¿Cuántos ejes de simetría tiene un %s?" % NOMBRE[n], num(n), [num(n // 2) if n > 3 else "1", num(2 * n), num(n - 1)], "Un polígono regular de %d lados tiene <b>%d</b> ejes de simetría." % (n, n))
    if t == "orden":
        return M("¿Cuántas veces coincide un %s consigo mismo al dar una vuelta completa alrededor de su centro?" % NOMBRE[n], num(n), [num(n // 2) if n > 3 else "1", num(2 * n), num(360 // n)], "Coincide cada %d°: <b>%d</b> veces." % (360 // n, n))
    if t == "angulo":
        return M("¿Cuál es el menor ángulo de giro que deja igual a un %s?" % NOMBRE[n], "%d°" % (360 // n), ["%d°" % (180 // n) if 180 % n == 0 else "%d°" % (360 // n + 10), "%d°" % (180 * (n - 2) // n), "%d°" % n, "%d°" % (720 // n)], "360° : %d = <b>%d°</b>." % (n, 360 // n))
    if t == "letra":
        q, a, w = R.choice([("¿Qué letra tiene un eje de simetría vertical?", "A", ["F", "G", "J"]), ("¿Qué letra tiene un eje de simetría horizontal?", "E", ["F", "G", "N"]),
                            ("¿Qué letra tiene centro de simetría (queda igual al girarla 180°)?", "S", ["E", "A", "C"]), ("¿Qué letra tiene dos ejes de simetría?", "H", ["A", "E", "M"]),
                            ("¿Qué letra no tiene ningún eje de simetría?", "F", ["A", "H", "O"]), ("¿Qué letra tiene centro de simetría pero ningún eje?", "N", ["H", "O", "A"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    q, a, w = R.choice([("¿Qué movimiento genera un friso?", "una traslación que se repite", ["un único giro", "una homotecia", "una simetría central sola"]),
                        ("¿Con qué polígonos regulares iguales se puede hacer un mosaico regular?", "triángulos, cuadrados y hexágonos", ["pentágonos", "octógonos", "cualquier polígono regular"]),
                        ("¿Cuánto deben sumar los ángulos que coinciden en un vértice de un mosaico?", "360°", ["180°", "90°", "270°"]),
                        ("¿Por qué no se puede hacer un mosaico regular solo con pentágonos regulares?", "porque 108° no divide a 360°", ["porque tienen 5 lados", "porque son muy grandes", "porque no tienen ejes de simetría"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Vectores", mix(R, seen, [(s_vector, 20)])), ("Traslaciones", mix(R, seen, [(s_traslacion, 20)])), ("Giros y simetrías", mix(R, seen, [(s_giro_sim, 20)])),
        ("Reconocer movimientos", mix(R, seen, [(s_reconocer, 20)])), ("Composición y simetrías de figuras", mix(R, seen, [(s_compuesto, 10), (s_simetrias_figuras, 10)]))]
think = ["Un <b>movimiento</b> cambia la posición de una figura sin cambiar su forma ni su tamaño.",
         "El <b>vector</b> AB = (x<sub>B</sub> − x<sub>A</sub>, y<sub>B</sub> − y<sub>A</sub>). Una <b>traslación</b> suma el vector a cada punto.",
         "Giros respecto al origen: 90° (antihorario): (x, y) → (−y, x); 180°: (x, y) → (−x, −y).",
         "Simetrías: eje X: (x, −y); eje Y: (−x, y); recta y = x: (y, x)."]
ex = [("P(2, 5) por la traslación de vector (−3, 1)", ["(2 − 3, 5 + 1)"], "P′(−1, 6)"), ("P(2, 5) girado 90°", ["(x, y) → (−y, x)"], "P′(−5, 2)")]
mist = [["Restar al revés en el vector", "Siempre extremo menos origen."], ["Girar en sentido horario", "Un giro positivo va en sentido antihorario."], ["Cambiar el signo equivocado", "Simetría respecto al eje X: cambia la y."]]
p0 = [(1, 1), (5, 2), (2, 4)]
body = L(think, ex, mist, plano([(p0, BLUE, "F"), ([(-y, x) for x, y in p0], RED, "F′")], label="giro de 90° respecto al origen"))
faq = [("¿Qué diferencia hay entre simetría central y axial?", "La central es respecto a un punto (equivale a un giro de 180°); la axial es respecto a una recta y da la vuelta a la figura."),
       ("¿Dónde se ven los movimientos en la vida real?", "En frisos, mosaicos, azulejos (como los de la Alhambra), logotipos y en el movimiento de las agujas del reloj.")]
unit(3, R, "movimientos-en-el-plano", "E", "Movimientos en el plano: vectores, traslaciones, giros y simetrías; composición de movimientos; frisos y mosaicos; uso de coordenadas",
     "Movimientos en el plano", "Movimientos", "Fichas de matemáticas de 3.º de ESO: vectores, traslaciones, giros, simetrías, composición de movimientos, frisos y mosaicos. 100 ejercicios con soluciones.",
     "Movimientos: misma forma y tamaño", "Traslación, giro y simetría.", body, faq, sets, 9)
