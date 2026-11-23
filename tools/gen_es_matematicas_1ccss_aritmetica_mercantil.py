# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Aritmética mercantil (Sentido numérico)
Porcentajes, índices de variación, aumentos y disminuciones encadenados, IVA; interés simple y compuesto, capitalización fraccionada, TAE; préstamos (cuota de amortización).
Errores: sumar porcentajes encadenados, quitar el IVA multiplicando por 0,79, usar el tipo anual en periodos mensuales, confundir TAE con el tipo nominal.
"""
import math
import random
from es_ccss import M, mix, num, unit, L, r2, W, eu, pc, tabla, MINUS

R = random.Random(53001)
SEEN = set()


def X(lo, hi, step=10):
    return R.randrange(lo, hi + 1, step)


def s_porcentaje():
    t = R.choice(["sube", "baja", "iva", "iva", "indice", "variacion", "descuento"])
    if t in ("sube", "baja"):
        x, p = X(40, 900, 10), R.choice([4, 5, 8, 12, 15, 18, 25, 30, 35])
        f = 1 + p / 100 if t == "sube" else 1 - p / 100
        obj = R.choice(["un abrigo", "una bicicleta", "un móvil", "un billete de avión", "un sofá"])
        return M("El precio de %s es %s y %s un %d %%. ¿Cuál es el precio final?" % (obj, eu(x, 0), "sube" if t == "sube" else "baja", p),
                 eu(x * f), W([eu(x * p / 100), eu(x * (2 - f)), eu(x + (p if t == "sube" else -p)), eu(x * (1 + (p if t == "sube" else -p) / 10))]),
                 "Se multiplica por el índice de variación %s: %s · %s = <b>%s</b>." % (r2(f), eu(x, 0), r2(f), eu(x * f)))
    if t == "iva":
        base = X(20, 800, 5)
        x = base * 1.21
        return M("Un artículo cuesta %s con el IVA incluido (21 %%). ¿Cuál es su precio sin IVA?" % eu(x),
                 eu(base), W([eu(x * 0.79), eu(x - 21), eu(x / 1.021), eu(x * 1.21)]),
                 "Precio con IVA = base · 1,21, así que base = %s / 1,21 = <b>%s</b>. Multiplicar por 0,79 no deshace la subida." % (eu(x), eu(base)))
    if t == "indice":
        a, b = R.choice([(10, 20), (20, 10), (15, 10), (30, 20), (25, 20), (10, 10), (40, 25), (5, 8)])
        f = (1 + a / 100) * (1 - b / 100)
        v = (f - 1) * 100
        return M("Un precio sube un %d %% y después baja un %d %%. ¿Cuál es la variación total?" % (a, b),
                 ("sube un " if v > 0 else "baja un ") + pc(abs(v)) if abs(v) > 1e-9 else "no varía",
                 W([("sube un " if a > b else "baja un ") + pc(abs(a - b)) if a != b else "no varía", "sube un " + pc(a + b), ("baja un " if v > 0 else "sube un ") + pc(abs(v)) if abs(v) > 1e-9 else "baja un 1 %"]),
                 "Índice total: %s · %s = %s, es decir, <b>%s</b>. Los porcentajes no se suman." % (r2(1 + a / 100), r2(1 - b / 100), r2(f, 4), (("sube un " if v > 0 else "baja un ") + pc(abs(v))) if abs(v) > 1e-9 else "no varía"))
    if t == "variacion":
        a = X(1200, 9000, 100)
        p = R.choice([-15, -12, -8, -5, 4, 6, 10, 12, 20, 25])
        b = a * (1 + p / 100)
        if b != int(b):
            return None
        b = int(b)
        quien = R.choice(["Los habitantes de un pueblo", "Las visitas a un museo", "Los socios de un club", "Las ventas de una tienda (en unidades)"])
        ok = ("aumentó un " if p > 0 else "disminuyó un ") + pc(abs(p))
        wr = (b - a) / b * 100
        return M("%s pasaron de %s a %s en un año. ¿Cuál fue la variación porcentual?" % (quien, num(a), num(b)), ok,
                 W([("aumentó un " if p > 0 else "disminuyó un ") + pc(abs(wr)), ("disminuyó un " if p > 0 else "aumentó un ") + pc(abs(p)), ("aumentó un " if p > 0 else "disminuyó un ") + pc(abs(b - a) / 10)]),
                 "(%s − %s) / %s = %s → <b>%s</b>. Se divide entre el valor inicial." % (num(b), num(a), num(a), r2((b - a) / a, 2), ok))
    x, dsc = X(50, 600, 10), R.choice([10, 15, 20, 25, 30])
    f = (1 - dsc / 100) * 1.21
    return M("Un artículo de %s (sin IVA) tiene un descuento del %d %%. Después se añade el 21 %% de IVA. ¿Cuánto se paga?" % (eu(x, 0), dsc),
             eu(x * f), W([eu(x * (1 + (21 - dsc) / 100)), eu(x * (1 - dsc / 100)), eu(x * 1.21 - dsc), eu(x * 1.21)]),
             "%s · %s · 1,21 = <b>%s</b>." % (eu(x, 0), r2(1 - dsc / 100), eu(x * f)))


def s_simple():
    t = R.choice(["I", "I", "meses", "C", "r", "t"])
    C = X(1000, 20000, 500)
    r = R.choice([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    if t == "I":
        n = R.randint(2, 6)
        I = C * r / 100 * n
        return M("¿Qué interés producen %s al %s anual de interés simple durante %d años?" % (eu(C, 0), pc(r), n), eu(I),
                 W([eu(C * r / 100), eu(C * ((1 + r / 100) ** n - 1)), eu(C + I), eu(C * r * n)]), "I = C · r · t = %s · %s · %d = <b>%s</b>." % (eu(C, 0), r2(r / 100, 3), n, eu(I)))
    if t == "meses":
        m = R.choice([3, 4, 6, 8, 9, 10])
        I = C * r / 100 * m / 12
        return M("¿Qué interés simple producen %s al %s anual en %d meses?" % (eu(C, 0), pc(r), m), eu(I),
                 W([eu(C * r / 100 * m), eu(C * r / 100), eu(C * r / 100 * m / 100), eu(C * r / 100 * 12 / m)]), "El tiempo en años es %d/12: I = %s · %s · %d/12 = <b>%s</b>." % (m, eu(C, 0), r2(r / 100, 3), m, eu(I)))
    n = R.randint(2, 5)
    I = C * r / 100 * n
    if t == "C":
        return M("Un capital al %s anual de interés simple produce %s en %d años. ¿Cuál es el capital?" % (pc(r), eu(I), n), eu(C),
                 W([eu(I * n * r / 100), eu(I / (r / 100)), eu(I * 100 / r / n * 2), eu(C + I)]), "C = I / (r · t) = %s / (%s · %d) = <b>%s</b>." % (eu(I), r2(r / 100, 3), n, eu(C)))
    if t == "r":
        return M("%s producen %s de interés simple en %d años. ¿Cuál es el tipo de interés anual?" % (eu(C, 0), eu(I), n), pc(r),
                 W([pc(r * n), pc(I / C * 100), pc(r / 2), pc(r + 1)]), "r = I / (C · t) = %s / (%s · %d) = %s → <b>%s</b>." % (eu(I), eu(C, 0), n, r2(r / 100, 3), pc(r)))
    return M("¿Cuántos años tienen que estar %s al %s de interés simple para producir %s?" % (eu(C, 0), pc(r), eu(I)), "%d años" % n,
             W(["%d años" % (n + 1), "%d años" % (n * 2), "%d años" % (n - 1) if n > 2 else None, "%d años" % (n + 2), "%d años" % (n + 3)]), "t = I / (C · r) = %s / (%s · %s) = <b>%d años</b>." % (eu(I), eu(C, 0), r2(r / 100, 3), n))


def s_compuesto():
    t = R.choice(["Cf", "Cf", "mensual", "C0", "doblar", "r"])
    C = X(1000, 30000, 500)
    r = R.choice([1.5, 2, 2.5, 3, 3.5, 4, 5, 6])
    i = r / 100
    if t == "Cf":
        n = R.randint(3, 10)
        cf = C * (1 + i) ** n
        return M("Se invierten %s al %s anual de interés compuesto durante %d años. ¿Cuál es el capital final?" % (eu(C, 0), pc(r), n), eu(cf),
                 W([eu(C * (1 + i * n)), eu(C * (1 + i) ** (n - 1)), eu(C * (1 + i) ** n - C), eu(C * (1 + i) ** (n + 1))]),
                 "C<sub>f</sub> = C · (1 + r)<sup>t</sup> = %s · %s<sup>%d</sup> = <b>%s</b>." % (eu(C, 0), r2(1 + i, 3), n, eu(cf)))
    if t == "mensual":
        n = R.randint(2, 6)
        cf = C * (1 + i / 12) ** (12 * n)
        return M("Se depositan %s al %s anual con capitalización mensual durante %d años. ¿Cuál es el capital final?" % (eu(C, 0), pc(r), n), eu(cf),
                 W([eu(C * (1 + i) ** n), eu(C * (1 + i) ** (12 * n)), eu(C * (1 + i / 12) ** n), eu(C * (1 + i * n))]),
                 "Tipo mensual r/12 y 12 · %d = %d periodos: %s · (1 + %s/12)<sup>%d</sup> = <b>%s</b>." % (n, 12 * n, eu(C, 0), r2(i, 3), 12 * n, eu(cf)))
    if t == "C0":
        n = R.randint(3, 8)
        cf = C * (1 + i) ** n
        return M("¿Qué capital hay que invertir hoy al %s anual compuesto para tener %s dentro de %d años?" % (pc(r), eu(cf), n), eu(C),
                 W([eu(cf * (1 - i) ** n), eu(cf / (1 + i * n)), eu(cf / (1 + i) ** (n - 1)), eu(cf - C * i * n)]),
                 "C = C<sub>f</sub> / (1 + r)<sup>t</sup> = %s / %s<sup>%d</sup> = <b>%s</b>." % (eu(cf), r2(1 + i, 3), n, eu(C)))
    if t == "doblar":
        k = R.choice([2, 2, 3])
        n = math.log(k) / math.log(1 + i)
        ok = math.ceil(n - 1e-9)
        return M("Al %s anual de interés compuesto, ¿cuántos años completos hacen falta para que un capital se %s?" % (pc(r), "duplique" if k == 2 else "triplique"), "%d años" % ok,
                 W(["%d años" % round(100 * (k - 1) / r), "%d años" % (ok - 1), "%d años" % (ok + 2), "%d años" % round(k / i)]),
                 "(1 + r)<sup>t</sup> = %d → t = log %d / log %s ≈ %s. Hacen falta <b>%d años</b>. Se usan logaritmos." % (k, k, r2(1 + i, 3), r2(n), ok))
    n = R.randint(3, 6)
    cf = C * (1 + i) ** n
    return M("%s se convierten en %s en %d años a interés compuesto. ¿Cuál es el tipo de interés anual?" % (eu(C, 0), eu(cf), n), pc(r),
             W([pc((cf / C - 1) / n * 100), pc(r * n), pc((cf / C - 1) * 100), pc(r + 0.5)]),
             "(1 + r)<sup>%d</sup> = %s / %s → 1 + r = <sup>%d</sup>√%s = %s → <b>%s</b>." % (n, eu(cf), eu(C, 0), n, r2(cf / C, 4), r2(1 + i, 3), pc(r)))


def tae(r, k):
    return ((1 + r / 100 / k) ** k - 1) * 100


def s_tae():
    t = R.choice(["calc", "calc", "calc", "comparar", "teo"])
    if t == "calc":
        r = R.choice([2, 2.4, 3, 3.6, 4, 4.8, 5, 6])
        k, nm = R.choice([(12, "mensual"), (4, "trimestral"), (2, "semestral")])
        v = tae(r, k)
        return M("Un banco ofrece un %s nominal anual con liquidación %s de intereses. ¿Cuál es la TAE?" % (pc(r), nm), pc(v),
                 W([pc(r), pc(r / k), pc(r * (1 + r / 100)), pc(tae(r, 12 if k != 12 else 4))]),
                 "TAE = (1 + %s/%d)<sup>%d</sup> − 1 ≈ %s → <b>%s</b>." % (r2(r / 100, 3), k, k, r2(v / 100, 4), pc(v)))
    if t == "comparar":
        r1, r2_ = R.choice([(3, 2.95), (4, 3.95), (5, 4.9), (2, 1.98), (6, 5.85)])
        a, b = tae(r1, 1), tae(r2_, 12)
        if abs(a - b) < 0.005:
            return None
        ok = "B (%s nominal, mensual)" % pc(r2_) if b > a else "A (%s anual)" % pc(r1)
        return M("Oferta A: %s anual con un pago al año. Oferta B: %s nominal con liquidación mensual. ¿Cuál da más intereses?" % (pc(r1), pc(r2_)), ok,
                 W(["A (%s anual)" % pc(r1) if b > a else "B (%s nominal, mensual)" % pc(r2_), "las dos igual", "no se puede saber sin el capital"]),
                 "Se comparan las TAE: A → %s; B → %s. Es mejor <b>%s</b>." % (pc(a), pc(b), ok))
    q, a, w = R.choice([("¿Qué indica la TAE?", "el interés anual real, teniendo en cuenta la frecuencia de los pagos", ["el interés de cada mes", "el interés nominal que anuncia el banco", "el impuesto sobre los intereses"]),
                        ("Con el mismo tipo nominal, ¿qué liquidación da una TAE mayor?", "la mensual", ["la anual", "la semestral", "todas dan la misma"]),
                        ("Si los intereses se pagan una vez al año, la TAE es…", "igual al tipo nominal", ["mayor que el tipo nominal", "menor que el tipo nominal", "el doble del tipo nominal"]),
                        ("¿Para qué sirve la TAE?", "para comparar productos financieros con distinta frecuencia de pago", ["para calcular el IVA", "para saber el capital inicial", "para calcular la inflación"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def cuota(C, r, n, k=12):
    i = r / 100 / k
    return C * i / (1 - (1 + i) ** (-n * k))


def s_prestamo():
    t = R.choice(["cuota", "cuota", "anual", "total", "intereses"])
    C = X(6000, 30000, 1000) if t != "anual" else X(20000, 150000, 5000)
    r = R.choice([3, 4, 4.5, 5, 6, 7, 8])
    n = R.randint(2, 6) if t != "anual" else R.randint(5, 20)
    if t == "anual":
        a = cuota(C, r, n, 1)
        return M("Se pide un préstamo de %s al %s anual, a devolver en %d cuotas anuales iguales. ¿Cuánto es cada cuota?" % (eu(C, 0), pc(r), n), eu(a),
                 W([eu(C / n), eu(C * (1 + r / 100) / n), eu(C * (1 + r / 100 * n) / n), eu(C * r / 100)]),
                 "a = C · i / (1 − (1 + i)<sup>−n</sup>) con i = %s y n = %d: <b>%s</b>." % (r2(r / 100, 3), n, eu(a)))
    a = cuota(C, r, n)
    if t == "cuota":
        return M("Se pide un préstamo de %s al %s anual, a devolver en %d años con cuotas mensuales iguales. ¿Cuánto es la cuota mensual?" % (eu(C, 0), pc(r), n), eu(a),
                 W([eu(C / (12 * n)), eu(C * (1 + r / 100 * n) / (12 * n)), eu(cuota(C, r * 12, n)), eu(cuota(C, r, n, 1) / 12)]),
                 "i = %s/12 al mes, n = %d meses: a = C · i / (1 − (1 + i)<sup>−n</sup>) = <b>%s</b>." % (r2(r / 100, 3), 12 * n, eu(a)))
    if t == "total":
        return M("Un préstamo de %s se devuelve con %d cuotas mensuales de %s. ¿Cuánto se paga en total?" % (eu(C, 0), 12 * n, eu(a)), eu(a * 12 * n),
                 W([eu(a * n), eu(C), eu(a * 12 * n - C), eu(a * 12)]), "%d · %s = <b>%s</b>." % (12 * n, eu(a), eu(a * 12 * n)))
    return M("Un préstamo de %s se devuelve con %d cuotas mensuales de %s. ¿Cuánto se paga de intereses?" % (eu(C, 0), 12 * n, eu(a)), eu(a * 12 * n - C),
             W([eu(a * 12 * n), eu(C * r / 100 * n), eu(a * n - C) if a * n > C else eu(a), eu(C - a * n) if C > a * n else eu(a * 12)]),
             "Total pagado: %d · %s = %s. Intereses: %s − %s = <b>%s</b>." % (12 * n, eu(a), eu(a * 12 * n), eu(a * 12 * n), eu(C, 0), eu(a * 12 * n - C)))


sets = [("Porcentajes e IVA", mix(R, SEEN, [(s_porcentaje, 20)])), ("Interés simple", mix(R, SEEN, [(s_simple, 20)])), ("Interés compuesto", mix(R, SEEN, [(s_compuesto, 20)])),
        ("TAE", mix(R, SEEN, [(s_tae, 20)])), ("Préstamos y problemas", mix(R, SEEN, [(s_prestamo, 14), (s_compuesto, 3), (s_porcentaje, 3)]))]
think = ["<b>Porcentajes</b>: subir un p % es multiplicar por 1 + p/100; bajar, por 1 − p/100. Varios cambios seguidos: se multiplican los índices.",
         "<b>IVA</b> (21 %): con IVA = base · 1,21; para quitarlo se divide entre 1,21.",
         "<b>Interés simple</b>: I = C · r · t (los intereses no se acumulan). <b>Compuesto</b>: C<sub>f</sub> = C · (1 + r)<sup>t</sup> (los intereses producen intereses).",
         "Si se liquida k veces al año, el tipo de cada periodo es r/k y hay k · t periodos. La <b>TAE</b> = (1 + r/k)<sup>k</sup> − 1 permite comparar.",
         "<b>Préstamo</b> con cuotas iguales: a = C · i / (1 − (1 + i)<sup>−n</sup>), con i el tipo de cada periodo y n el número de cuotas."]
ex = [("5 000 € al 4 % compuesto, 3 años", ["5 000 · 1,04³ = 5 000 · 1,124864"], "5 624,32 €"), ("4 % nominal con liquidación trimestral", ["(1 + 0,04/4)⁴ − 1 = 0,04060"], "TAE 4,06 %")]
mist = [["Sumar porcentajes encadenados", "+20 % y −20 % no se anulan: 1,2 · 0,8 = 0,96."], ["Quitar el IVA multiplicando por 0,79", "Hay que dividir entre 1,21."],
        ["Usar el tipo anual con periodos mensuales", "Divide el tipo entre 12 y multiplica los años por 12."]]
body = L(think, ex, mist, tabla(["Años", "Interés simple (1 000 € al 5 %)", "Interés compuesto (1 000 € al 5 %)"],
                                [[str(t), eu(1000 * (1 + 0.05 * t)), eu(1000 * 1.05 ** t)] for t in (1, 5, 10, 20)]))
faq = [("¿Qué diferencia hay entre interés simple y compuesto?", "En el simple los intereses no se suman al capital; en el compuesto sí, y a partir de entonces también producen intereses. A largo plazo el compuesto crece mucho más."),
       ("¿Qué es la TAE?", "La tasa anual equivalente: el interés que de verdad se obtiene (o se paga) en un año. Sirve para comparar ofertas con distintas frecuencias de pago."),
       ("¿Cómo se calcula la cuota de un préstamo?", "Con la fórmula a = C · i / (1 − (1 + i)⁻ⁿ), donde i es el tipo de cada periodo (anual/12 si es mensual) y n el número de cuotas.")]
unit(1, R, "aritmetica-mercantil", "N", "Matemática financiera: porcentajes, índices de variación e IVA; interés simple y compuesto, capitalización fraccionada, TAE y préstamos",
     "Aritmética mercantil", "Aritmética mercantil", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: porcentajes, IVA, interés simple y compuesto, TAE y cuota de un préstamo. 100 ejercicios con soluciones.",
     "Compuesto: C · (1 + r)ᵗ", "Varios porcentajes: multiplica los índices.", body, faq, sets, 1)
