# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Figuras planas (Sentido espacial)
build(lv): lv = 1 → círculo, triángulo, cuadrado y rectángulo, líneas rectas y curvas, contar figuras;
lv = 2 → también pentágono, hexágono y octógono, lados y vértices, polígonos y no polígonos.
Errores: llamar rectángulo al cuadrado girado, contar mal los vértices, pensar que el círculo tiene lados.
"""
import math
import random
from es_common import mcq, mix, lesson, make_unit, fig
import k_pics

R = None
LV = 2
COL = [("#f4d03f", "#a57c00"), ("#3498db", "#1f5f8b"), ("#e74c3c", "#922b21"), ("#27ae60", "#196f3d")]
NOM = {"circulo": "círculo", "triangulo": "triángulo", "cuadrado": "cuadrado", "rectangulo": "rectángulo", "pentagono": "pentágono", "hexagono": "hexágono", "octogono": "octógono"}
LADOS = {"triangulo": 3, "cuadrado": 4, "rectangulo": 4, "pentagono": 5, "hexagono": 6, "octogono": 8}
COLNOM = {"#f4d03f": "amarillo", "#3498db": "azul", "#e74c3c": "rojo", "#27ae60": "verde"}


def forma(k, cx, cy, r, col, rot=0):
    f, st = col
    a = "fill='%s' stroke='%s' stroke-width='2'" % (f, st)
    if k == "circulo":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' %s/>" % (cx, cy, r, a)
    if k == "rectangulo":
        pts = [(-1.4, -0.75), (1.4, -0.75), (1.4, 0.75), (-1.4, 0.75)]
    elif k == "cuadrado":
        pts = [(-0.8, -0.8), (0.8, -0.8), (0.8, 0.8), (-0.8, 0.8)]
    else:
        n = LADOS[k]
        pts = [(math.cos(-math.pi / 2 + 2 * math.pi * i / n), math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    t = math.radians(rot)
    p = " ".join("%.1f,%.1f" % (cx + r * (x * math.cos(t) - y * math.sin(t)), cy + r * (x * math.sin(t) + y * math.cos(t))) for x, y in pts)
    return "<polygon points='%s' %s/>" % (p, a)


def una(k, rot=0):
    col = R.choice(COL)
    return fig("<svg viewBox='0 0 160 130' width='160' height='130' role='img' aria-label='una figura plana'>%s</svg>" % forma(k, 80, 65, 42, col, rot))


def kinds():
    return ["circulo", "triangulo", "cuadrado", "rectangulo"] + (["pentagono", "hexagono", "octogono"] if LV == 2 else [])


def s_nombre():
    k = R.choice(kinds())
    rot = R.choice([0, 0, 15, 30]) if k not in ("circulo",) else 0
    ok = NOM[k]
    return mcq(una(k, rot) + "¿Cómo se llama esta figura?", ok, [NOM[x] for x in kinds() if x != k] + ["óvalo"], "Es un <b>%s</b>." % ok + (" Tiene %d lados." % LADOS[k] if k in LADOS else ""))


def s_lados():
    k = R.choice([x for x in kinds() if x != "circulo"])
    rot = R.choice([0, 10, 20, 30, 45])
    n = LADOS[k]
    t = R.choice(["lados", "vértices"]) if LV == 2 else "lados"
    return mcq(una(k, rot) + "¿Cuántos %s tiene esta figura?" % t, str(n), [str(n + 1), str(n - 1), str(n + 2)], "Tiene <b>%d</b> %s: es un %s." % (n, t, NOM[k]))


def s_contar():
    target = R.choice(["triangulo", "circulo", "cuadrado", "rectangulo"] + (["hexagono"] if LV == 2 else []))
    n = R.randint(2, 5)
    others = [x for x in kinds() if x != target and x != ("cuadrado" if target == "rectangulo" else "rectangulo" if target == "cuadrado" else "")]
    items = [target] * n + [R.choice(others) for _ in range(R.randint(4, 7))]
    R.shuffle(items)
    cells = R.sample([(r, c) for r in range(3) for c in range(5)], len(items))
    s = "".join(forma(k, 34 + c * 64, 34 + r * 60, 21, R.choice(COL), R.choice([0, 0, 20])) for (r, c), k in zip(cells, items))
    pic = fig("<svg viewBox='0 0 324 186' width='324' height='186' role='img' aria-label='figuras mezcladas'>%s</svg>" % s)
    plural = {"triangulo": "triángulos", "circulo": "círculos", "cuadrado": "cuadrados", "rectangulo": "rectángulos", "hexagono": "hexágonos"}[target]
    return mcq(pic + "¿Cuántos %s hay?" % plural, str(n), [str(n + 1), str(n - 1), str(len(items))], "Hay <b>%d</b> %s." % (n, plural))


def s_saber():
    items = [("¿Qué figura no tiene lados ni vértices?", "el círculo", ["el triángulo", "el cuadrado", "el rectángulo"]),
             ("¿Qué figura tiene 3 lados?", "el triángulo", ["el cuadrado", "el círculo", "el rectángulo"]),
             ("¿Qué figura tiene 4 lados iguales?", "el cuadrado", ["el rectángulo", "el triángulo", "el círculo"]),
             ("¿Qué figura tiene 4 lados, dos largos y dos cortos?", "el rectángulo", ["el cuadrado", "el triángulo", "el círculo"]),
             ("Una rueda tiene forma de…", "círculo", ["cuadrado", "triángulo", "rectángulo"]),
             ("Una puerta tiene forma de…", "rectángulo", ["círculo", "triángulo", "hexágono"]),
             ("Una porción de pizza tiene forma parecida a un…", "triángulo", ["cuadrado", "rectángulo", "círculo"]),
             ("Una baldosa de 20 cm por 20 cm tiene forma de…", "cuadrado", ["triángulo", "círculo", "pentágono"]),
             ("Una moneda tiene forma de…", "círculo", ["cuadrado", "triángulo", "rectángulo"]),
             ("Una pantalla de televisión tiene forma de…", "rectángulo", ["círculo", "triángulo", "pentágono"]),
             ("¿Qué línea tiene el borde de un círculo?", "una línea curva", ["una línea recta", "tres líneas rectas", "cuatro líneas rectas"]),
             ("¿Cuántas esquinas tiene un triángulo?", "3", ["4", "2", "0"]),
             ("¿Cuántas esquinas tiene un rectángulo?", "4", ["3", "2", "0"])]
    if LV == 2:
        items += [("¿Qué figura tiene 5 lados?", "el pentágono", ["el hexágono", "el cuadrado", "el octógono"]),
                  ("¿Qué figura tiene 6 lados?", "el hexágono", ["el pentágono", "el octógono", "el triángulo"]),
                  ("¿Qué figura tiene 8 lados?", "el octógono", ["el hexágono", "el pentágono", "el rectángulo"]),
                  ("Una señal de STOP tiene forma de…", "octógono", ["hexágono", "círculo", "pentágono"]),
                  ("Las celdas de un panal de abejas tienen forma de…", "hexágono", ["pentágono", "cuadrado", "círculo"]),
                  ("¿Qué figura no es un polígono?", "el círculo", ["el triángulo", "el hexágono", "el rectángulo"]),
                  ("Un polígono es una figura cerrada con lados…", "rectos", ["curvos", "abiertos", "redondos"]),
                  ("¿Cuántos vértices tiene un pentágono?", "5", ["4", "6", "10"]),
                  ("¿Cuántos lados tienen 2 triángulos en total?", "6", ["3", "5", "8"]),
                  ("¿Cuántos lados tienen un cuadrado y un triángulo juntos?", "7", ["4", "6", "8"])]
    q, a, w = R.choice(items)
    return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_lineas():
    k = R.choice(["recta", "curva", "abierta", "cerrada"] if LV == 1 else ["poli", "poli", "abierta", "cerrada"])
    col = "#1565c0"
    if k == "recta":
        a = R.choice([0, 10, 15, -20, 30, -35, 40, -10])
        x = 60 * math.cos(math.radians(a))
        y = 60 * math.sin(math.radians(a))
        s = "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4'/>" % (80 - x, 55 - y, 80 + x, 55 + y, col)
        return mcq(fig("<svg viewBox='0 0 160 110' width='160' height='110' role='img' aria-label='una línea'>%s</svg>" % s) + "¿Cómo es esta línea?", "recta", ["curva", "cerrada", "redonda"], "No se tuerce: es una línea <b>recta</b>.")
    if k == "curva":
        s = "<path d='M 15 55 Q 50 %d 80 55 T 145 55' fill='none' stroke='%s' stroke-width='4'/>" % (R.choice([15, 25, 35, 75, 85, 95]), col)
        return mcq(fig("<svg viewBox='0 0 160 110' width='160' height='110' role='img' aria-label='una línea'>%s</svg>" % s) + "¿Cómo es esta línea?", "curva", ["recta", "cerrada", "un triángulo"], "Se tuerce: es una línea <b>curva</b>.")
    if k == "poli":
        sh = R.choice(["circulo", "triangulo", "cuadrado", "pentagono", "hexagono", "rectangulo"])
        ok = "no, es un círculo: no tiene lados rectos" if sh == "circulo" else "sí, es un polígono"
        return mcq(una(sh, R.choice([0, 20])) + "¿Es esta figura un polígono?", ok, ["sí, es un polígono" if sh == "circulo" else "no, es un círculo: no tiene lados rectos", "no, porque es de color", "solo si es grande"],
                   "Un polígono es cerrado y tiene lados rectos: <b>%s</b>." % ok)
    pts = [(20, R.randint(60, 90)), (R.randint(45, 70), R.randint(15, 35)), (R.randint(90, 110), R.randint(60, 90)), (140, R.randint(15, 40))]
    path = "M " + " L ".join("%d %d" % p for p in pts) + (" Z" if k == "cerrada" else "")
    s = "<path d='%s' fill='none' stroke='%s' stroke-width='4'/>" % (path, col)
    ok = "cerrada" if k == "cerrada" else "abierta"
    return mcq(fig("<svg viewBox='0 0 160 110' width='160' height='110' role='img' aria-label='una línea'>%s</svg>" % s) + "¿Esta línea es abierta o cerrada?", ok, ["abierta" if ok == "cerrada" else "cerrada", "curva", "redonda"],
               "Una línea cerrada no tiene extremos sueltos: es <b>%s</b>." % ok)


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30015 + lv * 1000)
    seen = set()
    sets = [("¿Cómo se llama?", mix(R, seen, [(s_nombre, 20)])), ("Lados y vértices" if lv == 2 else "Contar los lados", mix(R, seen, [(s_lados, 20)])),
            ("Contar figuras", mix(R, seen, [(s_contar, 20)])), ("Formas a nuestro alrededor", mix(R, seen, [(s_saber, 10), (s_nombre, 10)])),
            ("Polígonos y líneas" if lv == 2 else "Líneas rectas y curvas", mix(R, seen, [(s_lineas, 12), (s_lados, 4), (s_contar, 4)]))]
    if lv == 1:
        think = ["El <b>círculo</b> es redondo: no tiene lados.", "El <b>triángulo</b> tiene 3 lados. El <b>cuadrado</b> tiene 4 lados iguales. El <b>rectángulo</b> tiene 4 lados: dos largos y dos cortos.",
                 "Para contar los lados, pon el dedo en uno y ve contando hasta volver al principio."]
        ex = [("Una figura con 3 lados", ["3 lados"], "triángulo"), ("Una puerta", ["4 lados: dos largos y dos cortos"], "rectángulo")]
        kb, ks = "Triángulo 3 lados, cuadrado 4", "El círculo no tiene lados."
        meta = "Fichas de matemáticas de 1.º de Primaria: círculo, triángulo, cuadrado y rectángulo, contar lados, líneas rectas y curvas. 100 ejercicios con soluciones."
        std = "Figuras planas: círculo, triángulo, cuadrado y rectángulo; líneas rectas y curvas; reconocimiento en el entorno"
    else:
        think = ["Un <b>polígono</b> es una figura cerrada con lados rectos. Se llama por el número de lados: 3 triángulo, 4 cuadrilátero, 5 pentágono, 6 hexágono, 8 octógono.",
                 "Un <b>vértice</b> es una esquina. Un polígono tiene tantos vértices como lados.", "El círculo no es un polígono: su borde es curvo."]
        ex = [("Una figura con 6 lados", ["6 lados"], "hexágono"), ("Un pentágono", ["5 lados y 5 vértices"], "5 vértices")]
        kb, ks = "Tantos vértices como lados", "Pentágono 5, hexágono 6, octógono 8."
        meta = "Fichas de matemáticas de 2.º de Primaria: polígonos, triángulo, cuadrado, rectángulo, pentágono, hexágono y octógono, lados y vértices. 100 ejercicios con soluciones."
        std = "Figuras planas: polígonos y círculo; lados y vértices; líneas abiertas y cerradas; reconocimiento en el entorno"
    mist = [["Llamar rectángulo a un cuadrado girado", "Si gira, sigue siendo un cuadrado."], ["Contar dos veces el mismo lado", "Marca el lado por el que empiezas."], ["Pensar que el círculo tiene lados", "Su borde es una línea curva."]]
    pic = fig("<svg viewBox='0 0 330 90' width='330' height='90' role='img' aria-label='círculo, triángulo, cuadrado y rectángulo'>%s</svg>" %
              "".join(forma(k, 45 + i * 80, 45, 30, COL[i]) for i, k in enumerate(["circulo", "triangulo", "cuadrado", "rectangulo"])))
    body = lesson(think, ex, mist, pic)
    faq = [("¿Qué diferencia hay entre cuadrado y rectángulo?", "Los dos tienen 4 lados y 4 esquinas rectas, pero el cuadrado tiene los 4 lados iguales."), ("¿El círculo tiene lados?", "No. El borde del círculo es una línea curva, por eso no tiene lados ni vértices.")]
    make_unit(R, "figuras-planas", "E", std, "Figuras planas" if lv == 1 else "Figuras planas y polígonos", "Figuras planas", meta, kb, ks, body, faq, sets, 11 if lv == 1 else 14, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
