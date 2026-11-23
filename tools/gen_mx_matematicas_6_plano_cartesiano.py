# -*- coding: utf-8 -*-
"""México 6.º grado: Ubicación espacial: el primer cuadrante del plano cartesiano, pares ordenados, desplazamientos y simetría (Fase 5). Plano propio (SVG) y España 6.º (ampliar y reducir) con otra semilla."""
import random
from mx_common import src, unit, mcq, fig, svg_wrap
from ws_common import text

esc = src("gen_es_matematicas_6_coordenadas_y_movimientos", 66320, "s5_escala", lv=6)
R = random.Random(66120)
N = 10
S = 26
X0, Y0 = 30, 10
LET = "ABCDEFGH"


def px(x, y):
    return X0 + x * S, Y0 + (N - y) * S


def plano(pts, poly=None, label="plano cartesiano"):
    s = []
    for i in range(N + 1):
        x, _ = px(i, 0)
        _, y = px(0, i)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#dde3ea'/>" % (x, Y0, x, Y0 + N * S))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#dde3ea'/>" % (X0, y, X0 + N * S, y))
        s.append(text(x, Y0 + N * S + 16, str(i), 11, weight=400))
        if i:
            s.append(text(X0 - 10, y + 4, str(i), 11, weight=400))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#333' stroke-width='1.6'/>" % (X0, Y0 + N * S, X0 + N * S + 8, Y0 + N * S))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#333' stroke-width='1.6'/>" % (X0, Y0 + N * S, X0, Y0 - 4))
    s.append(text(X0 + N * S + 12, Y0 + N * S + 4, "x", 12, italic=True))
    if poly:
        s.append("<polygon points='%s' fill='#cfe6d4' fill-opacity='0.7' stroke='#1d6b3a' stroke-width='2'/>" % " ".join("%d,%d" % px(*p) for p in poly))
    for name, (x, y) in pts:
        cx, cy = px(x, y)
        s.append("<circle cx='%d' cy='%d' r='4.5' fill='#c0392b'/>" % (cx, cy))
        s.append(text(cx + 9, cy - 6, name, 13))
    return fig(svg_wrap(X0 + N * S + 22, Y0 + N * S + 24, "".join(s), label).replace("<svg ", "<svg data-pf='lg' ", 1))


def pares(k):
    ps = set()
    while len(ps) < k:
        ps.add((R.randint(1, N - 1), R.randint(1, N - 1)))
    ps = sorted(ps)
    R.shuffle(ps)
    return ps


def c(p):
    return "(%d, %d)" % p


def s_leer():
    ps = pares(4)
    names = list(LET[:4])
    i = R.randrange(4)
    x, y = ps[i]
    w = [c((y, x)) if x != y else c((x + 1, y)), c((x + 1, y)) if x < N else c((x - 1, y)), c((x, y - 1)) if y > 0 else c((x, y + 1)), c((x - 1, y + 1))]
    return mcq(plano(list(zip(names, ps))) + "¿Cuáles son las coordenadas del punto %s?" % names[i], c((x, y)), w,
               "%s está %d lugares a la derecha y %d hacia arriba: <b>%s</b>." % (names[i], x, y, c((x, y))))


def s_ubicar():
    ps = pares(4)
    names = list(LET[:4])
    i = R.randrange(4)
    x, y = ps[i]
    if (y, x) in ps and (y, x) != (x, y):
        return None
    return mcq(plano(list(zip(names, ps))) + "¿Qué punto tiene las coordenadas %s?" % c((x, y)), names[i], [n for j, n in enumerate(names) if j != i],
               "Avanza %d a la derecha y sube %d: es el punto <b>%s</b>." % (x, y, names[i]))


def s_mover():
    x, y = R.randint(1, 8), R.randint(1, 8)
    dx, dy = R.randint(-3, 4), R.randint(-3, 4)
    if (dx == 0 and dy == 0) or not (0 <= x + dx <= N and 0 <= y + dy <= N):
        return None
    def d(v, a, b):
        return "%d %s %s" % (abs(v), "lugar" if abs(v) == 1 else "lugares", a if v > 0 else b)
    mov = " y ".join(t for t in [d(dx, "a la derecha", "a la izquierda") if dx else "", d(dy, "hacia arriba", "hacia abajo") if dy else ""] if t)
    ok = c((x + dx, y + dy))
    w = [c((x + dy, y + dx)), c((x - dx, y - dy)) if 0 <= x - dx and 0 <= y - dy else c((x + dx + 1, y + dy)), c((x + dx, y)), c((x, y + dy))]
    return mcq("Un punto está en %s. Se mueve %s. ¿Dónde queda?" % (c((x, y)), mov), ok, [v for v in w if v != ok], "x: %d %s %d = %d; y: %d %s %d = %d. Queda en <b>%s</b>." % (
        x, "+" if dx >= 0 else "−", abs(dx), x + dx, y, "+" if dy >= 0 else "−", abs(dy), y + dy, ok))


def s_figura():
    x, y = R.randint(1, 4), R.randint(1, 4)
    w_, h = R.randint(2, 4), R.randint(2, 4)
    poly = [(x, y), (x + w_, y), (x + w_, y + h), (x, y + h)]
    k = R.choice(["vert", "tras", "lado"])
    names = ["A", "B", "C", "D"]
    pic = plano(list(zip(names, poly)), poly)
    if k == "vert":
        return mcq(pic + "¿Cuáles son las coordenadas del vértice C del rectángulo?", c(poly[2]), [c((poly[2][1], poly[2][0])) if poly[2][0] != poly[2][1] else c((x, y)), c(poly[1]), c(poly[3])],
                   "C está en <b>%s</b>." % c(poly[2]))
    if k == "lado":
        return mcq(pic + "¿Cuántas unidades mide el lado AB del rectángulo?", str(w_), [str(h) if h != w_ else str(w_ + 1), str(x + w_), str(w_ + 2)],
                   "De x = %d a x = %d hay %d − %d = <b>%d</b> unidades." % (x, x + w_, x + w_, x, w_))
    dx = R.randint(2, 4)
    return mcq(pic + "Si el rectángulo se traslada %d lugares a la derecha, ¿dónde queda el vértice A?" % dx, c((x + dx, y)), [c((x, y + dx)), c((x + dx, y + dx)), c((x - dx, y)) if x - dx >= 0 else c((x + dx + 1, y))],
               "Solo cambia la x: %d + %d = %d → <b>%s</b>." % (x, dx, x + dx, c((x + dx, y))))


def s_sim():
    """simetría respecto a la recta x = 5"""
    x, y = R.randint(1, 9), R.randint(1, 9)
    if x == 5:
        return None
    ok = c((10 - x, y))
    return mcq("En el plano, la recta vertical x = 5 es un eje de simetría. ¿Cuál es el punto simétrico de %s?" % c((x, y)), ok, [c((x, 10 - y)) if y != 5 else c((x, y)), c((y, x)) if (y, x) != (10 - x, y) else c((x + 1, y)), c((10 - y, x)) if (10 - y, x) != (10 - x, y) else c((5, y))],
               "Está %d lugares a la %s del eje; el simétrico está a la misma distancia del otro lado: <b>%s</b>." % (abs(5 - x), "izquierda" if x < 5 else "derecha", ok))


unit("plano-cartesiano", 10, "U",
     "Lee y ubica puntos en el primer cuadrante del plano cartesiano con pares ordenados; describe desplazamientos y traslaciones; identifica puntos simétricos; amplía y reduce figuras",
     "El plano cartesiano: primer cuadrante", "Plano cartesiano",
     "Ejercicios de matemáticas de 6.º grado de primaria: coordenadas en el primer cuadrante, pares ordenados, desplazamientos, figuras en el plano, simetría, ampliar y reducir. 100 ejercicios con respuestas.",
     "(x, y): primero →, luego ↑", "El origen es (0, 0).",
     ["El <b>plano cartesiano</b> tiene dos ejes: el horizontal (x) y el vertical (y). Se cruzan en el <b>origen</b> (0, 0).",
      "Un punto se nombra con un <b>par ordenado</b> (x, y): primero cuántos lugares a la derecha y después cuántos hacia arriba. (4, 2) no es lo mismo que (2, 4).",
      "Para trasladar una figura, mueve todos sus puntos lo mismo: 3 a la derecha suma 3 a la x."],
     [("Punto 5 a la derecha y 3 arriba", ["x = 5", "y = 3"], "(5, 3)"), ("(2, 6) se mueve 4 a la derecha", ["x: 2 + 4 = 6"], "(6, 6)")],
     [["Cambiar el orden de las coordenadas", "(4, 2): primero x = 4."], ["Contar los cuadros en lugar de las líneas", "Los puntos están en los cruces."], ["Mover solo un punto de la figura", "En una traslación se mueven todos."]],
     [("¿Qué coordenada se escribe primero?", "La del eje horizontal (x). Después la del eje vertical (y)."),
      ("¿Qué es el origen?", "El punto donde se cruzan los ejes: (0, 0).")],
     [("Leer coordenadas", [(s_leer, 20)]), ("Ubicar puntos", [(s_ubicar, 20)]), ("Desplazamientos", [(s_mover, 20)]), ("Figuras en el plano y simetría", [(s_figura, 12), (s_sim, 8)]), ("Ampliar y reducir", [(esc, 20)])],
     66010, pic=plano([("A", (4, 2)), ("B", (2, 4))], label="plano cartesiano con A(4, 2) y B(2, 4)"), lv=6)
