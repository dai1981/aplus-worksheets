# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Patrones y series (Sentido algebraico)
build(lv): lv = 1 → series que se repiten con dibujos y figuras, contar de 1 en 1, de 2 en 2, de 5 en 5 y de 10 en 10 hasta 99, igualdades sencillas;
lv = 2 → también la regla de la serie (sumar o restar 2, 3, 5, 10 o 100) hasta 999 y el número que falta para que los dos lados valgan lo mismo.
Errores: mirar solo los dos primeros elementos, contar mal el grupo que se repite, pensar que = significa «el resultado es».
"""
import random
from es_common import mcq, mix, lesson, make_unit
from f_common import pattern_svg
import es_pics as P

R = None
LV = 2
SHAPES = {"circle": ("círculo", "m"), "square": ("cuadrado", "m"), "triangle": ("triángulo", "m")}
COLORS = {"red": ("rojo", "roja"), "blue": ("azul", "azul"), "yellow": ("amarillo", "amarilla"), "green": ("verde", "verde")}


def nombre(it):
    if it[0] == "obj":
        return P.nombre(it[1], 1)
    return "%s %s" % (SHAPES[it[1]][0], COLORS[it[2]][0])


def unidad():
    k = R.choice(["obj", "shape", "shape"])
    n = R.choice([2, 2, 3, 3] + ([4] if LV == 2 else []))
    if k == "obj":
        kinds = R.sample(P.KINDS, n if n < 4 else 3)
        if n == 4:
            kinds = kinds + [kinds[0]]
        return [("obj", x) for x in kinds]
    pool = [(s, c) for s in SHAPES for c in COLORS]
    picks = R.sample(pool, min(n, 3))
    if n == 4:
        picks = picks + [picks[1]]
    if len(set(picks)) < 2:
        return None
    return [("shape", s, c) for s, c in picks]


def s_siguiente():
    u = unidad()
    if not u:
        return None
    L = len(u)
    shown = R.randint(L + 1, min(9, 2 * L + 2))
    seq = [u[i % L] for i in range(shown)]
    ok = u[shown % L]
    names = list(dict.fromkeys(nombre(x) for x in u))
    w = [x for x in names if x != nombre(ok)]
    extra = ["estrella", "corazón", "flor", "hexágono azul", "pelota"]
    return mcq(P.pic(pattern_svg(seq, 1), "una serie que se repite") + "¿Qué va en el hueco?", nombre(ok), w + extra, "Se repite: %s. Después va <b>%s</b>." % (", ".join(nombre(x) for x in u), nombre(ok)))


def s_grupo():
    u = unidad()
    if not u:
        return None
    L = len(u)
    seq = [u[i % L] for i in range(2 * L + R.randint(0, L - 1))]
    return mcq(P.pic(pattern_svg(seq), "una serie que se repite") + "¿Cuántos elementos tiene el grupo que se repite?", str(L), [str(x) for x in (1, 2, 3, 4, 5) if x != L], "El grupo %s se repite: tiene <b>%d</b> elementos." % (", ".join(nombre(x) for x in u), L))


def s_serie():
    step = R.choice([1, 2, 5, 10] if LV == 1 else [2, 3, 5, 10, 100, 4])
    down = LV == 2 and R.random() < 0.35
    top = 99 if LV == 1 else 999
    if step == 100:
        a = R.randint(1, 5) * 100 + R.randint(0, 99)
    elif step == 1:
        a = R.randint(10, 90)
    else:
        a = R.randint(0, top // 2) // step * step + (0 if R.random() < 0.6 or step in (2, 5) and LV == 1 else R.randint(1, step - 1))
    seq = [a + i * step for i in range(5)]
    if down:
        seq = seq[::-1]
    if max(seq) > top or min(seq) < 0:
        return None
    hole = R.randint(2, 4)
    ok = seq[hole]
    shown = ", ".join("___" if i == hole else str(x) for i, x in enumerate(seq))
    return mcq("¿Qué número falta? %s" % shown, str(ok), [str(ok + 1), str(ok - 1), str(ok + step) if ok + step not in seq else str(ok + 2 * step), str(ok + 10)],
               "%s de %d en %d: <b>%d</b>." % ("Va hacia atrás" if down else "Contamos", step, step, ok))


def s_regla():
    step = R.choice([2, 3, 5, 10, 100])
    down = R.random() < 0.4
    a = R.randint(100, 500) if step == 100 else R.randint(10, 300)
    seq = [a + i * step for i in range(4)]
    if down:
        seq = seq[::-1]
    ok = "%s %d" % ("restar" if down else "sumar", step)
    return mcq("¿Cuál es la regla de la serie? %s, …" % ", ".join(map(str, seq)), ok, ["%s %d" % ("sumar" if down else "restar", step), "%s %d" % ("restar" if down else "sumar", step + 1 if step != 100 else 10), "%s %d" % ("restar" if down else "sumar", step * 2)],
               "Cada número es %d %s que el anterior: <b>%s</b>." % (step, "menos" if down else "más", ok))


def s_igual():
    top = 10 if LV == 1 else 50
    a, b = R.randint(1, top), R.randint(1, top)
    c = R.randint(1, a + b - 1)
    d = a + b - c
    if d <= 0:
        return None
    t = R.choice(["hueco", "vf"])
    if t == "hueco":
        return mcq("¿Qué número hace que los dos lados valgan lo mismo? %d + %d = %d + ___" % (a, b, c), str(d), [str(a + b), str(d + 1), str(a + b + c)], "%d + %d = %d y %d + %d = %d: <b>%d</b>." % (a, b, a + b, c, d, a + b, d))
    ok = R.random() < 0.5
    dd = d if ok else d + R.choice([1, 2, -1]) if d > 2 else d + 1
    return mcq("¿Es verdad? %d + %d = %d + %d" % (a, b, c, dd), "sí" if ok else "no", ["no" if ok else "sí", "solo a veces", "no se puede saber"],
               "%d + %d = %d y %d + %d = %d: <b>%s</b>." % (a, b, a + b, c, dd, c + dd, "sí, valen lo mismo" if ok else "no, no valen lo mismo"))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30010 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("¿Qué va después?", mix(R, seen, [(s_siguiente, 20)])), ("El grupo que se repite", mix(R, seen, [(s_grupo, 12), (s_siguiente, 8)])), ("Contar hacia delante", mix(R, seen, [(s_serie, 20)])),
                ("Series de números", mix(R, seen, [(s_serie, 20)])), ("¿Valen lo mismo?", mix(R, seen, [(s_igual, 20)]))]
        think = ["En una <b>serie</b>, un grupo se repite una y otra vez: rojo, azul, rojo, azul…", "Para saber qué va después, busca el grupo que se repite y señálalo con el dedo.",
                 "Con números, mira cuánto aumenta cada vez: 10, 20, 30… va de 10 en 10.", "El signo <b>=</b> dice que los dos lados valen lo mismo: 4 + 1 = 3 + 2."]
        ex = [("Rojo, azul, rojo, azul, rojo, …", ["Se repite rojo, azul"], "azul"), ("5, 10, 15, ___", ["De 5 en 5"], "20")]
        kb, ks = "Busca el grupo que se repite", "Señálalo con el dedo."
        meta = "Fichas de matemáticas de 1.º de Primaria: series que se repiten con dibujos, contar de 2 en 2, de 5 en 5 y de 10 en 10 y el signo igual. 100 ejercicios con soluciones."
        std = "Patrones de repetición con objetos y figuras; series numéricas sencillas; el signo igual"
        sort = 7
    else:
        sets = [("Series con figuras", mix(R, seen, [(s_siguiente, 14), (s_grupo, 6)])), ("¿Qué número falta?", mix(R, seen, [(s_serie, 20)])), ("La regla de la serie", mix(R, seen, [(s_regla, 20)])),
                ("Series hacia delante y hacia atrás", mix(R, seen, [(s_serie, 20)])), ("Los dos lados valen lo mismo", mix(R, seen, [(s_igual, 20)]))]
        think = ["En una <b>serie</b> todo sigue la misma <b>regla</b>: sumar 2, restar 10, repetir un grupo de figuras…", "Comprueba la regla con todos los números, no solo con los dos primeros.",
                 "El signo <b>=</b> dice que los dos lados valen lo mismo: 12 + 3 = 10 + 5."]
        ex = [("350, 450, 550, ___", ["Suma 100"], "650"), ("8 + 7 = 10 + ___", ["8 + 7 = 15", "10 + 5 = 15"], "5")]
        kb, ks = "Busca la regla y compruébala", "= significa «vale lo mismo»."
        meta = "Fichas de matemáticas de 2.º de Primaria: series con figuras, el número que falta, la regla de la serie y el signo igual. 100 ejercicios con soluciones."
        std = "Patrones de repetición y series numéricas (sumar o restar una cantidad); el signo igual como equivalencia"
        sort = 9
    mist = [["Mirar solo los dos primeros", "Comprueba el patrón hasta el final."], ["Contar mal el grupo que se repite", "Marca dónde empieza y acaba el grupo."], ["Pensar que = es «el resultado es»", "En 4 + 1 = 3 + ___, el hueco es 2."]]
    pic = P.pic(pattern_svg([("shape", "circle", "red"), ("shape", "square", "blue")] * 3, 1), "una serie que se repite")
    body = lesson(think, ex, mist, pic)
    faq = [("¿Qué es una serie?", "Una fila de números, figuras o dibujos que sigue una regla, por ejemplo repetir un grupo o sumar siempre lo mismo."), ("¿Qué significa el signo igual?", "Que lo que hay a un lado vale lo mismo que lo que hay al otro.")]
    make_unit(R, "patrones-y-series", "A", std, "Patrones y series", "Patrones", meta, kb, ks, body, faq, sets, sort, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
