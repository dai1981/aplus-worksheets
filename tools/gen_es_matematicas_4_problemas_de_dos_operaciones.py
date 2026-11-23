# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Problemas de dos operaciones (Sentido numérico)
Leer el problema, elegir las operaciones y el orden, operaciones combinadas con paréntesis, problemas de suma y resta,
de multiplicación y suma o resta, de multiplicación y división, y de dinero.
Errores: hacer solo una operación, operar sin respetar el paréntesis, elegir la operación por las palabras sin entender.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, DIV, eur, Kids, ao

R = random.Random(44009)
K = Kids(R)


def s1_parentesis():
    a, b, c = R.randint(10, 90), R.randint(2, 30), R.randint(2, 9)
    k = R.choice(["(a+b)xc", "ax(b+c)", "(a-b)xc", "a-(b+c)", "(a+b):c", "a+bxc", "a-bxc"])
    if k == "(a+b)xc":
        r, txt, w = (a + b) * c, "(%d + %d) %s %d" % (a, b, POR, c), a + b * c
    elif k == "ax(b+c)":
        a = R.randint(2, 9)
        r, txt, w = a * (b + c), "%d %s (%d + %d)" % (a, POR, b, c), a * b + c
    elif k == "(a-b)xc":
        if a <= b:
            return None
        r, txt, w = (a - b) * c, "(%d − %d) %s %d" % (a, b, POR, c), a - b * c
    elif k == "a-(b+c)":
        if a <= b + c:
            return None
        r, txt, w = a - (b + c), "%d − (%d + %d)" % (a, b, c), a - b + c
    elif k == "(a+b):c":
        s = a + b
        if s % c:
            return None
        r, txt, w = s // c, "(%d + %d) %s %d" % (a, b, DIV, c), a + b // c if b % c == 0 else s // c + 1
    elif k == "a+bxc":
        r, txt, w = a + b * c, "%d + %d %s %d" % (a, b, POR, c), (a + b) * c
    else:
        if a <= b * c:
            return None
        r, txt, w = a - b * c, "%d − %d %s %d" % (a, b, POR, c), (a - b) * c
    if w == r or w < 0:
        w = r + 10
    return mcq("Calcula: %s" % txt, num(r), [num(w), num(r + c), num(r - 1) if r > 1 else num(r + 2), num(r + 10)],
               "%s <b>%s</b>." % ("Primero el paréntesis." if "(" in txt else "Primero la multiplicación y después la suma o la resta:", num(r)))


def s2_suma_resta():
    p, g = K.next()
    k = R.choice(["cromos", "tren", "biblio", "puntos", "litros"])
    if k == "cromos":
        a, b, c = R.randint(120, 400), R.randint(30, 150), R.randint(20, 100)
        return mcq("%s tenía %d cromos. Le regalan %d y después da %d a su primo. ¿Cuántos cromos tiene ahora?" % (p, a, b, c), str(a + b - c), [str(a + b + c), str(a + b), str(a - b - c), str(a - b + c)],
                   "%d + %d = %d; %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b - c))
    if k == "tren":
        a, b, c = R.randint(200, 500), R.randint(50, 150), R.randint(40, 120)
        return mcq("En un tren van %d pasajeros. En una estación bajan %d y suben %d. ¿Cuántos pasajeros van ahora?" % (a, b, c), str(a - b + c), [str(a - b - c), str(a + b + c), str(a + b - c), str(a - b)],
                   "%d − %d = %d; %d + %d = <b>%d</b>." % (a, b, a - b, a - b, c, a - b + c))
    if k == "biblio":
        a, b = R.randint(1200, 4000), R.randint(200, 900)
        t = 2 * a + b
        return mcq("Una biblioteca tiene %s libros de cuentos y %d más de cómics que de cuentos. ¿Cuántos libros tiene en total entre cuentos y cómics?" % (num(a), b), num(t), [num(a + b), num(a + a - b), num(t - a), num(t + b)],
                   "Cómics: %s + %d = %s. Total: %s + %s = <b>%s</b>." % (num(a), b, num(a + b), num(a), num(a + b), num(t)))
    if k == "puntos":
        a = R.randint(60, 99)
        b = R.randint(5, a - 30)
        t = 2 * a - b
        return mcq("En un partido de baloncesto, un equipo hizo %d puntos y el otro %d puntos menos. ¿Cuántos puntos se marcaron en el partido?" % (a, b), str(t), [str(a - b), str(2 * a + b), str(a + b), str(t + 10)],
                   "El otro equipo: %d − %d = %d. Total: %d + %d = <b>%d</b>." % (a, b, a - b, a, a - b, t))
    a = R.randint(500, 900)
    b, c = R.randint(100, 250), R.randint(100, 250)
    return mcq("Un depósito tenía %d litros de agua. Por la mañana se gastan %d litros y por la tarde %d. ¿Cuántos litros quedan?" % (a, b, c), "%d L" % (a - b - c), ["%d L" % (a - b), "%d L" % (a - b + c), "%d L" % (b + c), "%d L" % (a + b + c)],
               "%d + %d = %d litros gastados; %d − %d = <b>%d L</b>." % (b, c, b + c, a, b + c, a - b - c))


def s3_mult():
    p, g = K.next()
    k = R.choice(["compra", "cajas", "ahorro", "entradas", "sobran", "flores"])
    if k == "compra":
        n, pr, m = R.randint(2, 6), R.randint(3, 12), R.choice([20, 50, 50, 100])
        if n * pr >= m:
            return None
        return mcq("%s compra %d libretas de %d € cada una y paga con un billete de %d €. ¿Cuánto le devuelven?" % (p, n, pr, m), "%d €" % (m - n * pr), ["%d €" % (n * pr), "%d €" % (m - pr), "%d €" % (m - n - pr), "%d €" % (m + n * pr)],
                   "%d %s %d = %d €; %d − %d = <b>%d €</b>." % (n, POR, pr, n * pr, m, n * pr, m - n * pr))
    if k == "cajas":
        c, u, s = R.randint(12, 40), R.choice([6, 12, 24]), R.randint(5, 20)
        return mcq("Una tienda recibe %d cajas de %d botellas. Ya ha vendido %d botellas. ¿Cuántas le quedan?" % (c, u, s), str(c * u - s), [str(c * u), str(c * u + s), str(c * (u - s)) if u > s else str(c + u - s), str((c - s) * u) if c > s else str(c * u - u)],
                   "%d %s %d = %d; %d − %d = <b>%d</b>." % (c, POR, u, c * u, c * u, s, c * u - s))
    if k == "ahorro":
        w, e, t = R.randint(3, 12), R.randint(5, 20), R.randint(10, 60)
        return mcq("%s tiene %d € y ahorra %d € cada semana. ¿Cuánto dinero tendrá dentro de %d semanas?" % (p, t, e, w), "%d €" % (t + e * w), ["%d €" % (e * w), "%d €" % ((t + e) * w), "%d €" % (t + e + w), "%d €" % (t * w + e)],
                   "%d %s %d = %d €; %d + %d = <b>%d €</b>." % (e, POR, w, e * w, t, e * w, t + e * w))
    if k == "entradas":
        a, n, kp, m = R.randint(8, 15), R.randint(2, 4), R.randint(4, 9), R.randint(1, 4)
        return mcq("En el teatro, la entrada de adulto cuesta %d € y la de niño %d €. ¿Cuánto pagan %d adultos y %d niños?" % (a, kp, n, m), "%d €" % (a * n + kp * m), ["%d €" % (a + kp), "%d €" % ((a + kp) * (n + m)), "%d €" % (a * n), "%d €" % (a * m + kp * n) if a * m + kp * n != a * n + kp * m else "%d €" % (a * n + kp)],
                   "%d %s %d + %d %s %d = %d + %d = <b>%d €</b>." % (n, POR, a, m, POR, kp, a * n, kp * m, a * n + kp * m))
    if k == "sobran":
        n, g_, x = R.randint(3, 8), R.randint(4, 9), R.randint(1, 6)
        t = n * g_ + x
        return mcq("En una clase hay %d alumnos. Se hacen %d grupos de %d alumnos. ¿Cuántos alumnos quedan sin grupo?" % (t, n, g_), str(x), [str(n * g_), str(t - n), str(t - g_), str(x + 1)],
                   "%d %s %d = %d; %d − %d = <b>%d</b>." % (n, POR, g_, n * g_, t, n * g_, x))
    r, f = R.randint(3, 8), R.randint(4, 9)
    m = R.randint(2, 5)
    return mcq("En un jardín hay %d filas de %d rosas y %d filas de %d claveles. ¿Cuántas flores hay?" % (r, f, m, f + 2), str(r * f + m * (f + 2)), [str(r * f), str((r + m) * f), str(r + f + m + f + 2), str(r * f + m)],
               "%d %s %d + %d %s %d = %d + %d = <b>%d</b>." % (r, POR, f, m, POR, f + 2, r * f, m * (f + 2), r * f + m * (f + 2)))


def s4_div():
    p, g = K.next()
    k = R.choice(["reparte", "precio", "km", "sobres", "equipo"])
    if k == "reparte":
        a, b, n = R.randint(20, 60), R.randint(20, 60), R.choice([3, 4, 5, 6])
        t = a + b
        if t % n:
            return None
        return mcq("%s tiene %d caramelos de fresa y %d de limón. Los reparte a partes iguales entre %d amigos. ¿Cuántos recibe cada uno?" % (p, a, b, n), str(t // n), [str(t), str(a // n + b) if a % n == 0 else str(t // n + 1), str(t - n), str(t * n)],
                   "%d + %d = %d; %d %s %d = <b>%d</b>." % (a, b, t, t, DIV, n, t // n))
    if k == "precio":
        n, c = R.randint(3, 8), R.randint(5, 15)
        tot = n * c
        q = R.randint(2, 9)
        return mcq("%d bolígrafos cuestan %d €. ¿Cuánto cuestan %d bolígrafos?" % (n, tot, q), "%d €" % (c * q), ["%d €" % (tot + q), "%d €" % (tot * q), "%d €" % c, "%d €" % (tot - q)],
                   "Un bolígrafo: %d %s %d = %d €. %d bolígrafos: %d %s %d = <b>%d €</b>." % (tot, DIV, n, c, q, c, POR, q, c * q)) if c * q != tot + q else None
    if k == "km":
        d, h = R.randint(2, 6), R.randint(60, 120)
        return mcq("Un tren recorre %d km en %d horas, siempre a la misma velocidad. ¿Cuántos kilómetros recorre en %d horas?" % (h * d, d, d + 2), "%d km" % (h * (d + 2)), ["%d km" % (h * d + 2), "%d km" % (h * d * (d + 2)), "%d km" % h, "%d km" % (h * d + h)],
                   "En 1 hora: %d %s %d = %d km. En %d horas: %d %s %d = <b>%d km</b>." % (h * d, DIV, d, h, d + 2, h, POR, d + 2, h * (d + 2)))
    if k == "sobres":
        s, c = R.randint(4, 9), R.randint(5, 10)
        n = R.choice([2, 3, 4, 5])
        t = s * c
        if t % n:
            return None
        return mcq("%s compra %d sobres de %d cromos y los reparte entre %d amigos a partes iguales. ¿Cuántos cromos recibe cada uno?" % (p, s, c, n), str(t // n), [str(t), str(s * n), str(c // n) if c % n == 0 else str(t // n + 1), str(t - n)],
                   "%d %s %d = %d; %d %s %d = <b>%d</b>." % (s, POR, c, t, t, DIV, n, t // n))
    pr, n = R.randint(4, 9), R.randint(5, 12)
    tot = pr * n * 11
    return mcq("Un equipo de fútbol tiene 11 jugadores. Cada jugador paga %d € al mes. ¿Cuánto pagan entre todos en %d meses?" % (pr, n), "%d €" % tot, ["%d €" % (pr * 11), "%d €" % (pr * n), "%d €" % (pr + n + 11), "%d €" % (tot + pr)],
               "11 %s %d = %d € al mes; %d %s %d = <b>%d €</b>." % (POR, pr, 11 * pr, 11 * pr, POR, n, tot))


def s5_operacion():
    p, g = K.next()
    a, b, c = R.randint(3, 9), R.randint(10, 40), R.randint(5, 50)
    k = R.choice(["libros", "manzanas", "dinero", "km", "fotos"])
    if k == "libros":
        q = "%s tiene %d estanterías con %d libros cada una y compra %d libros más. ¿Qué operación da el total de libros?" % (p, a, b, c)
        ok = "%d %s %d + %d" % (a, POR, b, c)
        ws = ["%d + %d + %d" % (a, b, c), "%d %s (%d + %d)" % (a, POR, b, c), "%d %s %d − %d" % (a, POR, b, c)]
    elif k == "manzanas":
        q = "En una frutería hay %d cajas de %d manzanas. Se estropean %d manzanas. ¿Qué operación da las manzanas buenas?" % (a, b, c)
        ok = "%d %s %d − %d" % (a, POR, b, c)
        ws = ["%d %s (%d − %d)" % (a, POR, b, c) if b > c else "%d + %d − %d" % (a, b, c), "%d %s %d + %d" % (a, POR, b, c), "%d − %d %s %d" % (c, a, POR, b)]
    elif k == "dinero":
        q = "%s tenía %d €. Gastó %d € en un libro y %d € en un cuaderno. ¿Qué operación da el dinero que le queda?" % (p, b + c + 50, b, a)
        ok = "%d − (%d + %d)" % (b + c + 50, b, a)
        ws = ["%d − %d + %d" % (b + c + 50, b, a), "%d + %d + %d" % (b + c + 50, b, a), "(%d − %d) %s %d" % (b + c + 50, b, POR, a)]
    elif k == "km":
        q = "Una familia hace %d km por la mañana y %d km por la tarde, durante %d días. ¿Qué operación da los kilómetros recorridos?" % (b * 10, c * 2, a)
        ok = "(%d + %d) %s %d" % (b * 10, c * 2, POR, a)
        ws = ["%d + %d %s %d" % (b * 10, c * 2, POR, a), "%d + %d + %d" % (b * 10, c * 2, a), "(%d − %d) %s %d" % (b * 10, c * 2, POR, a)]
    else:
        q = "%s hace %d fotos el sábado y %d el domingo, y las reparte en %d álbumes iguales. ¿Qué operación da las fotos de cada álbum?" % (p, b * a, c * a, a)
        ok = "(%d + %d) %s %d" % (b * a, c * a, DIV, a)
        ws = ["%d + %d %s %d" % (b * a, c * a, DIV, a), "(%d + %d) %s %d" % (b * a, c * a, POR, a), "%d − %d %s %d" % (b * a, c * a, DIV, a)]
    return mcq(q, ok, ws, "La operación correcta es <b>%s</b>." % ok)


def main():
    seen = set()
    sets = [
        ("Operaciones combinadas", mix(R, seen, [(s1_parentesis, 20)])),
        ("¿Qué operaciones hay que hacer?", mix(R, seen, [(s5_operacion, 20)])),
        ("Problemas de suma y resta", mix(R, seen, [(s2_suma_resta, 20)])),
        ("Problemas de multiplicar con suma o resta", mix(R, seen, [(s3_mult, 20)])),
        ("Problemas con división", mix(R, seen, [(s4_div, 20)])),
    ]
    body = lesson(
        ["Lee el problema con calma y busca la <b>pregunta</b>. Piensa qué datos necesitas.",
         "Muchas veces hace falta una operación para calcular un dato que no está en el enunciado, y otra para responder a la pregunta.",
         "En una expresión, primero se hace lo que está entre <b>paréntesis</b>; después, las multiplicaciones y divisiones; y al final, las sumas y restas.",
         "Al terminar, comprueba que la respuesta tiene sentido."],
        [("Compra 3 libretas de 4 € y paga con 20 €. ¿Cuánto le devuelven?", ["3 × 4 = 12 €", "20 − 12 = 8 €"], "8 €"),
         ("(25 + 15) × 3", ["Primero el paréntesis: 25 + 15 = 40", "40 × 3"], "120")],
        [["Hacer solo una operación", "Comprueba si has respondido de verdad a la pregunta."],
         ["Saltarse el paréntesis", "(25 + 15) × 3 = 120, pero 25 + 15 × 3 = 70."],
         ["Elegir la operación por una palabra", "«Más» no siempre es sumar: piensa en la situación."]])
    faq = [("¿En qué orden se hacen las operaciones?", "Primero los paréntesis, después las multiplicaciones y divisiones, y por último las sumas y restas, de izquierda a derecha."),
           ("¿Cómo se resuelve un problema de dos operaciones?", "Se lee, se buscan los datos y la pregunta, se piensa qué dato intermedio hace falta, se hacen las dos operaciones y se comprueba la solución.")]
    make_unit(R, "problemas-de-dos-operaciones", "N",
              "Resolución de problemas de la vida cotidiana que requieren dos operaciones con números naturales; uso del paréntesis; jerarquía de las operaciones",
              "Problemas de dos operaciones", "Problemas de dos operaciones",
              "Fichas de matemáticas de 4.º de Primaria: problemas de dos operaciones con suma, resta, multiplicación y división, operaciones combinadas con paréntesis. 100 ejercicios con soluciones.",
              "Primero el paréntesis", "Calcula el dato que falta y responde.",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
