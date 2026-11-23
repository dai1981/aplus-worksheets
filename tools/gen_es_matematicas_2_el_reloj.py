# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: El reloj y el calendario (Sentido de la medida)
build(lv): lv = 1 → en punto y y media, mañana/tarde/noche, días de la semana;
lv = 2 → también y cuarto y menos cuarto, el reloj digital, meses del año, una hora más tarde.
Errores: confundir las agujas, leer «menos cuarto» con la hora siguiente, olvidar el orden de los días.
"""
import random
from es_common import mcq, mix, lesson, make_unit, reloj
from gen_es_matematicas_4_el_tiempo_y_el_reloj import dicho

R = None
LV = 2
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def leer(ms):
    def mk():
        h = R.randint(1, 12)
        m = R.choice(ms)
        ok = dicho(h, m)
        sw = (m // 5) % 12 or 12
        cands = [dicho(sw, (h % 12) * 5) if (h % 12) * 5 in (0, 15, 30, 45) else None, dicho(h % 12 + 1, m), dicho(h - 1 if h > 1 else 12, m)]
        cands += [dicho(h, x) for x in (0, 15, 30, 45) if x != m]
        return mcq(reloj(h, m, 150) + "¿Qué hora marca el reloj?", ok, cands, "La aguja corta marca la hora y la larga, los minutos: <b>%s</b>." % ok)
    mk.__name__ = "leer_%s" % ms
    return mk


def digital():
    h = R.randint(1, 12)
    m = R.choice([0, 30] if LV == 1 else [0, 15, 30, 45])
    ok = dicho(h, m)
    d = "%d:%02d" % (h, m)
    cands = [dicho(h % 12 + 1, m), dicho(h - 1 if h > 1 else 12, m)] + [dicho(h, x) for x in (0, 15, 30, 45) if x != m]
    if (h % 12) * 5 in (0, 15, 30, 45):
        cands.insert(0, dicho(m // 5 or 12, (h % 12) * 5))
    return mcq("El reloj digital marca <b>%s</b>. ¿Qué hora es?" % d, ok, cands, "%s son <b>%s</b>." % (d, ok))


def agujas(m):
    def mk():
        h = R.randint(1, 12)
        pos = {0: "en el 12", 15: "en el 3", 30: "en el 6", 45: "en el 9"}
        if R.random() < 0.5:
            ok = pos[m]
            return mcq("Son %s. ¿Dónde está la aguja larga?" % dicho(h, m), ok, [x for x in pos.values() if x != ok], "La aguja larga marca los minutos: está <b>%s</b>." % ok)
        if m == 0:
            ok = "en el %d" % h
            w = ["en el %d" % (h % 12 + 1), "en el %d" % (h - 1 if h > 1 else 12), "en el 12", "en el 6"]
        else:
            nx = h % 12 + 1
            ok = "entre el %d y el %d" % (h, nx)
            w = ["en el %d" % h, "en el %d" % nx, "entre el %d y el %d" % (h - 1 if h > 1 else 12, h)]
        return mcq("Son %s. ¿Dónde está la aguja corta?" % dicho(h, m), ok, w, "La aguja corta marca la hora: <b>%s</b>." % ok)
    mk.__name__ = "agujas_%d" % m
    return mk


def despues():
    h = R.randint(1, 11)
    m = R.choice([0, 30] if LV == 1 else [0, 15, 30, 45])
    k = R.choice([1, 1, 2]) if LV == 2 else 1
    h2 = (h + k - 1) % 12 + 1
    ok = dicho(h2, m)
    pal = "una hora" if k == 1 else "dos horas"
    return mcq(reloj(h, m, 150) + "¿Qué hora será %s más tarde?" % pal, ok, [dicho(h, m), dicho((h + k) % 12 + 1, m), dicho(h - 1 if h > 1 else 12, m), dicho(h2, (m + 30) % 60)],
               "La aguja corta avanza %s: <b>%s</b>." % ("un número" if k == 1 else "dos números", ok))


def momento():
    q, a, w = R.choice([("¿Cuándo desayunas normalmente?", "por la mañana", ["por la noche", "a mediodía", "por la tarde"]),
                        ("¿Cuándo te vas a dormir?", "por la noche", ["por la mañana", "a mediodía", "al amanecer"]),
                        ("¿Cuándo empiezan las clases en el colegio?", "por la mañana", ["por la noche", "a medianoche", "de madrugada"]),
                        ("¿Cuándo se ve la luna y las estrellas?", "por la noche", ["por la mañana", "a mediodía", "después de desayunar"]),
                        ("¿Qué haces primero?", "levantarme", ["cenar", "irme a dormir", "merendar"]),
                        ("¿Qué haces después de cenar?", "irme a dormir", ["desayunar", "ir al colegio", "levantarme"]),
                        ("¿Qué dura más?", "un día", ["una hora", "un minuto", "un segundo"]),
                        ("¿Qué dura menos?", "un minuto", ["una hora", "un día", "una semana"]),
                        ("¿Qué tarda más o menos un minuto?", "lavarse los dientes", ["dormir por la noche", "ir de vacaciones", "un curso del colegio"]),
                        ("¿Qué dura más o menos una hora?", "una clase de natación", ["parpadear", "un año", "estornudar"]),
                        ("¿Cuántas horas tiene un día?", "24", ["12", "60", "7"]),
                        ("¿Cuántos minutos tiene una hora?", "60", ["100", "24", "30"])])
    if LV == 1 and a in ("24", "60"):
        return None
    return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)


def dias():
    k = R.choice(["despues", "antes", "cuantos", "orden", "finde"] + (["mes_desp", "mes_antes", "meses", "estacion"] if LV == 2 else []))
    i = R.randrange(7)
    if k == "despues":
        return mcq("¿Qué día va después del %s?" % DIAS[i], DIAS[(i + 1) % 7], [DIAS[i - 1], DIAS[(i + 2) % 7], DIAS[(i + 3) % 7]], "Después del %s viene el <b>%s</b>." % (DIAS[i], DIAS[(i + 1) % 7]))
    if k == "antes":
        return mcq("¿Qué día va antes del %s?" % DIAS[i], DIAS[i - 1], [DIAS[(i + 1) % 7], DIAS[i - 2], DIAS[(i + 2) % 7]], "Antes del %s está el <b>%s</b>." % (DIAS[i], DIAS[i - 1]))
    if k == "cuantos":
        q, a, w = R.choice([("¿Cuántos días tiene una semana?", "7", ["5", "10", "12"]), ("¿Cuántos días de la semana vas al colegio?", "5", ["7", "2", "6"]), ("¿Cuántos días tiene el fin de semana?", "2", ["1", "5", "7"])])
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    if k == "orden":
        j = R.randrange(5)
        return mcq("¿Qué día falta? %s, ___, %s" % (DIAS[j], DIAS[j + 2]), DIAS[j + 1], [DIAS[j + 3], DIAS[j - 1], DIAS[(j + 4) % 7]], "Después del %s va el <b>%s</b>." % (DIAS[j], DIAS[j + 1]))
    if k == "finde":
        return mcq("Hoy es %s. ¿Qué día será mañana?" % DIAS[i], DIAS[(i + 1) % 7], [DIAS[i - 1], DIAS[i], DIAS[(i + 2) % 7]], "Mañana es el día siguiente: <b>%s</b>." % DIAS[(i + 1) % 7])
    j = R.randrange(12)
    if k == "mes_desp":
        return mcq("¿Qué mes va después de %s?" % MESES[j], MESES[(j + 1) % 12], [MESES[j - 1], MESES[(j + 2) % 12], MESES[(j + 3) % 12]], "Después de %s viene <b>%s</b>." % (MESES[j], MESES[(j + 1) % 12]))
    if k == "mes_antes":
        return mcq("¿Qué mes va antes de %s?" % MESES[j], MESES[j - 1], [MESES[(j + 1) % 12], MESES[j - 2], MESES[(j + 2) % 12]], "Antes de %s está <b>%s</b>." % (MESES[j], MESES[j - 1]))
    if k == "meses":
        q, a, w = R.choice([("¿Cuántos meses tiene un año?", "12", ["10", "7", "24"]), ("¿Cuál es el primer mes del año?", "enero", ["diciembre", "marzo", "septiembre"]),
                            ("¿Cuál es el último mes del año?", "diciembre", ["enero", "noviembre", "junio"]), ("¿Qué mes tiene menos días?", "febrero", ["enero", "agosto", "diciembre"])])
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    q, a, w = R.choice([("¿En qué estación hace más calor?", "en verano", ["en invierno", "en otoño", "en primavera"]),
                        ("¿En qué estación caen las hojas de muchos árboles?", "en otoño", ["en verano", "en primavera", "en invierno"]),
                        ("¿Cuántas estaciones tiene el año?", "4", ["2", "3", "12"]), ("¿En qué estación salen muchas flores?", "en primavera", ["en invierno", "en otoño", "en verano"])])
    return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30013 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("Las horas en punto", mix(R, seen, [(leer([0]), 12), (agujas(0), 8)])), ("Las horas y media", mix(R, seen, [(leer([30]), 12), (agujas(30), 8)])),
                ("El reloj digital y el día", mix(R, seen, [(digital, 12), (momento, 8)])), ("Los días de la semana", mix(R, seen, [(dias, 20)])), ("Una hora más tarde", mix(R, seen, [(despues, 20)]))]
        think = ["La aguja <b>corta</b> marca la hora. La aguja <b>larga</b> marca los minutos.", "Si la aguja larga está en el 12, es la hora <b>en punto</b>. Si está en el 6, es la hora <b>y media</b>.",
                 "La semana tiene 7 días: lunes, martes, miércoles, jueves, viernes, sábado y domingo."]
        ex = [("La corta en el 4 y la larga en el 12", ["En punto"], "las cuatro en punto"), ("La corta entre el 7 y el 8 y la larga en el 6", ["Y media"], "las siete y media")]
        mist = [["Confundir las agujas", "La corta es la hora."], ["Leer la hora siguiente en «y media»", "A las siete y media, la corta aún no ha llegado al 8."], ["Saltarse un día", "Repite los días en orden."]]
        kb, ks = "La aguja corta marca la hora", "Larga en el 12: en punto."
        meta = "Fichas de matemáticas de 1.º de Primaria: el reloj en punto y y media, mañana, tarde y noche y los días de la semana. 100 ejercicios con soluciones."
        std = "La hora en punto y la media hora en relojes de agujas; momentos del día; días de la semana"
        slug, title, short = "el-reloj", "El reloj y los días", "El reloj"
    else:
        sets = [("En punto y y media", mix(R, seen, [(leer([0, 30]), 20)])), ("Y cuarto y menos cuarto", mix(R, seen, [(leer([15, 45]), 20)])),
                ("El reloj digital", mix(R, seen, [(digital, 20)])), ("Días, meses y estaciones", mix(R, seen, [(dias, 20)])), ("Más tarde y cuánto dura", mix(R, seen, [(despues, 14), (momento, 6)]))]
        think = ["La aguja <b>corta</b> marca la hora y la <b>larga</b>, los minutos.", "Larga en el 12: en punto. En el 3: y cuarto. En el 6: y media. En el 9: menos cuarto.",
                 "«Menos cuarto» quiere decir que falta un cuarto de hora para la hora siguiente: las 4 menos cuarto son las 3:45.", "1 hora = 60 minutos. El año tiene 12 meses."]
        ex = [("La larga en el 3 y la corta un poco pasada del 5", ["Y cuarto"], "las cinco y cuarto"), ("La larga en el 9 y la corta casi en el 8", ["Falta un cuarto para las 8"], "las ocho menos cuarto")]
        mist = [["Confundir las agujas", "La corta es la hora."], ["Leer «menos cuarto» con la hora anterior", "Si la corta casi llega al 8, son las 8 menos cuarto."], ["Leer 3:15 como «las tres y quince» o «las tres y tres»", "3:15 son las tres y cuarto."]]
        kb, ks = "Larga en el 3: y cuarto", "En el 6: y media. En el 9: menos cuarto."
        meta = "Fichas de matemáticas de 2.º de Primaria: el reloj en punto, y cuarto, y media y menos cuarto, el reloj digital, días y meses. 100 ejercicios con soluciones."
        std = "Lectura del reloj analógico y digital: en punto, y cuarto, y media y menos cuarto; días de la semana, meses y estaciones"
        slug, title, short = "el-reloj-y-el-calendario", "El reloj y el calendario", "El reloj"
    body = lesson(think, ex, mist, reloj(7, 30))
    faq = [("¿Qué aguja marca la hora?", "La aguja corta. La aguja larga marca los minutos."), ("¿Qué hora es si la aguja larga está en el 6?", "Es la hora y media: la aguja corta está entre dos números.")]
    make_unit(R, slug, "M", std, title, short, meta, kb, ks, body, faq, sets, 9 if lv == 1 else 12, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
