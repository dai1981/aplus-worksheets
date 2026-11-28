# -*- coding: utf-8 -*-
"""España / Física y Química: 2.º de ESO"""
from es_sci import H, nq, num, it

D = "¿Qué corresponde a esta descripción: {v}?"


def f_unid(R):
    k = R.choice(["km", "cm", "g", "min", "L", "kmh", "h"])
    if k == "km":
        x = R.choice([2.5, 3.2, 0.75, 12, 1.8, 0.4, 7.5])
        return nq("Expresa %s km en metros." % num(x), x * 1000, [x * 100, x / 1000, x * 10], "m", "1 km = 1000 m: %s · 1000 = %s m." % (num(x), num(x * 1000)))
    if k == "cm":
        x = R.choice([250, 75, 1500, 32, 480, 6])
        return nq("Expresa %s cm en metros." % num(x), x / 100, [x * 100, x / 10, x / 1000], "m", "1 m = 100 cm: %s : 100 = %s m." % (num(x), num(x / 100)))
    if k == "g":
        x = R.choice([3.5, 0.25, 12, 0.08, 1.2, 45])
        return nq("Expresa %s kg en gramos." % num(x), x * 1000, [x * 100, x / 1000, x * 10], "g", "1 kg = 1000 g: %s · 1000 = %s g." % (num(x), num(x * 1000)))
    if k == "min":
        x = R.choice([2.5, 15, 0.5, 4, 12, 1.5])
        return nq("Expresa %s minutos en segundos." % num(x), x * 60, [x * 100, x / 60, x * 3600], "s", "1 min = 60 s: %s · 60 = %s s." % (num(x), num(x * 60)))
    if k == "L":
        x = R.choice([1.5, 0.33, 2, 0.75, 5, 0.2])
        return nq("Expresa %s L en mililitros." % num(x), x * 1000, [x * 100, x / 1000, x * 10], "mL", "1 L = 1000 mL: %s · 1000 = %s mL." % (num(x), num(x * 1000)))
    if k == "kmh":
        x = R.choice([36, 72, 108, 90, 54, 18, 120])
        return nq("Expresa %s km/h en m/s." % num(x), x / 3.6, [x * 3.6, x / 60, x * 1000 / 60], "m/s", "Se divide entre 3,6: %s : 3,6 = %s m/s." % (num(x), num(x / 3.6)))
    x = R.choice([2, 1.5, 0.5, 3, 0.25, 4])
    return nq("Expresa %s h en segundos." % num(x), x * 3600, [x * 60, x * 360, x * 100], "s", "1 h = 3600 s: %s · 3600 = %s s." % (num(x), num(x * 3600)))


def f_dens(R):
    k = R.choice(["d", "d", "m", "V", "kgm3"])
    if k == "d":
        m, V = R.choice([(540, 200), (79, 10), (226, 20), (89, 10), (19.3, 1), (46, 50), (136, 10), (27, 10), (12, 15)])
        return nq("Un trozo de material de %s g ocupa %s cm³. ¿Cuál es su densidad?" % (num(m), num(V)), m / V, [m * V, V / m, m - V], "g/cm³",
                  "d = m : V = %s g : %s cm³ = %s g/cm³." % (num(m), num(V), num(m / V)))
    if k == "m":
        d, V = R.choice([(2.7, 20), (7.9, 5), (0.8, 250), (13.6, 10), (1.03, 1000), (0.92, 50)])
        return nq("La densidad de una sustancia es %s g/cm³. ¿Qué masa tienen %s cm³?" % (num(d), num(V)), d * V, [d / V, V / d, d + V], "g",
                  "m = d · V = %s · %s = %s g." % (num(d), num(V), num(d * V)))
    if k == "V":
        d, m = R.choice([(2.7, 54), (7.9, 158), (0.8, 40), (13.6, 68), (11.3, 113), (0.9, 18)])
        return nq("¿Qué volumen ocupan %s g de una sustancia de densidad %s g/cm³?" % (num(m), num(d)), m / d, [m * d, d / m, m - d], "cm³",
                  "V = m : d = %s : %s = %s cm³." % (num(m), num(d), num(m / d)))
    d = R.choice([2.7, 7.9, 1.0, 0.8, 13.6, 0.92, 1.26])
    return nq("Expresa una densidad de %s g/cm³ en kg/m³." % num(d), d * 1000, [d / 1000, d * 100, d * 10], "kg/m³", "1 g/cm³ = 1000 kg/m³: %s · 1000 = %s kg/m³." % (num(d), num(d * 1000)))


def f_conc(R):
    k = R.choice(["c", "c", "m", "V", "pct"])
    if k == "c":
        m, V = R.choice([(20, 0.5), (15, 0.25), (6, 0.2), (40, 2), (9, 0.3), (2.5, 0.1), (30, 1.5)])
        return nq("Se disuelven %s g de sal en agua hasta tener %s L de disolución. ¿Cuál es la concentración en g/L?" % (num(m), num(V)), m / V, [m * V, V / m, m / V / 1000], "g/L",
                  "c = m(soluto) : V(disolución) = %s : %s = %s g/L." % (num(m), num(V), num(m / V)))
    if k == "m":
        c, V = R.choice([(40, 0.5), (12, 2), (25, 0.2), (80, 0.25), (5, 3), (150, 0.1)])
        return nq("Una disolución tiene %s g/L. ¿Cuántos gramos de soluto hay en %s L?" % (num(c), num(V)), c * V, [c / V, V / c, c + V], "g",
                  "m = c · V = %s · %s = %s g." % (num(c), num(V), num(c * V)))
    if k == "V":
        c, m = R.choice([(20, 5), (50, 10), (8, 2), (100, 25), (40, 6), (30, 12)])
        return nq("Necesitas %s g de soluto de una disolución de %s g/L. ¿Qué volumen tomas?" % (num(m), num(c)), m / c, [m * c, c / m, m / c * 1000], "L",
                  "V = m : c = %s : %s = %s L." % (num(m), num(c), num(m / c)))
    ms, mw = R.choice([(10, 90), (5, 95), (20, 180), (25, 75), (3, 97), (15, 135), (8, 192)])
    p = ms / (ms + mw) * 100
    return nq("Se disuelven %s g de azúcar en %s g de agua. ¿Cuál es el porcentaje en masa de azúcar?" % (ms, mw), p, [ms / mw * 100, ms + mw, mw / (ms + mw) * 100], "%",
              "%% = %s : (%s + %s) · 100 = %s %%." % (ms, ms, mw, num(p)))


def f_masa(R):
    k = R.choice(["prod", "react", "gas", "lavoisier"])
    if k == "prod":
        a, b = R.choice([(56, 32), (24, 16), (12, 32), (4, 32), (65, 16), (27, 24)])
        return nq("Reaccionan completamente %s g de un reactivo con %s g de otro. ¿Qué masa de productos se obtiene?" % (a, b), a + b, [a - b, a * b, abs(a - b) / 2 + a], "g",
                  "Ley de Lavoisier: la masa se conserva, %s + %s = %s g." % (a, b, a + b))
    if k == "react":
        a, p = R.choice([(56, 88), (12, 44), (4, 36), (24, 40), (32, 64), (2, 18)])
        return nq("Con %s g de un reactivo y cierta masa de oxígeno se obtienen %s g de producto. ¿Cuánto oxígeno ha reaccionado?" % (a, p), p - a, [p + a, p, a], "g",
                  "Masa de oxígeno = %s − %s = %s g." % (p, a, p - a))
    if k == "gas":
        m0, m1 = R.choice([(250, 238), (120, 115.6), (300, 289), (80, 76.4), (500, 478)])
        return nq("En un vaso abierto, una pastilla efervescente con agua pasa de %s g a %s g. ¿Qué masa de gas escapó?" % (num(m0), num(m1)), m0 - m1, [m0 + m1, m1, (m0 - m1) * 10], "g",
                  "La masa no desaparece: %s − %s = %s g de CO₂ salen al aire." % (num(m0), num(m1), num(m0 - m1)))
    m = R.choice([10, 25, 40, 7, 100])
    return nq("Se queman %s g de magnesio y se forman %s g de óxido. Si quemas el doble de magnesio, ¿cuánto óxido obtienes?" % (num(m * 0.6), num(m)), 2 * m, [m, m * 0.6, m + 2], "g",
              "Las masas son proporcionales (ley de Proust): el doble de reactivo da el doble de producto, %s g." % num(2 * m))


def f_mov(R):
    k = R.choice(["v", "d", "t", "a", "vf"])
    if k == "v":
        d, t = R.choice([(100, 10), (400, 50), (1500, 300), (42000, 7200), (60, 8), (200, 25)])
        return nq("Un corredor recorre %s m en %s s. ¿Cuál es su velocidad media?" % (num(d), num(t)), d / t, [d * t, t / d, d - t], "m/s",
                  "v = d : t = %s : %s = %s m/s." % (num(d), num(t), num(d / t)))
    if k == "d":
        v, t = R.choice([(25, 40), (340, 3), (15, 120), (8, 45), (30, 20), (12, 15)])
        return nq("Un móvil va a %s m/s durante %s s con MRU. ¿Qué distancia recorre?" % (v, t), v * t, [v / t, v + t, t / v], "m", "d = v · t = %s · %s = %s m." % (v, t, num(v * t)))
    if k == "t":
        d, v = R.choice([(300, 15), (1200, 40), (90, 6), (2000, 25), (500, 20), (150, 3)])
        return nq("¿Cuánto tarda en recorrer %s m un móvil que va a %s m/s?" % (num(d), v), d / v, [d * v, v / d, d - v], "s", "t = d : v = %s : %s = %s s." % (num(d), v, num(d / v)))
    if k == "a":
        v0, v, t = R.choice([(0, 20, 5), (10, 30, 4), (0, 27, 9), (5, 25, 10), (0, 12, 3), (20, 0, 4)])
        a = (v - v0) / t
        return nq("Un coche pasa de %s m/s a %s m/s en %s s. ¿Cuál es su aceleración?" % (v0, v, t), a, [(v + v0) / t, (v - v0) * t, v / t if v0 else v * t], "m/s²",
                  "a = (v − v₀) : t = (%s − %s) : %s = %s m/s²." % (v, v0, t, num(a)), neg=True)
    v0, a, t = R.choice([(0, 2, 10), (5, 3, 4), (0, 9.8, 2), (10, 1.5, 6), (0, 4, 5)])
    return nq("Un móvil parte a %s m/s con una aceleración de %s m/s². ¿Qué velocidad tiene a los %s s?" % (v0, num(a), t), v0 + a * t, [a * t * t, v0 * t + a, (v0 + a) * t + 1], "m/s",
              "v = v₀ + a · t = %s + %s · %s = %s m/s." % (v0, num(a), t, num(v0 + a * t)))


def f_fuer(R):
    k = R.choice(["p", "p", "m", "hooke", "luna", "res"])
    if k == "p":
        m = R.choice([2, 5, 0.5, 60, 12, 0.25, 75])
        return nq("¿Cuánto pesa en la Tierra un cuerpo de %s kg? (g = 9,8 m/s²)" % num(m), m * 9.8, [m, m / 9.8, m * 10 * 10], "N", "P = m · g = %s · 9,8 = %s N." % (num(m), num(m * 9.8)))
    if k == "m":
        P = R.choice([98, 490, 19.6, 735, 4.9, 1960])
        return nq("Un cuerpo pesa %s N en la Tierra. ¿Cuál es su masa? (g = 9,8 m/s²)" % num(P), P / 9.8, [P * 9.8, P, P / 98], "kg", "m = P : g = %s : 9,8 = %s kg." % (num(P), num(P / 9.8)))
    if k == "hooke":
        kk, x = R.choice([(200, 0.05), (50, 0.1), (400, 0.02), (100, 0.15), (25, 0.2), (300, 0.04)])
        return nq("Un muelle de constante %s N/m se estira %s m. ¿Qué fuerza se aplica? (ley de Hooke)" % (kk, num(x)), kk * x, [kk / x, x / kk, kk + x], "N",
                  "F = k · Δx = %s · %s = %s N." % (kk, num(x), num(kk * x)))
    if k == "luna":
        m = R.choice([60, 30, 12, 90, 45])
        return nq("¿Cuánto pesa en la Luna una persona de %s kg? (g en la Luna = 1,6 m/s²)" % m, m * 1.6, [m * 9.8, m, m / 1.6], "N", "P = m · g = %s · 1,6 = %s N; su masa sigue siendo %s kg." % (m, num(m * 1.6), m))
    a, b = R.choice([(30, 20), (50, 15), (12, 8), (100, 60), (40, 25)])
    return nq("Dos personas empujan una caja en sentidos opuestos con %s N y %s N. ¿Cuál es la fuerza resultante?" % (a, b), a - b, [a + b, a * b, (a + b) / 2], "N",
              "Sentidos opuestos: se restan, %s − %s = %s N hacia el lado de la fuerza mayor." % (a, b, a - b))


def f_ener(R):
    k = R.choice(["ec", "ep", "ep", "kwh", "pot"])
    if k == "ec":
        m, v = R.choice([(2, 10), (1000, 20), (60, 5), (0.5, 4), (80, 3), (1500, 30)])
        return nq("Calcula la energía cinética de un cuerpo de %s kg que va a %s m/s." % (num(m), v), 0.5 * m * v * v, [m * v * v, m * v, 0.5 * m * v], "J",
                  "Ec = ½ · m · v² = 0,5 · %s · %s² = %s J." % (num(m), v, num(0.5 * m * v * v)))
    if k == "ep":
        m, h = R.choice([(2, 10), (50, 3), (0.5, 20), (70, 100), (10, 4), (5, 15)])
        return nq("Calcula la energía potencial de %s kg a %s m de altura. (g = 9,8 m/s²)" % (num(m), h), m * 9.8 * h, [m * h, m * 9.8, 0.5 * m * h * h], "J",
                  "Ep = m · g · h = %s · 9,8 · %s = %s J." % (num(m), h, num(m * 9.8 * h)))
    if k == "kwh":
        P, t = R.choice([(2, 3), (0.1, 5), (1.5, 2), (2.2, 0.5), (0.01, 10), (3, 4)])
        return nq("Un aparato de %s kW funciona %s h. ¿Cuánta energía consume?" % (num(P), num(t)), P * t, [P / t, P + t, P * t * 1000], "kWh",
                  "E = P · t = %s kW · %s h = %s kWh." % (num(P), num(t), num(P * t)))
    E, t = R.choice([(6000, 60), (1200, 10), (90000, 300), (500, 5), (36000, 120)])
    return nq("Un motor realiza %s J de trabajo en %s s. ¿Qué potencia desarrolla?" % (num(E), t), E / t, [E * t, t / E, E / t / 1000], "W",
              "P = W : t = %s : %s = %s W." % (num(E), t, num(E / t)))


def f_temp(R):
    k = R.choice(["CK", "KC", "q", "q", "C"])
    if k == "CK":
        c = R.choice([25, 100, -20, 37, 0, -196, 80])
        return nq("Expresa %s °C en kelvin." % num(c), c + 273, [c - 273, c * 273, c + 100], "K", "T(K) = T(°C) + 273 = %s + 273 = %s K." % (num(c), num(c + 273)), neg=True)
    if k == "KC":
        kk = R.choice([300, 373, 250, 310, 77, 400])
        return nq("Expresa %s K en grados Celsius." % kk, kk - 273, [kk + 273, kk / 273, kk - 100], "°C", "T(°C) = T(K) − 273 = %s − 273 = %s °C." % (kk, kk - 273), neg=True)
    if k == "q":
        m, dT = R.choice([(2, 10), (0.5, 20), (1, 50), (3, 5), (0.2, 80), (5, 4)])
        return nq("¿Cuánto calor hace falta para calentar %s kg de agua %s °C? (c = 4180 J/(kg·°C))" % (num(m), dT), m * 4180 * dT, [m * 4180, 4180 * dT, m * dT], "J",
                  "Q = m · c · ΔT = %s · 4180 · %s = %s J." % (num(m), dT, num(m * 4180 * dT)))
    Q, m = R.choice([(41800, 1), (20900, 0.5), (83600, 2), (8360, 0.2), (125400, 3)])
    return nq("Se dan %s J a %s kg de agua. ¿Cuánto sube su temperatura? (c = 4180 J/(kg·°C))" % (num(Q), num(m)), Q / (m * 4180), [Q / 4180, Q * m / 4180, Q / m], "°C",
              "ΔT = Q : (m · c) = %s : (%s · 4180) = %s °C." % (num(Q), num(m), num(Q / (m * 4180))))


def f_onda(R):
    k = R.choice(["rayo", "eco", "luz", "lam", "f"])
    if k == "rayo":
        t = R.choice([2, 3, 5, 1.5, 4, 6])
        return nq("Ves un rayo y oyes el trueno %s s después. ¿A qué distancia cayó? (sonido: 340 m/s)" % num(t), 340 * t, [340 / t, 340 * t * 2, 340 + t], "m",
                  "d = v · t = 340 · %s = %s m." % (num(t), num(340 * t)))
    if k == "eco":
        t = R.choice([2, 1, 3, 0.5, 4])
        return nq("Gritas frente a una montaña y oyes el eco a los %s s. ¿A qué distancia está? (340 m/s)" % num(t), 340 * t / 2, [340 * t, 340 / t, 340 * t * 2], "m",
                  "El sonido va y vuelve: d = 340 · %s : 2 = %s m." % (num(t), num(340 * t / 2)))
    if k == "luz":
        d = R.choice([384000, 150000000, 3000, 300000])
        return nq("¿Cuánto tarda la luz en recorrer %s km? (300 000 km/s)" % num(d), d / 300000, [d * 300000, 300000 / d, d / 3000], "s",
                  "t = d : v = %s : 300 000 = %s s." % (num(d), num(d / 300000)))
    if k == "lam":
        f = R.choice([170, 340, 680, 440, 85, 1700])
        return nq("Un sonido de %s Hz viaja a 340 m/s. ¿Cuál es su longitud de onda?" % f, 340 / f, [340 * f, f / 340, 340 - f], "m", "λ = v : f = 340 : %s = %s m." % (f, num(340 / f)))
    T = R.choice([0.01, 0.002, 0.5, 0.25, 0.001, 0.04])
    return nq("Una onda tiene un periodo de %s s. ¿Cuál es su frecuencia?" % num(T), 1 / T, [T, T * 100, 1 / T / 10], "Hz", "f = 1 : T = 1 : %s = %s Hz." % (num(T), num(1 / T)))


def UNITS(grade):
    return [
        H("F", "magnitudes-y-unidades", "Magnitudes, unidades y el Sistema Internacional", "Magnitudes y unidades",
          "Los alumnos distinguen magnitudes fundamentales y derivadas, usan las unidades del Sistema Internacional, sus múltiplos y submúltiplos, cambian de unidades y expresan resultados en notación científica.",
          "magnitud, unidad, Sistema Internacional, metro, kilogramo, segundo, kelvin, múltiplos y submúltiplos, factores de conversión, notación científica, error",
          "Una medida es un número con su unidad", "En el SI la longitud se mide en metros, la masa en kilogramos y el tiempo en segundos.",
          ["Una magnitud es lo que se puede medir (longitud, masa, tiempo). Las fundamentales del SI son metro, kilogramo, segundo, kelvin, amperio, mol y candela.",
           "Las derivadas se obtienen de las fundamentales: la velocidad (m/s), la superficie (m²) o el volumen (m³).",
           "Para cambiar de unidades se usan factores de conversión: 1 km = 1000 m; 1 h = 3600 s. Los números muy grandes o pequeños se escriben en notación científica."],
          [("Expresa 72 km/h en m/s.", ["72 km/h · 1000 m/km · 1 h/3600 s.", "= 72 : 3,6."], "20 m/s.")],
          [("El kilogramo es una unidad de peso.", "Es de masa; el peso es una fuerza y se mide en newtons."), ("1 m² = 100 cm².", "1 m² = 10 000 cm² porque cada lado tiene 100 cm.")],
          [("¿Qué es la notación científica?", "Escribir un número como una cifra entre 1 y 10 por una potencia de 10, como 3 · 10⁸."), ("¿Por qué hay errores en las medidas?", "Ningún instrumento es perfecto; por eso se repiten y se calcula la media.")],
          [("Unidades del SI", [("longitud", "metro"), ("masa", "kilogramo"), ("tiempo", "segundo"), ("temperatura", "kelvin"), ("intensidad de corriente", "amperio"), ("cantidad de sustancia", "mol"),
                                ("intensidad luminosa", "candela")],
            "¿Cuál es la unidad del SI de: {k}?", "¿Qué magnitud se mide en {v}?", ["litro", "gramo"]),
           ("Prefijos", [("kilo", "mil veces la unidad"), ("hecto", "cien veces la unidad"), ("deca", "diez veces la unidad"), ("deci", "la décima parte"), ("centi", "la centésima parte"),
                         ("mili", "la milésima parte"), ("micro", "la millonésima parte"), ("mega", "un millón de veces la unidad")],
            "¿Qué significa el prefijo {k}?", "¿Qué prefijo significa {v}?"),
           ("Fundamentales y derivadas", {"las magnitudes fundamentales": ["longitud", "masa", "tiempo", "temperatura", "intensidad de corriente", "cantidad de sustancia"],
                                          "las magnitudes derivadas": ["velocidad", "superficie", "volumen", "densidad", "fuerza", "aceleración"]})],
          ["El metro es la unidad de longitud del SI.", "El kilogramo es la unidad de masa.", "La velocidad es una magnitud derivada.", "1 km son 1000 m.", "Mili significa la milésima parte.",
           "1 h son 3600 s.", "La temperatura en el SI se mide en kelvin."],
          [("El kilogramo mide el peso.", "Mide la masa."), ("1 h son 360 s.", "Son 3600 s."), ("La velocidad es fundamental.", "Es derivada."), ("Centi significa cien veces.", "Es la centésima parte."),
           ("El litro es la unidad del SI de volumen.", "Es el metro cúbico.")],
          "las magnitudes y las unidades", "working-scientifically", calc=f_unid),

        H("F", "la-materia-y-sus-propiedades", "La materia: propiedades generales y densidad", "Propiedades de la materia",
          "Los alumnos distinguen propiedades generales (masa, volumen) y características (densidad, puntos de fusión y ebullición, solubilidad), miden volúmenes y calculan densidades.",
          "masa, volumen, propiedad general, propiedad característica, densidad, punto de fusión, punto de ebullición, solubilidad, probeta, balanza",
          "Densidad = masa : volumen", "La densidad es una propiedad característica: sirve para identificar sustancias.",
          ["Las propiedades generales (masa, volumen, temperatura) las tiene toda la materia pero no sirven para identificarla.",
           "Las propiedades características, como la densidad o el punto de fusión, son propias de cada sustancia.", "La densidad se calcula como d = m : V y se expresa en g/cm³ o kg/m³."],
          [("Un anillo de 19,3 g desplaza 1 cm³ de agua. ¿Es de oro? (oro: 19,3 g/cm³)", ["d = 19,3 : 1.", "Coincide con la del oro."], "Sí, puede ser de oro.")],
          [("La densidad depende del tamaño del objeto.", "Un clavo y una viga de hierro tienen la misma densidad."), ("Lo que pesa más es más denso.", "Hay que comparar masa por unidad de volumen.")],
          [("¿Cómo se mide el volumen de un sólido irregular?", "Por desplazamiento de agua en una probeta."), ("¿Por qué el hielo flota?", "Su densidad (0,92 g/cm³) es menor que la del agua.")],
          [("Densidades", [("agua", "1 g/cm³"), ("hielo", "0,92 g/cm³"), ("aceite de oliva", "0,91 g/cm³"), ("aluminio", "2,7 g/cm³"), ("hierro", "7,9 g/cm³"), ("plomo", "11,3 g/cm³"),
                            ("mercurio", "13,6 g/cm³"), ("oro", "19,3 g/cm³"), ("corcho", "0,24 g/cm³")],
            "¿Qué densidad aproximada tiene: {k}?", None),
           ("General o característica", [("masa", "general"), ("volumen", "general"), ("temperatura", "general"), ("longitud", "general"), ("densidad", "característica"), ("punto de fusión", "característica"),
                                         ("punto de ebullición", "característica"), ("solubilidad", "característica"), ("conductividad eléctrica", "característica")],
            "¿Qué tipo de propiedad es: {k}?", None, ["accidental", "biológica"]),
           ("Flota o se hunde en agua", {"las sustancias que flotan en agua": ["corcho", "hielo", "aceite", "madera de pino", "gasolina", "poliestireno expandido"],
                                         "las sustancias que se hunden en agua": ["hierro", "plomo", "aluminio", "vidrio", "mercurio", "piedra"]})],
          ["La densidad es masa entre volumen.", "El hielo es menos denso que el agua.", "La densidad identifica sustancias.", "El oro es más denso que el hierro.", "La masa es una propiedad general.",
           "1 g/cm³ equivale a 1000 kg/m³.", "El volumen de un sólido irregular se mide por desplazamiento."],
          [("La densidad depende del tamaño.", "No depende del tamaño."), ("La masa identifica una sustancia.", "Es general."), ("El hierro flota en agua.", "Se hunde."), ("El hielo es más denso que el agua.", "Es menos denso."),
           ("1 g/cm³ son 100 kg/m³.", "Son 1000 kg/m³.")],
          "la materia", "matter", calc=f_dens),

        H("F", "estados-de-agregacion-y-teoria-cinetica", "Estados de agregación y teoría cinético-molecular", "Estados de agregación",
          "Los alumnos explican las propiedades de sólidos, líquidos y gases con la teoría cinético-molecular, interpretan los cambios de estado y las gráficas de calentamiento y relacionan presión, volumen y temperatura de un gas.",
          "teoría cinético-molecular, sólido, líquido, gas, fusión, vaporización, evaporación, ebullición, condensación, sublimación, gráfica de calentamiento, presión de un gas",
          "Las partículas se mueven más al calentarlas", "Durante un cambio de estado de una sustancia pura la temperatura no cambia.",
          ["Según la teoría cinético-molecular, la materia está formada por partículas en movimiento. En los sólidos vibran en posiciones fijas; en los líquidos se deslizan; en los gases se mueven libres.",
           "Al calentar, las partículas se mueven más deprisa. En una gráfica de calentamiento, los tramos horizontales son cambios de estado.",
           "Un gas encerrado ejerce presión por los choques de sus partículas. Si se calienta a volumen constante, la presión aumenta."],
          [("El agua hierve a 100 °C. Si sigues calentando, ¿sube la temperatura mientras hierve?", ["La energía se usa para separar las partículas.", "Es un cambio de estado de una sustancia pura."], "No, se mantiene en 100 °C.")],
          [("Evaporación y ebullición son lo mismo.", "La evaporación ocurre en la superficie a cualquier temperatura; la ebullición en todo el líquido a una temperatura fija."),
           ("Las partículas de un sólido están quietas.", "Vibran sin cambiar de posición.")],
          [("¿Por qué un globo se encoge en el frigorífico?", "Las partículas se mueven más despacio y chocan menos contra el globo."), ("¿Qué es la sublimación?", "El paso directo de sólido a gas, como el hielo seco.")],
          [("Cambios de estado", [("sólido a líquido", "fusión"), ("líquido a sólido", "solidificación"), ("líquido a gas", "vaporización"), ("gas a líquido", "condensación"), ("sólido a gas", "sublimación"),
                                  ("gas a sólido", "sublimación inversa o deposición")],
            "¿Cómo se llama el cambio de {k}?", "¿Qué cambio de estado es la {v}?", ["dilatación"]),
           ("Teoría cinético-molecular", [("sólido", "partículas muy unidas que solo vibran"), ("líquido", "partículas unidas que se deslizan"), ("gas", "partículas separadas que se mueven libremente"),
                                          ("calentar", "aumenta la velocidad de las partículas"), ("presión de un gas", "choques de las partículas contra las paredes"), ("difusión", "las partículas se mezclan solas")],
            "¿Cómo explica la teoría cinético-molecular: {k}?", D),
           ("Propiedades de los estados", {"las propiedades de los sólidos": ["forma propia", "volumen propio", "no se comprimen", "partículas ordenadas", "no fluyen"],
                                           "las propiedades de los líquidos": ["volumen propio y forma del recipiente", "fluyen", "casi no se comprimen", "superficie horizontal en reposo", "partículas que se deslizan"],
                                           "las propiedades de los gases": ["ocupan todo el recipiente", "se comprimen fácilmente", "se expanden al calentar mucho", "partículas muy separadas", "baja densidad"]})],
          ["Las partículas se mueven más al calentar.", "Los gases se comprimen fácilmente.", "Durante la ebullición del agua pura la temperatura no cambia.", "La sublimación es pasar de sólido a gas.",
           "La presión de un gas se debe a los choques de sus partículas.", "Los líquidos toman la forma del recipiente.", "La evaporación ocurre en la superficie."],
          [("Las partículas de un sólido están quietas.", "Vibran."), ("Evaporación y ebullición son lo mismo.", "Son distintas."), ("La temperatura sube mientras el agua hierve.", "Se mantiene constante."),
           ("Los líquidos se comprimen mucho.", "Casi no se comprimen."), ("La condensación es pasar de líquido a gas.", "Es de gas a líquido.")],
          "los estados de la materia", "matter"),

        H("F", "sustancias-puras-y-mezclas", "Sustancias puras, mezclas y disoluciones", "Mezclas y disoluciones",
          "Los alumnos clasifican la materia en sustancias puras (elementos y compuestos) y mezclas, preparan disoluciones, calculan su concentración y eligen técnicas de separación.",
          "sustancia pura, elemento, compuesto, mezcla homogénea y heterogénea, disolución, soluto, disolvente, concentración g/L, porcentaje en masa, solubilidad, filtración, destilación, cristalización",
          "Concentración = masa de soluto : volumen de disolución", "Una disolución saturada ya no admite más soluto.",
          ["Las sustancias puras son elementos (oxígeno, hierro) o compuestos (agua, sal). Las mezclas pueden ser heterogéneas o homogéneas (disoluciones).",
           "La concentración en g/L es la masa de soluto dividida entre el volumen de disolución. La solubilidad es la máxima cantidad de soluto que se disuelve.",
           "Separación: filtración (sólido y líquido), decantación (líquidos que no se mezclan), destilación (líquidos con distinto punto de ebullición), cristalización (sólido disuelto)."],
          [("Disuelves 10 g de sal en agua hasta 0,5 L. ¿Concentración?", ["c = 10 g : 0,5 L.", "= 20 g/L."], "20 g/L.")],
          [("El agua es una mezcla de hidrógeno y oxígeno.", "Es un compuesto: sus átomos están unidos químicamente."), ("Si añades más soluto, siempre se disuelve.", "Al llegar a la saturación ya no se disuelve más.")],
          [("¿Cómo se separa el alcohol del agua?", "Por destilación, porque hierven a temperaturas distintas."), ("¿La solubilidad cambia con la temperatura?", "Sí; la mayoría de sólidos se disuelven más en caliente.")],
          [("Clasificación", [("oxígeno", "elemento"), ("hierro", "elemento"), ("oro", "elemento"), ("agua", "compuesto"), ("sal común", "compuesto"), ("dióxido de carbono", "compuesto"),
                              ("granito", "mezcla heterogénea"), ("agua y aceite", "mezcla heterogénea"), ("aire", "mezcla homogénea"), ("agua de mar", "mezcla homogénea"), ("bronce", "mezcla homogénea")],
            "¿Qué tipo de materia es: {k}?", None),
           ("Técnicas de separación", [("arena y agua", "filtración"), ("agua y aceite", "decantación con embudo"), ("alcohol y agua", "destilación"), ("sal disuelta en agua", "cristalización"),
                                       ("limaduras de hierro y azufre", "separación magnética"), ("tinta de distintos colores", "cromatografía"), ("piedras de distintos tamaños", "tamizado")],
            "¿Qué técnica separa: {k}?", "¿Qué se separa por {v}?"),
           ("Soluto y disolvente", [("agua azucarada", "soluto: azúcar; disolvente: agua"), ("agua salada", "soluto: sal; disolvente: agua"), ("aire", "disolvente: nitrógeno"),
                                    ("bronce", "soluto: estaño; disolvente: cobre"), ("refresco con gas", "soluto: dióxido de carbono; disolvente: agua"), ("alcohol de farmacia", "soluto: agua; disolvente: etanol")],
            "En la disolución {k}, ¿cuál es el soluto y cuál el disolvente?", None, ["no hay disolvente"])],
          ["El agua es un compuesto.", "El aire es una mezcla homogénea.", "La destilación separa líquidos por su punto de ebullición.", "Una disolución saturada no admite más soluto.", "La filtración separa sólidos de líquidos.",
           "El oxígeno es un elemento.", "La concentración se puede expresar en g/L."],
          [("El agua es una mezcla.", "Es un compuesto."), ("El aire es una sustancia pura.", "Es una mezcla."), ("La filtración separa la sal disuelta.", "La sal pasa el filtro."), ("El bronce es un elemento.", "Es una aleación, una mezcla."),
           ("La concentración es volumen entre masa.", "Es masa de soluto entre volumen de disolución.")],
          "las mezclas y disoluciones", "matter", calc=f_conc),

        H("F", "los-cambios-quimicos", "Los cambios químicos y las reacciones", "Reacciones químicas",
          "Los alumnos distinguen cambios físicos y químicos, reconocen reactivos y productos, aplican la ley de conservación de la masa y relacionan reacciones de la vida diaria y la industria con el medio ambiente.",
          "cambio físico, cambio químico, reacción química, reactivos, productos, ley de Lavoisier, combustión, oxidación, velocidad de reacción, catalizador, efecto invernadero",
          "En una reacción la masa se conserva", "Los reactivos se transforman en productos con propiedades nuevas.",
          ["En un cambio químico unas sustancias (reactivos) se transforman en otras (productos). Se nota por cambios de color, gases, calor o luz.",
           "Ley de Lavoisier: la masa de los reactivos es igual a la masa de los productos.",
           "La velocidad de una reacción aumenta con la temperatura, la concentración, la superficie de contacto y los catalizadores."],
          [("Quemas 12 g de carbono con 32 g de oxígeno. ¿Qué masa de CO₂ se forma?", ["La masa se conserva.", "12 + 32 = 44."], "44 g.")],
          [("Al quemar papel desaparece masa.", "Se forman gases que van al aire; la masa total se conserva."), ("Disolver es un cambio químico.", "Es físico: no se forman sustancias nuevas.")],
          [("¿Por qué la comida dura más en la nevera?", "El frío hace más lentas las reacciones de descomposición."), ("¿Qué es un catalizador?", "Una sustancia que acelera la reacción sin gastarse.")],
          [("¿Físico o químico?", [("fundir hierro", "físico"), ("evaporar alcohol", "físico"), ("disolver azúcar", "físico"), ("romper un vaso", "físico"), ("oxidarse una verja", "químico"),
                                   ("quemar gas butano", "químico"), ("cocer un huevo", "químico"), ("digerir los alimentos", "químico"), ("hacer la fotosíntesis", "químico"), ("agriarse la leche", "químico")],
            "¿Qué tipo de cambio es {k}?", None, ["nuclear", "no es un cambio"]),
           ("Velocidad de reacción", [("calentar la mezcla", "la reacción se acelera"), ("triturar el sólido en polvo", "la reacción se acelera"), ("añadir un catalizador", "la reacción se acelera"),
                                      ("aumentar la concentración", "la reacción se acelera"), ("enfriar los reactivos", "la reacción se frena"), ("diluir con agua", "la reacción se frena"), ("añadir un conservante", "la reacción se frena")],
            "¿Qué ocurre con la velocidad al {k}?", None, ["la masa desaparece", "no se forman productos"]),
           ("Reactivos y productos", [("combustión del metano", "dióxido de carbono y agua"), ("oxidación del hierro", "óxido de hierro"), ("fotosíntesis", "glucosa y oxígeno"), ("respiración celular", "dióxido de carbono, agua y energía"),
                                      ("vinagre con bicarbonato", "dióxido de carbono, agua y una sal"), ("fermentación del mosto", "etanol y dióxido de carbono")],
            "¿Qué productos se forman en: {k}?", "¿Qué reacción produce {v}?")],
          ["En una reacción la masa se conserva.", "Quemar butano es un cambio químico.", "Un catalizador acelera la reacción.", "El frío frena las reacciones.", "La fotosíntesis produce oxígeno.",
           "Fundir hierro es un cambio físico.", "La combustión produce dióxido de carbono."],
          [("La masa desaparece al quemar papel.", "Se conserva."), ("Disolver es un cambio químico.", "Es físico."), ("El catalizador se gasta.", "No se gasta."), ("El calor frena las reacciones.", "Las acelera."),
           ("La fotosíntesis produce dióxido de carbono.", "Produce oxígeno y glucosa.")],
          "los cambios químicos", "matter", calc=f_masa),

        H("F", "el-movimiento", "El movimiento: velocidad y aceleración", "El movimiento",
          "Los alumnos describen el movimiento con sistema de referencia, posición, trayectoria y desplazamiento, calculan velocidades y aceleraciones e interpretan gráficas del movimiento rectilíneo uniforme y uniformemente acelerado.",
          "sistema de referencia, posición, trayectoria, distancia, desplazamiento, rapidez, velocidad media, MRU, aceleración, MRUA, gráficas posición-tiempo y velocidad-tiempo",
          "v = d : t y a = (v − v₀) : t", "En el MRU la velocidad es constante; en el MRUA cambia lo mismo cada segundo.",
          ["Un cuerpo se mueve si cambia su posición respecto a un sistema de referencia. La trayectoria es la línea que dibuja.",
           "La velocidad media es la distancia entre el tiempo. En el MRU la velocidad no cambia y la gráfica posición-tiempo es una recta.",
           "La aceleración indica cuánto cambia la velocidad cada segundo: a = (v − v₀) : t. Si frena, la aceleración es negativa."],
          [("Un ciclista pasa de 2 m/s a 8 m/s en 3 s. ¿Aceleración?", ["a = (8 − 2) : 3.", "= 2 m/s²."], "2 m/s².")],
          [("Distancia y desplazamiento son lo mismo.", "Si das una vuelta completa a la pista, la distancia es 400 m y el desplazamiento 0."), ("Si la velocidad es grande, la aceleración también.", "Un avión a velocidad constante tiene aceleración cero.")],
          [("¿Qué significa una aceleración negativa?", "Que la velocidad disminuye: el móvil frena."), ("¿Cómo es la gráfica v-t de un MRU?", "Una recta horizontal.")],
          [("Conceptos", [("trayectoria", "línea que describe el móvil"), ("desplazamiento", "distancia en línea recta entre la posición inicial y la final"), ("sistema de referencia", "punto desde el que se observa el movimiento"),
                          ("velocidad media", "distancia recorrida entre el tiempo empleado"), ("aceleración", "cambio de la velocidad en cada segundo"), ("MRU", "movimiento rectilíneo con velocidad constante"),
                          ("MRUA", "movimiento rectilíneo con aceleración constante")],
            "¿Qué es: {k}?", D),
           ("Gráficas", [("recta horizontal en una gráfica posición-tiempo", "el móvil está parado"), ("recta inclinada en una gráfica posición-tiempo", "MRU"), ("recta horizontal en una gráfica velocidad-tiempo", "MRU"),
                         ("recta inclinada hacia arriba en velocidad-tiempo", "MRUA que acelera"), ("recta inclinada hacia abajo en velocidad-tiempo", "MRUA que frena"), ("parábola en posición-tiempo", "MRUA")],
            "¿Qué movimiento representa una {k}?", None),
           ("Movimientos cotidianos", [("un tren a velocidad constante en una vía recta", "MRU"), ("una escalera mecánica", "MRU"), ("una cinta transportadora", "MRU"),
                                       ("una piedra que cae", "MRUA"), ("un coche que frena en un semáforo", "MRUA"), ("un avión que despega por la pista", "MRUA"),
                                       ("una noria", "movimiento circular uniforme"), ("las agujas de un reloj", "movimiento circular uniforme"), ("un columpio", "movimiento oscilatorio"),
                                       ("el péndulo de un reloj", "movimiento oscilatorio")],
            "¿Qué tipo de movimiento tiene {k}?", None)],
          ["La velocidad media es distancia entre tiempo.", "En el MRU la velocidad es constante.", "La aceleración se mide en m/s².", "Si un móvil frena su aceleración es negativa.", "El movimiento depende del sistema de referencia.",
           "En el MRUA la velocidad cambia lo mismo cada segundo.", "La trayectoria es la línea que describe el móvil."],
          [("Distancia y desplazamiento son siempre iguales.", "Pueden ser distintos."), ("En el MRU hay aceleración.", "La aceleración es cero."), ("La velocidad se mide en m/s².", "Se mide en m/s."),
           ("Frenar es aceleración positiva.", "Es negativa."), ("El movimiento es absoluto.", "Depende del sistema de referencia.")],
          "el movimiento", "forces-and-motion", calc=f_mov),

        H("F", "las-fuerzas", "Las fuerzas: efectos, peso, muelles y rozamiento", "Las fuerzas",
          "Los alumnos describen los efectos de las fuerzas, las representan como vectores, calculan resultantes, aplican la ley de Hooke, el peso (P = m · g) y analizan el rozamiento y la fuerza gravitatoria.",
          "fuerza, newton, vector, resultante, dinamómetro, ley de Hooke, peso, masa, gravedad, rozamiento, fuerzas a distancia, magnetismo, carga eléctrica",
          "Peso = masa · gravedad", "Una fuerza deforma los cuerpos o cambia su movimiento; se mide en newtons.",
          ["Una fuerza se representa con un vector: tiene módulo, dirección y sentido. Varias fuerzas se suman para dar la resultante.",
           "El peso es la fuerza con que un planeta atrae los cuerpos: P = m · g, con g = 9,8 m/s² en la Tierra.",
           "La ley de Hooke dice que el alargamiento de un muelle es proporcional a la fuerza: F = k · Δx. El rozamiento se opone al movimiento."],
          [("¿Cuánto pesa una mochila de 5 kg?", ["P = m · g.", "5 · 9,8 = 49."], "49 N.")],
          [("Masa y peso son lo mismo.", "La masa no cambia; el peso depende de la gravedad del lugar."), ("Sin fuerza un objeto se para.", "Un objeto en movimiento sigue igual si no hay fuerzas como el rozamiento.")],
          [("¿Qué es un dinamómetro?", "Un muelle calibrado que mide fuerzas en newtons."), ("¿Por qué los neumáticos tienen dibujo?", "Para aumentar el rozamiento con el suelo y no derrapar.")],
          [("Tipos de fuerzas", [("peso", "fuerza a distancia"), ("fuerza magnética", "fuerza a distancia"), ("fuerza eléctrica", "fuerza a distancia"), ("rozamiento", "fuerza de contacto"),
                                 ("tensión de una cuerda", "fuerza de contacto"), ("fuerza normal", "fuerza de contacto"), ("fuerza elástica de un muelle", "fuerza de contacto")],
            "¿De qué tipo es: {k}?", None, ["no es una fuerza", "energía"]),
           ("Conceptos", [("módulo", "valor numérico de la fuerza"), ("dirección", "recta sobre la que actúa la fuerza"), ("sentido", "hacia dónde apunta la fuerza"), ("resultante", "fuerza que equivale a todas juntas"),
                          ("constante elástica", "rigidez de un muelle en N/m"), ("newton", "unidad de fuerza del SI"), ("gravedad", "aceleración con que caen los cuerpos")],
            "¿Qué es: {k}?", D),
           ("Efectos", {"los efectos estáticos de las fuerzas": ["estirar un muelle", "aplastar una lata", "doblar una regla", "comprimir una esponja", "deformar la plastilina"],
                        "los efectos dinámicos de las fuerzas": ["poner en marcha un balón", "frenar una bici", "desviar una pelota", "acelerar un coche", "hacer girar una peonza"]})],
          ["El peso es una fuerza.", "La fuerza se mide en newtons.", "El rozamiento se opone al movimiento.", "El dinamómetro mide fuerzas.", "En la Luna pesamos menos que en la Tierra.",
           "La ley de Hooke relaciona fuerza y alargamiento.", "Una fuerza tiene módulo, dirección y sentido."],
          [("Masa y peso son lo mismo.", "La masa no cambia con el lugar."), ("El peso se mide en kilogramos.", "Se mide en newtons."), ("El rozamiento favorece el movimiento.", "Se opone a él."),
           ("En la Luna la masa disminuye.", "Disminuye el peso."), ("Las fuerzas solo cambian el movimiento.", "También deforman.")],
          "las fuerzas", "forces-and-motion", calc=f_fuer),

        H("F", "la-energia", "La energía: formas, transformaciones y fuentes", "La energía",
          "Los alumnos describen la energía y sus formas (cinética, potencial, química, eléctrica, térmica), su conservación y transformaciones, calculan energía y potencia y comparan fuentes renovables y no renovables.",
          "energía, julio, kilovatio hora, energía cinética, energía potencial, conservación, transformación, degradación, potencia, vatio, renovables, no renovables, eficiencia",
          "La energía se conserva y se transforma", "Ec = ½ · m · v² y Ep = m · g · h.",
          ["La energía es la capacidad de producir cambios. Se mide en julios (J); en las facturas eléctricas, en kilovatios hora (kWh).",
           "La energía cinética depende de la masa y la velocidad; la potencial gravitatoria, de la masa y la altura.",
           "La energía no se crea ni se destruye: se transforma. Siempre se degrada en parte como calor. La potencia es la energía por segundo (vatios)."],
          [("¿Qué energía tiene un libro de 2 kg en una estantería a 1,5 m?", ["Ep = m · g · h.", "2 · 9,8 · 1,5 = 29,4."], "29,4 J.")],
          [("La energía se gasta y desaparece.", "Se transforma; parte se degrada como calor."), ("Potencia y energía son lo mismo.", "La potencia es la energía por unidad de tiempo.")],
          [("¿Qué es un kWh?", "La energía que consume un aparato de 1 kW durante 1 hora: 3 600 000 J."), ("¿Qué energía predomina en la electricidad de España?", "Cada año crece la parte renovable, sobre todo eólica y solar.")],
          [("Formas de energía", [("coche en movimiento", "cinética"), ("agua de un embalse", "potencial gravitatoria"), ("muelle comprimido", "potencial elástica"), ("alimentos y combustibles", "química"),
                                  ("corriente de un enchufe", "eléctrica"), ("agua caliente", "térmica"), ("luz del Sol", "radiante"), ("núcleo del uranio", "nuclear")],
            "¿Qué forma de energía tiene: {k}?", None),
           ("Transformaciones", [("bombilla", "eléctrica en luminosa y térmica"), ("placa fotovoltaica", "radiante en eléctrica"), ("aerogenerador", "cinética del viento en eléctrica"),
                                 ("central hidroeléctrica", "potencial del agua en eléctrica"), ("motor de un coche", "química en cinética"), ("pila", "química en eléctrica"), ("ventilador", "eléctrica en cinética"),
                                 ("frenos de una bici", "cinética en térmica")],
            "¿Qué transformación ocurre en: {k}?", "¿Qué aparato transforma energía {v}?"),
           ("Fuentes", {"las fuentes renovables": ["solar", "eólica", "hidráulica", "biomasa", "geotérmica", "mareomotriz"],
                        "las fuentes no renovables": ["petróleo", "carbón", "gas natural", "uranio", "pizarra bituminosa", "gas de esquisto"]})],
          ["La energía se conserva.", "La energía se mide en julios.", "Un coche en marcha tiene energía cinética.", "La potencia se mide en vatios.", "Parte de la energía se degrada en calor.",
           "El viento es una fuente renovable.", "La pila transforma energía química en eléctrica."],
          [("La energía se destruye.", "Se transforma."), ("La potencia se mide en julios.", "Se mide en vatios."), ("El uranio es renovable.", "No es renovable."), ("La Ep depende de la velocidad.", "Depende de la altura."),
           ("La bombilla transforma luz en electricidad.", "Transforma electricidad en luz y calor.")],
          "la energía", "energy", calc=f_ener),

        H("F", "calor-y-temperatura", "Calor y temperatura", "Calor y temperatura",
          "Los alumnos distinguen calor y temperatura, usan las escalas Celsius y Kelvin, explican el equilibrio térmico, la dilatación y la propagación del calor y calculan el calor con Q = m · c · ΔT.",
          "temperatura, calor, energía térmica, escala Celsius, escala Kelvin, cero absoluto, equilibrio térmico, calor específico, dilatación, conducción, convección, radiación, aislantes",
          "T(K) = T(°C) + 273", "El calor pasa del cuerpo caliente al frío hasta igualar temperaturas.",
          ["La temperatura mide la agitación media de las partículas. El calor es la energía que pasa de un cuerpo a otro por diferencia de temperatura.",
           "En la escala Kelvin el cero es el cero absoluto (−273 °C): T(K) = T(°C) + 273.",
           "El calor para cambiar la temperatura de un cuerpo es Q = m · c · ΔT. Se propaga por conducción, convección y radiación."],
          [("Expresa 27 °C en kelvin.", ["T(K) = T(°C) + 273.", "27 + 273 = 300."], "300 K.")],
          [("El frío pasa a los objetos.", "Es el calor el que sale del objeto caliente."), ("Un abrigo calienta.", "Aísla: impide que perdamos calor.")],
          [("¿Por qué las vías del tren tienen juntas?", "Para que los raíles puedan dilatarse en verano sin deformarse."), ("¿Por qué el mar suaviza el clima?", "El agua tiene un calor específico alto: se calienta y se enfría despacio.")],
          [("Propagación", [("cuchara metálica en la sopa", "conducción"), ("mango de la sartén caliente", "conducción"), ("agua que circula en la olla", "convección"), ("brisa marina", "convección"),
                            ("aire caliente de un radiador que sube", "convección"), ("calor del Sol en la piel", "radiación"), ("calor de una estufa de infrarrojos", "radiación"), ("calor de la hoguera en la cara", "radiación")],
            "¿Cómo se propaga el calor en: {k}?", None, ["dilatación"]),
           ("Conceptos", [("cero absoluto", "temperatura más baja posible, 0 K"), ("equilibrio térmico", "dos cuerpos en contacto llegan a la misma temperatura"), ("calor específico", "energía para subir 1 °C un kilogramo"),
                          ("dilatación", "aumento de tamaño al calentar"), ("termómetro", "instrumento que mide la temperatura"), ("aislante térmico", "material que conduce mal el calor")],
            "¿Qué es: {k}?", D),
           ("Conductores y aislantes", {"los buenos conductores térmicos": ["cobre", "aluminio", "plata", "acero", "hierro"],
                                        "los aislantes térmicos": ["corcho", "lana", "poliestireno", "aire", "madera", "fibra de vidrio"]})],
          ["El calor pasa del cuerpo caliente al frío.", "El cero absoluto es 0 K.", "0 °C son 273 K.", "Los metales conducen bien el calor.", "El Sol calienta por radiación.", "El agua tiene un calor específico alto.",
           "Los cuerpos se dilatan al calentarse."],
          [("El frío pasa a los objetos.", "Pasa el calor."), ("0 °C son 0 K.", "Son 273 K."), ("El abrigo produce calor.", "Aísla."), ("La madera conduce bien el calor.", "Es aislante."),
           ("El Sol calienta por conducción.", "Por radiación.")],
          "el calor y la temperatura", "energy", calc=f_temp),

        H("F", "la-luz-y-el-sonido", "Ondas: la luz y el sonido", "Luz y sonido",
          "Los alumnos describen las ondas y sus magnitudes (amplitud, longitud de onda, frecuencia), el sonido y sus cualidades, la luz, la reflexión, la refracción y el espectro electromagnético.",
          "onda, amplitud, longitud de onda, frecuencia, hercio, sonido, velocidad del sonido, eco, decibelio, luz, reflexión, refracción, espectro electromagnético",
          "Velocidad = longitud de onda · frecuencia", "El sonido necesita un medio; la luz puede viajar por el vacío.",
          ["Una onda transporta energía sin transportar materia. Se describe por su amplitud, su longitud de onda (λ) y su frecuencia (f, en hercios): v = λ · f.",
           "El sonido es una onda mecánica: viaja a unos 340 m/s en el aire y no se propaga en el vacío. Su intensidad se mide en decibelios.",
           "La luz viaja a 300 000 km/s. Se refleja en los espejos y se refracta al cambiar de medio. La luz visible es una parte del espectro electromagnético."],
          [("Una nota de 340 Hz en el aire (340 m/s). ¿Longitud de onda?", ["λ = v : f.", "340 : 340 = 1."], "1 m.")],
          [("El sonido viaja por el espacio.", "En el vacío no hay sonido."), ("Los rayos X no son luz.", "Son ondas electromagnéticas como la luz, pero de mayor energía.")],
          [("¿Qué son los ultrasonidos?", "Sonidos de más de 20 000 Hz que no oímos; se usan en ecografías."), ("¿Por qué vemos el rayo antes de oír el trueno?", "La luz viaja casi un millón de veces más rápido que el sonido.")],
          [("Magnitudes de las ondas", [("amplitud", "altura máxima de la onda"), ("longitud de onda", "distancia entre dos crestas"), ("frecuencia", "número de oscilaciones por segundo"),
                                        ("periodo", "tiempo de una oscilación completa"), ("hercio", "unidad de frecuencia"), ("decibelio", "unidad de intensidad sonora")],
            "¿Qué es: {k}?", D),
           ("Espectro electromagnético", [("ondas de radio", "radio y televisión"), ("microondas", "calentar comida y telefonía"), ("infrarrojos", "mandos a distancia y cámaras térmicas"),
                                          ("luz visible", "ver los colores"), ("ultravioleta", "broncear y esterilizar"), ("rayos X", "radiografías"), ("rayos gamma", "tratamientos contra el cáncer")],
            "¿Para qué se usan: {k}?", "¿Qué radiación se usa para {v}?"),
           ("Fenómenos", [("espejo que devuelve tu imagen", "reflexión de la luz"), ("lápiz que parece roto en el agua", "refracción de la luz"), ("arco iris", "dispersión de la luz"),
                          ("eco en una montaña", "reflexión del sonido"), ("sonar de un barco", "reflexión del sonido"), ("lupa que aumenta", "refracción de la luz"), ("sombra", "propagación rectilínea de la luz")],
            "¿Qué fenómeno ondulatorio es: {k}?", None)],
          ["El sonido no se propaga en el vacío.", "La luz viaja a unos 300 000 km/s.", "La frecuencia se mide en hercios.", "Los rayos X son ondas electromagnéticas.", "El eco es un sonido reflejado.",
           "La refracción ocurre al cambiar de medio.", "Las ondas transportan energía."],
          [("El sonido viaja por el vacío.", "Necesita un medio."), ("El sonido es más rápido que la luz.", "La luz es mucho más rápida."), ("La frecuencia se mide en decibelios.", "Se mide en hercios."),
           ("Las ondas transportan materia.", "Transportan energía."), ("El arco iris se debe a la reflexión.", "Se debe a la dispersión.")],
          "las ondas", "waves-and-light", calc=f_onda),
    ]
