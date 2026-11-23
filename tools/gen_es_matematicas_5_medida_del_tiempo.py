# -*- coding: utf-8 -*-
"""
España Matemáticas 5.º de Primaria: Medida del tiempo (Sentido de la medida)
Horas, minutos y segundos (1 h = 60 min = 3600 s), forma compleja e incompleja, sumar y restar tiempos,
horario de 24 horas, duraciones y horarios de trenes y autobuses, días, años, décadas, siglos y milenios.
Errores: pasar de minutos a horas dividiendo entre 100, sumar 1:50 + 0:20 como 1:70, contar mal los siglos.
"""
import random
from es_c3 import M, mix, lesson, make_unit, num, table
from es_common import hora, dur

R = None


def hms(h, m, s=0):
    out = []
    if h:
        out.append("%d h" % h)
    if m:
        out.append("%d min" % m)
    if s:
        out.append("%d s" % s)
    return " ".join(out) or "0 s"


def s1_unidades():
    k = R.choice(["h_min", "min_s", "h_s", "min_h", "s_min", "dia_h"])
    n = R.randint(2, 9)
    if k == "h_min":
        return M("¿Cuántos minutos son %d horas?" % n, "%d min" % (n * 60), ["%d min" % (n * 100), "%d min" % (n * 10), "%d min" % (n * 3600)], "1 h = 60 min: <b>%d min</b>." % (n * 60))
    if k == "min_s":
        return M("¿Cuántos segundos son %d minutos?" % n, "%d s" % (n * 60), ["%d s" % (n * 100), "%d s" % (n * 10), "%s s" % num(n * 3600)], "1 min = 60 s: <b>%d s</b>." % (n * 60))
    if k == "h_s":
        return M("¿Cuántos segundos son %d horas?" % n, "%s s" % num(n * 3600), ["%d s" % (n * 60), "%s s" % num(n * 1000), "%s s" % num(n * 360)], "1 h = 60 × 60 = 3600 s: <b>%s s</b>." % num(n * 3600))
    if k == "min_h":
        return M("¿Cuántas horas son %d minutos?" % (n * 60), "%d h" % n, ["%d h" % (n * 6), "%s h" % num(n * 60 // 100) if n * 60 // 100 != n else "%d h" % (n + 1), "%d h" % (n * 10)], "%d : 60 = <b>%d h</b>." % (n * 60, n))
    if k == "s_min":
        return M("¿Cuántos minutos son %d segundos?" % (n * 60), "%d min" % n, ["%d min" % (n * 6), "%d min" % (n * 10), "%d min" % (n + 1)], "%d : 60 = <b>%d min</b>." % (n * 60, n))
    return M("¿Cuántas horas tienen %d días?" % n, "%d h" % (n * 24), ["%d h" % (n * 12), "%d h" % (n * 60), "%d h" % (n * 24 + 24)], "1 día = 24 h: <b>%d h</b>." % (n * 24))


def s2_compleja():
    k = R.choice(["a_incomp", "a_comp", "a_comp_s"])
    h, m = R.randint(1, 5), R.randint(5, 55)
    if k == "a_incomp":
        return M("¿Cuántos minutos son %s?" % hms(h, m), "%d min" % (h * 60 + m), ["%d min" % (h * 100 + m), "%d min" % (h + m), "%d min" % (h * 60 + m + 60)], "%d × 60 + %d = <b>%d min</b>." % (h, m, h * 60 + m))
    if k == "a_comp":
        t = h * 60 + m
        return M("Expresa %d minutos en horas y minutos." % t, hms(h, m), [hms(t // 100, t % 100) if t >= 100 else hms(h + 1, m), hms(h, m + 10) if m < 50 else hms(h + 1, m - 50), hms(t // 10, t % 10)], "%d : 60 = %d y resto %d: <b>%s</b>." % (t, h, m, hms(h, m)))
    s = R.randint(5, 55)
    t = m * 60 + s
    return M("Expresa %s segundos en minutos y segundos." % num(t), hms(0, m, s), [hms(0, t // 100, t % 100) if t % 100 < 60 else hms(0, m + 1, s), hms(0, m, s + 1), hms(1, m - 60, s) if m > 60 else hms(0, m - 1, s)], "%s : 60 = %d y resto %d: <b>%s</b>." % (num(t), m, s, hms(0, m, s)))


def s3_operar():
    h1, m1, h2, m2 = R.randint(1, 4), R.randint(10, 55), R.randint(0, 3), R.randint(10, 55)
    k = R.choice(["+", "-"])
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    if k == "+":
        t = t1 + t2
        bad = hms(h1 + h2, m1 + m2) if m1 + m2 >= 60 else hms(h1 + h2, m1 + m2 + 10)
        return M("Calcula: %s + %s" % (hms(h1, m1), hms(h2, m2)), hms(t // 60, t % 60), [bad, hms(t // 60 + 1, t % 60), hms(t // 60, (t % 60 + 40) % 60)], "Sumamos y pasamos 60 min a 1 h: <b>%s</b>." % hms(t // 60, t % 60))
    if t1 <= t2:
        t1, t2 = t2, t1
    t = t1 - t2
    if t1 % 60 >= t2 % 60:
        return None
    return M("Calcula: %s − %s" % (hms(t1 // 60, t1 % 60), hms(t2 // 60, t2 % 60)), hms(t // 60, t % 60), [hms(t1 // 60 - t2 // 60, abs(t1 % 60 - t2 % 60)), hms(t // 60 + 1, t % 60), hms(t // 60, (t % 60 + 40) % 60)],
             "Pasamos 1 h a 60 min antes de restar: <b>%s</b>." % hms(t // 60, t % 60))


def s4_horarios():
    k = R.choice(["24", "dur", "llega", "tabla"])
    if k == "24":
        h, m = R.randint(13, 23), R.choice([0, 10, 15, 20, 30, 45, 50])
        pt = "de la tarde" if h < 21 else "de la noche"
        hh = "la 1" if h == 13 else "las %d" % (h - 12)
        txt = "%s y %d %s" % (hh, m, pt) if m else "%s en punto %s" % (hh, pt)
        return M("¿Cómo se escribe en formato de 24 horas «%s»?" % txt, hora(h, m), [hora(h - 12, m), hora(h + 1 if h < 23 else h - 1, m), hora(h - 10, m)],
                 "Por la tarde sumamos 12: <b>%s</b>." % hora(h, m))
    h1, m1 = R.randint(6, 18), R.choice([0, 5, 15, 20, 30, 40, 45, 50])
    dd = R.choice([35, 45, 50, 75, 85, 95, 110, 135, 150, 165])
    t = h1 * 60 + m1 + dd
    if k == "dur":
        return M("Un autobús sale a las %s y llega a las %s. ¿Cuánto dura el viaje?" % (hora(h1, m1), hora(t // 60, t % 60)), dur(dd), [dur(dd + 40) if (t // 60 * 100 + t % 60) - (h1 * 100 + m1) != dd else dur(dd + 60), dur(dd - 10), dur(dd + 10)],
                 "De %s a %s pasan <b>%s</b>." % (hora(h1, m1), hora(t // 60, t % 60), dur(dd)))
    if k == "llega":
        return M("Un tren sale a las %s y el viaje dura %s. ¿A qué hora llega?" % (hora(h1, m1), dur(dd)), hora(t // 60, t % 60), [hora(h1 + dd // 100, (m1 + dd % 100) % 60), hora(t // 60 + 1, t % 60), hora(t // 60, (t % 60 + 10) % 60)],
                 "%s + %s = <b>%s</b>." % (hora(h1, m1), dur(dd), hora(t // 60, t % 60)))
    st = ["Madrid", "Toledo", "Ciudad Real", "Córdoba", "Sevilla"]
    ts = [h1 * 60 + m1]
    for _ in range(4):
        ts.append(ts[-1] + R.choice([25, 30, 35, 40, 50, 55]))
    if ts[-1] >= 24 * 60:
        return None
    tb = table(["Estación"] + st, [["Hora"] + [hora(x // 60, x % 60) for x in ts]])
    i, j = sorted(R.sample(range(5), 2))
    return M(tb + "¿Cuánto tarda el tren de %s a %s?" % (st[i], st[j]), dur(ts[j] - ts[i]), [dur(ts[j] - ts[i] + 10), dur(ts[j] - ts[i] - 10) if ts[j] - ts[i] > 10 else dur(ts[j] - ts[i] + 20), dur(ts[j] - ts[i] + 40)],
             "De %s a %s: <b>%s</b>." % (hora(ts[i] // 60, ts[i] % 60), hora(ts[j] // 60, ts[j] % 60), dur(ts[j] - ts[i])))


def rom(n):
    v = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    s = ""
    for a, r in v:
        while n >= a:
            s += r
            n -= a
    return s


def s5_calendario():
    k = R.choice(["siglo", "siglo", "decadas", "anios", "semanas", "edad", "bisiesto"])
    if k == "siglo":
        y = R.randint(500, 2026)
        sgl = (y - 1) // 100 + 1
        return M("¿En qué siglo está el año %d?" % y, "en el siglo %s" % rom(sgl), ["en el siglo %s" % rom(sgl - 1), "en el siglo %s" % rom(sgl + 1), "en el siglo %s" % rom(y // 100) if y // 100 not in (sgl, sgl - 1, sgl + 1) else "en el siglo %s" % rom(sgl + 2)],
                 "Del año %d01 al %d00 es el siglo %s: <b>siglo %s</b>." % (sgl - 1, sgl, rom(sgl), rom(sgl)))
    if k == "decadas":
        n = R.randint(2, 9)
        return M("¿Cuántos años son %d décadas?" % n, "%d años" % (n * 10), ["%d años" % (n * 100), "%d años" % n, "%d años" % (n * 12)], "1 década = 10 años: <b>%d años</b>." % (n * 10))
    if k == "anios":
        n = R.randint(2, 5)
        return M("¿Cuántos años son %d siglos y medio?" % n, "%d años" % (n * 100 + 50), ["%d años" % (n * 100 + 5), "%d años" % (n * 10 + 5), "%d años" % (n * 100)], "%d × 100 + 50 = <b>%d años</b>." % (n, n * 100 + 50))
    if k == "semanas":
        n = R.randint(3, 12)
        return M("¿Cuántos días son %d semanas?" % n, "%d días" % (n * 7), ["%d días" % (n * 5), "%d días" % (n * 10), "%d días" % (n * 7 + 7)], "%d × 7 = <b>%d días</b>." % (n, n * 7))
    if k == "edad":
        y = R.randint(1900, 1990)
        return M("Un edificio se construyó en %d. ¿Cuántos años cumplirá en 2026?" % y, "%d años" % (2026 - y), ["%d años" % (2026 - y + 1), "%d años" % (2026 - y - 10), "%d años" % (y - 1900)], "2026 − %d = <b>%d años</b>." % (y, 2026 - y))
    y = R.choice([2020, 2024, 2028, 2023, 2025, 2026, 2100, 2000])
    b = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
    return M("¿El año %d es bisiesto (366 días)?" % y, "sí" if b else "no", ["no" if b else "sí", "solo en febrero", "no se puede saber"],
             "Son bisiestos los múltiplos de 4 (salvo los que acaban en 00 y no son múltiplos de 400): <b>%s</b>." % ("sí" if b else "no"))


def build(lv=5):
    global R
    R = random.Random(40023 + lv * 1000)
    seen = set()
    sets = [
        ("Horas, minutos y segundos", mix(R, seen, [(s1_unidades, 20)])),
        ("Forma compleja e incompleja", mix(R, seen, [(s2_compleja, 20)])),
        ("Sumar y restar tiempos", mix(R, seen, [(s3_operar, 20)])),
        ("Horarios y duraciones", mix(R, seen, [(s4_horarios, 20)])),
        ("Calendario, siglos y años", mix(R, seen, [(s5_calendario, 20)])),
    ]
    body = lesson(
        ["<b>1 h = 60 min</b> y <b>1 min = 60 s</b>, así que 1 h = 3600 s. Un día tiene 24 horas.",
         "Para sumar tiempos, suma horas con horas y minutos con minutos; cada 60 min forman 1 h. Para restar, si faltan minutos, pasa 1 h a 60 min.",
         "Un siglo son 100 años: el siglo XXI va del año 2001 al 2100."],
        [("1 h 45 min + 2 h 30 min", ["3 h 75 min", "75 min = 1 h 15 min"], "4 h 15 min"),
         ("De 9:40 a 11:15", ["De 9:40 a 10:00: 20 min", "De 10:00 a 11:15: 1 h 15 min"], "1 h 35 min")],
        [["Dividir entre 100", "150 min no son 1 h 50 min: son 2 h 30 min."],
         ["Dejar 70 minutos", "1:50 + 0:20 = 2:10, no 1:70."],
         ["Contar mal el siglo", "El año 1492 está en el siglo XV, no en el XIV."]])
    faq = [("¿Cómo se pasan minutos a horas?", "Se divide entre 60: el cociente son las horas y el resto, los minutos. 150 min = 2 h 30 min."),
           ("¿Cómo se calcula el siglo de un año?", "Se quitan las dos últimas cifras y se suma 1 (si el año no acaba en 00). 1975 → 19 + 1 = siglo XX.")]
    make_unit(R, "medida-del-tiempo", "M",
              "Medida del tiempo: unidades (segundo, minuto, hora, día, semana, año, década, siglo) y equivalencias; expresiones complejas e incomplejas; operaciones con tiempos; lectura de horarios",
              "Medida del tiempo", "Medida del tiempo",
              "Fichas de matemáticas de 5.º de Primaria: horas, minutos y segundos, forma compleja e incompleja, sumar y restar tiempos, horarios, duraciones y siglos. 100 ejercicios con soluciones.",
              "1 h = 60 min. 1 min = 60 s", "60 min forman 1 h.",
              body, faq, sets, 23, grade="5-primaria")


if __name__ == "__main__":
    build(5)
