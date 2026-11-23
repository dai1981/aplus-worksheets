# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Multiplicación (Sentido numérico)
Las tablas, multiplicar por una cifra y por dos o tres cifras en vertical, por 10, 100, 1000 y por números acabados en cero,
términos (factores y producto), propiedades conmutativa, asociativa y distributiva, problemas.
Errores: no desplazar el segundo producto parcial, olvidar la llevada, sumar en lugar de multiplicar.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, vertical, bank, Kids

R = random.Random(44006)
K = Kids(R)


def nocarry_mul(a, b):
    """error: multiplicar cada cifra sin llevar"""
    return int("".join(str(int(c) * b % 10) for c in str(a)))


def s1_tablas():
    a, b = R.randint(2, 9), R.randint(2, 10)
    k = R.choice(["prod", "falta"])
    if k == "prod":
        return mcq("Calcula: %d %s %d" % (a, POR, b), str(a * b), [str(a * b + a), str(a * b - a), str(a + b), str(a * (b + 2))], "%d %s %d = <b>%d</b>." % (a, POR, b, a * b))
    return mcq("¿Qué número falta? %d %s ___ = %d" % (a, POR, a * b), str(b), [str(b + 1), str(b - 1), str(a * b - a), str(b + 2)], "%d %s %d = %d: falta el <b>%d</b>." % (a, POR, b, a * b, b))


def s1_una():
    a = R.choice([R.randint(100, 999), R.randint(1000, 9999), R.randint(10000, 99999)])
    b = R.randint(3, 9)
    p = a * b
    if p > 999999 or nocarry_mul(a, b) == p:
        return None
    return mcq(vertical([str(a), str(b)], op=POR) + "Calcula: %s %s %d" % (num(a), POR, b), num(p), [num(nocarry_mul(a, b)), num(a * (b - 1)), num(p + 10), num(p - 100)],
               "Multiplicamos %d por cada cifra, desde las unidades, y sumamos las llevadas: <b>%s</b>." % (b, num(p)))


def s2_ceros():
    a = R.randint(2, 99) * R.choice([1, 1, 10])
    b = R.choice([10, 100, 1000, 20, 30, 40, 50, 200, 300, 500, 600])
    p = a * b
    if p > 999999:
        return None
    return mcq("Calcula mentalmente: %s %s %s" % (num(a), POR, num(b)), num(p), [num(p // 10), num(p * 10), num(a * (b // 10 ** (len(str(b)) - 1))), num(p // 100) if p % 100 == 0 else num(p + b)],
               "Multiplicamos sin los ceros y añadimos los ceros al final: <b>%s</b>." % num(p))


def s3_dos():
    a = R.randint(100, 999) if R.random() < 0.6 else R.randint(1000, 9999)
    b = R.randint(12, 99)
    p = a * b
    if p > 999999:
        return None
    t, u = divmod(b, 10)
    noshift = a * u + a * t
    return mcq(vertical([str(a), str(b)], op=POR) + "Calcula: %s %s %d" % (num(a), POR, b), num(p), [num(noshift), num(a * u + a * t * 100), num(p + a), num(p - 10)],
               "%s %s %d = %s y %s %s %d = %s (se coloca una columna a la izquierda); %s + %s = <b>%s</b>." % (num(a), POR, u, num(a * u), num(a), POR, t * 10, num(a * t * 10), num(a * u), num(a * t * 10), num(p)))


def s3_tres():
    a = R.randint(100, 999)
    b = R.randint(102, 999)
    p = a * b
    if p > 999999:
        return None
    return mcq("Calcula: %d %s %d" % (a, POR, b), num(p), [num(a * (b % 10) + a * (b // 10 % 10) * 10 + a * (b // 100)), num(p + a), num(p - 1000), num(p + 100)],
               "Hacemos tres productos parciales (por las unidades, por las decenas y por las centenas) y los sumamos: <b>%s</b>." % num(p))


def s4_prop():
    k = R.choice(["conm", "asoc", "dist", "dist2", "nombre"])
    if k == "conm":
        a, b = R.randint(12, 99), R.randint(3, 9)
        return mcq("Si %d %s %d = %d, ¿cuánto es %d %s %d?" % (a, POR, b, a * b, b, POR, a), str(a * b), [str(a * b + b), str(a + b), str(a * b - a), str(a * b * 10)],
                   "Propiedad conmutativa: el orden de los factores no cambia el producto. <b>%d</b>." % (a * b))
    if k == "asoc":
        a, b, c = R.randint(2, 9), R.choice([2, 5, 4, 25, 20]), R.choice([5, 2, 25, 4, 50])
        if b * c not in (10, 100, 1000):
            return None
        return mcq("Calcula de la forma más fácil: %d %s %d %s %d" % (a, POR, b, POR, c), num(a * b * c), [num(a * b + c), num(a + b * c), num(a * b * c * 10), num(a * b * c + 10)],
                   "Propiedad asociativa: %d %s (%d %s %d) = %d %s %d = <b>%s</b>." % (a, POR, b, POR, c, a, POR, b * c, num(a * b * c)))
    if k == "dist":
        a = R.randint(3, 9)
        b, c = R.randint(10, 90) // 10 * 10, R.randint(1, 9)
        return mcq("Completa: %d %s %d = %d %s %d + %d %s ___" % (a, POR, b + c, a, POR, b, a, POR), str(c), [str(b), str(b + c), str(a), str(c + 1), str(a * c)],
                   "Propiedad distributiva: %d %s (%d + %d) = %d %s %d + %d %s %d." % (a, POR, b, c, a, POR, b, a, POR, c)) if b > 0 else None
    if k == "dist2":
        a = R.randint(3, 9)
        b = R.randint(11, 99)
        if b % 10 == 0:
            return None
        t, u = b // 10 * 10, b % 10
        return mcq("Calcula usando la propiedad distributiva: %d %s %d" % (a, POR, b), str(a * b), [str(a * t + u), str(a * t), str(a * b + a), str(a * u + t)],
                   "%d %s %d = %d %s %d + %d %s %d = %d + %d = <b>%d</b>." % (a, POR, b, a, POR, t, a, POR, u, a * t, a * u, a * b))
    a, b = R.randint(12, 99), R.randint(3, 9)
    w = R.choice(["factores", "producto"])
    return mcq("En %d %s %d = %d, ¿cómo se llama%s %s?" % (a, POR, b, a * b, "n" if w == "factores" else "", "%d y %d" % (a, b) if w == "factores" else str(a * b)),
               w, ["producto" if w == "factores" else "factores", "sumandos", "cociente"], "%s %s %s = producto: <b>%s</b>." % ("Factor", POR, "factor", w))


def s5_problema():
    k = R.choice(["cajas", "bus", "entradas", "huevos", "km", "sillas", "paginas", "fila"])
    p, g = K.next()
    if k == "cajas":
        a, b = R.randint(12, 48), R.randint(24, 96)
        return mcq("Un camión lleva %d cajas. Cada caja tiene %d botellas. ¿Cuántas botellas lleva?" % (a, b), num(a * b), [num(a + b), num(a * b - b), num(a * (b % 10) + a * (b // 10)), num(a * b + 10)],
                   "%d %s %d = <b>%s</b> botellas." % (a, POR, b, num(a * b)))
    if k == "bus":
        a, b = R.randint(12, 35), R.choice([45, 52, 55, 60, 48])
        return mcq("Para una excursión se alquilan %d autobuses de %d plazas. ¿Cuántas plazas hay en total?" % (a, b), num(a * b), [num(a + b), num(a * b + a), num(a * b - b), num(a * b * 10)],
                   "%d %s %d = <b>%s</b> plazas." % (a, POR, b, num(a * b)))
    if k == "entradas":
        a, pr = R.randint(120, 950), R.choice([6, 8, 12, 15, 9, 7])
        return mcq("Un cine vende %d entradas a %d € cada una. ¿Cuánto dinero recauda?" % (a, pr), "%s €" % num(a * pr), ["%s €" % num(a + pr), "%s €" % num(a * pr - pr), "%s €" % num(a * pr + 100), "%s €" % num(a * pr // 10)],
                   "%d %s %d = <b>%s €</b>." % (a, POR, pr, num(a * pr)))
    if k == "huevos":
        a = R.randint(25, 99)
        return mcq("Una granja llena %d docenas de huevos. ¿Cuántos huevos son?" % a, num(a * 12), [num(a + 12), num(a * 10), num(a * 12 + 12), num(a * 6)],
                   "Una docena son 12: %d %s 12 = <b>%s</b>." % (a, POR, num(a * 12)))
    if k == "km":
        a, d = R.randint(120, 480), R.choice([5, 6, 7, 12, 14, 20, 22])
        return mcq("Un tren recorre %d km cada día. ¿Cuántos kilómetros recorre en %d días?" % (a, d), "%s km" % num(a * d), ["%s km" % num(a + d), "%s km" % num(a * d - a), "%s km" % num(a * d + 10), "%s km" % num(a * (d - 1) + 10)],
                   "%d %s %d = <b>%s km</b>." % (a, POR, d, num(a * d)))
    if k == "sillas":
        f, c = R.randint(15, 45), R.randint(12, 30)
        return mcq("En el salón de actos hay %d filas de %d sillas. ¿Cuántas sillas hay?" % (f, c), num(f * c), [num(f + c), num(f * c - c), num(f * c + f), num((f + c) * 2)],
                   "%d %s %d = <b>%s</b> sillas." % (f, POR, c, num(f * c)))
    if k == "paginas":
        a, b = R.randint(5, 9), R.randint(120, 350)
        return mcq("%s lee una colección de %d libros. Cada libro tiene %d páginas. ¿Cuántas páginas lee?" % (p, a, b), num(a * b), [num(a + b), num(a * b - a), num(nocarry_mul(b, a)) if nocarry_mul(b, a) != a * b else num(a * b + 100), num(a * b + 10)],
                   "%d %s %d = <b>%s</b>." % (b, POR, a, num(a * b)))
    pr, n = R.randint(12, 45), R.randint(3, 8)
    q = R.randint(2, 5)
    return mcq("%s compra %d camisetas de %d € y %d gorras de %d €. ¿Cuánto paga en total?" % (p, n, pr, q, pr // 3 + 2), "%d €" % (n * pr + q * (pr // 3 + 2)),
               ["%d €" % (n * pr + pr // 3 + 2), "%d €" % (pr + pr // 3 + 2), "%d €" % (n * pr), "%d €" % ((n + q) * pr)],
               "%d %s %d + %d %s %d = %d + %d = <b>%d €</b>." % (n, POR, pr, q, POR, pr // 3 + 2, n * pr, q * (pr // 3 + 2), n * pr + q * (pr // 3 + 2)))


def main():
    seen = set()
    sets = [
        ("Tablas y multiplicar por una cifra", mix(R, seen, [(s1_tablas, 6), (s1_una, 14)])),
        ("Multiplicar por 10, 100, 1000 y números con ceros", mix(R, seen, [(s2_ceros, 20)])),
        ("Multiplicar por dos y tres cifras", mix(R, seen, [(s3_dos, 15), (s3_tres, 5)])),
        ("Propiedades de la multiplicación", mix(R, seen, [(s4_prop, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Multiplicar es sumar varias veces el mismo número: 4 × 125 = 125 + 125 + 125 + 125. Los números que se multiplican son los <b>factores</b> y el resultado es el <b>producto</b>.",
         "Para multiplicar por un número de dos cifras, multiplica primero por las unidades y después por las decenas. El segundo producto se escribe <b>una columna a la izquierda</b>. Luego suma.",
         "Para multiplicar por 10, 100 o 1000, añade uno, dos o tres ceros."],
        [("346 × 27", ["346 × 7 = 2422", "346 × 20 = 6920", "2422 + 6920"], "9342"),
         ("8 × 25 × 4", ["Asociativa: 25 × 4 = 100", "8 × 100"], "800")],
        [["No desplazar el segundo producto", "346 × 2 decenas = 692 decenas = 6920."],
         ["Olvidar la llevada", "Escribe la llevada encima y súmala después de multiplicar."],
         ["Sumar en lugar de multiplicar", "«Cada caja tiene…» y «¿cuántos en total?» suele ser una multiplicación."]],
        vertical(["346", "27"], op=POR, result="9342"))
    faq = [("¿Cómo se multiplica por dos cifras?", "Se multiplica el primer factor por las unidades y después por las decenas, escribiendo este segundo producto una columna más a la izquierda. Al final se suman los dos productos parciales."),
           ("¿Qué es la propiedad distributiva?", "Multiplicar un número por una suma es lo mismo que multiplicarlo por cada sumando y sumar: 6 × 23 = 6 × 20 + 6 × 3.")]
    make_unit(R, "multiplicacion", "N",
              "Estrategias y algoritmo de la multiplicación de números naturales por números de una, dos y tres cifras; propiedades de la multiplicación; resolución de problemas",
              "Multiplicación por una, dos y tres cifras", "Multiplicación",
              "Fichas de matemáticas de 4.º de Primaria: tablas, multiplicar por una, dos y tres cifras, por 10, 100 y 1000, propiedades de la multiplicación y problemas. 100 ejercicios con soluciones.",
              "Desplaza una columna cada producto", "Primero unidades, luego decenas; después suma.",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
