# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Coordenadas y movimientos en el plano (Sentido espacial)
Ejes de coordenadas, coordenadas de un punto (5.º: primer cuadrante; 6.º: los cuatro cuadrantes), traslaciones, simetrías
respecto a un eje y giros de 90° y 180°; ampliaciones y reducciones (semejanza).
Errores: cambiar el orden de las coordenadas, olvidar el signo en los cuadrantes negativos, trasladar en la dirección contraria.
"""
import random
from es_c3 import M, mix, lesson, make_unit, sg

R = None
LV = 6
C = 24


def lim():
    return (-5, 5) if LV == 6 else (0, 8)


def plano(points, poly=None, poly2=None, axis=None):
    lo, hi = lim()
    n = hi - lo
    ox = 26 - lo * C
    oy = 16 + hi * C
    X = lambda x: ox + x * C
    Y = lambda y: oy - y * C
    s = []
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#d6e4ee'/>" % (X(v), Y(lo), X(v), Y(hi)))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#d6e4ee'/>" % (X(lo), Y(v), X(hi), Y(v)))
        if v:
            s.append("<text x='%d' y='%d' font-size='10' text-anchor='middle' fill='#555'>%s</text>" % (X(v), Y(0) + 13 if lo < 0 else Y(lo) + 13, sg(v)))
            s.append("<text x='%d' y='%d' font-size='10' text-anchor='end' fill='#555'>%s</text>" % (X(0) - 4 if lo < 0 else X(lo) - 4, Y(v) + 4, sg(v)))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#333' stroke-width='1.6'/>" % (X(lo), Y(max(lo, 0)), X(hi), Y(max(lo, 0))))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#333' stroke-width='1.6'/>" % (X(max(lo, 0)), Y(lo), X(max(lo, 0)), Y(hi)))
    if axis:
        if axis[0] == "v":
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c0392b' stroke-width='2.5' stroke-dasharray='6 4'/>" % (X(axis[1]), Y(lo), X(axis[1]), Y(hi)))
        else:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c0392b' stroke-width='2.5' stroke-dasharray='6 4'/>" % (X(lo), Y(axis[1]), X(hi), Y(axis[1])))
    for pl, col in ((poly, "#9fd3a8"), (poly2, "#f6d8b8")):
        if pl:
            s.append("<polygon points='%s' fill='%s' fill-opacity='0.8' stroke='#333' stroke-width='1.5'/>" % (" ".join("%d,%d" % (X(x), Y(y)) for x, y in pl), col))
    for x, y, nm in points:
        s.append("<circle cx='%d' cy='%d' r='4.5' fill='#1f5fbf'/><text x='%d' y='%d' font-size='13' font-weight='700' fill='#1f5fbf'>%s</text>" % (X(x), Y(y), X(x) + 5, Y(y) - 5, nm))
    W, H = X(hi) + 14, Y(lo) + 22
    return "<div class='fig'><svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='ejes de coordenadas'>%s</svg></div>" % (W, H, W, "".join(s))


def P(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


def rp():
    lo, hi = lim()
    return R.randint(lo if lo else 1, hi), R.randint(lo if lo else 1, hi)


def s1_leer():
    pts = []
    while len(pts) < 4:
        x, y = rp()
        if (x, y) in [(a, b) for a, b, _ in pts] or x == 0 or y == 0:
            continue
        pts.append((x, y, "ABCD"[len(pts)]))
    i = R.randrange(4)
    x, y, nm = pts[i]
    if R.random() < 0.6:
        return M(plano(pts) + "¿Cuáles son las coordenadas del punto %s?" % nm, P(x, y), [P(y, x) if x != y else P(x + 1, y), P(-x, y) if LV == 6 else P(x + 1, y), P(x, -y) if LV == 6 else P(x, y + 1), P(pts[(i + 1) % 4][0], pts[(i + 1) % 4][1])],
                 "Primero el eje horizontal (%s) y después el vertical (%s): <b>%s</b>." % (sg(x), sg(y), P(x, y)))
    return M(plano(pts) + "¿Qué punto tiene las coordenadas %s?" % P(x, y), nm, [p[2] for p in pts], "%s a la derecha/izquierda y %s arriba/abajo: el punto <b>%s</b>." % (sg(x), sg(y), nm))


def s2_cuadrante():
    x, y = R.choice([-1, 1]) * R.randint(1, 9), R.choice([-1, 1]) * R.randint(1, 9)
    q = {(1, 1): "primer", (-1, 1): "segundo", (-1, -1): "tercer", (1, -1): "cuarto"}[(1 if x > 0 else -1, 1 if y > 0 else -1)]
    return M("¿En qué cuadrante está el punto %s?" % P(x, y), "en el %s cuadrante" % q, ["en el %s cuadrante" % c for c in ("primer", "segundo", "tercer", "cuarto") if c != q],
             "x %s 0 e y %s 0: <b>%s cuadrante</b>." % ("&gt;" if x > 0 else "&lt;", "&gt;" if y > 0 else "&lt;", q))


def s3_traslacion():
    x, y = rp()
    lo, hi = lim()
    dx, dy = R.choice([-3, -2, -1, 1, 2, 3, 4]), R.choice([-3, -2, -1, 1, 2, 3])
    nx, ny = x + dx, y + dy
    if not (lo <= nx <= hi and lo <= ny <= hi) or (LV == 5 and (nx < 1 or ny < 1)):
        return None
    h = "%d %s a la %s" % (abs(dx), "unidad" if abs(dx) == 1 else "unidades", "derecha" if dx > 0 else "izquierda")
    v = "%d %s hacia %s" % (abs(dy), "unidad" if abs(dy) == 1 else "unidades", "arriba" if dy > 0 else "abajo")
    return M("Trasladamos el punto %s %s y %s. ¿Dónde queda?" % (P(x, y), h, v), P(nx, ny), [P(x - dx, y + dy), P(x + dx, y - dy), P(x + dy, y + dx) if dx != dy else P(nx + 1, ny), P(nx, ny + 1)],
             "x: %s %s %d = %s; y: %s %s %d = %s → <b>%s</b>." % (sg(x), "+" if dx > 0 else "−", abs(dx), sg(nx), sg(y), "+" if dy > 0 else "−", abs(dy), sg(ny), P(nx, ny)))


def s4_simetria():
    k = R.choice(["ejeY", "ejeX", "giro180", "giro90"] if LV == 6 else ["recta", "recta", "figura"])
    if LV == 5:
        a = R.randint(3, 5)
        x, y = R.randint(1, a - 1), R.randint(1, 7)
        sx = 2 * a - x
        if sx > 8:
            return None
        if k == "figura":
            ok = R.random() < 0.5
            pts = [(x, y), (x, y + 1), (a, y + 1), (a, y)]
            mir = [(2 * a - px, py) for px, py in pts]
            if not ok:
                mir = [(px + 1, py) for px, py in mir]
            if y + 1 > 8 or max(px for px, py in mir) > 8:
                return None
            return M(plano([], poly=pts, poly2=mir, axis=("v", a)) + "¿Es la figura naranja simétrica de la verde respecto a la línea roja?", "sí" if ok else "no", ["no" if ok else "sí", "solo arriba", "no se puede saber"],
                     "%s" % ("Cada punto está a la misma distancia del eje, al otro lado: <b>sí</b>." if ok else "No está a la misma distancia del eje: <b>no</b>."))
        return M(plano([(x, y, "P")], axis=("v", a)) + "La línea roja es un eje de simetría. ¿Cuáles son las coordenadas del simétrico de P?", P(sx, y), [P(sx + 1, y), P(sx - 1, y), P(y, sx) if y != sx else P(sx, y + 1), P(a, y)],
                 "P está a %d del eje; su simétrico, a %d al otro lado: <b>%s</b>." % (a - x, a - x, P(sx, y)))
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    if x == 0 or y == 0 or abs(x) == abs(y):
        return None
    if k == "ejeY":
        return M(plano([(x, y, "P")], axis=("v", 0)) + "¿Cuál es el simétrico de P respecto al eje vertical?", P(-x, y), [P(x, -y), P(-x, -y), P(y, x)], "Cambia el signo de x: <b>%s</b>." % P(-x, y))
    if k == "ejeX":
        return M(plano([(x, y, "P")], axis=("h", 0)) + "¿Cuál es el simétrico de P respecto al eje horizontal?", P(x, -y), [P(-x, y), P(-x, -y), P(y, x)], "Cambia el signo de y: <b>%s</b>." % P(x, -y))
    if k == "giro180":
        return M(plano([(x, y, "P")]) + "Giramos P 180° alrededor del origen (0, 0). ¿Dónde queda?", P(-x, -y), [P(-x, y), P(x, -y), P(-y, x)], "Un giro de 180° cambia los dos signos: <b>%s</b>." % P(-x, -y))
    return M(plano([(x, y, "P")]) + "Giramos P 90° en sentido contrario a las agujas del reloj alrededor del origen. ¿Dónde queda?", P(-y, x), [P(y, -x), P(-x, -y), P(y, x)], "(x, y) → (−y, x): <b>%s</b>." % P(-y, x))


def s5_escala():
    k = R.choice(["ampliar", "reducir", "semejante"])
    a, b = R.randint(2, 8), R.randint(2, 8)
    f = R.choice([2, 3, 4])
    if k == "ampliar":
        return M("Ampliamos un rectángulo de %d cm × %d cm con razón %d (todo %d veces más grande). ¿Cuánto miden los lados nuevos?" % (a, b, f, f), "%d cm × %d cm" % (a * f, b * f), ["%d cm × %d cm" % (a + f, b + f), "%d cm × %d cm" % (a * f, b), "%d cm × %d cm" % (a * f * f, b * f * f)],
                 "Multiplicamos cada lado por %d: <b>%d cm × %d cm</b>." % (f, a * f, b * f))
    if k == "reducir":
        return M("Reducimos un dibujo de %d cm × %d cm a la mitad. ¿Cuánto mide ahora?" % (a * 2, b * 2), "%d cm × %d cm" % (a, b), ["%d cm × %d cm" % (a * 2 - 2, b * 2 - 2), "%d cm × %d cm" % (a * 4, b * 4), "%d cm × %d cm" % (a, b * 2)], "Dividimos cada lado entre 2: <b>%d cm × %d cm</b>." % (a, b))
    if a == b:
        return None
    ok = R.random() < 0.5
    c, dd = (a * f, b * f) if ok else (a * f, b * f + 1)
    return M("¿Son semejantes un rectángulo de %d × %d y otro de %d × %d?" % (a, b, c, dd), "sí" if ok else "no", ["no" if ok else "sí", "solo si son cuadrados", "no se puede saber"],
             "%s" % ("Los dos lados se multiplican por %d: <b>sí</b>." % f if ok else "Un lado se multiplica por %d y el otro no: <b>no</b>." % f))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40020 + lv * 1000)
    seen = set()
    sets = [
        ("Coordenadas de puntos", mix(R, seen, [(s1_leer, 20)])),
        ("Cuadrantes y puntos" if lv == 6 else "Más coordenadas", mix(R, seen, [(s2_cuadrante, 10), (s1_leer, 10)] if lv == 6 else [(s1_leer, 20)])),
        ("Traslaciones", mix(R, seen, [(s3_traslacion, 20)])),
        ("Simetrías y giros" if lv == 6 else "Simetrías", mix(R, seen, [(s4_simetria, 20)])),
        ("Ampliaciones y reducciones", mix(R, seen, [(s5_escala, 20)])),
    ]
    think = ["Un punto se sitúa con dos <b>coordenadas</b> (x, y): primero lo que avanza en el eje horizontal y después en el vertical.",
             "En una <b>traslación</b>, todos los puntos se mueven lo mismo y en la misma dirección. En una <b>simetría</b>, cada punto pasa al otro lado del eje, a la misma distancia.",
             "Al <b>ampliar o reducir</b>, todas las medidas se multiplican o dividen por el mismo número: la figura es semejante."]
    if lv == 6:
        think.insert(1, "Los ejes dividen el plano en cuatro <b>cuadrantes</b>. A la izquierda del origen, x es negativa; por debajo, y es negativa.")
    body = lesson(think,
                  [("Traslada (−2, 3) 4 a la derecha y 5 hacia abajo" if lv == 6 else "Traslada (2, 3) 4 a la derecha y 1 arriba", ["x: −2 + 4 = 2", "y: 3 − 5 = −2"] if lv == 6 else ["x: 2 + 4 = 6", "y: 3 + 1 = 4"], "(2, −2)" if lv == 6 else "(6, 4)"),
                   ("Amplía 3 cm × 5 cm con razón 2", ["3 × 2 = 6", "5 × 2 = 10"], "6 cm × 10 cm")],
                  [["Cambiar el orden de las coordenadas", "(3, 5) no es (5, 3): primero el eje horizontal."],
                   ["Olvidar el signo" if lv == 6 else "Contar casillas en vez de líneas", "En el segundo cuadrante, x es negativa: (−3, 2)." if lv == 6 else "Los puntos están en los cruces de las líneas."],
                   ["Ampliar solo un lado", "En una ampliación, todos los lados se multiplican por el mismo número."]],
                  plano([(3, 2, "A")] + ([(-2, -3, "B")] if lv == 6 else [(5, 6, "B")])))
    faq = [("¿Cómo se escriben las coordenadas de un punto?", "Entre paréntesis y separadas por una coma: primero la coordenada horizontal (x) y después la vertical (y), por ejemplo (−3, 2)."),
           ("¿Qué diferencia hay entre una traslación y una simetría?", "En una traslación la figura se desliza sin girar; en una simetría se refleja como en un espejo respecto a un eje.")]
    make_unit(R, "coordenadas-y-movimientos", "E",
              "Localización en el plano mediante coordenadas cartesianas" + (" en los cuatro cuadrantes" if lv == 6 else "") + "; transformaciones: traslaciones, simetrías" + (" y giros" if lv == 6 else "") + "; ampliaciones, reducciones y semejanza",
              "Coordenadas y movimientos en el plano", "Coordenadas y movimientos",
              "Fichas de matemáticas de %d.º de Primaria: coordenadas de puntos%s, traslaciones, simetrías%s, ampliaciones y reducciones. 100 ejercicios con soluciones." % (lv, " en los cuatro cuadrantes" if lv == 6 else "", ", giros" if lv == 6 else ""),
              "(x, y): primero horizontal", "Traslación: todos los puntos se mueven igual.",
              body, faq, sets, 20, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
