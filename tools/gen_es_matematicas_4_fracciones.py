# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Fracciones (Sentido numérico)
Numerador y denominador, leer y escribir fracciones, representarlas (tiras y círculos), comparar fracciones con el mismo
denominador o el mismo numerador, fracciones mayores, menores e iguales que la unidad, número mixto,
fracción de un número, sumar y restar fracciones con el mismo denominador.
Errores: contar las partes sin colorear, pensar que 1/8 es mayor que 1/4 porque 8 &gt; 4, sumar también los denominadores.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, DIV, fr, tira, circulo, nomfrac, Kids

R = random.Random(44010)
K = Kids(R)


def s1_leer():
    d = R.randint(2, 10)
    n = R.randint(1, d - 1)
    k = R.choice(["dib", "dib", "leer", "escribir", "terminos"])
    if k == "dib":
        pic = tira(d, n) if R.random() < 0.6 else circulo(d, n)
        return mcq(pic + "¿Qué fracción está coloreada?", fr(n, d), [fr(d - n, d) if d - n != n else fr(n, d + 1), fr(d, n), fr(n, d - n) if d - n != n else fr(n + 1, d), fr(n + 1, d) if n + 1 < d else fr(n - 1, d) if n > 1 else fr(n, d + 2)],
                       "Hay %d partes iguales y %d coloreada%s: <b>%s</b>." % (d, n, "" if n == 1 else "s", fr(n, d)))
    if k == "leer":
        return mcq("¿Cómo se lee la fracción %s?" % fr(n, d), nomfrac(n, d), [nomfrac(d - n, d) if d - n != n else nomfrac(n, d + 1) if d < 10 else nomfrac(n, d - 1), nomfrac(n, d - 1) if d > 2 and n < d - 1 else nomfrac(n, d + 1),
                                                                         nomfrac(n + 1, d) if n + 1 < d else nomfrac(n, d + 2) if d + 2 <= 12 else nomfrac(n, d - 2)],
                   "%s se lee «<b>%s</b>»." % (fr(n, d), nomfrac(n, d)))
    if k == "escribir":
        return mcq("¿Cómo se escribe «%s»?" % nomfrac(n, d), fr(n, d), [fr(d, n), fr(n, d + 1), fr(n + 1, d) if n + 1 < d else fr(n, d - 1) if d > 2 else fr(n, d + 2)],
                   "«%s» = <b>%s</b>." % (nomfrac(n, d), fr(n, d)))
    w = R.choice(["numerador", "denominador"])
    return mcq("En la fracción %s, ¿cuál es el %s?" % (fr(n, d), w), str(n if w == "numerador" else d), [str(d if w == "numerador" else n), str(n + d), str(d - n) if d - n not in (n, d) else str(n * d)],
               "El numerador (arriba) es %d: las partes que se toman. El denominador (abajo) es %d: las partes iguales en que se divide. Respuesta: <b>%d</b>." % (n, d, n if w == "numerador" else d))


def s2_comparar():
    k = R.choice(["mismo_d", "mismo_n", "unidad", "unidad", "mayor"])
    if k == "mismo_d":
        d = R.randint(3, 12)
        a, b = R.sample(range(1, d), 2)
        ok = "%s %s %s" % (fr(a, d), "&lt;" if a < b else "&gt;", fr(b, d))
        return mcq("Compara %s y %s. ¿Qué es correcto?" % (fr(a, d), fr(b, d)), ok, ["%s %s %s" % (fr(a, d), "&gt;" if a < b else "&lt;", fr(b, d)), "%s = %s" % (fr(a, d), fr(b, d)), "no se pueden comparar"],
                       "Con el mismo denominador, es mayor la que tiene mayor numerador: <b>%s</b>." % ok)
    if k == "mismo_n":
        n = R.randint(1, 3)
        a, b = R.sample(range(n + 1, 11), 2)
        ok = "%s %s %s" % (fr(n, a), "&gt;" if a < b else "&lt;", fr(n, b))
        return mcq("Compara %s y %s. ¿Qué es correcto?" % (fr(n, a), fr(n, b)), ok, ["%s %s %s" % (fr(n, a), "&lt;" if a < b else "&gt;", fr(n, b)), "%s = %s" % (fr(n, a), fr(n, b)), "no se pueden comparar"],
                       "Con el mismo numerador, es mayor la de menor denominador (las partes son más grandes): <b>%s</b>." % ok)
    if k == "unidad":
        d = R.randint(2, 10)
        n = R.choice([R.randint(1, d - 1), d, R.randint(d + 1, 3 * d)])
        ok = "menor que la unidad" if n < d else "igual a la unidad" if n == d else "mayor que la unidad"
        return mcq("¿La fracción %s es mayor, menor o igual que la unidad?" % fr(n, d), ok, [x for x in ["menor que la unidad", "igual a la unidad", "mayor que la unidad", "no se puede saber"] if x != ok],
                   "El numerador %d es %s el denominador %d: <b>%s</b>." % (n, "menor que" if n < d else "igual que" if n == d else "mayor que", d, ok))
    d = R.randint(4, 12)
    ns = R.sample(range(1, d), 4) if d > 4 else None
    if not ns:
        return None
    m = max(ns)
    return mcq("¿Cuál es la mayor de %s?" % ", ".join(fr(x, d) for x in ns), fr(m, d), [fr(x, d) for x in ns], "Mismo denominador: la de mayor numerador, <b>%s</b>." % fr(m, d))


def s3_de_un_numero():
    d = R.choice([2, 3, 4, 5, 6, 8, 10])
    n = R.randint(1, d - 1)
    t = d * R.randint(2, 30)
    r = t // d * n
    k = R.choice(["calc", "ctx"])
    if k == "calc":
        return mcq("Calcula %s de %d." % (fr(n, d), t), str(r), [str(t // d), str(t * n), str(t - r), str(t // n) if t % n == 0 and n > 1 else str(r + n)],
                   "%d %s %d = %d; %d %s %d = <b>%d</b>." % (t, DIV, d, t // d, t // d, POR, n, r))
    p, g = K.next()
    ctx = R.choice([("En un autobús van %d personas y %s son niños. ¿Cuántos niños van?", "niños"), ("Una clase tiene %d libros y %s son de aventuras. ¿Cuántos libros son de aventuras?", "libros"),
                    ("Un pastel cuesta %d € y hoy está rebajado %s del precio. ¿Cuántos euros de rebaja son?", "€"), ("En un huerto hay %d plantas y %s son tomateras. ¿Cuántas tomateras hay?", "plantas")])
    return mcq(ctx[0] % (t, fr(n, d)), str(r), [str(t // d) if n > 1 else str(t // d + 1), str(t * n), str(t - r), str(r + d)],
               "%s de %d: %d %s %d = %d; %d %s %d = <b>%d</b>." % (fr(n, d), t, t, DIV, d, t // d, t // d, POR, n, r))


def s4_suma():
    d = R.randint(3, 12)
    k = R.choice(["suma", "resta", "mixto", "mixto2"])
    if k == "suma":
        a = R.randint(1, d - 1)
        b = R.randint(1, d)
        return mcq("Calcula: %s + %s" % (fr(a, d), fr(b, d)), fr(a + b, d), [fr(a + b, d + d), fr(a * b, d), fr(a + b, d * d), fr(a + b + 1, d)],
                   "Con el mismo denominador se suman los numeradores y se deja el denominador: <b>%s</b>." % fr(a + b, d))
    if k == "resta":
        a = R.randint(2, d + 3)
        b = R.randint(1, a - 1)
        return mcq("Calcula: %s − %s" % (fr(a, d), fr(b, d)), fr(a - b, d), [fr(a + b, d), fr(a - b, d + d), fr(b, d) if b != a - b else fr(a, d), fr(a - b + 1, d)],
                   "Se restan los numeradores y se deja el denominador: <b>%s</b>." % fr(a - b, d))
    if k == "mixto":
        e = R.randint(1, 4)
        n = R.randint(1, d - 1)
        tot = e * d + n
        return mcq("Escribe %s como número mixto." % fr(tot, d), "%d %s" % (e, fr(n, d)), ["%d %s" % (n, fr(e, d)) if e < d and n != e else "%d %s" % (e + 1, fr(n, d)), "%d %s" % (e + 1, fr(n, d)), "%d %s" % (e, fr(n + 1, d)) if n + 1 < d else "%d %s" % (e - 1, fr(n, d)) if e > 1 else "%d %s" % (e, fr(n, d + 1))],
                   "%d %s %d = %d y resto %d: <b>%d %s</b>." % (tot, DIV, d, e, n, e, fr(n, d)))
    e = R.randint(1, 4)
    n = R.randint(1, d - 1)
    tot = e * d + n
    return mcq("Escribe %d %s como fracción." % (e, fr(n, d)), fr(tot, d), [fr(e + n, d), fr(e * n, d), fr(tot, d * e), fr(tot + d, d)],
               "%d %s %d + %d = %d: <b>%s</b>." % (e, POR, d, n, tot, fr(tot, d)))


def s5_problema():
    p, g = K.next()
    k = R.choice(["pizza", "camino", "dinero", "botella", "libro", "tarta"])
    if k == "pizza":
        d = R.choice([6, 8, 10, 12])
        a, b = R.randint(1, d // 2), R.randint(1, d // 2)
        return mcq("Una pizza está cortada en %d trozos iguales. %s come %s y su hermano %s. ¿Qué fracción de pizza han comido entre los dos?" % (d, p, fr(a, d), fr(b, d)), fr(a + b, d),
                   [fr(a + b, 2 * d), fr(d - a - b, d) if d - a - b != a + b else fr(a + b + 1, d), fr(a * b, d) if a * b != a + b else fr(a + b, d + 1), fr(a + b + 1, d)],
                   "%s + %s = <b>%s</b>." % (fr(a, d), fr(b, d), fr(a + b, d)))
    if k == "camino":
        d = R.choice([5, 6, 8, 10])
        a = R.randint(1, d - 1)
        return mcq("%s ha recorrido %s del camino al colegio. ¿Qué fracción del camino le falta?" % (p, fr(a, d)), fr(d - a, d), [fr(a, d) if a != d - a else fr(a + 1, d), fr(d - a, 2 * d), fr(1, d) if d - a != 1 else fr(2, d), fr(d, a)],
                   "El camino entero es %s. %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(a, d), fr(d - a, d)))
    if k == "dinero":
        d = R.choice([2, 3, 4, 5])
        n = R.randint(1, d - 1)
        t = d * R.randint(4, 20)
        return mcq("%s tiene %d € y se gasta %s en un regalo. ¿Cuánto dinero le queda?" % (p, t, fr(n, d)), "%d €" % (t - t // d * n), ["%d €" % (t // d * n), "%d €" % (t // d), "%d €" % (t - n), "%d €" % (t - d)],
                   "Gasta %d %s %d %s %d = %d €. Le quedan %d − %d = <b>%d €</b>." % (t, DIV, d, POR, n, t // d * n, t, t // d * n, t - t // d * n))
    if k == "botella":
        n = R.choice([1, 3])
        return mcq("Una botella tiene 1000 mL de zumo. Nos bebemos %s. ¿Cuántos mililitros quedan?" % fr(n, 4),
                   "%d mL" % (1000 - 250 * n), ["%d mL" % (250 * n), "%d mL" % (1000 - n), "%d mL" % (1000 - 250 * n + 250), "%d mL" % (1000 // 3)],
                   "%s de 1000 = %d mL. Quedan 1000 − %d = <b>%d mL</b>." % (fr(n, 4), 250 * n, 250 * n, 1000 - 250 * n))
    if k == "libro":
        d = R.choice([3, 4, 5, 6])
        t = d * R.randint(20, 60)
        n = R.randint(1, d - 1)
        return mcq("Un libro tiene %d páginas. %s ha leído %s. ¿Cuántas páginas ha leído?" % (t, p, fr(n, d)), str(t // d * n), [str(t // d), str(t - t // d * n) if t - t // d * n != t // d * n else str(t // d * n + d), str(t * n), str(t - n)],
                   "%d %s %d = %d; %d %s %d = <b>%d</b>." % (t, DIV, d, t // d, t // d, POR, n, t // d * n))
    d = R.choice([8, 10, 12])
    a = R.randint(2, d // 2)
    b = R.randint(1, d - a - 1)
    return mcq("Una tarta tiene %d trozos iguales. Por la mañana se comen %s y por la tarde %s. ¿Qué fracción de tarta queda?" % (d, fr(a, d), fr(b, d)), fr(d - a - b, d),
               [fr(a + b, d), fr(d - a, d), fr(d - a - b, 2 * d), fr(d - b, d) if d - b != d - a else fr(d - a - b + 1, d)],
               "Se comen %s + %s = %s. Queda %s − %s = <b>%s</b>." % (fr(a, d), fr(b, d), fr(a + b, d), fr(d, d), fr(a + b, d), fr(d - a - b, d)))


def main():
    seen = set()
    sets = [
        ("Leer y representar fracciones", mix(R, seen, [(s1_leer, 20)])),
        ("Comparar fracciones", mix(R, seen, [(s2_comparar, 20)])),
        ("Fracción de un número", mix(R, seen, [(s3_de_un_numero, 20)])),
        ("Sumar, restar y número mixto", mix(R, seen, [(s4_suma, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Una <b>fracción</b> indica las partes que tomamos de una unidad dividida en partes iguales. En %s, el <b>denominador</b> (4) indica en cuántas partes se divide y el <b>numerador</b> (3), cuántas tomamos." % fr(3, 4),
         "Con el mismo denominador, es mayor la fracción con mayor numerador. Con el mismo numerador, es mayor la de menor denominador.",
         "Para calcular %s de 20: 20 : 4 = 5 y 5 × 3 = 15." % fr(3, 4),
         "Para sumar fracciones con el mismo denominador, se suman los numeradores y se deja el denominador."],
        [("¿Cuánto es %s de 24?" % fr(2, 3), ["24 : 3 = 8", "8 × 2 = 16"], "16"),
         ("%s + %s" % (fr(3, 8), fr(4, 8)), ["3 + 4 = 7", "el denominador sigue siendo 8"], fr(7, 8))],
        [["Contar las partes sin colorear", "El numerador son las partes coloreadas."],
         ["Creer que %s &gt; %s porque 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Si divides en más partes, cada parte es más pequeña."],
         ["Sumar los denominadores", "%s + %s = %s, no %s." % (fr(1, 5), fr(2, 5), fr(3, 5), fr(3, 10))]],
        tira(4, 3))
    faq = [("¿Cómo se calcula la fracción de un número?", "Se divide el número entre el denominador y el resultado se multiplica por el numerador. Por ejemplo, 3/4 de 20: 20 : 4 = 5 y 5 × 3 = 15."),
           ("¿Cuándo una fracción es mayor que la unidad?", "Cuando el numerador es mayor que el denominador, como 7/4. Entonces se puede escribir como número mixto: 7/4 = 1 y 3/4.")]
    make_unit(R, "fracciones", "N",
              "Fracciones: significado, lectura, escritura y representación; comparación de fracciones; fracciones y la unidad; fracción de una cantidad; suma y resta de fracciones con igual denominador",
              "Fracciones", "Fracciones",
              "Fichas de matemáticas de 4.º de Primaria: leer y representar fracciones, comparar, fracciones y la unidad, número mixto, fracción de un número y sumar y restar fracciones. 100 ejercicios con soluciones.",
              "Numerador: las partes que tomas; denominador: en cuántas partes divides", "Mismo denominador: suma o resta los numeradores.",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
