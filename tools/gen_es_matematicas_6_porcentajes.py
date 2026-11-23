# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Porcentajes (Sentido numérico)
Qué es un porcentaje (de cada 100), porcentaje, fracción y decimal (50 % = 1/2 = 0,5), calcular el porcentaje de una cantidad,
descuentos y aumentos (rebajas, IVA), qué porcentaje representa una parte; 5.º con porcentajes sencillos (10 %, 25 %, 50 %, 75 %).
Errores: restar el porcentaje como si fueran euros (20 % de 80 € no son 20 €), confundir el descuento con el precio final.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d, fr, fq

R = None
LV = 6
EASY = [10, 20, 25, 50, 75]


def P():
    return R.choice(EASY) if LV == 5 else R.choice(EASY + [5, 15, 30, 40, 60, 12, 35, 80, 90])


def pc(p):
    return "%s %%" % d(F(p))


def s1_concepto():
    p = R.randint(1, 99)
    k = R.choice(["cuadros", "fr", "dec", "frac2"])
    if k == "cuadros":
        s = []
        for i in range(100):
            x, y = 6 + (i % 10) * 16, 6 + (i // 10) * 16
            s.append("<rect x='%d' y='%d' width='15' height='15' fill='%s' stroke='#555' stroke-width='0.6'/>" % (x, y, "#2e7d32" if i < p else "#fff"))
        pic = "<div class='fig'><svg viewBox='0 0 172 172' width='172' role='img' aria-label='cuadrícula de 100 casillas'>%s</svg></div>" % "".join(s)
        return M(pic + "¿Qué porcentaje de la cuadrícula está coloreado?", pc(p), [pc(100 - p), pc(p + 10) if p < 90 else pc(p - 10), pc(p // 10) if p >= 10 else pc(p + 5)], "%d de 100 casillas: <b>%s</b>." % (p, pc(p)))
    q = R.choice([10, 20, 25, 50, 75, 5, 40, 60, 80, 30, 90])
    f = F(q, 100)
    if k == "fr":
        return M("¿Qué fracción es igual a %s?" % pc(q), fq(f), [fr(1, q) if q < 50 else fr(q, 10), fr(q, 10), fq(F(100 - q, 100)) if q != 50 else fr(1, 4)], "%s = %s = <b>%s</b>." % (pc(q), fr(q, 100), fq(f)))
    if k == "dec":
        return M("¿Qué número decimal es %s?" % pc(q), d(f), [str(q), d(F(q, 10)), d(F(q, 1000))], "%s = %s = <b>%s</b>." % (pc(q), fr(q, 100), d(f)))
    return M("¿Qué porcentaje es %s?" % fq(f), pc(q), [pc(f.denominator), pc(f.numerator * 10), pc(100 - q)], "%s = %s = <b>%s</b>." % (fq(f), fr(q, 100), pc(q)))


def s2_calcular():
    p = P()
    t = R.choice([20, 40, 60, 80, 120, 200, 240, 300, 360, 400, 500, 600, 800, 1000, 1200])
    r = F(p * t, 100)
    if r.denominator != 1:
        return None
    r = int(r)
    return M("Calcula el %s de %s." % (pc(p), num(t)), num(r), [num(p), num(t - r), num(r * 10), num(t // p) if t % p == 0 and t // p != r else num(r + p)],
             "%s de %s = %s × %d : 100 = <b>%s</b>." % (pc(p), num(t), num(t), p, num(r)))


def s3_descuento():
    k = R.choice(["rebaja", "rebaja", "final", "subida"] if LV == 6 else ["rebaja", "final"])
    p = P()
    t = R.choice([20, 40, 50, 60, 80, 100, 120, 150, 200, 240, 300, 400, 500])
    r = F(p * t, 100)
    if r.denominator != 1:
        return None
    r = int(r)
    if k == "rebaja":
        return M("Unas zapatillas cuestan %d € y tienen un %s de descuento. ¿Cuántos euros te descuentan?" % (t, pc(p)), "%d €" % r, ["%d €" % p, "%d €" % (t - r), "%d €" % (r * 2), "%d €" % (r + 10)],
                 "%s de %d = <b>%d €</b>." % (pc(p), t, r))
    if k == "final":
        return M("Una mochila cuesta %d €. En rebajas tiene un %s de descuento. ¿Cuánto cuesta ahora?" % (t, pc(p)), "%d €" % (t - r), ["%d €" % r, "%d €" % (t - p), "%d €" % (t + r), "%d €" % (t - r + 10)],
                 "Descuento: %d €. Precio final: %d − %d = <b>%d €</b>." % (r, t, r, t - r))
    return M("Una entrada costaba %d € y sube un %s. ¿Cuánto cuesta ahora?" % (t, pc(p)), "%d €" % (t + r), ["%d €" % (t - r), "%d €" % (t + p), "%d €" % r, "%d €" % (t + r + 10)],
             "Sube %d €: %d + %d = <b>%d €</b>." % (r, t, r, t + r))


def s4_que_porcentaje():
    t = R.choice([20, 25, 50, 200, 40, 80, 500])
    p = P()
    pa = F(p * t, 100)
    if pa.denominator != 1:
        return None
    pa = int(pa)
    k = R.choice(["clase"] if t in (20, 25) else ["examen"] if t in (40, 50) else ["pelotas"])
    ctx = {"clase": "En una clase de %d alumnos, %d llevan gafas. ¿Qué porcentaje lleva gafas?", "examen": "En un examen de %d preguntas, Martina acierta %d. ¿Qué porcentaje ha acertado?",
           "pelotas": "En una caja hay %d pelotas y %d son rojas. ¿Qué porcentaje son rojas?"}[k]
    return M(ctx % (t, pa), pc(p), [pc(pa) if pa != p else pc(p + 5), pc(100 - p), pc(t - pa) if t - pa != p and t - pa <= 100 else pc(p * 2 if p <= 50 else p - 10)],
             "%s = %s = <b>%s</b>." % (fr(pa, t), fr(p, 100), pc(p)))


def s5_problema():
    k = R.choice(["iva", "votos", "ahorro", "grafico", "comparar"] if LV == 6 else ["votos", "ahorro", "comparar"])
    if k == "iva":
        t = R.choice([100, 200, 50, 300, 400])
        return M("Una bicicleta cuesta %d € sin IVA. El IVA es del 21 %%. ¿Cuánto cuesta con IVA?" % t, "%s €" % d(F(t * 121, 100)), ["%s €" % d(F(t * 21, 100)), "%d €" % (t + 21), "%s €" % d(F(t * 79, 100))],
                 "21 %% de %d = %s €; %d + %s = <b>%s €</b>." % (t, d(F(t * 21, 100)), t, d(F(t * 21, 100)), d(F(t * 121, 100))))
    if k == "votos":
        n = R.choice([200, 300, 400, 500, 600, 800, 1000])
        a, b = R.sample([20, 25, 30, 35, 40, 15, 45], 2)
        c = 100 - a - b
        if c <= 0:
            return None
        return M("En una votación del colegio, la opción A recibe el %d %% de los %d votos y la B, el %d %%. ¿Cuántos votos recibe la opción C (el resto)?" % (a, n, b), num(n * c // 100), [num(c), num(n * (a + b) // 100), num(n - c)],
                 "C: 100 − %d − %d = %d %%; %d %% de %d = <b>%s</b>." % (a, b, c, c, n, num(n * c // 100))) if n * c % 100 == 0 else None
    if k == "ahorro":
        t = R.choice([40, 60, 80, 100, 120, 200])
        p = R.choice([10, 25, 50, 20])
        return M("Lucía recibe %d € por su cumpleaños y ahorra el %d %%. ¿Cuánto ahorra?" % (t, p), "%d €" % (t * p // 100), ["%d €" % p, "%d €" % (t - t * p // 100), "%d €" % (t * p // 10)],
                 "%d %% de %d = <b>%d €</b>." % (p, t, t * p // 100)) if t * p % 100 == 0 else None
    if k == "grafico":
        p = R.choice([25, 50, 75])
        return M("En un gráfico de sectores, una parte ocupa un cuarto del círculo. ¿Qué porcentaje representa?" if p == 25 else "En un gráfico de sectores, una parte ocupa medio círculo. ¿Qué porcentaje representa?" if p == 50 else "En un gráfico de sectores, una parte ocupa tres cuartos del círculo. ¿Qué porcentaje representa?",
                 pc(p), [pc(x) for x in (25, 50, 75, 100, 4) if x != p], "<b>%s</b>." % pc(p))
    t1, t2 = R.sample([40, 50, 60, 80, 100], 2)
    p1, p2 = R.choice([(25, 20), (50, 25), (10, 20), (20, 25), (25, 50)])
    r1, r2 = t1 * p1 / 100.0, t2 * p2 / 100.0
    if r1 == r2 or t1 * p1 % 100 or t2 * p2 % 100:
        return None
    big = "la tienda A" if r1 > r2 else "la tienda B"
    return M("En la tienda A una camiseta de %d € tiene un %d %% de descuento. En la tienda B, otra de %d € tiene un %d %%. ¿Dónde te descuentan más euros?" % (t1, p1, t2, p2), "en %s" % big,
             ["en %s" % ("la tienda B" if big == "la tienda A" else "la tienda A"), "en las dos igual", "no se puede saber"], "A: %d €; B: %d € → <b>%s</b>." % (r1, r2, big))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40010 + lv * 1000)
    seen = set()
    sets = [
        ("Qué es un porcentaje", mix(R, seen, [(s1_concepto, 20)])),
        ("Calcular un porcentaje", mix(R, seen, [(s2_calcular, 20)])),
        ("Descuentos" + (" y aumentos" if lv == 6 else ""), mix(R, seen, [(s3_descuento, 20)])),
        ("¿Qué porcentaje es?", mix(R, seen, [(s4_que_porcentaje, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Un <b>porcentaje</b> indica cuántos de cada 100. 30 %% = %s = 0,3." % fr(30, 100),
         "Para calcular el 30 % de 80: 80 × 30 : 100 = 24. Atajos: 50 % es la mitad; 25 %, la cuarta parte; 10 %, la décima parte.",
         "Con un <b>descuento</b>, el precio final es el precio menos el descuento. Con un aumento, se suma."],
        [("25 % de 60 €", ["25 % es la cuarta parte", "60 : 4"], "15 €"),
         ("Una chaqueta de 80 € con un 20 % de descuento", ["20 % de 80 = 16 €", "80 − 16"], "64 €")],
        [["Tratar el % como euros", "20 % de 80 € son 16 €, no 20 €."],
         ["Confundir descuento y precio final", "Lee bien la pregunta: ¿cuánto te descuentan o cuánto pagas?"],
         ["Pensar que 25 %% = %s" % fr(1, 25), "25 %% = %s = %s." % (fr(25, 100), fr(1, 4))]])
    faq = [("¿Cómo se calcula un porcentaje de una cantidad?", "Se multiplica la cantidad por el porcentaje y se divide entre 100. El 15 % de 200 es 200 × 15 : 100 = 30."),
           ("¿Qué relación hay entre porcentajes y fracciones?", "Un porcentaje es una fracción con denominador 100: 50 % = 1/2, 25 % = 1/4, 75 % = 3/4 y 10 % = 1/10.")]
    make_unit(R, "porcentajes", "N",
              "Porcentajes: significado, relación con fracciones y decimales, cálculo del porcentaje de una cantidad, aumentos y disminuciones porcentuales en situaciones de consumo",
              "Porcentajes", "Porcentajes",
              "Fichas de matemáticas de %d.º de Primaria: qué es un porcentaje, porcentajes, fracciones y decimales, calcular el porcentaje de una cantidad, descuentos y problemas. 100 ejercicios con soluciones." % lv,
              "Porcentaje: de cada 100", "50 % = mitad; 25 % = cuarta parte.",
              body, faq, sets, 10, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
