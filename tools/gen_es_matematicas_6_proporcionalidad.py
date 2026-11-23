# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Proporcionalidad (Sentido numérico)
Magnitudes directamente proporcionales, tablas de proporcionalidad, reducción a la unidad y regla de tres,
razón, escalas en planos y mapas; 6.º también magnitudes no proporcionales.
Errores: sumar en lugar de multiplicar en una tabla, usar la escala al revés, creer que todo es proporcional (la edad y la altura).
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d, table

R = None
LV = 6
COSAS = [("kg de naranjas", "€", F(3, 2)), ("entradas", "€", 8), ("cuadernos", "€", F(5, 2)), ("horas de trabajo", "€", 12), ("litros de gasolina", "€", F(8, 5)), ("botes de pintura", "€", 9),
         ("paquetes de galletas", "€", 2), ("vueltas a la pista", "metros", 400), ("cajas", "botellas", 6), ("bolsas", "caramelos", 15)]


def s1_tabla():
    nm, u, k = R.choice(COSAS)
    xs = sorted(R.sample(range(1, 11), 4))
    ys = [F(x) * k for x in xs]
    i = R.randrange(1, 4)
    shown = [d(y) if j != i else "?" for j, y in enumerate(ys)]
    tb = table([nm.capitalize()] + [str(x) for x in xs], [[u] + shown])
    ans = d(ys[i])
    add = ys[i - 1] + (xs[i] - xs[i - 1])
    return M(tb + "La tabla es de proporcionalidad directa. ¿Qué número va en «?»?", ans, [d(add) if add != ys[i] else None, d(ys[i] + k), d(ys[i] - k) if ys[i] > k else d(ys[i] * 2), d(ys[i] * 10)],
             "Cada %s vale %s %s: %d × %s = <b>%s</b>." % ("unidad", d(F(k)), u, xs[i], d(F(k)), ans))


def s2_regla():
    nm, u, k = R.choice(COSAS)
    a, b = R.sample(range(2, 13), 2)
    ya, yb = F(a) * k, F(b) * k
    if u == "€":
        txt = "Si %d %s cuestan %s €, ¿cuánto cuestan %d %s?" % (a, nm, d(ya), b, nm)
        ans = "%s €" % d(yb)
        w = ["%s €" % d(ya + b - a) if ya + b - a > 0 else None, "%s €" % d(ya * b), "%s €" % d(yb + k), "%s €" % d(F(b, a))]
    else:
        txt = "Si en %d %s hay %s %s, ¿cuántos %s hay en %d %s?" % (a, nm, d(ya), u, u, b, nm)
        ans = "%s %s" % (d(yb), u)
        w = ["%s %s" % (d(ya + b - a), u) if ya + b - a > 0 else None, "%s %s" % (d(ya * b), u), "%s %s" % (d(yb + k), u)]
    return M(txt, ans, w, "Reducimos a la unidad: 1 → %s : %d = %s; %d → %s × %d = <b>%s</b>." % (d(ya), a, d(F(k)), b, d(F(k)), b, ans))


def s3_escala():
    k = R.choice(["mapa", "plano", "inversa", "leer"])
    if k == "mapa":
        e = R.choice([100000, 200000, 500000, 1000000, 50000])
        c = R.randint(2, 15)
        real = c * e // 100000
        return M("En un mapa a escala 1 : %s, dos pueblos están a %d cm. ¿Cuántos kilómetros hay en la realidad?" % (num(e), c), "%s km" % num(real),
                 ["%s km" % num(c * e // 1000), "%s km" % num(real * 10), "%s km" % num(max(1, real // 10)) if real // 10 else "%s km" % num(real + 1), "%s km" % num(c + e // 100000)],
                 "%d cm × %s = %s cm = <b>%s km</b>." % (c, num(e), num(c * e), num(real)))
    if k == "plano":
        e = R.choice([50, 100, 200])
        c = R.randint(3, 20)
        real = F(c * e, 100)
        return M("En el plano de una casa (escala 1 : %d), el salón mide %d cm de largo. ¿Cuánto mide en la realidad?" % (e, c), "%s m" % d(real), ["%s m" % d(real * 10), "%s m" % d(real / 10), "%s m" % num(c * e), "%s m" % d(real + 1)],
                 "%d × %d = %s cm = <b>%s m</b>." % (c, e, num(c * e), d(real)))
    if k == "inversa":
        e = R.choice([100, 200, 500, 1000])
        m = R.randint(2, 30)
        c = F(m * 100, e)
        if c.denominator not in (1, 2, 5, 10):
            return None
        return M("Un campo de deporte mide %d m. ¿Cuántos centímetros medirá en un plano a escala 1 : %d?" % (m, e), "%s cm" % d(c), ["%s cm" % d(c * 10), "%s cm" % num(m * e), "%s cm" % d(c / 10), "%s cm" % d(c + 1)],
                 "%d m = %s cm; %s : %d = <b>%s cm</b>." % (m, num(m * 100), num(m * 100), e, d(c)))
    e = R.choice([100, 1000, 50000, 200000])
    return M("¿Qué significa la escala 1 : %s?" % num(e), "1 cm en el dibujo son %s cm en la realidad" % num(e), ["1 cm en la realidad son %s cm en el dibujo" % num(e), "1 cm en el dibujo es 1 cm en la realidad", "el dibujo es %s veces más grande" % num(e)],
             "<b>1 cm en el dibujo son %s cm en la realidad</b>." % num(e))


def s4_razon():
    k = R.choice(["razon", "proporcional", "receta"] if LV == 6 else ["razon", "receta"])
    if k == "razon":
        a, b = R.randint(2, 12), R.randint(2, 12)
        if a == b:
            return None
        return M("En una clase hay %d niñas y %d niños. ¿Cuál es la razón entre niñas y niños?" % (a * 2, b * 2), "%d a %d" % (a * 2, b * 2),
                 ["%d a %d" % (b * 2, a * 2), "%d a %d" % (a * 2, (a + b) * 2), "%d a %d" % (a + b, a)], "Niñas a niños: <b>%d a %d</b> (o %d : %d)." % (a * 2, b * 2, a * 2, b * 2))
    if k == "proporcional":
        q, a, w = R.choice([("¿Son proporcionales la edad y la altura de una persona?", "no", ["sí, directamente", "sí, siempre", "solo hasta los 10 años"]),
                            ("¿Son proporcionales el número de kilos de fruta y su precio (sin ofertas)?", "sí, directamente", ["no", "solo si son naranjas", "no se puede saber"]),
                            ("¿Son proporcionales el número de páginas de un libro y su precio?", "no", ["sí, directamente", "sí, siempre", "solo si es de cuentos"]),
                            ("¿Son proporcionales los litros de gasolina y los kilómetros que recorre un coche (a la misma velocidad)?", "sí, directamente", ["no", "solo en ciudad", "nunca"]),
                            ("En una oferta «3 por 2», ¿son proporcionales las unidades y el precio?", "no", ["sí, directamente", "siempre", "solo si compras 3"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    p = R.choice([2, 4, 6])
    n = R.choice([3, 6, 8, 9, 12])
    h = R.choice([100, 150, 200, 250])
    r = F(h * n, p)
    return M("Una receta para %d personas lleva %d g de harina. ¿Cuánta harina hace falta para %d personas?" % (p, h, n), "%s g" % d(r), ["%s g" % d(F(h + n - p)), "%s g" % num(h * n), "%s g" % d(r + h)],
             "Para 1 persona: %d : %d; para %d: %s g." % (h, p, n, d(r)))


def s5_problema():
    k = R.choice(["coche", "grifo", "salario", "fotocopias", "mapa"])
    if k == "coche":
        a, b = R.choice([(2, 5), (3, 4), (3, 5), (2, 7), (4, 6)])
        v = R.choice([60, 80, 90, 100, 120])
        return M("Un coche recorre %d km en %d horas, siempre a la misma velocidad. ¿Cuántos kilómetros recorre en %d horas?" % (v * a, a, b), "%d km" % (v * b), ["%d km" % (v * a + b - a), "%d km" % (v * a * b), "%d km" % (v * (b + 1))],
                 "En 1 hora: %d km; en %d horas: <b>%d km</b>." % (v, b, v * b))
    if k == "grifo":
        l = R.choice([6, 8, 10, 12, 15])
        a, b = R.sample([2, 3, 4, 5, 6, 10], 2)
        return M("Un grifo echa %d litros en %d minutos. ¿Cuántos litros echa en %d minutos?" % (l * a, a, b), "%d L" % (l * b), ["%d L" % (l * a + b - a), "%d L" % (l * a * b), "%d L" % (l * (b + 1))], "1 minuto: %d L; %d minutos: <b>%d L</b>." % (l, b, l * b))
    if k == "salario":
        h = R.choice([8, 10, 12, 15])
        a, b = R.sample([3, 4, 5, 6, 8, 20], 2)
        return M("Por %d horas de trabajo pagan %d €. ¿Cuánto pagan por %d horas?" % (a, h * a, b), "%d €" % (h * b), ["%d €" % (h * a + b - a), "%d €" % (h * a * b), "%d €" % (h * (b + 1))], "1 hora: %d €; %d horas: <b>%d €</b>." % (h, b, h * b))
    if k == "fotocopias":
        a, b = R.sample([10, 20, 25, 40, 50, 100], 2)
        c = R.choice([5, 10])
        return M("%d fotocopias cuestan %s €. ¿Cuánto cuestan %d fotocopias?" % (a, d(F(a * c, 100)), b), "%s €" % d(F(b * c, 100)), ["%s €" % d(F(a * c, 100) + b - a) if F(a * c, 100) + b - a > 0 else None, "%s €" % d(F(b * c, 10)), "%s €" % d(F(b * c, 1000))],
                 "1 fotocopia: %d céntimos; %d: <b>%s €</b>." % (c, b, d(F(b * c, 100))))
    e = R.choice([100000, 200000, 500000])
    km = R.randint(2, 20) * e // 100000
    return M("En un mapa a escala 1 : %s, ¿a cuántos centímetros están dos ciudades que en la realidad están a %d km?" % (num(e), km), "%d cm" % (km * 100000 // e), ["%s cm" % num(km * e), "%d cm" % (km * 1000 // e) if km * 1000 // e else "%d cm" % (km * 100000 // e + 1), "%d cm" % km],
             "%d km = %s cm; %s : %s = <b>%d cm</b>." % (km, num(km * 100000), num(km * 100000), num(e), km * 100000 // e))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40011 + lv * 1000)
    seen = set()
    sets = [
        ("Tablas de proporcionalidad", mix(R, seen, [(s1_tabla, 20)])),
        ("Reducción a la unidad", mix(R, seen, [(s2_regla, 20)])),
        ("Razón y proporción", mix(R, seen, [(s4_razon, 20)])),
        ("Escalas en planos y mapas", mix(R, seen, [(s3_escala, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dos magnitudes son <b>directamente proporcionales</b> si, al multiplicar una por un número, la otra queda multiplicada por el mismo número: 2 kg → 3 €, 4 kg → 6 €.",
         "Para resolver, <b>reduce a la unidad</b>: averigua cuánto vale 1 y multiplica.",
         "Una <b>escala</b> 1 : 100 000 significa que 1 cm en el mapa son 100 000 cm (1 km) en la realidad."],
        [("Si 3 kg cuestan 4,50 €, ¿cuánto cuestan 5 kg?", ["1 kg: 4,50 : 3 = 1,50 €", "5 kg: 1,50 × 5"], "7,50 €"),
         ("Mapa 1 : 200 000, 4 cm", ["4 × 200 000 = 800 000 cm", "800 000 cm = 8 km"], "8 km")],
        [["Sumar en vez de multiplicar", "Si 2 kg son 3 €, 4 kg no son 5 €: son 6 €."],
         ["Usar la escala al revés", "En 1 : 100, el dibujo es más pequeño que la realidad."],
         ["Creer que todo es proporcional", "La edad y la altura no son proporcionales."]])
    faq = [("¿Qué es la reducción a la unidad?", "Es calcular primero cuánto corresponde a una unidad (dividiendo) y después multiplicar por las unidades que nos piden."),
           ("¿Qué significa una escala 1 : 50 000?", "Que cada centímetro del mapa equivale a 50 000 cm en la realidad, es decir, a 500 metros.")]
    make_unit(R, "proporcionalidad", "N",
              "Proporcionalidad: magnitudes directamente proporcionales, tablas, razón, reducción a la unidad y regla de tres; escalas en planos y mapas; resolución de problemas",
              "Proporcionalidad y escalas", "Proporcionalidad",
              "Fichas de matemáticas de %d.º de Primaria: magnitudes proporcionales, tablas de proporcionalidad, reducción a la unidad, razón, escalas en planos y mapas y problemas. 100 ejercicios con soluciones." % lv,
              "Calcula cuánto vale 1", "Después multiplica.",
              body, faq, sets, 11, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
