# -*- coding: utf-8 -*-
"""
México 6.º grado: Sistemas de numeración: maya (base 20, punto, raya y caracol), romano y decimal (Estudio de los números, Fase 5).
Numeración maya propia (dibujos SVG); numeración romana reutiliza España 4.º con otra semilla.
Errores: leer los niveles mayas como si valieran 10, olvidar el cero (caracol), escribir IIII en lugar de IV.
"""
import random
from mx_common import src, unit, mcq, num, fig, svg_wrap, NB
from ws_common import text

R = random.Random(66101)
letras, leer1, leer2, escribir, reglas, vida = src("gen_es_matematicas_4_numeros_romanos", 66201, "s1_letras", "s1_leer", "s2_leer", "s3_escribir", "s4_reglas", "s5_vida", mx_=3999)


def cifra(n, x, y):
    """una cifra maya (0–19) dentro de una caja de 80 × 56 cuyo borde superior está en y"""
    s = []
    if n == 0:
        s.append("<ellipse cx='%d' cy='%d' rx='22' ry='12' fill='#f3e3c3' stroke='#6b4b1f' stroke-width='2'/>" % (x + 40, y + 28))
        s.append("<path d='M%d %d q8 -10 16 0 q8 10 16 0' fill='none' stroke='#6b4b1f' stroke-width='2'/>" % (x + 24, y + 28))
        return "".join(s)
    rayas, puntos = divmod(n, 5)
    yy = y + 56 - 6 - 8 * rayas - (4 if rayas else 0)
    for i in range(rayas):
        s.append("<rect x='%d' y='%d' width='60' height='7' rx='2' fill='#1d6b3a'/>" % (x + 10, y + 56 - 6 - 7 - i * 10))
    if puntos:
        cy = y + 56 - 6 - 10 * rayas - 8 - (2 if rayas else 0)
        w = 14 * (puntos - 1)
        for i in range(puntos):
            s.append("<circle cx='%d' cy='%d' r='5' fill='#1d6b3a'/>" % (x + 40 - w // 2 + 14 * i, cy))
    return "".join(s)


def maya_svg(n, label=None):
    ds = []
    m = n
    while True:
        ds.insert(0, m % 20)
        m //= 20
        if m == 0:
            break
    H = 56 * len(ds) + 8 * (len(ds) - 1)
    s = []
    for i, d in enumerate(ds):
        y = i * 64
        s.append("<rect x='2' y='%d' width='80' height='56' fill='none' stroke='#bbb' stroke-dasharray='4 3'/>" % y)
        s.append(cifra(d, 2, y))
    return fig(svg_wrap(84, H, "".join(s), label or "número maya"))


def valor(n):
    ds, m = [], n
    while True:
        ds.insert(0, m % 20)
        m //= 20
        if m == 0:
            break
    return ds


def s_uno():
    n = R.randint(1, 19)
    r, p = divmod(n, 5)
    return mcq(maya_svg(n) + "¿Qué número maya es este?", str(n), [str(r + p), str(n + 5) if r < 3 else str(n - 5), str(10 * r + p) if r else str(n + 1), str(n + 1) if n < 19 else str(n - 1)],
               "Cada raya vale 5 y cada punto vale 1: %s = <b>%d</b>." % (" + ".join(["5"] * r + ["1"] * p), n))


def s_dos():
    a = R.randint(1, 19)
    b = R.choice([R.randint(1, 19), 0])
    n = 20 * a + b
    return mcq(maya_svg(n) + "¿Qué número maya es este? (el nivel de arriba vale 20 veces más)", num(n), [num(10 * a + b), num(a + b), num(20 * b + a) if b else num(a * 100), num(n + 20)],
               "Arriba: %d × 20 = %s. Abajo: %d. Total: %s + %d = <b>%s</b>." % (a, num(20 * a), b, num(20 * a), b, num(n)))


def s_tres():
    a, b, c = R.randint(1, 4), R.randint(0, 19), R.randint(0, 19)
    n = 400 * a + 20 * b + c
    return mcq(maya_svg(n) + "¿Qué número maya es este? (cada nivel vale 20 veces más que el de abajo)", num(n), [num(100 * a + 10 * b + c), num(20 * a + 20 * b + c), num(400 * a + b + c), num(n + 400)],
               "%d × 400 + %d × 20 + %d = %s + %s + %d = <b>%s</b>." % (a, b, c, num(400 * a), num(20 * b), c, num(n)))


def s_escribir():
    n = R.randint(1, 19) if R.random() < 0.5 else R.randint(21, 399)
    ds = valor(n)
    def desc(d):
        if d == 0:
            return "un caracol"
        r, p = divmod(d, 5)
        parts = []
        if r:
            parts.append("%d %s" % (r, "raya" if r == 1 else "rayas"))
        if p:
            parts.append("%d %s" % (p, "punto" if p == 1 else "puntos"))
        return " y ".join(parts)
    if len(ds) == 1:
        d = ds[0]
        r, p = divmod(d, 5)
        w = [desc(r + p if r + p < 20 else d - 1) if (r + p) != d else desc(d + 1), desc(d + 5) if d + 5 < 20 else desc(d - 5), desc(d + 1) if d < 19 else desc(d - 2)]
        if p == 0:
            w.append("%d puntos" % d)
        return mcq("¿Cómo se escribe el %d con números mayas?" % d, desc(d), w, "%d = %s: <b>%s</b>." % (d, " + ".join(["5"] * r + ["1"] * p), desc(d)))
    a, b = ds
    ok = "arriba %s; abajo %s" % (desc(a), desc(b))
    w = ["arriba %s; abajo %s" % (desc(b), desc(a)) if a != b else "arriba %s; abajo %s" % (desc(a), desc((b + 1) % 20)),
         "arriba %s; abajo %s" % (desc(a + 1) if a < 19 else desc(a - 1), desc(b)), "arriba %s; abajo %s" % (desc(a), desc((b + 5) % 20))]
    return mcq("¿Cómo se escribe el %s con números mayas (dos niveles)?" % num(n), ok, w, "%s = %d × 20 + %d: <b>%s</b>." % (num(n), a, b, ok))


BANCO = [("En la numeración maya, ¿cuánto vale un punto?", "1", ["5", "20", "10"]), ("En la numeración maya, ¿cuánto vale una raya?", "5", ["1", "10", "20"]),
         ("¿Con qué símbolo escribían los mayas el cero?", "con un caracol (concha)", ["con una raya", "con un punto", "no tenían cero"]),
         ("¿En qué base está la numeración maya?", "en base 20", ["en base 10", "en base 5", "en base 60"]),
         ("En el segundo nivel de un número maya, ¿cuánto vale cada punto?", "20", ["2", "10", "100"]),
         ("En el tercer nivel de un número maya, ¿cuánto vale cada punto?", "400", ["300", "100", "40"]),
         ("¿Cuál es el mayor número que cabe en un solo nivel maya?", "19", ["20", "15", "10"]),
         ("¿Cuántas rayas como máximo se ponen en un nivel maya?", "3", ["4", "5", "2"]),
         ("¿Cuántos puntos como máximo se ponen juntos en un nivel maya?", "4", ["5", "3", "9"]),
         ("¿En qué orden se escriben los niveles de un número maya?", "de abajo hacia arriba, de menor a mayor valor", ["de izquierda a derecha", "de arriba hacia abajo, de menor a mayor valor", "en cualquier orden"]),
         ("¿Qué sistema tiene un símbolo para el cero: el maya o el romano?", "el maya", ["el romano", "los dos", "ninguno"]),
         ("En nuestro sistema decimal, ¿cuánto vale el 3 en 3 520?", "3 000", ["3", "300", "30"]),
         ("¿Por qué nuestro sistema se llama decimal?", "porque cada lugar vale 10 veces más que el de su derecha", ["porque usa decimales", "porque tiene 20 símbolos", "porque se inventó en el siglo X"]),
         ("¿Qué sistema es posicional: el romano o el decimal?", "el decimal", ["el romano", "los dos", "ninguno"]),
         ("¿Cuántas cifras distintas usa nuestro sistema decimal?", "10 (del 0 al 9)", ["9", "20", "100"])]


def s_ideas():
    q, a, w = R.choice(BANCO)
    return mcq(q, a.replace("3 000", "3" + NB + "000"), w, "Respuesta: <b>%s</b>." % a.replace("3 000", "3" + NB + "000"))


unit("sistemas-de-numeracion", 1, "N",
     "Lee y escribe números con el sistema de numeración maya (base 20, punto, raya y caracol) y con el sistema romano; los compara con el sistema decimal posicional",
     "Numeración maya, romana y decimal", "Numeración maya y romana",
     "Ejercicios de matemáticas de 6.º grado de primaria: números mayas con punto, raya y caracol, niveles de base 20, números romanos y el sistema decimal. 100 ejercicios con respuestas.",
     "Maya: punto 1, raya 5, caracol 0", "Cada nivel maya vale 20 veces más.",
     ["En la numeración <b>maya</b>, el punto vale 1, la raya vale 5 y el caracol vale 0. En un nivel se escriben números del 0 al 19 (como máximo 3 rayas y 4 puntos).",
      "Los mayas escribían en <b>niveles</b>, de abajo hacia arriba: el primer nivel vale 1, el segundo 20 y el tercero 400. Así, 2 puntos arriba y 1 raya abajo = 2 × 20 + 5 = 45.",
      "En los números <b>romanos</b>, I = 1, V = 5, X = 10, L = 50, C = 100, D = 500 y M = 1 000. Un símbolo menor a la izquierda de uno mayor se resta: IV = 4, XC = 90."],
     [("Arriba 3 puntos; abajo 2 rayas y 1 punto", ["3 × 20 = 60", "abajo: 11"], "71"), ("Escribe 49 con números romanos", ["40 = XL", "9 = IX"], "XLIX")],
     [["Pensar que el segundo nivel maya vale 10", "Vale 20: los mayas contaban de 20 en 20."], ["Olvidar el caracol", "Un nivel vacío se escribe con un caracol (0)."], ["Escribir IIII", "4 es IV: no se repite un símbolo más de 3 veces."]],
     [("¿Por qué los mayas contaban de 20 en 20?", "Se cree que contaban con los dedos de las manos y de los pies. Por eso cada nivel vale 20 veces más que el de abajo."),
      ("¿Qué ventaja tiene el cero maya?", "Permite saber que un nivel está vacío. Los romanos no tenían cero y su sistema no es posicional.")],
     [("Números mayas de un nivel", [(s_uno, 12), (s_escribir, 8)]), ("Números mayas de dos y tres niveles", [(s_dos, 14), (s_tres, 6)]), ("Ideas de la numeración maya y decimal", [(s_ideas, 15), (s_escribir, 5)]),
      ("Leer números romanos", [(letras, 4), (leer1, 8), (leer2, 8)]), ("Escribir números romanos", [(escribir, 12), (reglas, 4), (vida, 4)])],
     66001, pic=maya_svg(45, "45 en números mayas: 2 puntos arriba, 1 raya abajo"), lv=6)
