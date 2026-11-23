# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Posiciones y orientación (Sentido espacial)
build(lv): lv = 1 → «posiciones»: encima, debajo, al lado, delante, detrás, arriba, abajo, izquierda y derecha, primero y último;
lv = 2 → «orientacion-en-el-espacio»: también desplazamientos e itinerarios en una cuadrícula y figuras simétricas (reutiliza 4.º).
Errores: confundir la izquierda y la derecha, confundir delante y detrás, contar la casilla de salida.
"""
import random
from es_common import mcq, mix, lesson, make_unit
from es_low import src
import es_pics as P
import k_pics

R = None
LV = 2


def art(kind):
    return ("la " if P.fem(kind) else "el ") + P.nombre(kind, 1)


def de(kind):
    return ("de la " if P.fem(kind) else "del ") + P.nombre(kind, 1)


def s_mesa():
    k = R.choice(P.KINDS)
    rel = R.choice(["above", "below", "beside", "beside-left"])
    ok = {"above": "encima de la mesa", "below": "debajo de la mesa", "beside": "al lado de la mesa", "beside-left": "al lado de la mesa"}[rel]
    pic = P.pic(k_pics.table_scene_svg(k, rel), "una mesa y %s" % art(k))
    return mcq(pic + "¿Dónde está %s?" % art(k), ok, [x for x in ("encima de la mesa", "debajo de la mesa", "al lado de la mesa", "dentro de la mesa") if x != ok], "Respuesta: <b>%s</b>." % ok)


def s_caja():
    k = R.choice(P.KINDS)
    rel = R.choice(["front", "behind", "beside", "above"])
    ok = {"front": "delante de la caja", "behind": "detrás de la caja", "beside": "al lado de la caja", "above": "encima de la caja"}[rel]
    pic = P.pic(k_pics.box_scene_svg(k, rel), "una caja y %s" % art(k))
    return mcq(pic + "¿Dónde está %s?" % art(k), ok, [x for x in ("delante de la caja", "detrás de la caja", "al lado de la caja", "encima de la caja", "debajo de la caja") if x != ok],
               "%s<b>%s</b>." % ("La caja tapa una parte: está " if rel == "behind" else "", ok))


def s_estante():
    ks = R.sample(P.KINDS, 3)
    pic = P.pic(k_pics.shelf_svg(ks), "estantería con %s" % ", ".join(P.nombre(k, 1) for k in ks))
    t = R.choice(["arriba", "abajo", "medio", "encima", "debajo"])
    if t in ("arriba", "abajo", "medio"):
        i = {"arriba": 0, "medio": 1, "abajo": 2}[t]
        q = {"arriba": "¿Qué hay en el estante de arriba?", "abajo": "¿Qué hay en el estante de abajo?", "medio": "¿Qué hay en el estante del medio?"}[t]
        ok = P.nombre(ks[i], 1)
    elif t == "encima":
        q = "¿Qué hay justo encima %s?" % de(ks[1])
        ok = P.nombre(ks[0], 1)
    else:
        q = "¿Qué hay justo debajo %s?" % de(ks[1])
        ok = P.nombre(ks[2], 1)
    return mcq(pic + q, ok, [P.nombre(k, 1) for k in ks if P.nombre(k, 1) != ok] + [P.nombre(R.choice([x for x in P.KINDS if x not in ks]), 1)], "Respuesta: <b>%s</b>." % ok)


def s_fila():
    n = R.choice([4, 5])
    ks = R.sample(P.KINDS, n)
    pic = P.pic(k_pics.kinds_row_svg(ks), "una fila: " + ", ".join(P.nombre(k, 1) for k in ks))
    t = R.choice(["der", "izq", "pos", "pos", "extremo"])
    if t in ("der", "izq"):
        i = R.randrange(n - 1) if t == "der" else R.randrange(1, n)
        ok = P.nombre(ks[i + 1] if t == "der" else ks[i - 1], 1)
        return mcq(pic + "¿Qué hay justo a la %s %s?" % ("derecha" if t == "der" else "izquierda", de(ks[i])), ok, [P.nombre(k, 1) for k in ks if P.nombre(k, 1) != ok and k != ks[i]] + [P.nombre(ks[i], 1)],
                   "Mirando el dibujo, a la %s %s está <b>%s</b>." % ("derecha" if t == "der" else "izquierda", de(ks[i]), ok))
    if t == "extremo":
        side = R.choice(["izquierda", "derecha"])
        ok = P.nombre(ks[0] if side == "izquierda" else ks[-1], 1)
        return mcq(pic + "¿Qué hay al final de la fila, a la %s?" % side, ok, [P.nombre(k, 1) for k in ks if P.nombre(k, 1) != ok], "Respuesta: <b>%s</b>." % ok)
    i = R.randrange(n)
    k = ks[i]
    fem = P.fem(k)
    ok = {0: "primera", 1: "segunda", 2: "tercera", 3: "cuarta", 4: "quinta"}[i] if fem else {0: "primero", 1: "segundo", 2: "tercero", 3: "cuarto", 4: "quinto"}[i]
    opts = [{0: "primera", 1: "segunda", 2: "tercera", 3: "cuarta", 4: "quinta"}[j] if fem else {0: "primero", 1: "segundo", 2: "tercero", 3: "cuarto", 4: "quinto"}[j] for j in range(5) if j != i]
    return mcq(pic + "Contando desde la izquierda, ¿en qué lugar está %s?" % art(k), ok, opts, "Contamos desde la izquierda: %s está %s <b>%s</b>." % (art(k), "la" if fem else "el", ok))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30019 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("Encima, debajo y al lado", mix(R, seen, [(s_mesa, 20)])), ("Delante y detrás", mix(R, seen, [(s_caja, 20)])), ("Arriba, abajo y en medio", mix(R, seen, [(s_estante, 20)])),
                ("Izquierda y derecha", mix(R, seen, [(s_fila, 20)])), ("Repaso", mix(R, seen, [(s_mesa, 5), (s_caja, 5), (s_estante, 5), (s_fila, 5)]))]
        think = ["Para decir dónde está algo, lo comparamos con otra cosa: la pelota está <b>encima</b> de la mesa.", "Si una cosa tapa a otra, la que se ve entera está <b>delante</b> y la tapada está <b>detrás</b>.",
                 "Para la <b>izquierda</b> y la <b>derecha</b>, mira el dibujo como lo ves tú."]
        ex = [("El gato está bajo la mesa", ["Debajo"], "debajo de la mesa"), ("En la fila: pato, flor, pez", ["Justo a la derecha del pato"], "la flor")]
        kb, ks = "Encima, debajo, delante, detrás", "Izquierda y derecha: como lo ves tú."
        meta = "Fichas de matemáticas de 1.º de Primaria: encima, debajo, al lado, delante, detrás, arriba, abajo, izquierda y derecha con dibujos. 100 ejercicios con soluciones."
        std = "Posiciones relativas de objetos: encima/debajo, delante/detrás, al lado, arriba/abajo, izquierda/derecha; ordinales"
        slug, title, short = "posiciones", "Posiciones", "Posiciones"
        sort = 13
    else:
        mover, camino, figura = src("simetria_y_coordenadas", 32917, "s2_mover", "s2_camino", "s4_figura", mx=100)
        sets = [("Delante, detrás, encima y debajo", mix(R, seen, [(s_caja, 10), (s_mesa, 10)])), ("Izquierda y derecha", mix(R, seen, [(s_fila, 14), (s_estante, 6)])),
                ("Moverse en la cuadrícula", mix(R, seen, [(mover, 20)])), ("Caminos e itinerarios", mix(R, seen, [(camino, 20)])), ("Figuras simétricas", mix(R, seen, [(figura, 20)]))]
        think = ["Para decir dónde está algo, lo comparamos con otra cosa: encima, debajo, delante, detrás, a la izquierda, a la derecha.",
                 "En la cuadrícula, cuenta los saltos de cuadro en cuadro: 3 a la derecha, 2 hacia arriba.", "Una figura es <b>simétrica</b> si al doblarla por una línea las dos mitades coinciden."]
        ex = [("Salgo de la casilla A y me muevo 2 a la derecha y 1 hacia arriba", ["Cuenta los saltos, no la casilla de salida"], "llego 2 cuadros a la derecha y 1 arriba"), ("Una mariposa", ["Si la doblas por el medio, las alas coinciden"], "es simétrica")]
        kb, ks = "Cuenta saltos, no casillas", "La casilla de salida no se cuenta."
        meta = "Fichas de matemáticas de 2.º de Primaria: posiciones, izquierda y derecha, moverse en una cuadrícula, itinerarios y figuras simétricas. 100 ejercicios con soluciones."
        std = "Localización y desplazamientos: posiciones relativas, itinerarios en cuadrículas; figuras simétricas"
        slug, title, short = "orientacion-en-el-espacio", "Orientación en el espacio", "Orientación"
        sort = 16
    mist = [["Confundir izquierda y derecha", "Mira el dibujo como lo ves tú."], ["Confundir delante y detrás", "Lo que está detrás se ve tapado."], ["Contar la casilla de salida", "Cuenta solo los saltos."]]
    body = lesson(think, ex, mist, P.pic(k_pics.box_scene_svg("ball", "front"), "una pelota delante de una caja"))
    faq = [("¿Cómo sé qué es izquierda y derecha en un dibujo?", "Mira el dibujo de frente, como lo ves tú. La mano con la que escribes te puede ayudar a recordarlo."), ("¿Qué significa «detrás»?", "Que algo está tapado por otra cosa que está delante.")]
    make_unit(R, slug, "E", std, title, short, meta, kb, ks, body, faq, sets, sort, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
