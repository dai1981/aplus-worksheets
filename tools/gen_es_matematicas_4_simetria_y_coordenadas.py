# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Simetría y coordenadas (Sentido espacial)
Figuras simétricas y ejes de simetría, el simétrico de un punto respecto a un eje en la cuadrícula,
coordenadas de puntos en una cuadrícula (x, y), desplazamientos (derecha, izquierda, arriba, abajo) e itinerarios.
Errores: cambiar el orden de las coordenadas (primero el número de abajo, después el de la izquierda), contar las casillas en lugar de las líneas.
"""
import random
from es_common import mcq, mix, lesson, make_unit, bank

R = random.Random(44022)
C = 30
LET = "ABCDEFGH"


def plano(points, n=8, axis=None, cells=(), label="cuadrícula con puntos"):
    """cuadrícula de 0 a n con puntos [(x, y, nombre)]; axis = ('v', x) o ('h', y); cells = [(x, y)] casillas pintadas"""
    ox, oy = 30, 20 + n * C
    s = []
    for (x, y) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#9fd3a8' stroke='#2e7d32' stroke-width='1'/>" % (ox + x * C, oy - (y + 1) * C, C, C))
    for i in range(n + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#bcd6e6' stroke-width='1'/>" % (ox + i * C, oy, ox + i * C, oy - n * C))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#bcd6e6' stroke-width='1'/>" % (ox, oy - i * C, ox + n * C, oy - i * C))
        s.append("<text x='%d' y='%d' font-size='12' text-anchor='middle' fill='#333'>%d</text>" % (ox + i * C, oy + 16, i))
        if i:
            s.append("<text x='%d' y='%d' font-size='12' text-anchor='end' fill='#333'>%d</text>" % (ox - 6, oy - i * C + 4, i))
    s.append("<text x='%d' y='%d' font-size='12' text-anchor='end' fill='#333'>0</text>" % (ox - 6, oy + 4))
    if axis:
        if axis[0] == "v":
            x = ox + axis[1] * C
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c0392b' stroke-width='3' stroke-dasharray='6 4'/>" % (x, oy + 4, x, oy - n * C - 4))
        else:
            y = oy - axis[1] * C
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c0392b' stroke-width='3' stroke-dasharray='6 4'/>" % (ox - 4, y, ox + n * C + 4, y))
    for (x, y, nm) in points:
        s.append("<circle cx='%d' cy='%d' r='5' fill='#1f5fbf'/>" % (ox + x * C, oy - y * C))
        s.append("<text x='%d' y='%d' font-size='14' font-weight='700' fill='#1f5fbf'>%s</text>" % (ox + x * C + 6, oy - y * C - 6, nm))
    W, H = ox + n * C + 16, oy + 26
    return "<div class='fig'><svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='%s'>%s</svg></div>" % (W, H, W, label, "".join(s))


def pt(x, y):
    return "(%d, %d)" % (x, y)


def s1_coord():
    pts = []
    used = set()
    while len(pts) < 4:
        x, y = R.randint(1, 8), R.randint(1, 8)
        if (x, y) in used or (y, x) in used:
            continue
        used.add((x, y))
        pts.append((x, y, LET[len(pts)]))
    i = R.randrange(4)
    x, y, nm = pts[i]
    k = R.choice(["coord", "punto"])
    if k == "coord":
        return mcq(plano(pts) + "¿Cuáles son las coordenadas del punto %s?" % nm, pt(x, y), [pt(y, x) if x != y else pt(x + 1, y), pt(x + 1, y) if x < 8 else pt(x - 1, y), pt(x, y - 1) if y > 1 else pt(x, y + 1), pt(pts[(i + 1) % 4][0], pts[(i + 1) % 4][1])],
                   "Primero contamos hacia la derecha (%d) y después hacia arriba (%d): <b>%s</b>." % (x, y, pt(x, y)))
    return mcq(plano(pts) + "¿Qué punto está en %s?" % pt(x, y), nm, [p[2] for p in pts], "%d hacia la derecha y %d hacia arriba: el punto <b>%s</b>." % (x, y, nm))


def s2_mover():
    x, y = R.randint(2, 6), R.randint(2, 6)
    dx, dy = R.choice([-2, -1, 1, 2, 3]), R.choice([-2, -1, 1, 2, 3])
    nx, ny = x + dx, y + dy
    if not (0 <= nx <= 8 and 0 <= ny <= 8):
        return None
    h = "%d %s a la %s" % (abs(dx), "casilla" if abs(dx) == 1 else "casillas", "derecha" if dx > 0 else "izquierda")
    v = "%d %s hacia %s" % (abs(dy), "casilla" if abs(dy) == 1 else "casillas", "arriba" if dy > 0 else "abajo")
    return mcq(plano([(x, y, "R")], label="robot en una cuadrícula") + "Un robot está en el punto R %s. Se mueve %s y %s. ¿Dónde está ahora?" % (pt(x, y), h, v), pt(nx, ny),
               [pt(x - dx, y + dy), pt(x + dx, y - dy), pt(ny, nx) if nx != ny else pt(nx + 1, ny), pt(x + dy, y + dx) if (dx, dy) != (dy, dx) else pt(nx, ny + 1)],
               "%s: %d %s %d = %d; %d %s %d = %d → <b>%s</b>." % (pt(x, y), x, "+" if dx > 0 else "−", abs(dx), nx, y, "+" if dy > 0 else "−", abs(dy), ny, pt(nx, ny)))


def s2_camino():
    a = (R.randint(0, 3), R.randint(0, 3))
    b = (a[0] + R.randint(1, 5), a[1] + R.randint(1, 5))
    if b[0] > 8 or b[1] > 8:
        return None
    dx, dy = b[0] - a[0], b[1] - a[1]
    ok = "%d a la derecha y %d hacia arriba" % (dx, dy)
    return mcq(plano([(a[0], a[1], "A"), (b[0], b[1], "B")]) + "¿Qué movimiento lleva del punto A al punto B?", ok,
               ["%d a la derecha y %d hacia arriba" % (dy, dx) if dx != dy else "%d a la derecha y %d hacia arriba" % (dx + 1, dy), "%d a la izquierda y %d hacia abajo" % (dx, dy), "%d a la derecha y %d hacia abajo" % (dx, dy), "%d a la derecha y %d hacia arriba" % (b[0], b[1])],
               "De %d a %d hay %d hacia la derecha; de %d a %d hay %d hacia arriba: <b>%s</b>." % (a[0], b[0], dx, a[1], b[1], dy, ok))


def s3_simetrico():
    ax = R.choice([("v", R.randint(3, 5)), ("h", R.randint(3, 5))])
    if ax[0] == "v":
        x = R.randint(0, ax[1] - 1)
        y = R.randint(1, 7)
        sx, sy = 2 * ax[1] - x, y
    else:
        y = R.randint(0, ax[1] - 1)
        x = R.randint(1, 7)
        sx, sy = x, 2 * ax[1] - y
    if not (0 <= sx <= 8 and 0 <= sy <= 8):
        return None
    ws = [pt(sx + 1, sy) if ax[0] == "v" else pt(sx, sy + 1), pt(sx - 1, sy) if ax[0] == "v" else pt(sx, sy - 1), pt(sy, sx) if sx != sy else pt(sx + 2, sy),
          pt(x, y + (sx - x)) if ax[0] == "v" and y + (sx - x) <= 8 else pt(x + (sy - y), y) if x + (sy - y) <= 8 else pt(sx + 2, sy + 1)]
    d = abs(sx - x) // 2 if ax[0] == "v" else abs(sy - y) // 2
    return mcq(plano([(x, y, "P")], axis=ax, label="punto y eje de simetría") + "La línea roja es un eje de simetría. ¿Cuáles son las coordenadas del simétrico de P?", pt(sx, sy), ws,
               "P está a %d %s del eje; su simétrico está a %d %s al otro lado: <b>%s</b>." % (d, "casilla" if d == 1 else "casillas", d, "casilla" if d == 1 else "casillas", pt(sx, sy)))


def s4_figura():
    a = R.choice([3, 4, 5])
    half = set()
    while len(half) < R.randint(3, 6):
        half.add((R.randint(a - 3 if a >= 3 else 0, a - 1), R.randint(1, 6)))
    half = sorted(half)
    sym = R.random() < 0.5
    other = [(2 * a - 1 - x, y) for x, y in half]
    if not sym:
        x, y = R.choice(other)
        other.remove((x, y))
        nb = (x, y + 1) if y < 7 and (x, y + 1) not in other else (x, y - 1)
        if nb in other or nb[1] < 0:
            return None
        other.append(nb)
    cells = half + other
    return mcq(plano([], axis=("v", a), cells=cells, label="figura y eje") + "¿Es simétrica la figura verde respecto a la línea roja?", "sí" if sym else "no",
               ["no" if sym else "sí", "solo la parte de arriba", "no se puede saber"],
               "%s" % ("Cada casilla tiene su pareja a la misma distancia al otro lado: <b>sí</b>." if sym else "Hay una casilla sin su pareja al otro lado: <b>no</b>."))


s5_ejes = bank(R, [
    ("¿Cuántos ejes de simetría tiene un cuadrado?", "4", ["2", "1", "0"]),
    ("¿Cuántos ejes de simetría tiene un rectángulo (que no es cuadrado)?", "2", ["4", "1", "0"]),
    ("¿Cuántos ejes de simetría tiene un triángulo equilátero?", "3", ["1", "2", "0"]),
    ("¿Cuántos ejes de simetría tiene un triángulo isósceles (no equilátero)?", "1", ["2", "3", "0"]),
    ("¿Cuántos ejes de simetría tiene un triángulo escaleno?", "0", ["1", "2", "3"]),
    ("¿Cuántos ejes de simetría tiene un círculo?", "infinitos", ["1", "2", "4"]),
    ("¿Cuántos ejes de simetría tiene un rombo (que no es cuadrado)?", "2", ["4", "1", "0"]),
    ("¿Cuántos ejes de simetría tiene un hexágono regular?", "6", ["3", "2", "12"]),
    ("¿Qué letra mayúscula tiene un eje de simetría vertical?", "A", ["F", "G", "J"]),
    ("¿Qué letra mayúscula tiene un eje de simetría horizontal?", "E", ["F", "G", "L"]),
    ("¿Qué letra mayúscula no tiene ningún eje de simetría?", "F", ["A", "H", "O"]),
    ("¿Qué letra mayúscula tiene dos ejes de simetría?", "H", ["A", "E", "M"]),
    ("¿Qué número no tiene ningún eje de simetría?", "7", ["8", "0", "3"]),
    ("En una figura simétrica, cada punto y su simétrico están…", "a la misma distancia del eje", ["sobre el eje", "siempre arriba", "a distinta distancia del eje"]),
    ("Si doblas una figura simétrica por su eje, las dos mitades…", "coinciden", ["no coinciden", "se separan", "cambian de tamaño"]),
    ("¿Cuántos ejes de simetría tiene un pentágono regular?", "5", ["1", "2", "10"]),
], "ejes")


def main():
    seen = set()
    sets = [
        ("Coordenadas de puntos", mix(R, seen, [(s1_coord, 20)])),
        ("Desplazamientos", mix(R, seen, [(s2_mover, 12), (s2_camino, 8)])),
        ("Ejes de simetría", mix(R, seen, [(s5_ejes, 16), (s4_figura, 4)])),
        ("Figuras simétricas", mix(R, seen, [(s4_figura, 8), (s3_simetrico, 12)])),
        ("El simétrico de un punto", mix(R, seen, [(s3_simetrico, 14), (s2_camino, 6)])),
    ]
    body = lesson(
        ["Para dar la posición de un punto en una cuadrícula usamos dos números, sus <b>coordenadas</b>: primero lo que avanzamos hacia la <b>derecha</b> y después lo que subimos hacia <b>arriba</b>. El punto (3, 5) está 3 a la derecha y 5 arriba.",
         "Una figura es <b>simétrica</b> si al doblarla por una línea, el <b>eje de simetría</b>, las dos mitades coinciden.",
         "El <b>simétrico</b> de un punto está al otro lado del eje y a la misma distancia."],
        [("Del punto (2, 3) avanzas 4 a la derecha y 1 arriba", ["2 + 4 = 6", "3 + 1 = 4"], "(6, 4)"),
         ("El eje es la línea vertical del 4. ¿Simétrico de (1, 5)?", ["(1, 5) está a 3 del eje", "4 + 3 = 7"], "(7, 5)")],
        [["Cambiar el orden de las coordenadas", "(3, 5) no es lo mismo que (5, 3): primero hacia la derecha, después hacia arriba."],
         ["Contar casillas en vez de líneas", "Los puntos están en los cruces de las líneas."],
         ["Poner el simétrico a otra distancia", "Cuenta las casillas desde el eje hacia los dos lados."]],
        plano([(3, 5, "A")], n=6))
    faq = [("¿Cómo se leen las coordenadas de un punto?", "Se escribe primero el número del eje horizontal (hacia la derecha) y después el del eje vertical (hacia arriba), entre paréntesis y separados por una coma: (3, 5)."),
           ("¿Qué es un eje de simetría?", "Es una línea que divide una figura en dos partes iguales que coinciden al doblarla por esa línea.")]
    make_unit(R, "simetria-y-coordenadas", "E",
              "Localización y desplazamientos en el plano: coordenadas en una cuadrícula e itinerarios; simetría axial: ejes de simetría y figuras simétricas en la cuadrícula",
              "Simetría y coordenadas", "Simetría y coordenadas",
              "Fichas de matemáticas de 4.º de Primaria: coordenadas de puntos en una cuadrícula, desplazamientos, ejes de simetría, figuras simétricas y el simétrico de un punto. 100 ejercicios con soluciones.",
              "Coordenadas: primero hacia la derecha, después hacia arriba", "El simétrico está a la misma distancia del eje.",
              body, faq, sets, 22)


if __name__ == "__main__":
    main()
