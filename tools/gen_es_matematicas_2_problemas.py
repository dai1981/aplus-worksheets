# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Problemas (Sentido numérico)
build(lv): lv = 1 → «problemas»: juntar, quitar, comparar y completar hasta 20 (algunos con decenas hasta 99), con dibujos;
lv = 2 → «problemas»: suma y resta hasta 999, comparar, completar, multiplicar (2, 3, 4, 5 y 10) y dos pasos.
Errores: sumar cuando hay que restar porque aparece «más», no leer la pregunta, olvidar la segunda operación.
"""
import random
from es_common import mcq, mix, lesson, make_unit
import es_pics as P

R = None
LV = 2
NOMBRES = [("Lucía", "ella"), ("Hugo", "él"), ("Martina", "ella"), ("Pablo", "él"), ("Sofía", "ella"), ("Mateo", "él"), ("Vega", "ella"), ("Leo", "él"), ("Alba", "ella"), ("Mario", "él")]
# (plural, femenino)
COSAS = [("cromos", False), ("canicas", True), ("pegatinas", True), ("caramelos", False), ("cuentos", False), ("globos", False), ("galletas", True), ("lápices", False), ("conchas", True), ("piedras", True),
         ("botones", False), ("flores", True), ("manzanas", True), ("estrellas", True)]
DIBUJO = {"canicas": "ball", "botones": "button", "flores": "flower", "manzanas": "apple", "estrellas": "star"}


def two():
    a, b = R.sample(NOMBRES, 2)
    return a, b


def nums():
    if LV == 1:
        return R.randint(3, 12), R.randint(2, 8)
    return R.randint(120, 600), R.randint(30, 380)


def cu(fem):
    return "¿Cuántas" if fem else "¿Cuántos"


def ops(ok, a, b):
    return [str(abs(a - b)) if a != b else str(ok + 2), str(a + b), str(ok + 1), str(ok - 1) if ok > 1 else str(ok + 3), str(ok + 10)]


def s_juntar():
    (p, _), _ = two()
    w, f = R.choice(COSAS)
    a, b = nums()
    t = R.choice(["regalan", "dos", "compra"])
    if t == "regalan":
        q = "%s tiene %d %s. Le regalan %d más. %s %s tiene ahora?" % (p, a, w, b, cu(f), w)
    elif t == "dos":
        q = "En una caja hay %d %s y en otra hay %d. %s %s hay en total?" % (a, w, b, cu(f), w)
    else:
        q = "%s junta %d %s por la mañana y %d por la tarde. %s %s junta en todo el día?" % (p, a, w, b, cu(f), w)
    pic = ""
    if LV == 1 and a + b <= 20 and w in DIBUJO:
        pic = P.dos_grupos(a, DIBUJO[w], b)
    return mcq(pic + q, str(a + b), ops(a + b, a, b), "Juntamos: %d + %d = <b>%d</b>." % (a, b, a + b))


def s_quitar():
    (p, _), _ = two()
    w, f = R.choice(COSAS)
    a, b = nums()
    a = a + b
    t = R.choice(["pierde", "regala", "gasta"])
    if t == "pierde":
        q = "%s tenía %d %s y %s %d. %s %s le quedan?" % (p, a, w, "pierde", b, cu(f), w)
    elif t == "regala":
        q = "%s tiene %d %s y regala %d a su hermano. %s %s le quedan?" % (p, a, w, b, cu(f), w)
    else:
        q = "En una bolsa hay %d %s. Sacamos %d. %s %s quedan en la bolsa?" % (a, w, b, cu(f), w)
    pic = P.tachados(a, DIBUJO[w], b) if LV == 1 and a <= 20 and w in DIBUJO else ""
    return mcq(pic + q, str(a - b), [str(a + b)] + ops(a - b, a, b)[2:], "Quitamos: %d − %d = <b>%d</b>." % (a, b, a - b))


def s_comparar():
    (p, _), (q2, _) = two()
    w, f = R.choice(COSAS)
    a, b = nums()
    big = a + b
    t = R.choice(["mas", "menos", "diferencia"])
    if t == "mas":
        q = "%s tiene %d %s. %s tiene %d más que %s. %s %s tiene %s?" % (p, a, w, q2, b, p, cu(f), w, q2)
        return mcq(q, str(a + b), [str(abs(a - b)) if a != b else str(a + b + 2), str(b), str(a + b + 1)], "Tiene %d más: %d + %d = <b>%d</b>." % (b, a, b, a + b))
    if t == "menos":
        q = "%s tiene %d %s. %s tiene %d menos que %s. %s %s tiene %s?" % (p, big, w, q2, b, p, cu(f), w, q2)
        return mcq(q, str(a), [str(big + b), str(b), str(a + 1)], "Tiene %d menos: %d − %d = <b>%d</b>." % (b, big, b, a))
    q = "%s tiene %d %s y %s tiene %d. %s %s más tiene %s?" % (p, big, w, q2, a, cu(f), w, p)
    return mcq(q, str(b), [str(big + a), str(b + 1), str(a)], "Restamos para comparar: %d − %d = <b>%d</b>." % (big, a, b))


def s_completar():
    (p, _), _ = two()
    w, f = R.choice(COSAS)
    a, b = nums()
    t = R.choice(["album", "quiere"])
    if t == "album":
        q = "En un álbum caben %d %s. %s ya tiene %d. %s le faltan para completarlo?" % (a + b, w, p, a, cu(f))
    else:
        q = "%s tiene %d %s y quiere tener %d. %s le faltan?" % (p, a, w, a + b, cu(f))
    return mcq(q, str(b), [str(2 * a + b), str(b + 1), str(a)] + ([str(b - 1)] if b > 1 else []), "%d + ___ = %d. Faltan %d − %d = <b>%d</b>." % (a, a + b, a + b, a, b))


def s_dos():
    (p, _), _ = two()
    w, f = R.choice(COSAS)
    if LV == 1:
        a, b, c = R.randint(5, 10), R.randint(2, 6), R.randint(1, 4)
        if a + b - c <= 0:
            return None
        q = "%s tiene %d %s. Le regalan %d y después pierde %d. %s %s tiene ahora?" % (p, a, w, b, c, cu(f), w)
        r = a + b - c
        return mcq(q, str(r), [str(a + b), str(a + b + c), str(r + 1)], "%d + %d = %d; %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, r))
    k = R.choice(["mas_menos", "mult"])
    if k == "mas_menos":
        a, b, c = R.randint(200, 500), R.randint(100, 300), R.randint(50, 150)
        r = a + b - c
        q = "Una biblioteca tenía %d libros. Compra %d y presta %d. ¿Cuántos libros quedan en la biblioteca?" % (a, b, c)
        return mcq(q, str(r), [str(a + b), str(a + b + c), str(a - b + c) if a - b + c > 0 else str(r + 10)], "%d + %d = %d; %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, r))
    g, n, extra = R.choice([2, 3, 4, 5, 10]), R.randint(2, 9), R.randint(3, 20)
    q = "%s compra %d paquetes de %d %s y ya tenía %d. %s %s tiene ahora?" % (p, n, g, w, extra, cu(f), w)
    return mcq(q, str(n * g + extra), [str(n * g), str(n + g + extra), str((n + extra) * g)], "%d × %d = %d; %d + %d = <b>%d</b>." % (n, g, n * g, n * g, extra, n * g + extra))


GRUPOS = [("ruedas", "bicicleta", "bicicletas", 2, True), ("patas", "perro", "perros", 4, True), ("dedos", "mano", "manos", 5, False), ("ruedas", "coche", "coches", 4, True),
          ("lados", "triángulo", "triángulos", 3, False), ("huevos", "cartón", "cartones", 10, False), ("cromos", "sobre", "sobres", 5, False), ("yogures", "paquete", "paquetes", 4, False),
          ("lápices", "caja", "cajas", 10, False), ("zapatos", "par", "pares", 2, False)]


def s_mult():
    what, one, many, k, f = R.choice(GRUPOS)
    n = R.randint(2, 10)
    return mcq("Cada %s tiene %d %s. %s %s hay en %d %s?" % (one, k, what, cu(f), what, n, many), str(n * k), [str(n + k), str(n * k + k), str(n * k - k)], "%d grupos de %d: %d × %d = <b>%d</b>." % (n, k, n, k, n * k))


def s_elegir():
    a, b = nums()
    w, f = R.choice(COSAS)
    (p, _), _ = two()
    t = R.choice(["suma", "resta", "resta2"] + (["mult"] if LV == 2 else []))
    if t == "suma":
        q, ok = "%s tiene %d %s y le dan %d más. ¿Qué operación hay que hacer para saber %s tiene?" % (p, a, w, b, "cuántas" if f else "cuántos"), "%d + %d" % (a, b)
    elif t == "resta":
        q, ok = "%s tiene %d %s y regala %d. ¿Qué operación hay que hacer para saber %s le quedan?" % (p, a + b, w, b, "cuántas" if f else "cuántos"), "%d − %d" % (a + b, b)
    elif t == "resta2":
        q, ok = "%s tiene %d %s y quiere tener %d. ¿Qué operación hay que hacer para saber %s le faltan?" % (p, a, w, a + b, "cuántas" if f else "cuántos"), "%d − %d" % (a + b, a)
    else:
        n, g = R.randint(2, 9), R.choice([2, 3, 4, 5, 10])
        q, ok = "Hay %d bolsas con %d %s cada una. ¿Qué operación hay que hacer para saber %s hay?" % (n, g, w, "cuántas" if f else "cuántos"), "%d × %d" % (n, g)
        return mcq(q, ok, ["%d + %d" % (n, g), "%d − %d" % (max(n, g), min(n, g)) if n != g else "%d − %d" % (n + 1, g), "%d × %d" % (n, g + 1)], "Grupos iguales: <b>%s</b>." % ok)
    x, y = [int(v) for v in ok.replace("+", " ").replace("−", " ").split()]
    alt = ["%d − %d" % (max(x, y), min(x, y)) if "+" in ok else "%d + %d" % (x, y), "%d + %d" % (x, y + 1) if "+" in ok else "%d − %d" % (x, y + 1) if y + 1 < x else "%d + %d" % (x + 1, y), "%d + %d" % (x, x) if "+" in ok and x != y else "%d − %d" % (x + y, y) if "−" in ok else "%d + %d" % (y, y + 2)]
    return mcq(q, ok, alt, "Respuesta: <b>%s</b>." % ok)


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30008 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("Juntar y añadir", mix(R, seen, [(s_juntar, 20)])), ("Quitar", mix(R, seen, [(s_quitar, 20)])), ("Comparar y completar", mix(R, seen, [(s_comparar, 10), (s_completar, 10)])),
                ("¿Qué operación es?", mix(R, seen, [(s_elegir, 20)])), ("Problemas de dos pasos", mix(R, seen, [(s_dos, 14), (s_juntar, 3), (s_quitar, 3)]))]
        think = ["Lee el problema y busca la <b>pregunta</b>.", "Si se junta o se añade, se <b>suma</b>. Si se quita, se pierde o se regala, se <b>resta</b>.", "Al final, mira si la respuesta tiene sentido."]
        ex = [("Tengo 8 cromos y me dan 5. ¿Cuántos tengo?", ["Me dan: sumar", "8 + 5"], "13 cromos"), ("Tengo 12 globos y se escapan 4. ¿Cuántos quedan?", ["Se escapan: restar", "12 − 4"], "8 globos")]
        kb, ks = "Juntar: sumar. Quitar: restar.", "Busca primero la pregunta."
        meta = "Fichas de matemáticas de 1.º de Primaria: problemas de juntar, quitar, comparar y completar hasta 20 con dibujos. 100 ejercicios con soluciones."
        std = "Resolución de problemas de suma y resta (juntar, quitar, comparar, completar) con números hasta 20"
        sort = 5
    else:
        sets = [("Problemas de sumar", mix(R, seen, [(s_juntar, 20)])), ("Problemas de restar", mix(R, seen, [(s_quitar, 10), (s_completar, 10)])), ("Comparar: más que, menos que", mix(R, seen, [(s_comparar, 20)])),
                ("Problemas de multiplicar", mix(R, seen, [(s_mult, 14), (s_elegir, 6)])), ("Problemas de dos pasos", mix(R, seen, [(s_dos, 14), (s_elegir, 6)]))]
        think = ["Lee el problema y busca la <b>pregunta</b> y los <b>datos</b>.", "Juntar o añadir: suma. Quitar o comparar: resta. Grupos iguales: multiplicación.",
                 "En los problemas de <b>dos pasos</b>, la primera operación calcula un dato que no aparece en el enunciado."]
        ex = [("Tiene 245 cromos y 130 menos que su prima. ¿Cuántos tiene la prima?", ["La prima tiene más", "245 + 130"], "375"), ("Compra 4 paquetes de 5 yogures y ya tenía 3", ["4 × 5 = 20", "20 + 3"], "23")]
        kb, ks = "Datos, pregunta y operación", "Grupos iguales: multiplica."
        meta = "Fichas de matemáticas de 2.º de Primaria: problemas de sumar, restar, comparar, multiplicar y de dos pasos hasta 999. 100 ejercicios con soluciones."
        std = "Resolución de problemas de suma, resta y multiplicación con números hasta 999; problemas de dos pasos"
        sort = 7
    mist = [["Sumar porque aparece la palabra «más»", "«Tiene 5 más que yo» puede pedir una resta si buscas lo que tienes tú."], ["No leer la pregunta", "Subraya la pregunta antes de calcular."], ["Olvidar el segundo paso", "Comprueba que has respondido a lo que se pregunta."]]
    body = lesson(think, ex, mist)
    faq = [("¿Cómo sé si tengo que sumar o restar?", "Piensa en lo que pasa: si se junta o se añade, se suma; si se quita o se compara, se resta."), ("¿Qué es un problema de dos pasos?", "Un problema que necesita dos operaciones: la primera da un dato para la segunda.")]
    make_unit(R, "problemas", "N", std, "Problemas", "Problemas", meta, kb, ks, body, faq, sets, sort, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
