# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Suma y resta (Sentido numérico)
Sumas y restas en vertical con llevadas hasta seis cifras, términos de la suma y la resta, prueba de la resta,
el término que falta, propiedades conmutativa y asociativa, problemas.
Errores: no colocar las cifras en su columna, olvidar la llevada, restar la cifra pequeña de la grande en cada columna.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, vertical, Kids, ao, bank

R = random.Random(44004)
K = Kids(R)


def nocarry_add(a, b):
    """error: sumar sin llevar"""
    s = ""
    x, y = str(a), str(b).rjust(len(str(a)), "0")
    for p, q in zip(x.rjust(max(len(x), len(y)), "0"), y.rjust(max(len(x), len(y)), "0")):
        s += str((int(p) + int(q)) % 10)
    return int(s)


def small_from_big(a, b):
    """error: restar la cifra pequeña de la grande en cada columna"""
    x, y = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(p) - int(q))) for p, q in zip(x, y)))


def nums(lo, hi):
    return R.randint(lo, hi)


def s1_suma():
    d = R.choice([4, 5, 5, 6])
    a = nums(10 ** (d - 1), 10 ** d - 1)
    b = nums(10 ** (d - 2), min(10 ** d - 1, 999999 - a))
    if b < 100:
        return None
    s = a + b
    if s > 999999 or nocarry_add(a, b) == s:
        return None
    pic = vertical([str(a), str(b)])
    return mcq(pic + "Calcula: %s + %s" % (num(a), num(b)), num(s), [num(nocarry_add(a, b)), num(s + 10), num(s - 100), num(s + 1000)],
               "Sumamos por columnas empezando por las unidades y nos llevamos cuando pasamos de 9: <b>%s</b>." % num(s))


def s1_tres():
    a, b, c = nums(1000, 99999), nums(1000, 99999), nums(100, 9999)
    s = a + b + c
    if s > 999999:
        return None
    return mcq("Calcula: %s + %s + %s" % (num(a), num(b), num(c)), num(s), [num(s - 1000), num(s + 10), num(a + b), num(s + 100)], "<b>%s</b>." % num(s))


def s2_resta():
    d = R.choice([4, 5, 5, 6])
    a = nums(10 ** (d - 1) * 2, 10 ** d - 1)
    b = nums(10 ** (d - 2), a - 1)
    r = a - b
    sm = small_from_big(a, b)
    if sm == r or r < 10:
        return None
    pic = vertical([str(a), str(b)], op="−")
    return mcq(pic + "Calcula: %s − %s" % (num(a), num(b)), num(r), [num(sm), num(r + 10), num(r - 100) if r > 100 else num(r + 1), num(r + 1000)],
               "Restamos por columnas; si arriba hay una cifra menor, pedimos una a la columna de la izquierda: <b>%s</b>." % num(r))


def s2_ceros():
    a = R.choice([10000, 20000, 50000, 100000, 300000, 40000, 70000, 200000, 600000, 90000]) + R.choice([0, 0, 100, 1000, 10])
    b = nums(100, a - 1)
    r = a - b
    return mcq("Calcula: %s − %s" % (num(a), num(b)), num(r), [num(small_from_big(a, b)), num(r + 10), num(r - 1000) if r > 1000 else num(r + 100), num(r + 1)],
               "Con ceros arriba hay que pedir prestado varias veces seguidas: <b>%s</b>." % num(r))


def s3_falta():
    k = R.choice(["sum1", "sum2", "min", "sus"])
    a = nums(1000, 99999)
    b = nums(1000, 99999)
    if k == "sum1":
        return mcq("¿Qué número falta? %s + ___ = %s" % (num(a), num(a + b)), num(b), [num(a + b + a), num(b + 10), num(b - 1000) if b > 2000 else num(b + 100), num(b + 1)],
                   "El sumando que falta = suma − el otro sumando: %s − %s = <b>%s</b>." % (num(a + b), num(a), num(b)))
    if k == "sum2":
        return mcq("¿Qué número falta? ___ + %s = %s" % (num(b), num(a + b)), num(a), [num(a + 2 * b), num(a + 10), num(a - 100), num(a + 1000)],
                   "%s − %s = <b>%s</b>." % (num(a + b), num(b), num(a)))
    if k == "min":
        m = a + b
        return mcq("¿Qué número falta? ___ − %s = %s" % (num(b), num(a)), num(m), [num(abs(a - b)), num(m + 10), num(m - 100), num(m + 1000)],
                   "El minuendo = resta + sustraendo: %s + %s = <b>%s</b>." % (num(a), num(b), num(m)))
    m = a + b
    return mcq("¿Qué número falta? %s − ___ = %s" % (num(m), num(a)), num(b), [num(m + a), num(b + 10), num(b - 100), num(b + 1000)],
               "El sustraendo = minuendo − resta: %s − %s = <b>%s</b>." % (num(m), num(a), num(b)))


s3_terminos = bank(R, [
    ("En 4520 − 1310 = 3210, ¿cómo se llama 4520?", "minuendo", ["sustraendo", "diferencia", "sumando"]),
    ("En 4520 − 1310 = 3210, ¿cómo se llama 1310?", "sustraendo", ["minuendo", "diferencia", "suma"]),
    ("En 4520 − 1310 = 3210, ¿cómo se llama 3210?", "diferencia (o resta)", ["minuendo", "sustraendo", "sumando"]),
    ("En 2400 + 1300 = 3700, ¿cómo se llaman 2400 y 1300?", "sumandos", ["sustraendos", "minuendos", "diferencias"]),
    ("Para comprobar una resta (prueba de la resta) se suma…", "la diferencia y el sustraendo", ["el minuendo y el sustraendo", "el minuendo y la diferencia", "los tres números"]),
    ("La propiedad conmutativa dice que…", "el orden de los sumandos no cambia la suma", ["el orden de la resta no cambia el resultado", "si sumas 0 cambia la suma", "la suma siempre es par"]),
    ("¿Qué propiedad usamos en (300 + 45) + 55 = 300 + (45 + 55)?", "asociativa", ["conmutativa", "distributiva", "ninguna"]),
], "s3_terminos")


def s4_prueba():
    a = nums(10000, 99999)
    b = nums(1000, a - 1000)
    r = a - b
    ok = R.random() < 0.5
    shown = r if ok else r + R.choice([10, 100, -10, 1000, -100])
    return mcq("Pablo dice que %s − %s = %s. Haz la prueba: %s + %s = %s. ¿Está bien la resta?" % (num(a), num(b), num(shown), num(shown), num(b), num(shown + b)),
               "sí, está bien" if ok else "no, está mal", ["no, está mal" if ok else "sí, está bien", "no se puede saber", "solo si la diferencia es par"],
               "La prueba de la resta: diferencia + sustraendo debe dar el minuendo (%s). %s" % (num(a), "Da el minuendo: <b>está bien</b>." if ok else "No da el minuendo: <b>está mal</b>; el resultado correcto es %s." % num(r)))


def s5_problema():
    k = R.choice(["libros", "viaje", "ahorro", "estadio", "fabrica", "subida", "km", "diferencia"])
    p, g = K.next()
    if k == "libros":
        a, b = nums(10000, 40000), nums(5000, 20000)
        return mcq("La biblioteca de un pueblo tiene %s libros. Este año ha comprado %s más. ¿Cuántos libros tiene ahora?" % (num(a), num(b)), num(a + b), [num(a - b), num(nocarry_add(a, b)) if nocarry_add(a, b) != a + b else num(a + b + 100), num(a + b - 1000), num(a + b + 10)],
                   "%s + %s = <b>%s</b> libros." % (num(a), num(b), num(a + b)))
    if k == "viaje":
        a = nums(300, 900)
        b = nums(300, 900)
        return mcq("Una familia viaja de Madrid a Cádiz (%d km) y después de Cádiz a Barcelona (%s km). ¿Cuántos kilómetros recorre en total?" % (a, num(b + 600)), num(a + b + 600), [num(abs(b + 600 - a)), num(a + b + 500), num(a + b + 700), num(a + b + 610)],
                   "%d + %s = <b>%s</b> km." % (a, num(b + 600), num(a + b + 600)))
    if k == "ahorro":
        a = nums(800, 2500)
        b = nums(100, a - 100)
        return mcq("%s tiene %s € ahorrados y se gasta %s € en una bicicleta. ¿Cuánto dinero le queda?" % (p, num(a), num(b)), "%s €" % num(a - b), ["%s €" % num(a + b), "%s €" % num(small_from_big(a, b)) if small_from_big(a, b) != a - b else "%s €" % num(a - b + 100), "%s €" % num(a - b + 10), "%s €" % num(a - b - 10)],
                   "%s − %s = <b>%s €</b>." % (num(a), num(b), num(a - b)))
    if k == "estadio":
        cap = R.choice([81044, 99354, 68456, 60721, 53400, 70560])
        o = nums(20000, cap - 2000)
        return mcq("Un estadio tiene %s asientos. En un partido se han ocupado %s. ¿Cuántos asientos han quedado libres?" % (num(cap), num(o)), num(cap - o), [num(cap + o), num(small_from_big(cap, o)) if small_from_big(cap, o) != cap - o else num(cap - o + 100), num(cap - o + 1000), num(cap - o - 10)],
                   "%s − %s = <b>%s</b>." % (num(cap), num(o), num(cap - o)))
    if k == "fabrica":
        a, b, c = nums(10000, 50000), nums(10000, 50000), nums(10000, 50000)
        return mcq("Una fábrica de galletas hace %s paquetes en enero, %s en febrero y %s en marzo. ¿Cuántos paquetes hace en los tres meses?" % (num(a), num(b), num(c)), num(a + b + c), [num(a + b), num(a + b + c - 1000), num(a + b + c + 100), num(a + b + c + 10)],
                   "%s + %s + %s = <b>%s</b>." % (num(a), num(b), num(c), num(a + b + c)))
    if k == "subida":
        a = R.choice([3478, 3404, 2648, 3718, 3145, 2591])
        nm = {3478: "el Mulhacén", 3404: "el Aneto", 2648: "el Moncayo", 3718: "el Teide", 3145: "el Monte Perdido", 2591: "el Almanzor"}[a]
        b = nums(1000, a - 500)
        return mcq("%s mide %s metros. Un grupo de montañeros está a %s metros de altura. ¿Cuántos metros les faltan para llegar a la cima?" % (nm[0].upper() + nm[1:], num(a), num(b)), "%s m" % num(a - b), ["%s m" % num(a + b), "%s m" % num(a - b + 100), "%s m" % num(a - b - 10), "%s m" % num(small_from_big(a, b)) if small_from_big(a, b) != a - b else "%s m" % num(a - b + 1000)],
                   "%s − %s = <b>%s m</b>." % (num(a), num(b), num(a - b)))
    if k == "km":
        a = nums(20000, 90000)
        b = nums(1000, 15000)
        return mcq("Un coche tenía %s km en el cuentakilómetros. Después de las vacaciones tiene %s km. ¿Cuántos kilómetros ha recorrido en las vacaciones?" % (num(a), num(a + b)), "%s km" % num(b), ["%s km" % num(2 * a + b), "%s km" % num(b + 1000), "%s km" % num(b - 100), "%s km" % num(b + 10)],
                   "%s − %s = <b>%s km</b>." % (num(a + b), num(a), num(b)))
    a, b = nums(100000, 500000), nums(100000, 500000)
    if a == b:
        return None
    x, y = R.sample([("Zaragoza", 680000), ("Málaga", 590000), ("Bilbao", 345000), ("Valladolid", 300000), ("Córdoba", 320000), ("Vigo", 295000), ("Alicante", 340000), ("Murcia", 460000)], 2)
    hi, lo = max(x[1], y[1]), min(x[1], y[1])
    h = x if x[1] == hi else y
    l_ = y if h is x else x
    hi += nums(0, 9999)
    lo += nums(0, 9999)
    return mcq("%s tiene unos %s habitantes y %s, unos %s. ¿Cuántos habitantes más tiene %s?" % (h[0], num(hi), l_[0], num(lo), h[0]), num(hi - lo), [num(hi + lo), num(hi - lo + 10000), num(hi - lo - 1000), num(small_from_big(hi, lo)) if small_from_big(hi, lo) != hi - lo else num(hi - lo + 100)],
               "%s − %s = <b>%s</b>." % (num(hi), num(lo), num(hi - lo)))


def main():
    seen = set()
    sets = [
        ("Sumas en vertical", mix(R, seen, [(s1_suma, 15), (s1_tres, 5)])),
        ("Restas en vertical", mix(R, seen, [(s2_resta, 14), (s2_ceros, 6)])),
        ("Términos y el número que falta", mix(R, seen, [(s3_terminos, 6), (s3_falta, 14)])),
        ("Prueba de la resta y repaso", mix(R, seen, [(s4_prueba, 8), (s1_suma, 6), (s2_resta, 6)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Coloca los números en <b>columnas</b>: unidades debajo de unidades, decenas debajo de decenas…",
         "En la suma, si una columna pasa de 9, escribe las unidades y <b>llévate</b> la decena a la columna siguiente.",
         "En la resta, si la cifra de arriba es menor, pide <b>una</b> a la columna de la izquierda (10 unidades de esta columna).",
         "<b>Prueba de la resta</b>: diferencia + sustraendo = minuendo."],
        [("45 678 + 27 435", ["8 + 5 = 13, escribo 3 y me llevo 1", "7 + 3 + 1 = 11, escribo 1 y me llevo 1", "…"], "73 113"),
         ("60 000 − 23 452", ["Pido prestado en cadena: 60 000 = 59 990 + 10", "Prueba: 36 548 + 23 452 = 60 000"], "36 548")],
        [["Olvidar la llevada", "Escribe la llevada pequeña encima de la columna siguiente."],
         ["Restar la cifra pequeña de la grande", "En 52 − 18 no hagas 8 − 2: pide prestado, 12 − 8 = 4."],
         ["Descolocar las columnas", "Alinea los números por la derecha."]],
        vertical(["45678", "27435"], result="73113"))
    faq = [("¿Cómo se hace la prueba de la resta?", "Se suma la diferencia (el resultado) y el sustraendo. Si da el minuendo, la resta está bien."),
           ("¿Cómo se llaman los términos de la resta?", "Minuendo − sustraendo = diferencia. En la suma, los números que se suman son los sumandos y el resultado es la suma o el total.")]
    make_unit(R, "suma-y-resta", "N",
              "Estrategias y algoritmos de suma y resta con números naturales de hasta seis cifras; propiedades de la suma; relación entre suma y resta; resolución de problemas",
              "Suma y resta con llevadas", "Suma y resta",
              "Fichas de matemáticas de 4.º de Primaria: sumas y restas en vertical con llevadas hasta seis cifras, términos, prueba de la resta, número que falta y problemas. 100 ejercicios con soluciones.",
              "Alinea las cifras por la derecha", "Empieza por las unidades.",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
