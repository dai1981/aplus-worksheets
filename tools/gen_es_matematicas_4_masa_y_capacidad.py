# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Masa y capacidad (Sentido de la medida)
El kilogramo, el gramo y la tonelada; medio kilo y cuarto de kilo; el litro, el decilitro, el centilitro y el mililitro;
medio litro y cuarto de litro; pasar de una unidad a otra; elegir la unidad adecuada; leer básculas y jarras; problemas.
Errores: pensar que 1 kg = 100 g, confundir masa y capacidad, sumar gramos y kilos sin pasar a la misma unidad.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, dz, bank, POR, DIV, Kids
import es_medida as M
import fr_common as _F

R = random.Random(44015)
K = Kids(R)

PM = [("kg", "g"), ("g", "mg"), ("kg", "dag"), ("kg", "hg"), ("hg", "g"), ("dag", "g")]
PC = [("L", "mL"), ("L", "cL"), ("L", "dL"), ("dL", "mL"), ("cL", "mL"), ("kL", "L"), ("hL", "L"), ("daL", "L")]


def s1_masa():
    k = R.choice(["conv", "conv", "up", "t", "fr"])
    if k == "conv":
        return M.conv(R, M.MAS, PM)
    if k == "up":
        return M.conv(R, M.MAS, [(b, a) for a, b in PM])
    if k == "t":
        t = R.randint(2, 40)
        if R.random() < 0.5:
            return mcq("¿Cuántos kilos son %d toneladas?" % t, "%s kg" % num(t * 1000), ["%s kg" % num(t * 100), "%s kg" % num(t * 10), "%s kg" % num(t * 10000)], "1 t = 1000 kg: <b>%s kg</b>." % num(t * 1000))
        return mcq("¿Cuántas toneladas son %s kg?" % num(t * 1000), "%d t" % t, ["%d t" % (t * 10), "%s t" % num(t * 100), "%s t" % num(t * 1000)], "1000 kg = 1 t: <b>%d t</b>." % t)
    return bank(R, [
        ("¿Cuántos gramos son medio kilo?", "500 g", ["50 g", "250 g", "5000 g"]),
        ("¿Cuántos gramos son un cuarto de kilo?", "250 g", ["25 g", "400 g", "500 g"]),
        ("¿Cuántos gramos son tres cuartos de kilo?", "750 g", ["75 g", "340 g", "300 g"]),
        ("¿Cuántos gramos son un kilo y medio?", "1500 g", ["150 g", "1050 g", "1005 g"]),
        ("¿Cuántos cuartos de kilo hay en un kilo?", "4", ["2", "10", "100"]),
        ("¿Cuántos gramos son 2 kg y 300 g?", "2300 g", ["230 g", "2030 g", "5 g"]),
    ], "fr")()


def s2_cap():
    k = R.choice(["conv", "conv", "up", "fr"])
    if k == "conv":
        return M.conv(R, M.CAP, PC)
    if k == "up":
        return M.conv(R, M.CAP, [(b, a) for a, b in PC])
    return bank(R, [
        ("¿Cuántos mililitros son medio litro?", "500 mL", ["50 mL", "250 mL", "5000 mL"]),
        ("¿Cuántos mililitros son un cuarto de litro?", "250 mL", ["25 mL", "400 mL", "500 mL"]),
        ("Una lata tiene 33 cL. ¿Cuántos mililitros son?", "330 mL", ["33 mL", "3300 mL", "3,3 mL"]),
        ("¿Cuántas botellas de medio litro se llenan con 3 litros?", "6", ["3", "5", "15"]),
        ("¿Cuántos vasos de un cuarto de litro se llenan con 2 litros?", "8", ["4", "2", "6"]),
        ("¿Cuántos mililitros son un litro y medio?", "1500 mL", ["150 mL", "1050 mL", "15 mL"]),
    ], "frc")()


def bascula(g):
    """báscula de aguja de 0 a 1000 g"""
    import math
    cx, cy, r = 110, 110, 86
    s = ["<circle cx='%d' cy='%d' r='%d' fill='#fff' stroke='#333' stroke-width='3'/>" % (cx, cy, r)]
    for i in range(0, 41):
        a = math.radians(-90 + i * 9)
        r1 = r - (14 if i % 4 == 0 else 7)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#333' stroke-width='%s'/>" % (cx + r * math.cos(a), cy + r * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a), "2" if i % 4 == 0 else "1"))
        if i % 4 == 0 and i < 40:
            s.append("<text x='%.1f' y='%.1f' font-size='12' text-anchor='middle' fill='#333'>%d</text>" % (cx + (r - 28) * math.cos(a), cy + (r - 28) * math.sin(a) + 4, i * 25))
    a = math.radians(-90 + g / 25.0 * 9)
    s.append("<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='#c0392b' stroke-width='3'/>" % (cx, cy, cx + (r - 18) * math.cos(a), cy + (r - 18) * math.sin(a)))
    s.append("<circle cx='%d' cy='%d' r='5' fill='#c0392b'/>" % (cx, cy))
    s.append("<text x='%d' y='%d' font-size='12' text-anchor='middle' fill='#333'>gramos</text>" % (cx, cy + 34))
    return "<div class='fig'><svg viewBox='0 0 220 220' width='220' role='img' aria-label='báscula'>%s</svg></div>" % "".join(s)


def jarra(ml, top=1000):
    s = ["<path d='M40 20 L40 200 L140 200 L140 20' fill='none' stroke='#333' stroke-width='3'/>"]
    h = 180.0 * ml / top
    s.append("<rect x='42' y='%.1f' width='96' height='%.1f' fill='#9fd3f0'/>" % (200 - h, h - 1))
    for v in range(0, top + 1, 100):
        y = 200 - 180.0 * v / top
        s.append("<line x1='140' y1='%.1f' x2='%d' y2='%.1f' stroke='#333' stroke-width='%s'/>" % (y, 158 if v % 500 == 0 else 150, y, "2" if v % 500 == 0 else "1"))
        if v % 200 == 0 or v in (100,):
            s.append("<text x='164' y='%.1f' font-size='12' fill='#333'>%d mL</text>" % (y + 4, v))
    return "<div class='fig'><svg viewBox='0 0 240 215' width='240' role='img' aria-label='jarra medidora'>%s</svg></div>" % "".join(s)


def s3_leer():
    k = R.choice(["bas", "jarra"])
    if k == "bas":
        g = R.randint(1, 39) * 25
        return mcq(bascula(g) + "¿Cuántos gramos marca la báscula?", "%d g" % g, ["%d g" % (g + 25), "%d g" % (g - 25) if g > 25 else "%d g" % (g + 50), "%d g" % (g + 100) if g + 100 < 1000 else "%d g" % (g - 100), "%d kg" % g],
                   "Cada marca pequeña son 25 g: <b>%d g</b>." % g)
    m = R.randint(1, 9) * 100 + R.choice([0, 0, 50])
    return mcq(jarra(m) + "¿Cuánta agua hay en la jarra?", "%d mL" % m, ["%d mL" % (m + 100), "%d mL" % (m - 100) if m > 100 else "%d mL" % (m + 200), "%d L" % m, "%d mL" % (m + 50)],
               "El agua llega a <b>%d mL</b>." % m)


def s4_unidad():
    return bank(R, [
        ("¿Qué unidad usarías para medir la masa de un camión?", "toneladas", ["gramos", "miligramos", "litros"]),
        ("¿Qué unidad usarías para medir la masa de una manzana?", "gramos", ["toneladas", "kilolitros", "metros"]),
        ("¿Qué unidad usarías para medir el agua de una piscina?", "kilolitros", ["mililitros", "gramos", "centilitros"]),
        ("¿Qué unidad usarías para medir el jarabe de una cucharilla?", "mililitros", ["litros", "kilogramos", "kilolitros"]),
        ("¿Cuánto puede pesar un niño de 4.º de Primaria?", "30 kg", ["30 g", "3 t", "300 kg"]),
        ("¿Cuánto puede pesar una hoja de papel?", "5 g", ["5 kg", "50 kg", "5 t"]),
        ("¿Cuánta agua cabe en un cubo de fregar?", "10 L", ["10 mL", "100 L", "1 mL"]),
        ("¿Cuánta leche cabe en un vaso?", "250 mL", ["25 L", "2 mL", "250 L"]),
        ("¿Cuánto puede pesar un elefante?", "5 t", ["5 kg", "50 g", "500 g"]),
        ("¿Qué se mide en litros?", "la capacidad de una botella", ["la masa de una piedra", "el largo de una mesa", "la hora del recreo"]),
        ("¿Qué se mide en kilogramos?", "la masa de un saco de patatas", ["el agua de un vaso", "la altura de un árbol", "la duración de una película"]),
        ("¿Cuánto zumo cabe en un brik pequeño?", "200 mL", ["200 L", "2 mL", "20 L"]),
        ("¿Cuánto puede pesar una bicicleta?", "12 kg", ["12 g", "12 t", "120 kg"]),
        ("¿Qué instrumento sirve para medir la masa?", "la báscula", ["la regla", "el reloj", "la jarra medidora"]),
    ], "unidad")()


def s5_problema():
    p, g = K.next()
    k = R.choice(["compra", "botellas", "bidon", "harina", "camion", "jarabe", "vasos"])
    if k == "compra":
        a, b = R.randint(1, 3), R.choice([250, 500, 750])
        c = R.choice([200, 300, 400, 150])
        t = a * 1000 + b + c
        return mcq("%s compra %d kg y %d g de patatas y %d g de queso. ¿Cuántos gramos lleva en total?" % (p, a, b, c), "%s g" % num(t), ["%s g" % num(a + b + c), "%s g" % num(a * 100 + b + c), "%s g" % num(t + 1000), "%s g" % num(a * 1000 + b)],
                   "%d kg = %s g; %s + %d + %d = <b>%s g</b>." % (a, num(a * 1000), num(a * 1000), b, c, num(t)))
    if k == "botellas":
        v, n = R.choice([(250, 4), (250, 8), (250, 12), (500, 6), (500, 4), (200, 10), (250, 24), (500, 12), (200, 15)])
        t = v * n
        return mcq("Una caja tiene %d botellas de %d mL. ¿Cuántos litros hay en total?" % (n, v), "%d L" % (t // 1000),
                   ["%s L" % num(t), "%s L" % num(t // 100), "%d L" % (t // 1000 + 1), "%d L" % (n + v // 100)],
                   "%d %s %d = %s mL = <b>%d L</b>." % (v, POR, n, num(t), t // 1000))
    if k == "bidon":
        t = R.choice([5, 8, 10, 20])
        v = R.choice([250, 500])
        return mcq("¿Cuántos vasos de %d mL se pueden llenar con un bidón de %d L?" % (v, t), str(t * 1000 // v), [str(t * 100 // v) if t * 100 // v else str(t * 1000 // v + 1), str(t * v), str(t * 1000 // v * 10), str(t * 2)],
                   "%d L = %s mL; %s %s %d = <b>%d</b>." % (t, num(t * 1000), num(t * 1000), DIV, v, t * 1000 // v))
    if k == "harina":
        t = R.choice([1000, 2000])
        u = R.randint(2, 7) * 125
        return mcq("Para un bizcocho, %s usa %d g de harina de un paquete de %d kg. ¿Cuántos gramos quedan en el paquete?" % (p, u, t // 1000), "%s g" % num(t - u), ["%s g" % num(t // 1000 * 100 - u) if t // 1000 * 100 > u else "%s g" % num(t + u), "%s g" % num(u), "%s g" % num(t - u + 100), "%s g" % num(t - u - 100)],
                   "%d kg = %s g; %s − %d = <b>%s g</b>." % (t // 1000, num(t), num(t), u, num(t - u)))
    if k == "camion":
        n = R.randint(20, 80)
        m = R.choice([25, 50])
        return mcq("Un camión lleva %d sacos de %d kg. ¿Cuántos kilos lleva? ¿Son más o menos de 1 tonelada?" % (n, m), "%s kg, %s de 1 t" % (num(n * m), "más" if n * m > 1000 else "menos" if n * m < 1000 else "igual"),
                   ["%s kg, %s de 1 t" % (num(n * m), "menos" if n * m > 1000 else "más"), "%s kg, %s de 1 t" % (num(n + m), "menos"), "%s kg, %s de 1 t" % (num(n * m * 10), "más")],
                   "%d %s %d = %s kg; 1 t = 1000 kg." % (n, POR, m, num(n * m))) if n * m != 1000 else None
    if k == "jarabe":
        d = R.choice([5, 10])
        v = R.choice([100, 150, 200, 250])
        return mcq("Un frasco tiene %d mL de jarabe. Cada toma es de %d mL. ¿Cuántas tomas hay en el frasco?" % (v, d), str(v // d), [str(v * d), str(v // d + d), str(v // 10) if d == 5 else str(v // 5), str(v - d)],
                   "%d %s %d = <b>%d</b>." % (v, DIV, d, v // d))
    a = R.randint(2, 6)
    b = R.choice([250, 500, 750])
    q = R.choice([250, 500, 750, 1250])
    t = a * 1000 + b
    if q >= t:
        return None
    return mcq("Una olla tiene %d L y %d mL de caldo. Se sirven %d mL. ¿Cuánto caldo queda?" % (a, b, q), "%s mL" % num(t - q), ["%s mL" % num(t + q), "%s mL" % num(a + b - q) if a + b > q else "%s mL" % num(t - q + 1000), "%s mL" % num(t - q - 100), "%s mL" % num(a * 100 + b - q) if a * 100 + b > q else "%s mL" % num(t - q + 100)],
               "%d L y %d mL = %s mL; %s − %d = <b>%s mL</b>." % (a, b, num(t), num(t), q, num(t - q)))


def main():
    seen = set()
    sets = [
        ("Unidades de masa", mix(R, seen, [(s1_masa, 20)])),
        ("Unidades de capacidad", mix(R, seen, [(s2_cap, 20)])),
        ("Leer básculas y jarras", mix(R, seen, [(s3_leer, 20)])),
        ("Elegir la unidad adecuada", mix(R, seen, [(s4_unidad, 14), (s1_masa, 3), (s2_cap, 3)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["La <b>masa</b> se mide en kilogramos (kg) y gramos (g): 1 kg = 1000 g. Para masas muy grandes se usa la <b>tonelada</b>: 1 t = 1000 kg.",
         "La <b>capacidad</b> se mide en litros (L), decilitros (dL), centilitros (cL) y mililitros (mL): 1 L = 10 dL = 100 cL = 1000 mL.",
         "Medio kilo = 500 g y un cuarto de kilo = 250 g. Medio litro = 500 mL y un cuarto de litro = 250 mL.",
         "Para sumar o restar medidas, pásalas antes a la <b>misma unidad</b>."],
        [("¿Cuántos gramos son 2 kg y 350 g?", ["2 kg = 2000 g", "2000 + 350"], "2350 g"),
         ("¿Cuántos vasos de 250 mL llenas con 2 L?", ["2 L = 2000 mL", "2000 : 250"], "8 vasos")],
        [["Pensar que 1 kg = 100 g", "1 kg = 1000 g y 1 L = 1000 mL."],
         ["Confundir masa y capacidad", "La masa (kg, g) dice cuánto pesa; la capacidad (L, mL), cuánto cabe."],
         ["Sumar unidades distintas", "2 kg + 300 g no es 302: es 2300 g."]],
        _F.table(["", "Masa", "Capacidad"], [["Unidad principal", "kilogramo (kg) y gramo (g)", "litro (L)"], ["Equivalencias", "1 t = 1000 kg; 1 kg = 1000 g", "1 L = 10 dL = 100 cL = 1000 mL"]]))
    faq = [("¿Cuántos gramos tiene un kilo?", "Un kilogramo tiene 1000 gramos. Medio kilo son 500 g y un cuarto de kilo, 250 g."),
           ("¿Cuántos mililitros tiene un litro?", "Un litro tiene 1000 mililitros, 100 centilitros y 10 decilitros.")]
    make_unit(R, "masa-y-capacidad", "M",
              "Unidades del Sistema Métrico Decimal de masa y capacidad: equivalencias y conversiones; medición con instrumentos; estimación; resolución de problemas",
              "Masa y capacidad", "Masa y capacidad",
              "Fichas de matemáticas de 4.º de Primaria: kilogramos, gramos y toneladas, litros, centilitros y mililitros, medio y cuarto, básculas y jarras, y problemas. 100 ejercicios con soluciones.",
              "1 kg = 1000 g y 1 L = 1000 mL", "Pasa las medidas a la misma unidad antes de sumar o restar.",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
