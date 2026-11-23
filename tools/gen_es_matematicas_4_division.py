# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: División (Sentido numérico)
Términos (dividendo, divisor, cociente y resto), divisiones exactas y enteras, dividir entre una cifra y entre dos cifras,
prueba de la división (D = d × c + r), dividir entre 10, 100 y 1000, problemas con el resto.
Errores: un resto mayor o igual que el divisor, olvidar el 0 del cociente (618 : 3 = 206), no tener en cuenta el resto en los problemas.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, DIV, bank, Kids

R = random.Random(44007)
K = Kids(R)


def q_r(D, d):
    return divmod(D, d)


def drop_zero(c):
    """error: olvidar el 0 del cociente"""
    s = str(c)
    if "0" in s[1:]:
        return int(s[0] + s[1:].replace("0", "", 1))
    return None


def s1_una():
    d = R.randint(2, 9)
    exact = R.random() < 0.5
    c = R.randint(12, 999)
    if R.random() < 0.3:
        c = int(str(c)[0] + "0" + str(c)[1:]) if c < 100 else c // 10 * 10 + 0
    r = 0 if exact else R.randint(1, d - 1)
    D = c * d + r
    if D > 9999:
        return None
    ans = "%s" % num(c) if r == 0 else "%s y resto %d" % (num(c), r)
    alts = []
    dz = drop_zero(c)
    if dz:
        alts.append(num(dz) if r == 0 else "%s y resto %d" % (num(dz), r))
    if r == 0:
        alts += [num(c + 1), num(c - 1), num(c * 10)]
    else:
        alts += ["%s y resto %d" % (num(c + 1), r), "%s y resto %d" % (num(c - 1), r + d), "%s y resto %d" % (num(c), r + 1) if r + 1 < d else "%s y resto %d" % (num(c), r - 1) if r > 1 else None,
                 "%s y resto %d" % (num(c * 10), r)]
    return mcq("Calcula: %s %s %d" % (num(D), DIV, d), ans, alts,
               "%s %s %d = %s%s. Prueba: %d %s %s%s = %s." % (num(D), DIV, d, num(c), "" if r == 0 else " y resto %d" % r, d, POR, num(c), "" if r == 0 else " + %d" % r, num(D)))


def s2_dos():
    d = R.randint(12, 49)
    c = R.randint(11, 99) if R.random() < 0.6 else R.randint(101, 299)
    r = R.randint(0, d - 1) if R.random() < 0.6 else 0
    D = c * d + r
    ans = num(c) if r == 0 else "%s y resto %d" % (num(c), r)
    alts = [num(c + 1) if r == 0 else "%s y resto %d" % (num(c + 1), r), "%s y resto %d" % (num(c - 1), r + d) if r + d < 10 ** 4 else None,
            num(c - 1) if r == 0 else "%s y resto %d" % (num(c - 1), r), num(c * 10) if r == 0 else "%s y resto %d" % (num(c), (r + 1) % d)]
    return mcq("Calcula: %s %s %d" % (num(D), DIV, d), ans, alts,
               "%d %s %s = %s%s; el resto es menor que %d: <b>%s</b>." % (d, POR, num(c), num(c * d), "" if r == 0 else ", y %s + %d = %s" % (num(c * d), r, num(D)), d, ans))


def s3_terminos():
    D = R.randint(100, 9999)
    d = R.randint(3, 25)
    c, r = q_r(D, d)
    k = R.choice(["cociente", "resto", "prueba_D", "resto_max", "exacta"])
    if k == "cociente":
        return mcq("En la división %s %s %d, ¿cuál es el cociente?" % (num(D), DIV, d), num(c), [str(r) if r != c else num(c + 1), num(d), num(D), num(c + 1)],
                   "%s %s %d = %s y resto %d. El cociente es <b>%s</b>." % (num(D), DIV, d, num(c), r, num(c)))
    if k == "resto":
        return mcq("En la división %s %s %d, ¿cuál es el resto?" % (num(D), DIV, d), str(r), [str(r + 1) if r + 1 < d else str(r - 1), str(d - r) if d - r != r else str(r + 2), num(c), str(d)],
                   "%d %s %s = %s; %s − %s = <b>%d</b>." % (d, POR, num(c), num(c * d), num(D), num(c * d), r))
    if k == "prueba_D":
        return mcq("En una división el divisor es %d, el cociente %s y el resto %d. ¿Cuál es el dividendo?" % (d, num(c), r), num(D), [num(c * d), num(c * d - r) if r else num(c * d + d), num(c + d + r), num((c + r) * d)],
                   "Dividendo = divisor %s cociente + resto: %d %s %s + %d = <b>%s</b>." % (POR, d, POR, num(c), r, num(D)))
    if k == "resto_max":
        return mcq("Si divides entre %d, ¿cuál es el resto más grande que puede quedar?" % d, str(d - 1), [str(d), str(d + 1), str(d // 2), "no hay límite"],
                   "El resto siempre es menor que el divisor: el mayor es <b>%d</b>." % (d - 1))
    d = R.randint(3, 9)
    c = R.randint(20, 400)
    ex = R.random() < 0.5
    D = c * d + (0 if ex else R.randint(1, d - 1))
    return mcq("¿La división %s %s %d es exacta o entera?" % (num(D), DIV, d), "exacta" if ex else "entera", ["entera" if ex else "exacta", "ni exacta ni entera", "no se puede hacer"],
               "%s %s %d = %s%s: <b>%s</b>." % (num(D), DIV, d, num(D // d), "" if ex else " y resto %d" % (D % d), "exacta (resto 0)" if ex else "entera (el resto no es 0)"))


def s4_ceros():
    k = R.choice([10, 100, 1000, "20", "50", "30", "40"])
    if isinstance(k, int):
        c = R.randint(2, 999)
        D = c * k
        if D > 999999:
            return None
        return mcq("Calcula mentalmente: %s %s %s" % (num(D), DIV, num(k)), num(c), [num(c * 10), num(c // 10) if c >= 10 else num(c + 10), num(D - k), num(c * 100)],
                   "Dividir entre %s es quitar %s cero%s: <b>%s</b>." % (num(k), {10: "un", 100: "dos", 1000: "tres"}[k], "" if k == 10 else "s", num(c)))
    d = int(k)
    c = R.randint(2, 90)
    D = c * d
    return mcq("Calcula mentalmente: %s %s %d" % (num(D), DIV, d), num(c), [num(c * 10), num(D // (d // 10)), num(c + 1), num(c // 10 if c >= 10 else c + 10)],
               "%s %s %d = %s %s %d = <b>%s</b> (quitamos un cero a cada número)." % (num(D), DIV, d, num(D // 10), DIV, d // 10, num(c)))


def s5_problema():
    k = R.choice(["reparte", "autobus", "cajas", "paga", "semanas", "equipos", "sobran", "precio"])
    p, g = K.next()
    if k == "reparte":
        d = R.randint(3, 9)
        c = R.randint(25, 250)
        D = c * d
        return mcq("Un club reparte %s balones entre %d colegios a partes iguales. ¿Cuántos balones recibe cada colegio?" % (num(D), d), num(c), [num(D - d), num(c + 1), num(D * d), num(c - 1)],
                   "%s %s %d = <b>%s</b>." % (num(D), DIV, d, num(c)))
    if k == "autobus":
        pl = R.choice([45, 50, 55, 60])
        n = R.randint(4, 12) * pl + R.randint(1, pl - 1)
        c = n // pl
        return mcq("Al viaje de fin de curso van %d personas. Cada autobús tiene %d plazas. ¿Cuántos autobuses hacen falta como mínimo?" % (n, pl), str(c + 1), [str(c), str(c + 2), str(n % pl), str(c - 1)],
                   "%d %s %d = %d y resto %d. Las %d personas que sobran también necesitan autobús: <b>%d</b>." % (n, DIV, pl, c, n % pl, n % pl, c + 1))
    if k == "cajas":
        d = R.choice([6, 8, 12, 24])
        n = R.randint(20, 90) * d + R.randint(1, d - 1)
        c = n // d
        return mcq("Una fábrica tiene %s yogures y los mete en paquetes de %d. ¿Cuántos paquetes completos puede hacer?" % (num(n), d), num(c), [num(c + 1), num(n % d), num(c - 1), num(n - d)],
                   "%s %s %d = %s y resto %d. Solo cuentan los paquetes completos: <b>%s</b>." % (num(n), DIV, d, num(c), n % d, num(c)))
    if k == "paga":
        m = R.choice([3, 4, 5, 6, 10, 12])
        c = R.randint(8, 60)
        return mcq("Unos patines cuestan %d €. %s los paga en %d plazos iguales. ¿Cuánto paga en cada plazo?" % (c * m, p, m), "%d €" % c, ["%d €" % (c * m - m), "%d €" % (c + m), "%d €" % (c + 1), "%d €" % (c * 2)],
                   "%d %s %d = <b>%d €</b>." % (c * m, DIV, m, c))
    if k == "semanas":
        d = R.choice([7, 30, 24, 60])
        c = R.randint(3, 40)
        unit = {7: ("días", "semanas"), 30: ("días", "meses de 30 días"), 24: ("horas", "días"), 60: ("minutos", "horas")}[d]
        return mcq("¿Cuántas %s son %s %s?" % (unit[1], num(c * d), unit[0]), str(c), [str(c * 10), str(c + d), str(c + 1), str(c * d - d)],
                   "%s %s %d = <b>%d</b>." % (num(c * d), DIV, d, c))
    if k == "equipos":
        e = R.choice([5, 6, 7, 11])
        n = R.randint(5, 30) * e + R.randint(1, e - 1)
        c, r = divmod(n, e)
        return mcq("En un torneo hay %d jugadores. Se hacen equipos de %d. ¿Cuántos jugadores se quedan sin equipo?" % (n, e), str(r), [str(c), str(e - r) if e - r != r else str(r + 1), str(r + e), "0"],
                   "%d %s %d = %d y resto <b>%d</b>." % (n, DIV, e, c, r))
    if k == "sobran":
        d = R.randint(3, 9)
        n = R.randint(30, 300) * d + R.randint(1, d - 1)
        c, r = divmod(n, d)
        return mcq("%s reparte %d cromos entre %d amigos, a partes iguales y dando el máximo posible. ¿Cuántos cromos le sobran?" % (p, n, d), str(r), [str(c), str(d - r) if d - r != r else str(r + 1), "0", str(r + d)],
                   "%d %s %d = %d y resto <b>%d</b>." % (n, DIV, d, c, r))
    t = R.randint(4, 12)
    c = R.randint(15, 95)
    return mcq("En una papelería, %d cajas iguales cuestan %d €. ¿Cuánto cuesta cada caja?" % (t, t * c), "%d €" % c, ["%d €" % (t * c - t), "%d €" % (c + t), "%d €" % (c + 1), "%d €" % (c * 10)],
               "%d %s %d = <b>%d €</b>." % (t * c, DIV, t, c))


def main():
    seen = set()
    sets = [
        ("Dividir entre una cifra", mix(R, seen, [(s1_una, 20)])),
        ("Términos y prueba de la división", mix(R, seen, [(s3_terminos, 20)])),
        ("Dividir entre dos cifras", mix(R, seen, [(s2_dos, 20)])),
        ("Dividir entre 10, 100, 1000 y números con ceros", mix(R, seen, [(s4_ceros, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dividir es repartir en partes iguales. En 47 : 5 = 9 y resto 2, 47 es el <b>dividendo</b>, 5 el <b>divisor</b>, 9 el <b>cociente</b> y 2 el <b>resto</b>.",
         "Si el resto es 0, la división es <b>exacta</b>; si no, es <b>entera</b>. El resto siempre es <b>menor que el divisor</b>.",
         "<b>Prueba de la división</b>: divisor × cociente + resto = dividendo.",
         "Si al bajar una cifra no cabe el divisor, escribe un <b>0</b> en el cociente."],
        [("618 : 3", ["6 : 3 = 2", "1 : 3 no cabe → 0 en el cociente", "18 : 3 = 6"], "206"),
         ("947 : 23", ["94 : 23 = 4 (4 × 23 = 92, quedan 2)", "27 : 23 = 1 y quedan 4", "Prueba: 23 × 41 + 4 = 947"], "41 y resto 4")],
        [["Resto mayor que el divisor", "Si el resto es mayor o igual que el divisor, el cociente puede ser mayor."],
         ["Olvidar el 0 del cociente", "618 : 3 = 206, no 26."],
         ["Ignorar el resto en el problema", "Si sobran personas, hace falta un autobús más."]])
    faq = [("¿Cómo se hace la prueba de la división?", "Se multiplica el divisor por el cociente y se suma el resto. Si da el dividendo, la división está bien: 23 × 41 + 4 = 947."),
           ("¿Qué diferencia hay entre una división exacta y una entera?", "En la división exacta el resto es 0; en la división entera queda un resto distinto de 0, pero siempre menor que el divisor.")]
    make_unit(R, "division", "N",
              "Estrategias y algoritmo de la división de números naturales entre números de una y dos cifras; división exacta y entera; relación entre los términos de la división; resolución de problemas",
              "División entre una y dos cifras", "División",
              "Fichas de matemáticas de 4.º de Primaria: dividir entre una y dos cifras, términos de la división, prueba de la división, dividir entre 10, 100 y 1000 y problemas con resto. 100 ejercicios con soluciones.",
              "El resto es menor que el divisor", "Prueba: divisor × cociente + resto = dividendo.",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
