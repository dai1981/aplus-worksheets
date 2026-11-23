# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: El tiempo y el reloj (Sentido de la medida)
Leer el reloj de agujas y el digital (en punto, y cuarto, y media, menos cuarto, de 5 en 5 minutos y minuto a minuto),
la hora de 24 horas (17:30 = las cinco y media de la tarde), horas, minutos y segundos, duraciones,
días, semanas, meses, años, décadas y siglos, problemas de horarios.
Errores: confundir la aguja larga y la corta, leer «menos cuarto» con la hora equivocada, contar 100 minutos en una hora.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, hora, dur, reloj, bank, POR, Kids

R = random.Random(44016)
K = Kids(R)
NUM = ["doce", "una", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce"]
MIN = {5: "cinco", 10: "diez", 15: "cuarto", 20: "veinte", 25: "veinticinco", 30: "media"}


def dicho(h, m):
    """«las tres y cuarto», «las cuatro menos veinte», «la una en punto»"""
    h12 = h % 12
    if m <= 30:
        art = "la" if h12 == 1 else "las"
        if m == 0:
            return "%s %s en punto" % (art, NUM[h12])
        return "%s %s y %s" % (art, NUM[h12], MIN.get(m, str(m)))
    h2 = (h + 1) % 12
    art = "la" if h2 == 1 else "las"
    return "%s %s menos %s" % (art, NUM[h2], MIN.get(60 - m, str(60 - m)))


def parte(h):
    return "de la madrugada" if h < 6 else "de la mañana" if h < 12 else "del mediodía" if h < 14 else "de la tarde" if h < 21 else "de la noche"


def s1_agujas():
    h = R.randint(1, 12)
    m = R.choice([0, 15, 30, 45, 5, 10, 20, 25, 35, 40, 50, 55])
    ws = [dicho(h, (m + 30) % 60) if m not in (0, 30) else dicho(h % 12 + 1, m), dicho((h + 1) % 12 or 12, m) if m < 30 else dicho(h - 1 if h > 1 else 12, m),
          dicho(m // 5 if m // 5 else 12, h * 5 % 60), dicho(h, (m + 5) % 60) if m != 55 else dicho(h, 50)]
    return mcq(reloj(h, m) + "¿Qué hora marca el reloj?", dicho(h, m), ws,
               "La aguja corta marca la hora y la larga, los minutos: <b>%s</b>." % dicho(h, m))


def s1_digital():
    h = R.randint(1, 12)
    m = R.choice([0, 15, 30, 45, 5, 10, 20, 25, 35, 40, 50, 55])
    k = R.choice(["a_dicho", "a_dig"])
    if k == "a_dicho":
        return mcq("El reloj digital marca %s. ¿Cómo lo dices?" % hora(h, m), dicho(h, m), [dicho(h - 1 if h > 1 else 12, m) if m > 30 else dicho(h % 12 + 1, m), dicho(h, 60 - m) if m not in (0, 30) else dicho(h, 15), dicho(m // 5 or 12, h * 5 % 60)],
                   "%s = <b>%s</b>." % (hora(h, m), dicho(h, m)))
    return mcq("¿Cómo se escribe en un reloj digital «%s»?" % dicho(h, m), hora(h, m), [hora(h - 1 if h > 1 else 12, m) if m > 30 else hora(h % 12 + 1, m), hora(h, 60 - m) if m not in (0, 30) else hora(h, 15), hora(h, m // 5) if m >= 10 else hora(h, 50)],
               "«%s» = <b>%s</b>." % (dicho(h, m), hora(h, m)))


def s2_24():
    h = R.randint(13, 23)
    m = R.choice([0, 15, 30, 45, 10, 20, 40, 50])
    k = R.choice(["a12", "a24"])
    if k == "a12":
        return mcq("Son las %s. ¿Cómo lo dices?" % hora(h, m), "%s %s" % (dicho(h, m), parte(h if m <= 30 else h + 1)),
                   ["%s %s" % (dicho(h, m), "de la mañana"), "%s %s" % (dicho(h - 10, m), parte(h)), "%s %s" % (dicho(h - 2, m), parte(h))],
                   "%d − 12 = %d: <b>%s %s</b>." % (h, h - 12, dicho(h, m), parte(h if m <= 30 else h + 1)))
    return mcq("Un tren sale a %s %s. ¿Qué hora es en el horario de 24 horas?" % (dicho(h, m), parte(h if m <= 30 else h + 1)), hora(h, m),
               [hora(h - 12, m), hora(h + 1, m) if h < 23 else hora(h - 1, m), hora(h - 10, m), hora(h, 60 - m) if m not in (0, 30) else hora(h, 45)],
               "Por la tarde y por la noche sumamos 12 a la hora: <b>%s</b>." % hora(h, m))


def s3_unidades():
    k = R.choice(["h_min", "min_h", "min_s", "hm", "dia", "bank"])
    if k == "h_min":
        h = R.randint(2, 9)
        return mcq("¿Cuántos minutos son %d horas?" % h, "%d min" % (h * 60), ["%d min" % (h * 100), "%d min" % (h * 10), "%d min" % (h * 60 + 60), "%d min" % (h * 30)], "1 h = 60 min; %d %s 60 = <b>%d min</b>." % (h, POR, h * 60))
    if k == "min_h":
        h = R.randint(2, 9)
        return mcq("¿Cuántas horas son %d minutos?" % (h * 60), "%d h" % h, ["%d h" % (h * 6), "%d h" % (h * 60 // 100) if h * 60 // 100 != h else "%d h" % (h + 1), "%d h" % (h * 10), "%d h" % (h + 1)], "%d : 60 = <b>%d h</b>." % (h * 60, h))
    if k == "min_s":
        m = R.randint(2, 10)
        return mcq("¿Cuántos segundos son %d minutos?" % m, "%d s" % (m * 60), ["%d s" % (m * 100), "%d s" % (m * 10), "%d s" % (m * 60 + 60), "%d s" % (m * 30)], "1 min = 60 s: <b>%d s</b>." % (m * 60))
    if k == "hm":
        h, m = R.randint(1, 4), R.randint(5, 55)
        return mcq("¿Cuántos minutos son %d h y %d min?" % (h, m), "%d min" % (h * 60 + m), ["%d min" % (h * 100 + m), "%d min" % (h + m), "%d min" % (h * 60 + m + 60), "%d min" % (h * 10 + m)],
                   "%d h = %d min; %d + %d = <b>%d min</b>." % (h, h * 60, h * 60, m, h * 60 + m))
    if k == "dia":
        d = R.randint(2, 7)
        return mcq("¿Cuántas horas son %d días?" % d, "%d h" % (d * 24), ["%d h" % (d * 12), "%d h" % (d * 60), "%d h" % (d * 24 + 24), "%d h" % (d * 100)], "1 día = 24 h: <b>%d h</b>." % (d * 24))
    return bank(R, [
        ("¿Cuántos días tiene una semana?", "7", ["5", "10", "30"]),
        ("¿Cuántos meses tiene un año?", "12", ["10", "52", "365"]),
        ("¿Cuántos días tiene un año que no es bisiesto?", "365", ["366", "360", "300"]),
        ("¿Cuántos años tiene una década?", "10", ["100", "12", "1000"]),
        ("¿Cuántos años tiene un siglo?", "100", ["10", "1000", "50"]),
        ("¿Cuántos días tiene un año bisiesto?", "366", ["365", "364", "360"]),
        ("¿Cuántos días tiene el mes de febrero en un año bisiesto?", "29", ["28", "30", "31"]),
        ("¿Cuántas semanas tiene un año, aproximadamente?", "52", ["12", "48", "100"]),
        ("¿Cuántos días tiene el mes de abril?", "30", ["31", "28", "29"]),
        ("¿Cuántos días tiene el mes de agosto?", "31", ["30", "28", "29"]),
        ("¿Cuántos minutos son media hora?", "30", ["50", "15", "60"]),
        ("¿Cuántos minutos son un cuarto de hora?", "15", ["25", "4", "45"]),
        ("¿Cuántos minutos son tres cuartos de hora?", "45", ["75", "34", "30"]),
        ("¿Cuántos años tiene un milenio?", "1000", ["100", "10", "10 000"]),
    ], "cal")()


def s4_duracion():
    h1 = R.randint(8, 18)
    m1 = R.choice([0, 10, 15, 20, 30, 40, 45])
    d = R.choice([25, 35, 40, 45, 50, 70, 80, 85, 95, 105, 120, 135, 150])
    t2 = h1 * 60 + m1 + d
    h2, m2 = divmod(t2, 60)
    k = R.choice(["fin", "dur", "ini"])
    if k == "fin":
        return mcq("Una película empieza a las %s y dura %s. ¿A qué hora termina?" % (hora(h1, m1), dur(d)), hora(h2, m2),
                   [hora(h1 + d // 100, m1 + d % 100) if m1 + d % 100 < 60 else hora(h2 + 1, m2), hora(h2 + 1, m2), hora(h2, (m2 + 10) % 60), hora(h2 - 1, m2)],
                   "%s + %s = <b>%s</b>." % (hora(h1, m1), dur(d), hora(h2, m2)))
    if k == "dur":
        return mcq("El tren sale a las %s y llega a las %s. ¿Cuánto dura el viaje?" % (hora(h1, m1), hora(h2, m2)), dur(d),
                   [dur(d + 40) if (h2 * 100 + m2) - (h1 * 100 + m1) != d else dur(d + 60), dur(d - 10), dur(d + 10), dur((h2 - h1) * 60)],
                   "De %s a %s pasan <b>%s</b>." % (hora(h1, m1), hora(h2, m2), dur(d)))
    return mcq("Un partido termina a las %s y ha durado %s. ¿A qué hora empezó?" % (hora(h2, m2), dur(d)), hora(h1, m1),
               [hora(h1 - 1, m1), hora(h1 + 1, m1), hora(h1, (m1 + 10) % 60), hora(h2, m1)],
               "%s − %s = <b>%s</b>." % (hora(h2, m2), dur(d), hora(h1, m1)))


def s5_problema():
    p, g = K.next()
    k = R.choice(["cole", "sueno", "semana", "siglo", "edad", "carrera", "tren"])
    if k == "cole":
        h, m = 9, 0
        e = R.choice([(14, 0), (13, 30), (14, 30), (16, 0), (16, 30)])
        d = e[0] * 60 + e[1] - 9 * 60
        return mcq("Las clases empiezan a las 9:00 y terminan a las %s. ¿Cuánto tiempo está %s en el colegio?" % (hora(*e), p), dur(d), [dur(d + 60), dur(d - 30), dur(d + 30), "%d h" % (e[0] - 9 + 12)],
                   "De las 9:00 a las %s: <b>%s</b>." % (hora(*e), dur(d)))
    if k == "sueno":
        a = R.choice([(21, 30), (22, 0), (21, 0), (22, 30)])
        b = R.choice([(7, 0), (7, 30), (8, 0)])
        d = (24 * 60 - a[0] * 60 - a[1]) + b[0] * 60 + b[1]
        return mcq("%s se acuesta a las %s y se levanta a las %s. ¿Cuánto tiempo duerme?" % (p, hora(*a), hora(*b)), dur(d), [dur(d - 60), dur(d + 60), dur(abs(a[0] - b[0]) * 60), dur(d + 30)],
                   "Hasta las 24:00 hay %s y después %s más: <b>%s</b>." % (dur(24 * 60 - a[0] * 60 - a[1]), dur(b[0] * 60 + b[1]), dur(d)))
    if k == "semana":
        w = R.randint(2, 12)
        return mcq("Las vacaciones de %s duran %d semanas. ¿Cuántos días son?" % (p, w), "%d días" % (w * 7), ["%d días" % (w * 5), "%d días" % (w * 10), "%d días" % (w * 7 + 7), "%d días" % (w * 30)],
                   "%d %s 7 = <b>%d días</b>." % (w, POR, w * 7))
    if k == "siglo":
        y = R.choice([1492, 1605, 1808, 1936, 1978, 1714, 1898, 2001, 1561, 1212])
        s = (y - 1) // 100 + 1
        return mcq("¿En qué siglo fue el año %d?" % y, "en el siglo %d" % s, ["en el siglo %d" % (s - 1), "en el siglo %d" % (s + 1), "en el siglo %d" % (y // 10)],
                   "Del año %d01 al %d00 es el siglo %d: <b>siglo %d</b>." % (s - 1, s, s, s))
    if k == "edad":
        y = R.randint(2015, 2018)
        return mcq("%s nació en %d. ¿Cuántos años cumple en 2026?" % (p, y), "%d años" % (2026 - y), ["%d años" % (2026 - y + 1), "%d años" % (2026 - y - 1), "%d años" % (y - 2000), "%d años" % (2026 - y + 10)],
                   "2026 − %d = <b>%d años</b>." % (y, 2026 - y))
    if k == "carrera":
        a = R.randint(40, 59)
        b = R.randint(5, 50)
        return mcq("%s tarda %d segundos en dar una vuelta a la pista y su amigo %d segundos más. ¿Cuánto tarda su amigo?" % (p, a, b), "%d min y %d s" % divmod(a + b, 60) if a + b >= 60 else "%d s" % (a + b),
                   ["%d min y %d s" % ((a + b) // 100, (a + b) % 100) if a + b >= 100 else "%d s" % (a + b + 10), "%d s" % (a - b), "%d min y %d s" % (1, a + b - 50) if a + b >= 60 else "%d s" % (a + b - 1), "%d min" % (a + b)],
                   "%d + %d = %d s%s." % (a, b, a + b, " = <b>%d min y %d s</b>" % divmod(a + b, 60) if a + b >= 60 else "")) if (a + b) % 60 else None
    h1 = R.randint(7, 19)
    m1 = R.choice([5, 15, 25, 35, 45])
    d = R.choice([75, 95, 110, 125, 140])
    t = h1 * 60 + m1 + d
    if t >= 24 * 60:
        return None
    return mcq("Un AVE sale de Madrid a las %s y tarda %s en llegar a Sevilla. ¿A qué hora llega?" % (hora(h1, m1), dur(d)), hora(*divmod(t, 60)),
               [hora(*divmod(t + 60, 60)), hora(*divmod(t - 10, 60)), hora(h1 + d // 100, (m1 + d % 100) % 60), hora(*divmod(t + 40, 60))],
               "%s + %s = <b>%s</b>." % (hora(h1, m1), dur(d), hora(*divmod(t, 60))))


def main():
    seen = set()
    sets = [
        ("El reloj de agujas", mix(R, seen, [(s1_agujas, 20)])),
        ("El reloj digital y las 24 horas", mix(R, seen, [(s1_digital, 10), (s2_24, 10)])),
        ("Horas, minutos, segundos y calendario", mix(R, seen, [(s3_unidades, 20)])),
        ("Duraciones", mix(R, seen, [(s4_duracion, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["En el reloj de agujas, la aguja <b>corta</b> marca la hora y la <b>larga</b>, los minutos. Cada número de la esfera son 5 minutos.",
         "Hasta la media decimos «y» (las tres y diez); después de la media decimos «menos» y la hora siguiente (las cuatro menos veinte = 3:40).",
         "El día tiene 24 horas. Por la tarde, sumamos 12: las cinco de la tarde son las 17:00.",
         "1 h = 60 min; 1 min = 60 s; 1 día = 24 h; 1 año = 12 meses = 365 días; 1 siglo = 100 años."],
        [("¿Qué hora es 15:45?", ["15 − 12 = 3", "45 min = menos cuarto de la siguiente hora"], "las cuatro menos cuarto de la tarde"),
         ("De 10:40 a 12:15, ¿cuánto pasa?", ["De 10:40 a 11:00, 20 min", "De 11:00 a 12:15, 1 h 15 min"], "1 h 35 min")],
        [["Confundir las agujas", "La corta es la hora; la larga, los minutos."],
         ["Leer mal «menos cuarto»", "Las cuatro menos cuarto son las 3:45, no las 4:45."],
         ["Contar 100 minutos en una hora", "Una hora tiene 60 minutos: 10:50 + 20 min = 11:10."]],
        reloj(3, 40))
    faq = [("¿Cómo se pasa de la hora de 12 a la de 24 horas?", "Por la mañana la hora es la misma (las 9 de la mañana = 9:00); por la tarde y por la noche se suman 12 (las 9 de la noche = 21:00)."),
           ("¿Cómo se calcula cuánto dura algo?", "Se cuenta desde la hora de inicio hasta la siguiente hora en punto, después las horas completas y por último los minutos que faltan.")]
    make_unit(R, "el-tiempo-y-el-reloj", "M",
              "Medida del tiempo: lectura de relojes analógicos y digitales; unidades de tiempo (segundo, minuto, hora, día, semana, mes, año, década y siglo) y sus equivalencias; cálculo de duraciones; resolución de problemas",
              "El tiempo y el reloj", "El tiempo y el reloj",
              "Fichas de matemáticas de 4.º de Primaria: leer el reloj de agujas y el digital, la hora de 24 horas, horas, minutos y segundos, duraciones, calendario y siglos. 100 ejercicios con soluciones.",
              "Aguja corta: horas; larga: minutos", "1 h = 60 min. Por la tarde, suma 12.",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
