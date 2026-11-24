# -*- coding: utf-8 -*-
"""
México 1.er grado de secundaria (Fase 6): problemas propios (no vienen de España).
Cada función devuelve un problema ya en formato mexicano (punto decimal, $ en pesos reales, 1 000 con espacio).
Se usan con mx_common.unit(..., lv=7). Las funciones reciben R (random.Random) y K (Kids) con setup(R).
"""
import math
from fractions import Fraction as F
from es_c3 import M as _M, fr


def M(q, ok, cands, e):
    try:
        return _M(q, ok, cands, e)
    except AssertionError:
        return None
from mx_common import num, dec, peso, NB, Kids
from ws_common import svg_wrap, text, line, fig

R = None
K = None
MINUS = "−"


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def sg(x):
    return (MINUS + num(-x)) if x < 0 else num(x)


def sgd(x, p=None):
    return (MINUS + dec(-x, p)) if x < 0 else dec(x, p)


def fq(x):
    x = F(x)
    s = MINUS if x < 0 else ""
    x = abs(x)
    return s + (num(x.numerator) if x.denominator == 1 else fr(x.numerator, x.denominator))


def ov(s):
    return "<span class='ov'>%s</span>" % s


def dexact(x):
    """Fraction → «0.375» (exacto) o None"""
    x = F(x)
    for k in range(7):
        if (x * 10 ** k).denominator == 1:
            return sgd(float(x), k) if k else sg(int(x))
    return None


def periodic(x):
    """Fraction (0 < x) → texto con el periodo marcado: 0.<ov>3</ov>, 0.1<ov>6</ov>"""
    x = F(x)
    ip, r = divmod(x.numerator, x.denominator)
    digs, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digs)
        r *= 10
        digs.append(str(r // x.denominator))
        r %= x.denominator
    if not r:
        return num(ip) + ("." + "".join(digs) if digs else "")
    i = seen[r]
    return num(ip) + "." + "".join(digs[:i]) + ov("".join(digs[i:]))


# ============================================================ fracciones y decimales
DEN_EX = [2, 4, 5, 8, 10, 20, 25, 40, 50]


def fd_frac2dec():
    b = R.choice(DEN_EX)
    a = R.randint(1, 3 * b)
    if a % b == 0 or math.gcd(a, b) != 1:
        return None
    x = F(a, b)
    ok = dexact(x)
    w = ["%d.%d" % (a, b), dexact(F(b, a)) or "%d.%d" % (b, a), dexact(x * 10), dexact(x / 10)]
    return M("Escribe %s como número decimal." % fq(x), ok, w,
             "Divide el numerador entre el denominador: %d ÷ %d = <b>%s</b>." % (a, b, ok))


def fd_dec2frac():
    k = R.choice([1, 2, 2, 3])
    n = R.randint(1, 10 ** k * 3)
    if n % 10 == 0:
        return None
    x = F(n, 10 ** k)
    if x.denominator == 10 ** k and k == 1 and R.random() < .5:
        return None
    ok = fq(x)
    raw = fr(n, 10 ** k)
    w = [fr(n, 10 ** (k + 1)), fr(x.denominator, x.numerator) if x.numerator > 1 else fr(n, 10 ** k + 1), fr(n % 10 ** k or 1, 10 ** k) if n > 10 ** k else fr(n, 100 if k == 1 else 10),
         fr(x.numerator, x.denominator * 10), fr(n + 1, 10 ** k)]
    if raw != ok:
        w.insert(0, raw)
    lab = {1: "décimos", 2: "centésimos", 3: "milésimos"}[k]
    return M("Escribe %s como fracción irreducible." % sgd(float(x), k), ok, w,
             "%s = %s (%s). Simplificamos: <b>%s</b>." % (sgd(float(x), k), raw, lab, ok))


def fd_periodic():
    b = R.choice([3, 6, 9, 11, 12, 15, 18, 7])
    a = R.randint(1, 2 * b)
    if math.gcd(a, b) != 1 or a % b == 0:
        return None
    x = F(a, b)
    if dexact(x):
        return None
    t = R.choice(["valor", "valor", "tipo"])
    if t == "tipo":
        b2 = R.choice(DEN_EX)
        a2 = R.randint(1, b2 * 2)
        if math.gcd(a2, b2) != 1:
            return None
        return M("¿Cuál de estas fracciones da un decimal periódico?", fq(x), [fq(F(a2, b2)), fq(F(1, R.choice([4, 5, 8]))), fq(F(R.choice([3, 7, 9]), 10))],
                 "Una fracción irreducible da decimal exacto solo si el denominador tiene como factores 2 y 5. %s tiene el factor %s: <b>periódico</b>." % (fq(x), "3" if b % 3 == 0 else "7" if b % 7 == 0 else "11"))
    ok = periodic(x)
    v = float(x)
    w = [dec(round(v, 2), 2), dec(round(v, 1), 1), periodic(F(b, a)) if b > a else dec(round(v + .1, 2), 2), periodic(x + F(1, 10))]
    return M("Escribe %s como número decimal." % fq(x), ok, w,
             "%d ÷ %d nunca termina: las cifras se repiten. Escribimos el periodo con una raya encima: <b>%s</b>." % (a, b, ok))


def fd_compare():
    b = R.choice([4, 5, 8, 3, 6, 20, 25])
    a = R.randint(1, b - 1)
    if math.gcd(a, b) != 1:
        return None
    x = F(a, b)
    v = float(x)
    dv = round(v + R.choice([-.07, -.03, .02, .04, .06]), 2)
    if dv <= 0 or abs(dv - v) < 1e-9:
        return None
    big = fq(x) if v > dv else dec(dv, 2)
    return M("¿Qué número es mayor: %s o %s?" % (fq(x), dec(dv, 2)), big, [dec(dv, 2) if v > dv else fq(x), "son iguales", "no se pueden comparar"],
             "%s = %s. Comparamos %s con %s: el mayor es <b>%s</b>." % (fq(x), dexact(x) or periodic(x), dexact(x) or periodic(x), dec(dv, 2), big))


FD_CTX = [("Una receta pide %s de kg de harina. ¿Qué número debe marcar la báscula digital (en kg)?", "kg"),
          ("Un garrafón tiene %s de litro de agua. ¿Cuántos litros son en número decimal?", "L"),
          ("%s tardó %s de hora en llegar a la escuela. ¿Cuántas horas son en número decimal?", "h"),
          ("Una tela mide %s de metro. ¿Cuántos metros son en número decimal?", "m")]


def fd_problem():
    t = R.choice(["ctx", "ctx", "minutos", "orden"])
    if t == "ctx":
        b = R.choice([2, 4, 5, 8, 10])
        a = R.randint(1, b - 1) if b > 2 else 1
        if math.gcd(a, b) != 1:
            return None
        x = F(a, b)
        q, u = R.choice(FD_CTX)
        q = q % ((K.next()[0], fq(x)) if q.count("%s") == 2 else (fq(x),))
        ok = dexact(x) + " " + u
        return M(q, ok, ["%d.%d %s" % (a, b, u), (dexact(F(b, a)) or "%d.%d" % (b, a)) + " " + u, dexact(x / 10) + " " + u],
                 "%s = %d ÷ %d = <b>%s</b>." % (fq(x), a, b, ok))
    if t == "minutos":
        m = R.choice([15, 45, 12, 6, 30, 24, 36, 48, 54, 18])
        x = F(m, 60)
        ok = dexact(x) + " h"
        return M("Un video dura %d minutos. ¿Cuántas horas son en número decimal?" % m, ok, ["0.%d h" % m, dexact(x * 10) + " h", dec(round(60 / m, 2), 2) + " h"],
                 "%d min = %s de hora = <b>%s</b>." % (m, fq(x), ok))
    xs = R.sample([F(1, 2), F(3, 4), F(2, 5), F(3, 8), F(7, 10), F(1, 4), F(3, 5), F(5, 8), F(9, 20)], 2)
    ds = R.sample([0.45, 0.6, 0.35, 0.72, 0.5, 0.8, 0.28], 2)
    allv = [(float(x), fq(x)) for x in xs] + [(d, dec(d, 2)) for d in ds]
    if len(set(v for v, _ in allv)) < 4:
        return None
    srt = [s for _, s in sorted(allv)]
    ok = " &lt; ".join(srt)
    w = [" &lt; ".join(srt[::-1]), " &lt; ".join([fq(x) for x in xs] + [dec(d, 2) for d in ds]), " &lt; ".join(srt[1:2] + srt[:1] + srt[2:])]
    return M("Ordena de menor a mayor: %s" % ", ".join(s for _, s in allv), ok, w,
             "Pasamos todo a decimal y comparamos: <b>%s</b>." % ok)


# ============================================================ números con signo (contextos de México)
CIUDADES_FRIAS = ["Chihuahua", "Durango", "Zacatecas", "Toluca", "Ciudad Juárez"]


def pn_context():
    t = R.choice(["temp", "temp", "saldo", "altura", "elevador", "historia"])
    if t == "temp":
        c = R.choice(CIUDADES_FRIAS)
        a, b = -R.randint(1, 9), R.randint(4, 22)
        if R.random() < .5:
            return M("En %s, una mañana de enero la temperatura fue de %s °C y en la tarde de %s °C. ¿Cuántos grados subió?" % (c, sg(a), sg(b)),
                     "%d °C" % (b - a), [sg(b + a) + " °C", "%d °C" % b, "%s °C" % sg(a - b)], "De %s a 0 hay %d grados y de 0 a %d hay %d: <b>%d °C</b>." % (sg(a), -a, b, b, b - a))
        d = R.randint(abs(a) + 2, abs(a) + 12)
        return M("En %s la temperatura era de %s °C y bajó %d grados. ¿Qué temperatura hay ahora?" % (c, sg(b), d) if b - d < 0 else
                 "En %s la temperatura era de %s °C y bajó %d grados. ¿Qué temperatura hay ahora?" % (c, sg(b), d + b), sg(b - d) + " °C" if b - d < 0 else sg(-d) + " °C",
                 [sg(d - b) + " °C" if b - d < 0 else sg(d) + " °C", sg(b + d) + " °C" if b - d < 0 else sg(b + d + b) + " °C", sg(b - d - 1) + " °C" if b - d < 0 else sg(-d - 1) + " °C"],
                 "Bajar es restar: <b>%s °C</b>." % (sg(b - d) if b - d < 0 else sg(-d)))
    if t == "saldo":
        s = R.choice([350, 500, 820, 1200, 1500, 640])
        r = s + R.choice([150, 250, 400, 600, 900])
        return M("%s tenía %s en su cuenta y pagó %s con su tarjeta de débito con sobregiro. ¿Cuál es su saldo ahora?" % (K.next()[0], peso(s * 100), peso(r * 100)),
                 MINUS + peso((r - s) * 100), [peso((r - s) * 100), MINUS + peso((r + s) * 100), peso((r + s) * 100)],
                 "%s − %s = <b>−%s</b> (debe dinero)." % (num(s), num(r), peso((r - s) * 100)))
    if t == "altura":
        h = R.choice([("el Pico de Orizaba", 5636), ("el Popocatépetl", 5426), ("el Nevado de Toluca", 4680), ("el Iztaccíhuatl", 5230)])
        p = -R.choice([120, 250, 300, 450, 600])
        return M("La cima de %s está a %s m sobre el nivel del mar y un submarino está a %s m. ¿Cuántos metros hay entre los dos?" % (h[0], num(h[1]), sg(p)),
                 "%s m" % num(h[1] - p), ["%s m" % num(h[1] + p), "%s m" % num(h[1]), "%s m" % num(-p)],
                 "Distancia = %s − (%s) = %s + %d = <b>%s m</b>." % (num(h[1]), sg(p), num(h[1]), -p, num(h[1] - p)))
    if t == "elevador":
        a = -R.randint(1, 4)
        b = R.randint(3, 15)
        return M("Un edificio tiene pisos de estacionamiento bajo tierra (−1, −2, …). %s sube en el elevador del piso %s al piso %d. ¿Cuántos pisos subió?" % (K.next()[0], sg(a), b),
                 str(b - a), [sg(b + a), str(b), str(b - a + 1)], "De %s a 0 son %d y de 0 a %d son %d: <b>%d pisos</b>." % (sg(a), -a, b, b, b - a))
    a = R.choice([(-500, "la fundación de una ciudad olmeca"), (-300, "un registro maya antiguo"), (-100, "una ciudad de Teotihuacan")])
    b = R.choice([1325, 1521, 1810, 1910])
    return M("Si tomamos el año 1 como referencia, %s fue en el año %d a. C. (lo escribimos como %s) y otro hecho en %d d. C. ¿Cuál número representa mejor el año %d a. C.?" % (a[1], -a[0], sg(a[0]), b, -a[0]),
             sg(a[0]), [num(-a[0]), sg(a[0] - 1), "0"], "Los años antes de Cristo se representan con números negativos: <b>%s</b>." % sg(a[0]))


# ============================================================ ecuaciones: problemas con pesos reales
def ec_problem():
    t = R.choice(["cine", "consec", "reparto", "edad", "papeleria", "taxi", "perimetro"])
    if t == "cine":
        x = R.choice([65, 70, 75, 80, 85, 90])
        n = R.randint(2, 5)
        p = R.choice([55, 60, 75, 85])
        tot = n * x + p
        return M("%s compró %d boletos de cine iguales y unas palomitas de %s. Pagó %s en total. ¿Cuánto costó cada boleto?" % (K.next()[0], n, peso(p * 100), peso(tot * 100)),
                 peso(x * 100), [peso((tot + p) // n * 100), peso(tot // n * 100), peso((tot - p) * 100)],
                 "%dx + %d = %s → %dx = %s → x = <b>%s</b>." % (n, p, num(tot), n, num(tot - p), peso(x * 100)))
    if t == "consec":
        a = R.randint(12, 90)
        k = R.choice([2, 3])
        tot = sum(a + i for i in range(k))
        return M("La suma de %s números enteros consecutivos es %d. ¿Cuál es el menor?" % ("dos" if k == 2 else "tres", tot), str(a),
                 [str(a + 1), str(tot // k), str(a - 1)], "%s = %d → x = <b>%d</b>." % ("x + (x + 1)" if k == 2 else "x + (x + 1) + (x + 2)", tot, a))
    if t == "reparto":
        x = R.choice([120, 150, 180, 200, 250, 300])
        m = R.choice([2, 3])
        tot = x * (m + 1)
        a, b = K.next()[0], K.next()[0]
        return M("%s y %s se reparten %s. %s recibe el %s de lo que recibe %s. ¿Cuánto recibe %s?" % (a, b, peso(tot * 100), b, "doble" if m == 2 else "triple", a, a),
                 peso(x * 100), [peso(x * m * 100), peso(tot // 2 * 100), peso(tot // m * 100)],
                 "x + %dx = %s → %dx = %s → x = <b>%s</b>." % (m, num(tot), m + 1, num(tot), peso(x * 100)))
    if t == "edad":
        h = R.randint(8, 15)
        k = R.choice([3, 4])
        return M("La edad de una mamá es %s veces la de su hijo. Juntos suman %d años. ¿Cuántos años tiene el hijo?" % ("tres" if k == 3 else "cuatro", h * (k + 1)),
                 "%d años" % h, ["%d años" % (h * k), "%d años" % (h * (k + 1) // 2), "%d años" % (h + 1)], "x + %dx = %d → %dx = %d → x = <b>%d</b>." % (k, h * (k + 1), k + 1, h * (k + 1), h))
    if t == "papeleria":
        x = R.choice([12, 15, 18, 22, 25, 28])
        n = R.randint(3, 8)
        c = R.choice([200, 300, 500])
        r = c - n * x
        if r <= 0:
            return None
        return M("%s pagó con un billete de %s por %d cuadernos iguales y le dieron %s de cambio. ¿Cuánto cuesta cada cuaderno?" % (K.next()[0], peso(c * 100), n, peso(r * 100)),
                 peso(x * 100), [peso((c + r) // n * 100) if (c + r) % n == 0 else peso((x + 3) * 100), peso(r * 100), peso((x - 2) * 100)],
                 "%d − %dx = %d → %dx = %d → x = <b>%s</b>." % (c, n, r, n, c - r, peso(x * 100)))
    if t == "taxi":
        b = R.choice([13, 15, 19])
        k = R.choice([6, 7, 8])
        km = R.randint(4, 15)
        tot = b + k * km
        return M("Un taxi cobra %s al subir y %s por kilómetro. Un viaje costó %s. ¿Cuántos kilómetros se recorrieron?" % (peso(b * 100), peso(k * 100), peso(tot * 100)),
                 "%d km" % km, ["%d km" % (tot // k), "%d km" % (km + 1), "%d km" % ((tot + b) // k)], "%d + %dx = %d → %dx = %d → x = <b>%d km</b>." % (b, k, tot, k, tot - b, km))
    w = R.randint(5, 20)
    e = R.randint(2, 9)
    per = 2 * (w + w + e)
    return M("En un rectángulo, el largo mide %d cm más que el ancho y el perímetro es %d cm. ¿Cuánto mide el largo?" % (e, per), "%d cm" % (w + e),
             ["%d cm" % w, "%d cm" % (per // 4), "%d cm" % (per // 2 - e)], "2x + 2(x + %d) = %d → 4x = %d → x = %d; largo = <b>%d cm</b>." % (e, per, per - 2 * e, w, w + e))


# ============================================================ porcentajes con precios de México (IVA 16 %)
COSAS = [("una chamarra", 800, 1800), ("una mochila", 400, 900), ("una bocina", 500, 1500), ("una bicicleta", 3000, 6000), ("un celular", 4000, 9000), ("una licuadora", 700, 1500), ("una guitarra", 1500, 3500)]


def pc_problem():
    t = R.choice(["desc", "desc", "iva", "aum", "que", "total", "propina"])
    c, lo, hi = R.choice(COSAS)
    p = R.randrange(lo, hi + 1, 50)
    if t == "desc":
        k = R.choice([10, 15, 20, 25, 30, 40])
        if p * k % 100:
            return None
        n = p * (100 - k) // 100
        return M("%s cuesta %s y tiene %d %% de descuento. ¿Cuánto pagas?" % (c[0].upper() + c[1:], peso(p * 100), k), peso(n * 100),
                 [peso(p * k // 100 * 100), peso((p - k) * 100), peso((p + p * k // 100) * 100)], "Pagas el %d %%: %s × %s = <b>%s</b>." % (100 - k, num(p), dec((100 - k) / 100.0, 2), peso(n * 100)))
    if t == "iva":
        if p * 16 % 100:
            p = p - p % 25
            if p * 16 % 100:
                return None
        n = p * 116 // 100
        return M("El precio de %s es %s más IVA (16 %%). ¿Cuánto se paga en total?" % (c, peso(p * 100)), peso(n * 100),
                 [peso(p * 16 // 100 * 100), peso((p + 16) * 100), peso(p * 84 // 100 * 100)], "Total = %s × 1.16 = <b>%s</b>." % (num(p), peso(n * 100)))
    if t == "aum":
        k = R.choice([5, 8, 10, 12, 20])
        if p * k % 100:
            return None
        n = p * (100 + k) // 100
        return M("%s costaba %s y subió de precio un %d %%. ¿Cuánto cuesta ahora?" % (c[0].upper() + c[1:], peso(p * 100), k), peso(n * 100),
                 [peso(p * k // 100 * 100), peso((p + k) * 100), peso(p * (100 - k) // 100 * 100)], "%s × %s = <b>%s</b>." % (num(p), dec((100 + k) / 100.0, 2), peso(n * 100)))
    if t == "que":
        k = R.choice([10, 20, 25, 30, 40, 50])
        if p * k % 100:
            return None
        n = p * (100 - k) // 100
        return M("%s costaba %s y ahora cuesta %s. ¿Qué porcentaje de descuento le hicieron?" % (c[0].upper() + c[1:], peso(p * 100), peso(n * 100)), "%d %%" % k,
                 ["%d %%" % (100 - k), "%d %%" % (k + 5), dec(round((p - n) * 100.0 / n, 1)) + " %"], "Descuento: %s de %s = %s ÷ %s = <b>%d %%</b>." % (num(p - n), num(p), num(p - n), num(p), k))
    if t == "total":
        k = R.choice([20, 25, 40, 60, 75])
        tot = R.choice([40, 60, 80, 120, 200, 240, 300])
        part = tot * k // 100
        if tot * k % 100:
            return None
        return M("En una escuela, %d alumnos son el %d %% de los alumnos de primer grado. ¿Cuántos alumnos de primer grado hay?" % (part, k), str(tot),
                 [str(part * k // 100 or 2), str(tot + part), str(part + k)], "%d ÷ %s = <b>%d</b>." % (part, dec(k / 100.0, 2), tot))
    cuenta = R.choice([480, 650, 820, 1240, 960])
    k = R.choice([10, 15])
    pr = cuenta * k / 100.0
    return M("Una cuenta en un restaurante es de %s y dejan %d %% de propina. ¿Cuánto es la propina?" % (peso(cuenta * 100), k), peso(int(round(pr * 100))),
             [peso(int(round(pr * 1000))), peso((cuenta + int(pr)) * 100), peso(k * 100)], "%d %% de %s = %s × %s = <b>%s</b>." % (k, num(cuenta), num(cuenta), dec(k / 100.0, 2), peso(int(round(pr * 100)))))


# ============================================================ proporcional / no proporcional
def tabla_html(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


CTX_P = [("Kilos de tortillas", "Precio ($)", 24), ("Litros de gasolina", "Precio ($)", 25), ("Horas trabajadas", "Pago ($)", 60), ("Cajas", "Botellas", 12), ("Minutos", "Litros", 8)]
CTX_N = [("Kilómetros en taxi", "Precio ($)", 8, 15), ("Meses", "Ahorro total ($)", 200, 500), ("Horas de renta de bici", "Precio ($)", 30, 20), ("Semanas", "Altura de la planta (cm)", 3, 5)]


def fu_table():
    xs = sorted(R.sample(range(1, 9), 4))
    prop = R.random() < .5
    if prop:
        a, b, k = R.choice(CTX_P)
        ys = [k * x for x in xs]
    else:
        a, b, k, c = R.choice(CTX_N)
        ys = [k * x + c for x in xs]
    t = tabla_html([a] + [str(x) for x in xs], [[b] + [num(y) for y in ys]])
    if R.random() < .6:
        ok = "Sí: el cociente siempre es %d" % k if prop else "No: el cociente no es constante"
        w = ["No: el cociente no es constante", "Sí: los dos valores aumentan", "No: los valores son muy grandes"] if prop else ["Sí: los dos valores aumentan", "Sí: el cociente siempre es %d" % k, "Sí: aumenta %d cada vez" % k]
        return M(t + "¿Es una relación de proporcionalidad directa?", ok, w,
                 ("%s ÷ %d = %d en todas las columnas: <b>sí es proporcional</b>." % (num(ys[0]), xs[0], k)) if prop else
                 ("%s ÷ %d ≠ %s ÷ %d: el cociente cambia, así que <b>no es proporcional</b> (hay una cantidad fija de %d)." % (num(ys[0]), xs[0], num(ys[-1]), xs[-1], c)))
    if prop:
        x = R.choice([v for v in range(2, 13) if v not in xs])
        return M(t + "Si la relación es proporcional, ¿qué valor corresponde a %d?" % x, num(k * x), [num(k * x + k), num(ys[-1] + (x - xs[-1])), num(k + x)],
                 "Constante de proporcionalidad: %d. %d × %d = <b>%s</b>." % (k, k, x, num(k * x)))
    return M(t + "¿Qué expresión relaciona las dos cantidades (x arriba, y abajo)?", "y = %dx + %d" % (k, c), ["y = %dx" % k, "y = %dx" % (ys[0] // xs[0]) if ys[0] % xs[0] == 0 and ys[0] // xs[0] != k else "y = %dx + %d" % (c, k), "y = x + %d" % (ys[0] - xs[0])],
             "Cada vez que x aumenta 1, y aumenta %d, y hay %d fijos: <b>y = %dx + %d</b> (no proporcional)." % (k, c, k, c))


def fu_graph():
    """gráfica sencilla: recta que pasa o no por el origen"""
    prop = R.random() < .5
    k = R.choice([1, 2, 3])
    b = 0 if prop else R.choice([1, 2, 3])
    W_, H_, ox, oy, u = 240, 200, 30, 175, 22
    s = [line(ox, oy, W_ - 10, oy, "#555", 1.5), line(ox, oy, ox, 10, "#555", 1.5)]
    for i in range(1, 9):
        s.append(line(ox + i * u, oy - 3, ox + i * u, oy + 3, "#555", 1))
        s.append(line(ox - 3, oy - i * u * .9, ox + 3, oy - i * u * .9, "#555", 1))
    s.append(text(ox - 8, oy + 14, "0", 11))
    s.append(text(W_ - 12, oy - 6, "x", 13))
    s.append(text(ox + 10, 16, "y", 13))
    x2 = min(8.0, (7.5 - b) / k)
    s.append(line(ox, oy - b * u * .9, ox + x2 * u, oy - (k * x2 + b) * u * .9, "#c0392b", 3))
    pic = fig(svg_wrap(W_, H_, "".join(s), "gráfica de una recta"))
    ok = "Sí: es una recta que pasa por el origen" if prop else "No: la recta no pasa por el origen"
    w = ["No: la recta no pasa por el origen", "Sí: es una recta", "No: la recta sube"] if prop else ["Sí: es una recta", "Sí: la recta sube", "Sí: es una recta que pasa por el origen"]
    return M(pic + "¿La gráfica representa una relación de proporcionalidad directa?", ok, w,
             "Una proporcionalidad directa se ve como una recta que <b>pasa por el origen (0, 0)</b>. Esta %s." % ("sí pasa" if prop else "empieza en y = %d" % b))


# ============================================================ rectas, ángulos y distancia
def ra_notacion():
    P = R.sample("ABCDEFGHMNPQRST", 3)
    t = R.choice(["vert", "vert", "seg", "semi", "tipo", "tipo", "simb"])
    if t == "vert":
        return M("En el ángulo ∠%s%s%s, ¿cuál es el vértice?" % tuple(P), P[1], [P[0], P[2], "%s%s" % (P[0], P[2])],
                 "En la notación de tres letras, el vértice es la letra de en medio: <b>%s</b>." % P[1])
    if t == "seg":
        L = R.randint(3, 15)
        return M("El segmento %s mide %d cm. ¿Cuánto mide el segmento %s?" % (ov(P[0] + P[1]), L, ov(P[1] + P[0])), "%d cm" % L, ["%d cm" % (2 * L), "0 cm", "no se puede saber"],
                 "%s y %s son el mismo segmento (los mismos extremos): <b>%d cm</b>." % (ov(P[0] + P[1]), ov(P[1] + P[0]), L))
    if t == "semi":
        q = R.choice([("Tiene dos extremos y se puede medir.", "segmento"), ("Tiene un origen y se prolonga sin fin en un solo sentido.", "semirrecta"),
                      ("No tiene principio ni fin.", "recta"), ("Lo forman dos semirrectas con el mismo origen.", "ángulo")])
        return M("¿Qué figura es? %s" % q[0], q[1], [x for x in ["segmento", "semirrecta", "recta", "ángulo"] if x != q[1]],
                 "<b>%s</b>." % q[1].capitalize())
    if t == "simb":
        q = R.choice([("r ⊥ s", "r y s son perpendiculares"), ("r ∥ s", "r y s son paralelas")])
        return M("¿Qué significa %s?" % q[0], q[1], ["r y s son perpendiculares" if "∥" in q[0] else "r y s son paralelas", "r y s son iguales", "r y s se cortan en un ángulo agudo"],
                 "El símbolo %s se lee «%s»: <b>%s</b>." % (q[0][2], "es perpendicular a" if "⊥" in q[0] else "es paralela a", q[1]))
    a = R.choice([R.randint(5, 85), 90, R.randint(95, 175), 180, R.randint(185, 355), 360])
    nm = "agudo" if a < 90 else "recto" if a == 90 else "obtuso" if a < 180 else "llano" if a == 180 else "entrante (cóncavo)" if a < 360 else "perigonal (completo)"
    return M("¿Cómo se clasifica un ángulo de %d°?" % a, nm, [x for x in ["agudo", "recto", "obtuso", "llano", "entrante (cóncavo)", "perigonal (completo)"] if x != nm][:3] if a not in (90, 180) else
             [x for x in ["agudo", "obtuso", "entrante (cóncavo)", "recto", "llano"] if x != nm][:3],
             "Agudo &lt; 90° &lt; obtuso &lt; 180° &lt; entrante &lt; 360°. Un ángulo de %d° es <b>%s</b>." % (a, nm))


def ra_distancia():
    t = R.choice(["recta", "recta", "plano", "plano", "concepto"])
    if t == "recta":
        a, b = R.sample(range(-15, 16), 2)
        if a * b >= 0 and R.random() < .6:
            return None
        return M("En la recta numérica, A está en %s y B en %s. ¿Cuál es la distancia entre A y B?" % (sg(a), sg(b)), str(abs(a - b)),
                 [str(abs(a + b)) if abs(a + b) != abs(a - b) else str(abs(a - b) + 2), sg(b - a) if b - a < 0 else sg(a - b), str(abs(a - b) + 1)],
                 "Distancia = |%s − (%s)| = <b>%d</b>. Una distancia nunca es negativa." % (sg(b), sg(a), abs(a - b)))
    if t == "plano":
        x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
        if R.random() < .5:
            y2 = R.choice([v for v in range(-7, 8) if v != y1])
            x2 = x1
            d = abs(y1 - y2)
        else:
            x2 = R.choice([v for v in range(-7, 8) if v != x1])
            y2 = y1
            d = abs(x1 - x2)
        w = [str(abs(x1 + x2 + y1 + y2)) if abs(x1 + x2 + y1 + y2) != d else str(d + 3), str(d + 1), str(abs(abs(x1 - x2) + abs(y1 - y2) + (y1 + y2 if x1 == x2 else x1 + x2))) if abs(abs(x1 - x2) + abs(y1 - y2) + (y1 + y2 if x1 == x2 else x1 + x2)) != d else str(d * 2)]
        return M("¿Cuál es la distancia entre los puntos A(%s, %s) y B(%s, %s)?" % (sg(x1), sg(y1), sg(x2), sg(y2)), str(d), w,
                 "Tienen la misma %s; restamos las otras coordenadas: |%s − (%s)| = <b>%d</b>." % ("abscisa (x)" if x1 == x2 else "ordenada (y)", sg(y2 if x1 == x2 else x2), sg(y1 if x1 == x2 else x1), d))
    a = R.randint(2, 9)
    b = a + R.randint(2, 9)
    return M("A, B y C están alineados en ese orden. AB = %d cm y AC = %d cm. ¿Cuánto mide BC?" % (a, b), "%d cm" % (b - a), ["%d cm" % (a + b), "%d cm" % a, "%d cm" % b],
             "La distancia entre dos puntos es la longitud del segmento que los une: BC = AC − AB = <b>%d cm</b>." % (b - a))


# ============================================================ construcciones con regla y compás
def mediatriz_svg(L, lab=True):
    W_, H_ = 300, 190
    ax, bx, y = 70, 230, 110
    mx = (ax + bx) / 2.0
    s = [line(ax, y, bx, y, "#222", 2.5), line(mx, 20, mx, 180, "#2b6cb0", 2, " stroke-dasharray='6 4'")]
    r = (bx - ax) * .7
    for cx, sgn in ((ax, 1), (bx, -1)):
        s.append("<path d='M%.1f %.1f A%.1f %.1f 0 0 %d %.1f %.1f' fill='none' stroke='#999' stroke-width='1.4'/>" % (cx + sgn * r * .55, y - r * .83, r, r, 1 if sgn > 0 else 0, cx + sgn * r * .55, y + r * .83))
    s += ["<circle cx='%.1f' cy='%d' r='4' fill='#222'/>" % (x, y) for x in (ax, bx)]
    s.append("<circle cx='%.1f' cy='%d' r='4' fill='#c0392b'/>" % (mx, y))
    s += [text(ax - 12, y + 6, "A", 16), text(bx + 12, y + 6, "B", 16), text(mx + 12, y + 20, "M", 16, col="#c0392b"), text(mx + 12, 30, "m", 15, italic=True, col="#2b6cb0")]
    if lab:
        s.append(text(mx - 40, y - 8, "%s cm" % dec(L), 13))
    return fig(svg_wrap(W_, H_, "".join(s), "mediatriz m del segmento AB con regla y compás"))


def bisectriz_svg(a):
    W_, H_ = 300, 200
    vx, vy, L = 50, 170, 220
    import math as m
    p1 = (vx + L, vy)
    p2 = (vx + L * m.cos(m.radians(a)), vy - L * m.sin(m.radians(a)))
    pb = (vx + L * .95 * m.cos(m.radians(a / 2.0)), vy - L * .95 * m.sin(m.radians(a / 2.0)))
    s = [line(vx, vy, p1[0], p1[1], "#222", 2.5), line(vx, vy, p2[0], p2[1], "#222", 2.5), line(vx, vy, pb[0], pb[1], "#2b6cb0", 2, " stroke-dasharray='6 4'"),
         text(vx - 12, vy + 6, "B", 16), text(p1[0] - 4, p1[1] + 18, "C", 16), text(p2[0] - 8, p2[1] - 6, "A", 16), text(pb[0] + 6, pb[1] - 4, "D", 16, col="#2b6cb0")]
    return fig(svg_wrap(W_, H_, "".join(s), "bisectriz BD del ángulo ABC"))


def cf_construccion(*ks):
    t = R.choice(ks or ["med", "med", "medP", "bis", "bis2", "perp", "par", "copia", "compas", "equi", "exist", "exist", "medio", "instr"])
    if t == "med":
        L = R.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 7.5, 8.4, 9.6])
        h = L / 2.0
        return M(mediatriz_svg(L) + "Con regla y compás se trazó la mediatriz m del segmento AB, que mide %s cm. ¿Cuánto mide AM?" % dec(L), "%s cm" % dec(h),
                 ["%s cm" % dec(L), "%s cm" % dec(L * 2), "%s cm" % dec(L / 4.0)], "La mediatriz pasa por el <b>punto medio</b> de AB: AM = %s ÷ 2 = <b>%s cm</b>." % (dec(L), dec(h)))
    if t == "medP":
        k = R.randint(4, 15)
        n = R.choice("PQRST")
        return M("El punto %s está sobre la mediatriz del segmento AB y %sA = %d cm. ¿Cuánto mide %sB?" % (n, n, k, n), "%d cm" % k, ["%d cm" % (2 * k), "%s cm" % dec(k / 2.0), "no se puede saber"],
                 "Todos los puntos de la mediatriz están a la <b>misma distancia</b> de A y de B: %sB = <b>%d cm</b>." % (n, k))
    if t == "bis":
        a = R.choice(range(30, 171, 2))
        return M(bisectriz_svg(min(a, 150)) + "BD es la bisectriz del ángulo ∠ABC, que mide %d°. ¿Cuánto mide ∠DBC?" % a, "%d°" % (a // 2), ["%d°" % a, "%d°" % (180 - a), "%d°" % (90 - a // 2)],
                 "La bisectriz divide el ángulo en dos ángulos iguales: %d° ÷ 2 = <b>%d°</b>." % (a, a // 2))
    if t == "bis2":
        h = R.randint(12, 85)
        return M("La bisectriz de un ángulo forma un ángulo de %d° con uno de sus lados. ¿Cuánto mide el ángulo completo?" % h, "%d°" % (2 * h), ["%d°" % h, "%d°" % (90 - h), "%d°" % (180 - h)],
                 "Las dos mitades son iguales: %d° × 2 = <b>%d°</b>." % (h, 2 * h))
    if t == "perp":
        q = R.choice([("Si r ⊥ s y s ⊥ t, ¿cómo son r y t?", "paralelas", ["perpendiculares", "se cortan en 45°", "son la misma recta siempre"]),
                      ("Si r ∥ s y t ⊥ r, ¿cómo son t y s?", "perpendiculares", ["paralelas", "se cortan en 45°", "no se cortan"]),
                      ("¿Qué ángulo forman dos rectas perpendiculares?", "90°", ["180°", "45°", "60°"]),
                      ("Para trazar una perpendicular a una recta por un punto P con regla y compás, primero se traza un arco con centro en P que corte la recta en dos puntos. ¿Qué se traza después?", "la mediatriz del segmento entre esos dos puntos", ["la bisectriz de un ángulo de 180°", "una circunferencia con centro en un extremo", "una paralela por P"])])
        return M(q[0], q[1], q[2], "<b>%s</b>." % (q[1][0].upper() + q[1][1:]))
    if t == "par":
        a = R.choice(range(35, 146, 5))
        return M("Para trazar por un punto P una paralela a la recta r, se traza una recta auxiliar que corta a r formando un ángulo de %d°. ¿Qué ángulo hay que copiar en P, en la misma posición?" % a,
                 "%d°" % a, ["%d°" % (180 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90), "90°"],
                 "Si los ángulos correspondientes son iguales, las rectas son paralelas: se copia el mismo ángulo de <b>%d°</b>." % a)
    if t == "copia":
        L = R.choice([4.5, 5.2, 6, 6.8, 7.3, 8, 9.5])
        return M("Quieres trazar un segmento congruente (igual) a otro de %s cm usando el compás. ¿Qué abertura debe tener el compás?" % dec(L), "%s cm" % dec(L),
                 ["%s cm" % dec(L / 2), "%s cm" % dec(L * 2), "cualquier abertura"], "Segmentos congruentes miden lo mismo: abres el compás <b>%s cm</b>." % dec(L))
    if t == "compas":
        r = R.choice([2.5, 3, 3.5, 4, 4.5, 5, 6])
        return M("Con el compás abierto %s cm trazas una circunferencia. ¿Cuánto mide su diámetro?" % dec(r), "%s cm" % dec(2 * r), ["%s cm" % dec(r), "%s cm" % dec(r / 2), "%s cm" % dec(r * 3.14, 2)],
                 "La abertura del compás es el radio; el diámetro es el doble: <b>%s cm</b>." % dec(2 * r))
    if t == "equi":
        L = R.randint(3, 9)
        return M("Para construir con regla y compás un triángulo equilátero de lado %d cm, trazas el lado AB y luego dos arcos con centro en A y en B. ¿Qué radio deben tener los arcos?" % L, "%d cm" % L,
                 ["%s cm" % dec(L / 2.0), "%d cm" % (2 * L), "%d cm" % (3 * L)], "Los tres lados miden lo mismo: los arcos tienen radio <b>%d cm</b>." % L)
    if t == "exist":
        a, b = R.randint(2, 9), R.randint(2, 9)
        c = R.choice([a + b + R.randint(1, 3), a + b, abs(a - b) + R.randint(1, min(a, b) * 2 - 1)])
        okb = a + b > c and a + c > b and b + c > a
        ok = "Sí" if okb else "No"
        return M("¿Se puede construir un triángulo con lados de %d cm, %d cm y %d cm?" % (a, b, c), ok + (": cada lado es menor que la suma de los otros dos" if okb else ": %d + %d no es mayor que %d" % (min(a, b, c), sorted([a, b, c])[1], max(a, b, c))),
                 ["Sí: con cualquier medida se puede", "No: los lados deben ser iguales", "Sí: cada lado es menor que la suma de los otros dos" if not okb else "No: %d + %d no es mayor que %d" % (min(a, b, c), sorted([a, b, c])[1], max(a, b, c))],
                 "Un triángulo existe si cada lado es menor que la suma de los otros dos. %d + %d %s %d: <b>%s</b>." % (sorted([a, b, c])[0], sorted([a, b, c])[1], "&gt;" if okb else "≤", max(a, b, c), ok.lower()))
    if t == "medio":
        a, b = R.sample(range(-12, 21, 2), 2)
        m = (a + b) // 2
        return M("En la recta numérica, A está en %s y B en %s. ¿Dónde está el punto medio de AB?" % (sg(a), sg(b)), sg(m), [sg(abs(b - a) // 2), sg(a + b), sg(m + 1)],
                 "El punto medio está a la misma distancia de A y de B: (%s + %s) ÷ 2 = <b>%s</b>." % (sg(a), sg(b), sg(m)))
    q = R.choice([("¿Qué instrumento sirve para trasladar una medida sin usar números?", "el compás"), ("¿Qué instrumento se usa para trazar líneas rectas sin medir?", "la regla"),
                  ("¿Qué recta se traza para dividir un segmento en dos partes iguales?", "la mediatriz"), ("¿Qué recta divide un ángulo en dos ángulos iguales?", "la bisectriz")])
    pool = ["el compás", "la regla", "el transportador", "la escuadra"] if q[1] in ("el compás", "la regla") else ["la mediatriz", "la bisectriz", "la altura", "una tangente"]
    return M(q[0], q[1], [x for x in pool if x != q[1]], "<b>%s</b>." % (q[1][0].upper() + q[1][1:]))


# ============================================================ circunferencia: rectas notables
def circ_svg(ask):
    W_, H_, cx, cy, r = 300, 230, 145, 115, 78
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#222' stroke-width='2.5'/>" % (cx, cy, r), "<circle cx='%d' cy='%d' r='3.5' fill='#222'/>" % (cx, cy), text(cx - 10, cy + 16, "O", 14)]
    pt = lambda deg: (cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg)))
    els = {}
    A = pt(30)
    els["radio"] = [line(cx, cy, A[0], A[1], "#c0392b", 2.5), text(A[0] + 10, A[1] - 2, "A", 14)]
    B, C = pt(160), pt(340)
    els["diámetro"] = [line(B[0], B[1], C[0], C[1], "#2b6cb0", 2.5), text(B[0] - 12, B[1] - 2, "B", 14), text(C[0] + 10, C[1] + 10, "C", 14)]
    D, E = pt(200), pt(260)
    els["cuerda"] = [line(D[0], D[1], E[0], E[1], "#7d3c98", 2.5), text(D[0] - 12, D[1] + 6, "D", 14), text(E[0] - 4, E[1] + 18, "E", 14)]
    T = pt(90)
    els["tangente"] = [line(T[0] - 110, T[1], T[0] + 110, T[1], "#1e8449", 2.5), text(T[0] + 4, T[1] - 6, "T", 14)]
    s1, s2 = (cx - r - 30, cy + 70), (cx + r + 30, cy - 5)
    els["secante"] = [line(s1[0], s1[1], s2[0], s2[1], "#d35400", 2.5)]
    show = R.sample([k for k in els if k != ask], 2) + [ask]
    for k in show:
        s += els[k]
    lab = {"radio": "el segmento OA", "diámetro": "el segmento BC", "cuerda": "el segmento DE", "tangente": "la recta que toca la circunferencia solo en T",
           "secante": "la recta naranja que corta la circunferencia en dos puntos"}[ask]
    return fig(svg_wrap(W_, H_, "".join(s), "circunferencia con centro O y algunas de sus rectas notables")), lab


def cc_rectas(*ks):
    t = R.choice(ks or ["fig", "fig", "fig", "rd", "dist", "dist", "tang", "cuerda", "puntos", "mitad"])
    if t == "fig":
        ask = R.choice(["radio", "diámetro", "cuerda", "tangente", "secante"])
        pic, lab = circ_svg(ask)
        return M(pic + "En la figura, ¿qué es %s?" % lab, "un%s %s" % ("a" if ask in ("cuerda", "tangente", "secante") else "", ask),
                 ["un%s %s" % ("a" if x in ("cuerda", "tangente", "secante") else "", x) for x in ["radio", "diámetro", "cuerda", "tangente", "secante"] if x != ask],
                 {"radio": "Une el centro con un punto de la circunferencia: <b>radio</b>.", "diámetro": "Une dos puntos pasando por el centro: <b>diámetro</b>.",
                  "cuerda": "Une dos puntos de la circunferencia sin pasar por el centro: <b>cuerda</b>.", "tangente": "Toca la circunferencia en un solo punto: <b>tangente</b>.",
                  "secante": "Corta la circunferencia en dos puntos: <b>secante</b>."}[ask])
    if t == "rd":
        r = R.choice([3, 4.5, 6, 7.5, 8, 9, 12.5, 15, 18])
        if R.random() < .5:
            return M("Una circunferencia tiene %s cm de radio. ¿Cuánto mide su diámetro?" % dec(r), "%s cm" % dec(2 * r), ["%s cm" % dec(r / 2), "%s cm" % dec(r), "%s cm" % dec(r * 3.14, 2)],
                     "Diámetro = 2 × radio = <b>%s cm</b>." % dec(2 * r))
        return M("El diámetro de una rueda mide %s cm. ¿Cuánto mide su radio?" % dec(2 * r), "%s cm" % dec(r), ["%s cm" % dec(4 * r), "%s cm" % dec(2 * r), "%s cm" % dec(r / 2)],
                 "Radio = diámetro ÷ 2 = <b>%s cm</b>." % dec(r))
    if t == "dist":
        r = R.randint(3, 12)
        d = R.choice([r - R.randint(1, r - 1), r, r + R.randint(1, 6)])
        ok = "secante" if d < r else "tangente" if d == r else "exterior"
        return M("Una circunferencia tiene radio %d cm y la distancia de su centro a una recta es %d cm. ¿Cómo es la recta?" % (r, d), ok,
                 [x for x in ["secante", "tangente", "exterior", "un diámetro"] if x != ok],
                 "Si la distancia es menor que el radio, es secante; igual, tangente; mayor, exterior. %d %s %d: <b>%s</b>." % (d, "&lt;" if d < r else "=" if d == r else "&gt;", r, ok))
    if t == "tang":
        return M("¿Qué ángulo forma una recta tangente con el radio que llega al punto de tangencia?", "90°", ["180°", "45°", "60°"],
                 "La tangente es siempre <b>perpendicular</b> al radio en el punto de tangencia: 90°.") if R.random() < .5 else \
            M("¿Cuál es la cuerda más larga de una circunferencia?", "el diámetro", ["el radio", "cualquier cuerda", "la tangente"], "La cuerda más larga es la que pasa por el centro: <b>el diámetro</b>.")
    if t == "cuerda":
        r = R.randint(4, 12)
        c = R.choice([2 * r - R.randint(1, 3), 2 * r + R.randint(1, 4), 3 * r, 2 * r + 7])
        okv = c - R.randint(1, 3) if c > 2 * r else c
        okv = min(okv, 2 * r)
        opts = [2 * r + 1, 2 * r + 4, 3 * r]
        return M("Una circunferencia tiene %d cm de radio. ¿Cuál de estas puede ser la longitud de una cuerda?" % r, "%d cm" % okv, ["%d cm" % x for x in opts if x != okv],
                 "Ninguna cuerda puede ser mayor que el diámetro (%d cm): <b>%d cm</b>." % (2 * r, okv))
    if t == "puntos":
        q = R.choice([("secante", "2"), ("tangente", "1"), ("exterior", "0")])
        return M("¿En cuántos puntos corta a la circunferencia una recta %s?" % q[0], q[1], [x for x in ["0", "1", "2", "3"] if x != q[1]],
                 "Exterior: 0 puntos; tangente: 1; secante: 2. Respuesta: <b>%s</b>." % q[1])
    c = R.choice([6, 8, 10, 12, 14, 16, 18, 20, 24])
    return M("Desde el centro O se traza una perpendicular a la cuerda AB, que mide %d cm, y la corta en M. ¿Cuánto mide AM?" % c, "%d cm" % (c // 2), ["%d cm" % c, "%d cm" % (c // 4) if c % 4 == 0 else "%s cm" % dec(c / 4.0), "%d cm" % (2 * c)],
             "La perpendicular desde el centro corta la cuerda en su punto medio: <b>%d cm</b>." % (c // 2))


# ============================================================ sistema inglés
EQ = {"pulgada": (2.54, "cm"), "yarda": (0.9144, "m"), "galón": (3.785, "L"), "libra": (0.4536, "kg"), "onza": (28.35, "g")}
EQS = {"pulgada": "2.54", "yarda": "0.9144", "galón": "3.785", "libra": "0.4536", "onza": "28.35"}
PL = {"pulgada": "pulgadas", "yarda": "yardas", "galón": "galones", "libra": "libras", "onza": "onzas"}
CTX_I = {"pulgada": ["Una pantalla de %s pulgadas mide eso en diagonal.", "Una televisión de %s pulgadas mide eso en diagonal."],
         "yarda": ["En el futbol americano, un equipo avanzó %s yardas.", "Un rollo de tela tiene %s yardas."],
         "galón": ["Un garrafón de agua tiene %s galones.", "Una cubeta de pintura tiene %s galones."],
         "libra": ["Unas pesas para hacer ejercicio pesan %s libras.", "Un paquete de carne pesa %s libras."],
         "onza": ["Un bistec pesa %s onzas.", "Una lata de atún tiene %s onzas."]}
VALS = {"pulgada": [24, 32, 40, 43, 50, 55, 65, 3, 6], "yarda": [10, 15, 20, 25, 40, 50], "galón": [2, 4, 5, 10, 20], "libra": [5, 8, 10, 15, 20, 25], "onza": [4, 6, 8, 10, 12, 16]}


def ingles(*ks):
    t = R.choice(ks or ["a_metrico", "a_metrico", "a_metrico", "a_ingles", "interno", "comparar"])
    u = R.choice(list(EQ))
    f, mu = EQ[u]
    if t == "a_metrico":
        v = R.choice(VALS[u])
        if u == "pulgada" and v < 10:
            ctx0 = R.choice(["Un tubo tiene un diámetro de %s pulgadas.", "Una llave de tuercas mide %s pulgadas."])
        else:
            ctx0 = None
        res = round(v * f, 2)
        ctx = (ctx0 or R.choice(CTX_I[u])) % num(v)
        ok = "%s %s" % (dec(res), mu)
        return M("%s Si 1 %s = %s %s, ¿cuánto es en %s? (redondea a centésimos)" % (ctx, u, EQS[u], mu, mu), ok,
                 ["%s %s" % (dec(round(v / f, 2)), mu), "%s %s" % (dec(round(res * 10, 2)), mu), "%s %s" % (dec(round(v + f, 2)), mu)],
                 "Multiplicamos: %s × %s = <b>%s</b>." % (num(v), EQS[u], ok))
    if t == "a_ingles":
        v = R.choice([5.08, 10.16, 25.4, 76.2]) if u == "pulgada" else None
        if u == "pulgada":
            n = round(v / f)
            return M("Un tornillo mide %s cm. Si 1 pulgada = 2.54 cm, ¿cuántas pulgadas mide?" % dec(v), "%d pulgadas" % n if n != 1 else "1 pulgada",
                     ["%s pulgadas" % dec(round(v * f, 2)), "%d pulgadas" % (n * 10), "%d pulgadas" % (n + 1)], "Dividimos: %s ÷ 2.54 = <b>%d</b>." % (dec(v), n))
        n = R.choice([2, 3, 4, 5, 10])
        tot = round(n * f, 3 if u != "onza" else 2)
        obj = {"yarda": "Un rollo de listón mide", "galón": "Un tinaco pequeño tiene", "libra": "Un costal de frijol pesa", "onza": "Un paquete de queso pesa"}[u]
        return M("%s %s %s. Si 1 %s = %s %s, ¿cuánt%s %s son?" % (obj, dec(tot), mu, u, EQS[u], mu, "os" if u == "galón" else "as", PL[u]), "%d %s" % (n, PL[u]),
                 ["%s %s" % (dec(round(tot * f, 2)), PL[u]), "%d %s" % (n * 10, PL[u]), "%d %s" % (n + 1, PL[u])], "Dividimos entre %s: <b>%d %s</b>." % (EQS[u], n, PL[u]))
    if t == "interno":
        q = R.choice([("yardas", "pulgadas", 36), ("libras", "onzas", 16), ("pies", "pulgadas", 12), ("yardas", "pies", 3)])
        n = R.randint(2, 9)
        return M("Si 1 %s = %d %s, ¿cuánt%s %s son %d %s?" % (q[0][:-1] if q[0] != "pies" else "pie", q[2], q[1], "os" if q[1] == "pies" else "as", q[1], n, q[0]), "%d %s" % (n * q[2], q[1]),
                 ["%d %s" % (n + q[2], q[1]), "%s %s" % (dec(round(n / float(q[2]), 2)), q[1]), "%d %s" % (n * q[2] + q[2], q[1])], "%d × %d = <b>%d %s</b>." % (n, q[2], n * q[2], q[1]))
    n = R.choice([3, 4, 5, 6, 10])
    if u in ("galón",):
        m = round(n * f)
        other = m + R.choice([-1, 1])
        big = "%d galones" % n if n * f > other else "%d L" % other
        return M("¿Qué es más: %d galones o %d litros? (1 galón = 3.785 L)" % (n, other), big, ["%d L" % other if big.endswith("galones") else "%d galones" % n, "son iguales", "no se pueden comparar"],
                 "%d galones = %s L. Comparamos con %d L: <b>%s</b>." % (n, dec(round(n * f, 2)), other, big))
    m = round(n * 0.4536, 2)
    other = round(m + R.choice([-0.3, 0.3]), 1)
    big = "%d libras" % n if m > other else "%s kg" % dec(other)
    return M("¿Qué pesa más: %d libras de frijol o %s kg de arroz? (1 libra = 0.4536 kg)" % (n, dec(other)), big,
             ["%s kg" % dec(other) if big.endswith("libras") else "%d libras" % n, "pesan lo mismo", "no se pueden comparar"],
             "%d libras = %s kg. Comparamos con %s kg: <b>%s</b>." % (n, dec(m), dec(other), big))


# ============================================================ cuerpos geométricos
POLY = {3: "triangular", 4: "cuadrangular", 5: "pentagonal", 6: "hexagonal", 7: "heptagonal", 8: "octagonal", 10: "decagonal", 12: "dodecagonal"}


def cuerpos(*ks):
    t = R.choice(ks or ["cvA", "cvA", "cvA", "euler", "base", "nopoli", "lat", "redondo"])
    n = R.choice(list(POLY))
    if t in ("cvA", "cvAp", "cvAy"):
        k = {"cvAp": "prisma", "cvAy": "pirámide"}.get(t) or R.choice(["prisma", "pirámide"])
        p = R.choice(["caras", "vértices", "aristas"])
        val = {("prisma", "caras"): n + 2, ("prisma", "vértices"): 2 * n, ("prisma", "aristas"): 3 * n,
               ("pirámide", "caras"): n + 1, ("pirámide", "vértices"): n + 1, ("pirámide", "aristas"): 2 * n}[(k, p)]
        alt = [n + 2, 2 * n, 3 * n, n + 1, n, 2 * n + 2]
        return M("¿Cuánt%s %s tiene %s %s %s?" % ("os" if p == "vértices" else "as", p, "un" if k == "prisma" else "una", k, POLY[n]), str(val), [str(x) for x in alt if x != val],
                 {"caras": "%s" % ("2 bases + %d caras laterales" % n if k == "prisma" else "1 base + %d caras laterales" % n),
                  "vértices": "%s" % ("%d arriba + %d abajo" % (n, n) if k == "prisma" else "%d de la base + la cúspide" % n),
                  "aristas": "%s" % ("%d de cada base + %d laterales" % (n, n) if k == "prisma" else "%d de la base + %d laterales" % (n, n))}[p] + ": <b>%d</b>." % val)
    if t == "euler":
        c, v = R.choice([(n + 2, 2 * n), (n + 1, n + 1)])
        a = c + v - 2
        return M("Un poliedro tiene %d caras y %d vértices. Por la fórmula de Euler (C + V = A + 2), ¿cuántas aristas tiene?" % (c, v), str(a), [str(c + v), str(c + v + 2), str(abs(c - v) + 2) if abs(c - v) + 2 != a else str(a + 1)],
                 "A = C + V − 2 = %d + %d − 2 = <b>%d</b>." % (c, v, a))
    if t in ("base", "basep", "basey"):
        k = {"basep": "prisma", "basey": "pirámide"}.get(t) or R.choice(["prisma", "pirámide"])
        return M("La base de %s %s %s es un polígono de… " % ("un" if k == "prisma" else "una", k, POLY[n]), "%d lados" % n, ["%d lados" % (n + 1), "%d lados" % (n + 2), "%d lados" % (2 * n)],
                 "El nombre lo da la base: %s → <b>%d lados</b>." % (POLY[n], n))
    if t == "nopoli":
        no = R.choice(["un cilindro", "un cono", "una esfera"])
        return M("¿Cuál de estos cuerpos NO es un poliedro?", no, ["un cubo", "un prisma %s" % POLY[n], "una pirámide %s" % POLY[R.choice([3, 4, 5])]],
                 "Los poliedros solo tienen caras planas. %s tiene superficie curva: <b>no es poliedro</b>." % no.capitalize())
    if t in ("lat", "latp", "laty"):
        k = {"latp": ("prisma", "rectángulos (paralelogramos)"), "laty": ("pirámide", "triángulos")}.get(t) or R.choice([("prisma", "rectángulos (paralelogramos)"), ("pirámide", "triángulos")])
        return M("¿Qué forma tienen las caras laterales de %s %s %s?" % ("un" if k[0] == "prisma" else "una", k[0], POLY[n]), k[1],
                 [x for x in ["rectángulos (paralelogramos)", "triángulos", "círculos", "polígonos de %d lados" % n] if x != k[1]], "<b>%s</b>." % k[1].capitalize())
    q = R.choice([("¿Qué cuerpo tiene dos bases circulares iguales y paralelas?", "el cilindro", ["el cono", "la esfera", "el prisma"]),
                  ("¿Qué cuerpo tiene una base circular y un vértice (cúspide)?", "el cono", ["el cilindro", "la esfera", "la pirámide"]),
                  ("¿Qué cuerpo tiene todos sus puntos a la misma distancia del centro?", "la esfera", ["el cono", "el cilindro", "el cubo"]),
                  ("¿Cuántas caras tiene un cubo?", "6", ["8", "12", "4"]), ("¿Cuántas aristas tiene un cubo?", "12", ["6", "8", "24"]),
                  ("¿Cuántas bases tiene un cilindro?", "2", ["1", "0", "3"]), ("¿Cuántas bases tiene un cono?", "1", ["2", "0", "3"]),
                  ("¿Cuántos vértices tiene un cono?", "1", ["0", "2", "3"]), ("Al girar un rectángulo sobre uno de sus lados se forma…", "un cilindro", ["un cono", "una esfera", "un prisma"]),
                  ("Al girar un triángulo rectángulo sobre uno de sus catetos se forma…", "un cono", ["un cilindro", "una esfera", "una pirámide"]),
                  ("Al girar un semicírculo sobre su diámetro se forma…", "una esfera", ["un cono", "un cilindro", "un círculo"]),
                  ("¿Qué figura se obtiene al cortar una esfera con un plano?", "un círculo", ["un cuadrado", "un triángulo", "un rectángulo"]),
                  ("¿Qué figura tiene la base de un cono?", "un círculo", ["un triángulo", "un cuadrado", "un óvalo"]),
                  ("¿Qué cuerpo redondo tiene la forma de una lata de chiles?", "el cilindro", ["el cono", "la esfera", "el prisma"]),
                  ("¿Qué cuerpo tiene la forma de un balón de futbol?", "la esfera", ["el cilindro", "el cono", "el cubo"]),
                  ("¿Qué cuerpo tiene la forma de un gorro de fiesta?", "el cono", ["el cilindro", "la esfera", "la pirámide"]),
                  ("Los cuerpos con alguna superficie curva se llaman…", "cuerpos redondos", ["poliedros", "prismas", "pirámides"])])
    return M(q[0], q[1], q[2], "<b>%s</b>." % q[1].capitalize())


# ============================================================ gráfica circular: porcentajes y grados
def circular():
    t = R.choice(["pg", "gp", "datos", "datos"])
    if t == "pg":
        p = R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 75])
        g = p * 360 // 100
        return M("En una gráfica circular, ¿cuántos grados le corresponden al %d %%?" % p, "%d°" % g, ["%d°" % p, "%d°" % (g // 2), "%d°" % (360 - g)], "%d %% de 360° = 360 × %s = <b>%d°</b>." % (p, dec(p / 100.0, 2), g))
    if t == "gp":
        g = R.choice([36, 72, 90, 108, 144, 180, 216, 270, 54, 18])
        p = g * 100 / 360.0
        return M("Un sector de una gráfica circular mide %d°. ¿Qué porcentaje representa?" % g, "%s %%" % dec(p), ["%d %%" % g, "%s %%" % dec(round(p / 2, 1)), "%s %%" % dec(100 - p)],
                 "%d ÷ 360 = %s → <b>%s %%</b>." % (g, dec(round(g / 360.0, 3)), dec(p)))
    tot = R.choice([40, 60, 80, 120, 200, 240, 360, 400])
    f = R.choice([F(1, 4), F(1, 2), F(1, 5), F(3, 10), F(1, 8), F(3, 4), F(1, 10), F(2, 5)])
    if (tot * f).denominator != 1:
        return None
    n = int(tot * f)
    g = int(360 * f)
    deporte = R.choice(["futbol", "basquetbol", "beisbol", "voleibol", "natación"])
    return M("Se preguntó a %d alumnos su deporte favorito y %d eligieron %s. ¿Cuántos grados mide ese sector en la gráfica circular?" % (tot, n, deporte), "%d°" % g,
             ["%d°" % n, "%s %%" % dec(float(f * 100)), "%d°" % (360 - g)], "%d de %d = %s del total; %s de 360° = <b>%d°</b>." % (n, tot, fq(f), fq(f), g))


# ============================================================ sucesiones de figuras (progresión aritmética)
FIG_CTX = [("palillos", "cuadrados en fila", 3, 1), ("palillos", "triángulos en fila", 2, 1), ("puntos", "filas de puntos", 4, 0), ("cuadritos", "escaleras", 2, 1), ("sillas", "mesas juntas", 2, 2), ("puntos", "figuras en forma de L", 2, 1)]


def dots_svg(cnts, label):
    W_, H_ = 90 * len(cnts) + 20, 120
    s = []
    for i, c in enumerate(cnts):
        x0 = 20 + i * 90
        cols = 6
        for j in range(c):
            s.append("<circle cx='%d' cy='%d' r='4.5' fill='#2b6cb0'/>" % (x0 - 6 + (j % cols) * 13, 16 + (j // cols) * 13))
        s.append(text(x0 + 24, 112, "Figura %d" % (i + 1), 12))
    return fig(svg_wrap(W_, H_, "".join(s), label))


def sc_figuras(*ks):
    t = R.choice(ks or ["cuenta", "cuenta", "regla", "lugar"])
    d = R.randint(2, 6)
    b = R.randint(0, 5)
    first = [d * n + b for n in (1, 2, 3)]
    if first[2] > 28:
        return None
    pic = dots_svg(first, "sucesión de figuras con %d, %d y %d puntos" % tuple(first))
    if t == "cuenta":
        n = R.choice([6, 8, 10, 12, 15, 20, 25])
        v = d * n + b
        return M(pic + "Cada figura tiene %d puntos más que la anterior. ¿Cuántos puntos tendrá la figura %d?" % (d, n), str(v), [str(d * n), str(first[0] * n), str(v + d)],
                 "Regla: %s. Figura %d: %d × %d%s = <b>%d</b>." % (expr_n(d, b), n, d, n, (" + %d" % b) if b else "", v))
    if t == "regla":
        ok = expr_n(d, b)
        return M(pic + "¿Qué expresión da el número de puntos de la figura n?", ok, [expr_n(first[0], 0), expr_n(d, first[0]) if first[0] != b else expr_n(d + 1, b), "n + %d" % d],
                 "Aumenta %d cada vez (diferencia %d) y en la figura 1 hay %d: %d × 1 + %d. Regla: <b>%s</b>." % (d, d, first[0], d, b, ok))
    v = d * R.randint(8, 30) + b
    n = (v - b) // d
    return M(pic + "Con la regla %s, ¿qué figura tiene %d puntos?" % (expr_n(d, b), v), "la figura %d" % n, ["la figura %d" % (v // d + 1 if v % d else v // d + 2), "la figura %d" % (n + 1), "la figura %d" % (v - b)],
             "%s = %d → %dn = %d → n = <b>%d</b>." % (expr_n(d, b), v, d, v - b, n))


def expr_n(d, b):
    return ("%dn" % d if d != 1 else "n") + ((" + %d" % b) if b > 0 else (" − %d" % -b) if b < 0 else "")


def sc_contexto():
    obj, fig_, d, b = R.choice(FIG_CTX)
    n = R.choice([5, 7, 10, 12, 15, 20, 30, 50])
    v = d * n + b
    first = [d * k + b for k in (1, 2, 3)]
    return M("Con %s se forman %s: la figura 1 usa %d, la 2 usa %d y la 3 usa %d. ¿Cuántos %s usa la figura %d?" % (obj, fig_, first[0], first[1], first[2], obj, n), str(v),
             [str(first[0] * n), str(v + d), str(d * n)], "Aumenta %d cada vez: regla %s. Figura %d: <b>%d</b>." % (d, expr_n(d, b), n, v))


def arit(it):
    """solo sucesiones aritméticas (deja fuera cuadráticas, geométricas y de Fibonacci)"""
    import re as _re
    t = _re.sub(r"<[^>]+>", "", it["q"])
    m = _re.search(r"([−\-]?\d+(?:; [−\-]?\d+){3,});", t)
    if m:
        xs = [int(x.replace("−", "-")) for x in m.group(1).split("; ")]
        ds = set(b - a for a, b in zip(xs, xs[1:]))
        if len(ds) != 1:
            return False
    if _re.search(r"n²|n / |\^|%|anteriores|mitad|doble|razón|geom", t):
        return False
    return True


# ============================================================ comparar probabilidades (cualitativo)
COLS = ["rojas", "azules", "verdes", "amarillas", "blancas", "negras"]


def az_compara(*ks):
    t = R.choice(ks or ["urna", "urna", "dado", "ruleta", "escala"])
    if t == "urna":
        cs = R.sample(COLS, 3)
        ns = R.sample(range(1, 13), 3)
        i, j = R.sample(range(3), 2)
        SG_ = {"rojas": "roja", "azules": "azul", "verdes": "verde", "amarillas": "amarilla", "blancas": "blanca", "negras": "negra"}
        a, b = SG_[cs[i]], SG_[cs[j]]
        txt = ", ".join("%d %s" % (n, c) for n, c in zip(ns, cs))
        ok = "una %s" % (a if ns[i] > ns[j] else b)
        return M("Una bolsa tiene canicas: %s. Sacas una sin ver. ¿Qué es más probable: sacar una %s o una %s?" % (txt, a, b), ok,
                 ["una %s" % (b if ns[i] > ns[j] else a), "las dos son igual de probables", "no se puede saber"],
                 "Hay %d %s y %d %s: es más probable sacar <b>%s</b>." % (ns[i], cs[i], ns[j], cs[j], ok))
    if t == "dado":
        evs = [("sacar un número par", 3), ("sacar un 6", 1), ("sacar un número menor que 5", 4), ("sacar un múltiplo de 3", 2), ("sacar un número mayor que 1", 5), ("sacar un 7", 0), ("sacar un número primo", 3)]
        e1, e2 = R.sample(evs, 2)
        if e1[1] == e2[1]:
            ok = "son igual de probables"
        else:
            ok = ("es más probable " if e1[1] > e2[1] else "es menos probable ") + e1[0]
        w = [x for x in ["es más probable " + e1[0], "es menos probable " + e1[0], "son igual de probables", "no se puede saber"] if x != ok]
        return M("Al lanzar un dado, compara: «%s» y «%s»." % (e1[0], e2[0]), ok, w,
                 "Casos favorables: %d y %d de 6: <b>%s</b>." % (e1[1], e2[1], ok))
    if t == "ruleta":
        n = R.choice([8, 10, 12])
        a = R.randint(1, n - 2)
        b = R.randint(1, n - a - 1)
        if a == b:
            return None
        c1, c2 = R.sample(["rojo", "azul", "verde", "amarillo"], 2)
        ok = "%s, porque tiene más sectores" % (c1 if a > b else c2)
        return M("Una ruleta tiene %d sectores iguales: %d de color %s, %d de color %s y el resto blancos. ¿Qué color es más probable que salga?" % (n, a, c1, b, c2), ok,
                 ["%s, porque tiene más sectores" % (c2 if a > b else c1), "los dos son igual de probables", "blanco, siempre"] if n - a - b < max(a, b) else ["%s, porque tiene más sectores" % (c2 if a > b else c1), "los dos son igual de probables", "no se puede saber"],
                 "%d sectores %s contra %d %s: <b>%s</b>." % (a, c1, b, c2, c1 if a > b else c2))
    q = R.choice([("Que salga el sol mañana", "seguro"), ("Sacar un 8 con un dado normal", "imposible"), ("Que una moneda caiga águila", "probable"), ("Sacar una canica roja de una bolsa con solo canicas rojas", "seguro"),
                  ("Sacar un 10 al sumar dos dados", "poco probable"), ("Sacar 1 o más con un dado", "seguro"), ("Que llueva en Mérida un día de junio", "probable"), ("Sacar una canica verde de una bolsa sin canicas verdes", "imposible")])
    return M("¿Cómo es este evento? «%s»." % q[0], q[1], [x for x in ["seguro", "imposible", "probable", "poco probable"] if x != q[1]], "Es un evento <b>%s</b>." % q[1])
