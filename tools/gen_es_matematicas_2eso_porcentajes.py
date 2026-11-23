# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Porcentajes e interés (Sentido numérico)
build(lv): lv = 2 → «porcentajes»: porcentaje de una cantidad, el total a partir de la parte, aumentos y disminuciones con índice de variación, IVA, interés simple;
lv = 4 → «porcentajes-e-interes-compuesto»: variaciones encadenadas, porcentaje inverso, interés simple y compuesto, TAE sencilla.
Errores: encadenar porcentajes sumándolos (subir 10 % y bajar 10 % no deja igual), calcular el precio original restando el porcentaje al precio final, aplicar el interés simple año a año sobre el total.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, d, num, eur, unit, L, Kids

R = None
LV = 2
K = None


def r2(x):
    v = int(math.floor(float(x) * 100 + 0.5))
    return d(F(v, 100))


def euros(x):
    return r2(x) + " €"


def s_basico():
    t = R.choice(["de", "total", "que", "indice"])
    if t == "de":
        p = R.choice([3, 4, 6, 12, 15, 18, 35, 45, 65, 85])
        n = R.choice([120, 240, 360, 450, 600, 840, 1200, 1500])
        r = F(p * n, 100)
        return M("Calcula el %d %% de %s." % (p, num(n)), d(r), [d(F(n, p)) if F(n, p).denominator in (1, 2, 4, 5, 10) else d(r + 10), d(n - r), d(r * 10)], "%d · %s : 100 = <b>%s</b>." % (p, num(n), d(r)))
    if t == "total":
        p = R.choice([10, 20, 25, 30, 40, 60, 75])
        tot = R.choice([80, 120, 200, 240, 360, 480, 600])
        part = F(p * tot, 100)
        if part.denominator != 1:
            return None
        return M("El %d %% de una cantidad es %d. ¿Cuál es la cantidad?" % (p, part), num(tot), [num(int(part) * p // 100) if int(part) * p % 100 == 0 else num(int(part) + p), num(int(part) + 100 - p), num(tot // 2) if tot // 2 != part else num(tot + 20)],
                 "Total = parte · 100 / %d = %d · 100 / %d = <b>%s</b>." % (p, part, p, num(tot)))
    if t == "que":
        tot = R.choice([40, 50, 80, 120, 200, 250, 400])
        p = R.choice([5, 10, 15, 20, 30, 35, 45, 60, 85])
        part = F(p * tot, 100)
        if part.denominator != 1:
            return None
        return M("¿Qué porcentaje de %d es %d?" % (tot, part), "%d %%" % p, ["%d %%" % part, "%d %%" % (100 - p), "%s %%" % d(F(tot, int(part))) if F(tot, int(part)).denominator in (1, 2, 4, 5, 10) else "%d %%" % (p + 5)],
                 "%d / %d · 100 = <b>%d %%</b>." % (part, tot, p))
    p = R.choice([5, 8, 12, 15, 20, 25, 30, 35, 40])
    up = R.random() < 0.5
    iv = F(100 + p, 100) if up else F(100 - p, 100)
    return M("¿Cuál es el índice de variación de %s del %d %%?" % ("un aumento" if up else "una disminución", p), d(iv), [d(F(100 - p, 100)) if up else d(F(100 + p, 100)), d(F(p, 100)), d(F(p, 10))],
             "%s: <b>%s</b>." % ("1 + %s" % d(F(p, 100)) if up else "1 − %s" % d(F(p, 100)), d(iv)))


def s_variacion():
    t = R.choice(["sube", "baja", "inverso", "iva", "encadena"])
    pr = R.choice([40, 60, 80, 120, 150, 250, 360, 480])
    p = R.choice([5, 10, 15, 20, 25, 30, 40])
    if t == "sube":
        return M("Un producto cuesta %d € y sube un %d %%. ¿Cuánto cuesta ahora?" % (pr, p), euros(F(pr * (100 + p), 100)), [euros(F(pr * p, 100)), euros(F(pr + p)), euros(F(pr * (100 - p), 100))],
                 "%d · %s = <b>%s</b>." % (pr, d(F(100 + p, 100)), euros(F(pr * (100 + p), 100))))
    if t == "baja":
        return M("Un abrigo de %d € tiene una rebaja del %d %%. ¿Cuánto cuesta?" % (pr, p), euros(F(pr * (100 - p), 100)), [euros(F(pr * p, 100)), euros(F(pr - p)), euros(F(pr * (100 + p), 100))],
                 "%d · %s = <b>%s</b>." % (pr, d(F(100 - p, 100)), euros(F(pr * (100 - p), 100))))
    if t == "inverso":
        fin = F(pr * (100 - p), 100)
        return M("Después de una rebaja del %d %%, una mochila cuesta %s. ¿Cuánto costaba antes?" % (p, euros(fin)), "%d €" % pr, [euros(fin * F(100 + p, 100)), euros(fin + p), euros(fin + F(pr * p, 100) + 5)],
                 "Antes = %s : %s = <b>%d €</b>." % (euros(fin), d(F(100 - p, 100)), pr))
    if t == "iva":
        iva = R.choice([21, 10, 4])
        return M("Una factura es de %d € sin IVA. ¿Cuánto se paga con un IVA del %d %%?" % (pr, iva), euros(F(pr * (100 + iva), 100)), [euros(F(pr * iva, 100)), euros(F(pr + iva)), euros(F(pr * (100 - iva), 100))],
                 "%d · %s = <b>%s</b>." % (pr, d(F(100 + iva, 100)), euros(F(pr * (100 + iva), 100))))
    a, b = R.choice([10, 20, 25, 30]), R.choice([10, 20, 25, 30])
    iv = F(100 + a, 100) * F(100 - b, 100)
    ch = (iv - 1) * 100
    ok = ("aumenta un %s %%" % d(ch)) if ch > 0 else ("disminuye un %s %%" % d(-ch)) if ch < 0 else "se queda igual"
    return M("Un precio sube un %d %% y después baja un %d %%. ¿Cómo cambia en total?" % (a, b), ok, ["se queda igual" if ch else "aumenta un 1 %", "%s un %d %%" % ("aumenta" if a > b else "disminuye", abs(a - b)) if a != b else "disminuye un %d %%" % a, "aumenta un %d %%" % (a + b)],
             "Índice total: %s · %s = %s: <b>%s</b>." % (d(F(100 + a, 100)), d(F(100 - b, 100)), d(iv), ok))


def s_interes():
    C = R.choice([1000, 2000, 3000, 5000, 8000, 10000, 12000])
    r = R.choice([2, 3, 4, 5, 6])
    t = R.randint(2, 6)
    k = R.choice(["simple", "simple_t", "compuesto", "compuesto", "comp_vs"] if LV >= 4 else ["simple", "simple", "simple_t", "simple"])
    if k == "simple":
        I = F(C * r * t, 100)
        return M("¿Qué interés producen %s € al %d %% anual de interés simple durante %d años?" % (num(C), r, t), euros(I), [euros(F(C * r, 100)), euros(C + I), euros(C * (F(100 + r, 100) ** t) - C)],
                 "I = C · r · t / 100 = %s · %d · %d / 100 = <b>%s</b>." % (num(C), r, t, euros(I)))
    if k == "simple_t":
        I = F(C * r * t, 100)
        return M("Un capital de %s € al %d %% de interés simple ha producido %s €. ¿Cuántos años ha estado?" % (num(C), r, euros(I)), "%d años" % t, ["%d años" % (t + 1), "%d años" % r, "%d años" % (t * 2)] if r != t else ["%d años" % (t + 1), "%d años" % (t - 1), "%d años" % (t * 2)],
                 "t = I · 100 / (C · r) = <b>%d años</b>." % t)
    if k == "compuesto":
        Cf = C * F(100 + r, 100) ** t
        return M("Se invierten %s € al %d %% anual de interés compuesto durante %d años. ¿Qué capital final se obtiene?" % (num(C), r, t), euros(Cf), [euros(C + F(C * r * t, 100)), euros(C * F(100 + r * t, 100) + 1), euros(C * F(100 + r, 100) ** (t - 1))],
                 "C<sub>f</sub> = C · (1 + r/100)<sup>t</sup> = %s · %s<sup>%d</sup> ≈ <b>%s</b>." % (num(C), d(F(100 + r, 100)), t, euros(Cf)))
    Cs = C + F(C * r * t, 100)
    Cc = C * F(100 + r, 100) ** t
    return M("%s € durante %d años al %d %%: ¿cuánto más se gana con interés compuesto que con simple?" % (num(C), t, r), euros(Cc - Cs), [euros(Cc - C), euros(Cs - C), "nada, es lo mismo"],
             "Compuesto: %s; simple: %s; diferencia ≈ <b>%s</b>." % (euros(Cc), euros(Cs), euros(Cc - Cs)))


def s_problema():
    p = K.next()[0]
    t = R.choice(["clase", "salario", "poblacion", "oferta", "deuda"])
    if t == "clase":
        n = R.choice([25, 28, 30, 32])
        k = R.randint(5, n - 5)
        return M("En una clase de %d alumnos, %d llevan gafas. ¿Qué porcentaje lleva gafas (redondea a las unidades)?" % (n, k), "%d %%" % round(100.0 * k / n), ["%d %%" % k, "%d %%" % round(100.0 * (n - k) / n), "%d %%" % (round(100.0 * k / n) + 3)],
                 "%d / %d · 100 ≈ <b>%d %%</b>." % (k, n, round(100.0 * k / n)))
    if t == "salario":
        s = R.choice([1200, 1500, 1800, 2000, 2400])
        p_ = R.choice([2, 3, 4, 5])
        return M("A %s le suben el sueldo un %d %%. Ganaba %s € al mes. ¿Cuánto gana ahora?" % (p, p_, num(s)), euros(F(s * (100 + p_), 100)), [euros(F(s + p_)), euros(F(s * p_, 100)), euros(F(s * (100 - p_), 100))],
                 "%s · %s = <b>%s</b>." % (num(s), d(F(100 + p_, 100)), euros(F(s * (100 + p_), 100))))
    if t == "poblacion":
        P0 = R.choice([5000, 8000, 12000, 20000])
        p_ = R.choice([2, 5, 10])
        y = R.randint(2, 3) if LV >= 4 else 1
        Pf = P0 * F(100 - p_, 100) ** y
        return M("Un pueblo de %s habitantes pierde el %d %% de su población cada año. ¿Cuántos habitantes tendrá dentro de %d año%s?" % (num(P0), p_, y, "" if y == 1 else "s"), num(int(round(float(Pf)))),
                 [num(P0 - P0 * p_ * y // 100) if y > 1 else num(P0 * p_ // 100), num(P0 + P0 * p_ // 100), num(int(round(float(Pf))) - 100)], "%s · %s%s ≈ <b>%s</b>." % (num(P0), d(F(100 - p_, 100)), "<sup>%d</sup>" % y if y > 1 else "", num(int(round(float(Pf))))))
    if t == "oferta":
        pr = R.choice([3, 4, 6, 8])
        return M("Oferta: «3 × 2» (te llevas 3 y pagas 2). ¿Qué porcentaje de descuento es, más o menos?", "33 %", ["50 %", "30 %", "66 %"], "Pagas 2 de 3: ahorras 1/3 ≈ <b>33 %</b>.") if pr == 3 else \
            M("Oferta: «2.ª unidad al 50 %». Si compras dos unidades, ¿qué descuento total tienes?", "25 %", ["50 %", "75 %", "20 %"], "Pagas 1,5 de 2 unidades: ahorras 0,5/2 = <b>25 %</b>.")
    C = R.choice([600, 900, 1200, 1500])
    m = R.choice([6, 10, 12])
    return M("%s compra un móvil de %s € en %d cuotas sin intereses. Si paga una entrada del 20 %%, ¿cuánto es cada cuota?" % (p, num(C), m), euros(F(C * 80, 100 * m)), [euros(F(C, m)), euros(F(C * 20, 100 * m)), euros(F(C * 80, 100 * (m - 1)))],
             "Entrada %s; queda %s; %s : %d = <b>%s</b>." % (euros(F(C * 20, 100)), euros(F(C * 80, 100)), euros(F(C * 80, 100)), m, euros(F(C * 80, 100 * m))))


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(48004 + (lv - 2) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 2:
        sets = [("Porcentajes de una cantidad", mix(R, seen, [(s_basico, 20)])), ("Aumentos y disminuciones", mix(R, seen, [(s_variacion, 20)])), ("Precio antes y después", mix(R, seen, [(s_variacion, 20)])),
                ("Interés simple", mix(R, seen, [(s_interes, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Para calcular un porcentaje: cantidad · p / 100. Para hallar el total: parte · 100 / p.",
                 "<b>Índice de variación</b>: subir un 15 % es multiplicar por 1,15; bajar un 15 % es multiplicar por 0,85.",
                 "<b>Interés simple</b>: I = C · r · t / 100 (el capital no cambia de un año a otro)."]
        slug, title, short, kb, ks, sort = "porcentajes", "Porcentajes, aumentos e interés simple", "Porcentajes", "Subir un 15 %: multiplica por 1,15", "Bajar un 15 %: multiplica por 0,85.", 4
        meta = "Fichas de matemáticas de 2.º de ESO: porcentajes, índice de variación, aumentos y rebajas, IVA, precio original e interés simple. 100 ejercicios con soluciones."
        std = "Porcentajes; aumentos y disminuciones porcentuales; índice de variación; interés simple; problemas de consumo"
    else:
        sets = [("Índice de variación", mix(R, seen, [(s_basico, 20)])), ("Variaciones encadenadas", mix(R, seen, [(s_variacion, 20)])), ("Interés simple y compuesto", mix(R, seen, [(s_interes, 20)])),
                ("Interés compuesto", mix(R, seen, [(s_interes, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Variaciones encadenadas: se multiplican los índices. Subir un 20 % y bajar un 20 % da 1,2 · 0,8 = 0,96, es decir, baja un 4 %.",
                 "<b>Interés compuesto</b>: los intereses se suman al capital cada año. C<sub>f</sub> = C · (1 + r/100)<sup>t</sup>.",
                 "Para hallar el precio original, se divide entre el índice de variación."]
        slug, title, short, kb, ks, sort = "porcentajes-e-interes-compuesto", "Porcentajes e interés compuesto", "Porcentajes e interés", "C · (1 + r/100)ᵗ", "Interés compuesto: capital final.", 10
        meta = "Fichas de matemáticas de 4.º de ESO: índices de variación, porcentajes encadenados, interés simple y compuesto y problemas financieros. 100 ejercicios con soluciones."
        std = "Porcentajes encadenados; interés simple y compuesto; matemática financiera en contextos cotidianos"
    ex = [("80 € con rebaja del 15 %", ["80 · 0,85"], "68 €"), ("Tras subir un 10 % cuesta 66 €. ¿Y antes?", ["66 : 1,10"], "60 €")]
    mist = [["Sumar porcentajes encadenados", "Subir 10 % y bajar 10 % no deja igual: 1,1 · 0,9 = 0,99."], ["Restar el porcentaje al precio final para volver atrás", "Divide entre el índice."], ["Confundir interés simple y compuesto", "En el compuesto los intereses también generan intereses."]]
    body = L(think, ex, mist)
    faq = [("¿Qué es el índice de variación?", "El número por el que se multiplica una cantidad al aumentarla o disminuirla un porcentaje: +12 % → 1,12; −12 % → 0,88."),
           ("¿Qué diferencia hay entre interés simple y compuesto?", "En el simple, los intereses se calculan siempre sobre el capital inicial; en el compuesto, sobre el capital acumulado.")]
    unit(lv, R, slug, "N", std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(2)
