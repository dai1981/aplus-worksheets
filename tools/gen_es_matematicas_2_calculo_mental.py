# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Cálculo mental (Sentido numérico)
build(lv): lv = 1 → «sumas-y-restas-hasta-99»: decenas, sumar y restar 10, sumas y restas sin llevar con regletas;
lv = 2 → «calculo-mental»: sumar y restar decenas y centenas, completar la decena y la centena, sumar 9 y 11, problemas.
Errores: sumar las decenas a las unidades (34 + 20 = 36), cambiar la cifra equivocada, olvidar quitar 1 al sumar 9.
"""
import random
from es_common import mcq, mix, lesson, make_unit
import es_pics as P

R = None
LV = 2
NOMBRES = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo", "Alba", "Mario"]


def s_decenas():
    if LV == 1:
        a, b = R.randint(1, 8), R.randint(1, 8)
        if a + b > 9:
            return None
        if R.random() < 0.5:
            return mcq(P.regletas(a, 0) + "%d decenas y %d decenas más. ¿Cuánto es %d + %d?" % (a, b, 10 * a, 10 * b), str(10 * (a + b)), [str(a + b), str(10 * (a + b) + 10), str(10 * abs(a - b)) if a != b else str(10 * (a + b) - 10)],
                       "%d decenas + %d decenas = %d decenas = <b>%d</b>." % (a, b, a + b, 10 * (a + b)))
        x, y = max(a, b) + min(a, b), min(a, b)
        return mcq("Calcula: %d − %d" % (10 * x, 10 * y), str(10 * (x - y)), [str(x - y), str(10 * (x - y) + 10), str(10 * (x + y))], "%d decenas − %d decenas = <b>%d</b>." % (x, y, 10 * (x - y)))
    n = R.randint(11, 899)
    d = R.randint(1, 9) * 10
    if R.random() < 0.5:
        if n + d > 999 or (n % 100) // 10 * 10 + d >= 100:
            return None
        return mcq("Calcula mentalmente: %d + %d" % (n, d), str(n + d), [str(n + d // 10), str(n + d * 10) if n + d * 10 < 1000 else str(n + d + 1), str(n + d + 10)], "Solo cambian las decenas: <b>%d</b>." % (n + d))
    if (n % 100) // 10 * 10 < d:
        return None
    return mcq("Calcula mentalmente: %d − %d" % (n, d), str(n - d), [str(n - d // 10), str(n - d + 10), str(n - d - 10) if n - d >= 10 else str(n + d)], "Solo cambian las decenas: <b>%d</b>." % (n - d))


def s_diez():
    if LV == 1:
        n = R.randint(1, 89)
        if R.random() < 0.5:
            return mcq("Calcula: %d + 10" % n, str(n + 10), [str(n + 1), str(n + 11), str(n + 20)], "Sumar 10 es una decena más: <b>%d</b>." % (n + 10))
        m = n + 10
        return mcq("Calcula: %d − 10" % m, str(n), [str(m - 1), str(n - 1) if n > 1 else str(n + 2), str(n + 20) if n + 20 < 100 else str(n - 10) if n > 10 else str(n + 5)], "Restar 10 es una decena menos: <b>%d</b>." % n)
    n = R.randint(100, 899)
    c = R.randint(1, 9) * 100
    if R.random() < 0.5:
        if n + c > 999:
            return None
        return mcq("Calcula mentalmente: %d + %d" % (n, c), str(n + c), [str(n + c // 10), str(n + c + 100) if n + c + 100 < 1000 else str(n + c - 10), str(n + c // 100)], "Solo cambian las centenas: <b>%d</b>." % (n + c))
    if n < c:
        return None
    return mcq("Calcula mentalmente: %d − %d" % (n, c), str(n - c), [str(n - c // 10), str(n - c + 100), str(n - c // 100)], "Solo cambian las centenas: <b>%d</b>." % (n - c))


def s_completar():
    if LV == 1:
        a = R.randint(1, 8)
        b = R.randint(0, 9 - a)
        x, y = R.randint(1, 8), R.randint(1, 9)
        if R.random() < 0.5:
            t1, o1, t2, o2 = x, y, R.randint(1, 9 - x), R.randint(0, 9 - y)
            s = 10 * (t1 + t2) + o1 + o2
            return mcq(P.regletas(t1, o1) + "Calcula: %d + %d" % (10 * t1 + o1, 10 * t2 + o2), str(s), [str(s + 10), str(s - 1), str(t1 + t2 + o1 + o2)], "Decenas con decenas y unidades con unidades: <b>%d</b>." % s)
        t1, o1 = x + 1, y
        t2, o2 = R.randint(1, t1 - 1), R.randint(0, o1)
        r = 10 * (t1 - t2) + o1 - o2
        if r <= 0:
            return None
        return mcq("Calcula: %d − %d" % (10 * t1 + o1, 10 * t2 + o2), str(r), [str(r + 10), str(r + 1), str(10 * t1 + o1 + 10 * t2 + o2) if 10 * t1 + o1 + 10 * t2 + o2 < 100 else str(r - 1) if r > 1 else str(r + 2)],
                   "Decenas: %d − %d = %d. Unidades: %d − %d = %d. Resultado: <b>%d</b>." % (t1, t2, t1 - t2, o1, o2, o1 - o2, r))
    k = R.choice(["dec", "cien", "mil"])
    if k == "dec":
        n = R.randint(11, 98)
        if n % 10 == 0:
            return None
        t = (n // 10 + 1) * 10
        return mcq("¿Cuánto le falta a %d para llegar a %d?" % (n, t), str(t - n), [str(10 - (t - n)) if t - n != 5 else str(t - n + 1), str(t - n + 1), str(t - n + 10)], "%d + %d = %d: falta <b>%d</b>." % (n, t - n, t, t - n))
    if k == "cien":
        n = R.randint(1, 9) * 10 + (R.randint(1, 9) if R.random() < 0.4 else 0)
        if n >= 100:
            return None
        return mcq("¿Cuánto le falta a %d para llegar a 100?" % n, str(100 - n), [str(100 - n + 10), str(110 - n) if n % 10 else str(n), str(100 - n - 1)], "%d + %d = 100: falta <b>%d</b>." % (n, 100 - n, 100 - n))
    n = R.randint(1, 9) * 100 + R.randint(1, 9) * 10
    t = (n // 100 + 1) * 100
    return mcq("¿Cuánto le falta a %d para llegar a %d?" % (n, t), str(t - n), [str(t - n + 10), str(t - n - 10) if t - n > 10 else str(t - n + 20), str(100 - (t - n) // 10)], "%d + %d = %d: falta <b>%d</b>." % (n, t - n, t, t - n))


def s_nueve():
    n = R.randint(12, 88)
    k = R.choice([9, 11, 19, 21])
    if n + k > 100:
        return None
    base = (k + 1) if k in (9, 19) else (k - 1)
    sign = "y quitamos 1" if k in (9, 19) else "y sumamos 1"
    return mcq("Calcula mentalmente: %d + %d" % (n, k), str(n + k), [str(n + base), str(n + k + 2) if k in (9, 19) else str(n + k - 2), str(n + k + 10)],
               "Sumamos %d %s: %d + %d = %d; resultado: <b>%d</b>." % (base, sign, n, base, n + base, n + k))


def s_problema():
    p = R.choice(NOMBRES)
    if LV == 1:
        t = R.choice(["junta", "quita", "decena"])
        if t == "decena":
            a = R.randint(1, 8)
            b = R.randint(1, 9 - a)
            return mcq("%s tiene %d paquetes de 10 cromos y le regalan %d paquetes más. ¿Cuántos cromos tiene?" % (p, a, b), str(10 * (a + b)), [str(a + b), str(10 * (a + b) + 10), str(10 * a + b)], "%d decenas = <b>%d</b> cromos." % (a + b, 10 * (a + b)))
        a = R.randint(21, 68)
        b = R.randint(10, 30)
        if t == "junta":
            if a % 10 + b % 10 > 9 or a + b > 99:
                return None
            return mcq("En el patio hay %d niños y llegan %d más. ¿Cuántos niños hay ahora?" % (a, b), str(a + b), [str(a - b), str(a + b + 10), str(a + b + 1)], "%d + %d = <b>%d</b>." % (a, b, a + b))
        if a % 10 < b % 10 or b > a:
            return None
        return mcq("%s tiene %d canicas y pierde %d. ¿Cuántas canicas le quedan?" % (p, a, b), str(a - b), [str(a + b) if a + b < 100 else str(a - b + 1), str(a - b + 10), str(a - b - 1)], "%d − %d = <b>%d</b>." % (a, b, a - b))
    t = R.choice(["dec", "cien", "falta"])
    if t == "dec":
        a, d = R.randint(120, 860), R.randint(1, 9) * 10
        if (a % 100) // 10 * 10 + d >= 100:
            return None
        return mcq("Una tienda tenía %d cuadernos y recibe %d más. ¿Cuántos cuadernos tiene ahora?" % (a, d), str(a + d), [str(a + d // 10), str(a + d + 10), str(a - d)], "%d + %d = <b>%d</b>." % (a, d, a + d))
    if t == "cien":
        a, c = R.randint(300, 999), R.randint(1, 2) * 100
        return mcq("En un cine caben %d personas. Hoy hay %d sitios vacíos. ¿Cuántas personas hay?" % (a, c), str(a - c), [str(a + c), str(a - c // 10), str(a - c + 100)], "%d − %d = <b>%d</b>." % (a, c, a - c))
    n = R.randint(1, 9) * 10
    return mcq("%s ha leído %d páginas de un libro de 100. ¿Cuántas le faltan?" % (p, n), str(100 - n), [str(n), str(100 - n + 10), str(10 - n // 10)], "100 − %d = <b>%d</b>." % (n, 100 - n))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30004 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("Sumar y restar decenas", mix(R, seen, [(s_decenas, 20)])), ("Sumar 10 y restar 10", mix(R, seen, [(s_diez, 20)])), ("Sumas sin llevar", mix(R, seen, [(s_completar, 20)])),
                ("Sumas y restas hasta 99", mix(R, seen, [(s_completar, 10), (s_decenas, 5), (s_diez, 5)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Una <b>decena</b> son 10 unidades. 30 + 20 es como 3 decenas + 2 decenas = 5 decenas = 50.", "Sumar 10 es poner una decena más: 34 + 10 = 44. Solo cambian las decenas.",
                 "Para sumar 34 + 25: decenas con decenas (3 + 2 = 5) y unidades con unidades (4 + 5 = 9): 59."]
        ex = [("43 + 25", ["Decenas: 4 + 2 = 6", "Unidades: 3 + 5 = 8"], "68"), ("57 − 10", ["Una decena menos"], "47")]
        mist = [["Sumar las decenas a las unidades", "En 34 + 20, el 2 va con el 3: 54."], ["Cambiar la cifra equivocada al sumar 10", "+ 10 cambia las decenas, no las unidades."], ["Leer 45 como «cuatro y cinco»", "Son 4 decenas y 5 unidades."]]
        kb, ks = "Decenas con decenas", "Y unidades con unidades."
        meta = "Fichas de matemáticas de 1.º de Primaria: sumar y restar decenas, sumar 10, sumas y restas sin llevar hasta 99 con regletas. 100 ejercicios con soluciones."
        std = "Suma y resta de números hasta 99 sin llevadas; decenas completas; estrategias de cálculo mental"
        slug, title, short = "sumas-y-restas-hasta-99", "Sumas y restas hasta 99", "Sumas hasta 99"
        pic = P.regletas(3, 4)
        sort = 4
    else:
        sets = [("Sumar y restar decenas", mix(R, seen, [(s_decenas, 20)])), ("Sumar y restar centenas", mix(R, seen, [(s_diez, 20)])), ("Completar la decena y la centena", mix(R, seen, [(s_completar, 20)])),
                ("Sumar 9, 11, 19 y 21", mix(R, seen, [(s_nueve, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Para sumar o restar decenas, solo cambia la cifra de las decenas: 340 + 20 = 360.", "Con centenas, solo cambian las centenas: 450 + 300 = 750.",
                 "Para sumar 9, suma 10 y quita 1. Para sumar 11, suma 10 y suma 1.", "Para completar: 37 + 3 = 40, porque 7 + 3 = 10."]
        ex = [("46 + 9", ["46 + 10 = 56", "56 − 1"], "55"), ("¿Cuánto le falta a 70 para 100?", ["7 decenas + 3 decenas = 10 decenas"], "30")]
        mist = [["Cambiar la cifra equivocada", "En 520 + 40, cambian las decenas: 560."], ["Olvidar quitar 1 al sumar 9", "+ 10 − 1, siempre los dos pasos."], ["Completar a 100 como si fuera a 10", "A 70 le faltan 30, no 3."]]
        kb, ks = "Sumar 9 es sumar 10 y quitar 1", "Busca la decena o la centena."
        meta = "Fichas de matemáticas de 2.º de Primaria: sumar y restar decenas y centenas, completar la decena y la centena, sumar 9 y 11. 100 ejercicios con soluciones."
        std = "Estrategias de cálculo mental con números hasta 999: decenas y centenas, complementos, compensación"
        slug, title, short = "calculo-mental", "Cálculo mental", "Cálculo mental"
        pic = P.regletas(4, 6)
        sort = 4
    body = lesson(think, ex, mist, pic)
    faq = [("¿Qué es el cálculo mental?", "Calcular sin escribir la cuenta, usando trucos como sumar decenas o buscar números redondos."), ("¿Cómo se suma 10 a un número?", "Se añade una decena: la cifra de las decenas aumenta 1 y las unidades no cambian.")]
    make_unit(R, slug, "N", std, title, short, meta, kb, ks, body, faq, sets, sort, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
