# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Potencias y raíz cuadrada (Sentido numérico)
Potencia como producto de factores iguales (base y exponente), cuadrados y cubos, potencias de base 10 y descomposición polinómica;
6.º: raíz cuadrada exacta y entera, cuadrados perfectos.
Errores: multiplicar la base por el exponente (3² = 6), contar mal los ceros de 10ⁿ.
"""
import random
from es_c3 import M, mix, lesson, make_unit, num, POR, bank

R = None
LV = 6
SUP = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}


def pw(b, e):
    return "%s%s" % (num(b), "".join(SUP[c] for c in str(e)))


def s1_concepto():
    b, e = R.randint(2, 9), R.randint(2, 5)
    k = R.choice(["producto", "escribir", "base", "leer"])
    prod = " %s " % POR
    if k == "producto":
        return M("¿Qué producto es igual a %s?" % pw(b, e), prod.join([str(b)] * e), [prod.join([str(e)] * b), "%d %s %d" % (b, POR, e), " + ".join([str(b)] * e)], "La base %d se multiplica %d veces: <b>%s</b>." % (b, e, prod.join([str(b)] * e)))
    if k == "escribir":
        return M("Escribe como potencia: %s" % prod.join([str(b)] * e), pw(b, e), [pw(e, b), pw(b, e + 1), pw(b * e, 1)], "%d factores iguales a %d: <b>%s</b>." % (e, b, pw(b, e)))
    if k == "base":
        w = R.choice(["base", "exponente"])
        return M("En la potencia %s, ¿cuál es el %s?" % (pw(b, e), w), str(b if w == "base" else e), [str(e if w == "base" else b), str(b ** e), str(b * e)], "Base %d (el número que se multiplica), exponente %d (las veces): <b>%d</b>." % (b, e, b if w == "base" else e))
    n = {2: "al cuadrado", 3: "al cubo", 4: "a la cuarta", 5: "a la quinta"}[e]
    return M("¿Cómo se lee %s?" % pw(b, e), "%s %s" % (num(b), n), ["%s por %s" % (num(b), num(e)), "%s elevado a %s" % (num(e), num(b)), "%s %s" % (num(b), {2: "al cubo", 3: "al cuadrado", 4: "al cubo", 5: "a la cuarta"}[e])],
             "Se lee «<b>%s %s</b>»." % (num(b), n))


def s2_calcular():
    k = R.choice(["cuad", "cubo", "pot", "comparar"])
    if k == "cuad":
        b = R.randint(2, 15 if LV == 6 else 10)
        return M("Calcula: %s" % pw(b, 2), num(b * b), [num(2 * b), num(b * b + b), num(b * b - 1), num(b + 2)], "%d %s %d = <b>%s</b>." % (b, POR, b, num(b * b)))
    if k == "cubo":
        b = R.randint(2, 10 if LV == 6 else 6)
        return M("Calcula: %s" % pw(b, 3), num(b ** 3), [num(3 * b), num(b * b), num(b ** 3 + b), num(b ** 3 - 1)], "%d %s %d %s %d = <b>%s</b>." % (b, POR, b, POR, b, num(b ** 3)))
    if k == "pot":
        b, e = R.choice([(2, 4), (2, 5), (2, 6), (3, 4), (2, 7), (5, 3), (3, 3), (4, 3), (2, 8), (5, 4), (6, 3), (10, 3)])
        return M("Calcula: %s" % pw(b, e), num(b ** e), [num(b * e), num(b ** (e - 1)), num(b ** e + b), num(e ** b) if e ** b != b ** e else num(b ** e * 2)], "<b>%s</b>." % num(b ** e))
    a, b = R.sample([(2, 5), (5, 2), (3, 4), (4, 3), (2, 6), (6, 2), (3, 3), (2, 4), (4, 2), (10, 2), (2, 10), (5, 3), (3, 5)], 2)
    va, vb = a[0] ** a[1], b[0] ** b[1]
    if va == vb:
        ok = "%s = %s" % (pw(*a), pw(*b))
    else:
        ok = "%s %s %s" % (pw(*a), "&lt;" if va < vb else "&gt;", pw(*b))
    opts = ["%s %s %s" % (pw(*a), s, pw(*b)) for s in ("&lt;", "&gt;", "=")]
    return M("Compara %s y %s. ¿Qué es correcto?" % (pw(*a), pw(*b)), ok, opts + ["no se pueden comparar"], "%s = %s y %s = %s: <b>%s</b>." % (pw(*a), num(va), pw(*b), num(vb), ok))


def s3_diez():
    k = R.choice(["valor", "pot", "desc", "desc2"])
    if k == "valor":
        e = R.randint(2, 9)
        return M("Calcula: %s" % pw(10, e), num(10 ** e), [num(10 ** (e - 1)), num(10 ** (e + 1)), num(10 * e)], "%d ceros: <b>%s</b>." % (e, num(10 ** e)))
    if k == "pot":
        e = R.randint(2, 9)
        a = R.randint(2, 9)
        return M("Escribe %s como producto de un número por una potencia de 10." % num(a * 10 ** e), "%d %s %s" % (a, POR, pw(10, e)), ["%d %s %s" % (a, POR, pw(10, e - 1)), "%d %s %s" % (a, POR, pw(10, e + 1)), "%s %s %d" % (pw(a, e), POR, 10)],
                 "%s tiene %d ceros: <b>%d %s %s</b>." % (num(a * 10 ** e), e, a, POR, pw(10, e)))
    n = R.randint(1000, 99999 if LV == 5 else 999999)
    s = str(n)
    parts = [(int(c), len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    def tx(L):
        return " + ".join(("%d %s %s" % (c, POR, pw(10, e)) if e > 1 else "%d %s 10" % (c, POR) if e == 1 else str(c)) for c, e in L)
    ok = tx(parts)
    w1 = tx([(c, e + 1 if e else e) for c, e in parts])
    w2 = tx([(c, e - 1 if e > 1 else e) for c, e in parts])
    if k == "desc":
        return M("¿Cuál es la descomposición polinómica de %s?" % num(n), ok, [w1, w2, " + ".join(str(c) for c, e in parts)], "<b>%s</b>." % ok)
    return M("¿Qué número es %s?" % ok, num(n), [num(int(s[::-1])), num(n * 10), num(int(s.replace("0", "")))], "<b>%s</b>." % num(n))


def s4_raiz():
    k = R.choice(["exacta", "exacta", "entera", "perfecto"])
    if k == "exacta":
        r = R.randint(2, 15)
        return M("Calcula: √%s" % num(r * r), num(r), [num(r * r // 2), num(r + 1), num(r - 1), num(2 * r)], "%d %s %d = %s, así que √%s = <b>%d</b>." % (r, POR, r, num(r * r), num(r * r), r))
    if k == "entera":
        r = R.randint(3, 12)
        n = r * r + R.randint(1, 2 * r)
        return M("¿Entre qué dos números está √%d?" % n, "entre %d y %d" % (r, r + 1), ["entre %d y %d" % (r - 1, r), "entre %d y %d" % (r + 1, r + 2), "entre %d y %d" % (n // 2 - 1, n // 2)],
                 "%d² = %d y %d² = %d; %d está entre los dos: <b>entre %d y %d</b>." % (r, r * r, r + 1, (r + 1) ** 2, n, r, r + 1))
    sq = [x * x for x in range(4, 16)]
    p = R.choice(sq)
    ws = [p + R.choice([1, 2, -1, 3, 5]) for _ in range(6)]
    ws = [w for w in ws if w not in sq]
    return M("¿Cuál es un cuadrado perfecto: %s?" % ", ".join(sorted([num(p)] + [num(w) for w in ws[:3]], key=lambda t: int(t.replace(" ", "")))), num(p), [num(w) for w in ws], "%s = %d²: es un cuadrado perfecto." % (num(p), int(p ** 0.5)))


def s5_problema():
    k = R.choice(["cajas", "baldosas", "bacterias", "cubo"] + (["jardin"] if LV == 6 else []))
    if k == "cajas":
        b = R.randint(3, 8)
        return M("En un almacén hay %d estanterías. Cada estantería tiene %d cajas y cada caja, %d paquetes. ¿Cuántos paquetes hay? Escríbelo como potencia y calcula." % (b, b, b), "%s = %s" % (pw(b, 3), num(b ** 3)), ["%s = %s" % (pw(b, 2), num(b * b)), "%s = %s" % (pw(3, b), num(3 ** b)), "%d %s 3 = %d" % (b, POR, 3 * b)],
                 "%d %s %d %s %d = <b>%s</b>." % (b, POR, b, POR, b, num(b ** 3)))
    if k == "baldosas":
        l = R.randint(4, 15)
        return M("Un patio cuadrado tiene %d baldosas en cada lado. ¿Cuántas baldosas tiene en total?" % l, num(l * l), [num(4 * l), num(2 * l), num(l * l + l)], "%s = <b>%s</b>." % (pw(l, 2), num(l * l)))
    if k == "bacterias":
        h = R.randint(3, 8)
        return M("Unas bacterias se duplican cada hora. Si empiezas con 1, ¿cuántas hay después de %d horas?" % h, num(2 ** h), [num(2 * h), num(2 ** (h - 1)), num(h * h)], "%s = <b>%s</b>." % (pw(2, h), num(2 ** h)))
    if k == "cubo":
        a = R.randint(2, 6)
        return M("Un cubo grande está hecho con cubitos: %d de largo, %d de ancho y %d de alto. ¿Cuántos cubitos tiene?" % (a, a, a), num(a ** 3), [num(a * a), num(3 * a), num(6 * a * a)], "%s = <b>%s</b>." % (pw(a, 3), num(a ** 3)))
    a = R.randint(5, 15)
    return M("Un jardín cuadrado mide %s m². ¿Cuánto mide cada lado?" % num(a * a), "%d m" % a, ["%d m" % (a * a // 4), "%d m" % (a * a // 2), "%d m" % (a + 1)], "√%s = <b>%d m</b>." % (num(a * a), a))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40003 + lv * 1000)
    seen = set()
    if lv == 6:
        sets = [
            ("Qué es una potencia", mix(R, seen, [(s1_concepto, 20)])),
            ("Calcular potencias", mix(R, seen, [(s2_calcular, 20)])),
            ("Potencias de base 10", mix(R, seen, [(s3_diez, 20)])),
            ("La raíz cuadrada", mix(R, seen, [(s4_raiz, 20)])),
            ("Problemas", mix(R, seen, [(s5_problema, 20)])),
        ]
    else:
        sets = [
            ("Qué es una potencia", mix(R, seen, [(s1_concepto, 20)])),
            ("Cuadrados y cubos", mix(R, seen, [(s2_calcular, 20)])),
            ("Potencias de base 10", mix(R, seen, [(s3_diez, 20)])),
            ("Repaso", mix(R, seen, [(s1_concepto, 6), (s2_calcular, 7), (s3_diez, 7)])),
            ("Problemas", mix(R, seen, [(s5_problema, 20)])),
        ]
    body = lesson(
        ["Una <b>potencia</b> es un producto de factores iguales: 5³ = 5 × 5 × 5 = 125. El 5 es la <b>base</b> y el 3, el <b>exponente</b> (las veces que se multiplica).",
         "Exponente 2: «al cuadrado». Exponente 3: «al cubo».",
         "Las potencias de 10 tienen tantos ceros como indica el exponente: 10⁴ = 10 000."
         + (" La <b>raíz cuadrada</b> es la operación contraria al cuadrado: √49 = 7 porque 7² = 49." if lv == 6 else "")],
        [("Calcula 2⁵", ["2 × 2 × 2 × 2 × 2"], "32"),
         ("Descompón 4072", ["4 × 10³ + 7 × 10 + 2"], "4 × 10³ + 7 × 10 + 2")],
        [["Multiplicar base por exponente", "3² = 3 × 3 = 9, no 3 × 2 = 6."],
         ["Contar mal los ceros", "10⁶ = 1 000 000: seis ceros."],
         ["Confundir 2³ y 3²", "2³ = 8 y 3² = 9: no son iguales."]])
    faq = [("¿Qué es una potencia?", "Es una forma abreviada de escribir un producto de factores iguales. 4³ = 4 × 4 × 4 = 64."),
           ("¿Cómo se calcula la raíz cuadrada?", "Se busca el número que multiplicado por sí mismo da el número dado. √81 = 9 porque 9 × 9 = 81.")]
    make_unit(R, "potencias-y-raiz-cuadrada" if lv == 6 else "potencias", "N",
              "Potencias como producto de factores iguales; cuadrados y cubos; potencias de base 10 y descomposición polinómica" + ("; raíz cuadrada" if lv == 6 else ""),
              "Potencias y raíz cuadrada" if lv == 6 else "Potencias", "Potencias y raíz cuadrada" if lv == 6 else "Potencias",
              "Fichas de matemáticas de %d.º de Primaria: potencias, base y exponente, cuadrados y cubos, potencias de 10, descomposición polinómica%s y problemas. 100 ejercicios con soluciones." % (lv, ", raíz cuadrada" if lv == 6 else ""),
              "5³ = 5 × 5 × 5", "Base: el número; exponente: las veces.",
              body, faq, sets, 3, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
